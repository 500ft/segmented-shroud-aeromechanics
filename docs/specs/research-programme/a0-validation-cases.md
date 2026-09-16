# Study A0 — validation ladder case definitions

Status: draft for owner review, 2026-09-16. Every number in the "nominal" columns is transcribed from memory of the public source and is **to be verified against the cited document in T01/T02 before any run**; the "verified" column stays blank until then. No case has been run.

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

Source of record: NASA Langley Turbulence Modeling Resource, "2D NACA 0012 Airfoil Validation Case", and the experimental references it lists. The TMR page also publishes a family of structured grids; using them removes mesh generation from the critical path and makes the grid-convergence study comparable to published results.

| item | nominal (verify) | verified | locator |
| --- | --- | --- | --- |
| Mach | 0.15 | | TMR case page |
| Reynolds number, chord-based | 6 × 10⁶ | | TMR case page |
| angles of attack | 0°, 10°, 15° | | TMR case page |
| reference quantities | lift and drag coefficients; surface pressure coefficient | | TMR page and cited wind-tunnel data |
| grid family | TMR structured C-grids, at least three levels | | TMR grid page |
| turbulence models | Spalart–Allmaras; k-ω SST | | plan D4 |

Acceptance, fixed in T03 before running, per plan D9: comparison error E on lift and drag at 0° and 10° against the validation uncertainty U_val (15° is near stall and is reported, not gated); GCI on the finest grid by the Celik et al. 2008 procedure; the TMR's published CFD results plotted alongside as the field's spread. Validated at the U_val level when |E| ≤ U_val; U_val is reported so a reader can judge how strong that statement is. Solver: incompressible at M 0.15 is defensible; the compressibility neglect is recorded as an assumption, optimistic on drag by a known small amount.

## 3. A0.2 — Caradonna–Tung hover rotor

Source of record: F. X. Caradonna and C. Tung, "Experimental and Analytical Studies of a Model Helicopter Rotor in Hover", NASA TM 81232, 1981.

| item | nominal (verify) | verified | locator |
| --- | --- | --- | --- |
| blades | 2, untwisted, rectangular planform | | TM 81232 |
| section | NACA 0012 | | TM 81232 |
| radius R | 1.143 m | | TM 81232 |
| chord c | 0.1905 m (aspect ratio 6) | | TM 81232 |
| collective pitch | 8° | | TM 81232 test matrix |
| rotor speed | 1250 rpm (subsonic tip) and 2500 rpm (transonic tip) | | TM 81232 test matrix |
| measured quantities | sectional pressure coefficient at several r/R stations; thrust coefficient; tip-vortex trajectory | | TM 81232 |

Only the subsonic-tip condition is in scope for an incompressible solver; the transonic condition is out. Domain: one blade with 180° periodic boundaries in a rotating frame (MRF), far-field distance and boundary treatment for hover recorded as assumptions. Acceptance, fixed in T03, per plan D9: comparison error on thrust coefficient against U_val; sectional pressure distributions at the stations most commonly used in published reproductions of this rotor (nominally r/R = 0.50, 0.68, 0.80, 0.89, 0.96, to verify against the report) with an RMS error per station; GCI on thrust by the Celik et al. 2008 procedure; two turbulence models; published CFD reproductions of this rotor tabulated as the field's spread.

## 4. Claim boundary after the ladder

- After A0.1: the workflow reproduces canonical 2D data within stated bands. Nothing about rotors.
- After A0.2: the workflow reproduces measured loading on an open rotor with NACA 0012 blades. Nothing about ducts or tip gaps; nothing about small-UAV Reynolds numbers (the model rotor's chord Reynolds number is higher than a small UAV's).
- Until A0.3: every Study A effect size carries the label "gap-unvalidated", and the proposal's kill criterion for A applies to the numerical band only, not to model-form error at the gap.

## 5. Study A rotor after this decision

Study A's rotor is the A0.2 rotor unchanged (two untwisted NACA 0012 blades, R = 1.143 m, c = 0.1905 m, 8° collective, 1250 rpm), placed inside a generic duct with the seam parameters (n, g, s). This is plan decision D3 under the owner's rule of taking the most-used baseline: the open-rotor half of every Study A comparison then has the largest published comparator set of any rotor. The chord Reynolds number is higher than a small UAV's; scale transfer is a later study and the Reynolds number is reported on every case.
