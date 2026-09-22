#!/usr/bin/env python3
"""Build the literature register from every corpus this repository already holds, plus the
thematic extension search.

The register is a CATALOGUE, not a reading. Each entry carries a `read_state` that says exactly
how far it has been taken:

  close_read  a full or sectioned read exists with a locator and per-axis states
  triaged     a disposition exists from the 2026-09-14 top-25 screen, from title or abstract only
  identified  the record was returned by a logged query and nothing more

Ranking signals are retrievable facts, not judgements: the exporter's concept score, the
OpenAlex citation count, and whether the record was already vetted. Importance for this project
is argued in the review text, where a reader can disagree with it.

usage: python scripts/literature_register.py --extension <dir> --out docs/literature/register.json
"""
import argparse, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "evidence/task-2026-09-11-public/database-export.json"
REGISTER = ROOT / "docs/source-eligibility-register.json"
TRIAGE = ROOT / "docs/candidate-screening-2026-09-14.json"
READINGS = [ROOT / "docs/day3-reading-records.json", ROOT / "docs/reading-records-2026-09-21.json"]


def canonical_id(v):
    v = str(v).strip().lower()
    v = re.sub(r"^https?://(?:dx\.)?doi\.org/", "doi:", v)
    v = re.sub(r"^https?://arxiv\.org/(?:abs|pdf)/", "arxiv:", v)
    v = v.replace("doi:10.48550/arxiv.", "arxiv:")
    return re.sub(r"v\d+$", "", v) if v.startswith("arxiv:") else v


def openalex_enrich(ids, pause=0.3):
    """Citation count, venue and type for DOI-bearing records, 50 at a time."""
    out, dois = {}, [i for i in ids if i.startswith("doi:")]
    for k in range(0, len(dois), 50):
        chunk = dois[k:k + 50]
        filt = "doi:" + "|".join(i.split(":", 1)[1] for i in chunk)
        url = ("https://api.openalex.org/works?per-page=50&select=doi,cited_by_count,type,"
               "publication_year,primary_location,title&filter=" + urllib.parse.quote(filt, safe="|:./"))
        try:
            with urllib.request.urlopen(urllib.request.Request(url), timeout=45) as r:
                data = json.loads(r.read())
        except Exception as e:
            print(f"  openalex chunk {k//50}: {type(e).__name__}", file=sys.stderr)
            time.sleep(pause); continue
        for w in data.get("results", []):
            d = (w.get("doi") or "").replace("https://doi.org/", "").lower()
            if not d:
                continue
            loc = (w.get("primary_location") or {}).get("source") or {}
            out["doi:" + d] = dict(cited_by_count=w.get("cited_by_count"),
                                   type=w.get("type"), year=w.get("publication_year"),
                                   venue=loc.get("display_name"))
        time.sleep(pause)
    return out


