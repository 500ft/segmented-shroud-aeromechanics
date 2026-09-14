#!/usr/bin/env python3
"""Reference-coverage reconciliation for the day-1 prior-art set (SSY-R02).

Accounts for EVERY day-1 source: takes its resolved identifiers from
docs/source-eligibility-register.json, decides whether a scholarly-database export could in
principle have returned it, then looks for it in each export under every alias (arXiv id, arXiv
DOI, publisher DOI). Recall is over ELIGIBLE sources only; ineligible sources stay in the output
with their reason. An export is credited only for hits traceable to a logged successful query,
and for NOTHING if it fails the native-response audit (rerun_search.audit_export). Each export's
SHA-256 is recorded, so --check is bound to exact bytes.

usage: python scripts/reference_coverage.py            # print + write evidence JSON
       python scripts/reference_coverage.py --check    # exit 1 if committed JSON is stale
"""
import hashlib, importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/source-eligibility-register.json"
EXPORTS = {"day2_historical": ROOT / "evidence/task-2026-09-09/database-export.json",
           "day4_public":     ROOT / "evidence/task-2026-09-11-public/database-export.json"}
OUT = ROOT / "evidence/task-2026-09-12/reference-coverage.json"
AUDIT_KEYS = ("unsupported_provenance_routes", "missing_request_provenance", "response_record_mismatches",
              "query_count_mismatches", "response_hash_mismatches", "rows_without_successful_logged_query")
ASSESSMENT_STATES = {"disclosed_or_addressed", "not_found_in_inspected", "not_applicable", "unresolved"}
PREVIOUSLY_REPORTED = {"day2_historical": "1 of 6 (anchor set held S1 only; S2, S3, S5 present but uncredited)",
                       "day4_public": "3 of 3 (denominator was the three resolved anchors, not the six eligible sources)"}


def audit_export(export):
    """The export's own native-response audit, reused from the evidence script, not re-implemented."""
    spec = importlib.util.spec_from_file_location("rerun_search", ROOT / "evidence/task-2026-09-09/rerun_search.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.audit_export(export)


def aliases(ids):
    out = {f"doi:{d}".lower() for d in ids.get("dois", [])}
    a = ids.get("arxiv")
    return (out | {f"arxiv:{a}".lower(), f"doi:10.48550/arxiv.{a}".lower()}) if a else out


def export_ids(path):
    """(ids, retrieved_utc, provenance) for one export. ids is empty unless every hit is traceable to a
    logged successful query AND the native audit passes: an export is credited only for what it can show."""
    raw = path.read_bytes(); d = json.loads(raw); hits = d["hits"]
    ok = {(q.get("db"), q.get("query")) for q in d.get("query_log", []) if q.get("status") == "ok"}
    untraceable = [h.get("id") for h in hits if (h.get("db"), h.get("query")) not in ok]
    audit = audit_export(d)
    native = {k: audit.get(k) for k in AUDIT_KEYS}
    failures = {k: v for k, v in native.items() if v}
    clean = not untraceable and not failures
    ids = set()
    if clean:
        for h in hits:
            ids.add(str(h["id"]).lower())
            ids |= {f"{k}:{str(h[k]).lower()}" for k in ("doi", "arxiv") if h.get(k)}
    prov = dict(hits=len(hits), traceable=len(hits) - len(untraceable), untraceable=len(untraceable),
                untraceable_ids_sample=sorted(untraceable)[:10], export_sha256=hashlib.sha256(raw).hexdigest(),
                provenance_clean=clean, native_audit=native, native_audit_passed=not failures, failures=failures)
    return ids, d.get("retrieved_utc"), prov


def novelty_axes():
    """Per axis, per source, the record's EXPLICIT axis_states assessment. Blank, unknown, or without a
    locator (unless already unresolved) -> unresolved. An axis is supported_bounded only if no source
    discloses it AND at least one inspected source records not_found_in_inspected."""
    table = {}
    for r in json.loads((ROOT / "docs/day3-reading-records.json").read_text()):
        states, locator = r.get("axis_states") or {}, str(r.get("locator", ""))
        for ax in sorted(set(states) | set(r.get("axes") or {})):
            st = states.get(ax)
            if st not in ASSESSMENT_STATES or (st != "unresolved" and not locator.strip()):
                st = "unresolved"
            table.setdefault(ax, []).append(dict(source_id=r["source_id"], state=st, access=r.get("access"), locator=locator[:160]))
    summary = {}
    for ax, xs in table.items():
        disc, nf, un = ([x["source_id"] for x in xs if x["state"] == s]
                        for s in ("disclosed_or_addressed", "not_found_in_inspected", "unresolved"))
        summary[ax] = dict(axis_status="narrowed_by_disclosure" if disc else "supported_bounded" if nf else "unresolved",
                           disclosed_by=disc, not_found_in_inspected=nf, unresolved_for=un)
    return dict(summary=summary, detail=table)


def _row(s, exports):
    al, elig = aliases(s["identifiers"]), s["eligible_for_database_export"]
    return dict(source_id=s["source_id"], title=s["title"], eligible=elig, eligibility_reason=s["eligibility_reason"],
                aliases=sorted(al), present={k: bool(al & ids) if elig else None for k, (ids, _, _) in exports.items()})


def compute():
    reg = json.loads(REGISTER.read_text())
    exports = {k: export_ids(p) for k, p in EXPORTS.items()}
    rows = [_row(s, exports) for s in reg["sources"]]
    elig = [r for r in rows if r["eligible"]]
    recall = {k: dict(recovered=sum(bool(r["present"][k]) for r in elig), of_eligible=len(elig),
                      recovered_ids=[r["source_id"] for r in elig if r["present"][k]],
                      missed_ids=[r["source_id"] for r in elig if not r["present"][k]],
                      export_retrieved_utc=utc, provenance=prov)
              for k, (_, utc, prov) in exports.items()}
    clean = [k for k in EXPORTS if exports[k][2]["provenance_clean"]]
    axes = novelty_axes()
    summary = dict(d01_sources=len(rows), eligible=len(elig), not_eligible=len(rows) - len(elig), recall=recall,
                   canonical_export=clean[0] if clean else None, rejected_exports=[k for k in EXPORTS if k not in clean],
                   novelty_axes=axes["summary"], previously_reported=PREVIOUSLY_REPORTED,
                   not_eligible_ids=[r["source_id"] for r in rows if not r["eligible"]])
    return dict(register_version=reg["version"], summary=summary, rows=rows, novelty_axes_detail=axes["detail"])


def main():
    res = compute()
    recall = json.dumps({k: f"{v['recovered']}/{v['of_eligible']}" for k, v in res["summary"]["recall"].items()})
    if "--check" in sys.argv:
        old = json.loads(OUT.read_text()) if OUT.exists() else {}
        if any(old.get(k) != res[k] for k in ("summary", "rows", "novelty_axes_detail")):
            sys.exit("STALE: committed reference-coverage.json missing or differs from recomputation")
        print("reference coverage OK:", recall); return
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(res, indent=1) + "\n")
    print("wrote", OUT.relative_to(ROOT), recall)


if __name__ == "__main__":
    main()
