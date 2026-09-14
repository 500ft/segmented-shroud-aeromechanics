# Day plan — 2026-09-14

Status: draft, for owner review. Build starts only after this PR is edited and merged.
Base: `main` after PR #14 (`bfde78c`). Branch for the build: `task/day-2026-09-14`.
Status of every task lives only in [SPRINT_TASKS.csv](../../SPRINT_TASKS.csv); this file is the work order, not a ledger.

## Outcome for today

Close the scholarly leg of SSY-01 by screening every unscreened database candidate under the committed rubric, and give the owner a measurement-system specification that needs only two numbers to become the Stage A gate. No hardware, no fabrication, no spending, no outreach, no novelty claim beyond the inspected set.

## Baseline (verified before this plan was written)

- 54 tests OK; `check_repo_contract` PASS; all three `--check` gates OK; presentation checker 0 issues; main CI green.
- Unscreened candidates: **25**, all in [candidates-unscreened.csv](../../../evidence/task-2026-09-11-public/candidates-unscreened.csv). The D04 export's candidate file holds the same 25 identifiers. 20 carry a publisher abstract; 5 are title-only.
- Ledger: every sprint row is `done` except SSY-S08 (Owner, blocked).

## Decisions the owner must confirm or change in this PR

These are design choices the build would otherwise make silently. Edit the line, or leave it to accept the default.

- **D1. Screening record location.** Default: one new file `docs/candidate-screening-2026-09-14.json`, one record per candidate, same field names as [day3-reading-records.json](../../day3-reading-records.json). Records are **not** appended to the day-3 file, because that file feeds `reference_coverage.py` and would silently change the committed 2026-09-12 coverage record. Feeding screened candidates into the novelty-axis table is a separate, later task with its own dated evidence folder.
- **D2. Screening decision vocabulary.** Default: `include_for_close_reading`, `exclude_off_topic`, `exclude_metadata_only` (title-only and no open full text, left explicitly unresolved, never counted as absence). Every `include` carries a locator; every `exclude` carries a one-line reason.
- **D3. Access rule.** Default: open routes only (publisher abstract, OA PDF, arXiv). A 403 or paywall is recorded as `inaccessible`, not worked around. Same rule as 2026-09-12.
- **D4. Check for the screening.** Default: one test file, `tests/test_candidate_screening.py`, no new script. It asserts every candidate id in the export has exactly one record, every decision is in the D2 vocabulary, and every include has a locator. Smallest check that fails if the screening is incomplete.
- **D5. SSY-01 closeout wording.** Default: SSY-01 moves to `blocked` on the patent leg, not `done`: no patent database is reachable from this environment, and the task's done-condition requires a dated patent search. The scholarly leg is recorded as complete. If the owner has patent-database access, say so here and T12 changes.
- **D6. Specification file.** Default: `docs/measurement-system-spec.md`, cross-linked from [experiment-01](../../experiment-01-rigid-defect-duct.md) Stage A and from [clearance-measurement-budget.csv](../../clearance-measurement-budget.csv). The two owner numbers stay as explicit `owner_decision: pending` placeholders.

## Owner actions, independent of the build

Each is a short written entry. None requires the lab.

- **O1.** [clearance-measurement-budget.csv](../../clearance-measurement-budget.csv): fill `minimum_effect_of_interest` (value, unit `um`, `evidence_state` = `owner_decision`, source = your reasoning or protocol reference). Then run `python scripts/clearance_uncertainty_budget.py` to regenerate the record.
- **O2.** Same file: `target_mean_clearance`, same procedure.
- **O3.** XC-02: record the repository's first-public date and the chosen disclosure path in [decision-log.md](../../decision-log.md). Every CAD task is parked behind this.
- **O4.** SSY-S08: a provisional rotor/stand/metrology entry in the ledger blocker column, even if marked provisional.

## Tasks

Sizing: each task is one concern, 5–20 minutes of focused work. `Done when` is a command or an observable artifact.

### [ ] T00 — Environment check
- Files: none
- Do: from a clean checkout of `main`, run the gate and record the exact outputs in `evidence/task-2026-09-14/README.md` (create the folder).
- Done when: all of these exit 0 and their first output lines are pasted into the README.
  ```
  python3 -m unittest discover -s tests
  python3 scripts/check_repo_contract.py
  python3 scripts/reference_coverage.py --check
  python3 scripts/acquisition_ledger.py --check
  python3 scripts/clearance_uncertainty_budget.py --check
  ```

### [ ] T01 — Freeze the screening rule before reading
- Files: `evidence/task-2026-09-14/README.md` (modify)
- Do: copy D2 and D3 verbatim into the README under "Screening rule, frozen before reading", with the UTC timestamp and the SHA-256 of the candidate CSV.
- Depends on: T00
- Done when: the README section exists and `shasum -a 256 evidence/task-2026-09-11-public/candidates-unscreened.csv` matches the recorded hash.

