# Data and Figure Contract

## Current state

The repository contains executed [airfoil CFD results](cfd-validation-a01.md)
and a [reference geometry audit](../evidence/task-reference-feasibility-2026-10-04/README.md).
The airfoil comparison has incomplete experimental validation uncertainty.
[Partial blade data and an exporter](../data/reference/akturk-camci/README.md)
are on main; the original inputs remain on the
[preservation branch](https://github.com/500ft/segmented-shroud-aeromechanics/tree/c4f6b5268298fd18c2c0d3ae618a18338e3c1c93/shutdown-preserved/geometry).
There is no complete shroud assembly, shroud flow solution or project bench
measurement. The decision diagrams describe proposed work.

The [uncertainty revision](../results/generated/cfd/a0.1/uncertainty.revision-2026-09-25.json)
and [status revision](../results/generated/cfd/a0.1/status-revision-2026-09-29.json)
govern interpretation of the retained airfoil outputs. Original manifests,
raw outputs and frozen acceptance files remain historical records.

## Planned data stages

```text
data/raw/<study>/<specimen-id>/<run-id>/
data/processed/<study>/<analysis-version>/
results/generated/<study>/<analysis-version>/
```

Raw measurements remain immutable. Processed tables identify their source runs, code commit, units, calibration version, and transformation command.

## Required experimental metadata

- Study, specimen, deployment-cycle, and run identifiers
- Evidence state
- Material, manufacturing process, and geometry revision
- Closure mechanism and preload setting
- Circumferential defect description and measurement method
- Rotor, motor, controller, and operating point
- Instrument models and calibration identifiers
- Test order, temperature, and environmental condition
- Abort, rubbing, or anomalous event flags
- Analysis commit and output generator

## Figure rules

Every future figure must state:

1. The claim it supports
2. Evidence state
3. Independent sample unit and repeated-measure structure
4. Test conditions and units
5. Input artifacts and calibration
6. Generator command and commit
7. Uncertainty representation

Color is never the only semantic channel. Reference conditions use solid lines; modeled predictions use dashed lines; measured samples use markers; safety boundaries are directly labeled.

## Current figure manifest

| ID | Artifact | Claim | Evidence state |
| --- | --- | --- | --- |
| SSY-00 | [`assets/segmented-shroud-overview.svg`](../assets/segmented-shroud-overview.svg) | Explains the proposed causal chain only | Planned / conceptual |
| SSY-AUDIT-01 | [`docs/research-dependency-audit.md`](research-dependency-audit.md#directed-dependency-map) | Explains the source-reviewed task and gate order | Planned / source-reviewed |
