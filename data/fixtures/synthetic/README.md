# Synthetic fixtures

**SYNTHETIC TEST DATA - NOT EVIDENCE.**

Nothing here was measured. Every value comes from the closed-form generator in
`scripts/make_synthetic_fixtures.py`, so the correct answer is known before the pipeline
runs. These exist only to fix the analysis before any real data exists, which is the
point of backlog task SSY-05.

| case | what it is for |
| --- | --- |
| `positive` | power depends on seam count beyond mean clearance; a defect-aware model should beat the baseline on a held-out seam configuration |
| `null` | power depends on mean clearance alone; the defect-aware model should NOT improve |
| `missing-data` | a walled sample carries no clearance value; ingestion must refuse it |
| `unit-error` | the clearance channel is declared in millimetres; ingestion must refuse it |

Regenerate with `python scripts/make_synthetic_fixtures.py`.
