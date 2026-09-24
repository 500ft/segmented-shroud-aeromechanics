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


class DescriptorTests(unittest.TestCase):
    def test_two_lobe_amplitude_is_recovered_from_the_wall_domain(self):
        """A seam removes wall samples; the harmonic must still be recovered from what remains."""
        import scripts.make_synthetic_fixtures as mk
        field = mk.clearance_field(c_bar=1000.0, lobe_a=45.0, lobe_phase_deg=0.0,
                                   n_seams=3, seam_width_deg=6.0, step_um=0.0)
        d = ap.clearance_descriptors({"clearance_field": field,
                                      "condition": {"n_seams": 3, "seam_width_deg": 6.0}})
        self.assertAlmostEqual(d["c_bar_um"], 1000.0, places=6)
        self.assertAlmostEqual(d["lobe_amplitude_um"], 45.0, places=6)
        self.assertGreater(d["occluded_fraction"], 0.0)

    def test_power_is_the_mean_of_the_product_not_the_product_of_the_means(self):
        """With correlated ripple the two differ, and the protocol requires the former."""
        run = {"channels": {"voltage_V": [10.0, 20.0], "current_A": [1.0, 3.0],
                            "thrust_N": [4.0, 4.0], "rpm": [6000.0, 6000.0]}}
        got = ap.run_endpoints(run)["power_W"]
        self.assertAlmostEqual(got, (10 * 1 + 20 * 3) / 2)                 # 35.0
        self.assertNotAlmostEqual(got, 15.0 * 2.0)                          # 30.0


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
        train, _ = ap.holdout(self.records("positive"), "seam", "family")
        report = ap.identifiability(train, ap.DESCRIPTORS)
        self.assertFalse(report["seam_count"]["identifiable"])
        self.assertIn("constant", report["seam_count"]["reason"])

    def test_a_collinear_descriptor_is_refused_and_names_what_absorbed_it(self):
        """Total seam width is seam count times a fixed width: both vary, neither is separable."""
        train, _ = ap.holdout(self.records("positive"), "seam_n5", "config_group")
        report = ap.identifiability(train, ap.DESCRIPTORS)
        self.assertTrue(report["seam_count"]["identifiable"])
        self.assertFalse(report["seam_total_width_deg"]["identifiable"])
        self.assertIn("seam_count", report["seam_total_width_deg"]["reason"])

    def test_whole_family_holdout_reports_not_identifiable_rather_than_fitting(self):
        result = ap.compare_models(self.records("positive"), "seam", holdout_key="family")
        self.assertIn("seam_count", result["descriptors_refused"])

    def test_random_split_is_not_offered(self):
        with self.assertRaises(ap.PipelineError):
            ap.holdout(self.records("positive"), "no-such-group", "config_group")


class HierarchyTests(unittest.TestCase):
    def test_repeated_runs_collapse_to_one_record_per_condition(self):
        runs = ap.load_runs(FIX / "positive")
        records = ap.group_conditions(runs, 4.0)
        self.assertEqual(len(runs), 24)
        self.assertEqual(len(records), 8)                 # 8 conditions x 3 thrust levels
        self.assertTrue(all(r["n_runs"] == 3 for r in records))


class VerdictTests(unittest.TestCase):
    def result(self, case):
        recs = ap.group_conditions(ap.load_runs(FIX / case), 4.0)
        return ap.compare_models(recs, "seam_n5", holdout_key="config_group")

    def test_positive_fixture_clears_the_registered_gate(self):
        r = self.result("positive")
        self.assertEqual(r["verdict"], "DEFECT_AWARE_BETTER")
        self.assertGreater(r["relative_improvement"], r["gate"]["min_relative_improvement"])

    def test_null_fixture_does_not_clear_the_gate(self):
        """The defect-aware model must not be credited when the defect does nothing."""
        r = self.result("null")
        self.assertNotEqual(r["verdict"], "DEFECT_AWARE_BETTER")
        self.assertLess(r["relative_improvement"], r["gate"]["min_relative_improvement"])

    def test_gate_thresholds_come_from_the_registered_values(self):
        r = self.result("positive")
        self.assertAlmostEqual(r["gate"]["min_relative_improvement"], 0.20)
        self.assertAlmostEqual(r["gate"]["max_relative_error"], 0.10)

    def test_zero_baseline_error_is_undefined_not_infinite(self):
        recs = ap.group_conditions(ap.load_runs(FIX / "positive"), 4.0)
        for r in recs:                                     # make the baseline exact by construction
            r["power_at_T_star"] = 10.0 + 0.0 * r["descriptors"]["c_bar_um"]
        out = ap.compare_models(recs, "seam_n5", holdout_key="config_group")
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
                    "--holdout-value", "seam_n5", "--holdout-key", "config_group")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("DEFECT_AWARE_BETTER", p.stdout)

    def test_every_fixture_is_labelled_not_evidence(self):
        files = sorted(FIX.rglob("*.json"))
        self.assertGreaterEqual(len(files), 40)
        for f in files:
            with self.subTest(fixture=f.name):
                self.assertIn("NOT EVIDENCE", json.loads(f.read_text())["evidence_state"].upper())

    def test_fixture_readme_says_it_is_not_evidence(self):
        self.assertIn("NOT EVIDENCE", (FIX / "README.md").read_text().upper())


if __name__ == "__main__":
    unittest.main()
