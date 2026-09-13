#!/usr/bin/env python3
"""Project-specific clearance-measurement uncertainty budget for Experiment 01 (SSY-R02b).

    python scripts/clearance_uncertainty_budget.py            # print the budget and the Stage A verdict
    python scripts/clearance_uncertainty_budget.py --check    # exit 1 if the committed record is stale

Stage A of docs/experiment-01-rigid-defect-duct.md stops the experiment if measurement uncertainty
is not smaller than the minimum effect of interest. This script is that rule as a computation over
docs/clearance-measurement-budget.csv. Literature values (S5/S6 sensor accuracy) are carried as
`literature_bound` and NEVER enter the combined uncertainty: published sensor resolution does not
establish achievable uncertainty on this rotor and fixture (review 2026-09-12). Only `measured`,
`calibration_record`, `protocol` or `owner_decision` rows are combined. While any term is pending the
verdict is UNRESOLVED and the pending terms are named; nothing is estimated in their place.

Verdicts: INPUTS_PENDING (exit 2) -> STOP_INSTRUMENTATION_REDESIGN (exit 3, k*u >= MEI) -> FEASIBLE (exit 0).
FEASIBLE is a budget verdict only; it authorises no rotor test.
"""
from __future__ import annotations
import argparse, csv, json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/clearance-measurement-budget.csv"
OUT = ROOT / "evidence/task-2026-09-12/clearance-uncertainty-budget.json"
ALLOWED = {"pending", "literature_bound", "measured", "calibration_record", "protocol", "owner_decision"}
COMBINABLE = {"measured", "calibration_record", "protocol", "owner_decision"}
UNCERTAINTY_TERMS = ["sensor_calibration_on_fixture", "rotor_radial_runout", "thermal_growth_at_speed",
                     "fixture_deflection_under_thrust", "seam_setting_repeatability"]
# Required terms, their governing unit, and the evidence states that may satisfy them. A required
# measurement carried at any other state (literature_bound included) is NOT combined and keeps the
# budget unresolved: excluding a term does not make its uncertainty zero (review 2, 2026-09-12).
REQUIRED = {t: ("um", COMBINABLE) for t in UNCERTAINTY_TERMS}
REQUIRED.update({"target_mean_clearance": ("um", COMBINABLE), "minimum_effect_of_interest": ("um", {"protocol", "owner_decision"}),
                 "coverage_factor_k": ("-", {"protocol", "owner_decision"})})
POSITIVE_GOVERNED = {"minimum_effect_of_interest", "coverage_factor_k", "target_mean_clearance"}   # must be finite and > 0
K_RANGE = (1.0, 3.0)                                                                                # governed coverage factor


class BudgetInputError(ValueError):
    pass


def load(path=REGISTER):
    rows = {}
    with Path(path).open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            name, state, raw, src, unit = r["term"].strip(), r["evidence_state"].strip(), r["value"].strip(), r["source"].strip(), r["unit"].strip()
            if name in rows:
                raise BudgetInputError(f"duplicate term {name}; each term may appear once")
            if state not in ALLOWED:
                raise BudgetInputError(f"unsupported evidence_state {state!r} for {name}")
            if name in REQUIRED and unit != REQUIRED[name][0]:
                raise BudgetInputError(f"{name} must be in {REQUIRED[name][0]!r}, got {unit!r}; convert before entering (a value in mm would be read as um)")
            if state == "pending":
                if raw: raise BudgetInputError(f"pending term {name} carries a value; refusing to treat it as measured")
                rows[name] = dict(value=None, unit=r["unit"], state=state, source=src); continue
            if not src: raise BudgetInputError(f"{name} has evidence_state {state!r} but no source")
            try: v = float(raw)
            except ValueError: raise BudgetInputError(f"{name}: non-numeric value {raw!r}")
            if not math.isfinite(v): raise BudgetInputError(f"{name}: value must be finite, got {raw!r}")
            if v < 0: raise BudgetInputError(f"{name}: negative uncertainty term {v}")
            if name in POSITIVE_GOVERNED and v <= 0: raise BudgetInputError(f"{name}: must be > 0, got {v}")
            if name == "coverage_factor_k" and not (K_RANGE[0] <= v <= K_RANGE[1]): raise BudgetInputError(f"coverage_factor_k {v} outside the governed range {K_RANGE}")
            rows[name] = dict(value=v, unit=r["unit"], state=state, source=src)
    missing = [t for t in UNCERTAINTY_TERMS + ["target_mean_clearance", "minimum_effect_of_interest", "coverage_factor_k"] if t not in rows]
    if missing: raise BudgetInputError("terms missing from register: " + ", ".join(missing))
    return rows