### [ ] T02 — Skeleton screening records
- Files: `docs/candidate-screening-2026-09-14.json` (new)
- Do: one record per candidate id from the CSV, fields `source_id` (the export id), `title`, `url`, `year`, `triage_score`, `access: "not_attempted"`, `decision: ""`, `reason: ""`, `locator: ""`, `aboutness: null`, `axis_states: {}`, `retrieved_on: ""`. Generate with a ten-line inline Python snippet recorded in the README; no script file.
- Depends on: T01
- Done when: `python3 -c "import json,csv; a={r['id'] for r in csv.DictReader(open('evidence/task-2026-09-11-public/candidates-unscreened.csv'))}; b={r['source_id'] for r in json.load(open('docs/candidate-screening-2026-09-14.json'))}; assert a==b and len(b)==25"` exits 0.

### [ ] T03 — Screening test
- Files: `tests/test_candidate_screening.py` (new)
- Do: per D4. Three assertions: id set equals the CSV; every `decision` in the vocabulary and non-empty; every `include_for_close_reading` has non-empty `locator` and `access` in `{full_text_pdf, publisher_indexed_abstract, arxiv_full_text}`.
- Depends on: T02
- Done when: `python3 -m unittest tests.test_candidate_screening` **fails** on the skeleton (empty decisions) and the failure message names the first unscreened id.
- Parallel group: A

### [ ] T04 — Screen candidates 1–5 (by triage score, descending)
- Files: `docs/candidate-screening-2026-09-14.json` (modify)
- Do: for each: open the URL by an open route; set `access`, `retrieved_on`, `decision`, `reason`, `locator`, `aboutness` 0–3 per the [rubric](../../day3-reading-rubric.md). For includes, fill `axis_states` using only the nine axis names already in the day-3 records, values from `{disclosed_or_addressed, not_found_in_inspected, not_applicable, unresolved}`. Abstract-only sources may not receive `disclosed_or_addressed` for a negative claim.
- Depends on: T03
- Done when: those 5 records have non-empty `decision`; T03 still fails only on ids 6–25.
- Parallel group: B

### [ ] T05 — Screen candidates 6–10
- Same as T04. Parallel group: B

### [ ] T06 — Screen candidates 11–15
- Same as T04. Parallel group: B

### [ ] T07 — Screen candidates 16–20
- Same as T04. Parallel group: B

### [ ] T08 — Screen candidates 21–25 (includes the 5 title-only)
- Same as T04. Title-only with no open full text: `decision: exclude_metadata_only`, `access: inaccessible` or `metadata_only`, reason states what was attempted.
- Parallel group: B
- Done when: `python3 -m unittest tests.test_candidate_screening` passes.

### [ ] T09 — Screening summary table
- Files: `docs/prior-art-search-2026-09-14-screening.md` (new)
- Do: one markdown table, 25 rows: id, title, year, access, decision, reason/locator, aboutness. Below it: counts per decision, the list of includes, and the sentence "Screening is relevance triage under the day-3 rubric; it is not novelty clearance and not a patent search."
- Depends on: T08
- Done when: `python3 scripts/check_repo_contract.py` passes (all links resolve) and the row count equals 25.

### [ ] T10 — Update the day-1 prior-art record
- Files: `docs/prior-art.md` (modify)
- Do: add a dated section "2026-09-14 database-candidate screening" linking T09, stating search strings are the frozen 18 (db, query) legs already in the export, inclusion rules per D2, and the scholarly-leg conclusion in the TASKS.md wording: "supported candidate gap" or "prior art found", per axis, bounded to the inspected set.
- Depends on: T09
- Done when: the section exists and contains one of the two required phrases verbatim.

### [ ] T11 — Included candidates handed to close reading
- Files: `evidence/task-2026-09-14/README.md` (modify)
- Do: list every `include_for_close_reading` id with its locator under "Close-reading queue (not read today)". This is the input to the later axis-table reconciliation (see D1). Do not modify `day3-reading-records.json`.
- Depends on: T08
- Done when: the list matches `[r for r in records if r['decision']=='include_for_close_reading']`.

### [ ] T12 — SSY-01 ledger disposition
- Files: `docs/SPRINT_TASKS.csv` (modify), `docs/TASKS.md` (modify)
- Do: add row `SSY-R03`, day `2026-09-14`, P1, Agent, depends on `SSY-R02`, task "Screen all unscreened database candidates under the day-3 rubric", deliverable T09's file, verification `python3 -m unittest tests.test_candidate_screening`, estimate 3, status `done`, evidence `evidence/task-2026-09-14/README.md`, blocker per D5: "Scholarly leg complete. SSY-01 remains open on the patent leg: no patent database reachable from this environment." In TASKS.md under SSY-01, add the dated sentence with the same content.
- Depends on: T10, T11
- Done when: `python3 -c "import csv; rows=list(csv.DictReader(open('docs/SPRINT_TASKS.csv'))); assert any(r['id']=='SSY-R03' for r in rows)"` exits 0 and the contract check passes.

