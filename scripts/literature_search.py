#!/usr/bin/env python3
"""Extend the literature corpus into themes the frozen 2026-09-09 query set never covered.

Reuses evidence/task-2026-09-09/rerun_search.py rather than adding a second searcher, so every
record carries the same provenance the existing exports do: raw response text, response hash,
per-query rank, and a query log that distinguishes an error from a genuine zero.
"""
import importlib.util, json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
spec = importlib.util.spec_from_file_location(
    "rerun_search", REPO / "evidence/task-2026-09-09/rerun_search.py")
rs = importlib.util.module_from_spec(spec); spec.loader.exec_module(rs)

# Themes the project depends on that the frozen query set does not reach.
THEMES = {
 "cfd_validation": [
   "Caradonna Tung hover rotor computational validation",
   "grid convergence index discretization uncertainty CFD",
   "RANS validation ducted fan thrust prediction"],
 "measurement_uncertainty": [
   "thrust stand calibration uncertainty small propeller",
   "measurement system analysis uncertainty propagation experiment"],
 "ducted_fan_uav": [
   "ducted fan VTOL UAV aerodynamic performance experiment",
   "shrouded rotor micro air vehicle static thrust"],
 "guard_and_containment": [
   "rotor guard impact protection unmanned aerial vehicle",
   "propeller blade containment safety cage"],
 "deployable_mechanism": [
   "deployable ring structure self-locking repeatability",
   "folding arm unmanned aerial vehicle deployment repeatability"],
 "defect_aware_modelling": [
   "surrogate model turbomachinery performance prediction validation",
   "held-out validation data-driven model turbomachinery"],
 "clearance_metrology": [
   "blade tip timing clearance measurement uncertainty calibration",
   "eddy current tip clearance sensor turbomachinery"],
 "circumferential_distribution": [
   "circumferential non-uniform tip clearance compressor stall margin",
   "casing treatment circumferential groove tip leakage"],
}

plan, theme_of = [], {}
for theme, queries in THEMES.items():
    for q in queries:
        for db in ("crossref", "openalex"):
            plan.append((db, q)); theme_of[q] = theme

print(f"{len(plan)} query legs across {len(THEMES)} themes", flush=True)
result = rs.collect(plan, {"crossref": rs.crossref, "openalex": rs.openalex, "arxiv": rs.arxiv})
result["protocol_version"] = "2026-09-22-literature-extension"
result["protocol_note"] = ("Additive thematic extension. It does not replace or amend the frozen "
                           "2026-09-09 query set or any existing export.")
result["themes"] = THEMES
for h in result["hits"]:
    h["themes"] = sorted({theme_of[p["query"]] for p in h["provenance"] if p["query"] in theme_of})

out = ROOT / "out"
out.mkdir(exist_ok=True)
rs.write_outputs(out, result)
audit = rs.audit_export(result)
(out / "export-audit.json").write_text(json.dumps(audit, indent=2) + "\n")
ok = sum(1 for q in result["query_log"] if q["status"] == "ok")
print(f"records={result['n_unique']} legs_ok={ok}/{len(result['query_log'])}", flush=True)
print("audit:", {k: audit[k] for k in ("unsupported_provenance_routes", "missing_request_provenance",
      "response_record_mismatches", "query_count_mismatches", "response_hash_mismatches",
      "rows_without_successful_logged_query")}, flush=True)
