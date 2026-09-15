# Task 2026-09-14 — top-25 candidate triage and measurement-requirements draft

Executed: 2026-09-15 (the directory keeps the work-order date). Work order: [plan](../../docs/specs/day-2026-09-14/plan.md) as merged to `main` in PR #16, revision `cfc45f1`. Build branch: `task/day-2026-09-14` from `cfc45f1`.

Interpreter: `/Users/redhose/ENTER/bin/python`, Python 3.11.8, jsonschema 4.26.0. Worktree clean at start: NO.

Nothing in this folder is a measurement, a novelty verdict, or a patent search. It records a triage of 25 retained database records under a rule frozen before reading, and a requirements draft whose inputs are still open.

## T00 — baseline command log (2026-09-15T18:23:17Z)

| command | exit | first line of output |
| --- | ---: | --- |
| `python -m unittest discover -s tests -v` | 0 | Ran 54 tests in 0.654s OK  |
| `python scripts/check_repo_contract.py` | 0 | Repository contract: PASS |
| `python scripts/reference_coverage.py --check` | 0 | reference coverage OK: {"day2_historical": "0/6", "day4_public": "4/6"} |
| `python scripts/acquisition_ledger.py --check` | 0 | Acquisition ledger consistent; source provenance gaps remain explicit |
| `python scripts/clearance_uncertainty_budget.py --check` | 0 | budget record OK: INPUTS_PENDING |
| `python evidence/task-2026-09-09/rerun_search.py --audit evidence/task-2026-09-11-public/database-export.json` | 0 | {'unsupported_provenance_routes': 0, 'missing_request_provenance': 0, 'response_record_mismatches': 0, 'query_count_mismatches': 0, 'response_hash_mismatches': 0, 'rows_without_successful_logged_query': 0, 'record_count': 450} |
| `python tools/check_presentation.py . "Segmented Shroud Aeromechanics" segmented-shroud-aeromechanics` | 0 |  "local_links_checked": 79, "issues": [], |
| `python tools/test_presentation.py` | 0 | .... |
| `git diff --check` | 0 | (no output) |

The budget verdict is `INPUTS_PENDING` with seven pending terms; a green `--check` means that pending record is reproducible, not that anything is qualified.

## T01 — corpus and procedure frozen before any candidate inspection

Screening rule: sections **D1, D2 and D3** of the merged plan, applied verbatim; the rule text is not copied here so that the plan revision above stays the single source. Inspection order: the frozen `candidate_ids` order below (exporter order `(-triage_score, id)`).

| input | value |
| --- | --- |
| candidate CSV | `evidence/task-2026-09-11-public/candidates-unscreened.csv` sha256 `184c3fb682af669e8e00c994809174e63d6b4c1d4b8aced43bc3c914180eacd1` |
| canonical export | `evidence/task-2026-09-11-public/database-export.json` sha256 `d7ca70193a82f67eea761b5dec3becfd9a71f2919d922f7801e4e836da5bad52` |
| native audit of the export | passed: unsupported_provenance_routes=0, missing_request_provenance=0, response_record_mismatches=0, query_count_mismatches=0, response_hash_mismatches=0, rows_without_successful_logged_query=0 |
| export identifier records | 450 |
| qualifying for the exporter's rank filter (non-anchor, triage_score >= 4) | 136 |
| selected (first 25 in exporter order) | 25 |
| qualifying but unselected | 111 |
| outside the rank-filter population | 314 |
| selection reproduces from the export | True |
| title-only rows (frozen positions) | [2, 3, 10, 11, 12] |
| abstracts at the exporter's 1,500-character cap | 4 |
| D04 candidate file `evidence/task-2026-09-11/candidates-unscreened.csv` | same 25 identifiers, different bytes; contributes no identifier and is not spliced into this triage |

Frozen ordered `candidate_ids`:

