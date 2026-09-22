"""The literature register must not overstate how far any record has been taken.

The register mixes three very different things: sources that were close-read, sources that got a
one-line triage disposition from an abstract, and sources a query merely returned. Collapsing
those is how a catalogue turns into a fake literature review, so the distinction is tested.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/literature/register.json"
TRIAGE = ROOT / "docs/candidate-screening-2026-09-14.json"
STATES = {"close_read", "triaged", "identified"}


def load():
    return json.loads(REGISTER.read_text())


class LiteratureRegisterTests(unittest.TestCase):
    def test_every_record_declares_a_known_read_state(self):
        for r in load()["records"]:
            with self.subTest(id=r["id"]):
                self.assertIn(r["read_state"], STATES)

    def test_a_close_read_record_names_where_it_was_read(self):
        for r in load()["records"]:
            if r["read_state"] == "close_read":
                with self.subTest(id=r["id"]):
                    self.assertTrue(str(r.get("read_locator") or "").strip(),
                                    "a close read must carry a locator")
                    self.assertTrue(str(r.get("read_record") or "").strip(),
                                    "a close read must name the reading record it came from")

    def test_identified_records_claim_nothing(self):
        """A record a query merely returned has no disposition and no reading."""
        for r in load()["records"]:
            if r["read_state"] == "identified":
                with self.subTest(id=r["id"]):
                    self.assertIsNone(r.get("triage_decision"))
                    self.assertIsNone(r.get("read_locator"))

    def test_triaged_state_matches_the_committed_triage_record(self):
        triaged = {x["source_id"] for x in json.loads(TRIAGE.read_text())["records"]}
        for r in load()["records"]:
            if r["read_state"] == "triaged":
                with self.subTest(id=r["id"]):
                    self.assertIn(r["id"], triaged,
                                  "a record may only be marked triaged if the triage record lists it")

    def test_counts_match_the_records(self):
        doc = load()
        recs = doc["records"]
        self.assertEqual(doc["counts"]["total"], len(recs))
        for state in STATES:
            self.assertEqual(doc["counts"][state],
                             sum(1 for r in recs if r["read_state"] == state), state)

    def test_every_record_traces_to_a_logged_query_or_the_day1_screen(self):
        for r in load()["records"]:
            with self.subTest(id=r["id"]):
                self.assertTrue(r["origins"], "a record must say which corpus it came from")
                if r["origins"] == ["day1_register"]:
                    self.assertIsNotNone(r.get("day1_source_id"))
                else:
                    self.assertGreater(r.get("provenance_count", 0), 0,
                                       "a searched record must carry query provenance")


if __name__ == "__main__":
    unittest.main()
