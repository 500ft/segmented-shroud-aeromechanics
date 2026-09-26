# Literature repair, 2026-09-25

Review item R12. Four sources had their access status and evidence grading repaired. The record
is [docs/reading-records-2026-09-25.json](../../docs/reading-records-2026-09-25.json).

Historical reading records are unchanged. Coverage is updated by adding a dated file, never by
overwriting one bound to a hash.

## Routes attempted and what each returned

| source | route | outcome |
| --- | --- | --- |
| Akturk & Camci Part 1 | open conference-proceedings copy of GT2011-46356 | **obtained**, pages 1–6 audited; sha256 `45d08d6c…` |
| | ASME Digital Collection (journal version) | not attempted for full text; the publisher interstitial is not circumvented |
| Graf et al. | OpenAlex metadata | **success**: authors, venue and issue date 1998-10-01 verified |
| | green OA copy, DSpace@MIT `hdl:1721.1/104762` | **blocked** by a human-verification interstitial. Not circumvented |
| Cui et al. 2023 | publisher DOI redirect | landing page returned no metadata |
| | Semantic Scholar graph API | **success** for title, authors, venue, year; abstract not served |
| Heliyon 2024 | Europe PMC full text, recorded 2026-09-21 | unchanged; regraded only |

No access control, paywall or bot check was bypassed, and no credentials were used. Retrieved
PDFs are **not** committed: the record carries the route and a content hash instead.

## What did not change

Two failed retrievals stayed failures. Neither became an absence finding, and neither source may
be cited as read. Graf is the highest-priority remaining acquisition because its title indicates
experimental study of the exact comparison this project makes, which is a reason to obtain it, not
a licence to use it. A person can open the MIT copy in a browser.

SSY-01 is **not** closed by any of this. The 111 qualifying unselected records, the under-sampled
extension themes and the dated patent search are all still outstanding.
