# Segmented Shroud Aeromechanics — revised CAD work orders

For the plain-language list of physical parts and assemblies, see [CAD_ITEMS.md](CAD_ITEMS.md). It maps to the existing work orders without adding tasks, estimates or completion status.

Amended 2026-09-06 after source review. Planning only: no CAD, fixture, fabrication or calibration result exists from this amendment.

**Main-branch placement authorized — 2026-09-06 (America/New_York).** The owner explicitly requested merging these PRs to their respective main branches. This supersedes the earlier placement hold for this PR's current documents and prerequisite integrity changes; it is not a blanket policy for future private material. Hardware, measurement and disclosure gates remain unchanged. See [CAD_REVIEW_DISPOSITION.md](CAD_REVIEW_DISPOSITION.md).

[CAD_TASKS.csv](CAD_TASKS.csv) is the sole CAD status ledger. [SPRINT_TASKS.csv](SPRINT_TASKS.csv) is the research-task ledger and carries no CAD status. [Scope tiers](specs/cad-development/scope.md) and [reproduction checks](CAD_PLAN_CHECKS.md) describe this amendment, not physical validation.

## 2026-09-21 — shared CAD tooling incorporated; tasks stay deferred

A cross-project CAD briefing was reviewed and folded into planning. **Nothing is promoted.** Every SSY-CAD task remains `deferred` in [CAD_TASKS.csv](CAD_TASKS.csv), which is still the sole CAD status ledger, and the entry conditions SSY-01, SSY-02, SSY-03 and XC-02 are unchanged. The briefing supplies capability information, not closure of those dependencies.

