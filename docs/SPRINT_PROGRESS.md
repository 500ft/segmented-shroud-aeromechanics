# Sprint progress

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

Newest section first; historical entries keep their original dates and wording.

## 2026-09-15 — top-25 candidate triage and measurement-requirements draft (work order 2026-09-14)

Executed on `task/day-2026-09-14` from the [merged plan](specs/day-2026-09-14/plan.md). Two bounded artifacts, both with their own test: the [triage record](candidate-screening-2026-09-14.json) with its [report and hand-off queues](prior-art-search-2026-09-14-screening.md) (25 dispositions: 22 include for close reading, 3 exclude off topic, 0 defer; rule frozen before reading; no novelty-axis state assigned), and the [measurement-requirements draft](measurement-system-spec.md) (12 channels, budget-register mapping, qualification procedures, open-input register IN-01 to IN-12). Ledger rows SSY-R03 and SSY-R04 are `done` for their artifacts only. [Evidence and command logs](../evidence/task-2026-09-14/README.md).

Not done, by responsible role: **owner** — IN-01 minimum clearance effect, IN-02 target mean clearance, IN-03 minimum power difference at matched thrust, IN-04 rotor/stand/sensor envelope, XC-02 disclosure path, SSY-S08; **agent** — close reading of the 22 includes with a new dated reading record, then novelty-axis reconciliation; a second frozen batch for the 111 qualifying unselected records; a dated patent search; derivation of channel limits once IN-01 and IN-03 exist; **metrology provider** — the five installed clearance contributors (SSY-12). Completed top-25 triage is not the unfinished scholarly review; a delivered requirements draft is not frozen requirements or physical qualification. Historical acquisitions, the day-3 reading records, the eligibility register and the budget CSV are unchanged.

## 2026-09-11 — evidence-gap correction

The [current correction](ACQUISITION_CORRECTION_2026-09-11.md) supersedes any interpretation that earlier preparation closed a physical, approval, or source-review gate. Work is on `fix/evidence-gaps-20260911` from current renamed main; historical entries below retain their original dates and PR snapshots. The original day-3 and presentation PRs are now merged, but this correction is a new reviewable change, not an asserted merge or publication.

Each omitted or incomplete recommendation is accounted for separately in the current correction and existing task ledgers. No owner signature, measurement, PI conversation, imagery judgment, disclosure approval or independent review was fabricated. Exact tests, scope and next inputs are linked from the correction record; actual delivery state is established by its PR.

## 2026-09-11 — SSY-D04 provenance-clean re-acquisition

The D02 provenance defect is corrected by one clean run of `rerun_search.py` from a
non-throttled network: 451 identifier records, 18/18 query legs ok,
**0** rows without a successful logged query (historical export: 50). Known D01 anchors
present: 3 of 3 comparable — a bounded overlap, not recall. 25 candidates, all UNSCREENED.
The 09-09 export and the day-3 acquisition ledger are unchanged; the new export is not merged into
either. No novelty, patent or owner gate is closed. [Evidence](../evidence/task-2026-09-11/README.md).

## Day-3 work — 2026-09-09

