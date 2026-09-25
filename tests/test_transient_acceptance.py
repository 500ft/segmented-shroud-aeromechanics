"""The transient acceptance branches, exercised on synthetic inputs before any case is run."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import transient_acceptance as ta  # noqa: E402


class DispositionTests(unittest.TestCase):
    def test_without_a_registered_tolerance_nothing_may_be_decided(self):
        r = ta.disposition(10.0, 10.1, 0.5, tolerance=None)
        self.assertEqual(r["outcome"], ta.NOT_FROZEN)

    def test_agreement_supports_only_the_cases_tested(self):
        r = ta.disposition(10.0, 10.1, 0.5, tolerance=1.0)
        self.assertEqual(r["outcome"], ta.SUPPORTED)
        self.assertIn("cases actually tested", r["reason"])

    def test_a_large_transient_difference_overturns_the_trend(self):
        self.assertEqual(ta.disposition(10.0, 14.0, 0.5, tolerance=1.0)["outcome"], ta.OVERTURNED)

    def test_a_sign_reversal_overturns_it_even_when_small(self):
        r = ta.disposition(0.4, -0.3, 0.05, tolerance=1.0)
        self.assertEqual(r["outcome"], ta.OVERTURNED, "a reversed sign is not agreement")

    def test_an_effect_inside_its_uncertainty_is_unresolved_not_null(self):
        r = ta.disposition(0.2, 0.25, 0.5, tolerance=1.0)
        self.assertEqual(r["outcome"], ta.UNRESOLVED)
        self.assertIn("not evidence of no effect", r["reason"])

    def test_unconverged_numerics_block_any_claim(self):
        for kw in ({"phase_converged": False}, {"time_step_converged": False},
                   {"averaging_converged": False}):
            r = ta.disposition(10.0, 10.1, 0.5, tolerance=1.0, **kw)
            self.assertEqual(r["outcome"], ta.UNRESOLVED, kw)


class PhaseSamplingTests(unittest.TestCase):
    def test_one_level_proves_nothing(self):
        self.assertFalse(ta.phase_sampling_converged({4: 10.0}, 0.1)["converged"])

    def test_refinement_that_still_moves_is_not_converged(self):
        self.assertFalse(ta.phase_sampling_converged({4: 10.0, 8: 10.9}, 0.1)["converged"])

    def test_refinement_that_settles_is_converged(self):
        r = ta.phase_sampling_converged({4: 10.0, 8: 10.5, 16: 10.52}, 0.1)
        self.assertTrue(r["converged"])
        self.assertEqual(r["levels"], [4, 8, 16])


class EnvelopeTests(unittest.TestCase):
    def test_the_envelope_never_claims_to_be_a_bound(self):
        e = ta.sampled_envelope(0.1, 0.2, 0.3)
        self.assertAlmostEqual(e["value"], 0.6)
        self.assertFalse(e["is_a_bound"])
        self.assertIn("not a worst case", e["note"])

    def test_every_component_is_kept_separately(self):
        self.assertEqual(sorted(ta.sampled_envelope(1, 2, 3)["components"]),
                         ["clocking_spread", "model_spread", "u_num"])


if __name__ == "__main__":
    unittest.main()