**Shared tooling, pinned.** `500ft/engineering-audit`, reviewed at commit `cf56cdff50b09c9a266292006cbf5b2a0f2e8ac6` (2026-09-21): [`docs/cad_agent_briefing.md`](https://github.com/500ft/engineering-audit/blob/cf56cdff50b09c9a266292006cbf5b2a0f2e8ac6/docs/cad_agent_briefing.md), with `docs/host_setup.md` and `docs/solidworks_api_findings.md` alongside and reusable machinery under `cadloop/`. The revision is pinned here rather than tracked on a branch so a later reader sees what was actually reviewed. Its reported results are demonstrations on other geometry, chiefly a racing-mast example, and are **not** shroud results; its dimensions and acceptance numbers never become shroud inputs.

**Tool choice is unchanged.** The selection above stands: CadQuery for parameterized families with neutral STEP verification, Onshape for hand-modeled fixtures subject to access. Native SOLIDWORKS authoring is an optional route only when a deliverable requires it and a recorded plan amendment establishes the host, access and artifact ownership. A Windows host is not a prerequisite for the CadQuery path.

**Planning requirements to apply when a work order is activated.** Six items map onto the existing tasks rather than forming a parallel backlog: tool-to-work-order mapping (SSY-CAD-01/02, 10, 03/04/05, 06, 07); a geometry acceptance contract fixing axis, origin, angular zero, units, sampling and every metric with its tolerance and failure behavior; independent checks with deliberate negative cases, where reusing the same construction helper on both sides is not independence and volume agreement alone cannot accept geometry; evidence that parameters actually drive the saved and exported part, including seam azimuth and step position that a volume check cannot see; host execution requirements if and only if the native route is selected; and provenance carried through release, distinguishing a nominal design review from a geometrically verified artifact from a fabrication release.

Still unestablished in the shared tooling at the pinned revision: native assembly and mates, assembly STEP, modal analysis, a dimensioned drawing and tolerance set, complete position-parameter control, and independent FEA verification. None may be presented as available acceptance evidence. A solver completion message validates nothing, and a static solve establishes neither fatigue, nor blade containment, nor aerodynamic performance, nor dynamic tip clearance.

### Two integration points this repository has to own

**The equal-mean convention is one decision, not two.** The [measurement-requirements draft](measurement-system-spec.md#13-averaging-domain-and-the-missing-wall-rule) already defines the missing-wall problem and its three admissible treatments, and assigns the choice to open input **IN-08**. The CAD geometry contract needs the same convention. If CAD registers one treatment and the measurement system another, "equal mean clearance" means different things in the model and on the rig, and the experiment's control is broken before anything is built. IN-08 governs both; the CAD contract cites it rather than choosing independently.

**The geometric tolerance has a floor set by what the physics study can resolve.** [A0.1](cfd-validation-a01.md) established that steady RANS on a canonical case carries 1.4 to 3.3 percent model-form error in lift, and that turbulence model choice alone moves lift by about 1.2 percent. A seam effect below roughly 2 percent cannot be separated from model-form error by that class of simulation. Geometry tolerances must therefore be tight enough that geometric error is negligible against the smallest effect the study intends to claim, and the acceptance contract should state that relationship rather than picking a tolerance by habit. Numerical geometry tolerance, fabrication tolerance and measurement uncertainty stay three separate quantities.

## Verified source context

SSY-04 already requests CAD as one large item. It needs separate reference, defect, metrology and release tasks; expensive closure mechanisms must stay behind Experiment 01 rather than being modeled first.

Inspected source documents:

- [docs/TASKS.md](TASKS.md)
- [docs/experiment-01-rigid-defect-duct.md](experiment-01-rigid-defect-duct.md)
- [docs/research-plan.md](research-plan.md)


## Revised finish line and priority

Rigid-family CAD parked until SSY-01/02/03 and XC-02 close. SSY-CAD-08/09 are identifier-only placeholders with scope and estimates withheld. No new implementation-sensitive geometry is added.

## Tool and verification decision

**Selected design approach:** CadQuery code-CAD for parameterized families and neutral STEP verification; Onshape for hand-modeled fixtures with confirmed owner account/access. No Onshape automation, credentials or paid access is assumed. Agent owns code-CAD generators/tests; Owner or an authorized CAD operator owns interactive Onshape work. Lack of Onshape access blocks only affected fixture modeling and requires a documented alternative, not the entire parameter pipeline.

The dedicated tooling task budgets environment locking and CI setup. Pin actual Python/CadQuery/OCP versions only after a clean isolated install plus STEP export/reimport smoke test. No version, environment or geometry CI is claimed tested today. CadQuery's official [installation](https://cadquery.readthedocs.io/en/stable/installation.html) and [STEP import/export](https://cadquery.readthedocs.io/en/stable/importexport.html) docs establish the chosen workflow, not a completed build.

Required future automated sequence: read reviewed parameters.csv → reject invalid/missing dimensions and units → regenerate native geometry → export STEP → reimport into a fresh process → calculate geometric metrics → assert against predeclared tolerances. Geometry acceptance uses numeric JSON plus source/export identity; retain screenshots only for explanatory views. A golden image or a hash is not a geometry test. Tests include analytic nominal cases, registered bounds and invalid cases; expected values cannot be copied from the candidate's own output. CAD geometry tests do not validate physical stiffness, safety or fatigue.

Proposed commands (files DO NOT exist yet): `python cad/generate.py --parameters <registered-parameters.csv> --output <temporary-output>`; `python -m pytest cad/tests -q`. The tooling task must replace placeholders with actual checked-in defaults and wire CI before a model task can close.

## Rebaselined allocation

**0 estimated hours in the prioritized phase; 26 estimated hours parked; 2 withheld tasks have no public estimate (not zero).** This supersedes the previous CAD allocation, not the original 30-hour software sprint. Only tasks marked todo are executable now; blocked/parked estimates are not scheduled work. Owner decisions, fabrication lead times and external calibration do not shrink into focused hours.

| Workload day | Hours | Order |
| --- | ---: | --- |
| Parked | 0 active | Owner/research entry decision required |

## Individual work orders

IDs retain continuity with the first PR. New IDs represent split inputs, tooling or release tasks; display order is execution priority rather than numerical ID order. Proposed deliverables below are NEW, not present artifacts. Current status exists only in CAD_TASKS.csv.

### SSY-CAD-01 — Translate SSY-03 into a CAD parameter and defect contract

- Owner: Agent; priority: P2; estimate: 2 h; day: conditional.
- Dependencies: SSY-01;SSY-02;SSY-03;XC-02.
- Proposed output: `NEW cad/shroud/parameters.csv; cad/shroud/design-inputs.md`.
- Done when: Draft rotor frame, duct profile, uniform/two-lobe/seam/radial-step definitions, equal-mean convention and source status. Released parameter values depend on completion of SSY-01/02/03; do not invent those decisions.
- Verification/evidence: Review mappings to SSY-03 and matched-thrust protocol; list undecided amplitudes, tolerances and metrology resolution explicitly.

### SSY-CAD-02 — Approve reference geometry and design/fabrication input split

- Owner: Owner; priority: P2; estimate: 2 h; day: conditional.
- Dependencies: SSY-CAD-01;SSY-01;SSY-02;SSY-03;XC-02.
- Proposed output: `NEW cad/shroud/owner-inputs.md`.
- Done when: Confirm SSY-01/02/03 decisions and a sourced nominal rotor/reference profile for desk CAD. Separately record actual stand, probe and qualified containment access as available or pending; missing hardware does not prevent a clearly nominal design-only floor.
- Verification/evidence: Sign parameter contract and identify which interfaces are provisional; no fabrication release from assumed stand dimensions.

### SSY-CAD-10 — Establish code-CAD regeneration and CI geometry tests

- Owner: Agent; priority: P2; estimate: 3 h; day: conditional.
- Dependencies: SSY-CAD-02;XC-02.
- Proposed output: `NEW cad/requirements.lock; cad/generate.py; cad/tests/; .github/workflows/cad-geometry.yml`.
- Done when: Use CadQuery for parameter-driven families and neutral STEP checks, Onshape for hand-modeled fixtures after confirming account/access. Pin Python/CadQuery/OCP dependencies after a clean isolated install and export/reimport smoke test. Add geometry CI before accepting a parametric model; screenshots are supplementary, not acceptance.
- Verification/evidence: Proposed commands, NOT YET IMPLEMENTED: python cad/generate.py --parameters <registered-parameters.csv> --output <temporary-output>; python -m pytest cad/tests -q. Assert geometry metrics against a reviewed contract with declared tolerances; prove failure on an altered parameter, invalid dimensions, missing inputs and bad STEP. Retain version lock, numeric JSON and STEP outputs.

### SSY-CAD-03 — Model open-rotor carrier and continuous reference duct

- Owner: Agent; priority: P2; estimate: 4 h; day: conditional.
- Dependencies: SSY-CAD-02;SSY-CAD-10.
- Proposed output: `NEW cad/shroud/reference/ (source, STEP, datums)`.
- Done when: Use shared rotor-axis/stand datums and nominal profile; model monolithic reference plus removable open-rotor configuration without silently changing support blockage. Register static clearance, inlet arrangement and surface finish assumptions.
- Verification/evidence: Check symmetry, mounting repeatability, inlet/support obstruction and section dimensions; retain source-generated nominal gap samples.

### SSY-CAD-04 — Model uniform-clearance and two-lobe inserts

- Owner: Agent; priority: P2; estimate: 4 h; day: conditional.
- Dependencies: SSY-CAD-03.
- Proposed output: `NEW cad/shroud/inserts/harmonics/ (source, STEP, parameter cases)`.
- Done when: Parameterize interchangeable uniform and two-lobe treatments at the registered equal mean; isolate amplitude from mounting changes. Reject intersecting rotor envelopes and record minimum static clearance independently of mean.
- Verification/evidence: Regenerate each registered case; sample clearance around the full circumference and compare mean/harmonic amplitude against the contract, including zero-amplitude equivalence. CadQuery CI regenerates parameter rows, exports/reimports STEP and asserts clearance mean/harmonics/minimum, domain masks and volume against declared tolerances. Missing seam walls remain undefined, not fictitious finite radii. Test zero-defect and invalid-overlap cases.

### SSY-CAD-05 — Model discrete seam and radial-step insert families

- Owner: Agent; priority: P2; estimate: 4 h; day: conditional.
- Dependencies: SSY-CAD-03.
- Proposed output: `NEW cad/shroud/inserts/discrete/ (source, STEP, detail drawings)`.
- Done when: Define seam width/depth and local radial steps with explicit averaging convention, seam endpoint treatment and unchanged reference datums. Seam belongs to the pilot; step fabrication/testing requires its registered extension. A missing wall cannot be assigned a fictitious finite radial clearance.
- Verification/evidence: Check limiting zero-defect cases, domain of clearance sampling and equal-mean calculation; retain descriptor/geometry correspondence and separate undefined seam samples. CadQuery CI regenerates parameter rows, exports/reimports STEP and asserts clearance mean/harmonics/minimum, domain masks and volume against declared tolerances. Missing seam walls remain undefined, not fictitious finite radii. Test zero-defect and invalid-overlap cases.

### SSY-CAD-06 — Model exchange, alignment and clearance-metrology interfaces

- Owner: Agent; priority: P2; estimate: 4 h; day: conditional.
- Dependencies: SSY-CAD-02;SSY-CAD-03;SSY-CAD-04;SSY-CAD-05.
- Proposed output: `NEW cad/shroud/stand-interface/ (source, STEP, probe-access drawings)`.
- Done when: Design indexing/retention, rotor-axis alignment and dynamic-clearance probe/camera access around actual or explicitly nominal instruments. Keep the experimental duct distinct from qualified blade containment; external shielding must not bias inlet flow unnoticed.
- Verification/evidence: Review repeatability stack-up, sensor line of sight, installation/removal and inlet obstruction. Pending actual hardware blocks fabrication, not nominal floor CAD.

### SSY-CAD-07 — Release the rigid-defect inspection and CAD evidence pack

- Owner: Agent; priority: P2; estimate: 3 h; day: conditional.
- Dependencies: SSY-CAD-04;SSY-CAD-05;SSY-CAD-06.
- Proposed output: `NEW cad/shroud/release/ (BOM, drawings, export/descriptor manifest, inspection sheets)`.
- Done when: Deliver native/source version, STEP, defect parameters, toleranced datums, comparable cross-section/exploded views and individual specimen inspection points. Split nominal design review from fabrication release; reconcile SSY-04 acceptance without claiming SSY-06 research floor complete.
- Verification/evidence: Reopen all exports, compare profile/clearance descriptors and check units/part IDs. Retain hashes and review findings; data collection requires qualified measurement system and facility approval.

### SSY-CAD-08 — Details withheld pending XC-02

Details and estimates withheld until XC-02 closes. Do not restore detail from prior commits without that decision.

### SSY-CAD-09 — Details withheld pending XC-02

Details and estimates withheld until XC-02 closes. Do not restore detail from prior commits without that decision.

## Stop and release rules

Do not equate prepared drawings with fabricated/inspected apparatus. Unknown fit-critical dimensions block manufacture. Owner/facility review, actual metrology and prospective reference freezes remain separate gates. No spending, manufacture, pressurization, rotor operation, flight, publication or new third-party drawing disclosure is authorized here.

If time overruns, cut decorative views and already-parked variants first. Keep reference controls, fit/clearance tests, source provenance, filled measurement budgets and pre-load model freeze. Update estimates explicitly rather than claiming blocked hours as progress. Every future public visual needs a source/version, problem explained and CAD-only label.