1. `doi:10.1115/gt2020-15403`
2. `doi:10.1016/j.heliyon.2024.e25296`
3. `doi:10.1016/j.measurement.2024.115777`
4. `doi:10.1063/1.4964858`
5. `doi:10.1115/1.3230742`
6. `doi:10.1115/2000-gt-0416`
7. `doi:10.1115/78-gt-164`
8. `doi:10.1115/91-gt-164`
9. `doi:10.1115/gt2022-82750`
10. `doi:10.2139/ssrn.4820937`
11. `doi:10.1088/0957-0233/11/7/303`
12. `doi:10.1109/imtc.2002.1007093`
13. `doi:10.1115/1.4023468`
14. `doi:10.1115/96-ta-001`
15. `doi:10.1115/97-gt-406`
16. `doi:10.1115/gt2004-53563`
17. `doi:10.1115/gt2011-46356`
18. `doi:10.1243/jmes_jour_1974_016_070_02`
19. `doi:10.1088/1361-6501/ad915f`
20. `doi:10.1088/1742-6596/2428/1/012032`
21. `doi:10.1088/1742-6596/2820/1/012030`
22. `doi:10.1115/1.2777187`
23. `doi:10.1115/1.2814098`
24. `doi:10.1115/1.4023469`
25. `doi:10.1115/89-gt-82`

Historical files that this task must leave byte-identical: `docs/day3-reading-records.json`, `docs/source-eligibility-register.json`, `docs/clearance-measurement-budget.csv`, every folder under `evidence/` dated before 2026-09-14, and their derived records.

## T02 — skeleton record

`docs/candidate-screening-2026-09-14.json` initialised from the CSV with `rule_commit` = `d69cd98596081bf2c137f445c954fd74a85d450d` (the T01 freeze commit). Snippet used (standard library only):

```python
rows=list(csv.DictReader(open(P,newline='',encoding='utf-8')))
doc=dict(metadata=dict(schema_version=1, candidate_csv_path=P, candidate_csv_sha256=sha(P), export_path=E, export_sha256=sha(E),
    rule_commit=FREEZE, candidate_ids=[r['id'] for r in rows], screening_scope="ranked_top_25"),
  records=[dict(source_id=r['id'], title=r['title'], year=r['year'], triage_score=int(r['triage_score']), decision=None, reason="",
                aboutness=None, basis=None, locator=None, screened_utc=None, access_attempts=[], possible_related_ids=[]) for r in rows])
```
No skeleton counts as screened.

## T05 — dispositions (2026-09-15T18:27:57Z)

All 25 dispositions were made from the retained canonical export (title, or the retained abstract treated as an excerpt). No network retrieval was needed: every title-only record carried a title that either clearly named the measurand or method (queued for close reading, D2) or was resolved from its retained metadata, so `access_attempts` is empty for all 25. Locators bind each decision to `hits[id=<id>].<field>` of the export by path and SHA-256. Counts: 22 `include_for_close_reading`, 3 `exclude_off_topic`, 0 `defer_insufficient_evidence`.

## T06 — self-review of exclusions and inclusions

Self-review by the same agent, not an independent reviewer.

- Exclusions (3): `doi:10.1115/91-gt-164` (turbine hot-section structural design; the unnamed measurement technique is incidental), `doi:10.1088/1742-6596/2820/1/012030` (folding propeller blade, no duct or clearance), `doi:10.1115/89-gt-82` (nozzle-vane clearance in a radial turbine). Each rests on retained abstract text that positively describes an off-topic subject; none rests on missing access. Re-read and confirmed.
- Deferrals: none. The five title-only records all had titles naming the measurand or method directly, so D2's title-based inclusion applied; none was ambiguous.
- Inclusion overclaims checked: aboutness 3 was given once (`doi:10.1115/97-gt-406`), on excerpt text stating that stall-margin loss exceeded the average-clearance estimate; the reason records that equal mean clearance is not established by the excerpt. All other includes are 2 or below, or null for title-only.
- Possible duplicate counting: two clusters flagged in `possible_related_ids` and in the report, the Measurement/SSRN pair and the ducted-fan VTOL Part I journal/conference pair with its Part II; 22 includes are at most 19 distinct studies pending close reading. No identifier was removed.

## T07/T08 — report and queues

`docs/prior-art-search-2026-09-14-screening.md` is rendered from the JSON by an inline snippet (rows from `records`, counts from `Counter(decision)`, queue tiers assigned by id and asserted equal to the include set). Rendering asserts the three tiers partition the include set exactly; deferred queue is empty because no record was deferred. The 111 unselected qualifying records, the S2/S3 reading gaps and the patent search are listed as separate, unperformed work.

## T16 — review of the requirements draft as an experiment contract

Self-review against every SSY-02 done-condition and each D6 requirement. "Satisfied as draft" means the requirement is stated with structure and an assigned input; nothing here is frozen or installed.

