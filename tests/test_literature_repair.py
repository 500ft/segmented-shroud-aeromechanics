"""Access status and evidence strength must stay separate, and a failed retrieval is not a finding.

These check the discipline rather than the prose: a source nobody read carries no grade, a
record that names a blocked route says so, and historical evidence files are untouched.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPAIR = ROOT / "docs/reading-records-2026-09-25.json"
DOC = json.loads(REPAIR.read_text())
BY_ID = {r["source_id"]: r for r in DOC["records"]}


class GradingDisciplineTests(unittest.TestCase):
    def test_a_source_that_was_not_read_carries_no_grade(self):
        for sid in ("graf-1998-nonaxisymmetric-clearance", "cui-2023-circumferential-nonuniform"):
            r = BY_ID[sid]
            self.assertIn(r["access"], ("metadata_only", "retrieval_blocked"))
            self.assertIsNone(r["evidence_grade"],
                              "%s was graded without anyone inspecting text" % sid)
            self.assertTrue(r["grade_note"])

    def test_full_text_availability_is_not_an_evidence_grade(self):
        """The Heliyon regrade: one grade A covered both a validated baseline and new predictions."""
        by_claim = BY_ID["heliyon-2024-e25296"]["evidence_grade_by_claim"]
        self.assertEqual(by_claim["baseline_comparison_against_published_experiment"], "B")
        self.assertEqual(by_claim["predictions_for_unmeasured_nonuniform_geometries"], "C")
        self.assertNotEqual(by_claim["baseline_comparison_against_published_experiment"],
                            by_claim["predictions_for_unmeasured_nonuniform_geometries"])

    def test_every_blocked_route_is_recorded_with_its_outcome(self):
        graf = BY_ID["graf-1998-nonaxisymmetric-clearance"]
        outcomes = " ".join(a["outcome"] for a in graf["access_attempts"]).lower()
        self.assertIn("not circumvented", outcomes)
        self.assertIn("prohibited_claims", graf)
        self.assertIn("no absence claim", graf["prohibited_claims"].lower())

    def test_derived_quantities_are_labelled_as_derived(self):
        a = BY_ID["akturk-camci-part1"]
        self.assertIn("derived_here_not_stated_by_the_paper", a)
        self.assertIn("basis", a["derived_here_not_stated_by_the_paper"])
        for q in ("Reynolds number", "Mach number"):
            self.assertIn(q, a["absent"], "%s is derived here and must be listed as absent" % q)

    def test_the_institutional_access_claim_is_withdrawn(self):
        self.assertIn("WITHDRAWN", BY_ID["akturk-camci-part1"]["access_route"])

    def test_conference_and_journal_versions_are_one_study_family(self):
        self.assertIn("one study family",
                      BY_ID["akturk-camci-part1"]["study_family_note"].lower())
        self.assertIn("1998", BY_ID["graf-1998-nonaxisymmetric-clearance"]["publication_date"])


class HistoricalRecordsUntouchedTests(unittest.TestCase):
    def test_the_repair_says_it_supersedes_rather_than_overwrites(self):
        self.assertIn("never by overwriting", DOC["purpose"])

    def test_the_superseded_grade_is_named(self):
        self.assertIn("reading-records-2026-09-21.json", BY_ID["heliyon-2024-e25296"]["regrade"])


class ClaimBoundaryTests(unittest.TestCase):
    def test_no_universal_novelty_claim_survives(self):
        text = (ROOT / "docs/literature/README.md").read_text()
        self.assertIn("frozen 2026-09-25", text)
        self.assertIn("established methods, not contributions of this work", text)


if __name__ == "__main__":
    unittest.main()
