"""The eight behaviour cases the review requires of attempt dispositions.

Each test is one of the cases, written so that a failure names the scientific mistake rather
than a field value. The point throughout: excluding data from a fit must never remove it from
the record of what was attempted.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ingestion_dispositions as idp  # noqa: E402


def attempt(aid, **kw):
    base = dict(attempt_id=aid, specimen_id="S1", initiated=True, acquisition="ok",
                detector_functioning=True, detector_covered=True, contact_observed=False,
                thrust_matched=True)
    base.update(kw)
    return base


class RequiredCaseTests(unittest.TestCase):
    def test_1_clean_run_is_eligible_and_counted(self):
        d = idp.disposition(attempt("A1"))
        self.assertEqual(d["acquisition_validity"], "valid")
        self.assertEqual(d["aerodynamic_eligibility"], "eligible")
        self.assertEqual(d["contact_or_clearance_outcome"], "no_detected_failure")
        self.assertEqual(d["attempted_condition_membership"], "included")

    def test_2_rubbing_leaves_the_fit_but_stays_an_attempt_and_a_failure(self):
        d = idp.disposition(attempt("A2", contact_observed=True))
        self.assertEqual(d["aerodynamic_eligibility"], "ineligible")
        self.assertEqual(d["contact_or_clearance_outcome"], "failure",
                         "contact was observed and must remain an observed outcome")
        self.assertEqual(d["attempted_condition_membership"], "included",
                         "excluding a run from a fit must not remove it from the denominator")

    def test_3_detector_dropout_gives_unknown_not_success(self):
        d = idp.disposition(attempt("A3", detector_functioning=False, contact_observed=None))
        self.assertEqual(d["contact_or_clearance_outcome"], "unknown",
                         "a dead detector cannot establish that nothing happened")
        self.assertEqual(d["attempted_condition_membership"], "included")

    def test_4_unmatched_thrust_drops_the_endpoint_and_infers_no_contact(self):
        d = idp.disposition(attempt("A4", thrust_matched=False))
        self.assertEqual(d["aerodynamic_eligibility"], "ineligible")
        self.assertEqual(d["contact_or_clearance_outcome"], "no_detected_failure",
                         "failing to reach the thrust target is not a contact outcome")
        self.assertEqual(d["attempted_condition_membership"], "included")

    def test_5_cancellation_before_initiation_is_counted_separately(self):
        d = idp.disposition(attempt("A5", initiated=False))
        self.assertEqual(d["attempted_condition_membership"], "excluded")
        r = idp.reconcile([attempt("A5", initiated=False), attempt("A1")])
        self.assertEqual(r["counts"]["initiated"], 1)
        self.assertEqual(r["counts"]["cancelled_before_initiation"], 1)

    def test_6_invalid_acquisition_and_observed_contact_are_both_recorded(self):
        d = idp.disposition(attempt("A6", acquisition="invalid", contact_observed=True))
        self.assertEqual(d["acquisition_validity"], "invalid")
        self.assertEqual(d["contact_or_clearance_outcome"], "failure",
                         "an independently observed failure survives an invalid measurement")
        self.assertEqual(d["aerodynamic_eligibility"], "ineligible")

    def test_7_duplicate_ingest_does_not_inflate_the_denominator(self):
        r = idp.reconcile([attempt("A1"), attempt("A1"), attempt("A2")])
        self.assertEqual(r["counts"]["registered_attempts"], 2)
        self.assertEqual(r["counts"]["duplicate_ingests_collapsed"], 1)
        self.assertEqual(r["duplicate_attempt_ids"], ["A1"])

    def test_8_a_legacy_record_is_never_assumed_eligible(self):
        legacy = {"attempt_id": "L1", "initiated": True}
        d = idp.disposition(legacy)
        self.assertEqual(d["acquisition_validity"], "unknown")
        self.assertEqual(d["contact_or_clearance_outcome"], "unknown")
        self.assertEqual(d["aerodynamic_eligibility"], "ineligible")


class IndependenceTests(unittest.TestCase):
    def test_an_unparsed_file_still_counts_as_an_attempt(self):
        """The denominator cannot be rebuilt from the files that happened to load."""
        r = idp.reconcile([attempt("A1"), attempt("BAD", acquisition="unparsed")])
        self.assertEqual(r["counts"]["initiated"], 2)
        self.assertEqual(r["counts"]["eligible_for_aerodynamic_fit"], 1)
        self.assertEqual(r["counts"]["acquisition_invalid"], 1)

    def test_unknown_outcomes_are_bounded_not_treated_as_passes(self):
        r = idp.reconcile([attempt("A1"),
                           attempt("A2", contact_observed=True),
                           attempt("A3", detector_functioning=False, contact_observed=None)])
        b = r["counts"]["failure_fraction_bounds"]
        self.assertAlmostEqual(b["lower"], 1 / 3)
        self.assertAlmostEqual(b["upper"], 2 / 3)
        self.assertLess(b["lower"], b["upper"], "an unknown outcome must widen the interval")

    def test_eligibility_filter_keeps_the_audit_intact(self):
        reg = [attempt("A1"), attempt("A2", contact_observed=True)]
        r = idp.reconcile(reg)
        self.assertEqual(idp.eligible_specimens(r), ["A1"])
        self.assertEqual(len(r["dispositions"]), 2, "the excluded attempt left the report")

    def test_retries_keep_their_own_id_and_name_their_parent(self):
        r = idp.reconcile([attempt("A1"), attempt("A1r", parent_attempt_id="A1")])
        self.assertEqual(r["counts"]["registered_attempts"], 2)
        self.assertEqual([d["parent_attempt_id"] for d in r["dispositions"]], [None, "A1"])

    def test_every_disposition_carries_its_reason(self):
        d = idp.disposition(attempt("A3", detector_functioning=False, contact_observed=None))
        self.assertIn("unknown, not success", d["reasons"]["outcome"])

    def test_an_unrecognised_acquisition_value_is_refused(self):
        with self.assertRaises(idp.DispositionError):
            idp.disposition(attempt("A9", acquisition="probably fine"))


if __name__ == "__main__":
    unittest.main()
