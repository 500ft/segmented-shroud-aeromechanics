# Sprint progress

Newest section first; historical entries keep their original dates and wording.

## 2026-09-15 — top-25 candidate triage and measurement-requirements draft (work order 2026-09-14)

Executed on `task/day-2026-09-14` from the [merged plan](specs/day-2026-09-14/plan.md). Two bounded artifacts, both with their own test: the [triage record](candidate-screening-2026-09-14.json) with its [report and hand-off queues](prior-art-search-2026-09-14-screening.md) (25 dispositions: 22 include for close reading, 3 exclude off topic, 0 defer; rule frozen before reading; no novelty-axis state assigned), and the [measurement-requirements draft](measurement-system-spec.md) (12 channels, budget-register mapping, qualification procedures, open-input register IN-01 to IN-12). Ledger rows SSY-R03 and SSY-R04 are `done` for their artifacts only. [Evidence and command logs](../evidence/task-2026-09-14/README.md).

Not done, by responsible role: **owner** — IN-01 minimum clearance effect, IN-02 target mean clearance, IN-03 minimum power difference at matched thrust, IN-04 rotor/stand/sensor envelope, XC-02 disclosure path, SSY-S08; **agent** — close reading of the 22 includes with a new dated reading record, then novelty-axis reconciliation; a second frozen batch for the 111 qualifying unselected records; a dated patent search; derivation of channel limits once IN-01 and IN-03 exist; **metrology provider** — the five installed clearance contributors (SSY-12). Completed top-25 triage is not the unfinished scholarly review; a delivered requirements draft is not frozen requirements or physical qualification. Historical acquisitions, the day-3 reading records, the eligibility register and the budget CSV are unchanged.

## 2026-09-11 — evidence-gap correction

The [current correction](ACQUISITION_CORRECTION_2026-09-11.md) supersedes any interpretation that earlier preparation closed a physical, approval, or source-review gate. Work is on `fix/evidence-gaps-20260911` from current renamed main; historical entries below retain their original dates and PR snapshots. The original day-3 and presentation PRs are now merged, but this correction is a new reviewable change, not an asserted merge or publication.

Each omitted or incomplete recommendation is accounted for separately in the current correction and existing task ledgers. No owner signature, measurement, PI conversation, imagery judgment, disclosure approval or independent review was fabricated. Exact tests, scope and next inputs are linked from the correction record; actual delivery state is established by its PR.

## 2026-09-11 — SSY-D04 provenance-clean re-acquisition

The D02 provenance defect is corrected by one clean run of `rerun_search.py` from a
non-throttled network: 451 identifier records, 18/18 query legs ok,
**0** rows without a successful logged query (historical export: 50). Known D01 anchors
present: 3 of 3 comparable — a bounded overlap, not recall. 25 candidates, all UNSCREENED.
The 09-09 export and the day-3 acquisition ledger are unchanged; the new export is not merged into
either. No novelty, patent or owner gate is closed. [Evidence](../evidence/task-2026-09-11/README.md).

## Day-3 work — 2026-09-09

