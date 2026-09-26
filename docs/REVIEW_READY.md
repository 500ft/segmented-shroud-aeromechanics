# Review index

## 2026-09-26 — the convergence criterion answered, and CAD assessed as gated

Ledger rows SSY-R22 (partly closed) and SSY-R23.

**The flatness criterion no longer decides silently.** Provenance finding F3 left two selected values in force with no sensitivity behind them: a relative variation of one part in ten thousand over the last five hundred iterations, which is what separates a passing case from an unconverged one. The question is now answered against the committed histories, with no solver run.

Loosening changes nothing: every passing case still passes an order looser, so no recorded conclusion depends on the criterion being as strict as it is. Tightening is a different story. Three of the five passing cases fail one order tighter, with spreads between one and two parts in a hundred thousand against a threshold of one in ten thousand. The criterion sits closer to its margin than its round value suggests, and the window length matters as much as the tolerance, since the finest Spalart-Allmaras case also fails when the window is lengthened fourfold.

**The stalled case was never assessed, rather than assessed and found wanting.** The fine-grid shear-stress-transport run reached iteration 117, well short of a single window, so the criterion could never be applied to it. It is recorded as unconverged, which reads as a judgement that was never made. The compute-recovery record had flagged exactly this as unresolved, and it is now resolved. The status vocabulary needs a third term so a terminated run is not reported as a failed one; that is registered rather than done.

One limitation governs all of it. The committed histories are downsampled to roughly one sample per fifty iterations, so every spread is a lower bound on what the full history would show. Passing verdicts are therefore optimistic; failures and unassessable runs are sound. That is stated in the record itself rather than left for a reader to infer.

The criterion is left exactly as it was. Nothing recorded changes, and altering an acceptance rule after seeing results is the move this project's discipline exists to prevent.

**CAD was assessed and remains gated.** All ten tasks in the CAD ledger are deferred, and every one of them is transitively blocked: the two identifier-only placeholders on the disclosure path, and the other eight on a chain rooting in SSY-01, SSY-02, SSY-03 and the same disclosure decision. Even the tooling task, which looks like pure infrastructure, depends on the reference-geometry approval beneath it. The plan says in terms that released parameter values depend on those closures and that they must not be invented. No geometry was produced and no remote host was contacted, because there is nothing that could be built without fabricating a rotor radius, a mean clearance and a seam geometry that no decision has set.

## 2026-09-25 (third) — provenance audit of consequential numbers

Ledger row SSY-R21. An audit of documentation and traceability. No requirement, threshold, solver setting or geometry was changed by producing it.

**The gap was not missing vocabularies but missing coverage.** Three already existed: evidence labels on the A0 source parameters, evidence states on the clearance budget terms, and the claim ledger's own scale. Each governs one artifact well. None covered a number used in more than one place, so a repeated quantity had no single definition and nothing could notice two documents disagreeing.

Ten such quantities now have one definition each, with a provenance category, an evidence status, units, limits, and where relevant the question that would resolve them. Seven are tied to the code that implements them, and `scripts/check_quantities.py` fails when the two drift. A register nobody checks is decoration, so the checker runs in continuous integration and four deliberate defects were confirmed to fail it: a constant changed without the register, a defaulted gate drifting, a provisional value with no stated resolution path, and a false claim of physical testing.

**Two gates are enforced in code and derived nowhere.** The Stage 2 exit requires a twenty percent improvement over mean clearance and a held-out error under ten percent. Both are registered, both are enforced, and nothing anywhere states what decision either protects. They are now labelled provisional at the proposal, at the point of enforcement and in the register, each carrying the question that would settle it. The earlier review had already called them provisional; they had not been marked as such where a reader would meet them.

**One sourced assumption was applied outside its stated condition.** The grid-convergence safety factor of 1.25 comes from Celik and colleagues, who prescribe it where the observed order of convergence is close to the formal order. A0.1's observed order is 2.6697 against a formal order near two, and the procedure never limits it. Rather than assert this either way, the audit computed it: across the defensible combinations of factor and order limiting, the fine-grid index runs from 0.153 to 0.658 percent. The comparison error is 2.22 percent of the reference, between three and fifteen times the largest of them. **The choice does not change the conclusion of this case**, and that is now recorded beside the result rather than left for a reader to wonder about. A test recomputes the whole table from the committed record.

**Two convergence constants decide more than they look like they do.** A flatness of one part in ten thousand over the last five hundred iterations is what separates a passing case from an unconverged one, and it is what recorded the A0.1 fine-grid shear-stress-transport case as failed. Both are selected values with no provenance and no sensitivity study, and they are now labelled as such.

**A fixture constant could have been misread as a project target.** The synthetic fixtures use a mean clearance of one thousand micrometres, which is a plausible real value. It is now stated at the constant itself that this is not the target mean clearance, which remains an unset owner input.

