# Roadmap

This is the plan for finishing the project. The owner's scope decision is in
[docs/decision-log.md](docs/decision-log.md#2026-09-29--finish-as-a-cadansys-computational-study);
task status is in [docs/SPRINT_TASKS.csv](docs/SPRINT_TASKS.csv); work history
is in [docs/SPRINT_PROGRESS.md](docs/SPRINT_PROGRESS.md) and
[docs/REVIEW_READY.md](docs/REVIEW_READY.md).

## Finish line (owner decision, 2026-09-29)

A computational study in CAD and ANSYS Fluent: how seams and radial steps in a
rigid shroud change the shaft power a ducted rotor needs at the same total
thrust, for one rotor and one operating point. The deliverables are parametric
CAD, solver inputs and results, mesh-convergence and model-sensitivity checks,
and a report that says which differences the numbers resolve. "No resolvable
difference" is a valid result. No thrust stand or hardware purchase is needed.

## The constraint that shapes the plan

The installed licence is ANSYS Student 2026 R1, limited to 1,000,000 cells or
nodes and 4 cores ([readiness record](evidence/task-cad-ansys-2026-09-29/README.md)).
The decision log allows a rotating sector only when the rotor and shroud
geometry genuinely repeat around the axis, not just to fit the licence.

- A blade-resolved, full-annulus model of a rotor in a seamed duct, with the
  tip gap resolved, is unlikely to fit in 1M cells. The baseline mesh study
  (step 3) measures this before any sweep is planned. If it does not fit, the
  fallback is a modelled rotor (for example Fluent's virtual blade model, if
  the Student build includes it). That still captures seam and step effects on
  the duct's thrust, but not tip-leakage flow, and the question narrows to
  match.
- The seam count can keep the geometry periodic. With an 8-blade rotor, 8, 4 or
  2 evenly spaced seams make a 45°, 90° or 180° sector legitimate, because the
  combined geometry really does repeat. With the 2-blade Caradonna–Tung rotor,
  the smallest legitimate sector is 180°.

## Reference rotor (decided 2026-09-30)

The baseline is the 8-blade ducted fan of Akturk and Camci (ASME
GT2011-46356; J. Turbomachinery 136(2), 2014): 279.4 mm tip radius at 3500 rpm,
tested in a duct with thrust and power measured at several tip clearances. Its
blade and duct geometry has to be digitised from figures, and that uncertainty
is carried. The Caradonna–Tung rotor, tested without a duct, is kept only as a
rotor-only solver check. Reasons are in the
[decision log](docs/decision-log.md#2026-09-30--reference-rotor-the-akturkcamci-ducted-fan).

## Where it stands (2026-09-30)

- Fluent Student starts on the CAD host: licence checkout, compute node,
  journal read and clean exit. No case has been loaded or solved.
- An earlier OpenFOAM check on a 2D NACA 0012 airfoil reproduces published
  reference computations within 0.4%. Its validation verdict is
  `INCOMPLETE_UNCERTAINTY`, because one uncertainty component was never
  quantified ([A0.1 report](docs/cfd-validation-a01.md)). It does not qualify
  Fluent.
- The analysis pipeline for the final comparison exists and is tested on
  synthetic fixtures only.
- No shroud geometry, mesh or flow solution exists.

## What's left

| # | Step | Who | Done when |
|---|---|---|---|
| 1 | Choose the reference rotor | Owner | Done 2026-09-30: Akturk–Camci ducted fan |
| 2 | Digitise the Akturk–Camci rotor and duct and register the operating point and clearance convention, keeping values read from the paper apart from digitised and chosen ones | Agent | One geometry record, reviewed. **Current step.** |
| 3 | Build the baseline CAD and mesh; measure cell count and run time against the 1M-cell, 4-core limit | Agent, on the CAD host | Go or no-go on blade-resolved versus a modelled rotor, recorded with the numbers |
| 4 | Solve the baseline, check mesh convergence, compare with the reference's published thrust and power | Agent | Baseline report with the agreement stated |
| 5 | Run the seam and step cases at matched thrust, with the declared sensitivity checks | Agent | Comparison table with numerical uncertainty |
| 6 | Write the report: which differences are resolved and which are not. Update the README and portfolio | Agent | Merged |

Rules carried from the decision: no new checker framework (use the existing
engineering-audit CAD machinery), and no simulation result is presented as
evidence of deployment reliability or protection.

## Not in this version: the experimental programme

The original hardware programme is kept as a future extension. None of it
blocks the computational finish.

- **Stage 1 — Measurement qualification.** Clearance, thrust, voltage, current,
  RPM and temperature channels calibrated; stand drift and warm-up quantified.
  Exit gate: measurement uncertainty smaller than the smallest defect and
  performance difference the experiment has to resolve. A
  [requirements draft](docs/measurement-system-spec.md) exists.
- **Stage 2 — Adjustable rigid defect duct.** Open rotor, monolithic duct and
  adjustable duct compared at matched thrust under uniform clearance, two-lobe
  ovality, seam opening and local steps. Exit gate: a defect-aware model
  improves held-out error by at least 20% over a mean-clearance model and
  reaches below 10% prediction error. Failure branch: if defect geometry adds
  nothing beyond uncertainty, publish the simpler mean-clearance tolerance
  result and stop mechanism work.
- **Stage 3 — Closure-mechanism repeatability**, **Stage 4 — coupled
  aero-mechanical yield**, and **Stage 5** extensions (second rotor scale,
  aging, acoustics, free flight). Each is gated on the stage before it.
- **Guard claims** need their own impact, containment, deflection and
  power-penalty tests. An aerodynamic result, positive or null, says nothing
  about protection.
