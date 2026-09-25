# Study A0 — validation ladder case definitions

Status: **source verification complete, 2026-09-19** (work-order task T01). The nominal values below have been checked against the documents; the verified column now carries the outcome and the locator. Full parameter table with evidence labels: [source-inventory.json](../../../evidence/task-a0-validation/source-inventory.json). Findings and access problems: [execution record](../../../evidence/task-a0-validation/README.md). No mesh exists and no case has been run.

Owner decision 2026-09-16: the validation baseline is a standard aircraft wing, not a ducted fan. This trades the ducted-fan geometry-availability risk for a narrower validation claim, stated in §4.

## 1. Why a ladder

A single wing case validates the numerical workflow: solver, mesh family, wall treatment, turbulence model, grid-convergence procedure. It does not validate rotating-frame loading or tip-gap flow. The ladder adds one rung at a time and labels every Study A result by the highest rung passed.

| rung | case | geometry public | measured data public | what passing validates | what it does not validate |
| --- | --- | --- | --- | --- | --- |
| A0.1 | NACA 0012 airfoil, 2D, subsonic | yes (analytic section) | yes (NASA Turbulence Modeling Resource case page and the wind-tunnel data it cites) | solver, GCI procedure, y⁺ handling, two turbulence models | 3D, rotation, tip flow |
| A0.2 | Caradonna–Tung two-blade hover rotor, NACA 0012 blades | yes (NASA TM 81232) | yes (sectional pressure and thrust in the same report) | rotating frame, blade loading, tip vortex on an open rotor, periodic single-blade domain | duct, tip gap, small-UAV Reynolds number |
| A0.3 | ducted fan with published blade geometry | unverified | partial | tip-gap flow inside a duct | — |

A0.3 stays deferred until a source with usable geometry is confirmed; Study A may start after A0.2 with its results labelled **rotor-validated, gap-unvalidated**.

## 2. A0.1 — NACA 0012, 2D

Source of record: NASA Langley Turbulence Modeling Resource, "2D NACA 0012 Airfoil Validation Case". **The live site is gone.** Every path under `turbmodels.larc.nasa.gov` now returns HTTP 301 to a NASA landing page with none of the case content. The specification below was recovered from an Internet Archive snapshot of **2025-12-19T20:23:26Z** and every A0.1 row therefore carries the evidence label `VERIFIED_FROM_ARCHIVE`, which is weaker than reading the authoritative page.

| item | nominal (as planned) | verified outcome | locator |
| --- | --- | --- | --- |
| Mach | 0.15 | **confirmed** 0.15 | "the recommendation here is to run M = 0.15 in compressible CFD codes" |
| Reynolds number, chord-based | 6 × 10⁶ | **confirmed** 6 × 10⁶ | "The Reynolds number per chord is Re = 6 million." |
| angles of attack | 0°, 10°, 15° | **confirmed** for Cp and Cf; CL is compared over a range | "Surface pressure coefficient (Cp) vs. x/c (for alpha = 0, 10, 15)" |
| transition state | not stated in the plan | **fully turbulent** | "Boundary layers should be fully turbulent over most of the airfoil." |
| airfoil section | "NACA 0012 (analytic section)" | **WRONG AS PLANNED**: a modified **sharp-trailing-edge** section, max thickness 11.894% of chord | revised formula on the case page; extend the exact formula to x = 1.008930411365 then scale by that factor |
| farfield | not stated in the plan | ~500 chords in the provided grids, else the point-vortex correction is mandatory | Thomas and Salas, AIAA J 24(7):1074–1080, 1986 |
| force data of record | "the TMR's cited experimental data" | **Ladson, NASA TM 4074, 1988 (tripped)** | "the most appropriate of these data sets for comparison with fully turbulent CFD forces at Re=6 million"; NTRS 19880019495 |
| pressure data of record | not stated in the plan | **Gregory and O'Reilly, R&M 3726, 1970** (tripped, Re = 3 × 10⁶) | better resolved at the leading-edge suction peak than Ladson TM 100526 |
| grid family | "TMR structured C-grids, at least three levels" | **MISSING**: the grid archives are behind the dead domain | a scripted C-grid family must be generated instead |
| turbulence models | Spalart–Allmaras; k-ω SST | unchanged | reported per model, never averaged |

Two consequences of the verification. The **grid family is gone**, so a scripted C-grid must be generated and results are not directly comparable to TMR's published per-grid CFD values; agreement with other codes is therefore weaker evidence than it would have been on the shared family. The **airfoil as previously written was wrong**: substituting the standard blunt-trailing-edge NACA 0012 would have produced a wrong answer that looked like a solver failure.

