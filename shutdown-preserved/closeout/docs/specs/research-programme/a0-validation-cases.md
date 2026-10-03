# Study A0 — validation ladder case definitions

Status: **source assessment updated 2026-09-29; A0.2 geometry verification remains incomplete**. A0.1 has three completed SA grid levels and an incomplete SST arm; its experimental comparison is `INCOMPLETE_UNCERTAINTY`. The verified column records each source outcome and unresolved input. Full parameter table with evidence labels: [source-inventory.json](../../../evidence/task-a0-validation/source-inventory.json). Findings and access problems: [execution record](../../../evidence/task-a0-validation/README.md). Current computation: [A0.1 report](../../cfd-validation-a01.md). Quantity-specific coverage: [validation scope map](validation-scope-map.md). No A0.2 run is released.

Owner decision 2026-09-16: the validation baseline is a standard aircraft wing, not a ducted fan. This trades the ducted-fan geometry-availability risk for a narrower validation claim, stated in §4.

## 1. Why a ladder

Each case supplies numerical and experimental comparison evidence only for its reported quantities and conditions. A wing case exercises a numerical workflow; it does not independently validate every solver setting or transfer to rotating-frame loading and tip-gap flow. Report the uncertainty verdict and scope of each completed comparison, rather than treating completion as a validation pass.

| rung | case | geometry public | measured data public | intended comparison scope | what it does not validate |
| --- | --- | --- | --- | --- | --- |
| A0.1 | NACA 0012 airfoil, 2D, subsonic | yes (analytic section) | yes (NASA Turbulence Modeling Resource case page and the wind-tunnel data it cites) | 2D lift and reported drag at the specified conditions; numerical convergence per usable model | 3D, rotation, tip flow |
| A0.2 | Caradonna–Tung two-blade hover rotor, NACA 0012 blades | yes (NASA TM 81232) | yes (sectional pressure and thrust in the same report) | integrated thrust and sectional pressure on an open rotor; no independent tip-vortex or torque comparison | duct, tip gap, small-UAV Reynolds number |
| A0.3 | ducted fan with published blade geometry | unverified | partial | tip-gap flow inside a duct | — |

A0.3 stays deferred until usable geometry and comparison data are confirmed. Study A requires the recorded A0.2 release decision and its own preregistration; report the actual A0.2 verdict with **gap-unvalidated**, without automatically promoting an incomplete comparison to rotor validation.

## 2. A0.1 — NACA 0012, 2D

Source of record: NASA Langley Turbulence Modeling Resource, "2D NACA 0012 Airfoil Validation Case". **Access observation, 2026-09-19:** the attempted paths under `turbmodels.larc.nasa.gov` redirected to a NASA landing page without the case content. The specification below was recovered from an Internet Archive snapshot of **2025-12-19T20:23:26Z** and every A0.1 row therefore carries the evidence label `VERIFIED_FROM_ARCHIVE`, which is weaker than reading the authoritative page.

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
| grid family | "TMR structured C-grids, at least three levels" | **RECOVERED 2026-09-20**: archive grid levels 113×33, 225×65 and 449×129 | [work-order T04](plan.md), case manifests and [A0.1 report](../../cfd-validation-a01.md) |
| turbulence models | Spalart–Allmaras; k-ω SST | unchanged | reported per model, never averaged |

The original grid-access barrier was resolved by recovering the shared TMR family from the archive; no replacement scripted family was needed. The **airfoil as previously written was wrong**: substituting the standard blunt-trailing-edge NACA 0012 would have produced a wrong answer that looked like a solver failure.

