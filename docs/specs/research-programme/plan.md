# Work order — Study A0 entry and the systematic prior-art closeout

Status: proposed, for owner review; build starts only from the merged revision, on `task/research-programme-a0`. Date: 2026-09-16. Design: [proposal.md](proposal.md); tiers: [scope.md](scope.md). Status of research tasks lives only in the [sprint ledger](../../SPRINT_TASKS.csv); checkboxes here track implementation.

## Decisions to confirm or change before the build

- **D1. CFD toolchain.** Default: OpenFOAM (current ESI release) in its official arm64 container via Docker; SU2 only if the container route fails. Reason: free, scriptable, MRF and AMI both available, no licence. Alternative: a licensed solver you have access to at NYU; say which.
- **D2. A0 baseline dataset.** Default order: S1 Ryu 2017 → Akturk–Camci ducted fan → open rotor geometry with deferred validation. The first two tasks below check whether either publishes usable blade geometry; if neither does, the default falls to the third and every CFD number carries "unvalidated" until Study C.
- **D3. Study A rotor.** Default: the same rotor as A0, so validation transfers. Changing scale or rotor for A breaks that transfer and is recorded as a decision.
- **D4. Uncertainty band.** Default: U = √(GCI² + clocking² + model²) with GCI from three meshes (ratio ≥ 1.3, Fs = 1.25), clocking from four rotor positions, model from k-ω SST vs Spalart–Allmaras on the extreme cases.
- **D5. Equal-mean rule in CFD.** Default: post-process every case under both the wall-only rule and the fixed-grid-with-occlusion rule; report agreement; decide IN-08 from the result.
- **D6. Compute location.** Default: this laptop; cluster/cloud only when A0's timings trigger it (scope.md).
- **D7. Case records.** Default: one folder per case under `results/generated/cfd/<study>/<case>/` with a JSON manifest (geometry revision, mesh hash, solver version, settings, commit) and the raw case files kept out of git if larger than a stated size; no new schema tooling until more than three cases exist.
- **D8. Prior-art closeout lane.** Default: runs in parallel with A0; close reading writes a **new** dated reading record and never edits `docs/day3-reading-records.json`; the coverage script is re-pointed to a new dated evidence folder only in a separate, reviewed change.

## Owner inputs this work order prepares but cannot make
IN-01, IN-02, IN-03 (decisions after Study A), IN-04 (resources), IN-07 (XC-02). Each stays `pending` until an `owner_decision` row exists.

## Tasks

### [ ] T00 — Baseline and toolchain check
- Files: `evidence/task-a0-validation/README.md` (new).
- Do: run the repository gate; record interpreter, commit, hardware (cores, memory); pull the OpenFOAM arm64 container and run its tutorial cavity case; record versions and wall time.
- Done when: gate exit codes logged; the container solves the tutorial; versions recorded. Failure to run the container stops T04 and triggers the SU2 alternative in D1.

### [ ] T01 — Geometry availability, S1 Ryu 2017
- Files: evidence README (modify).
- Do: from the full text already on file (hash in the day-3 records), list what geometry is published: duct profile, rotor diameter, blade count, chord/twist/airfoil per radius, hub, clearance, operating points, measured quantities with uncertainties. Record page/figure locators.
- Done when: a table states for each item published / derivable / absent. Do not digitise figures yet.

### [ ] T02 — Geometry availability, Akturk–Camci
- Files: evidence README (modify).
- Do: same table for `doi:10.1115/1.4023468` and its Part II, through open routes only (two attempts max per identifier, recorded); this also counts as the close reading of those two includes, recorded in the new reading record of T10.
- Done when: the table exists, or the access failure is recorded with routes and dates.

### [ ] T03 — Choose the A0 baseline (owner confirms)
- Files: `docs/specs/research-programme/plan.md` D2 (modify).
- Depends on: T01, T02.
- Do: rank the candidates by geometry completeness and measured-data quality; record the choice and what remains to be derived or assumed, each assumption labelled conservative or optimistic.
- Done when: D2 names one dataset and the assumption list is in the evidence README.

### [ ] T04 — Geometry and mesh template
- Files: `results/generated/cfd/a0/geometry/` (new; scripts and small inputs only), case manifest per D7.
- Depends on: T00, T03.
- Do: build the rotor and duct with a scripted generator (gmsh or OpenFOAM utilities) from the published parameters; three meshes at ratio ≥ 1.3; record y⁺ target, cells across the tip gap (≥ 10 on the finest), total cells and peak memory.
- Done when: all three meshes pass `checkMesh` and the finest fits in memory with the solver loaded; numbers recorded. If the finest does not fit, record the scale or gap-ratio change as a decision before proceeding.

