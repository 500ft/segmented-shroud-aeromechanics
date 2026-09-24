"""The Experiment 01 analysis pipeline, tested against synthetic fixtures before any data exists.

Every fixture has a closed-form answer, so these tests distinguish a pipeline that is correct from
one that merely returns numbers. Roughly half of them assert a REFUSAL: the pipeline's value is as
much in what it declines to compute as in what it reports.
"""
import json
import math
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import analysis_pipeline as ap  # noqa: E402

FIX = ROOT / "data/fixtures/synthetic"


def run_cli(*args):
    return subprocess.run([sys.executable, str(ROOT / "scripts/analysis_pipeline.py"), *args],
                          capture_output=True, text=True, cwd=ROOT)


class IngestionRefusalTests(unittest.TestCase):
    def test_wrong_unit_is_refused_not_reinterpreted(self):
        with self.assertRaises(ap.PipelineError) as e:
            ap.load_runs(FIX / "unit-error")
        self.assertIn("mm", str(e.exception))
        self.assertIn("um", str(e.exception))

    def test_walled_sample_without_a_value_is_refused(self):
        with self.assertRaises(ap.PipelineError) as e:
            ap.load_runs(FIX / "missing-data")
        self.assertIn("no clearance value", str(e.exception))

    def test_a_clearance_inside_a_seam_is_refused(self):
        run = ap.load_run(sorted((FIX / "positive").glob("*.json"))[0])
        run["clearance_field"]["wall_mask"][0] = False        # claim no wall, but keep the value
        path = ROOT / "tests" / "_tmp_seam_value.json"
        path.write_text(json.dumps(run))
        try:
            with self.assertRaises(ap.PipelineError) as e:
                ap.load_run(path)
            self.assertIn("no wall", str(e.exception))
        finally:
            path.unlink()

    def test_missing_unit_declaration_is_refused(self):
        run = ap.load_run(sorted((FIX / "positive").glob("*.json"))[0])
        del run["units"]["thrust_N"]
        path = ROOT / "tests" / "_tmp_nounit.json"
        path.write_text(json.dumps(run))
        try:
            with self.assertRaises(ap.PipelineError):
                ap.load_run(path)
        finally:
            path.unlink()


class WallMeanTests(unittest.TestCase):
    """The defect the 2026-09-24 review reproduced: a fitted intercept is not a wall mean."""

    def counterexample(self):
        theta = [i * 30.0 for i in range(12)]
        c = [100.0 + 10.0 * math.cos(2 * math.radians(t)) for t in theta]
        mask = [not (abs(t - 0) < 1e-9 or abs(t - 180) < 1e-9) for t in theta]
        return theta, [None if not m else v for m, v in zip(mask, c)], mask, c

    def test_masked_wall_mean_is_the_integral_not_the_intercept(self):
        theta, cv, mask, c = self.counterexample()
        d = ap.clearance_descriptors({"clearance_field": {"theta_deg": theta, "c_um": cv,
                                                          "wall_mask": mask},
                                      "condition": {"n_seams": 2, "seam_width_deg": 30.0}})
        retained = [v for v, m in zip(c, mask) if m]
        self.assertAlmostEqual(d["wall_mean_um"], sum(retained) / len(retained), places=9)
        self.assertAlmostEqual(d["wall_mean_um"], 98.0, places=9)
        self.assertAlmostEqual(d["harmonic_intercept_um"], 100.0, places=9)
        self.assertAlmostEqual(d["intercept_minus_wall_mean_um"], 2.0, places=9)

    def test_on_a_full_circle_the_two_agree(self):
        theta = [i * 30.0 for i in range(12)]
        c = [100.0 + 10.0 * math.cos(2 * math.radians(t)) for t in theta]
        d = ap.clearance_descriptors({"clearance_field": {"theta_deg": theta, "c_um": c,
                                                          "wall_mask": [True] * 12},
                                      "condition": {}})
        self.assertAlmostEqual(d["wall_mean_um"], d["harmonic_intercept_um"], places=9)
        self.assertAlmostEqual(d["wall_mean_um"], 100.0, places=9)

    def test_non_uniform_sampling_is_weighted_by_actual_spacing(self):
        theta = [0.0, 10.0, 20.0, 180.0, 190.0, 200.0]
        c = [100.0, 100.0, 100.0, 200.0, 200.0, 200.0]
        d = ap.clearance_descriptors({"clearance_field": {"theta_deg": theta, "c_um": c,
                                                          "wall_mask": [True] * 6},
                                      "condition": {}})
        self.assertAlmostEqual(d["wall_mean_um"], 150.0, places=6)   # symmetric by construction

    def test_zero_amplitude_phase_is_undefined(self):
        theta = [i * 30.0 for i in range(12)]
        d = ap.clearance_descriptors({"clearance_field": {"theta_deg": theta, "c_um": [100.0] * 12,
                                                          "wall_mask": [True] * 12},
                                      "condition": {}})
        self.assertIsNone(d["lobe_phase_deg"])

    def test_seam_count_and_total_opening_are_separate_descriptors(self):
        d = ap.clearance_descriptors({
            "clearance_field": {"theta_deg": [i * 30.0 for i in range(12)],
                                "c_um": [100.0] * 12, "wall_mask": [True] * 12},
            "condition": {"n_seams": 3, "seam_width_deg": 8.0}})
        self.assertEqual(d["seam_count"], 3.0)
        self.assertEqual(d["seam_individual_width_deg"], 8.0)
        self.assertEqual(d["seam_total_opening_deg"], 24.0)