def compute(rows):
    pending = [t for t in REQUIRED if rows[t]["state"] == "pending"]
    # A required term at an ineligible evidence state is unresolved, exactly like pending: it is named, never dropped.
    ineligible = [t for t, (unit, states) in REQUIRED.items() if rows[t]["state"] not in states and rows[t]["state"] != "pending"]
    literature_only = [t for t, r in rows.items() if r["state"] == "literature_bound"]
    combined = {t: rows[t]["value"] for t in UNCERTAINTY_TERMS if rows[t]["state"] in COMBINABLE}
    unresolved = pending + ineligible
    u_c = math.sqrt(sum(v * v for v in combined.values())) if (len(combined) == len(UNCERTAINTY_TERMS) and not unresolved) else None
    k = rows["coverage_factor_k"]["value"]; mei = rows["minimum_effect_of_interest"]["value"]
    if unresolved:
        verdict, code = "INPUTS_PENDING", 2
    elif k * u_c >= mei:
        verdict, code = "STOP_INSTRUMENTATION_REDESIGN", 3
    else:
        verdict, code = "FEASIBLE", 0
    return dict(schema_version=2, verdict=verdict, exit_code=code, pending_terms=pending, ineligible_evidence_terms=ineligible,
                literature_bounds_excluded_from_combination=literature_only,
                combined_terms_um=combined, combined_standard_uncertainty_um=u_c,
                coverage_factor_k=k, expanded_uncertainty_um=(k * u_c if u_c is not None else None),
                minimum_effect_of_interest_um=mei, target_mean_clearance_um=rows["target_mean_clearance"]["value"],
                stage_a_rule="k * u_c < minimum_effect_of_interest, else stop for instrumentation redesign",
                note="Budget verdict only. FEASIBLE authorises no rotor test; the experiment's safety controls and SSY-S08 remain separate gates.")


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--check", action="store_true"); ap.add_argument("--register", default=str(REGISTER))
    a = ap.parse_args(argv)
    try:
        res = compute(load(a.register))
    except BudgetInputError as e:
        print("REFUSED INPUTS_UNSUPPORTED:", e, file=sys.stderr); return 2
    if a.check:
        if not OUT.exists(): print("STALE: record missing"); return 1
        old = json.loads(OUT.read_text())
        if old != res: print("STALE: committed budget record differs from recomputation"); return 1
        print("budget record OK:", res["verdict"]); return 0
    if Path(a.register).resolve() == REGISTER.resolve():      # only the committed register updates the committed record
        OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(res, indent=1) + "\n")
    print(f"{res['verdict']}" + (": pending " + ", ".join(res["pending_terms"]) + ("; ineligible evidence: " + ", ".join(res["ineligible_evidence_terms"]) if res["ineligible_evidence_terms"] else "") if res["exit_code"] == 2 else
          f": k*u_c = {res['expanded_uncertainty_um']:.1f} um vs MEI {res['minimum_effect_of_interest_um']:.1f} um"))
    print("literature bounds recorded but NOT combined:", res["literature_bounds_excluded_from_combination"])
    return res["exit_code"] if not a.check else 0


if __name__ == "__main__":
    sys.exit(main())