### [ ] T05 — Steady baseline runs and iterative convergence
- Files: case folders and manifests.
- Depends on: T04.
- Do: MRF steady runs on the three meshes at the published operating point; monitor thrust, torque and residuals; stop on plateau per a stated rule.
- Done when: each case's convergence history and wall time are in its manifest; no case is reported from an unconverged state.

### [ ] T06 — Grid-convergence and model uncertainty
- Files: `results/generated/cfd/a0/uncertainty.md` (new) and the numbers in a small JSON.
- Depends on: T05.
- Do: observed order, Richardson estimate and GCI on thrust and torque; rerun the finest mesh with the second turbulence model; tabulate.
- Done when: GCI and model difference are reported with the formulas used; the A0 success/kill criterion is evaluated and stated.

### [ ] T07 — Validation comparison
- Files: `docs/cfd-validation-a0.md` (new).
- Depends on: T06.
- Do: compare thrust (and torque/power if published) with the measured value and its uncertainty; compare the clearance-sensitivity sign and magnitude with the published sweep; state the verdict against §4 A0 of the proposal; state every assumption made where geometry was absent.
- Done when: the document gives the verdict in one sentence with the numbers, and the claim-ledger vocabulary is respected (this is CFD evidence under stated assumptions).

### [ ] T08 — One check for CFD records
- Files: `tests/test_cfd_records.py` (new).
- Depends on: T06.
- Do: one test that every case manifest under `results/generated/cfd/` names geometry revision, mesh hash, solver version and commit, and that any reported effect or validation number cites a GCI computed from at least three meshes. Negative controls: a manifest missing a field; a result citing a two-mesh GCI.
- Done when: the test discovers, passes on the A0 records, and rejects both controls.

### [ ] T09 — Preregister Study A
- Files: `docs/specs/research-programme/study-a-preregistration.md` (new).
- Depends on: T07 (verdict positive).
- Do: fix the screening design (factor levels, run list), the matched-thrust procedure, the uncertainty band, both averaging rules, the held-out configuration, and the kill criterion; commit before any variant geometry is generated.
- Done when: the file exists in a commit that predates every Study A case manifest; A's evidence README cites that commit.

### [ ] T10 — Close reading, first tier of the triage queue
- Files: `docs/reading-records-2026-09-16.json` (new), `docs/prior-art-search-2026-09-14-screening.md` (queue status, modify).
- Independent lane: may run while CFD cases compute.
- Do: read the six "likely direct competitor" includes under the day-3 rubric; record locator, aboutness, evidence grade and per-axis `axis_states` in the new file only.
- Done when: six records exist with locators; no edit to the day-3 file; the queue marks them read.

### [ ] T11 — Dated patent search, scoped
- Files: `docs/patent-search-2026-09-16.md` (new).
- Independent lane.
- Do: search strings and classifications fixed before searching; public routes only, each route and date recorded; record hits as UNSCREENED candidates with identifiers; no legal conclusion.
- Done when: the document lists routes attempted with outcomes, the frozen strings, and the candidate list; prior-art.md gets a dated one-paragraph link.

### [ ] T12 — Ledger and handoff
- Files: `docs/SPRINT_TASKS.csv`, `docs/SPRINT_PROGRESS.md`, `docs/REVIEW_READY.md`, `docs/TASKS.md` (modify).
- Depends on: T07, T10, T11 (whichever are complete at the checkpoint).
- Do: add rows for A0 (done or killed, with the verdict), the reading batch and the patent search; state residuals per role.
- Done when: CSV parses, ids unique, the contract check passes, and no prior row is reclassified.

### [ ] T13 — Integration and PR
- Depends on: T12.
- Do: full gate plus the new test; preservation diff against base for historical files; one PR against `main`; CI on the exact head; keep unmerged unless instructed.

## Traceability
| Requirement | Tasks | Remaining gate |
| --- | --- | --- |
| CFD evidence only under stated assumptions (claim ledger) | T03, T06, T07 | validation verdict |
| No seam prediction before validation (proposal §3) | T07 → T09 ordering | A0 pass |
| Preregistration before variants | T09 | commit order |
| MEI is an owner decision informed by CFD | Study B, not in this order | owner rows |
| Novelty table leaves "bounded" only with reads and searches | T10, T11 | S2/S3, 111 records, second batch |
| Disclosure boundary | D2/D3 generic geometry; no mechanism | XC-02 |
