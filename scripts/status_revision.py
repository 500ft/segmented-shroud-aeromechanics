#!/usr/bin/env python3
"""Reclassify recorded CFD case statuses under the current rule, without rewriting the records.

The committed manifests are frozen. One of them, the fine-grid k-omega SST case, is recorded
UNCONVERGED although it stopped at iteration 117, before a single 500-iteration assessment
window had elapsed, so the criterion was never applied to it. This writes a dated sidecar that
pins each manifest by hash and states what the current classifier says. Nothing recorded changes.

Iteration count comes from the committed history's final row, which is exact even though the
history itself is downsampled. Only the too-short test needs it, so downsampling does not matter.
"""
import glob
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfd_grid_convergence import PLATEAU_WINDOW, PASS, TERMINATED  # noqa: E402

ROOT = "results/generated/cfd/a0.1"
OUT = os.path.join(ROOT, "status-revision-2026-09-29.json")


def final_iteration(case_dir):
    rows = [l.split() for l in open(os.path.join(case_dir, "convergence.dat"))
            if not l.startswith("#") and l.strip()]
    return int(rows[-1][0])


def build():
    cases = {}
    for m in sorted(glob.glob(os.path.join(ROOT, "*", "case.manifest.json"))):
        d = os.path.dirname(m)
        recorded = json.load(open(m))["status"]
        last = final_iteration(d)
        revised = recorded
        if recorded == "UNCONVERGED" and last < PLATEAU_WINDOW:
            revised = TERMINATED
        cases[os.path.basename(d)] = {
            "manifest_sha256": hashlib.sha256(open(m, "rb").read()).hexdigest(),
            "recorded_status": recorded, "revised_status": revised,
            "final_iteration": last, "assessment_window": PLATEAU_WINDOW,
            "changed": revised != recorded}
    return {"schema_version": 1, "revision_date": "2026-09-29",
            "reason": ("A run shorter than the assessment window cannot be tested against the "
                       "flatness criterion, so UNCONVERGED reports a judgement nobody made. "
                       "Recorded manifests are unchanged; this sidecar reclassifies without rewriting."),
            "cases": cases}


if __name__ == "__main__":
    doc = build()
    open(OUT, "w").write(json.dumps(doc, indent=2) + "\n")
    print("wrote", OUT, "| changed:", [c for c, e in doc["cases"].items() if e["changed"]])
