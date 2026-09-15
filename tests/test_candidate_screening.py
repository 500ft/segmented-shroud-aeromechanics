"""Completeness and provenance of the 2026-09-14 candidate triage (plan D4).

Structural checks only: every frozen identifier has one reviewed disposition bound to a retained
source by path and hash. Whether an exclusion is justified by its text is a human review (T06)."""
import copy, csv, hashlib, json, shutil, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.reference_coverage import audit_export, AUDIT_KEYS  # noqa: E402

RECORD = ROOT / "docs/candidate-screening-2026-09-14.json"
DECISIONS = {"include_for_close_reading", "exclude_off_topic", "defer_insufficient_evidence"}
BASES = {"title", "abstract_excerpt", "abstract", "full_text"}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def problems(doc, root=ROOT):
    """Every defect as '<id>: <what>' (or 'metadata: <what>'); empty list means the record is complete and bound."""
    out, meta, recs = [], doc.get("metadata", {}), doc.get("records", [])
    csv_path, export_path = root / meta.get("candidate_csv_path", ""), root / meta.get("export_path", "")
    if not csv_path.is_file() or sha256(csv_path) != meta.get("candidate_csv_sha256"):
        out.append("metadata: candidate CSV missing or sha256 differs from the frozen hash")
        return out
    if not export_path.is_file() or sha256(export_path) != meta.get("export_sha256"):
        out.append("metadata: export missing or sha256 differs from the frozen hash")
        return out
    with csv_path.open(newline="", encoding="utf-8") as fh:
        source = {r["id"]: r for r in csv.DictReader(fh)}
    export = json.loads(export_path.read_text())
    audit = audit_export(export)
    if any(audit.get(k) for k in AUDIT_KEYS):
        out.append("metadata: export fails its native-response audit")
    hits = {h["id"]: h for h in export["hits"]}
    frozen, ids = meta.get("candidate_ids", []), [r.get("source_id") for r in recs]
    if list(source) != frozen:
        out.append("metadata: candidate_ids differ from the CSV order")
    if ids != frozen:
        out.append(f"metadata: record ids differ from candidate_ids (count {len(ids)} vs {len(frozen)}; "
                   f"duplicates {sorted({i for i in ids if ids.count(i) > 1})}, missing {sorted(set(frozen) - set(ids))}, "
                   f"foreign {sorted(set(ids) - set(frozen))})")
    for r in recs:
        i, src = r.get("source_id"), source.get(r.get("source_id"))
        if src is None:
            continue
        if r.get("title") != src["title"] or r.get("year") != src["year"] or r.get("triage_score") != int(src["triage_score"]):
            out.append(f"{i}: copied title/year/triage_score differ from the CSV")
        d = r.get("decision")
        if d is None:
            out.append(f"{i}: undecided")
            continue
        if d not in DECISIONS:
            out.append(f"{i}: unrecognised decision {d!r}")
        if not str(r.get("reason", "")).strip():
            out.append(f"{i}: blank reason")
        a = r.get("aboutness")
        if a is not None and not (isinstance(a, int) and 0 <= a <= 3):
            out.append(f"{i}: aboutness must be null or an integer 0-3")
        if r.get("basis") not in BASES:
            out.append(f"{i}: basis must be one of {sorted(BASES)}")
        if not isinstance(r.get("screened_utc"), str) or not r["screened_utc"].endswith("Z") or r["screened_utc"] == export.get("retrieved_utc"):
            out.append(f"{i}: screened_utc must be an actual UTC timestamp, not the acquisition timestamp")
        loc = r.get("locator") or {}
        if not all(isinstance(loc.get(k), str) and loc[k] for k in ("path_or_url", "section", "sha256")):
            out.append(f"{i}: locator needs path_or_url, section and sha256")
        elif not loc["path_or_url"].startswith(("http://", "https://")):
            p = root / loc["path_or_url"]
            if not p.is_file():
                out.append(f"{i}: locator path does not exist")
            elif sha256(p) != loc["sha256"]:
                out.append(f"{i}: locator sha256 differs from the file")
            elif p == export_path:
                field = loc["section"].rsplit(".", 1)[-1]
                if i not in loc["section"] or i not in hits or not hits[i].get(field):
                    out.append(f"{i}: export locator must name this id and a non-empty field; got {loc['section']!r}")
        if not isinstance(r.get("access_attempts"), list):
            out.append(f"{i}: access_attempts must be a list")
        rel = r.get("possible_related_ids")
        if not isinstance(rel, list) or i in rel or not set(rel) <= set(frozen):
            out.append(f"{i}: possible_related_ids must list other frozen ids only")
    return out


