"""The stated basis for the identifiability tolerances, recomputed rather than quoted."""
import math
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import analysis_pipeline as ap  # noqa: E402

N = 24


def relative_residual(cols, k):
    basis = [[1 / math.sqrt(N)] * N]
    for c in cols[:k]:
        res = ap._project_out(c, basis)
        basis.append([x / ap._norm(res) for x in res])
    res = ap._project_out(cols[k], basis)
    return ap._norm(res) / ap._norm(cols[k])


def columns():
    rng = random.Random(0)
    count = [rng.choice([2, 3, 4]) for _ in range(N)]
    total = [c * 5.0 for c in count]                 # exactly count x a fixed width
    return rng, count, total


class CollinearityGapTests(unittest.TestCase):
    def test_an_exactly_dependent_column_sits_near_machine_epsilon(self):
        _, count, total = columns()
        self.assertLess(relative_residual([count, total], 1), 1e-14)

    def test_an_independent_column_sits_far_above_the_threshold(self):
        rng, count, _ = columns()
        ind = [rng.uniform(3, 7) for _ in range(N)]
        self.assertGreater(relative_residual([count, ind], 1), 1e-2)

    def test_the_threshold_lies_inside_that_gap(self):
        rng, count, total = columns()
        low = relative_residual([count, total], 1)
        high = relative_residual([count, [rng.uniform(3, 7) for _ in range(N)]], 1)
        tol = ap.identifiability.__defaults__[1]
        self.assertLess(low, tol)
        self.assertGreater(high, tol)
        self.assertGreater(math.log10(tol / low), 5, "threshold should sit well clear of epsilon")
        self.assertGreater(math.log10(high / tol), 5, "and well clear of a genuine column")

    def test_the_identifiability_check_actually_refuses_the_dependent_column(self):
        _, count, total = columns()
        recs = [{"descriptors": {"seam_count": c, "seam_total_opening_deg": t}}
                for c, t in zip(count, total)]
        rep = ap.identifiability(recs, ["seam_count", "seam_total_opening_deg"])
        self.assertTrue(rep["seam_count"]["identifiable"])
        self.assertFalse(rep["seam_total_opening_deg"]["identifiable"])
        self.assertIn("seam_count", rep["seam_total_opening_deg"]["reason"])


class AbsoluteSpreadUnitTests(unittest.TestCase):
    """The spread tolerance is absolute, so it is safe only while ingestion pins the units."""

    def test_the_same_real_variation_is_kept_in_micrometres_and_refused_in_metres(self):
        tol = ap.identifiability.__defaults__[0]
        one_nm_in_um, one_nm_in_m = 1e-3, 1e-9
        self.assertGreater(one_nm_in_um, tol)
        self.assertLessEqual(one_nm_in_m, tol)

    def test_ingestion_pins_clearance_to_micrometres(self):
        self.assertEqual(ap.REQUIRED_UNITS["c_um"], "um")


if __name__ == "__main__":
    unittest.main()
