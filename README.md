# Segmented Shroud Aeromechanics

A closed research investigation into how seams and radial steps in a rigid
rotor shroud could affect shaft power at matched total thrust.

![Project status: closed](https://img.shields.io/badge/status-closed-64748b)
[![Repository checks](https://github.com/500ft/segmented-shroud-aeromechanics/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/500ft/segmented-shroud-aeromechanics/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-276c6b)](LICENSE)

[Retained evidence](#where-it-stands) · [Closure record](ROADMAP.md) ·
[Reproduce the checks](#quick-start) · [Reader guide](docs/START_HERE.md)

![Closed project: reference audit preserved, airfoil computation retained, shroud comparison uncompleted](docs/media/project-overview.svg)

The owner ended the project on 6 October 2026. The repository preserves its
code, source reviews, partial geometry and computational checks for reference.
There is no active backlog or request for equipment, measurements or further research.

## The question

Would a shroud with seams or steps require different shaft power from a smooth
shroud at the same mean tip clearance and total thrust? The proposed comparison
was never completed. The [prior-art review](docs/prior-art.md) records the
established clearance literature and unresolved novelty questions.

## Where it stands

| Retained work | Result and limit |
| --- | --- |
| [Reference geometry audit](evidence/task-reference-feasibility-2026-10-04/README.md) | Preserved exports reproduce. Complete source blade sections and duct/assembly dimensions remain missing: `BLOCKED_GEOMETRY`. |
| [Partial geometry and exporter](data/reference/akturk-camci/README.md) | Published blade stations and a digitised tip contour, with provenance and extraction allowances. Insufficient for a faithful complete assembly. |
| [OpenFOAM airfoil check](docs/cfd-validation-a01.md) | Retained numerical results and a reference-code comparison. Experimental validation remains `INCOMPLETE_UNCERTAINTY`. |
| [Electrical-power analysis](scripts/analysis_pipeline.py) | Computes mean voltage × current and compares at matched thrust; tested with synthetic fixtures. CFD shaft-power extraction was not implemented. |
| [Measurement-system draft](docs/measurement-system-spec.md) | Unqualified requirements and unresolved inputs. No installed measurement result. |

No shroud specimen, aerodynamic measurement, or rubbing test was completed for
this project. No shroud flow solution or seam-effect result exists. Closure is
an owner decision; it does not show that seams have no effect or that the design
is safe, protective or ready to fabricate.

## Quick start

Python 3.11 (the CI version) and Git. Dependencies are pinned in
[requirements.txt](requirements.txt). No CAD licence, solver or hardware is
needed.

```bash
git clone https://github.com/500ft/segmented-shroud-aeromechanics.git
cd segmented-shroud-aeromechanics
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check_repo_contract.py
python scripts/acquisition_ledger.py --check
python scripts/reference_coverage.py --check
python scripts/clearance_uncertainty_budget.py --check
python -m unittest discover -s tests -v
```

On Windows, activate with `.venv\Scripts\Activate.ps1` instead of `source`.

The contract check and the three record checks should pass (the measurement
budget reports `INPUTS_PENDING`), and the tests should end with `OK`.

To rebuild the literature ledger from committed inputs (offline; unchanged
inputs give no diff):

```bash
python scripts/acquisition_ledger.py
git diff -- evidence/task-day3-2026-09-09/acquisition-ledger.json
```

## Preserved history

The [closure record](ROADMAP.md) lists completed and discontinued work.
[Decisions](docs/decision-log.md), [literature](docs/literature/README.md),
[research plans](docs/research-plan.md) and [task ledgers](docs/TASKS.md) remain
available as history. Their unfinished tasks are no longer active.

The [WIP preservation branch](https://github.com/500ft/segmented-shroud-aeromechanics/tree/c4f6b5268298fd18c2c0d3ae618a18338e3c1c93)
retains additional unfinished material. Inclusion there does not establish
validated geometry or completed research.

## License and reuse

Project software is [MIT licensed](LICENSE). Publications and third-party data
retain their own rights; public access does not establish a reuse licence.
The [contribution and disclosure notes](CONTRIBUTING.md) remain for provenance.
The project is no longer maintained.
