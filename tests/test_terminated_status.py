"""A run too short to assess is not a run that failed the assessment."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cfd_grid_convergence as gc  # noqa: E402
import status_revision as sr  # noqa: E402

A01 = ROOT / "results/generated/cfd/a0.1"


class ClassifierTests(unittest.TestCase):
    def test_flat_history_of_full_length_passes(self):
        self.assertEqual(gc.assess_status([1.0] * 600)[0], gc.PASS)

    def test_drifting_history_of_full_length_is_unconverged(self):
        self.assertEqual(gc.assess_status([1.0 + 0.01 * i for i in range(600)])[0], gc.UNCONVERGED)

    def test_short_history_is_terminated_not_unconverged(self):
        status, rel = gc.assess_status([0.5, 0.9, 0.7] * 30)     # 90 iterations
        self.assertEqual(status, gc.TERMINATED)
        self.assertIsNone(rel, "no spread may be reported for a window that never closed")

    def test_a_short_history_would_have_failed_the_old_rule_for_the_wrong_reason(self):
        """The regression: the old code judged whatever it had and called wide scatter a failure."""
        wild = [0.5, 0.9, 0.7] * 30
        ok, rel = gc.plateau(wild)
        self.assertFalse(ok)
        self.assertGreater(rel, gc.PLATEAU_REL)
        self.assertEqual(gc.assess_status(wild)[0], gc.TERMINATED)

    def test_the_boundary_is_exactly_one_window(self):
        self.assertEqual(gc.assess_status([1.0] * (gc.PLATEAU_WINDOW - 1))[0], gc.TERMINATED)
        self.assertEqual(gc.assess_status([1.0] * gc.PLATEAU_WINDOW)[0], gc.PASS)

    def test_a_terminated_level_blocks_a_grid_study_like_any_unusable_level(self):
        import cfd_case_manifest as cm
        self.assertIn(gc.TERMINATED, cm.REQUIRED_STATUS)


class RevisionSidecarTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads((A01 / "status-revision-2026-09-29.json").read_text())

    def test_only_the_stalled_case_is_reclassified(self):
        changed = [c for c, e in self.doc["cases"].items() if e["changed"]]
        self.assertEqual(changed, ["g3_SST_a10.12"])
        e = self.doc["cases"]["g3_SST_a10.12"]
        self.assertEqual((e["recorded_status"], e["revised_status"]),
                         ("UNCONVERGED", gc.TERMINATED))
        self.assertLess(e["final_iteration"], e["assessment_window"])

    def test_recorded_manifests_are_untouched_and_pinned_by_hash(self):
        for case, e in self.doc["cases"].items():
            raw = (A01 / case / "case.manifest.json").read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), e["manifest_sha256"], case)
            self.assertEqual(json.loads(raw)["status"], e["recorded_status"], case)

    def test_passing_cases_stay_passing(self):
        for case, e in self.doc["cases"].items():
            if e["recorded_status"] == "PASS":
                self.assertEqual(e["revised_status"], "PASS", case)

    def test_reproducible_from_the_committed_histories(self):
        self.assertEqual(sr.build()["cases"], self.doc["cases"])


if __name__ == "__main__":
    unittest.main()
