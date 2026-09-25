#!/usr/bin/env python3
"""Attempt-level dispositions: what happened, kept separate from what may be analysed.

The failure this prevents is survivor-only reporting. A run that rubs is excluded from an
aerodynamic power fit and is still one of the outcomes this project exists to study, so the
two decisions must not share a field. A run whose file will not parse is still an attempt
that was made, so the denominator cannot be rebuilt from the files that happened to load.

Four independent assessments per attempt:

    acquisition_validity            valid | invalid | unknown
    aerodynamic_eligibility         eligible | ineligible | pending
    contact_or_clearance_outcome    no_detected_failure | failure | unknown
    attempted_condition_membership  included | excluded

They are independent but not arbitrary. Invalid acquisition cannot yield a trusted endpoint,
so it can never be eligible. A non-detection requires a detector that was working and covering
the window; without that the outcome is unknown, never success. Missing data is not success.

The attempt register is written before acquisition starts. That is what makes the denominator
real: it exists whether or not a file is ever produced.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

VALIDITY = ("valid", "invalid", "unknown")
ELIGIBILITY = ("eligible", "ineligible", "pending")
OUTCOME = ("no_detected_failure", "failure", "unknown")
MEMBERSHIP = ("included", "excluded")


class DispositionError(ValueError):
    """An attempt record the reconciler refuses, with the reason stated."""


def _reason(text):
    return text


def disposition(attempt):
    """Assign the four assessments for one attempt record. Never raises on a bad measurement.

    `attempt` carries what was observed, not what was concluded:
      attempt_id, parent_attempt_id, specimen_id
      initiated            bool   the registered initiation event occurred
      acquisition          "ok" | "invalid" | "missing" | "unparsed"
      detector_functioning bool | None
      detector_covered     bool | None
      contact_observed     bool | None   independent evidence of contact, if any
      thrust_matched       bool | None
    """
    out = {"attempt_id": attempt["attempt_id"],
           "parent_attempt_id": attempt.get("parent_attempt_id"),
           "specimen_id": attempt.get("specimen_id"),
           "reasons": {}}

    # ---- membership: was this an attempt at all?
    if not attempt.get("initiated", False):
        out["attempted_condition_membership"] = "excluded"
        out["reasons"]["membership"] = _reason(
            "cancelled before the registered initiation event, so it is counted as a "
            "cancellation and not as an initiated attempt")
    else:
        out["attempted_condition_membership"] = "included"
        out["reasons"]["membership"] = _reason("the registered initiation event occurred")

    # ---- acquisition validity
    acq = attempt.get("acquisition")
    if acq == "ok":
        out["acquisition_validity"] = "valid"
    elif acq in ("invalid", "unparsed"):
        out["acquisition_validity"] = "invalid"
        out["reasons"]["acquisition"] = _reason("acquisition recorded as %r" % acq)
    elif acq in (None, "missing"):
        out["acquisition_validity"] = "unknown"
        out["reasons"]["acquisition"] = _reason(
            "no usable acquisition record; absence of data is not evidence that the run was fine")
    else:
        raise DispositionError("attempt %s: unrecognised acquisition %r"
                               % (attempt["attempt_id"], acq))

    # ---- contact or clearance outcome
    if attempt.get("contact_observed") is True:
        out["contact_or_clearance_outcome"] = "failure"
        out["reasons"]["outcome"] = _reason("contact independently observed")
    elif (attempt.get("detector_functioning") is True
          and attempt.get("detector_covered") is True
          and attempt.get("contact_observed") is False):
        out["contact_or_clearance_outcome"] = "no_detected_failure"
        out["reasons"]["outcome"] = _reason(
            "a functioning detector covered the window and saw nothing")
    else:
        out["contact_or_clearance_outcome"] = "unknown"
        out["reasons"]["outcome"] = _reason(
            "no non-detection may be claimed without a functioning detector and a coverage "
            "rule; this is unknown, not success")

    # ---- aerodynamic eligibility, which depends on the two above
    if out["acquisition_validity"] != "valid":
        out["aerodynamic_eligibility"] = "ineligible"
        out["reasons"]["eligibility"] = _reason(
            "acquisition is not valid, so no trusted power endpoint exists")
    elif out["contact_or_clearance_outcome"] == "failure":
        out["aerodynamic_eligibility"] = "ineligible"
        out["reasons"]["eligibility"] = _reason(
            "contact occurred, so this is excluded from the steady aerodynamic fit while "
            "remaining an observed outcome and a counted attempt")
    elif attempt.get("thrust_matched") is False:
        out["aerodynamic_eligibility"] = "ineligible"
        out["reasons"]["eligibility"] = _reason(
            "the matched-thrust condition was not attained, so the power endpoint is "
            "unavailable; no contact outcome is inferred from this")
    elif attempt.get("thrust_matched") is None:
        out["aerodynamic_eligibility"] = "pending"
        out["reasons"]["eligibility"] = _reason("matched-thrust status not yet assessed")
    else:
        out["aerodynamic_eligibility"] = "eligible"

    for field, allowed in (("acquisition_validity", VALIDITY),
                           ("aerodynamic_eligibility", ELIGIBILITY),
                           ("contact_or_clearance_outcome", OUTCOME),
                           ("attempted_condition_membership", MEMBERSHIP)):
        assert out[field] in allowed, (field, out[field])
    return out


def reconcile(register):
    """Dispositions and counts for a whole attempt register.

    A duplicated attempt id is collapsed rather than counted twice; a legacy record with no
    disposition information comes through as unknown and pending, never as eligible.
    """
    seen, rows, duplicates = {}, [], []
    for attempt in register:
        aid = attempt["attempt_id"]
        if aid in seen:
            duplicates.append(aid)
            continue
        seen[aid] = True
        rows.append(disposition(attempt))

    counts = {
        "registered_attempts": len(rows),
        "initiated": sum(r["attempted_condition_membership"] == "included" for r in rows),
        "cancelled_before_initiation": sum(
            r["attempted_condition_membership"] == "excluded" for r in rows),
        "eligible_for_aerodynamic_fit": sum(
            r["aerodynamic_eligibility"] == "eligible" for r in rows),
        "observed_failures": sum(r["contact_or_clearance_outcome"] == "failure" for r in rows),
        "outcome_unknown": sum(r["contact_or_clearance_outcome"] == "unknown" for r in rows),
        "acquisition_invalid": sum(r["acquisition_validity"] == "invalid" for r in rows),
        "duplicate_ingests_collapsed": len(duplicates),
    }
    initiated = counts["initiated"]
    unknown = counts["outcome_unknown"]
    failures = counts["observed_failures"]
    counts["failure_fraction_bounds"] = {
        "note": ("Unknown outcomes are not passes. The lower bound counts them as no failure, "
                 "the upper bound counts them as failures; report the interval, not a point."),
        "lower": (failures / initiated) if initiated else None,
        "upper": ((failures + unknown) / initiated) if initiated else None,
    }
    return {"schema_version": 1, "dispositions": rows, "counts": counts,
            "duplicate_attempt_ids": sorted(set(duplicates))}


def eligible_specimens(report):
    """Attempt ids admissible to the aerodynamic fit. Filtering happens before fitting."""
    return [r["attempt_id"] for r in report["dispositions"]
            if r["aerodynamic_eligibility"] == "eligible"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("register", help="JSON list of attempt records written before acquisition")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    report = reconcile(json.loads(Path(a.register).read_text()))
    text = json.dumps(report, indent=2) + "\n"
    if a.out:
        Path(a.out).write_text(text)
    else:
        sys.stdout.write(text)
    c = report["counts"]
    print("attempts %d, initiated %d, eligible %d, failures %d, unknown %d"
          % (c["registered_attempts"], c["initiated"], c["eligible_for_aerodynamic_fit"],
             c["observed_failures"], c["outcome_unknown"]), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