Acceptance is frozen in [a01-acceptance.json](../../../evidence/task-a0-validation/a01-acceptance.json). **Lift at 0° and 10° is the only gated quantity**, against the Ladson tripped dataset, judged by |E| ≤ U_val per the [uncertainty decision record](uncertainty-decision-record.md). **Drag is reported, not gated**: the source states untripped data are inappropriate for fully-turbulent CFD drag comparison and that tripped drag at Re = 3 × 10⁶ runs about 10% above tripped drag at Re = 6 × 10⁶, so gating drag before that systematic is quantified would manufacture a pass or a fail from a data artefact. The earlier "drag within 15%" default is withdrawn. **15° is reported, not gated**, because the source states the experiments there are "no doubt very far from being two-dimensional any more". **Skin friction can never be validated here**: the source states no experimental data exist. Solver: incompressible at M 0.15. The Prandtl–Glauert factor 1.011 is a linearised sensitivity indicator, not a measured 1% Cp bias or an uncertainty correction. Compressibility discrepancy is unquantified. Only the completed 10.12° SA comparison is reported; the frozen scope does not imply every planned angle was run.

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

The report gives Mtip at 1750, 2250 and 2500 rpm as 0.612, 0.794 and 0.877. Linear scaling puts the **1250 rpm baseline at Mtip = 0.437**. The Prandtl–Glauert factor at that Mach number is 1.11.

**Corrected 2026-09-25.** The earlier text turned that factor into a predicted 11% discrepancy in outboard sectional Cp. It is not a prediction and not an error correction. Prandtl–Glauert is a linearised, thin-aerofoil, two-dimensional, steady, irrotational result. A rotor blade section carries induced flow from its own wake and its neighbours, radial flow, thickness and viscous effects, none of which that relation describes. What the factor legitimately supports is a **sensitivity flag**: compressibility is not negligible at this condition and an incompressible solver will carry an unquantified bias whose size is not given by 1.11.

The number therefore may not be quoted as a per-station correction, and an observed discrepancy near 11% would be coincidence rather than confirmation. Declaring it before any A0.2 mesh exists still matters, because discovered afterwards it would read as a validation failure. It forces the solver-regime decision open as **D10** in the [work order](plan.md), where the size of the bias is something to *measure* where it is material, not to predict from a linearised factor.

The transonic conditions are out of scope. Domain: one blade with 180° periodic boundaries in a rotating frame, far-field distance and boundary treatment for hover recorded as assumptions. Acceptance will be frozen the same way A0.1's was, before any A0.2 solution exists, and cannot be written until D10 settles the solver regime: **CT = 0.00460 is the force datum**, sectional Cp is compared at the verified stations r/R = 0.50, 0.68, 0.80 and 0.96 with solver regime and any unquantified compressibility discrepancy stated, numerical uncertainty by the Celik et al. 2008 procedure, both turbulence models reported separately. Because the source's own measurement uncertainty was not located, usable numerical evidence would still yield `INCOMPLETE_UNCERTAINTY` until the required experimental and input uncertainties are quantified; unusable numerical evidence instead yields `INCONCLUSIVE`. No result or verdict is claimed before a run.

## 4. Claim boundary after the ladder

- A0.1 currently supplies 2D numerical and cross-code evidence at its computed condition; the experimental comparison is `INCOMPLETE_UNCERTAINTY`. It supports no rotor claim.
- After A0.2: report the actual thrust and sectional-pressure comparisons and their uncertainty verdict. Those quantities alone do not validate shaft torque, tip-vortex trajectory, ducts or tip gaps, or establish transfer to small-UAV Reynolds numbers.
- Until A0.3: every Study A effect size carries the label "gap-unvalidated", and the proposal's screening rule includes numerical uncertainty and sampled clocking/model sensitivities; it is not a bound on physical model error at the gap.

## 5. Study A rotor after this decision

Study A's planned rotor is the A0.2 rotor unchanged (two untwisted NACA 0012 blades, R = 1.143 m, c = 0.1905 m, 8° collective, 1250 rpm), placed inside a generic duct with the seam parameters (n, g, s). Radius and chord remain provisional until their source dimensions are visually verified; no geometry is released by this paragraph. This is plan decision D3 under the owner's rule of taking the most-used baseline: the open-rotor half of every Study A comparison then has the largest published comparator set of any rotor. The chord Reynolds number is higher than a small UAV's; scale transfer is a later study and the Reynolds number is reported on every case.
