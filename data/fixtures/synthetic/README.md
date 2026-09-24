# Synthetic fixtures

**SYNTHETIC TEST DATA - NOT EVIDENCE.**

Nothing here was measured. Every value comes from the closed-form generator in
`scripts/make_synthetic_fixtures.py`, so the correct answer is known before the pipeline
runs. These exist only to fix the analysis before any real data exists, which is the
point of backlog task SSY-05.

| case | what it is for |
| --- | --- |
| `positive` | equal mean clearance throughout, the design the project actually proposes; power depends on seam count and total opening beyond mean clearance |
| `varying-mean` | the same generator with mean clearance deliberately varied, so the clearance-slope baseline is identifiable and both baseline forms are exercised |
| `null` | equal mean clearance and no seam sensitivity at all; the defect-aware model must NOT be credited |
| `missing-data` | a walled sample carries no clearance value; ingestion must refuse it |
| `unit-error` | the clearance channel is declared in millimetres; ingestion must refuse it |

| `underpowered` | a real but tiny seam effect buried under specimen scatter; the honest verdict is INCONCLUSIVE, not equivalence and not a null |

Specimen and run scatter are deterministic pseudo-random offsets, so the files are
reproducible while the specimen-first scoring and the uncertainty on the improvement are
actually exercised.

Regenerate with `python scripts/make_synthetic_fixtures.py`.
