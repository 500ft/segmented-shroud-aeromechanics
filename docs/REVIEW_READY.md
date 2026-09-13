# 2026-09-09 — latest review correction

## 2026-09-11 — SSY-D04 provenance-clean re-acquisition

The D02 provenance defect is corrected by one clean run of `rerun_search.py` from a
non-throttled network: 451 identifier records, 18/18 query legs ok,
**0** rows without a successful logged query (historical export: 50). Known D01 anchors
present: 3 of 3 comparable — a bounded overlap, not recall. 25 candidates, all UNSCREENED.
The 09-09 export and the day-3 acquisition ledger are unchanged; the new export is not merged into
either. No novelty, patent or owner gate is closed. [Evidence](../evidence/task-2026-09-11/README.md).

## Day-3 preparation — 2026-09-09

Six new ledger tests preserve acquisition routes, unavailable query mappings, zero-result semantics, unscreened status, all raw rows and deterministic regeneration. 21 tests and repository contract pass. All 499 raw rows retained; 50 provenance holes remain. Public JSASS PDF and a patent claim were accessed; other full-text and disclosure gates remain unresolved.

Review [DAY3_PLAN.md](DAY3_PLAN.md), [deliverable](day3-source-review.md), and [commands/evidence](../evidence/task-day3-2026-09-09/README.md). Base: `6ccb65c648318ca7f4f505452416813956a3ac06`; new PR branch: `task/day-three-20260909`. No original Owner/External gate is closed. Final source identity is the PR head, reported in its delivery record rather than embedded circularly here.

SSY-01 and XC-02 remain open; patent access is not legal clearance.

Read [the D02 integrity review](../evidence/task-2026-09-09-review/README.md)
before the historical handoff below. D02 is blocked on unexplained acquisition
provenance; original literal-ID overlap is not a valid recall estimate. The
rerun/audit software passes 15 tests plus contract checks. No new literature
screening or research validation is claimed.

# Segmented-Shroud-Yield — partial handoff, local software ready for review

## Latest follow-up — 2026-09-09

[SSY-D02 database export](../docs/prior-art-search-2026-09-09-database.md) adds a dated,
reproducible native-database search with a measured recall check (1/6 of the day-1 set
recovered — the two discovery routes diverge). Candidates are unscreened; no gate is closed.

## Follow-up — 2026-09-08

[SSY-D01 source-review handoff](../evidence/task-2026-09-08/README.md) adds a dated
first-pass research review. It does not close the full novelty or owner gates.
Original sprint evidence below is historical; no new experimental result exists.

Prepared 2026-09-05; resumed and checked 2026-09-06. Budget: six workload days,
30 focused hours per repository; estimates are not recorded time spent.

Canonical checkout: `/Users/redhose/Developer/research-sprints/2026-09-05/Segmented-Shroud-Yield`.
Remote: https://github.com/500ft/Segmented-Shroud-Yield.
Branch: `sprint/evidence-integrity-20260905`.
Base commit: `971eadb6b778c5fda764894235490dab2ad345e2`.
Final commit: this review packet's containing commit; its SHA is reported in the PR
because a commit cannot embed its own identity. No deployment, publication,
outreach or spending occurred. Original checkout/user changes were preserved.
Base includes the existing unmerged task PR #1 head; it is not origin/main.

[Roadmap](SPRINT_ROADMAP.md) · [Authoritative ledger](SPRINT_TASKS.csv) ·
[Progress](SPRINT_PROGRESS.md) · [Selected candidate hashes](../evidence/sprint-2026-09-05/candidate.json).

## Completed deliverables and evidence

The checker enforces specimen JSON Schema and finite values. Duct performance and protective-guard qualification now have independent evidence paths. Held-out-family predictions require descriptor support or explicitly specified physical extrapolation.

Implementation: [checker](../scripts/check_repo_contract.py), [tests](../tests/test_manifest_validation.py), [research plan](research-plan.md), [roadmap](../ROADMAP.md), [first experiment](experiment-01-rigid-defect-duct.md).

- [Baseline identity, commands and outputs](../evidence/sprint-2026-09-05/baseline.json).
- [Original failing evidence](../evidence/sprint-2026-09-05/manifest-red.json).
- [Implementation checks](../evidence/sprint-2026-09-05/implementation-green.json).
- [Final verification](../evidence/sprint-2026-09-05/final-checks.json).
- [Predeclared evaluation procedure](../evidence/sprint-2026-09-05/evaluation-plan.md),
  [retained replay](../evidence/sprint-2026-09-05/evaluate_candidate.py),
  [actual outputs](../evidence/sprint-2026-09-05/evaluation.json).

- [Consumer delivery evidence](../evidence/sprint-2026-09-05/consumer.json).

7 tests passed in development and clean consumer environments; repository contract passed; 7/7 additional metadata cases matched.

Design and intake only; no CAD, rotor test, trained response model or protective qualification. Null planned measurements remain valid metadata, not observed values.

## Reproduce

Run from the canonical checkout using the recorded Python3.11 environment and
repository dependencies. The local pytest workaround stubs readline before import;
it is not a skipped test or changed product requirement.

```sh
python -m unittest discover -s tests -v
python scripts/check_repo_contract.py
python evidence/sprint-2026-09-05/evaluate_candidate.py
git diff --check
```



Delivery route: a clean temporary venv installed pinned jsonschema4.26.0 and executed absolute checker/test paths from /private/tmp. Resolved transitive versions are retained in consumer.json. The checker uses the schema-declared dialect via validator_for; [official validation API](https://python-jsonschema.readthedocs.io/en/stable/validate/) is the interface reference.

No separate configured lint/typecheck is claimed. Syntax checks are compilation,
not static typing. Saved output truncation, if present, is indicated by the tool
result metadata; no omitted output is called a full log.

## Evaluation meaning and remaining work

Selected implementation/protocol hashes and expectations were saved before the
additional cases ran. Existing tests, reviewed fixtures and reviewer-discovered
bugs are development material. All additional cases were retained. These small
developer-selected checks establish behavior on those inputs, not independent
scientific validation or general accuracy. Another agent is not a human reviewer.
External feedback: pending.

1. Owner chooses rotor/stand/metrology access and closes the exact-gap prior-art task.
2. Define and qualify the rigid-defect apparatus before studying a folding mechanism.
3. Guard protection requires its own approved tests; aerodynamic failure does not confer a fallback success.

Next action: Owner resource choice, then long-term SSY-01 exact-gap closeout and rigid-defect metrology/CAD work order.

Evidence-supported portfolio bullet: “Built schema-checked specimen intake and an identifiable defect-study plan separating aerodynamic yield from unproven protective performance.”
This concerns engineering quality, not adoption or measured scientific performance.

## Ready-to-send review request

“Review Segmented-Shroud-Yield against docs/SPRINT_ROADMAP.md. Repository: /Users/redhose/Developer/research-sprints/2026-09-05/Segmented-Shroud-Yield. Base commit: 971eadb6b778c5fda764894235490dab2ad345e2. Final commit: PR head (see GitHub PR). Review index: docs/REVIEW_READY.md. Incomplete work: Owner chooses rotor/stand/metrology access and closes the exact-gap prior-art task. Define and qualify the rigid-defect apparatus before studying a folding mechanism. Guard protection requires its own approved tests; aerodynamic failure does not confer a fallback success. Reproduce the changed behaviors and counterexamples, rerun appropriate checks, and assess the code and evidence independently. Review first; make further changes only if requested.”
