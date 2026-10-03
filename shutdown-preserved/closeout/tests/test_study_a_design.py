"""Behaviour of the Study A candidate design audit.

The point of these is that the design is checked by fitting, not by restating the numbers in
the data file. A manufactured surface is recovered; an effect the design cannot see is shown
to be invisible in training and visible at the holdouts; and defective designs are rejected.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import study_a_design as sad  # noqa: E402

DESIGN = json.loads(sad.DESIGN.read_text())
TOL = 1e-9   # robust: the planning review saw ~2e-15, which is not a requirement


def quad(x, y, z, c):
    return (c[0] + c[1] * x + c[2] * y + c[3] * z + c[4] * x * y + c[5] * x * z
            + c[6] * y * z + c[7] * x * x + c[8] * y * y + c[9] * z * z)


class DesignAuditTests(unittest.TestCase):
    def test_training_design_has_full_rank(self):
        a = sad.audit(DESIGN)
        self.assertTrue(a["full_rank"])
        self.assertEqual(a["rank"], len(sad.TERMS))

    def test_conditioning_is_reported_with_its_convention(self):
        a = sad.audit(DESIGN)
        self.assertGreater(a["condition_number"], 0)
        self.assertTrue(a["scaling_convention"])

    def test_residual_dof_are_not_called_replication(self):
        self.assertIn("not physical replication", sad.audit(DESIGN)["residual_dof_note"])

    def test_generated_document_is_current(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/study_a_design.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)


class RecoveryTests(unittest.TestCase):
    """A design that can be fitted must actually recover a surface that lives in its basis."""

    COEFFS = [0.7, -1.3, 2.1, 0.4, 0.9, -0.6, 1.7, 0.3, -0.8, 1.1]

    def _fit(self, points, values):
        X = sad.model_matrix(points)
        beta, *_ = np.linalg.lstsq(X, np.asarray(values, float), rcond=None)
        return beta

    def test_a_manufactured_quadratic_is_recovered(self):
        train = DESIGN["training"]
        y = [quad(p["x"], p["y"], p["z"], self.COEFFS) for p in train]
        beta = self._fit(train, y)
        np.testing.assert_allclose(beta, self.COEFFS, atol=TOL)

    def test_held_out_points_are_predicted(self):
        train, hold = DESIGN["training"], DESIGN["holdouts"]
        beta = self._fit(train, [quad(p["x"], p["y"], p["z"], self.COEFFS) for p in train])
        pred = sad.model_matrix(hold) @ beta
        truth = [quad(p["x"], p["y"], p["z"], self.COEFFS) for p in hold]
        np.testing.assert_allclose(pred, truth, atol=TOL)

    def test_a_three_way_effect_is_invisible_in_training_and_shows_at_holdouts(self):
        """The design's stated blind spot, demonstrated rather than asserted."""
        train, hold = DESIGN["training"], DESIGN["holdouts"]
        amp = 5.0

        def truth(p):
            return quad(p["x"], p["y"], p["z"], self.COEFFS) + amp * p["x"] * p["y"] * p["z"]

        beta = self._fit(train, [truth(p) for p in train])
        # Training cannot tell the two surfaces apart: the extra column is identically zero there.
        np.testing.assert_allclose(beta, self.COEFFS, atol=TOL)
        residual = sad.model_matrix(train) @ beta - [truth(p) for p in train]
        np.testing.assert_allclose(residual, np.zeros(len(train)), atol=TOL)
        # The reserved holdouts are where it becomes visible.
        err = sad.model_matrix(hold) @ beta - [truth(p) for p in hold]
        worst = float(np.max(np.abs(err)))
        self.assertGreater(worst, 1.0, "holdouts failed to expose an effect training cannot see")
        expected = [amp * abs(p["x"] * p["y"] * p["z"]) for p in hold]
        np.testing.assert_allclose(np.abs(err), expected, atol=TOL)