Acceptance is frozen in [a01-acceptance.json](../../../evidence/task-a0-validation/a01-acceptance.json). **Lift at 0° and 10° is the only gated quantity**, against the Ladson tripped dataset, judged by |E| ≤ U_val per the [uncertainty decision record](uncertainty-decision-record.md). **Drag is reported, not gated**: the source states untripped data are inappropriate for fully-turbulent CFD drag comparison and that tripped drag at Re = 3 × 10⁶ runs about 10% above tripped drag at Re = 6 × 10⁶, so gating drag before that systematic is quantified would manufacture a pass or a fail from a data artefact. The earlier "drag within 15%" default is withdrawn. **15° is reported, not gated**, because the source states the experiments there are "no doubt very far from being two-dimensional any more". **Skin friction can never be validated here**: the source states no experimental data exist. Solver: incompressible at M 0.15, Prandtl–Glauert factor 1.011, so about 1% influence on Cp, recorded as a declared bias and not folded into any uncertainty band.

## 3. A0.2 — Caradonna–Tung hover rotor

Source of record: F. X. Caradonna and C. Tung, "Experimental and Analytical Studies of a Model Helicopter Rotor in Hover", NASA TM 81232, 1981.

Retrieved from NTRS as accession 19820004169: 60 pages, 2,334,139 bytes, sha256 `16c14789…57208d2`. Report identity confirmed on page 1, including the number **NASA-TM-81232** the plan cited.

| item | nominal (as planned) | verified outcome | locator |
| --- | --- | --- | --- |
| blades | 2, untwisted, rectangular planform | **confirmed**, and they carry **half degree precone** the plan omitted | "two cantilever-mounted, manually adjustable blades with half degree precone" |
| section | NACA 0012 | **confirmed**, untwisted and untapered | "These blades used an NACA 0012 profile and were untwisted and untapered." |
| aspect ratio | implied 6 | **confirmed** 6 | "An aspect ratio of 6 was chosen in order to maximize Reynolds Number and available instrumentation space." |
| radius R | 1.143 m | **DERIVED, not verified**: the figure-1 dimension text is OCR-ambiguous | must be confirmed visually against figure 1 before meshing |
| chord c | 0.1905 m | **DERIVED** as R / 6 | same confirmation requirement |
| collective pitch | 8° | **confirmed** as one of 5°, 8°, 12° | figures 3, 4, 5 |
| rotor speed | 1250 rpm subsonic, 2500 rpm transonic | **confirmed**; 2500 rpm is Mtip 0.877 and is out of scope | figure annotations |
| baseline datum | not stated in the plan | **CT = 0.00460** at 8° collective, 1250 rpm | "Omega = 1250 rpm, CT = 0.00460" |
| pressure stations | "several r/R stations" | **r/R = 0.50, 0.68, 0.80, 0.96** | figure annotations; three radial locations per blade |
| experimental uncertainty | assumed available | **MISSING** in the retrieved text | caps the A0.2 verdict at `INCOMPLETE_UNCERTAINTY` (previously `NUMERICALLY_BOUNDED`, retired 2026-09-24) |

### The baseline condition is not incompressible

The report gives Mtip at 1750, 2250 and 2500 rpm as 0.612, 0.794 and 0.877. Linear scaling puts the **1250 rpm baseline at Mtip = 0.437**. The Prandtl–Glauert factor is 1.11, so an incompressible solver will show roughly an 11% systematic discrepancy in outboard sectional Cp. **That is physics, not solver error.** Discovered after the runs it would read as a validation failure; it is declared here before any A0.2 mesh exists, and it forces the solver-regime decision now open as **D10** in the [work order](plan.md).

The transonic conditions are out of scope. Domain: one blade with 180° periodic boundaries in a rotating frame, far-field distance and boundary treatment for hover recorded as assumptions. Acceptance will be frozen the same way A0.1's was, before any A0.2 solution exists, and cannot be written until D10 settles the solver regime: **CT = 0.00460 is the force datum**, sectional Cp is compared at the verified stations r/R = 0.50, 0.68, 0.80 and 0.96 with the Mtip 0.437 compressibility bias stated per station, numerical uncertainty by the Celik et al. 2008 procedure, both turbulence models reported separately. Because the source's own measurement uncertainty was not located, the best achievable A0.2 verdict is `NUMERICALLY_BOUNDED` rather than a full validation statement.

## 4. Claim boundary after the ladder

- After A0.1: the workflow reproduces canonical 2D data within stated bands. Nothing about rotors.
- After A0.2: the workflow reproduces measured loading on an open rotor with NACA 0012 blades. Nothing about ducts or tip gaps; nothing about small-UAV Reynolds numbers (the model rotor's chord Reynolds number is higher than a small UAV's).
- Until A0.3: every Study A effect size carries the label "gap-unvalidated", and the proposal's kill criterion for A applies to the numerical band only, not to model-form error at the gap.

## 5. Study A rotor after this decision

Study A's rotor is the A0.2 rotor unchanged (two untwisted NACA 0012 blades, R = 1.143 m, c = 0.1905 m, 8° collective, 1250 rpm), placed inside a generic duct with the seam parameters (n, g, s). This is plan decision D3 under the owner's rule of taking the most-used baseline: the open-rotor half of every Study A comparison then has the largest published comparator set of any rotor. The chord Reynolds number is higher than a small UAV's; scale transfer is a later study and the Reynolds number is reported on every case.