def load_corpus(extension_dir):
    records, sources = {}, {}

    def add(cid, title, year, url, abstract, score, themes, origin, prov):
        r = records.setdefault(cid, dict(id=cid, title=title or "", year=str(year or ""), url=url or "",
                                         abstract=abstract or "", triage_score=score or 0,
                                         themes=[], origins=[], provenance=[]))
        if title and len(title) > len(r["title"]):
            r["title"] = title
        if abstract and len(abstract) > len(r["abstract"]):
            r["abstract"] = abstract
        r["triage_score"] = max(r["triage_score"], score or 0)
        r["themes"] = sorted(set(r["themes"]) | set(themes or []))
        if origin not in r["origins"]:
            r["origins"].append(origin)
        r["provenance"].extend(prov or [])

    canon = json.loads(CANONICAL.read_text())
    for h in canon["hits"]:
        add(canonical_id(h["id"]), h.get("title"), h.get("year"), h.get("url"), h.get("abstract"),
            h.get("triage_score"), ["frozen_2026_09_09_query_set"], "canonical_export_2026-09-11",
            h.get("provenance"))
    sources["canonical_export_2026-09-11"] = len(canon["hits"])

    ext_path = Path(extension_dir) / "database-export.json"
    ext = json.loads(ext_path.read_text())
    for h in ext["hits"]:
        add(canonical_id(h["id"]), h.get("title"), h.get("year"), h.get("url"), h.get("abstract"),
            h.get("triage_score"), h.get("themes"), "thematic_extension_2026-09-22", h.get("provenance"))
    sources["thematic_extension_2026-09-22"] = len(ext["hits"])

    reg = json.loads(REGISTER.read_text())
    day1 = {}
    for s in reg["sources"]:
        ids = s["identifiers"]
        cid = None
        for d in ids.get("dois", []):
            cid = canonical_id("doi:" + d); break
        if not cid and ids.get("arxiv"):
            cid = canonical_id("arxiv:" + ids["arxiv"])
        if not cid:
            cid = "unresolved:" + s["source_id"]
        day1[cid] = s["source_id"]
        add(cid, s["title"], "", s.get("day1_url"), "", 0, ["day1_screened_set"], "day1_register", [])
    sources["day1_register"] = len(reg["sources"])

    triage = {r["source_id"]: r for r in json.loads(TRIAGE.read_text())["records"]}
    read = {}
    for p in READINGS:
        if not p.is_file():
            continue
        doc = json.loads(p.read_text())
        rows = doc if isinstance(doc, list) else doc.get("records", [])
        for r in rows:
            sid = r.get("source_id", "")
            key = canonical_id(sid) if sid.startswith(("doi:", "arxiv:")) else sid
            if r.get("access") == "inaccessible":
                continue
            read[key] = dict(file=p.name, access=r.get("access"), locator=str(r.get("locator", ""))[:200])
    return records, day1, triage, read, sources, ext


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--extension", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-enrich", action="store_true")
    a = ap.parse_args()

    records, day1, triage, read, sources, ext = load_corpus(a.extension)
    print(f"merged corpus: {len(records)} distinct identifiers from {len(sources)} sources")

    enrich = {} if a.no_enrich else openalex_enrich(sorted(records), )
    print(f"enriched with citation counts: {len(enrich)}")

    for cid, r in records.items():
        e = enrich.get(cid, {})
        r["cited_by_count"] = e.get("cited_by_count")
        r["venue"] = e.get("venue")
        r["type"] = e.get("type")
        if e.get("year") and not r["year"]:
            r["year"] = str(e["year"])
        r["day1_source_id"] = day1.get(cid)
        t = triage.get(cid)
        r["triage_decision"] = t["decision"] if t else None
        rd = read.get(cid) or (read.get(day1.get(cid)) if day1.get(cid) else None)
        r["read_state"] = "close_read" if rd else ("triaged" if t else "identified")
        r["read_locator"] = rd["locator"] if rd else None
        r["read_record"] = rd["file"] if rd else None
        r["provenance_count"] = len(r.pop("provenance", []))

    doc = dict(schema_version=1,
               purpose="Catalogue of every literature record this repository has identified, with how far each has been taken.",
               generated_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               corpora=sources,
               read_states=dict(
                 close_read="a full or sectioned read exists with a locator",
                 triaged="a 2026-09-14 disposition exists, from title or abstract only",
                 identified="returned by a logged query; nothing more"),
               ranking_note=("triage_score is the exporter's concept-term score and cited_by_count is from "
                             "OpenAlex. Both are retrievable signals, not judgements of importance for this "
                             "project; that argument lives in the review text."),
               counts=dict(total=len(records),
                           close_read=sum(1 for r in records.values() if r["read_state"] == "close_read"),
                           triaged=sum(1 for r in records.values() if r["read_state"] == "triaged"),
                           identified=sum(1 for r in records.values() if r["read_state"] == "identified")),
               records=[records[k] for k in sorted(records)])
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print("counts:", json.dumps(doc["counts"]))
    print("wrote", out)


if __name__ == "__main__":
    sys.exit(main())