| requirement | state | where | next action |
| --- | --- | --- | --- |
| minimum resolvable defect effect | unresolved, assigned | spec §5 IN-01 | owner value with rationale |
| minimum resolvable performance effect (power at matched thrust) | unresolved, assigned; endpoint defined dimensionally | spec §1.1, §4.6, IN-03 | owner target; agent derives channel limits |
| max allowable bias and repeatability, every channel | satisfied as draft: 12 rows with statistic and method; limits assigned to IN-01/IN-03/IN-05 | spec §2 | allocation after IN-01, IN-03 |
| calibration references | satisfied as draft: per channel, traceable references named; availability pending IN-04 | spec §2, §4.2 | confirm references exist at facility |
| warm-up and drift tests | satisfied as draft; durations, N and limit pending IN-12 | spec §4.3 | propose values from rotor envelope |
| synchronization tolerance | satisfied as draft; limit and oversampling pending IN-11 | spec §2 timing row, §4.5 | derive from blade-passage frequency |
| dynamic-clearance method | shortlist only; selection pending IN-09; inclusion map of contributors required | spec §1.4, §2, IN-09 | choose after instrument-feasibility reads |
| sample unit | satisfied as draft | spec §1.6 | register aggregation before confirmation |
| PASS/FAIL measurement-system analysis preceding performance runs | satisfied as draft: pass/stop/pending logic per procedure; installed execution is SSY-12 | spec §4, §5 release criteria | none until rig exists |
| difference uncertainty (equal-mean and ΔP) | satisfied as draft with covariance treatment stated | spec §4.5, §4.6 | numerical model in analysis pipeline |
| budget register mapping | satisfied and test-bound (9 rows, exact) | spec §3; `tests/test_measurement_spec.py` | none |
| missing-wall averaging domain | three admissible treatments; choice pending IN-08 | spec §1.3 | decide before Stage B |
| contact/dropout/invalid-run rules | options stated; rule pending IN-10 | spec §1.5 | decide before commissioning |

Neither the SSY-02 freeze nor a Stage A PASS is claimed. The two spec tests were re-run after the last table correction.

## T20 — integration and preservation checks (2026-09-15T18:30:05Z)

| command | exit | result |
| --- | ---: | --- |
| `python -m unittest discover -s tests -v` | 0 | Ran 65 tests in 1.068s OK  |
| `python -m unittest discover -s tests -p 'test_candidate_screening.py' -v` | 0 | Ran 9 tests in 0.339s OK  |
| `python -m unittest discover -s tests -p 'test_measurement_spec.py' -v` | 0 | Ran 2 tests in 0.001s OK  |
| `python scripts/check_repo_contract.py` | 0 | Repository contract: PASS |
| `python scripts/reference_coverage.py --check` | 0 | reference coverage OK: {"day2_historical": "0/6", "day4_public": "4/6"} |
| `python scripts/acquisition_ledger.py --check` | 0 | Acquisition ledger consistent; source provenance gaps remain explicit |
| `python scripts/clearance_uncertainty_budget.py --check` | 0 | budget record OK: INPUTS_PENDING |
| `python evidence/task-2026-09-09/rerun_search.py --audit evidence/task-2026-09-11-public/database-export.json` | 0 | rows_without_successful_logged_query=0, record_count=450 |
| `python tools/check_presentation.py . "Segmented Shroud Aeromechanics" segmented-shroud-aeromechanics` | 0 |  "local_links_checked": 79, "issues": [], |
| `python tools/test_presentation.py` | 0 | .... |
| `git diff --check` | 0 | (no output) |

Preservation against build base `cfc45f1` (must be empty):

```
(no differences)
```

Anchor check on new and modified documents (the contract checker strips fragments):

- 9 documents scanned, 0 missing anchors

Changed files in this build (vs base):

```
 M docs/REVIEW_READY.md
 M docs/SPRINT_PROGRESS.md
 M docs/SPRINT_TASKS.csv
 M docs/TASKS.md
 M docs/experiment-01-rigid-defect-duct.md
 M docs/prior-art.md
 M docs/specs/day-2026-09-14/plan.md
 M evidence/task-2026-09-14/README.md
?? docs/candidate-screening-2026-09-14.json
?? docs/measurement-system-spec.md
?? docs/prior-art-search-2026-09-14-screening.md
?? tests/test_candidate_screening.py
?? tests/test_measurement_spec.py
```
