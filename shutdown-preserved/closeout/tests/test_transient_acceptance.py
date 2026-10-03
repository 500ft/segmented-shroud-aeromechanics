"""The transient acceptance branches, exercised on synthetic inputs before any case is run."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import transient_acceptance as ta  # noqa: E402


def converged_disposition(*args, **kwargs):
    evidence = dict(phase_converged=True, time_step_converged=True, averaging_converged=True)
    evidence.update(kwargs)
    return ta.disposition(*args, **evidence)


class DispositionTests(unittest.TestCase):
    def test_without_a_registered_tolerance_nothing_may_be_decided(self):
        r = ta.disposition(10.0, 10.1, 0.5, tolerance=None)
        self.assertEqual(r["outcome"], ta.NOT_FROZEN)

    def test_agreement_supports_only_the_cases_tested(self):
        r = converged_disposition(10.0, 10.1, 0.5, tolerance=1.0)
        self.assertEqual(r["outcome"], ta.SUPPORTED)
        self.assertIn("cases actually tested", r["reason"])

    def test_a_large_transient_difference_overturns_the_trend(self):
        self.assertEqual(converged_disposition(10.0, 14.0, 0.5, tolerance=1.0)["outcome"], ta.OVERTURNED)

    def test_a_sign_reversal_overturns_it_even_when_small(self):
        r = converged_disposition(0.4, -0.3, 0.05, tolerance=1.0)
        self.assertEqual(r["outcome"], ta.OVERTURNED, "a reversed sign is not agreement")

    def test_an_effect_inside_its_uncertainty_is_unresolved_not_null(self):
        r = converged_disposition(0.2, 0.25, 0.5, tolerance=1.0)
        self.assertEqual(r["outcome"], ta.UNRESOLVED)
        self.assertIn("not evidence of no effect", r["reason"])

    def test_unconverged_numerics_block_any_claim(self):
        for kw in ({"phase_converged": False}, {"time_step_converged": False},
                   {"averaging_converged": False}):
            r = converged_disposition(10.0, 10.1, 0.5, tolerance=1.0, **kw)
            self.assertEqual(r["outcome"], ta.UNRESOLVED, kw)

    def test_missing_convergence_evidence_is_not_assumed_success(self):
        self.assertEqual(ta.disposition(10, 10.1, .5, tolerance=1)["outcome"], ta.UNRESOLVED)

    def test_sign_reversal_inside_sampled_margin_is_unresolved(self):
        self.assertEqual(converged_disposition(.02, -.01, .5, tolerance=1)["outcome"],
                         ta.UNRESOLVED)

    def test_discrepancy_straddling_tolerance_is_unresolved(self):
        self.assertEqual(converged_disposition(10, 11.2, .5, tolerance=1)["outcome"],
                         ta.UNRESOLVED)

    def test_invalid_numbers_cannot_produce_a_scientific_claim(self):
        for invalid in (float("nan"), float("inf"), -float("inf")):
            for field in ("steady_delta", "transient_delta", "uncertainty", "tolerance"):
                values = dict(steady_delta=10, transient_delta=10.1, uncertainty=.5, tolerance=1)
                values[field] = invalid
                with self.subTest(field=field, value=invalid), self.assertRaises(ValueError):
                    converged_disposition(**values)
        for field in ("uncertainty", "tolerance"):
            values = dict(steady_delta=10, transient_delta=10.1, uncertainty=.5, tolerance=1)
            values[field] = -.1
            with self.assertRaises(ValueError):
                converged_disposition(**values)


class PhaseSamplingTests(unittest.TestCase):
    def test_one_level_proves_nothing(self):
        self.assertFalse(ta.phase_sampling_converged({4: 10.0}, 0.1)["converged"])

    def test_refinement_that_still_moves_is_not_converged(self):
        self.assertFalse(ta.phase_sampling_converged({4: 10.0, 8: 10.9}, 0.1)["converged"])

    def test_refinement_that_settles_is_converged(self):
        r = ta.phase_sampling_converged({4: 10.0, 8: 10.5, 16: 10.52}, 0.1,
                                       extrema_by_positions={4: (8, 12), 8: (8, 13), 16: (8, 13.02)})
        self.assertTrue(r["converged"])
        self.assertEqual(r["levels"], [4, 8, 16])

    def test_mean_alone_cannot_prove_extrema_convergence(self):
        self.assertFalse(ta.phase_sampling_converged({4: 10, 8: 10}, .1)["converged"])
        result = ta.phase_sampling_converged({4: 10, 8: 10}, .1,
                                            extrema_by_positions={4: (9, 11), 8: (5, 15)})
        self.assertFalse(result["converged"])

    def test_non_nested_levels_are_rejected(self):
        with self.assertRaises(ValueError):
            ta.phase_sampling_converged({4: 10, 7: 10}, .1)

    def test_unregistered_tolerance_remains_not_frozen(self):
        result = ta.phase_sampling_converged({4: 10, 8: 10}, None)
        self.assertFalse(result["converged"])
        self.assertEqual(result["outcome"], ta.NOT_FROZEN)


class EnvelopeTests(unittest.TestCase):
    def test_the_envelope_never_claims_to_be_a_bound(self):
        e = ta.sampled_envelope(0.1, 0.2, 0.3)
        self.assertAlmostEqual(e["value"], 0.6)
        self.assertFalse(e["is_a_bound"])
        self.assertIn("not a worst case", e["note"])

    def test_every_component_is_kept_separately(self):
        self.assertEqual(sorted(ta.sampled_envelope(1, 2, 3)["components"]),
                         ["clocking_spread", "model_spread", "u_num"])

    def test_invalid_envelope_components_are_rejected(self):
        for invalid in (-1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                ta.sampled_envelope(invalid, .1, .1)


if __name__ == "__main__":
    unittest.main()
