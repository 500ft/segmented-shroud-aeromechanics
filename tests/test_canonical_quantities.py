"""The canonical register must stay tied to the code, and its categories must mean something."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_quantities as cq  # noqa: E402

DOC = json.loads(cq.REGISTER.read_text())
Q = DOC["quantities"]


class RegisterAgreesWithCodeTests(unittest.TestCase):
    def test_the_checker_passes_on_the_committed_state(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/check_quantities.py")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_every_anchored_value_matches_its_source(self):
        """Read independently of the checker, so a bug there cannot hide a drift."""
        for name, q in Q.items():
            anchor = q.get("code_anchor")
            if not anchor:
                continue
            path = ROOT / anchor["file"]
            sym, want = anchor["symbol"], q["value"]
            consts = cq.literal_constants(path)
            defaults = cq.keyword_defaults(path).get(sym)
            found = {consts[sym]} if sym in consts else defaults
            self.assertIsNotNone(found, "%s: %s not found in %s" % (name, sym, anchor["file"]))
            self.assertEqual(found, {want}, "%s drifted from %s" % (name, anchor["file"]))


class ProvenanceDisciplineTests(unittest.TestCase):
    def test_the_two_acceptance_gates_are_marked_provisional(self):
        """They are enforced in code and derived nowhere. That must stay visible."""
        for name in ("GATE-IMPROVEMENT", "GATE-RELATIVE-ERROR"):
            self.assertEqual(Q[name]["provenance"], "provisional_estimate", name)
            self.assertTrue(Q[name]["open_question"], name)

    def test_the_grit_spread_is_not_registered_as_an_uncertainty(self):
        limits = Q["A01-GRIT-SPREAD"]["limits"].lower()
        self.assertIn("not eligible", limits)
        self.assertIn("neither an upper nor a lower bound", limits)

    def test_a_sourced_assumption_says_whether_its_condition_holds(self):
        g = Q["GCI-SAFETY-FACTOR"]
        self.assertTrue(g["source"])
        self.assertIn("NOT CHECKED", g["condition_status"])

    def test_nothing_claims_a_physical_test(self):
        for name, q in Q.items():
            self.assertNotEqual(q["evidence_status"], "physically_tested",
                                "%s claims a measurement this project does not have" % name)

    def test_the_fixture_constant_is_not_mistaken_for_a_project_target(self):
        self.assertIn("not IN-02", Q["FIXTURE-MEAN-CLEARANCE"]["limits"])

    def test_every_quantity_has_a_value_a_unit_and_a_definition(self):
        for name, q in Q.items():
            for field in ("value", "unit", "definition", "provenance", "evidence_status"):
                self.assertTrue(q.get(field) is not None and q.get(field) != "",
                                "%s is missing %s" % (name, field))


class AuditTests(unittest.TestCase):
    AUDIT = ROOT / "docs/number-provenance-audit-2026-09-25.md"

    def test_the_audit_exists_and_separates_the_three_kinds_of_gap(self):
        text = self.AUDIT.read_text()
        for phrase in ("Missing documentation for a supported decision",
                       "Needs engineering justification", "Cannot be assessed yet"):
            self.assertIn(phrase, text)

    def test_the_audit_labels_its_own_work_retrospective(self):
        self.assertIn("Retrospective assessment", self.AUDIT.read_text())

    def test_the_safety_factor_sensitivity_is_reproducible_from_committed_values(self):
        """Recompute the audit's own table rather than trusting the numbers it prints."""
        rec = json.loads((ROOT / "results/generated/cfd/a0.1/uncertainty.json").read_text())
        cases, model = rec["cases"]["SA"], rec["per_model"]["SA"]
        phi = [cases[g]["value"] for g in ("g3", "g2", "g1")]
        h = [cases[g]["h"] for g in ("g3", "g2", "g1")]
        r21 = h[1] / h[0]
        e21 = abs((phi[0] - phi[1]) / phi[0])

        def gci(p, fs):
            return fs * e21 / (r21 ** p - 1)

        p_obs = model["apparent_order"]
        self.assertAlmostEqual(gci(p_obs, 1.25), model["gci_fine_fraction"], places=9)
        spread = [gci(p_obs, 1.25), gci(p_obs, 3.0), gci(2.0, 1.25), gci(2.0, 3.0)]
        self.assertAlmostEqual(min(spread) * 100, 0.153, places=2)
        self.assertAlmostEqual(max(spread) * 100, 0.658, places=2)
        # The point of the audit entry: none of these reach the comparison error.
        error = abs(rec["validation"]["SA"]["comparison_error_E"] / rec["validation"]["SA"]["D"])
        self.assertGreater(error, max(spread) * 3,
                           "the safety-factor choice would now be able to change the conclusion")


if __name__ == "__main__":
    unittest.main()
