# Review index

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
