# Roadmap

This is the only plan for finishing the project. Earlier scope decisions are
in [docs/decision-log.md](docs/decision-log.md); work history is in
[docs/SPRINT_PROGRESS.md](docs/SPRINT_PROGRESS.md).

## Finish line

A computational comparison of seams and radial steps in a rigid shroud at
matched total thrust. The baseline must first be checked against Akturk-Camci
thrust and shaft-power data at matching operating conditions, with numerical,
geometry and experimental uncertainty. Deliver CAD, solver inputs and outputs,
convergence and model-sensitivity checks, and a report stating which differences
are resolved. An unresolved effect is a valid outcome. Physical validation
remains a later extension.

The owner authorized a public-data-first investigation. OpenFOAM is the
preferred route without the Student licence cell cap, subject to measured
compute cost. That authorization replaces the earlier D4 pause for the limited
reference and feasibility task; it does not approve an approximate reconstruction.

## Current result

The executed [reference audit](evidence/task-reference-feasibility-2026-10-04/README.md)
returns `BLOCKED_GEOMETRY`. Selected preserved data and the exporter are now
reviewed here. Their outputs reproduce the archived exports. The paper's
scaled mesh view provides partial duct information, but a faithful assembly
still needs the source material listed in the
[geometry record](data/reference/akturk-camci/geometry.json). No shroud mesh or
flow solution exists, and compute cost has not been measured.

The reference remains the Akturk-Camci ducted fan selected by the owner. Its
nominal facility speed is not automatically a reference operating point.
[The reference record](evidence/task-reference-feasibility-2026-10-04/reference.json)
identifies plotted speeds, clearance normalization, force boundaries and
measurement uncertainty gaps. Caradonna-Tung remains an unducted solver check.

## Existing capability

- Fluent Student starts on the CAD host, with no solved case. Its licence
  limits remain in the [readiness record](evidence/task-cad-ansys-2026-09-29/README.md);
  they are not the compute ceiling for the OpenFOAM route.
- The earlier OpenFOAM airfoil check has verdict `INCOMPLETE_UNCERTAINTY`:
  both experimental and input uncertainty remain unquantified
  ([A0.1 report](docs/cfd-validation-a01.md)). It provides no ducted-rotor validation.
- The [analysis pipeline](scripts/analysis_pipeline.py) computes mean electrical
  input power from voltage/current pairs and compares it at matched thrust.
  CFD shaft power from rotor torque times angular velocity remains unimplemented.
- [Official NYU documentation](evidence/task-reference-feasibility-2026-10-04/nyu-access.json)
  supports a conditional cluster route. Access, allocation and an OpenFOAM/MPI
  setup have not been established. The sponsorship question is a draft only.

## What's left

**Current step: obtain the missing source geometry.** The owner needs blade
sections with stacking/root definitions and dimensioned duct/assembly geometry,
plus clarification of thrust, torque and RPM uncertainty. Any approximate
reconstruction requires a separate scope decision.

| Step | Status and done condition |
|---|---|
| Reference and geometry audit | Executed. Recoverable data, conflicts and missing dimensions are recorded; complete geometry remains blocked. |
| Baseline mesh and compute feasibility | After source geometry is sufficient: record solver/version, cells, peak RAM, wall time, convergence target and force/torque export conventions on an available host. |
| Baseline comparison | Check mesh and timestep sensitivity in thrust and torque. Match the published assembly and operating conditions, carrying combined uncertainties and known correlations. |
| Seam and step comparison | After the baseline supports it: transient cases at matched total thrust with valid periodicity or full annulus; compare predicted shaft power with numerical and geometry sensitivity. |
| Report | Publish resolved and unresolved differences, inputs and reproducible outputs. |

Periodicity must include blades, seams and all retained supports. The paper's
unequal stationary and rotating sectors use circumferential averaging; that
does not establish an exact transient repeat unit. A blade-element or tip-loss
model can estimate baseline scale but needs a validated seam model before it
can decide seam effects. Reference uncertainty contributes to the comparison
interval; it is not a universal CFD acceptance threshold.

No new checker framework is needed. Simulations do not establish deployment
reliability or protection.

## Not in this version: the experimental programme

The original hardware programme below is retained as deferred scope. Its
historical numerical gates are not acceptance criteria for the current
computational study. No bench switch, equipment approval, measurable rotor
selection or practical-effect threshold has been adopted. The proposed
replacement stays in the external owner handoff pending those decisions.

- **Stage 1: Measurement qualification.** Clearance, thrust, voltage, current,
  RPM and temperature channels calibrated; stand drift and warm-up quantified.
  Exit gate: measurement uncertainty smaller than the smallest defect and
  performance difference the experiment has to resolve. A
  [requirements draft](docs/measurement-system-spec.md) exists.
- **Stage 2: Adjustable rigid defect duct.** Open rotor, monolithic duct and
  adjustable duct compared at matched thrust under uniform clearance, two-lobe
  ovality, seam opening and local steps. Exit gate: a defect-aware model
  improves held-out error by at least 20% over a mean-clearance model and
  reaches below 10% prediction error. Failure branch: if defect geometry adds
  nothing beyond uncertainty, publish the simpler mean-clearance tolerance
  result and stop mechanism work.
- **Stage 3: Closure-mechanism repeatability**, **Stage 4: coupled
  aero-mechanical yield**, and **Stage 5** extensions (second rotor scale,
  aging, acoustics, free flight). Each is gated on the stage before it.
- **Guard claims** need their own impact, containment, deflection and
  power-penalty tests. An aerodynamic result, positive or null, says nothing
  about protection.