class PowerTests(unittest.TestCase):
    def test_power_is_the_mean_of_the_product_not_the_product_of_the_means(self):
        run = {"channels": {"voltage_V": [10.0, 20.0], "current_A": [1.0, 3.0],
                            "thrust_N": [4.0, 4.0], "rpm": [6000.0, 6000.0]}}
        got = ap.run_endpoints(run)["power_W"]
        self.assertAlmostEqual(got, (10 * 1 + 20 * 3) / 2)
        self.assertNotAlmostEqual(got, 15.0 * 2.0)


class MatchedThrustTests(unittest.TestCase):
    def test_interpolates_between_bracketing_points(self):
        pts = [dict(thrust_N=3.0, power_W=30.0), dict(thrust_N=5.0, power_W=50.0)]
        self.assertAlmostEqual(ap.power_at_matched_thrust(pts, 4.0), 40.0)

    def test_refuses_to_extrapolate(self):
        pts = [dict(thrust_N=3.0, power_W=30.0), dict(thrust_N=5.0, power_W=50.0)]
        with self.assertRaises(ap.PipelineError) as e:
            ap.power_at_matched_thrust(pts, 9.0)
        self.assertIn("extrapolation is refused", str(e.exception))


class IdentifiabilityTests(unittest.TestCase):
    def records(self, case):
        return ap.group_conditions(ap.load_runs(FIX / case), 4.0)

    def test_a_constant_descriptor_is_refused(self):
        """Equal mean clearance is the design, so the clearance slope is not estimable."""
        recs = self.records("positive")
        report = ap.identifiability(recs, ap.DESCRIPTORS)
        self.assertFalse(report["wall_mean_um"]["identifiable"])
        self.assertIn("constant", report["wall_mean_um"]["reason"])

    def test_a_collinear_descriptor_is_refused_and_names_what_absorbed_it(self):
        """At fixed individual width, total opening is a multiple of count: both vary, neither is
        separately estimable. This is why the design must vary width independently."""
        recs = [dict(specimen_id=f"S{i}", deployment_cycle=1, family="seam", config_group=f"g{i}",
                     power_at_T_star=10.0 + i, n_runs=1,
                     descriptors={k: 0.0 for k in ap.DESCRIPTORS} |
                                 {"wall_mean_um": 100.0, "seam_count": float(i + 2),
                                  "seam_individual_width_deg": 6.0,
                                  "seam_total_opening_deg": 6.0 * (i + 2)})
                for i in range(4)]
        report = ap.identifiability(recs, ap.DESCRIPTORS)
        self.assertTrue(report["seam_count"]["identifiable"])
        self.assertFalse(report["seam_total_opening_deg"]["identifiable"])
        self.assertIn("seam_count", report["seam_total_opening_deg"]["reason"])

    def test_random_split_is_not_offered(self):
        with self.assertRaises(ap.PipelineError):
            ap.holdout(self.records("positive"), "no-such-group", "config_group")


