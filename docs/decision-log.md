# Decision Log

Current interpretation follows [ROADMAP.md](../ROADMAP.md). The entries below
retain the decisions and rationale recorded at the time. The later
[reference audit](../evidence/task-reference-feasibility-2026-10-04/README.md)
corrects the reference rationale: measured assembled thrust and rotor-only
thrust came from different configurations; the separately plotted rotor and
duct components were computed. The recorded nominal speed is not a selected
comparison point. Transient periodicity must include retained supports as well
as blades and seams. These corrections do not change the chosen reference.

## 2026-09-30 — Reference rotor: the Akturk–Camci ducted fan

**Decision:** the baseline rotor and duct for the computational study are the
8-blade ducted fan of Akturk and Camci (ASME GT2011-46356; J. Turbomachinery
136(2):021004, 2014), 279.4 mm tip radius at 3500 rpm. The owner delegated this
choice on 2026-09-30 ("make a decision for the other repos"); it was made by
Claude on the owner's behalf and is recorded here as the owner's decision.

**Why this rotor.**
- It was tested inside a duct, with thrust and power measured at several tip
  clearances and duct and rotor thrust measured separately. That is the
  comparison this study needs a baseline for.
- The Caradonna–Tung rotor was tested without a duct, so no ducted result
  could be checked against its data.
- Eight blades let seam counts of 8, 4 or 2 make a 45°, 90° or 180° sector
  model legitimate, because the combined geometry genuinely repeats. That is
  the only legitimate way to fit a seamed case inside the 1M-cell licence
  limit; with two blades the smallest legitimate sector is 180°.
- The paper is already read
  ([reading record](reading-records-2026-09-25.json), evidence grade B for the
  measured thrust and power response to tip clearance).

**What it costs.** Blade sections and the duct profile are given only as
figures, so the geometry has to be digitised, and that digitising uncertainty
is carried into the baseline comparison. The paper reports no Reynolds or Mach
number, transition state, numerical uncertainty or experimental uncertainty for
its coefficients; derived values (tip Mach 0.299, tip-chord Reynolds about
4.3 × 10⁵) are computed here and labelled as such.

**Consequences.**
- Caradonna–Tung is dropped as the reference. It stays available as a
  rotor-only solver-setup check, used only if the blade-resolved route is chosen
  in roadmap step 3.
- Roadmap step 2 starts: digitise and register the rotor, duct, operating point
  and clearance convention, keeping values read from the paper apart from
  digitised and chosen ones.
- The A0 validation cases and the uncertainty decision record are unchanged.

## 2026-09-29 — Finish as a CAD–ANSYS computational study

**Owner decision:** “lets go with the CAD-ANSYS setup”. The owner also authorized
updating this repository and opening a PR. This selects computational completion,
replacing the earlier choice between freezing the design and funding the thrust stand.
It is an adopted scope decision, not a proposed plan awaiting that same decision again.

**Finish line.** A reproducible assessment of how generic rigid-shroud seams and
radial steps affect predicted aerodynamic shaft power at matched total assembly
thrust, within one declared rotor/operating envelope. Deliver parametric CAD and
neutral exports, solver inputs and results, numerical convergence and model-sensitivity
evidence, and a report that states the supported comparisons and unresolved effects.
Completing this version does not require buying or building a thrust stand.

