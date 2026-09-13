# SSY-D04 — provenance-clean re-acquisition of the D02 database export, 2026-09-11

**What this closes:** the D02 provenance defect. The 2026-09-09 export retained
50 rows whose query tag had no successful logged request (hits from one run were
merged with the query log of another). This directory is one clean run of the same bounded
protocol from a non-throttled network: every retained row traces to a logged successful
query **in this run**, and every query leg completed.

**What this does not close:** screening (all candidates remain UNSCREENED), search recall as a
ratio (the eligible anchor register is still incomplete, so `recall` stays `null`), patent
review (no patent database is reachable), the parent novelty task, and every owner gate.

## Observed

| Item | Observed |
| --- | --- |
| protocol | `2026-09-09-review-1` (new bounded acquisition; not a replay of the 09-09 export) |
| retrieved (UTC) | 2026-09-11T18:04:05Z |
| query legs | 18 total; 18 ok, 0 incomplete |
| identifier records retained | 451 (normalized identifiers, not distinct studies) |
| rows without a successful logged query | **0** (historical 09-09 export: 50) |
| known D01 anchors present | 3 of 3 comparable (`doi:10.1016/j.ast.2023.108866`, `doi:10.1155/2017/4168150`, `doi:10.2322/tjsass.60.1`); historical export: 3 of 3 |
| overlap with the historical 09-09 identifier set | 407 of 499 historical ids reappear; 44 new, 92 not re-observed |
| candidates listed, all UNSCREENED | 25 (keyword triage score >= 4, anchors excluded) |
| patents | not queried — no patent database reachable |

Anchor overlap is a bounded identifier-overlap observation, not recall: the denominator is the
known comparable anchor set, which the 09-09 review found incomplete. Counts drift as the
databases grow; the provenance property (0 unlogged rows) is the reproducible fact.

### Query legs, in the order executed

| db | query | status | n |
| --- | --- | --- | --- |
| crossref | `ducted fan non-uniform tip clearance experimental` | ok | 40 |
| openalex | `ducted fan non-uniform tip clearance experimental` | ok | 50 |
| crossref | `ducted fan tip clearance ovality` | ok | 40 |
| openalex | `ducted fan tip clearance ovality` | ok | 50 |
| crossref | `segmented shroud rotor duct seam aerodynamic` | ok | 40 |
| openalex | `segmented shroud rotor duct seam aerodynamic` | ok | 15 |
| crossref | `tip clearance optical capacitive measurement fan blade` | ok | 40 |
| openalex | `tip clearance optical capacitive measurement fan blade` | ok | 50 |
| crossref | `foldable duct propeller rotor` | ok | 40 |
| openalex | `foldable duct propeller rotor` | ok | 50 |
| crossref | `non-axisymmetric tip clearance rotor performance` | ok | 40 |
| openalex | `non-axisymmetric tip clearance rotor performance` | ok | 50 |
| arxiv | `ducted fan tip clearance` | ok | 0 |
| arxiv | `non-uniform tip clearance` | ok | 0 |
| arxiv | `segmented shroud rotor` | ok | 0 |
| arxiv | `tip clearance optical measurement blade` | ok | 0 |
| arxiv | `foldable duct propeller` | ok | 0 |
| arxiv | `non-axisymmetric tip clearance` | ok | 0 |

The 6 arXiv legs with `n = 0` are genuine zero-result queries, not disguised
throttling: each was re-issued independently with `max_results=1` on 2026-09-11 and the feed's
`opensearch:totalResults` was 0 in every case. The tool ANDs every term (`all:t1 AND all:t2 ...`),
which is restrictive by design; loosening the query set would be a protocol amendment, not a fix.

## Files (sha256)

| file | sha256 |
| --- | --- |
| `database-export.json` | `0ea6946272a3386ad6c9082e855b0d51107698f8634b11ca787e68ee03f41279` |
| `database-export.csv` | `0922773bc6e1927eabc1108b4e2448fab74de0922a65a40e9093acee5fa41d5f` |
| `candidates-unscreened.csv` | `7c21e741e170ccb87ff1d270d0fc2050673d3e3001f738a1df8771749fe32229` |
| `export-audit.json` | derived offline from `database-export.json` by `rerun_search.py --audit` |

## Reproduce and verify

```sh
# offline audit of this acquisition (expected exit 0; 0 unlogged rows)
python evidence/task-2026-09-09/rerun_search.py --audit evidence/task-2026-09-11/database-export.json
# regression test pinning the property
python -m unittest discover -s tests -p test_search_export.py -v
python scripts/check_repo_contract.py
# a NEW acquisition (path must not exist; OPENALEX_API_KEY in env, never in a committed command)
OPENALEX_API_KEY=... python evidence/task-2026-09-09/rerun_search.py --out evidence/task-<date>
```

## Relationship to the historical export and the day-3 ledger

The 09-09 export, CSV and candidate list are unchanged. The day-3 acquisition ledger
(`scripts/acquisition_ledger.py`, `evidence/task-day3-2026-09-09/acquisition-ledger.json`)
still reads the historical export and is **not** regenerated from this one: merging rows from
two runs is the defect this directory corrects. Any future ledger that consumes this export must
consume it whole, with its own query log, as a separately dated route.

Run from the sandbox on 2026-09-11 with Python 3 and no credential value written to disk or logs.