class DefectiveDesignTests(unittest.TestCase):
    def test_a_rank_deficient_design_is_detected(self):
        bad = dict(DESIGN, training=DESIGN["training"][:9])
        a = sad.audit(bad)
        self.assertFalse(a["full_rank"])

    def test_rank_deficiency_reports_actual_residual_dof_and_infinite_condition(self):
        a = sad.audit(dict(DESIGN, training=DESIGN["training"][:9]))
        self.assertEqual(a["residual_degrees_of_freedom"], a["rows"] - a["rank"])
        self.assertTrue(np.isinf(a["condition_number"]))

    def test_declared_basis_drift_and_nonfinite_rows_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "basis"):
            sad.audit(dict(DESIGN, model_columns=list(reversed(sad.TERMS))))
        points = [dict(p, z=float("nan")) for p in DESIGN["training"]]
        with self.assertRaisesRegex(ValueError, "finite"):
            sad.audit(dict(DESIGN, training=points))

    def test_omitted_terms_are_computed_against_the_declared_basis(self):
        a = sad.audit(DESIGN)
        for term in ("x^3", "y^3", "z^3", "x*y*z"):
            alias = a["omitted_terms"][term]
            self.assertEqual(alias["augmented_rank"], a["rank"])
            self.assertLess(alias["projection_residual_norm"], TOL)
        changed = [dict(p, z=p["z"] + .2 * p["x"] * p["y"])
                   for p in DESIGN["training"]]
        changed_audit = sad.audit(dict(DESIGN, training=changed))
        self.assertGreater(changed_audit["omitted_terms"]["x*y*z"]["projection_residual_norm"], .1)

    def test_a_near_dependent_design_shows_a_large_condition_number(self):
        """Genuine collinearity: z is made a near-copy of y, so the two columns nearly coincide.

        Rank stays full in floating point, which is the point. Rank alone would not warn you;
        the condition number does, and it is what the audit reports.
        """
        nearly = [dict(p, z=p["y"] + 1e-3 * p["z"]) for p in DESIGN["training"]]
        a = sad.audit(dict(DESIGN, training=nearly))
        self.assertTrue(a["full_rank"], "rank alone does not reveal near-dependence")
        self.assertGreater(a["condition_number"],
                           sad.audit(DESIGN)["condition_number"] * 1000)

    def test_rescaling_a_factor_does_not_change_rank(self):
        """Conditioning depends on scaling, so it is reported with a convention; rank does not."""
        scaled = [dict(p, z=p["z"] * 1000.0) for p in DESIGN["training"]]
        a = sad.audit(dict(DESIGN, training=scaled))
        self.assertTrue(a["full_rank"])
        self.assertNotAlmostEqual(a["condition_number"], sad.audit(DESIGN)["condition_number"])


class StatusTests(unittest.TestCase):
    def test_the_design_is_not_presented_as_frozen(self):
        self.assertEqual(DESIGN["status"], "CANDIDATE_DESIGN_AUDITED")
        self.assertTrue(DESIGN["physical_inputs_open"])

    def test_count_and_opening_are_not_independent_factors(self):
        joined = " ".join(DESIGN["limits"]).lower()
        self.assertIn("never be supplied as independent factors", joined)


class PhysicalMappingTests(unittest.TestCase):
    # Synthetic values only; these are not registered study ranges.
    INPUTS = dict(F_low=.01, F_high=.03, s_high=.1, radius=10.,
                  mean_clearance=.2, clearance_margin=.05, minimum_ligament=.5)

    def test_registered_step_has_equal_wall_mean_and_maximum_jump(self):
        for point in DESIGN["training"] + DESIGN["holdouts"]:
            row = sad.physical_mapping(point, self.INPUTS)
            offsets = row["segment_offsets"]
            self.assertAlmostEqual(sum(offsets), 0.)
            self.assertAlmostEqual(max(abs(offsets[i] - offsets[i - 1])
                                       for i in range(len(offsets))), row["s"])
            self.assertAlmostEqual(row["n"] * row["w_radians"] / (2 * np.pi), row["F"])

    def test_valid_and_infeasible_physical_constraints_are_distinguished(self):
        self.assertTrue(sad.constraint_report(DESIGN, self.INPUTS)["feasible"])
        for update in (dict(F_low=.04), dict(s_high=0.), dict(radius=0.),
                       dict(mean_clearance=.01), dict(minimum_ligament=100.)):
            with self.subTest(update=update):
                report = sad.constraint_report(DESIGN, dict(self.INPUTS, **update))
                self.assertFalse(report["feasible"])
                self.assertTrue(report["failures"])
        self.assertIsNone(sad.constraint_report(DESIGN)["feasible"])

    def test_length_units_do_not_change_coded_prediction(self):
        scaled = {key: value if key.startswith("F_") else value * 1000
                  for key, value in self.INPUTS.items()}
        coefficients = RecoveryTests.COEFFS
        for inputs in (self.INPUTS, scaled):
            coded = []
            for p in DESIGN["holdouts"]:
                row = sad.physical_mapping(p, inputs)
                coded.append(dict(x=row["n"] - 3,
                                  y=(2 * row["F"] - inputs["F_low"] - inputs["F_high"])
                                    / (inputs["F_high"] - inputs["F_low"]),
                                  z=2 * row["s"] / inputs["s_high"] - 1))
            np.testing.assert_allclose(sad.model_matrix(coded) @ coefficients,
                                       sad.model_matrix(DESIGN["holdouts"]) @ coefficients,
                                       atol=TOL)


if __name__ == "__main__":
    unittest.main()