A traceability index links each consequential decision to its reasoning, its registered inputs, its validation and its status, without repeating a single equation. Fourteen rows: four supported, three provisional, six blocked on inputs that do not exist, one unresolved by owner decision.

Nothing here makes a prediction into a measurement. This project has made no measurement, and the register refuses to let any quantity claim otherwise.

## 2026-09-25 — evidence and protocol closeout

Ledger rows SSY-R16 to SSY-R19. Review items R08, R09, R11 and R12.

**A sensitivity flag was being quoted as a correction.** The A0.2 case notes turned the Prandtl-Glauert factor at Mtip 0.437 into a predicted eleven percent discrepancy in outboard sectional pressure. That relation is linearised, thin-aerofoil, two-dimensional and irrotational; a rotor blade section carries induced flow, radial flow, thickness and viscous effects that it does not describe. What survives is that compressibility is not negligible here and an incompressible solver carries a bias of **unknown** size. D10's option (b) can therefore no longer be read as a declared bias of known magnitude, and the recommendation for any pressure-comparison claim is a verified compressible workflow. The recommendation is prepared for the decision owner, not adopted.

**D10 no longer blocks the fine-grid recovery.** It governs A0.2. The unfinished A0.1 shear-stress-transport arm is a separate work item whose prerequisites are resource headroom, checkpoint integrity and the existing run protocol.

**The budget stopped inverting a derivative from another machine.** The rule set the clearance-equivalent effect of interest by dividing the power target by a sensitivity taken from the large computational rotor. That is withdrawn. Power detectability and clearance-setting fidelity are separate requirements, linked only through a model that is actually supported, which would need the same machine, endpoint and operating point, a justified local slope with sign and uncertainty, and a rule for where the slope approaches zero or changes sign.

**The sensor kill criterion is withdrawn.** It ruled out the pilot study whenever the required uncertainty fell below about half of one published accuracy figure for one sensor class. An accuracy quoted for a different rig is not an installed standard uncertainty, and one sensing paper does not establish the best achievable limit of all methods. Candidate methods are now named with an installed calibration and feasibility plan, and the published figure stays in the register as a literature bound that is recorded and never combined.

**The validation cases now say what they cannot support.** A scope map carries four rows: the two A0.1 arms, planned A0.2, and a candidate ducted-fan benchmark. Agreement on thrust and pressure does not validate shaft torque, gap leakage or tip-vortex trajectory.

**The benchmark was audited rather than assumed.** An open conference copy of the ducted-fan study was retrieved and read. It gives hub and tip radii, blade count, pitch angle and a nine-station table of chord and blade angles. It does **not** give blade section coordinates, the duct profile as coordinates, any Reynolds or Mach number, or any numerical or experimental uncertainty on the integrated coefficients: three meshes were compared by inspecting one pressure profile. Readable is not reproducible. Usefully, it measures ducted-fan thrust and rotor-only thrust separately, which is the force boundary this project's contract now requires, and it varies clearance by changing rotor diameter, so its rotor is not the same machine between conditions.

**Transient acceptance is specified before any case runs.** Estimand, phase interval derived from the real geometry rather than inherited from an axisymmetric sector, nested phase refinement, a selection rule committed before screening outcomes, time resolution set by the narrowest seam encounter rather than a universal steps-per-passage figure, and three outcomes with no fourth. The numerical tolerance stays `TOLERANCE_NOT_FROZEN`, and the classifier refuses to decide anything without one, which is what stops an attractive percentage being chosen after the result. The clocking and model envelope is reported as a sum over sampled choices and never as a worst case.

**Access quality and evidence strength are now separate axes.** A single grade A had rested partly on a full text being available; the validated baseline and the predictions for unmeasured geometries are now graded separately. The ducted-fan source's blanket institutional-access requirement is withdrawn, since an open route was verified. Two retrievals failed and stayed failures: the compressor paper served metadata but no abstract, and the non-axisymmetric clearance study has a green open-access copy indexed at MIT whose download is behind a human-verification interstitial that was not circumvented. Neither became an absence finding, and neither may be cited as read. That study's date is corrected from its conference year to its issue date.

The conservative claim boundary is frozen at the top of the literature review: nonuniform-clearance sensitivity and matched-equivalent-clearance comparison are established methods, not contributions of this work.
## 2026-09-25 (later) — Study A candidate design and attempt dispositions

Ledger rows SSY-R14 and SSY-R15. Review items R10 and R13.

**The design matrix is now a table, not an adjective.** The plan previously named three factors and roughly ten to twelve runs as a resolution-IV design without giving the rows, so there was no way to tell what could be estimated. The candidate is thirteen unique locations of a three-factor Box-Behnken layout against a ten-column quadratic basis, plus four reserved holdouts and three controls. The exact rows live in one machine-readable file and the prose table is generated from it, so a row cannot be edited in prose without the audit moving.