class BaselineFormTests(unittest.TestCase):
    """The review's R05: the proposed experiment holds mean clearance equal, which makes a
    clearance-slope baseline rank-deficient exactly when the intended comparison is run."""

    def equal_mean_records(self):
        return [dict(specimen_id=f"S{i}", deployment_cycle=1, family="seam", config_group=f"g{i}",
                     power_at_T_star=10.0 + i, n_runs=1,
                     descriptors={k: 0.0 for k in ap.DESCRIPTORS} |
                                 {"wall_mean_um": 100.0, "seam_count": float(i)})
                for i in range(4)]

    def test_equal_mean_design_uses_an_intercept_only_baseline(self):
        r = ap.compare_models(self.equal_mean_records(), "g3", holdout_key="config_group")
        self.assertEqual(r["baseline"]["form"], "intercept_only")
        self.assertEqual(r["baseline"]["descriptors"], [])

    def test_equal_mean_design_no_longer_raises(self):
        try:
            ap.compare_models(self.equal_mean_records(), "g3", holdout_key="config_group")
        except ap.PipelineError as e:
            self.fail(f"the experiment as designed must analyse, got: {e}")

    def test_varying_mean_fixture_uses_the_clearance_slope_baseline(self):
        recs = ap.group_conditions(ap.load_runs(FIX / "varying-mean"), 4.0)
        r = ap.compare_models(recs, "seam_n6_w4", holdout_key="config_group")
        self.assertEqual(r["baseline"]["form"], "intercept_plus_wall_mean")


class SpecimenAwareTests(unittest.TestCase):
    def test_scoring_is_specimen_first_not_row_first(self):
        """A specimen contributing more rows must not gain weight for that reason alone."""
        recs = ap.group_conditions(ap.load_runs(FIX / "positive"), 4.0)
        r = ap.compare_models(recs, "seam_n6_w4", holdout_key="config_group")
        ev = r["baseline"]
        self.assertGreater(ev["n_specimens"], 1)
        self.assertIn("per_specimen_abs_error_W", ev)
        self.assertEqual(len(ev["per_specimen_abs_error_W"]), ev["n_specimens"])

    def test_split_reports_whether_specimens_are_disjoint(self):
        recs = ap.group_conditions(ap.load_runs(FIX / "positive"), 4.0)
        r = ap.compare_models(recs, "seam_n6_w4", holdout_key="config_group")
        self.assertIn("split_is_specimen_disjoint", r)
        self.assertEqual(r["split_is_specimen_disjoint"], not r["specimens_on_both_sides"])

    def test_a_shared_specimen_is_reported_not_hidden(self):
        recs = [dict(specimen_id="SHARED", deployment_cycle=1, family="seam", config_group=g,
                     power_at_T_star=10.0 + i, n_runs=1,
                     descriptors={k: 0.0 for k in ap.DESCRIPTORS} |
                                 {"wall_mean_um": 100.0, "seam_count": float(i)})
                for i, g in enumerate(["a", "b", "c"])]
        r = ap.compare_models(recs, "c", holdout_key="config_group")
        self.assertEqual(r["specimens_on_both_sides"], ["SHARED"])
        self.assertFalse(r["split_is_specimen_disjoint"])


