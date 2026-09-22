# Thematic literature extension — 2026-09-22

Additive search into eight themes the frozen 2026-09-09 query set never reached. It **does not
amend or replace** that query set or any existing export; those remain byte-identical.

Review built from it: [docs/literature/README.md](../../docs/literature/README.md). Catalogue:
[docs/literature/register.json](../../docs/literature/register.json).

## What was run

The repository's existing search machinery was reused rather than a second searcher written, so
every record carries the same provenance the earlier exports do: raw response text, a response
hash, a per-query rank, and a query log that distinguishes an error from a genuine zero.

| item | value |
| --- | --- |
| query legs | 34 (17 queries x crossref, openalex) across 8 themes |
| legs successful | 33 |
| legs failed | 1 |
| distinct identifier records | 1,377 |
| export sha256 (uncompressed) | `d055b43fec457b157bbfeba57c592a69a1bd8dd227f2aa982ba74adce2b77343` |
| export sha256 (committed, gzipped) | `9fb30cafe177e3cd96288870466e4d214b3c5a686169f8721c61f0fed0c306b7` |

The export is committed gzipped because uncompressed it is 3.4 MB, above the 1 MB single-file
threshold in the work order's data policy and three times the largest existing committed export.
Gzipped it is 544 KB.

## The failed leg

`openalex` / `rotor guard impact protection unmanned aerial vehicle` returned **HTTP 429**. It is
recorded with `status: error` and `http_status: 429`, not as a zero-result query. The guard theme
is therefore under-sampled, and the review says so rather than presenting its 112 records as
coverage.

Both Crossref and OpenAlex were rate-limiting this machine during the run. A parallel process on
the same host was issuing the same class of request, which is the likely cause. The consequence
for the catalogue is that **citation counts could not be retrieved at all**, so nothing in the
review is ranked by impact.

## Audit

`rerun_search.audit_export` on the result, all six failure keys zero:

```json
{
  "unsupported_provenance_routes": 0,
  "missing_request_provenance": 0,
  "response_record_mismatches": 0,
  "query_count_mismatches": 0,
  "response_hash_mismatches": 0,
  "rows_without_successful_logged_query": 0
}
```

Every retained row traces to a logged successful query in the same run, and every retained raw
response hashes to its recorded digest.

## Reproduce

```sh
gunzip -c evidence/task-literature-2026-09-22/database-export.json.gz > /tmp/lit-export.json
python evidence/task-2026-09-09/rerun_search.py --audit /tmp/lit-export.json
python scripts/literature_register.py --extension <dir containing database-export.json> \
       --out docs/literature/register.json
python -m unittest discover -s tests -p 'test_literature_register.py' -v
```

Re-running the search will not reproduce these bytes: database relevance ordering and indexed
content both change. The hashes establish what was actually retrieved on this date, not a
repeatable query result.

## Claim boundary

This is candidate identification. **Of the 1,377 records, none was read.** Eleven records in the
merged catalogue have close readings, and all eleven come from earlier work. Nothing here
establishes novelty, closes SSY-01, or supports any statement about what a paper contains.
