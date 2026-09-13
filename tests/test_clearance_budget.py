"""The Stage A stop rule as a computation: pending stays pending, literature bounds never combine,
and a budget that cannot resolve the effect of interest stops the experiment."""
import csv, json, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import clearance_uncertainty_budget as B  # noqa: E402


def _reg(mutate):
    rows = list(csv.DictReader(B.REGISTER.open(newline="", encoding="utf-8")))
    mutate(rows)
    p = Path(tempfile.mkdtemp()) / "b.csv"
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    return p


def _fill(rows, sensor="10", runout="15", thermal="8", deflect="12", seam="10", target="1000", mei="150"):
    vals = dict(sensor_calibration_on_fixture=sensor, rotor_radial_runout=runout, thermal_growth_at_speed=thermal,
                fixture_deflection_under_thrust=deflect, seam_setting_repeatability=seam,
                target_mean_clearance=target, minimum_effect_of_interest=mei)
    for r in rows:
        if r["term"] in vals:
            state = "owner_decision" if r["term"] == "minimum_effect_of_interest" else "measured"
            r["value"], r["evidence_state"], r["source"] = vals[r["term"]], state, "synthetic test value"


class BudgetTests(unittest.TestCase):
    def test_committed_register_is_pending_and_record_current(self):
        res = B.compute(B.load())
        self.assertEqual(res["verdict"], "INPUTS_PENDING")
        self.assertEqual(len(res["pending_terms"]), 7)
        self.assertEqual(json.loads(B.OUT.read_text()), res)

    def test_literature_bound_never_enters_the_combination(self):
        res = B.compute(B.load(_reg(_fill)))
        self.assertIn("sensor_accuracy_literature", res["literature_bounds_excluded_from_combination"])
        self.assertNotIn("sensor_accuracy_literature", res["combined_terms_um"])

    def test_filled_budget_is_feasible_with_rss_and_k(self):
        res = B.compute(B.load(_reg(_fill)))
        self.assertEqual(res["verdict"], "FEASIBLE")
        self.assertAlmostEqual(res["combined_standard_uncertainty_um"], (10**2 + 15**2 + 8**2 + 12**2 + 10**2) ** 0.5)
        self.assertAlmostEqual(res["expanded_uncertainty_um"], 2 * res["combined_standard_uncertainty_um"])

    def test_effect_smaller_than_expanded_uncertainty_stops_the_experiment(self):
        res = B.compute(B.load(_reg(lambda rows: _fill(rows, mei="40"))))
        self.assertEqual(res["verdict"], "STOP_INSTRUMENTATION_REDESIGN")

    def test_one_pending_term_keeps_the_verdict_pending(self):
        def one_left(rows):
            _fill(rows)
            for r in rows:
                if r["term"] == "thermal_growth_at_speed": r["value"], r["evidence_state"], r["source"] = "", "pending", ""
        res = B.compute(B.load(_reg(one_left)))
        self.assertEqual(res["verdict"], "INPUTS_PENDING"); self.assertEqual(res["pending_terms"], ["thermal_growth_at_speed"])

    def test_pending_with_value_unsupported_state_and_sourceless_are_refused(self):
        def pv(rows):
            for r in rows:
                if r["term"] == "rotor_radial_runout": r["value"] = "5"
        with self.assertRaises(B.BudgetInputError): B.load(_reg(pv))
        def bad(rows):
            for r in rows:
                if r["term"] == "rotor_radial_runout": r["value"], r["evidence_state"], r["source"] = "5", "not_evidence", "x"
        with self.assertRaises(B.BudgetInputError): B.load(_reg(bad))
        def nosrc(rows):
            _fill(rows)
            for r in rows:
                if r["term"] == "rotor_radial_runout": r["source"] = ""
        with self.assertRaises(B.BudgetInputError): B.load(_reg(nosrc))

    # ── review 2 (2026-09-12): four completed-input cases returned FEASIBLE ──
    def _over(self, term, **fields):
        def m(rows):
            _fill(rows)
            for r in rows:
                if r["term"] == term: r.update(fields)
        return _reg(m)

    def test_nan_and_non_finite_values_are_refused(self):
        for bad in ("nan", "inf", "-inf"):
            with self.assertRaises(B.BudgetInputError): B.load(self._over("sensor_calibration_on_fixture", value=bad))

    def test_wrong_unit_is_refused_not_silently_read_as_micrometres(self):
        with self.assertRaises(B.BudgetInputError): B.load(self._over("sensor_calibration_on_fixture", value="0.010", unit="mm"))

    def test_coverage_factor_must_be_positive_and_in_the_governed_range(self):
        for k in ("0", "-2", "0.5", "10"):
            with self.assertRaises(B.BudgetInputError): B.load(self._over("coverage_factor_k", value=k))

    def test_required_term_relabelled_literature_bound_keeps_the_budget_unresolved(self):
        res = B.compute(B.load(self._over("sensor_calibration_on_fixture", evidence_state="literature_bound")))
        self.assertEqual(res["verdict"], "INPUTS_PENDING")
        self.assertEqual(res["ineligible_evidence_terms"], ["sensor_calibration_on_fixture"])
        self.assertIsNone(res["combined_standard_uncertainty_um"], "excluding a required term must not shrink u_c")

    def test_minimum_effect_of_interest_must_be_a_decision_not_a_measurement(self):
        res = B.compute(B.load(self._over("minimum_effect_of_interest", evidence_state="measured")))
        self.assertEqual(res["verdict"], "INPUTS_PENDING"); self.assertIn("minimum_effect_of_interest", res["ineligible_evidence_terms"])
        with self.assertRaises(B.BudgetInputError): B.load(self._over("minimum_effect_of_interest", value="0"))

    def test_duplicate_term_rows_are_refused(self):
        def dup(rows): _fill(rows); rows.append(dict(rows[1]))
        with self.assertRaises(B.BudgetInputError): B.load(_reg(dup))

    def test_cli_exit_codes(self):
        import subprocess
        p = subprocess.run([sys.executable, str(ROOT / "scripts/clearance_uncertainty_budget.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        p = subprocess.run([sys.executable, str(ROOT / "scripts/clearance_uncertainty_budget.py"), "--register", str(_reg(lambda rows: _fill(rows, mei="40")))], capture_output=True, text=True)
        self.assertEqual(p.returncode, 3)
