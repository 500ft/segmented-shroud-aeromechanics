# Start here — Segmented Shroud Aeromechanics

[Project overview](../README.md) · [Run the checks](../README.md#quick-start) ·
[Roadmap](../ROADMAP.md) · [Review index](REVIEW_READY.md)

## In one minute

A shroud built in segments can close into a ring and still have seams and
small steps where the pieces meet. The question here is whether those defects
matter beyond the average tip gap: compare a smooth shroud and a seamed one
with the same mean clearance, at the same total thrust, and see how much shaft
power each needs.

The owner chose to finish this as a computational study in CAD and ANSYS
Fluent ([decision](decision-log.md#2026-09-29--finish-as-a-cadansys-computational-study)).
Fluent starts on the CAD host; no shroud case has been solved. An earlier
OpenFOAM check on a 2D airfoil matches published reference computations within
0.4%, but it does not qualify Fluent or predict anything about a shroud. The
original plan to build a thrust stand is kept as a later extension.

## Reading paths

| If you have | Read |
| --- | --- |
| Five minutes | The [README](../README.md), then the [roadmap](../ROADMAP.md) |
| Half an hour | The [scope decision](decision-log.md#2026-09-29--finish-as-a-cadansys-computational-study), the [ANSYS readiness record](../evidence/task-cad-ansys-2026-09-29/README.md) and the [A0.1 report](cfd-validation-a01.md) |
| A review to do | The [review index](REVIEW_READY.md) |
| A question about novelty | The [source review](day3-source-review.md), the [candidate triage](prior-art-search-2026-09-14-screening.md) and [prior art](prior-art.md). The claim is narrowed to the equal-mean-clearance seam comparison; 22 triaged papers are still unread |
| A question about a claim | The [claim ledger](claim-ledger.md) and the [research plan](research-plan.md) |

## What the study will and won't say

It compares predicted shaft power for rigid shroud geometry, one rotor and one
operating point. It says nothing about electrical efficiency, rubbing risk,
deployment reliability or protection against impacts; those need hardware and
their own tests. The [uncertainty decision](specs/research-programme/uncertainty-decision-record.md)
sets how every CFD result is interpreted, and the
[transient rules](specs/research-programme/transient-acceptance.md) set when an
unsteady comparison counts.

## The deferred hardware programme

The original plan was an adjustable rigid duct on a contained rotor stand,
comparing electrical power at matched thrust. It is described in
[Experiment 01](experiment-01-rigid-defect-duct.md) and the
[measurement-requirements draft](measurement-system-spec.md), whose budget
still reports `INPUTS_PENDING`. The [roadmap](../ROADMAP.md) keeps its stage
gates. None of it blocks the computational finish.

![Planned measurement-first sequence with a simpler-model branch and independent evidence required for mechanism, performance-duct, and protective-guard claims](../assets/segmented-shroud-overview.svg)

*The original decision diagram, kept for its alternative outcomes. It is not a
result.*

## Where things live

- [Roadmap](../ROADMAP.md): finish line and remaining steps.
- [Long-term backlog](TASKS.md): later tasks, including hardware.
- [Decision log](decision-log.md): scope decisions and their reasons.
- [Specifications index](specs/README.md): what each spec is and whether it is
  still in use.
- [CONTRIBUTING.md](../CONTRIBUTING.md), including the
  [public-disclosure boundary](../CONTRIBUTING.md#public-disclosure-boundary)
  for mechanism details.
- The September 11 [acquisition correction](ACQUISITION_CORRECTION_2026-09-11.md)
  explains which early deliverables were preparation rather than finished work.
