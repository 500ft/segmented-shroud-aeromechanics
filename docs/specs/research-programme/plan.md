# Work order — Study A0 validation ladder and Study A preregistration

Status: proposed, for owner review; build starts only from the merged revision, on `task/research-programme-a0`. Date: 2026-09-16, revised the same day after the owner's baseline decision. Design: [proposal.md](proposal.md); tiers: [scope.md](scope.md); case definitions: [a0-validation-cases.md](a0-validation-cases.md). Status of research tasks lives only in the [sprint ledger](../../SPRINT_TASKS.csv); checkboxes here track implementation.

Owner decisions taken 2026-09-16: the validation baseline is a standard aircraft wing (A0.1 airfoil, A0.2 wing-section rotor); the budget-feed study is out of this work order and is not touched.

## Decisions to confirm or change before the build

- **D1. CFD toolchain.** Default: OpenFOAM, current ESI release, official arm64 container via Docker. Alternative: a licensed solver available at NYU; name it and T00 changes.
- **D2a. Evidence labels.** The four labels the handoff defined are extended by a fifth, `VERIFIED_FROM_ARCHIVE`, for a value read from a timestamped Internet Archive snapshot because the authoritative live page no longer serves it. It ranks below `VERIFIED_FROM_SOURCE` because the snapshot may not match whatever is now authoritative. Introduced because the entire NASA TMR domain now redirects to a content-free landing page.
- **D2. Validation ladder.** A0.1 NACA 0012 2D (NASA TMR case and grids) → A0.2 Caradonna–Tung hover rotor (NASA TM 81232) → A0.3 ducted fan, deferred until a source with usable geometry is confirmed. Study A may start after A0.2 with the label "rotor-validated, gap-unvalidated".
- **D3. Study A rotor and scale.** Default (owner rule 2026-09-16: take the most-used baseline so there is the most published data to compare against): the Caradonna–Tung rotor **unchanged**, two untwisted NACA 0012 blades, radius 1.143 m, chord 0.1905 m, collective 8°, 1250 rpm, inside a generic duct. It is the most widely reproduced hover-rotor validation case, so every open-rotor quantity in Study A has published CFD and measured comparators. Cost: its chord Reynolds number is well above a small UAV's; scale transfer is a separate, later study, and the Reynolds number is reported on every case. Alternative if a small-scale comparator is wanted later: a propeller from the UIUC propeller database, which has the most public small-rotor performance data but not fully public blade geometry.
- **D4. Uncertainty band. SUPERSEDED 2026-09-19** by the [uncertainty decision record](uncertainty-decision-record.md). The single band `U = √(GCI² + clocking² + model²)` is withdrawn: a grid-convergence index is an uncertainty, while turbulence-model spread and rotor clocking spread are deterministic sensitivities with no distribution, so adding all three in quadrature and calling the result a confidence interval overstates what is known. Two bands replace it — `U_val = √(U_num² + U_input² + U_D²)` for comparison against measured data, and a linear worst-case envelope `E_dec = U_num(Δ) + R_clock + R_model` for Study A decisions, where no data exist.
- **D5. Equal-mean rule in CFD.** Post-process every Study A case under both admissible averaging rules (wall-only; fixed grid with occlusion) and report agreement.
- **D6. Compute.** This laptop (10 cores, 16 GiB host) — but the **Docker VM is allocated 7.75 GiB**, measured 2026-09-19, and that is the real ceiling for meshing. Cluster or cloud only when A0.2 timings or memory trigger it.
- **D7. Case records.** One folder per case under `results/generated/cfd/<study>/<case>/` with a JSON manifest (source revision, mesh hash, solver version, settings, commit); raw case data outside git above a stated size; one test, no schema tooling.
- **D8. Solver regime.** Incompressible for A0.1 at M 0.15 and for A0.2 at the subsonic-tip condition; the transonic A0.2 condition is out of scope. Compressibility neglect recorded as an assumption on every case. **Amended 2026-09-19:** the A0.2 baseline is not actually incompressible (Mtip 0.437); see D10.
- **D9. Acceptance rule.** Default (same owner rule): the most-used validation procedure, not project-specific percentages. Pass rule per ASME V&V 20: comparison error E = S − D (simulation minus data) is compared with the validation uncertainty U_val = √(U_num² + U_input² + U_D²); the case is validated at the U_val level when |E| ≤ U_val, and the size of U_val is itself reported. Numerical uncertainty U_num by the three-grid GCI procedure of Celik et al. (ASME J. Fluids Eng. 2008), Fs = 1.25, refinement ratio ≥ 1.3, the most-cited grid-convergence method. Experimental uncertainty U_D from the source of record where given. The published experiment-to-CFD spread for each case (the TMR's own model comparisons for A0.1; the many Caradonna–Tung CFD reproductions for A0.2) is recorded alongside as the reporting context, so the reader sees where this toolchain sits in the field, and it is not the pass rule. Percentages appear only as reported numbers.
- **D10. A0.2 solver regime — OPEN, decide before A0.2 meshing.** Source verification established that the 1250 rpm baseline sits at **Mtip = 0.437**, not an incompressible condition, implying roughly an 11% compressibility influence on outboard sectional Cp. Options: (a) a compressible solver for A0.2, more setup but no bias; (b) incompressible, gate only on integrated thrust coefficient, and report sectional Cp with a declared per-station compressibility bias; (c) incompressible, comparing Cp only at inboard stations. Default **(b)**, because thrust is the quantity Study A depends on and the bias is then stated rather than hidden. Open because it determines the A0.2 acceptance file, which cannot be frozen until it is settled.
- **D11. Repository data policy for CFD artefacts.** Committed: case *inputs* (dictionaries, boundary conditions, generator scripts), JSON manifests, uncertainty JSONs, extracted result tables, and solver log tails with their hashes. Not committed: mesh files, time directories, reconstructed fields, retrieved source PDFs and archive HTML. Uncommitted artefacts live under `results/generated/cfd/.local/` (git-ignored) and every manifest records their path, SHA-256 and regeneration command. Any single committed file above 1 MB needs explicit justification in its pull request. Sources are referenced by URL plus hash, never vendored.

## Tasks

T00–T18 are ordered work units, one concern each. Retrieval, container pulls and solver wall time are not inside the 2–5 minute estimates. Record actual progress; do not promise calendar completion.

### [x] T00 — Baseline, toolchain, container — **done 2026-09-19**
- Files: `evidence/task-a0-validation/README.md` (new).
- Do: run the repository gate and log exit codes; record interpreter, commit, cores, memory; pull the OpenFOAM arm64 container; run its lid-driven-cavity tutorial; record image digest, solver version, wall time.
- Done when: gate logged; tutorial solves; versions recorded. A container failure stops T04 and switches D1 to the alternative.

### [x] T01 — Transcribe A0.1 from the source of record — **done 2026-09-19**
- Files: `docs/specs/research-programme/a0-validation-cases.md` (modify, "verified" column).
- Do: open the NASA TMR NACA 0012 case page through a public route; verify Mach, Reynolds number, angles, reference data source, grid family; fill the verified column with locators; record any difference from the nominal values.
- Done when: every A0.1 row has a verified value and locator, or a recorded reason it could not be verified.

### [x] T02 — Transcribe A0.2 from NASA TM 81232 — **done 2026-09-19, PASS**
- Files: case definitions (modify).
- Do: same for the Caradonna–Tung rotor: blade count, section, radius, chord, collective, speeds, measured stations and quantities; note the report's own stated uncertainties if given.
- Done when: every A0.2 row verified with page or figure locators.

### [x] T03 — Freeze acceptance bands before any run — **done 2026-09-19, frozen**
- Files: case definitions (modify, §2 and §3 acceptance); evidence README.
- Depends on: T01, T02.
- Do: for each gated quantity, set the band from the published experiment-to-CFD spread (TMR's published model comparisons for A0.1; literature CFD of the Caradonna–Tung rotor for A0.2), or the D9 default when no spread is found; commit.
- Done when: bands are in a commit that predates every case manifest; the evidence README cites that commit.

### [ ] T04 — A0.1 grids
- Files: `results/generated/cfd/a0-1/` case folders and manifests (new).
- Depends on: T00, T03.
- Do: obtain three TMR grid levels and convert to the solver's format, or generate an equivalent C-grid family with a scripted generator; run the solver's mesh check; record cells, y⁺ target, refinement ratio.
- Done when: three grids pass the mesh check with ratio ≥ 1.3 and manifests exist.

### [ ] T05 — A0.1 runs
- Files: case folders and manifests.
- Depends on: T04.
- Do: steady incompressible runs at the three angles on all three grids with Spalart–Allmaras; repeat the finest grid with k-ω SST; monitor lift, drag and residuals; stop on a stated plateau rule.
- Done when: every case has a convergence history and wall time in its manifest; no unconverged case is reported.

### [ ] T06 — A0.1 uncertainty and verdict
- Files: `docs/cfd-validation-a0.md` (new, section A0.1); `results/generated/cfd/a0-1/uncertainty.json`.
- Depends on: T05.
- Do: observed order, Richardson estimate, GCI on lift and drag; model difference; comparison with experiment and with TMR's published CFD; verdict against T03's bands in one sentence with the numbers.
- Done when: the verdict is stated; every assumption (incompressible, transition-free, far-field distance) is listed as conservative or optimistic.

### [ ] T07 — Check for CFD case records
- Files: `tests/test_cfd_records.py` (new).
- Depends on: T06.
- Do: one test: every manifest under `results/generated/cfd/` names source revision, mesh hash, solver version and commit; every validation or effect number in the JSON cites a GCI from at least three grids. Negative controls: a manifest missing a field; a result citing a two-grid GCI.
- Done when: the test discovers, passes on A0.1 records, rejects both controls.

### [ ] T08 — A0.2 geometry and periodic domain
- Files: `results/generated/cfd/a0-2/geometry/` (scripted generator and small inputs), manifests.
- Depends on: T02, T03, T06 (A0.1 verdict positive).
- Do: generate the blade from the verified section and planform; build a single-blade 180° periodic hover domain in a rotating frame; three mesh levels; record far-field distance, boundary treatment, cells, y⁺, peak memory.
- Done when: three meshes pass the mesh check and the finest fits in memory; assumptions recorded. If it does not fit, record the domain or resolution change as a decision before running.

### [ ] T09 — A0.2 runs
- Files: case folders and manifests.
- Depends on: T08.
- Do: steady MRF runs at the subsonic-tip condition on three meshes with Spalart–Allmaras; finest mesh with k-ω SST; monitor thrust, torque, residuals.
- Done when: convergence histories and wall times recorded; peak memory recorded (feeds D6).

### [ ] T10 — A0.2 uncertainty and verdict
- Files: `docs/cfd-validation-a0.md` (section A0.2); `results/generated/cfd/a0-2/uncertainty.json`.
- Depends on: T09.
- Do: GCI on thrust; model difference; thrust coefficient against measured; sectional pressure at three stations with RMS error each; verdict in one sentence with numbers.
- Done when: verdict stated; the claim boundary of the case definitions §4 is repeated verbatim under it.

### [ ] T11 — Ladder statement and Study A labels
- Files: `docs/cfd-validation-a0.md` (closing section).
- Depends on: T10.
- Do: state which rungs passed, what is validated and what is not, and the exact label every Study A result must carry ("rotor-validated, gap-unvalidated" until A0.3).
- Done when: a reader can quote the label and its reason in one sentence.

### [ ] T12 — Preregister Study A
- Files: `docs/specs/research-programme/study-a-preregistration.md` (new).
- Depends on: T11 (A0.2 passed).
- Do: fix the rotor per D3 with its provisional scale, the duct profile, the seam parameterisation (n, g, s only; no joint geometry), the screening design and run list, the matched-thrust procedure, the uncertainty band, both averaging rules, the held-out configuration, and the kill criterion; commit before any variant geometry is generated.
- Done when: the file exists in a commit that predates every Study A case manifest.

### [ ] T13 — Close reading, first tier of the triage queue
- Files: `docs/reading-records-2026-09-16.json` (new); triage report queue status (modify).
- Independent lane: runs while solvers run.
- Do: read the six "likely direct competitor" includes under the day-3 rubric; record locator, aboutness, evidence grade and `axis_states` in the new file only; never edit the day-3 file.
- Done when: six records with locators exist; the queue marks them read.

### [ ] T14 — Dated patent search, scoped
- Files: `docs/patent-search-2026-09-16.md` (new).
- Independent lane.
- Do: freeze search strings and classifications before searching; public routes only, each route and date recorded; hits recorded as UNSCREENED candidates; no legal conclusion.
- Done when: routes, outcomes, frozen strings and candidates are listed; `prior-art.md` gets a dated one-paragraph link.

### [ ] T15 — Ledger and handoff
- Files: `docs/SPRINT_TASKS.csv`, `docs/SPRINT_PROGRESS.md`, `docs/REVIEW_READY.md`, `docs/TASKS.md`, `ROADMAP.md` (modify).
- Depends on: T11, T13, T14 (whichever are complete at the checkpoint).
- Do: rows for A0.1, A0.2 (done, killed, or in progress with the verdict), the reading batch and the patent search; residuals per role; the claim ledger's "FEA/CFD" vocabulary used for every CFD statement.
- Done when: CSV parses, ids unique, contract check passes, no prior row reclassified.

### [ ] T16 — Integration and PR
- Depends on: T15.
- Do: full gate plus the new test; preservation diff for historical files; one PR against `main`; CI on the exact head; unmerged unless instructed.

## Out of this work order
Study B (budget feed) and every owner input to the budget; A0.3 until a ducted-fan geometry source is confirmed; any Study A variant run before T12 is committed; acoustics; CAD; mechanism detail.

## Traceability
| Requirement | Tasks | Remaining gate |
| --- | --- | --- |
| CFD evidence only under stated assumptions (claim ledger) | T03, T06, T10, T11 | ladder verdicts |
| Validation before any seam prediction (proposal §3) | T06 → T08 → T10 → T12 ordering | A0.2 pass |
| Public geometry and data for every validation case | D2, T01, T02 | A0.3 source |
| Acceptance fixed before running | T03 commit order | — |
| Preregistration before variants | T12 commit order | — |
| Uncertainty band includes clocking and model terms | D4, T12 | — |
| Novelty table leaves "bounded" only with reads and searches | T13, T14 | S2/S3, 111 records |
| Disclosure boundary | D3 generic geometry; no joint detail | XC-02 |
