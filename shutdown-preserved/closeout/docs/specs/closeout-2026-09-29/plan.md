# Closeout implementation — 2026-09-29

Status: in progress. Implements the remaining acceptance criteria in the September 25
closeout handoff against main `2317d8f`. PRs #31 and #34 already delivered most of
the proposed artifacts; #35 added convergence sensitivity. This work completes the
integration and corrects remaining inconsistencies, without repeating those changes.
Open PR #36 owns terminated CFD status; this work does not replace it.

- [ ] G0/C2: reconcile active validation decisions, task completion and scope with the
  evidence; preserve frozen records. Check: targeted consistency tests and repository contract.
- [ ] A1–A4: reconcile literature/read-scope statements and make transient acceptance
  conservative for missing or invalid evidence. Check: literature and transient tests.
- [ ] B1: connect registered attempts to analysis before interpolation; retain malformed,
  failed and missing acquisitions in the denominator; separate cancellations and retry units.
  Check: disposition tests and end-to-end pipeline fixtures.
- [ ] B2: finish coded-matrix and geometry-constraint checks; scale production least squares.
  Check: manufactured predictions, unit changes, deficient and near-dependent designs,
  generated design document freshness.
- [ ] C1: retain the diagnosed recovery barrier with an explicit current readiness record;
  do not assume a complete checkpoint or change machine resources. Check: read-only
  resource/runtime/input inventory and recorded outcome.
- [ ] Integration: relevant and full tests, generated-artifact checks, historical-evidence
  preservation, ledger row, test report and PR with hosted checks on its final head.

Physical levels, installed instrument evidence, D10, the A0.1 release decision and
XC-02 stay open. Completing these artifacts does not close SSY-01/02/03 or release
Study A or CAD. No physical testing or new CFD result is claimed by this work order.