Rank is ten of ten and the condition number is 7.109340 under the stated scaling convention. Those numbers were reproduced independently here under the repository's pinned NumPy before being adopted, and they match the review's own calculation to six figures.

**What the design cannot see is tested, not asserted.** The three-way interaction is exactly zero at every training location, so a manufactured one is invisible there. The test fits a surface carrying that effect, confirms training recovers the wrong coefficients with zero residual, and confirms the reserved holdouts expose it with the predicted error. Two of the four holdouts carry a non-zero triple product; that is what makes them worth reserving.

The status is `CANDIDATE_DESIGN_AUDITED`. Physical levels are open, no constraint can be evaluated yet because they are all stated in unresolved quantities, and no run is released. Twenty condition labels are not twenty solves.

**The solver no longer squares its own condition number.** Fitting went through normal equations, which square the conditioning of a design whose predictors span degrees, counts and micrometres. It now uses a singular-value decomposition, judging rank on a relative threshold, so a nearly dependent column is refused as well as an exactly dependent one. The change is scoped to fitting. All existing pipeline tests still pass.

**Excluding a run from a fit no longer erases it.** Attempt records carried one notion of validity, and a file that would not parse simply vanished, which means the denominator was being rebuilt from whichever files happened to load. Four independent assessments now travel together: acquisition validity, aerodynamic eligibility, contact outcome, and membership of the attempted-condition denominator.

They are independent but not arbitrary. Invalid acquisition can never be eligible. A rubbing run leaves the steady power fit while staying an observed failure and a counted attempt. A non-detection requires a detector that was working and covering the window; without that the outcome is unknown, and unknown is not success. Unknown outcomes are reported as an interval on the failure fraction rather than folded into the passes.

The attempt register is written before acquisition starts, which is what makes the denominator real. All eight behaviour cases from the review are tested, including duplicate ingestion, retries linked to a parent, and a legacy record with no disposition, which comes through as unknown and never as eligible.

## 2026-09-25 — PR #31 review response: the interpretation made consistent

Ledger row SSY-R13. An owner review of PR #31 found that green CI had not resolved contradictions in the prose and in what the tool actually does. Six findings, all reproduced on the exact head before anything was changed, plus a seventh the new check found by itself.

**A number was enough to become an uncertainty.** The command line accepted the grit spread as `U_D`, so a quantity the same file explicitly calls treatment sensitivity could complete the uncertainty budget just by being passed in. Provenance is now declared with the value, and only an eligible basis supplies `U_D`. An ineligible value is kept and reported, never used and never dropped. The committed A0.1 record was generated through that path, so its `U_D` is reclassified.

**The report contradicted itself twice more.** One passage still called the grit spread trip repeatability and another called it a lower bound on experimental uncertainty, while a third correctly called it treatment sensitivity. A spread produced by deliberately changing the trip bounds nothing about the measurement; that relationship is unknown and was never established. The "lower bound" wording is withdrawn wherever it appeared, including in the claim boundary this tool writes into every record.

**Nothing here validates anything.** The report and the generated claim boundary both said A0.1 validates the workflow while its own verdict was `INCOMPLETE_UNCERTAINTY`. Replaced with what is actually available: numerical evidence for the workflow, a comparison against published computations, and an unresolved comparison against the experiment.

**Two authorities disagreed.** The decision record retired three verdicts at one line and still prescribed one of them sixty lines later. Decision D9 still called the consistency screen an ASME pass rule. Following Eca, Dowding and Roache, that standard estimates discrepancy for specified outputs and conditions and is not inherently a pass or fail exercise. Both are corrected, with the superseded text kept in corrected form rather than deleted. A seventh copy in the A0 case definitions was found by the narrowed check rather than by reading.

**Precedence is now declared rather than incidental.** Unusable numerical evidence outranks the uncertainty state, because there is nothing to compare; missing components are still listed in that case. Usable numerics with a component unquantified give `INCOMPLETE_UNCERTAINTY`. Only a complete budget reaches the consistency screen.

**The tests were checking the wrong thing.** The previous check parsed verdict assignments out of the script, which proves nothing about behaviour on any output path, and scanned documents for one retired term while exempting the very file that still prescribed one. Replaced with the smallest useful document check, covering all three retired terms with no exemption for the decision record, plus behaviour tests that run the real command line end to end against synthetic input. Each was confirmed to fail for the scientific reason, not an import error.

The raw solver output for A0.1 no longer exists, so the record cannot be regenerated. The original stays byte-identical and carries a dated revision derived from it, pinned to its hash by test. The verdict does not move: it was already `INCOMPLETE_UNCERTAINTY`, and this adds a second missing component rather than changing the outcome.

## 2026-09-24 (later) — the corrections propagated into every copy

Ledger row SSY-R12. Follow-up to SSY-R11: the corrections landed in the places that were reviewed and were left stale in the places that were not.

