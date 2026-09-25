#!/usr/bin/env python3
"""Experiment 01 analysis pipeline (backlog task SSY-05), written before any data exists.

The point of writing it now is that matched-thrust interpolation, harmonic extraction,
repeated-measure handling and held-out selection all involve choices. Made after seeing physical
results, those choices are unfalsifiable. Made here, against synthetic fixtures, they are fixed
and testable.

What it refuses to do is as important as what it computes:

  * it will not read a clearance field in the wrong unit, because millimetres silently read as
    micrometres is a thousand-fold error that still produces a plausible-looking number;
  * it will not invent a clearance inside a seam, where there is no wall and therefore no gap;
  * it will not fit a descriptor that does not vary in the training set, because a coefficient
    that was never estimated cannot be validated by a held-out test;
  * it will not extrapolate to a matched-thrust set-point outside the runs that bracket it;
  * it will not report a relative improvement against a zero baseline error as an infinite gain.

Standard library only, by the repository's dependency rule. The design matrices here are a
handful of columns wide, so normal equations with partial pivoting are accurate enough and avoid
adding a linear-algebra dependency for one solve.

usage: python scripts/analysis_pipeline.py --runs <dir> --matched-thrust 4.0 --holdout-value seam
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

REQUIRED_UNITS = {"c_um": "um", "thrust_N": "N", "voltage_V": "V", "current_A": "A", "rpm": "rpm"}
DESCRIPTORS = ("wall_mean_um", "lobe_amplitude_um", "seam_count", "seam_individual_width_deg",
               "seam_total_opening_deg", "step_um")
TWO_PI = 2.0 * math.pi
AMPLITUDE_EPS = 1e-9


RANK_TOL = 1e-10


class PipelineError(ValueError):
    """An input the pipeline refuses, with the reason stated."""


# --------------------------------------------------------------------------- linear algebra


def solve_normal_equations(x_rows, y):
    """Least-squares coefficients for y ~ X, by SVD rather than by normal equations.

    The name is kept because callers use it. The method is not: forming X'X squares the
    condition number, and this design's predictors span degrees, counts and micrometres, so
    that squaring is not affordable. numpy's least-squares routine is used instead.

    Raises PipelineError when a column carries no independent information, which is the
    identifiability failure the research plan names. Rank is judged on the singular values,
    so a near-dependent column is caught as well as an exactly dependent one.
    """
    n_col = len(x_rows[0])
    if len(x_rows) < n_col:
        raise PipelineError(f"{len(x_rows)} observations cannot identify {n_col} coefficients")
    X = np.asarray(x_rows, dtype=float)
    sv = np.linalg.svd(X, compute_uv=False)
    # Relative threshold: an absolute one would depend on the units of whichever column is
    # largest, which is exactly the mistake this scale of predictor invites.
    if sv[-1] <= sv[0] * RANK_TOL:
        raise PipelineError(
            "design matrix is rank deficient: a predictor carries no independent variation, "
            f"so its coefficient cannot be estimated (smallest singular value {sv[-1]:.3g} "
            f"against largest {sv[0]:.3g})")
    beta, *_ = np.linalg.lstsq(X, np.asarray(y, dtype=float), rcond=None)
    return [float(v) for v in beta]


def predict(coefficients, row):
    return sum(c * v for c, v in zip(coefficients, row))


# --------------------------------------------------------------------------- ingestion


def load_run(path):
    """Read one run record, refusing wrong units and malformed channels."""
    doc = json.loads(Path(path).read_text())
    units = doc.get("units") or {}
    for field, expected in REQUIRED_UNITS.items():
        got = units.get(field)
        if got is None:
            raise PipelineError(f"{Path(path).name}: units['{field}'] is missing; a channel without "
                                "a declared unit cannot be read")
        if got != expected:
            raise PipelineError(f"{Path(path).name}: {field} is declared in {got!r} but this pipeline "
                                f"requires {expected!r}; convert before ingestion rather than "
                                "letting the value be reinterpreted")
    field = doc.get("clearance_field") or {}
    theta, c_vals, mask = field.get("theta_deg"), field.get("c_um"), field.get("wall_mask")
    if not (isinstance(theta, list) and isinstance(c_vals, list) and isinstance(mask, list)):
        raise PipelineError(f"{Path(path).name}: clearance_field needs theta_deg, c_um and wall_mask lists")
    if not len(theta) == len(c_vals) == len(mask):
        raise PipelineError(f"{Path(path).name}: clearance_field arrays differ in length "
                            f"({len(theta)}, {len(c_vals)}, {len(mask)})")
    for i, (walled, value) in enumerate(zip(mask, c_vals)):
        if not walled and value is not None:
            raise PipelineError(f"{Path(path).name}: sample {i} is outside the wall but carries a "
                                "clearance value; a seam has no wall and therefore no clearance")
        if walled and value is None:
            raise PipelineError(f"{Path(path).name}: sample {i} is on the wall but has no clearance value")
    ch = doc.get("channels") or {}
    lengths = {k: len(v) for k, v in ch.items() if isinstance(v, list)}
    if len(set(lengths.values())) > 1:
        raise PipelineError(f"{Path(path).name}: channels are not synchronised, lengths {lengths}")
    return doc


def load_runs(directory):
    paths = sorted(Path(directory).glob("*.json"))
    if not paths:
        raise PipelineError(f"no run records in {directory}")
    return [load_run(p) for p in paths]


# --------------------------------------------------------------------------- descriptors


def wall_domain_mean(theta_deg, c_um, mask):
    """Angle-weighted mean clearance over the wall domain.

    This is NOT the intercept of a harmonic fit. On an incomplete angular domain the basis
    {1, cos2t, sin2t} is not orthogonal to the constant, so the fitted intercept and the wall mean
    are different quantities: on a twelve-point circle carrying 100 + 10*cos(2t) with the samples
    at 0 and 180 degrees removed, the intercept is 100 while the wall mean is 98.

    Quadrature is declared, not implied. Each walled sample is given the midpoint rule's weight,
    half the angular distance to each of its immediate neighbours around the full sample ring.
    Seam edges are therefore resolved only to half the local sample spacing, and that spacing is
    reported so a reader can judge whether it is fine enough for the narrowest seam in the design.
    Non-uniform sampling is handled by construction, since the weights come from actual spacings.
    """
    n = len(theta_deg)
    if n < 2:
        raise PipelineError("a clearance field needs at least two angular samples")
    rad = [math.radians(a) for a in theta_deg]
    total_w, total_wc, walled = 0.0, 0.0, 0
    for i in range(n):
        if not mask[i]:
            continue
        prev_gap = (rad[i] - rad[(i - 1) % n]) % TWO_PI
        next_gap = (rad[(i + 1) % n] - rad[i]) % TWO_PI
        w = (prev_gap + next_gap) / 2.0
        total_w += w
        total_wc += w * c_um[i]
        walled += 1
    if not walled:
        raise PipelineError("no walled samples: the clearance field is entirely seam")
    spacing = TWO_PI / n
    return total_wc / total_w, total_w, spacing


def clearance_descriptors(run):
    """Geometry descriptors over the wall domain only.

    `wall_mean_um` is the integral of the previous function and is the quantity the equal-mean
    comparison is defined on. `harmonic_intercept_um` is the separate fit intercept, kept because
    it describes the underlying profile, and the two are reported side by side precisely because
    they are not interchangeable on a masked domain.
    """
    field = run["clearance_field"]
    theta_deg, c_um, mask = field["theta_deg"], field["c_um"], field["wall_mask"]
    pairs = [(math.radians(t), c) for t, c, w in zip(theta_deg, c_um, mask) if w]
    if len(pairs) < 4:
        raise PipelineError("fewer than four walled samples; the harmonic fit is not identifiable")
    rows = [[1.0, math.cos(2 * t), math.sin(2 * t)] for t, _ in pairs]
    intercept, a, b = solve_normal_equations(rows, [c for _, c in pairs])
    amplitude = math.hypot(a, b)
    mean_um, wall_angle, spacing = wall_domain_mean(theta_deg, c_um, mask)
    occluded = 1.0 - wall_angle / TWO_PI
    cond = run.get("condition") or {}
    n_seams = float(cond.get("n_seams", 0))
    width_deg = float(cond.get("seam_width_deg", 0.0))
    return {
        "wall_mean_um": mean_um,
        "harmonic_intercept_um": intercept,
        "intercept_minus_wall_mean_um": intercept - mean_um,
        "lobe_amplitude_um": amplitude,
        # Phase is meaningless when the amplitude vanishes; None rather than a number from noise.
        "lobe_phase_deg": (math.degrees(math.atan2(b, a)) / 2.0) if amplitude > AMPLITUDE_EPS else None,
        "c_min_um": min(c for _, c in pairs),
        "wall_angle_rad": wall_angle,
        "sample_spacing_deg": math.degrees(spacing),
        "occluded_fraction": occluded,
        "seam_count": n_seams,
        "seam_individual_width_deg": width_deg,
        # Total opening and count are DIFFERENT variables: varying count at fixed individual width
        # also varies the open area, so a count effect and an opening effect are confounded unless
        # the design holds one of them fixed. Both are reported so a contrast can state which.
        "seam_total_opening_deg": n_seams * width_deg,
        "step_um": float(cond.get("step_um", 0.0)),
    }


def run_endpoints(run):
    """Mean thrust and electrical power for one run.

    Power is the mean of the instantaneous product, not the product of the means: with ripple or
    any correlation between voltage and current the two differ, and the protocol requires the
    former unless the difference is shown negligible.
    """
    ch = run["channels"]
    v, i, t = ch["voltage_V"], ch["current_A"], ch["thrust_N"]
    if not v:
        raise PipelineError("empty channels")
    power = sum(a * b for a, b in zip(v, i)) / len(v)
    return dict(thrust_N=sum(t) / len(t), power_W=power,
                rpm=sum(ch["rpm"]) / len(ch["rpm"]) if ch.get("rpm") else None)


# --------------------------------------------------------------------------- matched thrust


def power_at_matched_thrust(points, t_star):
    """Linear interpolation of electrical power to a matched-thrust set-point.

    Refuses to extrapolate. A set-point outside the measured range is reported as unavailable,
    never as a nearest value, because the comparison is defined at matched thrust and a run that
    did not reach it has not made the comparison.
    """
    ordered = sorted(points, key=lambda p: p["thrust_N"])
    lo, hi = ordered[0]["thrust_N"], ordered[-1]["thrust_N"]
    if not lo - 1e-12 <= t_star <= hi + 1e-12:
        raise PipelineError(f"matched-thrust set-point {t_star} N is outside the measured range "
                            f"[{lo}, {hi}]; extrapolation is refused")
    for a, b in zip(ordered, ordered[1:]):
        if a["thrust_N"] <= t_star <= b["thrust_N"]:
            span = b["thrust_N"] - a["thrust_N"]
            if span < 1e-12:
                return (a["power_W"] + b["power_W"]) / 2.0
            f = (t_star - a["thrust_N"]) / span
            return a["power_W"] + f * (b["power_W"] - a["power_W"])
    return ordered[-1]["power_W"]


# --------------------------------------------------------------------------- hierarchy


def group_conditions(runs, t_star):
    """Collapse runs to one matched-thrust endpoint per (specimen, cycle, condition).

    Repeated runs of one condition are repeated measures, not independent specimens, so they are
    averaged within their group and the group is the unit that later enters a fit.
    """
    groups = {}
    for run in runs:
        key = (run["specimen_id"], run.get("deployment_cycle", 0), run["condition"]["family"],
               run["condition"].get("config_group", ""), json.dumps(run["condition"], sort_keys=True))
        groups.setdefault(key, []).append(run)
    out = []
    for (specimen, cycle, family, config_group, _), members in sorted(groups.items()):
        points = [run_endpoints(r) for r in members]
        descriptors = clearance_descriptors(members[0])
        out.append(dict(specimen_id=specimen, deployment_cycle=cycle, family=family,
                        config_group=config_group,
                        n_runs=len(members), descriptors=descriptors,
                        power_at_T_star=power_at_matched_thrust(points, t_star),
                        thrust_range=[min(p["thrust_N"] for p in points),
                                      max(p["thrust_N"] for p in points)]))
    return out


# --------------------------------------------------------------------------- models


def _project_out(column, basis):
    """Residual of `column` after removing its projection onto an orthonormal `basis`."""
    residual = list(column)
    for b in basis:
        dot = sum(x * y for x, y in zip(residual, b))
        residual = [x - dot * y for x, y in zip(residual, b)]
    return residual


def _norm(v):
    return math.sqrt(sum(x * x for x in v))


def identifiability(records, descriptors, tol=1e-9, collinearity_tol=1e-8):
    """Which descriptors can actually carry an estimated coefficient in this training set.

    Two distinct failures, and the second is easy to miss. A descriptor that is constant across
    every training condition has no coefficient to estimate: the research plan's case of a
    seam-only predictor that is zero everywhere in training. But a descriptor can vary and still
    be unidentifiable, if it is a linear combination of descriptors already accepted. Total seam
    width equal to seam count times a fixed width is exactly that: both vary, neither is
    separately estimable, and a solver will either fail or return an arbitrary split between them.

    Columns are tested in order by Gram-Schmidt against the intercept and the descriptors already
    accepted, so the report says which earlier descriptor absorbed the rejected one.
    """
    report, basis, accepted = {}, [], []
    n = len(records)
    intercept = [1.0] * n
    basis.append([x / _norm(intercept) for x in intercept])
    for name in descriptors:
        values = [r["descriptors"][name] for r in records]
        spread = max(values) - min(values)
        if spread <= tol:
            report[name] = dict(spread=spread, identifiable=False,
                                reason="constant across every training condition, so its coefficient "
                                       "cannot be estimated")
            continue
        residual = _project_out(values, basis)
        scale = _norm(values) or 1.0
        if _norm(residual) / scale <= collinearity_tol:
            report[name] = dict(spread=spread, identifiable=False,
                                reason=("a linear combination of the intercept and "
                                        f"{accepted or ['(intercept only)']}, so it carries no "
                                        "independent information and its coefficient is not separately "
                                        "estimable"))
            continue
        report[name] = dict(spread=spread, identifiable=True, reason=None)
        accepted.append(name)
        basis.append([x / _norm(residual) for x in residual])
    return report


def fit(records, descriptors):
    rows = [[1.0] + [r["descriptors"][d] for d in descriptors] for r in records]
    y = [r["power_at_T_star"] for r in records]
    return solve_normal_equations(rows, y)


def evaluate(coefficients, records, descriptors):
    """Prediction error, scored specimen-first.

    The research plan aggregates by independent specimen before averaging. Scoring rows directly
    would let a specimen contributing more cycles or more configurations carry more weight than
    one that contributed fewer, which is weighting by effort rather than by independent unit.
    Both scores are returned so the difference is visible rather than assumed away.

    Relative error is normalised by the observed power at matched thrust, never by the small
    duct-minus-open-rotor difference, which can approach zero and manufacture a huge ratio.
    """
    per_record, by_specimen = [], {}
    for r in records:
        row = [1.0] + [r["descriptors"][d] for d in descriptors]
        observed = r["power_at_T_star"]
        predicted = predict(coefficients, row)
        err = abs(observed - predicted)
        entry = dict(specimen_id=r["specimen_id"], family=r["family"],
                     config_group=r.get("config_group"), observed_W=observed,
                     predicted_W=predicted, abs_error_W=err,
                     rel_error=err / abs(observed) if abs(observed) > 1e-12 else None)
        per_record.append(entry)
        by_specimen.setdefault(r["specimen_id"], []).append(entry)

    specimen_scores = {s: sum(e["abs_error_W"] for e in v) / len(v) for s, v in by_specimen.items()}
    finite = [e["rel_error"] for e in per_record if e["rel_error"] is not None]
    return dict(per_record=per_record,
                per_specimen_abs_error_W=specimen_scores,
                mean_abs_error_W=sum(specimen_scores.values()) / len(specimen_scores),
                row_mean_abs_error_W=sum(e["abs_error_W"] for e in per_record) / len(per_record),
                n_specimens=len(specimen_scores), n_records=len(per_record),
                mean_rel_error=sum(finite) / len(finite) if finite else None)


def holdout(records, value, key="family"):
    """Split on a registered grouping, never at random.

    A random split over rows of the same condition leaks that condition into training and tests
    interpolation dressed as transfer.

    Two routes the research plan allows, and they answer different questions. Holding out a whole
    `family` is the extrapolation challenge: the held-out family's descriptors are then constant in
    training, so the identifiability gate refuses to fit them and the honest verdict is that the
    transfer was not tested. Holding out a registered `config_group` within a family keeps those
    descriptors varying in training and tests prediction inside their support.
    """
    train = [r for r in records if r.get(key) != value]
    test = [r for r in records if r.get(key) == value]
    if not test:
        raise PipelineError(f"no records with {key}={value!r} to hold out")
    if not train:
        raise PipelineError(f"holding out {key}={value!r} leaves no training data")
    return train, test


def classify_outcome(mean_delta, half_width, relative_improvement, relative_error,
                     min_improvement=0.20, max_rel_error=0.10, equivalence_bound=None):
    """Decide the outcome from the effect, its uncertainty and the declared bounds.

    Pure, so every branch can be exercised directly instead of hoping a fixture happens to land
    on it. Three families of answer, and the distinction between the last two is the whole point:

      resolved        the effect is separated from its own uncertainty
      equivalent      the interval fits inside a bound declared in advance
      inconclusive    neither. NOT evidence that the effect is absent.

    `half_width` of None means the uncertainty was never estimated, which cannot yield a resolved
    or an equivalent answer.
    """
    if half_width is None:
        return "INCONCLUSIVE", ("the uncertainty on the improvement was not estimated, so nothing "
                                "is resolved and no equivalence can be claimed")
    if equivalence_bound is not None and abs(mean_delta) + half_width < equivalence_bound:
        return "PRACTICALLY_EQUIVALENT", (
            f"the improvement interval {mean_delta:.4g} +/- {half_width:.4g} lies entirely inside "
            f"the declared equivalence bound of {equivalence_bound:.4g}")
    if abs(mean_delta) <= half_width:
        return "INCONCLUSIVE", (
            f"the improvement {mean_delta:.4g} is not separated from its own uncertainty "
            f"{half_width:.4g}, so the effect is unresolved. This is NOT evidence that seam "
            "topology is unimportant.")
    if mean_delta <= 0:
        return "NO_IMPROVEMENT", (
            f"the defect-aware model is resolvably worse on held-out data by {-mean_delta:.4g} W, "
            "which is what over-fitting a descriptor set to training scatter looks like")
    if relative_improvement < min_improvement:
        return "RESOLVED_BELOW_GATE", (
            f"a resolved improvement of {relative_improvement:.3g}, below the registered gate of "
            f"{min_improvement:.2f}")
    if relative_error is not None and relative_error > max_rel_error:
        return "IMPROVED_BUT_ERROR_TOO_HIGH", (
            f"relative improvement {relative_improvement:.3g} clears the gate, but held-out "
            f"relative error {relative_error:.3g} exceeds the maximum {max_rel_error:.2f}")
    return "DEFECT_AWARE_BETTER", (
        f"a resolved relative improvement of {relative_improvement:.3g} at relative error "
        f"{relative_error:.3g}")


def compare_models(records, holdout_value, descriptors=DESCRIPTORS, holdout_key="family",
                   min_improvement=0.20, max_rel_error=0.10, equivalence_bound_W=None,
                   coverage_k=2.0):
    """Mean-clearance baseline against a defect-aware model on a registered holdout.

    The baseline adapts to the design rather than assuming one. The experiment this project
    proposes holds mean clearance EQUAL across conditions by construction, so a baseline of
    intercept plus mean clearance is rank-deficient exactly when the intended comparison is run.
    Where mean clearance does not vary in training, the baseline is intercept-only, which is the
    correct null for an equal-mean design: it says every equal-mean condition draws the same power.
    A clearance slope is only fitted where real clearance variation supports it, never from
    metrology scatter about one target.

    Three outcomes, not two. An effect that cannot be separated from its own uncertainty is
    INCONCLUSIVE, not evidence that topology does not matter. Practical equivalence is claimed
    only against a bound declared in advance, and only when the interval fits inside it.
    """
    train, test = holdout(records, holdout_value, holdout_key)
    ident = identifiability(train, descriptors)
    usable = [d for d in descriptors if ident[d]["identifiable"]]
    refused = [d for d in descriptors if not ident[d]["identifiable"]]

    shared = sorted({r["specimen_id"] for r in train} & {r["specimen_id"] for r in test})
    if "wall_mean_um" in usable:
        baseline_desc, baseline_form = ["wall_mean_um"], "intercept_plus_wall_mean"
    else:
        baseline_desc, baseline_form = [], "intercept_only"
    baseline = fit(train, baseline_desc)
    baseline_eval = evaluate(baseline, test, baseline_desc)

    result = dict(holdout_key=holdout_key, holdout_value=holdout_value,
                  n_train=len(train), n_test=len(test),
                  specimens_on_both_sides=shared,
                  split_is_specimen_disjoint=not shared,
                  identifiability=ident, descriptors_used=usable, descriptors_refused=refused,
                  baseline=dict(descriptors=baseline_desc, form=baseline_form,
                                coefficients=baseline, **baseline_eval),
                  gate=dict(min_relative_improvement=min_improvement,
                            max_relative_error=max_rel_error,
                            equivalence_bound_W=equivalence_bound_W, coverage_k=coverage_k,
                            source="ROADMAP.md Stage 2 gates; provisional engineering choices, "
                                   "not prospectively confirmed acceptance criteria"))

    aware_desc = [d for d in usable if d not in baseline_desc]
    if not aware_desc:
        result["defect_aware"] = None
        result["verdict"] = "NOT_IDENTIFIABLE"
        result["verdict_reason"] = (
            "no defect descriptor is identifiable in the training set beyond the baseline, so the "
            "defect-aware model was not fitted. This is a reportable outcome about the design, not "
            "a result about seam topology.")
        return result

    aware = fit(train, usable)
    aware_eval = evaluate(aware, test, usable)
    result["defect_aware"] = dict(descriptors=usable, coefficients=aware, **aware_eval)

    # Uncertainty on the improvement, from the spread across independent specimens.
    b_by, a_by = baseline_eval["per_specimen_abs_error_W"], aware_eval["per_specimen_abs_error_W"]
    deltas = [b_by[s] - a_by[s] for s in sorted(b_by)]
    n = len(deltas)
    mean_delta = sum(deltas) / n
    if n > 1:
        var = sum((d - mean_delta) ** 2 for d in deltas) / (n - 1)
        se = math.sqrt(var / n)
    else:
        se = None
    half_width = coverage_k * se if se is not None else None
    result["improvement_W"] = dict(mean=mean_delta, standard_error=se, n_specimens=n,
                                   half_width=half_width,
                                   note="uncertainty from the spread across independent specimens; "
                                        "with one specimen it is unestimated, not zero")

    b, a = baseline_eval["mean_abs_error_W"], aware_eval["mean_abs_error_W"]
    rel = aware_eval["mean_rel_error"]
    if b <= 1e-12:
        result["relative_improvement"] = None
        result["verdict"] = "BASELINE_EXACT"
        result["verdict_reason"] = ("the baseline has zero held-out error, so relative improvement "
                                    "is undefined rather than infinite.")
        return result

    improvement = (b - a) / b
    result["relative_improvement"] = improvement

    result["verdict"], result["verdict_reason"] = classify_outcome(
        mean_delta, half_width, improvement, rel,
        min_improvement=min_improvement, max_rel_error=max_rel_error,
        equivalence_bound=equivalence_bound_W)
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--matched-thrust", type=float, required=True)
    ap.add_argument("--holdout-value", required=True)
    ap.add_argument("--holdout-key", default="family",
                    choices=["family", "config_group", "specimen_id"])
    ap.add_argument("--equivalence-bound-W", type=float, default=None)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    try:
        records = group_conditions(load_runs(a.runs), a.matched_thrust)
        result = compare_models(records, a.holdout_value, holdout_key=a.holdout_key,
                                equivalence_bound_W=a.equivalence_bound_W)
    except PipelineError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2
    result["evidence_state"] = "derived from the inputs supplied; this pipeline establishes no measurement"
    text = json.dumps(result, indent=1)
    if a.out:
        Path(a.out).write_text(text + "\n")
    print(json.dumps({k: result[k] for k in ("holdout_key", "holdout_value", "n_train", "n_test",
                                             "split_is_specimen_disjoint", "verdict",
                                             "descriptors_used", "descriptors_refused")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
