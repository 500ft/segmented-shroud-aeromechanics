# Segmented Shroud Aeromechanics

A shroud around a drone rotor can add thrust. Its performance depends in part
on the gap around the blade tips. A shroud built in segments has seams and small
steps where the pieces meet. The proposed CAD and CFD study would estimate their
predicted shaft-power cost at matched total thrust, compared with a smooth shroud
with the same average tip gap. OpenFOAM is the preferred feasibility route.

[![Repository checks](https://github.com/500ft/segmented-shroud-aeromechanics/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/500ft/segmented-shroud-aeromechanics/actions/workflows/ci.yml)
![Evidence: research design, not validated](https://img.shields.io/badge/evidence-research_design%2C_not_validated-415a77)
[![License: MIT](https://img.shields.io/badge/license-MIT-276c6b)](LICENSE)

[The question](#the-question) · [Where it stands](#where-it-stands) ·
[Roadmap](ROADMAP.md) · [Quick start](#quick-start) · [Reviewer guide](docs/START_HERE.md)

![Proposed workflow: baseline model, solver checks, then seam and step comparisons at matched thrust](docs/media/project-overview.svg)

*Proposed CFD workflow. The existing airfoil check is described below.*

## The question

Tip clearance matters for any ducted rotor, and that is well known. The
narrower question here is whether the shape of the defects adds information
beyond the average gap: two shrouds with the same mean clearance, one smooth and
one with seams or steps, compared at the same total thrust. The intended output
is the shaft power each needs.

The study uses rigid geometry only, so deployment mechanisms stay out of the
model. The [prior-art boundary](docs/prior-art.md) distinguishes the specific
seam comparison from established clearance and duct studies. Novelty remains
unresolved; equal-mean comparison alone is not a contribution.

## Where it stands

The [reference audit](evidence/task-reference-feasibility-2026-10-04/README.md)
reproduces the preserved geometry exports, but returns `BLOCKED_GEOMETRY`:
source blade sections and dimensioned duct/assembly geometry are still missing.
The reviewed data still describe only part of the rotor geometry.

The owner authorized a public-data-first computational investigation. OpenFOAM
is preferred, with compute cost to be measured once a faithful mesh is possible.
A thrust stand remains a later extension.

- Fluent Student starts on the CAD host
  ([readiness record](evidence/task-cad-ansys-2026-09-29/README.md)). No case
  has been solved there.
- An earlier OpenFOAM check on a 2D NACA 0012 airfoil agrees within 0.4%
  with the CFL3D Spalart-Allmaras reference lift coefficient after the stated
  incidence adjustment. Experimental and input uncertainty remain unquantified
  ([A0.1 report](docs/cfd-validation-a01.md)).
- The existing [analysis pipeline](scripts/analysis_pipeline.py) computes mean
  electrical input power as `mean(voltage × current)` and interpolates it to
  matched thrust. It is tested on synthetic data. CFD shaft-power extraction
  from rotor torque times angular velocity has not been implemented.

## Quick start

Python 3.11 (the CI version) and Git. The only dependency is pinned in
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

## What's next

The reference is the Akturk-Camci ducted fan. The next action is to obtain the
missing source geometry and measurement uncertainty definitions listed in the
[geometry record](data/reference/akturk-camci/geometry.json) and
[reference audit](evidence/task-reference-feasibility-2026-10-04/README.md).
The [roadmap](ROADMAP.md) records the authorized direction and remaining work.

## Limits

- Everything so far is software, literature and planning. No shroud CFD has run.
  No shroud specimen, aerodynamic measurement, or rubbing test has been completed for this repository.
- The planned CFD study compares predicted shaft power. Electrical efficiency,
  rubbing risk and deployment reliability are outside it.
- A good aerodynamic result would say nothing about whether the shroud protects
  against impacts; that needs its own tests.
- Rotor testing, if it ever happens, needs containment, remote arming and
  shutdown, current protection, a risk assessment and facility approval.
- Mechanism details are withheld under the
  [public-disclosure boundary](CONTRIBUTING.md#public-disclosure-boundary).

## Documentation

| Document | What it covers |
| --- | --- |
| [Reviewer guide](docs/START_HERE.md) | The project in five minutes |
| [Roadmap](ROADMAP.md) | Finish line, current evidence, remaining steps |
| [Decision log](docs/decision-log.md) | Scope decisions and their reasons |
| [Source review](docs/day3-source-review.md) · [prior art](docs/prior-art.md) | Closest competing work |
| [Literature](docs/literature/README.md) | Every source identified, and which were actually read |
| [Research plan](docs/research-plan.md) · [claim ledger](docs/claim-ledger.md) | Variables and claims |
| [Experiment 01](docs/experiment-01-rigid-defect-duct.md) | The deferred physical experiment |

## Contributing and license

Reproduction reports, source corrections and CFD or metrology critiques are
welcome. Include the commit, the command or source location, and what you
expected and saw. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a
[pull request or issue](https://github.com/500ft/segmented-shroud-aeromechanics/issues).

Software is [MIT licensed](LICENSE); publications keep their own licenses.
This is a research repository, not a qualified rotor enclosure or fabrication
package. [Repository identity](docs/REPOSITORY_IDENTITY.md).