**The validation report contradicted itself.** Section 3 reported the verdict as `INCOMPLETE_UNCERTAINTY`, while the closing sentence of section 6 still said the verdict stands as `NOT_VALIDATED`. A reader who finished the interpretation section got the withdrawn answer. Section 6 now states why `NOT_VALIDATED` is not available at all: with `U_input` unquantified there is no `U_val` for the comparison error to be judged against.

**The research ledger still carried the superseded narrative.** Row SSY-R06 quoted 0.004721 as `U_val`, called the grit spread repeatability, and repeated the claim that every published code misses this experiment by more than this work does. That claim is false and had already been withdrawn in the report. The ledger is the single research ledger, so this was the copy most likely to be read and reused. It now carries the correction and points at SSY-R11.

**The programme plan recorded the retired verdict** against the task that produced it. Restated.

**The decision record and the code named different verdicts.** The record defined `VALIDATED_AT_U_VAL`, `NUMERICALLY_BOUNDED` and `NOT_VALIDATED`; the script emits `INCOMPLETE_UNCERTAINTY`, `CONSISTENT_AT_U_VAL`, `INCONSISTENT_AT_U_VAL` and `INCONCLUSIVE`. The governing spec named a verdict the code could not produce, which is how the retired word survived. The record now defines exactly the four the code emits and marks the other three retired, with the reason each was dropped.

**A test now pins the two together.** It parses the verdict assignments out of the script rather than restating them, fails when an emitted verdict is undefined in the record, fails when a retired verdict is emitted, and fails when one is asserted in a live document. Dated entries here and in the review index are append-only history and are exempt. All three checks were confirmed to fail against a deliberately reintroduced defect and to pass once it was removed.

**Two smaller things.** The claim boundary written into every uncertainty record still described `U_D` as trip repeatability, contradicting the reclassification made a few lines above it in the same script. And `scripts/p2d_to_gmsh.py` imports NumPy while the requirements file declared only jsonschema, so a clean checkout could not rebuild the A0.1 meshes. NumPy is now declared at the version the committed meshes were generated with.

Nothing here changes a number, a run or a frozen acceptance record. The verification gate passes: 141 tests, the repository contract, reference coverage, the acquisition ledger, the clearance budget, and both presentation checks.

## 2026-09-24 — external review corrections applied

Ledger row SSY-R11. [Correction record](corrections/2026-09-24-review-corrections.md).

An external review reproduced several errors by counterexample and they are corrected in place. No raw run, solver output or frozen acceptance record was rewritten; the original calculations stand and only their interpretation changed.

**The universal two-percent floor is withdrawn.** It was inferred from a disagreement in two-dimensional airfoil lift and applied to differences in ducted-rotor power. Those are different quantities at different conditions, and errors in a paired comparison may cancel rather than persist. Study A must assess the sensitivity of its own paired difference.

**The uncertainty arithmetic is repaired.** A `U_val` was reported while a required component was unquantified, which silently treats the unknown as zero. It is now null when a component is missing, the missing ones are named, and the combination of known terms is reported as partial. A0.1's verdict is therefore `INCOMPLETE_UNCERTAINTY`, not `NOT_VALIDATED`. The grit spread that supplied `U_D` is reclassified as treatment sensitivity, because different trips are different conditions rather than repeats.

**The asymptotic-range check confirms nothing.** For equal refinement with a fitted order it is algebraically the fine-to-medium value ratio, which a test now pins. It is a diagnostic and gates no verdict. It was added and praised in this repository two sessions ago, and that was wrong.

**One claim was simply false** and is corrected against the report's own table: the SST reference results miss the experiment by 1.40 and 1.98 percent, *below* this work's 2.24 percent, so "every published code misses by more than this work" does not hold.

The pipeline and design-contract corrections went in with their own pull requests. Remaining review items are recorded in the ledger blocker: the unregistered design matrix, the scale bridge, transient acceptance rules, the budget rationale, literature evidence grades and failure dispositions.

## 2026-09-23 — SSY-05 analysis pipeline, written before the data

Ledger row SSY-R10. [Pipeline](../scripts/analysis_pipeline.py) · [synthetic fixtures](../data/fixtures/synthetic/README.md) · 21 new tests.

The analysis is now fixed in code before any result can influence it, which is the whole point of the task. It ingests synchronised channels, computes wall-domain clearance descriptors with a two-lobe harmonic fit that excludes seam samples, interpolates power to matched thrust, collapses repeated runs to one record per condition, and fits a mean-clearance baseline against a defect-aware model on a registered holdout.

About half the behaviour is refusal, and that is deliberate. It will not read a clearance declared in millimetres, invent a clearance inside a seam where there is no wall, accept a walled sample with no value, extrapolate past the measured thrust range, offer a random split, or fit a descriptor it cannot identify.