Delivery update: the preparation was committed as 500ft and pushed; [day-3 PR](https://github.com/500ft/Segmented-Shroud-Yield/pull/5) is open against main. Initial implementation source: `e5e69c002f71b3ea088da90a1e2205c8d1ee4314` (later review/documentation commits are visible in the PR). This supersedes the pre-push stopping state below. Original day-1/day-2 PRs are merged; this new PR is not merged. Resume from the named unresolved project gates in [DAY3_PLAN.md](DAY3_PLAN.md), not from the already completed push step.

Both reviewed PR layers merged into main; new work starts from `6ccb65c648318ca7f4f505452416813956a3ac06` on `task/day-three-20260909`. Six new ledger tests preserve acquisition routes, unavailable query mappings, zero-result semantics, unscreened status, all raw rows and deterministic regeneration. 21 tests and repository contract pass. All 499 raw rows retained; 50 provenance holes remain. Public JSASS PDF and a patent claim were accessed; other full-text and disclosure gates remain unresolved.

The [evidence record](../evidence/task-day3-2026-09-09/README.md) contains checks and limits. Work is locally verified and not yet recorded here as pushed/merged. Current edits belong to this task; original checkouts were preserved. Next: finish verification, commit the bounded change and open the new PR; preserve all stated external gates.

D02 is now blocked, not accepted as a complete acquisition. The retained export
contains unexplained query provenance; no recall or route-divergence conclusion
is established. Added offline audit and safe new-output rerun with explicit
missing-credential/error states. Fifteen tests and the repository contract pass.
[Review evidence](../evidence/task-2026-09-09-review/README.md). No raw exports,
owner gates, screening verdicts, novelty clearance or disclosure path were changed.

# Sprint progress — Segmented-Shroud-Yield

## 2026-09-09 — SSY-D02 native-database export

Ran the database leg that D01 named as the next step (Crossref, OpenAlex, arXiv APIs; no patent
database reachable). [Export and recall check](prior-art-search-2026-09-09-database.md): 499 unique
records with per-query provenance; **1 of 6** day-1 identifiers recovered, which is the finding —
native-database ranking and web-index discovery surface different populations here, so neither set
can be assumed to contain the other. arXiv's search API throttled most queries; that leg is recorded
as incomplete. 25 new candidates are listed **unscreened**. No novelty, patent or owner gate is
closed. [Verification](../evidence/task-2026-09-09/README.md). Branch `task/priority-two-20260909`.

## 2026-09-08 — SSY-D01 first-pass source review

Completed the bounded priority-one source-review subtask, not the full novelty
gate. [Report](prior-art-search-2026-09-08.md) and
[verification](../evidence/task-2026-09-08/README.md). Base `dddd4f107de978319bb3f41bfeebbe927d36ab91`,
branch `task/priority-one-20260908`; isolated daily worktree. No apparatus,
measurement, publication, outreach or disclosure approval. Original sprint rows
preserved. Next: resolve report-listed full-text/search limitations; checks:
`python scripts/check_repo_contract.py`. PR records committed/pushed identity.

## 2026-09-06 — Main-branch placement authorized

Owner explicitly requested these PRs be merged to their respective main branches. This supersedes earlier placement-blocked/draft-only entries for the current changes. The combined main-targeted PR retains prerequisite integrity work, unchanged task ledgers and all actual hardware/disclosure gates. No CAD or experiment is marked complete. Merge completion and resulting main commit are verified by GitHub rather than asserted in advance here.

## 2026-09-06 — Reviewer-driven CAD amendment

This entry supersedes the earlier CAD allocation and readiness wording. The same CAD PR is now draft, pending the owner planning-ledger placement decision. [Review disposition](CAD_REVIEW_DISPOSITION.md) records that block; [CAD_PLAN.md](CAD_PLAN.md) and [CAD_TASKS.csv](CAD_TASKS.csv) contain revised priorities, separate tooling estimates and explicit parked work. No CAD model or new measurement was produced. Original integrity-sprint tasks/evidence remain unchanged. Next work is limited to active input-register tasks and unresolved owner decisions, not the parked portfolio-wide CAD program.

## 2026-09-06 — CAD task amendment

Added [individual CAD work orders](CAD_PLAN.md) and [CAD_TASKS.csv](CAD_TASKS.csv), separating component modeling, fixtures, inspection and release deliverables. This is planning only: no CAD or physical task is complete. The original sprint ledger and evidence are unchanged. CAD branch: `plan/cad-tasks-20260906`; the PR supplies the committed source identity. Next CAD action: the first input-register task in the CAD ledger; owner-gated successors remain blocked. Verification of this amendment is recorded in [CAD_PLAN_CHECKS.md](CAD_PLAN_CHECKS.md).

## 2026-09-06 — Partial handoff

- Sprint start2026-09-05; canonical checkout `/Users/redhose/Developer/research-sprints/2026-09-05/Segmented-Shroud-Yield`.
- Branch `sprint/evidence-integrity-20260905`; HEAD/base `971eadb6b778c5fda764894235490dab2ad345e2`.
- Seven Agent tasks done with linked evidence; SSY-S08 blocked on: Rotor/stand selection, metrology access, fabrication and facility safety authority. No specimens are available in the baseline. Branch includes unmerged PR work.
- 7 tests passed in development and clean consumer environments; repository contract passed; 7/7 additional metadata cases matched.
- [Final checks](../evidence/sprint-2026-09-05/final-checks.json), [candidate](../evidence/sprint-2026-09-05/candidate.json), [original expectations](../evidence/sprint-2026-09-05/evaluation-plan.md), [outcomes](../evidence/sprint-2026-09-05/evaluation.json).
- These are developer software checks; no physical/new scientific results. Catan's real-data arm, where applicable, stays blocked despite its software fallback evaluation.
- Handoff was prepared before commit; the PR records the final commit and push. Original user changes remain untouched.
- Next verification command: `python evidence/sprint-2026-09-05/evaluate_candidate.py`.
- Exact next task: Owner resource choice, then long-term SSY-01 exact-gap closeout and rigid-defect metrology/CAD work order.
- One-time ID disambiguation: sprint SSY-01…08 became SSY-S01…S08 to avoid collisions with the unchanged long-term backlog. Only this CSV holds sprint statuses.
- Owner action moved to Day1 (2h); Day1 now7h, Day6 now2h, total30h. External turnaround is not accelerated.

## Baseline and interrupted execution

Baseline commands, outputs and identity remain in [evidence](../evidence/sprint-2026-09-05/baseline.json). Plans were saved before behavior changes. Runtime-limit pauses were followed by resuming the existing worktree; no baseline or external reply was invented. Original failing cases and corrected behavior are linked in [REVIEW_READY.md](REVIEW_READY.md).
