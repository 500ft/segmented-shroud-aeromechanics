"""The 2026-09-21 close-reading record must be honest about what was actually read.

Two failure modes this guards against: an inaccessible source quietly acquiring a per-axis
finding, and a decision recorded without the access attempts that justify it.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/reading-records-2026-09-21.json"
DAY3 = ROOT / "docs/day3-reading-records.json"
STATES = {"disclosed_or_addressed", "not_found_in_inspected", "not_applicable", "unresolved"}
AXES = {"equal_mean_seams", "equal_mean_clearance_discrete_seams", "measured_vs_cfd",
        "deployment_vs_fixed", "matched_controls", "held_out_prediction",
        "generic_segmentation", "guard_validation", "guard_claims"}


def load():
    return json.loads(RECORD.read_text())


class ReadingRecordTests(unittest.TestCase):
    def test_every_record_has_attempts_and_valid_axes(self):
        for r in load()["records"]:
            with self.subTest(source=r["source_id"]):
                self.assertTrue(r["access_attempts"], "a record must show how access was attempted")
                for a in r["access_attempts"]:
                    self.assertTrue(str(a.get("route", "")).strip())
                    self.assertTrue(str(a.get("outcome", "")).strip())
                self.assertEqual(set(r["axis_states"]), AXES)
                for ax, st in r["axis_states"].items():
                    self.assertIn(st, STATES, (r["source_id"], ax))

    def test_inaccessible_sources_resolve_nothing(self):
        """An abstract cannot establish what a full paper does or does not contain."""
        for r in load()["records"]:
            if r["access"] == "inaccessible":
                with self.subTest(source=r["source_id"]):
                    self.assertEqual(set(r["axis_states"].values()), {"unresolved"})
                    self.assertIsNone(r["aboutness"])

    def test_a_read_source_carries_a_locator(self):
        for r in load()["records"]:
            if r["access"] != "inaccessible":
                with self.subTest(source=r["source_id"]):
                    self.assertTrue(str(r["locator"]).strip(),
                                    "a source recorded as read must say what was read")

    def test_day3_file_is_not_extended_by_this_lane(self):
        """The day-3 record feeds the committed coverage record and is bound to exact bytes."""
        day3 = {r["source_id"] for r in json.loads(DAY3.read_text())}
        new = {r["source_id"] for r in load()["records"]}
        self.assertEqual(day3 & new, set(), "new readings must not be merged into the day-3 file")


if __name__ == "__main__":
    unittest.main()