**Two defects in my own first version were exposed by the fixtures and are now regression-tested.** The identifiability gate checked each descriptor's spread but not collinearity, so total seam width, which is seam count times a fixed width, passed the gate and made the fit singular; the gate now runs Gram-Schmidt and names which earlier descriptor absorbed the rejected one. And the verdict credited any positive improvement, so the null fixture reported success on a relative improvement of eight parts in ten billion; the verdict is now judged against the roadmap's registered 20 percent improvement and 10 percent error gate rather than against the sign of a floating-point number.

No measurement exists and none is implied. The ingestion schema is provisional until instruments are chosen, and the descriptor set is provisional until Study A registers amplitude levels.

## 2026-09-22 — SSY-03 design contract drafted

Ledger row SSY-R09. [Design contract](design-contract-experiment-01.md).

Uniform gap, ovality, seam and radial step are no longer words. The contract fixes datums and an angular zero, four reference conditions including a **zero-seam segmented control** that separates "assembled from segments" from "has a defect" and an installation re-fit that gives the repeatability every difference is judged against, defect families as equations parametric in the rotor tip radius, three tolerance classes kept separate, matched-thrust primary with matched-RPM secondary, randomised order with a recorded seed, and invalid-condition rules that exclude by rule before the response is inspected.

The equal-mean construction is **verified rather than asserted**: a test integrates the two-lobe family and confirms it is equal-mean for any amplitude and phase, confirms that an alternating segment offset preserves the wall mean exactly for an even seam count, and confirms that it does **not** for an odd count, which is why odd counts need solved offsets that are unequal in magnitude. That is a manufacturing consequence now recorded rather than discovered at assembly.

The contract also records something that would otherwise become a wrong claim: **the Study A computational rotor and the Experiment 01 physical rotor are different machines.** Study A uses the Caradonna–Tung rotor because A0.2 validation transfers to it; the project's distinctiveness rests on small-UAV ducted rotors. They differ by one to two orders of magnitude in tip Reynolds number, so a computed effect size is not a prediction for the rig and may not be carried across without a stated scaling argument.

**SSY-03 is not closed.** This is a draft with twelve open inputs, four of them the owner's, and amplitude levels cannot be set until Study A supplies an expected effect to compare against the 2 percent steady-RANS floor and the rig's pending budget. No fabrication is authorised and the CAD branch remains deferred.

## 2026-09-22 — literature catalogue and thematic review

Ledger row SSY-R08. [Review](literature/README.md) · [catalogue](literature/register.json) · [search evidence](../evidence/task-literature-2026-09-22/README.md).

A thematic search extended the corpus into eight areas the frozen 2026-09-09 query set never reached, reusing the existing search machinery so every record carries raw-response provenance; its audit is clean on all six keys. The merged catalogue holds **1,736 distinct records: 11 close-read, 24 triaged from abstracts, 1,701 merely identified.** The review is organised by the decision each theme informs and states the read state of every record it names.

Three findings worth carrying. The frozen query set **never reached the Vertical Flight Society literature**, where small-scale shrouded-rotor work lives, including hover performance at this project's Reynolds number. The extension surfaced **casing-treatment literature** — single circumferential grooves and their location and depth — which is geometrically close to a seam and was absent from the prior-art map; the project must decide explicitly whether to address it. And the highest-priority unread record in the corpus is now `doi:10.1016/j.ast.2023.108162`, on **circumferentially** non-uniform clearance, which is closer to the question than the source that already narrowed the claim; that judgement rests on its title, because no abstract was retained.

Two extension themes failed honestly: deployable mechanisms and guards returned drone-application and ship-landing papers rather than mechanism repeatability or containment, and one guard query leg returned HTTP 429. Neither is presented as coverage. Citation counts could not be retrieved at all, because both APIs were rate-limiting during the run, so nothing is ranked by impact.

Nothing here closes SSY-01, and the binding constraint has changed: it is now **access rather than search coverage**. The top four items in the reading queue are paywalled or block automated retrieval and need the owner's institutional route. 111 qualifying records from the frozen set remain unscreened, 314 more sit outside its filter, and no patent search has been performed.

## 2026-09-21 — first-tier close reading narrows the claim; CAD tooling incorporated as planning only

Ledger row SSY-R07. [Reading records](reading-records-2026-09-21.json) · [prior-art boundary](prior-art.md) · [CAD plan](CAD_PLAN.md).

Six queued first-tier competitors were attempted. One was read in full and **it narrowed the claim**: a 2024 transonic-compressor study designs its schemes "to control the circumferential leakage area of the tip gap to be the same as that of uniform type", so the idea of holding an equivalent clearance measure fixed while redistributing the gap is already in the literature. The claim ledger now prohibits presenting the equal-mean comparison method as a contribution. The triage screen could not have found this, because only the full text reveals the constraint. What the source does not disclose is equally specific: its variation is axial along the chord, with no discrete circumferential seams, no duct, no small-UAV rotor and no measurement of any nonuniform geometry, so distinctiveness now rests on the seam geometry, the machine, and measurement rather than simulation.