class OutcomeClassifierTests(unittest.TestCase):
    """Every branch exercised directly, rather than hoping a fixture lands on it."""

    def test_resolved_improvement(self):
        self.assertEqual(ap.classify_outcome(5.0, 0.5, 0.9, 0.02)[0], "DEFECT_AWARE_BETTER")

    def test_resolvably_worse_is_not_below_gate(self):
        self.assertEqual(ap.classify_outcome(-5.0, 0.5, -0.9, 0.02)[0], "NO_IMPROVEMENT")

    def test_effect_inside_its_own_uncertainty_is_inconclusive(self):
        verdict, reason = ap.classify_outcome(0.2, 0.5, 0.03, 0.02)
        self.assertEqual(verdict, "INCONCLUSIVE")
        self.assertIn("NOT evidence", reason)

    def test_unestimated_uncertainty_cannot_resolve_or_equate(self):
        self.assertEqual(ap.classify_outcome(5.0, None, 0.9, 0.02)[0], "INCONCLUSIVE")

    def test_equivalence_requires_a_declared_bound_and_a_fitting_interval(self):
        self.assertEqual(ap.classify_outcome(0.05, 0.10, 0.01, 0.02,
                                             equivalence_bound=0.5)[0], "PRACTICALLY_EQUIVALENT")
        self.assertEqual(ap.classify_outcome(0.05, 0.10, 0.01, 0.02)[0], "INCONCLUSIVE")
        # resolved and outside the bound, but the relative improvement is under the gate
        self.assertEqual(ap.classify_outcome(0.9, 0.10, 0.15, 0.02,
                                             equivalence_bound=0.5)[0], "RESOLVED_BELOW_GATE")

    def test_gate_and_error_ceiling(self):
        self.assertEqual(ap.classify_outcome(5.0, 0.5, 0.05, 0.02)[0], "RESOLVED_BELOW_GATE")
        self.assertEqual(ap.classify_outcome(5.0, 0.5, 0.9, 0.50)[0],
                         "IMPROVED_BUT_ERROR_TOO_HIGH")


class EndToEndVerdictTests(unittest.TestCase):
    def verdict(self, case, bound=None):
        recs = ap.group_conditions(ap.load_runs(FIX / case), 4.0)
        return ap.compare_models(recs, "seam_n6_w4", holdout_key="config_group",
                                 equivalence_bound_W=bound)

    def test_positive_fixture_clears_the_gate(self):
        self.assertEqual(self.verdict("positive")["verdict"], "DEFECT_AWARE_BETTER")

    def test_null_fixture_is_never_credited(self):
        self.assertNotEqual(self.verdict("null", bound=1.0)["verdict"], "DEFECT_AWARE_BETTER")

    def test_zero_baseline_error_is_undefined_not_infinite(self):
        recs = ap.group_conditions(ap.load_runs(FIX / "positive"), 4.0)
        for r in recs:
            r["power_at_T_star"] = 10.0
        out = ap.compare_models(recs, "seam_n6_w4", holdout_key="config_group")
        self.assertEqual(out["verdict"], "BASELINE_EXACT")
        self.assertIsNone(out["relative_improvement"])


class CliAndFixtureTests(unittest.TestCase):
    def test_cli_reports_a_refusal_with_a_nonzero_exit(self):
        p = run_cli("--runs", str(FIX / "unit-error"), "--matched-thrust", "4.0",
                    "--holdout-value", "uniform")
        self.assertEqual(p.returncode, 2)
        self.assertIn("REFUSED", p.stderr)

    def test_cli_succeeds_on_the_positive_fixture(self):
        p = run_cli("--runs", str(FIX / "positive"), "--matched-thrust", "4.0",
                    "--holdout-value", "seam_n6_w4", "--holdout-key", "config_group")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("DEFECT_AWARE_BETTER", p.stdout)

    def test_every_fixture_is_labelled_not_evidence(self):
        files = sorted(FIX.rglob("*.json"))
        self.assertGreaterEqual(len(files), 100)
        for f in files:
            with self.subTest(fixture=f.name):
                self.assertIn("NOT EVIDENCE", json.loads(f.read_text())["evidence_state"].upper())

    def test_fixture_readme_says_it_is_not_evidence(self):
        self.assertIn("NOT EVIDENCE", (FIX / "README.md").read_text().upper())


if __name__ == "__main__":
    unittest.main()