**Execution route.** Use the existing SOLIDWORKS/CadQuery capability from
`500ft/engineering-audit` for geometry and neutral STEP verification, and ANSYS Fluent
for CFD. The shared [CAD briefing](https://github.com/500ft/engineering-audit/blob/6e55653246ecf39f6b40927a4697d0218027b719/docs/cad_agent_briefing.md)
is capability guidance, not a shroud result. The executed host inventory and startup
assessment live in the [readiness record](../evidence/task-cad-ansys-2026-09-29/README.md).
CFX is an installed alternative, not a second solver campaign. Existing OpenFOAM
results remain historical benchmark evidence; they do not qualify Fluent automatically.

**What advances next.** Verify the published geometry and comparison data for the
existing Caradonna–Tung reference candidate, resolve its outstanding source ambiguities,
and register the nominal rotor, continuous duct, operating point and clearance convention
before authoring them. Keep sourced dimensions distinct from chosen generic duct
parameters. Values are recorded once in the relevant source/geometry record and linked
elsewhere. Do not substitute the unrelated CAD scaffold's dimensions or physical
measurement-budget targets. Establish a baseline mesh and measured compute cost before
committing to the candidate sweep. If the reference is unsuitable for the available
license or geometry evidence, record the reason and recommend a replacement before
changing the study's rotor identity.

**Computational release conditions.** Generic benchmark and rigid-defect CAD may
proceed when its source inputs, chosen design parameters and independent geometric
checks are specified. Installed sensor qualification and fabrication approval do not
gate that work. Solver regime, domain extent, rotor motion, boundary conditions,
force/torque surfaces and prospective convergence criteria must be explicit before
the baseline solve. A rotating-sector shortcut needs symmetry of the actual combined
rotor and shroud geometry; it cannot be used merely to fit the license ceiling.

Compare shaft power from rotor torque and angular speed, keeping rotor and duct
force contributions separate before summing total thrust. Electrical power, dynamic
rubbing probability and deployment yield are outside this model's claims. Hold mean
clearance under the registered wall-domain/occlusion convention; record total seam
opening separately. Treat frozen-rotor clocking as a numerical/model sensitivity.
Changing the angular origin alone is not a new time-averaged design in symmetric hover;
relative seam arrangements and their relation to fixed supports can be.

**Evidence required to finish.** Compare the baseline against accessible published
measurements with their limitations stated. Check spatial convergence and selected
model sensitivity; use sliding-mesh confirmation with phase/time-step/averaging-window
checks for consequential unsteady comparisons. A sampled sensitivity envelope is not
a proven bound on physical error. A supported ranking, no numerically resolved
difference, or an explicitly unresolved comparison are legitimate study outcomes.
An unstarted sweep or failed software launch alone is not computational completion.
No broad rotor-scale transfer, universal optimal design or global novelty claim follows.

**Scope and supersession.** This entry governs the finish line, solver route and
release conditions wherever the older roadmap, programme, or CAD work orders imply
that hardware or the entire original validation ladder must be completed first.
The earlier source-backed reference choice is retained as a candidate; dimensions,
solver physics (including the old D10 question) and validation accuracy are not silently
approved by choosing ANSYS. The uncertainty decision record still governs interpretation.
SSY-01/02/03 and the hardware CAD backlog are not marked complete. The measurement
budget, physical pilot, mechanism/structural studies, acoustics and guard qualification
are future extensions. XC-02 remains open for implementation-sensitive joint,
mechanism and fabrication detail; this decision authorizes generic computational
geometry only. No purchases, cloud charges or powered hardware operation are implied.

## 2026-09-03 — Use aero-mechanical yield instead of cycle count alone

**Decision:** model joint success across deployment, locking, dynamic clearance, and aerodynamic benefit.

**Reason:** cycle count is an exposure variable, not the engineering outcome. A ring that deploys repeatedly but loses clearance or aerodynamic value is not a successful duct.

## 2026-09-03 — Isolate defects before testing mechanisms

**Decision:** begin with an adjustable rigid duct.

**Reason:** it separates the aerodynamic value of seam, step, and harmonic descriptors from the variability of a new closure mechanism.

## 2026-09-03 — Keep the minimum paper to one rotor scale

**Decision:** hold out a defect family before attempting a second rotor scale.

**Reason:** scale changes Reynolds number, motor behavior, geometry, and manufacturing uncertainty simultaneously. It is an extension, not the cleanest first validation.

## 2026-09-03 — Make the guard branch an independent result path

**Decision:** do not call a failed performance duct a successful guard without new tests.

**Reason:** impact energy, containment, deflection, mass, and aerodynamic penalty are separate requirements.
