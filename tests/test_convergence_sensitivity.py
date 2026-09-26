"""The convergence-criterion sensitivity, and the distinction it exposes.

The substantive check is the last one: a run that stopped before the criterion could be applied
must not be reported as though it had been assessed and failed.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import convergence_sensitivity as cs  # noqa: E402

RECORD = ROOT / "results/generated/cfd/a0.1/convergence-sensitivity-2026-09-26.json"


class ClassifierTests(unittest.TestCase):
    def test_a_flat_history_passes(self):
        v, spread, _, _ = cs.classify([1.0] * 20, 1e-4, 500)
        self.assertEqual(v, cs.PASS)
        self.assertEqual(spread, 0.0)

    def test_a_drifting_history_fails(self):
        v, spread, _, _ = cs.classify([1.0 + 0.01 * i for i in range(20)], 1e-4, 500)
        self.assertEqual(v, cs.UNCONVERGED)
        self.assertGreater(spread, 1e-4)

    def test_a_short_run_is_not_reported_as_unconverged(self):
        """The distinction this whole analysis exists to make."""
        v, spread, used, need = cs.classify([1.0, 2.0, 3.0], 1e-4, 500)
        self.assertEqual(v, cs.SHORT)
        self.assertIsNone(spread, "no spread may be reported for a window that never closed")
        self.assertLess(used, need)


class RecordTests(unittest.TestCase):
    def setUp(self):
        if not RECORD.exists():
            self.skipTest("sensitivity record absent")
        self.doc = json.loads(RECORD.read_text())

    def test_it_is_reproducible_from_the_committed_histories(self):
        self.assertEqual(cs.run()["cases"], self.doc["cases"])

    def test_the_downsampling_limitation_is_stated(self):
        self.assertIn("LOWER BOUND", self.doc["limitation"])

    def test_loosening_the_tolerance_reclassifies_nothing(self):
        self.assertTrue(self.doc["findings"]["no_case_flips_when_loosened"])

    def test_the_criterion_has_less_than_one_order_of_headroom(self):
        """Three of five passing cases fail one order tighter, so the margin is not comfortable."""
        flips = self.doc["findings"]["cases_flipping_at_one_order_tighter"]
        self.assertGreaterEqual(len(flips), 3)
        for case in flips:
            spread = self.doc["cases"][case]["under"]["tol=0.0001,window=500"]["relative_spread"]
            self.assertLess(spread, 1e-4)
            self.assertGreater(spread, 1e-5)

    def test_the_stalled_case_was_never_assessed_rather_than_assessed_and_failed(self):
        never = self.doc["findings"]["recorded_unconverged_that_were_never_actually_assessed"]
        self.assertIn("g3_SST_a10.12", never)
        e = self.doc["cases"]["g3_SST_a10.12"]
        self.assertEqual(e["recorded_status"], "UNCONVERGED")
        self.assertEqual(e["under"]["tol=0.0001,window=500"]["verdict"], cs.SHORT)
        self.assertLess(e["final_iteration"], 500,
                        "this case never reached even one window length")


if __name__ == "__main__":
    unittest.main()