Five ASME papers were not obtainable. The publisher route returns HTTP 403 behind a bot interstitial, which was not worked around; one is indexed as open access and the host still refused automated retrieval. Every axis for those five stays unresolved, because an abstract cannot establish what a full paper contains. An institutional subscription through a browser is the ordinary route and is available to the owner.

A cross-project CAD briefing was folded into [CAD_PLAN.md](CAD_PLAN.md) with the shared-tool revision pinned. **No CAD task is promoted**; all remain deferred behind SSY-01, SSY-02, SSY-03 and XC-02. Two integration points are now recorded: the equal-mean convention is a single decision (IN-08) governing both the geometry contract and the measurement system, because two independent choices would make "equal mean clearance" mean different things in the model and on the rig; and the geometric tolerance has a floor set by A0.1's finding that steady RANS carries 1.4 to 3.3 percent model-form error.

Not done: four first-tier competitors unread, the 111 qualifying unselected records unreviewed, S2 and S3 outstanding, and no patent search performed. The committed 2026-09-12 coverage record still reflects the day-1 source set; re-pointing the coverage script at the new reading file is a separate reviewed change and has not been made.

## 2026-09-20 — A0.1 validation: verdict NOT_VALIDATED, workflow verified against the reference

Ledger row SSY-R06. [Validation report](cfd-validation-a01.md) · [execution record](../evidence/task-a0-validation/README.md) · [uncertainty record](../results/generated/cfd/a0.1/uncertainty.json).

Two items recorded MISSING the day before were recovered from the same archive route: the full TMR grid family (refinement ratio exactly 2) and TMR's curated experimental data, whose header states the exact case condition. Experimental uncertainty moved from MISSING to 0.00441 in lift coefficient, derived from the three trip conditions in the dataset, and recorded as a lower bound because it captures trip repeatability and nothing else.

Spalart-Allmaras, three converged levels: apparent order 2.670, monotonic, asymptotic-range ratio 1.007, grid-convergence index 0.153 percent. Comparison error against the experiment is +0.023813, which is 5.04 times the validation uncertainty, so the verdict is **NOT_VALIDATED** at the band committed before any case ran. The same computation sits 0.38 percent below the published CFL3D result on the same grid family, and every published code misses this experiment in the same direction by 1.4 to 3.3 percent. The workflow is therefore verified against the field while the experiment comparison fails, and those are stated as two separate claims. The likeliest cause is that the band is too narrow; widening it after seeing the result is what the acceptance record forbids, so the verdict stands and the reason is recorded.

Carried forward for Study A: steady RANS on this canonical case carries 1.4 to 3.3 percent model-form error in lift and the turbulence model alone moves lift by about 1.2 percent, so a seam effect below roughly 2 percent cannot be separated from model-form error by this class of simulation, at any mesh density.

Not done: the k-omega SST arm is incomplete at two of three levels, its fine grid stopped by host memory exhaustion and retained as UNCONVERGED, so it carries no index and no verdict and the model-form sensitivity for this work is unmeasured. **A0.1 does not pass its gate as written, so A0.2 does not start**; the owner decides whether to re-derive the experimental uncertainty or restate the gate as code-to-code verification. Decision D10 on the A0.2 solver regime is still open. No prior-art close reading or patent search was performed in this session.

## 2026-09-19 — A0 validation ladder: entry tasks and source verification

