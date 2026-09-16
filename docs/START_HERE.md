# Start here — Segmented Shroud Aeromechanics

[Project overview](../README.md) · [Run the checks](../README.md#quick-start) · [Review index](REVIEW_READY.md)

## In one minute

A segmented shroud can close successfully yet reconstruct poor aerodynamic geometry. This project separates that problem into a first, controlled question: at equal mean rotor-tip clearance, do seam and distortion patterns matter enough to improve prediction over a mean-clearance model?

The first apparatus is a **rigid adjustable duct**, not a folding shroud. Measurement qualification precedes performance testing. Mechanism reconstruction and deployment yield are conditional later studies; protective-guard performance needs its own experiment.

The current implementation validates research metadata, source provenance, prior-art coverage and the Stage A uncertainty budget. No shroud model, specimen, simulation result, or physical performance result has been produced.

## What to inspect first

1. Read the [2026-09-09 source-review decision](day3-source-review.md) and the [2026-09-15 candidate triage](prior-art-search-2026-09-14-screening.md). Together they identify what the accessible literature establishes, which competitor treatments remain unresolved, and which 22 records are queued for close reading.
2. Read the [research programme](specs/research-programme/proposal.md): validated CFD before hardware, a budget fed by owner decisions, and a pilot only if the budget says it can see the effect.
3. Inspect [Experiment 01](experiment-01-rigid-defect-duct.md) and the [measurement-requirements draft](measurement-system-spec.md); the draft's open-input register says which numbers the owner still has to decide.
4. Run the [README quick start](../README.md#quick-start). These are offline integrity checks after dependency installation, not aerodynamic calculations.
5. Read the [claim ledger](claim-ledger.md) and [disclosure boundary](../CONTRIBUTING.md#public-disclosure-boundary) before proposing stronger claims or adding implementation-sensitive geometry.

## Evidence map

| Layer | Committed source | Interpretation |
| --- | --- | --- |
| Research rationale | [Research plan](research-plan.md), [prior art](prior-art.md) | Hypotheses, yield definition, and prior-art boundary; novelty remains unresolved |
| Source acquisition | [Canonical public export](../evidence/task-2026-09-11-public/database-export.json), [historical export](../evidence/task-2026-09-09/database-export.json) | 450 records with every row traceable to a logged query; the historical export is retained and credited for nothing |
| Coverage of the day-1 set | [Coverage record](../evidence/task-2026-09-12/reference-coverage.json), [generator](../scripts/reference_coverage.py) | 4 of 6 eligible sources recovered by the canonical export; novelty axes bounded to inspected sources |
| Candidate triage | [Screening record](candidate-screening-2026-09-14.json), [report and queues](prior-art-search-2026-09-14-screening.md) | 25 dispositions under a rule frozen before reading; 22 queued for close reading, not read |
| Targeted reading | [Rubric](day3-reading-rubric.md), [reading records](day3-reading-records.json) | Identified source sections and access limits, not a complete systematic review |
| Derived provenance | [Acquisition ledger](../evidence/task-day3-2026-09-09/acquisition-ledger.json) | Deterministically reconciled identifiers and routes, not repaired history |
| Future specimen identity | [Specimen schema](../protocols/specimen-manifest.schema.json), [example](../protocols/example-specimen-manifest.json) | The example is explicitly planned, not a fabricated specimen or executed run |
| Executable checks | [Scripts](../scripts/), [tests](../tests/), [CI](../.github/workflows/ci.yml) | Schema, documentation, and acquisition-integrity checks |
| Stage A gate | [Budget register](clearance-measurement-budget.csv), [calculator](../scripts/clearance_uncertainty_budget.py), [requirements draft](measurement-system-spec.md) | Verdict `INPUTS_PENDING` with seven pending terms; the draft names who closes each input |
| Verification records | [2026-09-14 evidence](../evidence/task-2026-09-14/README.md), [day-3 evidence](../evidence/task-day3-2026-09-09/README.md) | Commands, baseline, limitations, and software outputs |
| Future study outputs | [Data contract](../data/README.md), [results notice](../results/README.md) | No CAD, FEA, CFD, or measured results are available |

Two acquisitions exist. The historical 2026-09-09 export keeps all 499 raw rows, 50 of them without successful query-log support, and the acquisition ledger preserves them with that gap visible. The canonical 2026-09-11 public export has 450 rows, all traceable, and is the only one credited in the coverage record. An identifier match is not a reviewed study; the 22 queued candidates are unread.

## First-experiment decision

This table is a reading aid; the [protocol](experiment-01-rigid-defect-duct.md) and [research plan](research-plan.md) are authoritative. All numerical gates below are **provisional design decisions**, not achieved results or a completed preregistration.

| Decision element | Planned contract |
| --- | --- |
| Hypothesis | At equal mean clearance, a two-lobe distortion or discrete seam changes thrust-per-power or dynamic minimum clearance beyond measurement uncertainty |
| Setup | Contained rotor stand; open-rotor and monolithic references; adjustable rigid duct |
| Pilot conditions | Uniform reference, two-lobe distortion, and discrete seam at equal mean clearance |
| Measure | Geometry, dynamic clearance, thrust, RPM, voltage/current, temperature, vibration, and contact |
| Control | Rotor/motor/controller, nominal profile, inlet arrangement, sensor positions, randomized blocked order |
| Primary comparison | Electrical power at matched thrust; RPM-matched results are a secondary diagnostic |
| Model prerequisite | Training supports the fitted descriptors; an unseen mechanism needs a specified physical extrapolation model, otherwise restrict the claim |
| Continue | Defect-aware held-out prediction error below 10% and at least 20% lower than the mean-clearance baseline |
| Repeat or redesign | Effect is comparable to measurement uncertainty: improve instrumentation before interpreting the hypothesis |
| Pivot | Defect descriptors add no predictive value: report the simpler tolerance result and stop mechanism integration |

Prediction error is normalized by observed electrical power at matched thrust, not the small duct-minus-open-rotor difference. A zero baseline error makes relative improvement undefined. Specimen aggregation, operating-point weights, and final thresholds must be fixed before new confirmation data.

## Three distinct claims

**Aerodynamic effect:** the rigid-defect study can test whether geometry changes measured power or clearance inside a defined operating envelope.

**Aero-mechanical yield:** a later study would combine successful deployment/locking, minimum-clearance requirements, and retained aerodynamic benefit. Rigid inserts alone cannot establish deployment repeatability or yield.

**Protective guard:** impact protection and debris containment are independent claims. Neither the absence of rubbing nor a failed aerodynamic-benefit hypothesis proves them.

Mass, packed volume, deployment time, and protection remain separate system-level outcomes. Do not advertise a universal shroud design rule from a single rotor scale or a small developer-designed experiment.

## Decision diagram

![Planned measurement-first sequence with a simpler-model branch and independent evidence required for mechanism, performance-duct, and protective-guard claims](../assets/segmented-shroud-overview.svg)

*Existing conceptual decision diagram, retained for its alternative branches. It is not CAD, manufactured hardware, a performance curve, or evidence of a qualified guard.*

The [directed dependency audit](research-dependency-audit.md) explains the separation between those claims and the limits of graph-derived findings.

## Where the next work lives

- [Research programme](specs/research-programme/proposal.md), [tiers and triggers](specs/research-programme/scope.md), [first work order](specs/research-programme/plan.md): Study A0 validation, Study A CFD parametric with an uncertainty band, Study B budget feed, then a gated pilot.
- [Gate-driven roadmap](../ROADMAP.md): measurement-first sequence and conditional expansion.
- [Research task definitions](TASKS.md): exact-gap, metrology, defect-basis, and disclosure prerequisites.
- [Sprint task ledger](SPRINT_TASKS.csv): authoritative status of bounded sprint work; this guide does not duplicate task status.
- [CAD inventory](CAD_ITEMS.md): categories only; parked tasks do not imply modeling or fabrication is authorized.
- [Decision log](decision-log.md): rejected framings and the reason for each change.
- [Contributing rules](../CONTRIBUTING.md): evidence labels, source requirements, safety, and disclosure.

XC-02 remains unresolved. Do not restore withheld mechanism detail from older public history or infer permission from the presence of a task. A qualified rotor stand, actual metrology, and site-specific operating approval remain required before physical work.

[Back to overview](../README.md) · [Repository identity and presentation references](REPOSITORY_IDENTITY.md)

## September 11 completion correction

Read the [item-by-item correction](ACQUISITION_CORRECTION_2026-09-11.md) before interpreting a prepared protocol, software check, or search export as a completed research gate. It identifies actual deliverables and the remaining measurement, review, or source-reading work separately.