Delivery update: the preparation was committed as 500ft and pushed; [day-3 PR](https://github.com/500ft/Segmented-Shroud-Yield/pull/5) is open against main. Initial implementation source: `e5e69c002f71b3ea088da90a1e2205c8d1ee4314` (later review/documentation commits are visible in the PR). This supersedes the pre-push stopping state below. Original day-1/day-2 PRs are merged; this new PR is not merged. Resume from the named unresolved project gates in [DAY3_PLAN.md](DAY3_PLAN.md), not from the already completed push step.

Both reviewed PR layers merged into main; new work starts from `6ccb65c648318ca7f4f505452416813956a3ac06` on `task/day-three-20260909`. Six new ledger tests preserve acquisition routes, unavailable query mappings, zero-result semantics, unscreened status, all raw rows and deterministic regeneration. 21 tests and repository contract pass. All 499 raw rows retained; 50 provenance holes remain. Public JSASS PDF and a patent claim were accessed; other full-text and disclosure gates remain unresolved.

The [evidence record](../evidence/task-day3-2026-09-09/README.md) contains checks and limits. Work is locally verified and not yet recorded here as pushed/merged. Current edits belong to this task; original checkouts were preserved. Next: finish verification, commit the bounded change and open the new PR; preserve all stated external gates.

D02 is now blocked, not accepted as a complete acquisition. The retained export
contains unexplained query provenance; no recall or route-divergence conclusion
is established. Added offline audit and safe new-output rerun with explicit
missing-credential/error states. Fifteen tests and the repository contract pass.
[Review evidence](../evidence/task-2026-09-09-review/README.md). No raw exports,
owner gates, screening verdicts, novelty clearance or disclosure path were changed.

# Sprint progress — Segmented-Shroud-Yield

## 2026-09-09 — SSY-D02 native-database export

Ran the database leg that D01 named as the next step (Crossref, OpenAlex, arXiv APIs; no patent
database reachable). [Export and recall check](prior-art-search-2026-09-09-database.md): 499 unique
records with per-query provenance; **1 of 6** day-1 identifiers recovered, which is the finding —
native-database ranking and web-index discovery surface different populations here, so neither set
can be assumed to contain the other. arXiv's search API throttled most queries; that leg is recorded
as incomplete. 25 new candidates are listed **unscreened**. No novelty, patent or owner gate is
closed. [Verification](../evidence/task-2026-09-09/README.md). Branch `task/priority-two-20260909`.

## 2026-09-08 — SSY-D01 first-pass source review

Completed the bounded priority-one source-review subtask, not the full novelty
gate. [Report](prior-art-search-2026-09-08.md) and
[verification](../evidence/task-2026-09-08/README.md). Base `dddd4f107de978319bb3f41bfeebbe927d36ab91`,
branch `task/priority-one-20260908`; isolated daily worktree. No apparatus,
measurement, publication, outreach or disclosure approval. Original sprint rows
preserved. Next: resolve report-listed full-text/search limitations; checks:
`python scripts/check_repo_contract.py`. PR records committed/pushed identity.

## 2026-09-06 — Main-branch placement authorized

Owner explicitly requested these PRs be merged to their respective main branches. This supersedes earlier placement-blocked/draft-only entries for the current changes. The combined main-targeted PR retains prerequisite integrity work, unchanged task ledgers and all actual hardware/disclosure gates. No CAD or experiment is marked complete. Merge completion and resulting main commit are verified by GitHub rather than asserted in advance here.

## 2026-09-06 — Reviewer-driven CAD amendment

This entry supersedes the earlier CAD allocation and readiness wording. The same CAD PR is now draft, pending the owner planning-ledger placement decision. [Review disposition](CAD_REVIEW_DISPOSITION.md) records that block; [CAD_PLAN.md](CAD_PLAN.md) and [CAD_TASKS.csv](CAD_TASKS.csv) contain revised priorities, separate tooling estimates and explicit parked work. No CAD model or new measurement was produced. Original integrity-sprint tasks/evidence remain unchanged. Next work is limited to active input-register tasks and unresolved owner decisions, not the parked portfolio-wide CAD program.

## 2026-09-06 — CAD task amendment

Added [individual CAD work orders](CAD_PLAN.md) and [CAD_TASKS.csv](CAD_TASKS.csv), separating component modeling, fixtures, inspection and release deliverables. This is planning only: no CAD or physical task is complete. The original sprint ledger and evidence are unchanged. CAD branch: `plan/cad-tasks-20260906`; the PR supplies the committed source identity. Next CAD action: the first input-register task in the CAD ledger; owner-gated successors remain blocked. Verification of this amendment is recorded in [CAD_PLAN_CHECKS.md](CAD_PLAN_CHECKS.md).

## 2026-09-06 — Partial handoff

- Sprint start2026-09-05; canonical checkout `/Users/redhose/Developer/research-sprints/2026-09-05/Segmented-Shroud-Yield`.
- Branch `sprint/evidence-integrity-20260905`; HEAD/base `971eadb6b778c5fda764894235490dab2ad345e2`.
- Seven Agent tasks done with linked evidence; SSY-S08 blocked on: Rotor/stand selection, metrology access, fabrication and facility safety authority. No specimens are available in the baseline. Branch includes unmerged PR work.
- 7 tests passed in development and clean consumer environments; repository contract passed; 7/7 additional metadata cases matched.
- [Final checks](../evidence/sprint-2026-09-05/final-checks.json), [candidate](../evidence/sprint-2026-09-05/candidate.json), [original expectations](../evidence/sprint-2026-09-05/evaluation-plan.md), [outcomes](../evidence/sprint-2026-09-05/evaluation.json).
- These are developer software checks; no physical/new scientific results. Catan's real-data arm, where applicable, stays blocked despite its software fallback evaluation.
- Handoff was prepared before commit; the PR records the final commit and push. Original user changes remain untouched.
- Next verification command: `python evidence/sprint-2026-09-05/evaluate_candidate.py`.
- Exact next task: Owner resource choice, then long-term SSY-01 exact-gap closeout and rigid-defect metrology/CAD work order.
- One-time ID disambiguation: sprint SSY-01…08 became SSY-S01…S08 to avoid collisions with the unchanged long-term backlog. Only this CSV holds sprint statuses.
- Owner action moved to Day1 (2h); Day1 now7h, Day6 now2h, total30h. External turnaround is not accelerated.

## Baseline and interrupted execution

Baseline commands, outputs and identity remain in [evidence](../evidence/sprint-2026-09-05/baseline.json). Plans were saved before behavior changes. Runtime-limit pauses were followed by resuming the existing worktree; no baseline or external reply was invented. Original failing cases and corrected behavior are linked in [REVIEW_READY.md](REVIEW_READY.md).