Executed on `task/research-programme-a0` from the merged work order (PR #20), base `c12ee80`. Ledger row SSY-R05. [Execution record](../evidence/task-a0-validation/README.md).

Delivered: a pinned, digest-recorded solver container proven to run a steady incompressible RANS tutorial natively on ARM64 in 10 seconds; a [source inventory](../evidence/task-a0-validation/source-inventory.json) giving every A0.1 and A0.2 parameter an evidence label and a locator; a [frozen A0.1 acceptance record](../evidence/task-a0-validation/a01-acceptance.json) committed before any A0.1 solution exists; an [uncertainty decision record](specs/research-programme/uncertainty-decision-record.md) that supersedes the work order's D4; and a test that enforces CFD manifest identity, rejects a two-mesh grid-convergence claim, and pins the historical acquisition evidence by hash. 79 tests pass.

Four verification findings changed the plan. The **NASA TMR live site is gone** — every path redirects to a content-free landing page — so A0.1's specification was recovered from a dated archive snapshot and a fifth evidence label, `VERIFIED_FROM_ARCHIVE`, was added. The **TMR grid family is MISSING**, so a scripted grid must be generated and results will not be directly comparable to TMR's published per-grid CFD. The **A0.1 airfoil is a modified sharp-trailing-edge section**, not the standard NACA 0012 the earlier case file implied. And the **A0.2 baseline is not incompressible**: at 1250 rpm the tip Mach number is 0.437, implying roughly an 11% compressibility influence on outboard sectional pressure, which is physics rather than solver error and is now an open solver-regime decision instead of a hidden assumption.

Not done: no mesh exists, no A0 case has been solved, and nothing is validated. Study A remains blocked at its release gate. Open by role — **agent**: extract the Ladson and Gregory/O'Reilly comparison values, generate the scripted grid family, confirm the A0.2 rotor dimensions against figure 1, close the six-competitor close reading and the patent search; **owner**: decide D10 (A0.2 solver regime), and whether to raise the Docker VM allocation above 7.75 GiB or size the design to it. The clearance budget is untouched and remains `INPUTS_PENDING`.

Newest section first. Each dated section is the handoff written at that time; later sections supersede earlier claims but do not rewrite them.

## 2026-09-15 — top-25 candidate triage and measurement-requirements draft (work order 2026-09-14)

Executed on `task/day-2026-09-14` from the [merged plan](specs/day-2026-09-14/plan.md). Two bounded artifacts, both with their own test: the [triage record](candidate-screening-2026-09-14.json) with its [report and hand-off queues](prior-art-search-2026-09-14-screening.md) (25 dispositions: 22 include for close reading, 3 exclude off topic, 0 defer; rule frozen before reading; no novelty-axis state assigned), and the [measurement-requirements draft](measurement-system-spec.md) (12 channels, budget-register mapping, qualification procedures, open-input register IN-01 to IN-12). Ledger rows SSY-R03 and SSY-R04 are `done` for their artifacts only. [Evidence and command logs](../evidence/task-2026-09-14/README.md).

Not done, by responsible role: **owner** — IN-01 minimum clearance effect, IN-02 target mean clearance, IN-03 minimum power difference at matched thrust, IN-04 rotor/stand/sensor envelope, XC-02 disclosure path, SSY-S08; **agent** — close reading of the 22 includes with a new dated reading record, then novelty-axis reconciliation; a second frozen batch for the 111 qualifying unselected records; a dated patent search; derivation of channel limits once IN-01 and IN-03 exist; **metrology provider** — the five installed clearance contributors (SSY-12). Completed top-25 triage is not the unfinished scholarly review; a delivered requirements draft is not frozen requirements or physical qualification. Historical acquisitions, the day-3 reading records, the eligibility register and the budget CSV are unchanged.

## 2026-09-11 — SSY-D04 provenance-clean re-acquisition

The D02 provenance defect is corrected by one clean run of `rerun_search.py` from a
non-throttled network: 451 identifier records, 18/18 query legs ok,
**0** rows without a successful logged query (historical export: 50). Known D01 anchors
present: 3 of 3 comparable — a bounded overlap, not recall. 25 candidates, all UNSCREENED.
The 09-09 export and the day-3 acquisition ledger are unchanged; the new export is not merged into
either. No novelty, patent or owner gate is closed. [Evidence](../evidence/task-2026-09-11/README.md).

## Day-3 preparation — 2026-09-09

Six new ledger tests preserve acquisition routes, unavailable query mappings, zero-result semantics, unscreened status, all raw rows and deterministic regeneration. 21 tests and repository contract pass. All 499 raw rows retained; 50 provenance holes remain. Public JSASS PDF and a patent claim were accessed; other full-text and disclosure gates remain unresolved.

Review [DAY3_PLAN.md](DAY3_PLAN.md), [deliverable](day3-source-review.md), and [commands/evidence](../evidence/task-day3-2026-09-09/README.md). Base: `6ccb65c648318ca7f4f505452416813956a3ac06`; new PR branch: `task/day-three-20260909`. No original Owner/External gate is closed. Final source identity is the PR head, reported in its delivery record rather than embedded circularly here.

SSY-01 and XC-02 remain open; patent access is not legal clearance.

Read [the D02 integrity review](../evidence/task-2026-09-09-review/README.md)
before the historical handoff below. D02 is blocked on unexplained acquisition
provenance; original literal-ID overlap is not a valid recall estimate. The
rerun/audit software passes 15 tests plus contract checks. No new literature
screening or research validation is claimed.

# Segmented-Shroud-Yield — partial handoff, local software ready for review

## Latest follow-up — 2026-09-09

[SSY-D02 database export](../docs/prior-art-search-2026-09-09-database.md) adds a dated,
reproducible native-database search with a measured recall check (1/6 of the day-1 set
recovered — the two discovery routes diverge). Candidates are unscreened; no gate is closed.

## Follow-up — 2026-09-08

[SSY-D01 source-review handoff](../evidence/task-2026-09-08/README.md) adds a dated
first-pass research review. It does not close the full novelty or owner gates.
Original sprint evidence below is historical; no new experimental result exists.

Prepared 2026-09-05; resumed and checked 2026-09-06. Budget: six workload days,
30 focused hours per repository; estimates are not recorded time spent.

Canonical checkout: `/Users/redhose/Developer/research-sprints/2026-09-05/Segmented-Shroud-Yield`.
Remote: https://github.com/500ft/Segmented-Shroud-Yield.
Branch: `sprint/evidence-integrity-20260905`.
Base commit: `971eadb6b778c5fda764894235490dab2ad345e2`.
Final commit: this review packet's containing commit; its SHA is reported in the PR
because a commit cannot embed its own identity. No deployment, publication,
outreach or spending occurred. Original checkout/user changes were preserved.
Base includes the existing unmerged task PR #1 head; it is not origin/main.

[Roadmap](SPRINT_ROADMAP.md) · [Authoritative ledger](SPRINT_TASKS.csv) ·
[Progress](SPRINT_PROGRESS.md) · [Selected candidate hashes](../evidence/sprint-2026-09-05/candidate.json).

## Completed deliverables and evidence

The checker enforces specimen JSON Schema and finite values. Duct performance and protective-guard qualification now have independent evidence paths. Held-out-family predictions require descriptor support or explicitly specified physical extrapolation.

Implementation: [checker](../scripts/check_repo_contract.py), [tests](../tests/test_manifest_validation.py), [research plan](research-plan.md), [roadmap](../ROADMAP.md), [first experiment](experiment-01-rigid-defect-duct.md).

- [Baseline identity, commands and outputs](../evidence/sprint-2026-09-05/baseline.json).
- [Original failing evidence](../evidence/sprint-2026-09-05/manifest-red.json).
- [Implementation checks](../evidence/sprint-2026-09-05/implementation-green.json).
- [Final verification](../evidence/sprint-2026-09-05/final-checks.json).
- [Predeclared evaluation procedure](../evidence/sprint-2026-09-05/evaluation-plan.md),
  [retained replay](../evidence/sprint-2026-09-05/evaluate_candidate.py),
  [actual outputs](../evidence/sprint-2026-09-05/evaluation.json).

- [Consumer delivery evidence](../evidence/sprint-2026-09-05/consumer.json).

7 tests passed in development and clean consumer environments; repository contract passed; 7/7 additional metadata cases matched.

Design and intake only; no CAD, rotor test, trained response model or protective qualification. Null planned measurements remain valid metadata, not observed values.

## Reproduce

Run from the canonical checkout using the recorded Python3.11 environment and
repository dependencies. The local pytest workaround stubs readline before import;
it is not a skipped test or changed product requirement.

```sh
python -m unittest discover -s tests -v
python scripts/check_repo_contract.py
python evidence/sprint-2026-09-05/evaluate_candidate.py
git diff --check
```



Delivery route: a clean temporary venv installed pinned jsonschema4.26.0 and executed absolute checker/test paths from /private/tmp. Resolved transitive versions are retained in consumer.json. The checker uses the schema-declared dialect via validator_for; [official validation API](https://python-jsonschema.readthedocs.io/en/stable/validate/) is the interface reference.

No separate configured lint/typecheck is claimed. Syntax checks are compilation,
not static typing. Saved output truncation, if present, is indicated by the tool
result metadata; no omitted output is called a full log.

## Evaluation meaning and remaining work

Selected implementation/protocol hashes and expectations were saved before the
additional cases ran. Existing tests, reviewed fixtures and reviewer-discovered
bugs are development material. All additional cases were retained. These small
developer-selected checks establish behavior on those inputs, not independent
scientific validation or general accuracy. Another agent is not a human reviewer.
External feedback: pending.

1. Owner chooses rotor/stand/metrology access and closes the exact-gap prior-art task.
2. Define and qualify the rigid-defect apparatus before studying a folding mechanism.
3. Guard protection requires its own approved tests; aerodynamic failure does not confer a fallback success.

Next action: Owner resource choice, then long-term SSY-01 exact-gap closeout and rigid-defect metrology/CAD work order.

Evidence-supported portfolio bullet: “Built schema-checked specimen intake and an identifiable defect-study plan separating aerodynamic yield from unproven protective performance.”
This concerns engineering quality, not adoption or measured scientific performance.

## Ready-to-send review request

“Review Segmented-Shroud-Yield against docs/SPRINT_ROADMAP.md. Repository: /Users/redhose/Developer/research-sprints/2026-09-05/Segmented-Shroud-Yield. Base commit: 971eadb6b778c5fda764894235490dab2ad345e2. Final commit: PR head (see GitHub PR). Review index: docs/REVIEW_READY.md. Incomplete work: Owner chooses rotor/stand/metrology access and closes the exact-gap prior-art task. Define and qualify the rigid-defect apparatus before studying a folding mechanism. Guard protection requires its own approved tests; aerodynamic failure does not confer a fallback success. Reproduce the changed behaviors and counterexamples, rerun appropriate checks, and assess the code and evidence independently. Review first; make further changes only if requested.”
