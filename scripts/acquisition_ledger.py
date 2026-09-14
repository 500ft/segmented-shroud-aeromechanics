"""Reconcile existing source routes offline; never manufacture search provenance."""
import argparse, hashlib, json, re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DAY1 = "docs/prior-art-search-2026-09-08.md"
DAY2 = "evidence/task-2026-09-09/database-export.json"
READING = "docs/day3-reading-records.json"
OUTPUT = ROOT / "evidence/task-day3-2026-09-09/acquisition-ledger.json"
# Explicit publisher DOI identity, verified separately; no title-fuzzy deduplication.
ALIASES = {"https://www.sciencedirect.com/science/article/abs/pii/s1270963823007629": "doi:10.1016/j.ast.2023.108866"}
DAY1_ROW = re.compile(r"^\| ([US]\d+) \[([^\]]+)\]\((https?://[^)]+)\) \| ([^|]+) \|", re.M)


def canonical(value):
    value = unquote(value.strip()).lower()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "doi:", ALIASES.get(value, value))
    value = re.sub(r"^https?://arxiv\.org/(?:abs|html|pdf)/", "arxiv:", value).replace("doi:10.48550/arxiv.", "arxiv:")
    return re.sub(r"v\d+$", "", value) if value.startswith("arxiv:") else value


def day1_rows(text):
    rows = [dict(id=i, title=t, url=u, assessment=a.strip()) for i, t, u, a in DAY1_ROW.findall(text)]
    if not rows or len({r["id"] for r in rows}) != len(rows):
        raise ValueError("day-1 evidence table missing or duplicate source IDs")
    return rows


def build(sources, raw, readings=()):
    records = {}

    def record(identifier, title):
        key = canonical(identifier)
        return records.setdefault(key, dict(identifier=key, title=title, screening_status="unscreened",
                                            assessments=[], acquisitions=[]))

    for s in sources:
        row = record(s["url"], s["title"])
        row["screening_status"] = "day1_assessment_available"
        row["assessments"].append(dict(route="day1", source_id=s["id"], reported_assessment=s["assessment"], artifact=DAY1))
        row["acquisitions"].append(dict(route="day1_web_index", retrieved_on="2026-09-08", url=s["url"], query=None,
                                        query_reason="Report lists a query set, not a per-source mapping", artifact=DAY1))
    supported = {(q["db"], q["query"]) for q in raw["query_log"]
                 if q["status"] == "ok" and type(q.get("n")) is int and q["n"] > 0}
    missing = 0
    for index, hit in enumerate(raw["hits"]):
        routes = [dict(**p, query_log_supported=(p["db"], p["query"]) in supported)
                  for p in hit.get("provenance") or [dict(db=hit["db"], query=hit["query"])]]
        ok = any(p["query_log_supported"] for p in routes)
        missing += not ok
        record(hit["id"], hit["title"])["acquisitions"].append(dict(
            route="day2_native_reported", artifact=DAY2, raw_index=index, retrieved_on=raw["retrieved_utc"],
            reported_id=hit["id"], reported_url=hit.get("url"), query_log_supported=ok, queries=routes))
    for reading in readings:
        row = record(reading["url"], reading["title"])
        row["assessments"].append(dict(route="day3", artifact=READING, **reading))
        row["acquisitions"].append(dict(route="day3_targeted_primary_open", retrieved_on=reading["retrieved_on"],
                                        url=reading["url"], access=reading["access"], query=None, artifact=READING))
        if reading["access"] not in {"inaccessible", "metadata_only"}:
            row["screening_status"] = "day3_assessment_available"
    return dict(schema_version=1, count_unit="normalized identifier records, not distinct studies",
                raw_day2_rows=len(raw["hits"]), rows_without_successful_logged_query=missing,
                recall=None, recall_reason="Historical provenance and eligible denominator remain incomplete",
                records=[records[k] for k in sorted(records)])


def render():
    result = build(day1_rows((ROOT / DAY1).read_text()), json.loads((ROOT / DAY2).read_text()),
                   json.loads((ROOT / READING).read_text()))
    result["inputs"] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in (DAY1, DAY2, READING)}
    return json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    text = render()
    if parser.parse_args().check:
        if not OUTPUT.is_file() or OUTPUT.read_text() != text:
            parser.exit(1, "Acquisition ledger missing or stale\n")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, encoding="utf-8")
    print("Acquisition ledger consistent; source provenance gaps remain explicit")


if __name__ == "__main__":
    main()
