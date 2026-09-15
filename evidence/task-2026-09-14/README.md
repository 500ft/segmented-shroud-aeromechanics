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