### [ ] T13 — Measurement-system specification: channels and limits
- Files: `docs/measurement-system-spec.md` (new)
- Do: per D6. Sections: purpose (one paragraph: this is SSY-02's committed specification; Stage A gate; PASS/FAIL precedes performance runs); channel table with columns channel, quantity, range, max allowable bias, max allowable repeatability, resolution, calibration reference, evidence state. Channels: dynamic tip clearance, thrust, electrical power (V, I), RPM, ambient and duct temperature, vibration, condition alignment. Every numeric limit that is not yet decided is written as `owner_decision: pending`, never a placeholder number.
- Depends on: T00
- Parallel group: A

### [ ] T14 — Specification: qualification procedure
- Files: `docs/measurement-system-spec.md` (modify)
- Do: sections: warm-up and drift test (repeated reference runs, acceptance in terms of the pending MEI); synchronization tolerance between clearance, RPM and thrust channels; dynamic-clearance method shortlist restated from the day-3 source review (S5/S6 class sensors) with the sentence that a literature bound never enters the budget; sample unit definition (specimen/condition/run); PASS/FAIL rule quoting `k * u_c < minimum_effect_of_interest` and linking the budget script.
- Depends on: T13
- Done when: the file links to `experiment-01-rigid-defect-duct.md`, `clearance-measurement-budget.csv` and `day3-source-review.md`, and the contract check passes.

### [ ] T15 — Specification check
- Files: `tests/test_measurement_spec.py` (new)
- Do: one test: every `term` in `clearance-measurement-budget.csv` appears verbatim in `docs/measurement-system-spec.md`, so the spec and the budget cannot drift apart silently.
- Depends on: T14
- Done when: `python3 -m unittest tests.test_measurement_spec` passes.

### [ ] T16 — Cross-links and ledger row for the spec
- Files: `docs/experiment-01-rigid-defect-duct.md` (modify, one link line under Stage A), `docs/SPRINT_TASKS.csv` (modify)
- Do: add row `SSY-R04`, day `2026-09-14`, P1, Agent, depends on `SSY-R02`, task "Draft the SSY-02 measurement-system specification with owner numbers pending", status `blocked`, blocker "Owner numbers pending: minimum_effect_of_interest, target_mean_clearance (O1, O2). Spec complete otherwise."
- Depends on: T15
- Done when: contract check passes; the CSV row parses.

### [ ] T17 — Progress and review index
- Files: `docs/SPRINT_PROGRESS.md`, `docs/REVIEW_READY.md` (modify, one dated section each)
- Do: same shape as the 2026-09-11 sections: what was done, what remains open, links to evidence. State plainly: 25 screened, N included, SSY-01 open on patent leg, SSY-02 spec blocked on two owner numbers.
- Depends on: T12, T16
- Done when: contract check passes.

### [ ] T18 — Integration
- Files: `evidence/task-2026-09-14/README.md` (modify)
- Do: run the full gate plus the two new tests; paste outputs; run `git diff --check`; commit as configured, push `task/day-2026-09-14`, open one PR to main with the PR body listing every decision D1–D6 as it was actually applied.
- Depends on: T17
- Done when: CI `verify` is green on the PR.

## Not today

- Close reading of included candidates and the novelty-axis reconciliation (needs a new dated coverage record; separate work order).
- SSY-05 analysis pipeline. Backlog order puts it after SSY-02 and SSY-03; SSY-02 is blocked on O1/O2 until the owner writes them.
- Any CAD task (parked on XC-02, O3).

## Traceability

| Requirement | Source | Tasks |
|---|---|---|
| Every candidate screened with a stated reason | SSY-R02 blocker; day-3 rubric | T02–T08 |
| Screened and unscreened remain distinguishable | day-3 rubric provenance rule | T01, T03, T11 |
| Abstract-only sources cannot establish negatives | day-3 rubric | T04 rule, T08 |
| SSY-01 "supported candidate gap / prior art found" wording | TASKS.md SSY-01 done-when | T10 |
| Dated search strings and inclusion rules in prior-art.md | TASKS.md SSY-01 done-when | T10 |
| Patent search | TASKS.md SSY-01 done-when | not reachable; D5, T12 |
| Committed measurement specification, every channel | TASKS.md SSY-02 done-when | T13, T14 |
| PASS/FAIL MSA precedes performance runs | experiment-01 Stage A | T14 |
| Literature bound never enters the budget | review 2026-09-12 | T14, T15 |
| Status only in the ledger | SPRINT_ROADMAP | T12, T16 |

## Execution notes

- Group A (T03, T13) can start while T02 is being generated. Group B (T04–T08) is five independent reading batches and can be split across subagents; each batch edits disjoint records in the same JSON file, so merge by id, never by line.
- Risk: candidate URLs that 403. Record and move on; do not spend more than two access attempts per candidate.
- Checkpoint after T08: if fewer than 3 candidates are included, say so before writing T10; a near-empty include list is a finding, not a failure.
- Estimated focused time: screening 2.5 h, spec 1.5 h, ledger and integration 1 h.