def load(path=RECORD):
    return json.loads(Path(path).read_text())


class LiveRecordTests(unittest.TestCase):
    def test_live_record_is_complete_and_bound(self):
        found = problems(load())
        self.assertEqual(found, [], "\n".join(found[:10]))

    def test_metadata_scope_and_rule_commit(self):
        m = load()["metadata"]
        self.assertEqual(m["schema_version"], 1)
        self.assertEqual(m["screening_scope"], "ranked_top_25")
        self.assertEqual(len(m["candidate_ids"]), 25)
        self.assertRegex(m["rule_commit"], r"^[0-9a-f]{40}$")


class CounterexampleTests(unittest.TestCase):
    """Synthetic defects on a copy of the live document; nothing tracked is written."""

    def setUp(self):
        self.doc = load()
        self.first = self.doc["records"][0]["source_id"]
        m = self.doc["metadata"]            # make record 0 a valid disposition so controls do not depend on live completeness
        self.doc["records"][0].update(decision="include_for_close_reading", reason="synthetic control", aboutness=2, basis="title",
                                      locator=dict(path_or_url=m["export_path"], section=f"hits[id={self.first}].title", sha256=m["export_sha256"]),
                                      screened_utc="2026-09-15T00:00:00Z", access_attempts=[], possible_related_ids=[])

    def mutated(self, fn):
        d = copy.deepcopy(self.doc); fn(d); return problems(d)

    def assertRejects(self, fn, needle):
        found = self.mutated(fn)
        self.assertTrue(any(needle in p for p in found), f"expected a problem containing {needle!r}, got {found[:5]}")

    def test_duplicate_id_rejected(self):
        self.assertRejects(lambda d: d["records"].append(copy.deepcopy(d["records"][0])), "duplicates")

    def test_missing_id_rejected(self):
        self.assertRejects(lambda d: d["records"].pop(), "missing")

    def test_substituted_id_rejected(self):
        def sub(d): d["records"][0]["source_id"] = "doi:10.1234/not-in-the-corpus"
        self.assertRejects(sub, "foreign")

    def test_altered_source_bytes_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); m = self.doc["metadata"]
            for key in ("candidate_csv_path", "export_path"):
                (root / m[key]).parent.mkdir(parents=True, exist_ok=True); shutil.copy(ROOT / m[key], root / m[key])
            p = root / m["candidate_csv_path"]; p.write_bytes(p.read_bytes().replace(b"UNSCREENED", b"SCREENED..", 1))
            self.assertTrue(any("sha256 differs" in x for x in problems(self.doc, root)))

    def test_missing_and_foreign_locator_rejected(self):
        def none(d): d["records"][0]["locator"] = {}
        self.assertRejects(none, "locator needs")
        def foreign(d): d["records"][0]["locator"] = dict(path_or_url="docs/prior-art.md", section="x", sha256=sha256(ROOT / "docs/prior-art.md"))
        found = self.mutated(foreign)
        self.assertFalse(any(self.first in p and "locator" in p for p in found), "a local non-export locator with a correct hash is a valid retained-content locator")
        def wrong_field(d): d["records"][0]["locator"]["section"] = f"hits[id={self.first}].no_such_field"
        self.assertRejects(wrong_field, "non-empty field")

    def test_blank_exclusion_reason_and_unknown_decision_rejected(self):
        def blank(d): d["records"][0].update(decision="exclude_off_topic", reason="  ")
        self.assertRejects(blank, "blank reason")
        def unknown(d): d["records"][0]["decision"] = "maybe"
        self.assertRejects(unknown, "unrecognised decision")

    def test_title_based_include_and_deferred_access_failure_accepted(self):
        m = self.doc["metadata"]
        def title_include(d):
            r = d["records"][0]
            r.update(decision="include_for_close_reading", reason="title names the exact measurand", aboutness=None, basis="title",
                     locator=dict(path_or_url=m["export_path"], section=f"hits[id={self.first}].title", sha256=m["export_sha256"]),
                     screened_utc="2026-09-15T00:00:00Z", access_attempts=[], possible_related_ids=[])
        self.assertFalse([p for p in self.mutated(title_include) if p.startswith(self.first)])
        def deferred(d):
            r = d["records"][0]
            r.update(decision="defer_insufficient_evidence", reason="title ambiguous; publisher route returned 403", aboutness=None, basis="title",
                     access_attempts=[dict(utc="2026-09-15T00:00:00Z", url="https://example.invalid/x", route="publisher", outcome="http_403")])
        self.assertFalse([p for p in self.mutated(deferred) if p.startswith(self.first)])


if __name__ == "__main__":
    unittest.main()
