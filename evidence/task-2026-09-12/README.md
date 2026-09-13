# SSY-R02 — reference coverage and seam-experiment distinctness — 2026-09-12

Branch `audit/reference-coverage-20260912` off `main` 9cb827e. Deliverable: [docs/reference-coverage-2026-09-12.md](../../docs/reference-coverage-2026-09-12.md).

## What was done
- `docs/source-eligibility-register.json`: all 10 day-1 sources, identifiers resolved (Crossref works/alternative-id, OpenAlex, PMC header), explicit eligibility each. S2's DOI is 10.1016/j.ast.2023.108866 (day-1 PII …7624 vs Crossref …7629, recorded); S3's is 10.1016/j.ast.2026.111933; S6's is 10.3390/s18082610.
- `scripts/reference_coverage.py` + `tests/test_reference_coverage.py` (6 tests; negative control: removing a source from the register fails 2).
- `docs/day3-reading-records.json`: S1 re-read in full text (uniform t/h sweep, baseline-only measurement), S6 full text, S4 and S5 complete abstracts, S3 inaccessible with failed routes listed, S7/S9/S10 stand on day-1 reads. The day-3 S4 record is retained inside the new one as `supersedes_day3_record`.
- Acquisition ledger regenerated (derives from the records). Ledger: SSY-R02 → done; SSY-D02 untouched.

## Finding
Recall over the six eligible sources is **4/6 for both exports** (reported 1/6 and 3/3). Both misses are MDPI items, including the paper actually titled "segmented ducted fan" — which on reading is **axial** duct spacing by CFD, not circumferential seams at equal mean clearance. Distinctness holds against all accessible sources; S3 and S2 full texts could still collapse axis 1 and are paywalled.

## Checks observed (repo root on PYTHONPATH, as the test modules import `scripts.`)
| command | observed |
|---|---|
| `PYTHONPATH=. python -m unittest discover -s tests` | Ran 36, OK (6 new) |
| `python scripts/check_repo_contract.py` | PASS |
| `python scripts/reference_coverage.py --check` | OK 4/6, 4/6 |
| `python scripts/acquisition_ledger.py --check` | consistent |

## Not done / not reachable
mdpi.com 403 to this client (not circumvented); sciencedirect landing paywalled; downloads.hindawi.com http-only host unreachable; ntrs.nasa.gov and patents.google.com not on the allowlist. No novelty, patent or owner gate closed; no apparatus, specimen or measurement.

## Review repair (SSY-R02b, same day)
- `scripts/reference_coverage.py` is provenance-bound: hits without a logged successful query are excluded from credit and enumerated; canonical export = `day4_public`, rejected = `['day2_historical']`. Recall unchanged (no anchor was untraceable); the record now says what it can show.
- Novelty-axis table generated from the reading records: each axis is `narrowed_by_disclosure` / `supported_bounded` / `unresolved`, with the sources in each state named. Abstract-only and inaccessible sources never count as support.
- `SSY-D02` reconciled and closed against this single record; no successor row.
- `scripts/clearance_uncertainty_budget.py` + `docs/clearance-measurement-budget.csv` + `tests/test_clearance_budget.py`: Stage A stop rule as a fail-closed computation; literature sensor bounds excluded from the combination; verdict `INPUTS_PENDING` (7 terms), record committed and `--check`-gated.

## Review repair 2 (SSY-R02c, 2026-09-13)
Review 2 substituted an identifier absent from a raw response: the coverage checker credited it while the existing native audit caught it. `reference_coverage.py` now **reuses `rerun_search.audit_export`** on every export; an export that fails it (unsupported provenance routes, missing request provenance, response-record or response-hash mismatch, unlogged rows) is credited for nothing and the record carries each export's SHA-256, so `--check` is bound to exact input bytes. Consequence stated plainly: the 2026-09-09 export fails the audit ({'unsupported_provenance_routes': 50, 'missing_request_provenance': 12, 'query_count_mismatches': 12, 'rows_without_successful_logged_query': 50}) and its recall is **0/6**, not 2/6 — the earlier figure was overlap with rows the export cannot show it retrieved. The public export passes (450/450) and stays canonical at 4/6.
Reading records now carry an explicit `axis_states` field (disclosed_or_addressed | not_found_in_inspected | not_applicable | unresolved); the classifier reads only that field, and blank, unrecognised, or locator-less assessments are unresolved. Tests: invented identifier not credited; `--check` bound to export bytes; blank/unknown/locator-less assessments unresolved.
