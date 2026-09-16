# Segmented-shroud aeromechanics — research programme

Status: proposal for owner review, 2026-09-16. Three-year, gate-driven; one publishable unit per phase. Nothing here is a result. Evidence state of the repository: research design; no CAD, CFD, FEA or measured results.

Scope of this document: the owner's four-study outline (A CFD parametric, B budget feed, C pilot, D decisive) stress-tested, revised where it does not survive, and turned into studies with a first experiment, a kill criterion and an honest claim boundary each. Companion files: [scope.md](scope.md) (what is built when, with triggers) and [plan.md](plan.md) (the first work order). Repository rules that bind every study: [research plan](../../research-plan.md), [claim ledger](../../claim-ledger.md), [measurement-requirements draft](../../measurement-system-spec.md), [prior-art boundary](../../prior-art.md), and the [disclosure boundary](../../../CONTRIBUTING.md#public-disclosure-boundary) (XC-02 open: no closure-mechanism detail).

## 1. Audited state, restated with sources

| item | state | source |
| --- | --- | --- |
| Prior-art coverage of the day-1 set by the canonical export | 4 of 6 eligible sources recovered; historical export credited for nothing | [reference coverage](../../reference-coverage-2026-09-12.md) |
| Novelty axes `equal_mean_clearance_discrete_seams`, `held_out_prediction` | supported-bounded: no inspected source addresses them; unresolved for S3, S4, S5 (and S7) | same |
| Closest 2026 works | S3 nonuniform clearance *layouts*, compressor, paywalled; S4 "segmented ducted fan" = axial duct spacing, CFD only | [day-3 review](../../day3-source-review.md) |
| Top-25 database triage | 22 include / 3 exclude / 0 defer; strongest lead is a 1997 compressor study where non-uniform clearance hurt stall margin more than the mean predicted | [triage report](../../prior-art-search-2026-09-14-screening.md) |
| Stage-A stop rule | implemented, fail-closed, `INPUTS_PENDING` with seven pending terms | `scripts/clearance_uncertainty_budget.py` |
| Open owner inputs | IN-01 minimum clearance effect, IN-02 target mean clearance, IN-03 minimum power difference at matched thrust, IN-04 rotor/stand/sensor envelope, IN-07 XC-02 | [spec §5](../../measurement-system-spec.md#5-open-input-register-and-release-criteria) |
| Compute available today | Apple M1 Pro, 10 cores, 16 GB; Docker present; no OpenFOAM or SU2 installed; gmsh present | checked 2026-09-16 |

## 2. The question

Owner's wording: *At equal mean tip clearance, do discrete circumferential seams in a ducted-rotor shroud change thrust, efficiency, or tonal noise relative to a continuous duct, and is the effect predictable from seam count, gap, and misalignment?*

Aligned to the repository's registered questions: the first clause is RQ1 with the defect family restricted to seams and the control fixed as the continuous duct at the same mean clearance; the second clause is RQ2 (H2, held-out prediction) with the descriptor basis named. Two edits are required for the question to be well-posed:

1. **"Equal mean clearance" needs the averaging rule first.** A seam has no wall over its angular extent, so there is no finite clearance there. The [spec's §1.3](../../measurement-system-spec.md#13-averaging-domain-and-the-missing-wall-rule) gives three admissible treatments (wall-only mean, fixed grid with declared occlusion, or both). CFD can evaluate both cheaply on the same geometry, which no rig can; that is one of Study A's jobs, not a footnote.
2. **Tonal noise moves out of the primary question.** The repository excludes acoustics as a headline contribution ([research plan, scope](../../research-plan.md#scope)), and steady CFD cannot produce it. Noise is a secondary observable of Study D and a triggered extension in [scope.md](scope.md).

Revised primary question: *At equal mean tip clearance under a declared averaging rule, and at matched thrust, do discrete circumferential seams (count n, gap g, radial step s) change shaft power and thrust relative to a continuous duct by more than the combined numerical and measurement uncertainty, and does a descriptor model in (n, g, s) predict a held-out seam configuration better than a mean-clearance model?*

## 3. Steelman of the owner's outline

Position: *run steady RANS with a rotating frame now, use its predicted effect as the minimum effect of interest, let the budget decide whether a pilot is worth building, and fund the decisive study from the budget's instrumentation list.*

| Angle | Case for | Case against | Winner |
| --- | --- | --- | --- |
| Simulation before hardware | • No rig exists; CFD is the only route to a number this year<br>• The repository already demands a numeric MEI before Stage A; CFD is the cheapest source of a plausible range<br>• Parametric sweeps over (n, g, s) are far cheaper in CFD than as inserts | • Tip-leakage flow is where RANS is least trustworthy; a CFD null could be a model artefact<br>• Without validation against a measured ducted fan, no seam prediction is credible | **For**, conditional on a validation study first |
| Steady RANS with a rotating frame | • Standard, cheap, converges on a laptop<br>• Adequate for an axisymmetric duct | • Seams break axisymmetry: the rotor sees a geometry that changes with blade position. A frozen-rotor (MRF) result depends on the arbitrary blade-to-seam clocking; a mixing plane averages away the very effect under study<br>• Tonal noise is unsteady by definition; steady RANS produces none | **Against**. Fix: full-360° MRF at several clocking positions with the spread carried as method uncertainty, unsteady sliding-mesh confirmation on a few cases, acoustics deferred |
| Kill criterion: effect below numerical uncertainty | • Correct shape: an effect you cannot separate from discretisation error is not a finding<br>• Forces the mesh-convergence work that most CFD papers skip | • "Numerical uncertainty" is only the GCI term; clocking spread and turbulence-model sensitivity are as large or larger for tip flows<br>• A correct kill here says "not resolvable by this route", not "no effect" | **For, with the uncertainty band widened** to GCI ⊕ clocking ⊕ model |
| CFD effect as the minimum effect of interest | • Gives the owner a defensible, non-arbitrary number<br>• Converts `INPUTS_PENDING` into an instrumentation requirement immediately | • MEI is a *decision* about the smallest effect worth knowing; the register says a measurement cannot supply it, and neither can a model. If CFD over-predicts, the rig is specified too loosely and the pilot cannot see the real effect<br>• The budget's MEI is in µm (clearance-equivalent); the CFD effect is in W. A conversion through dP/dc̄ carries its own uncertainty | **Reframing**: CFD bounds the plausible range and supplies the sensitivity; the owner sets IN-03 (W) as a decision informed by it; IN-01 (µm) follows through dP/dc̄ with its uncertainty stated |
| Validation | • The literature already validates RANS on ducted fans in general | • "In general" is not this rotor, this solver, this mesh, this laptop. The repository's own claim ledger allows CFD evidence only "under stated assumptions"; unvalidated CFD cannot even set a range | **Against**: a validation study (A0) is a must-have |
| Execution on a 16 GB laptop | • Steady 360° cases of 4–6 M cells run in hours; a screening design of ~15 cases is feasible in weeks<br>• Docker gives OpenFOAM on arm64 without a cluster | • Unsteady sliding-mesh cases are 10–20× slower; more than two or three is not feasible here<br>• Resolving a ~1 mm tip gap with ≥10 cells across it pushes cell counts up fast | **Even**: feasible for A0 and the steady screening of A; unsteady confirmation and acoustics need more compute |
| Disclosure (XC-02 open) | • A rigid duct with idealised slots is generic; it discloses no closure mechanism | • Misalignment/step patterns chosen to mimic a specific segment joint could disclose mechanism intent | **For**, with the rule that seam patterns are parameterised generically (n, g, s) and no joint geometry appears |

**Aggregate verdict: the outline needs revision, not replacement.** It loses on the method for Study A and on the missing validation, and the MEI logic needs reframing. It wins on order (simulation first), on the gate logic, and on the funding structure.

## 4. Revised study sequence

Every study below has the six-field first-experiment spec and a kill criterion. Evidence-state words follow the [claim ledger](../../claim-ledger.md): what these studies produce is **CFD** evidence, then **measured** evidence; neither is novelty.

### Study A0 — CFD credibility on a measured ducted fan (must-have, first)

*Why:* no seam prediction is worth a number until the same toolchain reproduces a published ducted-fan baseline with a stated uncertainty.

- **Hypothesis.** The chosen toolchain reproduces the published thrust coefficient of a documented ducted fan at its baseline tip clearance within 5 %, and the published sign and order of magnitude of the clearance sensitivity dT/dc̄, with a grid-convergence uncertainty below 2 % on thrust.
- **Setup.** OpenFOAM (arm64 container) or SU2, gmsh or snappyHexMesh, one workstation-class laptop. Baseline dataset candidates, in order of preference, each with a check task in [plan.md](plan.md) because geometry availability is unverified: S1 Ryu et al. 2017 (150 mm counter-rotating ducted fan; measured baseline with a CFD clearance sweep; full text on file), the Akturk–Camci ducted fan (559 mm, force/torque and Kiel-probe data; in the close-reading queue), or, if neither publishes blade geometry, a fully open rotor geometry with the baseline measured later on the project's own stand (weakest: validation deferred to Study C).
- **Variables.** Varied: mesh (three levels, refinement ratio ≥ 1.3), turbulence model (k-ω SST and Spalart–Allmaras). Measured: thrust, torque, shaft power, tip-gap mass flow. Held constant: geometry, operating point, boundary conditions as published.
- **Success criterion.** Thrust within 5 % of the published value on the finest mesh; GCI (Roache, Fs = 1.25) on thrust ≤ 2 %; model-to-model difference reported; clearance sensitivity sign correct and magnitude within the published experiment-to-CFD spread.
- **Timebox.** Two weeks for one baseline; the first week is geometry and mesh.
- **Kill criterion.** Thrust off by more than 10 % after mesh and model checks, or GCI that will not fall below 5 % within the laptop's memory: the CFD route is not credible on this toolchain and hardware, and the programme reverts to a measurement-first path with Study C's budget set from literature bounds only.

### Study A — CFD parametric seam study with an uncertainty band (must-have)

*Why:* the cheapest test of whether seams can matter at equal mean clearance, and the only place both averaging rules can be evaluated on identical geometry.

- **Hypothesis (H1-CFD).** At equal wall-region mean clearance and matched thrust, at least one (n, g, s) configuration changes shaft power by more than the combined uncertainty band U = √(GCI² + clocking² + model²).
- **Setup.** The validated A0 toolchain and rotor; a continuous duct control; slotted-duct variants parameterised only by seam count n, gap g, and radial step s; no joint geometry. Full-360° domain, MRF steady runs for screening, unsteady sliding-mesh (AMI) runs for two confirmation cases.
- **Variables.** Factors: n ∈ {2, 3, 4}, g/c̄ ∈ {0.5, 1, 2}, s/c̄ ∈ {0, 0.5, 1} in a resolution-IV fractional factorial plus centre (≈ 10–12 screening runs), control at three meshes, two extreme cases at three meshes and four clocking positions each, turbulence-model swap on the same two. Measured: thrust, torque, shaft power, tip-gap flow, circumferential loading. Held constant: operating point (matched thrust by iteration on rotor speed), inlet/outlet conditions, mesh topology across variants.
- **Both averaging rules.** Every case is post-processed under the wall-only rule and the fixed-grid-with-occlusion rule; the study reports whether the two rank conditions the same. If they do not, the spec's IN-08 is decided by this result before any hardware.
- **Success criterion.** Effect sizes on ΔP and ΔT with U attached for every screening case; at least one main effect with |ΔP| > U; a descriptor model fitted on the screening set predicting a held-out seam count within its stated interval (a within-support test only, per the [identifiability gate](../../research-plan.md#model-identifiability-gate-before-family-holdout)).
- **Timebox.** Six weeks after A0: two for geometry and mesh templates, three for runs, one for the uncertainty analysis and report. Unsteady confirmation runs overnight-to-days each; at most three.
- **Kill criterion.** |ΔP| < U and |ΔT| < U for every factor at every level: the question is not resolvable by steady-plus-limited-unsteady CFD on this hardware. That is a reportable result (a CFD-bounded null) and it re-routes Study B to literature-bounded inputs.

### Study B — feed the budget (must-have, follows A)

*Why:* turns the stop rule from `INPUTS_PENDING` into a numeric instrumentation requirement, with the numbers owned by the right role.

- **Rule.** CFD does not set the minimum effect of interest; it bounds it. The owner sets **IN-03**, the minimum meaningful power difference at matched thrust in W (or a declared ratio with its denominator), as a decision: the smallest effect that would change a design choice, informed by Study A's range. **IN-01**, the clearance-equivalent MEI in µm, follows as IN-03 divided by the clearance sensitivity dP/dc̄ from A0/A, with that sensitivity's uncertainty propagated and recorded. **IN-02**, target mean clearance, follows from the A0 baseline geometry.
- **Record.** The three values enter `docs/clearance-measurement-budget.csv` as `owner_decision` rows with sources citing the Study A record; the calculator is re-run. The verdict stays `INPUTS_PENDING` on the five installed contributors, but the budget now states the required combined uncertainty u_c < IN-01 / k, which is the number the rig must meet.
- **Kill criterion.** If the required u_c is smaller than about half the literature accuracy of the S5/S6 sensor class (25 µm), no known sensor meets it without in-situ calibration gains: Study C is not worth building as specified and the effect target or the rotor scale must change.

### Study C — pilot on the existing thrust-stand concept (trigger-gated)

*Why:* the smallest measured test of H1; the budget decides whether it is worth building.

- **Trigger.** Study B's required u_c is achievable with a named sensor and rig, IN-04 is filled with actual resources, and IN-06's calibration plan exists.
- **Hypothesis.** One seam configuration (the largest |ΔP| from Study A) and the continuous control differ in electrical power at matched thrust by more than k·u(ΔP), with open rotor and monolithic duct as references.
- **Setup.** Existing thrust-stand concept, one duct, interchangeable inserts (rigid, no mechanism), S5/S6-class clearance sensing calibrated in situ, [Stage A](../../experiment-01-rigid-defect-duct.md#stage-a--measurement-system-qualification) passed first.
- **Success criterion.** Stage A `FEASIBLE`; ΔP resolved at every matched-thrust set-point; agreement in sign with Study A, with the CFD-to-measured gap reported as the model's transfer error.
- **Timebox.** Two weeks of runs after commissioning; commissioning itself is Stage 1 of the [roadmap](../../../ROADMAP.md).
- **Kill criterion.** Stage A returns `STOP_INSTRUMENTATION_REDESIGN`, or the measured |ΔP| is inside k·u(ΔP): publish the tolerance result and stop mechanism integration (the roadmap's failure branch).

### Study D — decisive, funded (trigger-gated)

*Why:* the held-out prediction claim and any acoustic observable need more geometries, an unbuilt configuration, and instrumentation the budget names.

- **Trigger.** Study C positive; funding secured against the instrumentation list produced by Study B; XC-02 closed if any mechanism-derived seam pattern is to be used.
- **Content.** Multiple seam geometries covering the descriptor support; a preregistered model; prediction of an unbuilt configuration before it is built; acoustic measurement as a secondary observable; the roadmap's Stage 2 exit gate (held-out error below 10 % and at least 20 % better than mean-clearance).
- **Kill criterion.** Held-out error not better than the mean-clearance baseline: the simpler-model result is published as the finding.

## 5. Method commitments for the CFD studies

- **Numerical uncertainty.** Three meshes with refinement ratio ≥ 1.3; observed order of convergence and GCI on the finest mesh (Roache, Fs = 1.25 when the observed order is close to formal); iterative convergence to residual and monitor-quantity plateaus recorded per case. This follows the ASME V&V 20 structure of separating numerical from model uncertainty; it is a method reference, not a certification.
- **Clocking uncertainty.** For steady MRF cases with seams, four rotor positions spanning one blade pitch; the spread enters U.
- **Model uncertainty.** Two turbulence models on the extreme cases; the difference enters U. Wall treatment and y⁺ range stated per mesh.
- **Unsteady confirmation.** Sliding-mesh (AMI) runs on the control and the largest-effect case; time-step from a target of ≥ 100 steps per blade passage; effect sizes compared with the steady values.
- **Power quantity.** CFD yields aerodynamic shaft power (torque × ω). The rig measures electrical power; the bridge is a motor-efficiency map measured in Stage A. Both are always reported separately, as the research plan requires.
- **Matched thrust.** Each variant is iterated on rotor speed to the control's thrust; matched-RPM results are kept as the secondary diagnostic.
- **Preregistration.** The screening design, the uncertainty definition, the averaging rules and the held-out configuration are committed to the repository before the first variant runs. Study A's record folder carries the commit hash of that freeze.
- **Provenance.** Every case is a manifest (geometry revision, mesh hash, solver version, settings, commit) under the [data contract](../../data-and-figures.md); results regenerate from raw case files.

## 6. Feasibility on the hardware at hand

Order-of-magnitude estimates, to be replaced by A0's observations:

| item | estimate | basis |
| --- | --- | --- |
| cell count, 360° ducted rotor with ≥ 10 cells across a ~1 mm gap, wall functions | 4–8 M | 16 GB allows roughly 6–8 M cells for a steady incompressible solver |
| steady MRF case, 8 cores | 1–4 h | typical simpleFoam throughput at this size |
| screening study, ≈ 15 cases + 6 mesh-study cases + 8 clocking cases | 1–2 weeks of wall time | serial on one machine |
| unsteady sliding-mesh case | 1–3 days each | 10–20× steady |
| A0 + A total | ≈ 8 weeks | includes geometry, meshing, two reports |

These numbers are assumptions until A0 records actual timings; if the gap cannot be resolved within memory, the rotor scale or the gap ratio changes before any variant is run, and the change is recorded.

## 7. What the programme can and cannot claim

- It can claim, after A: a CFD-bounded effect size (or null) of seam descriptors at equal wall-region mean clearance for one rotor, with uncertainty; and whether the two averaging rules agree.
- It can claim, after C: a measured effect (or null) for one configuration on one rotor scale.
- It can claim, after D: a held-out prediction result within the registered descriptor support.
- It cannot claim global novelty (the axis table is bounded to inspected sources; S2/S3 unread; 111 records unscreened; no patent search yet), a performance-duct or protective-guard result, or anything about a closure mechanism while XC-02 is open.

## 8. Programme shape (36 months, gate-driven, not calendar-driven)

| phase | studies | exit gate | publishable unit |
| --- | --- | --- | --- |
| 1 (months 1–6) | systematic prior-art closeout (close-read the 22 includes, second frozen batch for the 111, dated patent search), A0, A, B | A's uncertainty-bounded result and the budget with owner numbers | Paper 1: CFD-bounded parametric study of equal-mean seam defects with a validated toolchain |
| 2 (months 6–18) | Stage 1 qualification, C | Stage A `FEASIBLE`; pilot result | Paper 2: measurement-system qualification and pilot |
| 3 (months 18–36) | D; mechanism work only if Stage 2 passes and XC-02 is closed | roadmap Stage 2 gate; Stage 3 conditional | Paper 3: held-out prediction; the three papers together are the programme's written record |

A null at any gate is written up at that gate; the roadmap's failure branches are alternative outcomes of the programme, not its failure.

## 9. Risks and honest limits

- **Geometry availability** for A0 is unverified; if no published rotor has usable blade geometry, validation slips to Study C and every CFD number before that carries an "unvalidated" label.
- **RANS on tip-leakage flow** may under-predict unsteady effects; the unsteady confirmation is limited to three cases by compute.
- **The owner's inputs** IN-01 to IN-04 are decisions; Study B prepares them but cannot make them.
- **Funding** for Study D is not assumed; the programme's floor is the CFD-bounded result plus the qualified measurement system.
- **Disclosure**: seam patterns stay generic (n, g, s); anything derived from a real segment joint waits for XC-02.

## 10. Scores (project-builder rubric)

| direction | evidence 30 | specificity 25 | execution fit 20 | distinctiveness 15 | traceability 10 | total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A0 + A: validated CFD parametric seam study | 24 (tip-clearance CFD well supported; seams at equal mean unaddressed in inspected sources) | 23 | 16 (laptop-feasible for steady; unsteady limited) | 13 | 10 | 86 |
| B: budget feed | 20 | 25 | 20 | 8 (methodological) | 10 | 83 |
| C: pilot | 18 | 20 | 8 (no rig yet) | 12 | 10 | 68 |
| D: decisive | 15 | 18 | 4 (funding, rig) | 15 | 10 | 62 |
