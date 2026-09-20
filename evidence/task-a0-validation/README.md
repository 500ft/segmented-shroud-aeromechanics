# A0 validation ladder — execution record

Work order: [plan.md](../../docs/specs/research-programme/plan.md) as merged in PR #20.
Base commit: `c12ee809bd283fdb94e98aaafd58d644cd039126` (main after PR #20 merged). Branch: `task/research-programme-a0`.
Executed: 2026-09-19. Scope of this record: work-order tasks **T00, T01, T02, T03**. No mesh has been generated and no A0 case has been solved.

Nothing here is a validation result. This record establishes what the toolchain is, what the sources say, and what A0.1 will be judged against, all fixed before any solution exists.

## T00 — baseline and environment

| item | value |
| --- | --- |
| interpreter | `/Users/redhose/ENTER/bin/python`, Python 3.11.8 |
| jsonschema | 4.26.0 |
| host | Apple M1 Pro, 10 cores, 16 GiB, macOS 14.7.3 |
| Docker | 29.5.3, VM memory 7.75 GiB |
| base commit | `c12ee809bd283fdb94e98aaafd58d644cd039126` |

All repository gates run from the base commit before any file was added:

| command | exit | result |
| --- | ---: | --- |
| `python -m unittest discover -s tests` | 0 | Ran 65 tests, OK |
| `python scripts/check_repo_contract.py` | 0 | Repository contract: PASS |
| `python scripts/reference_coverage.py --check` | 0 | `{"day2_historical": "0/6", "day4_public": "4/6"}` |
| `python scripts/acquisition_ledger.py --check` | 0 | consistent; provenance gaps remain explicit |
| `python scripts/clearance_uncertainty_budget.py --check` | 0 | budget record OK: **INPUTS_PENDING** |
| `python tools/check_presentation.py . "Segmented Shroud Aeromechanics" segmented-shroud-aeromechanics` | 0 | 108 local links, 0 issues |
| `python tools/test_presentation.py` | 0 | OK |
| `git diff --check` | 0 | clean |

The budget verdict is unchanged and remains `INPUTS_PENDING`. Nothing in this work order touches it.

## T01 — source verification

Full parameter table with evidence labels: [source-inventory.json](source-inventory.json). Four findings changed the plan.

**1. The A0.1 source of record is no longer served at its canonical URL.** Every path under `turbmodels.larc.nasa.gov` returns HTTP 301 to `https://www.nasa.gov/nasa-turbulence-modeling-resource/`, a NASA news landing page that contains none of the case content. Verified with curl and a browser user agent, on the case page, the grid page and the site root. The case specification was recovered instead from an Internet Archive snapshot dated **2025-12-19T20:23:26Z**, retrieved and hashed.

This forced a fifth evidence label beyond the four the plan defined. `VERIFIED_FROM_ARCHIVE` means the value was read from a timestamped archival snapshot because the authoritative live page is gone. It is weaker than `VERIFIED_FROM_SOURCE`: the snapshot may not match whatever NASA now considers current, and the resource is visibly being reorganised. Every A0.1 parameter carries this label.

**2. The A0.1 grid family is MISSING and this changes the work.** The TMR grid archives sit behind the same dead domain and are not in the retrieved snapshot. A scripted C-grid family must be generated in-repo. The consequence is recorded in the acceptance file: results will **not** be directly comparable to TMR's published per-grid CFD values, so agreement with other codes is weaker evidence than it would have been on the shared grid family.

**3. The A0.1 airfoil is not the standard NACA 0012.** The case uses a modified section with a **sharp** trailing edge, built by extending the exact formula to x = 1.008930411365 and scaling by that factor, giving a maximum thickness of 11.894 percent of chord. The exact revised formula is in the acceptance file. The earlier case file said only "NACA 0012 (analytic section)", which would have produced the wrong geometry and a wrong answer that looked like a solver failure.

**4. The A0.2 source is fully accessible and its identity is confirmed.** NASA TM-81232 / USAAVRADCOM TR-81-A-23, Caradonna and Tung, September 1981, retrieved from NTRS as 60 pages, 2,334,139 bytes, sha256 `16c14789a5f65892b4ffb4e3628872723195c930f96680068ead7375e57208d2`. Verified from it directly: two cantilever-mounted blades with **half degree precone** (a geometric feature the earlier plan omitted), NACA 0012, untwisted and untapered, aspect ratio 6, collective settings 5/8/12 degrees, pressure stations at r/R = 0.50, 0.68, 0.80, 0.96, and the baseline datum **CT = 0.00460 at 8 degrees collective and 1250 rpm**.

### The finding that most affects A0.2

The report gives tip Mach numbers at 1750, 2250 and 2500 rpm (0.612, 0.794, 0.877). The baseline 1250 rpm condition therefore sits at **Mtip = 0.437**, derived by linear scaling from the reported pair. That is subsonic but **not incompressible**: the Prandtl-Glauert factor is 1.11, implying roughly an 11 percent compressibility influence on outboard sectional Cp.

An incompressible solver run at this condition will show a systematic outboard pressure discrepancy that is **physics, not solver error**. If that is discovered after the runs it will look like a validation failure. It is declared here, before any A0.2 mesh exists, and the solver-regime decision it forces is now an open decision in the work order rather than an assumption.

### Items still blocking

- A0.2 absolute radius and chord are `DERIVED_FROM_SOURCE` and the figure-1 dimension text is OCR-ambiguous. Aspect ratio 6 is verified; the absolute scale must be confirmed visually against figure 1 before meshing. Nondimensional comparisons do not depend on it, blade Reynolds number does.
- A0.2 experimental uncertainty was not located in the retrieved text. Until it is, A0.2's best achievable verdict is `NUMERICALLY_BOUNDED`, not a full validation statement.
- A0.1 numeric comparison values from Ladson NASA TM 4074 and Gregory and O'Reilly R&M 3726 have not been extracted yet; the acceptance file lists this as required before the first run.

## T02 — container smoke test: PASS

Full record: [container-smoke.json](container-smoke.json).

`opencfd/openfoam-default:2512`, digest `sha256:33fb575aa9980d2bc42fd58c75ae698c489293ba30c991380fe3f899c622f319`, pinned by version rather than `latest` so the digest stays meaningful. It is a **native ARM64 build** (`linuxARM64GccDPInt32Opt`), OpenFOAM v2512 on Ubuntu 24.04.3, not x86 emulation. The `pitzDaily` steady incompressible RANS tutorial was chosen over a laminar cavity case because it exercises the same solver class A0.1 and A0.2 will use: `blockMesh` and `checkMesh` gave "Mesh OK" on 12,225 cells and `simpleFoam` converged in 282 iterations in **10 seconds**. The container wrote output to a host-mounted directory.

Two findings:

- **The Docker VM has 7.75 GiB, not the host's 16 GiB.** Every mesh-size estimate in the programme proposal was written against 16 GB and is optimistic by roughly a factor of two. The working ceiling for a steady incompressible case is order 3–4 million cells, not 6–8 million. Either the proposal's feasibility table is corrected or the VM allocation is raised before A0.2 meshing.
- `docker manifest inspect` returned no manifest for all four candidate images, which looks like "no arm64 build exists". The Docker Hub registry API shows arm64 manifests for `opencfd/openfoam-default` from tag 2306 onward. The manifest-inspect failure was a registry artefact. Recorded so the next person does not repeat the false conclusion and switch solvers for no reason.

## T03 — A0.1 acceptance, frozen

[a01-acceptance.json](a01-acceptance.json), frozen before any A0.1 solution exists.

The gated quantity is **lift coefficient at 0 and 10 degrees** against the Ladson tripped dataset, because the source states those data are the most appropriate for comparison with fully turbulent CFD forces at Re = 6 million.

**Drag is reported, not gated.** The earlier plan's default of "drag within 15 percent" was arbitrary and, worse, source-contradicted: the TMR page states that untripped data are inappropriate for fully-turbulent CFD drag comparison and that tripped drag at Re = 3 million runs about 10 percent above tripped drag at Re = 6 million. Gating drag before that systematic is quantified would manufacture a pass or a fail out of a known data artefact. Drag can be promoted to gated in a dated amendment once the experimental uncertainty is extracted.

**15 degrees is reported, not gated**, because the source states the experiments near stall are "no doubt very far from being two-dimensional any more". Skin friction is computed but can never be validated here: the source states no experimental data exist.

## What this record does not establish

No mesh exists. No A0 case has been solved. Nothing here validates a solver, a turbulence model, an open rotor, a duct or a tip gap. Study A remains blocked at its release gate.
