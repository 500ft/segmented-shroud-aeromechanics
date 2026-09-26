#!/usr/bin/env python3
"""Would a different convergence criterion reclassify any recorded A0.1 case?

Finding F3 of the provenance audit: PLATEAU_REL and PLATEAU_WINDOW are selected values with no
provenance, and together they decide PASS against UNCONVERGED. This answers the open question
registered against them, using only the committed convergence histories. No solver runs.

One limitation governs every number here. The committed histories are DOWNSAMPLED, roughly one
sample per 50 iterations, so the spread measured over a window is a LOWER BOUND on the spread
the full history would show. A case that fails on this data would certainly fail on the full
history; a case that passes here might not. Pass verdicts below are therefore optimistic and
are reported as such.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

SAMPLE_STEP = 50           # iterations between committed samples
PASS, UNCONVERGED, SHORT = "PASS", "UNCONVERGED", "TOO_SHORT_TO_ASSESS"

# (relative tolerance, window in iterations). The first row is the criterion in force.
GRID = [(1.0e-4, 500), (1.0e-3, 500), (1.0e-5, 500),
        (1.0e-4, 250), (1.0e-4, 1000), (1.0e-4, 2000)]


def history(case_dir):
    rows = [l.split() for l in open(os.path.join(case_dir, "convergence.dat"))
            if not l.startswith("#") and l.strip()]
    return [int(r[0]) for r in rows], [float(r[1]) for r in rows]


def classify(values, tol, window_iters):
    """Verdict under one criterion, plus the spread it was judged on.

    A run shorter than the window is TOO_SHORT_TO_ASSESS, which is NOT the same statement as
    'assessed and found unconverged'. Collapsing the two is what hides a terminated run.
    """
    need = max(2, round(window_iters / SAMPLE_STEP))
    if len(values) < need:
        return SHORT, None, len(values), need
    w = values[-need:]
    mean = sum(w) / len(w)
    spread = (max(w) - min(w)) / abs(mean) if mean else float("inf")
    return (PASS if spread <= tol else UNCONVERGED), spread, len(w), need


def run(root="results/generated/cfd/a0.1"):
    out = {"schema_version": 1,
           "question": "Would a different convergence criterion reclassify any recorded A0.1 case?",
           "criterion_in_force": {"relative_tolerance": GRID[0][0], "window_iterations": GRID[0][1]},
           "sample_step_iterations": SAMPLE_STEP,
           "limitation": ("Committed histories are downsampled, so each spread is a LOWER BOUND on "
                          "the full-history spread. PASS verdicts here are optimistic; "
                          "UNCONVERGED and TOO_SHORT_TO_ASSESS verdicts are sound."),
           "cases": {}}
    for d in sorted(glob.glob(os.path.join(root, "*", "convergence.dat"))):
        cd = os.path.dirname(d)
        case = os.path.basename(cd)
        it, cl = history(cd)
        recorded = json.load(open(os.path.join(cd, "case.manifest.json")))["status"]
        entry = {"recorded_status": recorded, "final_iteration": it[-1], "samples": len(it),
                 "under": {}}
        for tol, win in GRID:
            verdict, spread, used, need = classify(cl, tol, win)
            entry["under"]["tol=%g,window=%d" % (tol, win)] = {
                "verdict": verdict, "relative_spread": spread,
                "samples_used": used, "samples_required": need}
        entry["flips_under"] = sorted(
            k for k, v in entry["under"].items()
            if v["verdict"] != PASS and recorded == "PASS")
        out["cases"][case] = entry

    passed = [c for c, e in out["cases"].items() if e["recorded_status"] == "PASS"]
    out["findings"] = {
        "no_case_flips_when_loosened": all(
            out["cases"][c]["under"]["tol=0.001,window=500"]["verdict"] == PASS for c in passed),
        "cases_flipping_at_one_order_tighter": sorted(
            c for c in passed
            if out["cases"][c]["under"]["tol=1e-05,window=500"]["verdict"] != PASS),
        "cases_flipping_on_a_longer_window": sorted(
            c for c in passed
            if out["cases"][c]["under"]["tol=0.0001,window=2000"]["verdict"] != PASS),
        "recorded_unconverged_that_were_never_actually_assessed": sorted(
            c for c, e in out["cases"].items()
            if e["recorded_status"] == "UNCONVERGED"
            and e["under"]["tol=0.0001,window=500"]["verdict"] == SHORT),
    }
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    res = run()
    text = json.dumps(res, indent=2) + "\n"
    if a.out:
        open(a.out, "w").write(text)
        print("wrote", a.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
