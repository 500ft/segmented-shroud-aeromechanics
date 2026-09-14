#!/usr/bin/env python3
"""Project-specific clearance-measurement uncertainty budget for Experiment 01 (SSY-R02b).

    python scripts/clearance_uncertainty_budget.py            # print the budget and the Stage A verdict
    python scripts/clearance_uncertainty_budget.py --check    # exit 1 if the committed record is stale

Stage A of docs/experiment-01-rigid-defect-duct.md stops the experiment if measurement uncertainty
is not smaller than the minimum effect of interest. This script is that rule as a computation over
docs/clearance-measurement-budget.csv. Literature values (S5/S6 sensor accuracy) are carried as
`literature_bound` and NEVER enter the combined uncertainty: published sensor resolution does not
establish achievable uncertainty on this rotor and fixture (review 2026-09-12). Only `measured`,
`calibration_record`, `protocol` or `owner_decision` rows are combined. A required term that is
pending, or carried at an ineligible evidence state, keeps the verdict INPUTS_PENDING and is named:
excluding a term never shrinks u_c (review 2, 2026-09-12).

Verdicts: INPUTS_PENDING (exit 2) -> STOP_INSTRUMENTATION_REDESIGN (exit 3, k*u >= MEI) -> FEASIBLE (exit 0).
FEASIBLE is a budget verdict only; it authorises no rotor test.
"""
import argparse, csv, json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/clearance-measurement-budget.csv"
OUT = ROOT / "evidence/task-2026-09-12/clearance-uncertainty-budget.json"
ALLOWED = {"pending", "literature_bound", "measured", "calibration_record", "protocol", "owner_decision"}
COMBINABLE = {"measured", "calibration_record", "protocol", "owner_decision"}
DECIDED = {"protocol", "owner_decision"}
UNCERTAINTY_TERMS = ["sensor_calibration_on_fixture", "rotor_radial_runout", "thermal_growth_at_speed",
                     "fixture_deflection_under_thrust", "seam_setting_repeatability"]
# Required term -> (governing unit, evidence states that may satisfy it).
REQUIRED = {**{t: ("um", COMBINABLE) for t in UNCERTAINTY_TERMS},
            "target_mean_clearance": ("um", COMBINABLE),
            "minimum_effect_of_interest": ("um", DECIDED),
            "coverage_factor_k": ("-", DECIDED)}
POSITIVE = {"minimum_effect_of_interest", "coverage_factor_k", "target_mean_clearance"}   # finite and > 0
K_RANGE = (1.0, 3.0)                                                                       # governed coverage factor


class BudgetInputError(ValueError):
    pass


def _term(r):
    """Validate one register row; return (name, record). Refuses anything a later reader could misread."""
    name, state, raw, src, unit = (r[k].strip() for k in ("term", "evidence_state", "value", "source", "unit"))
    if state not in ALLOWED:
        raise BudgetInputError(f"unsupported evidence_state {state!r} for {name}")
    if name in REQUIRED and unit != REQUIRED[name][0]:
        raise BudgetInputError(f"{name} must be in {REQUIRED[name][0]!r}, got {unit!r}; convert before entering (a value in mm would be read as um)")
    if state == "pending":
        if raw:
            raise BudgetInputError(f"pending term {name} carries a value; refusing to treat it as measured")
        return name, dict(value=None, unit=r["unit"], state=state, source=src)
    if not src:
        raise BudgetInputError(f"{name} has evidence_state {state!r} but no source")
    try:
        v = float(raw)
    except ValueError:
        raise BudgetInputError(f"{name}: non-numeric value {raw!r}") from None
    if not math.isfinite(v):
        raise BudgetInputError(f"{name}: value must be finite, got {raw!r}")
    if v < 0 or (v == 0 and name in POSITIVE):
        raise BudgetInputError(f"{name}: must be {'> 0' if name in POSITIVE else '>= 0'}, got {v}")
    if name == "coverage_factor_k" and not K_RANGE[0] <= v <= K_RANGE[1]:
        raise BudgetInputError(f"coverage_factor_k {v} outside the governed range {K_RANGE}")
    return name, dict(value=v, unit=r["unit"], state=state, source=src)


def load(path=REGISTER):
    rows = {}
    with Path(path).open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            name, rec = _term(r)
            if name in rows:
                raise BudgetInputError(f"duplicate term {name}; each term may appear once")
            rows[name] = rec
    missing = [t for t in REQUIRED if t not in rows]
    if missing:
        raise BudgetInputError("terms missing from register: " + ", ".join(missing))
    return rows


def compute(rows):
    state = lambda t: rows[t]["state"]
    pending = [t for t in REQUIRED if state(t) == "pending"]
    ineligible = [t for t, (_, ok) in REQUIRED.items() if state(t) != "pending" and state(t) not in ok]
    unresolved = pending + ineligible
    combined = {t: rows[t]["value"] for t in UNCERTAINTY_TERMS if state(t) in COMBINABLE}
    u_c = None if unresolved or len(combined) < len(UNCERTAINTY_TERMS) else math.sqrt(sum(v * v for v in combined.values()))
    k, mei = rows["coverage_factor_k"]["value"], rows["minimum_effect_of_interest"]["value"]
    verdict, code = (("INPUTS_PENDING", 2) if unresolved else
                     ("STOP_INSTRUMENTATION_REDESIGN", 3) if k * u_c >= mei else ("FEASIBLE", 0))
    return dict(schema_version=2, verdict=verdict, exit_code=code, pending_terms=pending, ineligible_evidence_terms=ineligible,
                literature_bounds_excluded_from_combination=[t for t in rows if state(t) == "literature_bound"],
                combined_terms_um=combined, combined_standard_uncertainty_um=u_c,
                coverage_factor_k=k, expanded_uncertainty_um=None if u_c is None else k * u_c,
                minimum_effect_of_interest_um=mei, target_mean_clearance_um=rows["target_mean_clearance"]["value"],
                stage_a_rule="k * u_c < minimum_effect_of_interest, else stop for instrumentation redesign",
                note="Budget verdict only. FEASIBLE authorises no rotor test; the experiment's safety controls and SSY-S08 remain separate gates.")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true"); ap.add_argument("--register", default=str(REGISTER))
    a = ap.parse_args(argv)
    try:
        res = compute(load(a.register))
    except BudgetInputError as e:
        print("REFUSED INPUTS_UNSUPPORTED:", e, file=sys.stderr); return 2
    if a.check:
        if not OUT.exists() or json.loads(OUT.read_text()) != res:
            print("STALE: committed budget record missing or differs from recomputation"); return 1
        print("budget record OK:", res["verdict"]); return 0
    if Path(a.register).resolve() == REGISTER.resolve():      # only the committed register updates the committed record
        OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(res, indent=1) + "\n")
    if res["exit_code"] == 2:
        detail = "pending " + ", ".join(res["pending_terms"])
        if res["ineligible_evidence_terms"]:
            detail += "; ineligible evidence: " + ", ".join(res["ineligible_evidence_terms"])
    else:
        detail = f"k*u_c = {res['expanded_uncertainty_um']:.1f} um vs MEI {res['minimum_effect_of_interest_um']:.1f} um"
    print(f"{res['verdict']}: {detail}")
    print("literature bounds recorded but NOT combined:", res["literature_bounds_excluded_from_combination"])
    return res["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
