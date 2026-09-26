# Validation scope map
Date: 2026-09-25 · Review item R08 · Ledger row SSY-R16

A validation case supports claims about the quantities it actually compared, at the conditions
it actually ran. This table exists so that no case can be cited for more than that. Agreement
on thrust and pressure does not by itself validate shaft torque, gap leakage or tip-vortex
trajectory, and those are the quantities Study A depends on.

Nothing here is a transfer. A row records what a case can support; the bridge from any of them
to a small physical rotor is the separate open question in [§4](#4-the-scale-bridge-is-not-closed).

## 1. Case rows

| | **A0.1 Spalart-Allmaras** | **A0.1 k-ω SST** | **A0.2 (planned)** | **Candidate ducted-fan benchmark** |
| --- | --- | --- | --- | --- |
| Source | NASA TMR 2D NACA 0012, recovered from a dated archive snapshot | same | Caradonna–Tung hovering rotor | Akturk & Camci, GT2011-46356, ASME Turbo Expo 2011 |
| Geometry completeness | modified **sharp** trailing edge, not the standard section | same | published rotor dimensions, some needing visual verification | **partial**, see [§3](#3-benchmark-geometry-and-data-audit) |
| Reynolds number | 6 × 10⁶, chord | same | as published | **not stated**; derived ≈ 4.3 × 10⁵ on tip chord |
| Mach number | 0.15 | same | Mtip 0.437 at the 1250 rpm baseline | **not stated**; derived Mtip ≈ 0.30 at 3500 rpm |
| Transition state | fully turbulent against tripped data | same | as published | not stated |
| Quantities compared | lift at 0° and 10° (gated); drag reported | none | thrust coefficient; sectional Cp | thrust and power coefficients; rotor-exit total pressure |
| Clearance present | none | none | none | **yes**, 1.71% and 3.04% of blade height |
| Experimental uncertainty | **absent**; the grit spread is a treatment sensitivity, not U_D | same | **absent** in the retrieved text | **absent** for C_T and C_P; only transducer accuracy is quoted |
| Numerical uncertainty | GCI on three levels, apparent order computed | **incomplete**, two of three levels | not run | **absent**; three meshes compared by eye, no order, no index |
| Assessment state | `INCOMPLETE_UNCERTAINTY` | no verdict | not started | not a validation case as published |
| Supports | that this workflow reproduces a published 2-D computation | nothing yet | thrust, if D10 is settled | that a ducted rotor's thrust and power respond to tip clearance |
| Does **not** support | any rotating, three-dimensional, ducted or tip-gap claim; any seam-effect floor | anything | shaft torque, gap leakage or tip-vortex trajectory | a resolved tip-gap accuracy claim; any seam or seam-topology claim |

## 2. What each case is missing

- **A0.1 SA.** No experimental standard uncertainty exists, so the comparison against the
  experiment cannot be completed at any mesh density. Finishing more grids does not change this.
- **A0.1 SST.** The fine grid was stopped by host memory exhaustion. Two levels cannot carry an
  index or an order, so the model-form sensitivity for this work is unmeasured. Its recovery is a
  resource and checkpoint problem and does **not** depend on D10.
- **A0.2.** Not started. D10 is open, and with the Prandtl–Glauert reading corrected the
  incompressible option no longer carries a bias of known size.
- **Benchmark.** Published as an engineering study, not as a validation case. It has no numerical
  uncertainty and no experimental uncertainty on the integrated coefficients.

## 3. Benchmark geometry and data audit

Retrieved 2026-09-25 from an open conference-proceedings copy. Title, both authors, institution
and paper number match the record. The journal version, *J. Turbomach.* 136(2):021004 (2014),
sits behind a publisher interstitial that was not circumvented; conference and journal versions
are treated as one study family. Audited by reading pages 1–6.

**Present, numerically:** rotor hub radius 63.5 mm; rotor tip radius 279.4 mm at the 1.71%
clearance build; 8 blades; rotor pitch angle 55°; maximum tip thickness 5.15 mm; a nine-station
table of radius, r/R, inlet and outlet blade angles and chord; shroud inner radius 11.15 in; duct
lip wall thickness and leading-edge radius as percentages of duct chord; diffuser half-angle 6°
and axial length 117.85 mm; nominal 3500 rpm; disk loading 828.3 Pa. Force and torque transducer
accuracy is quoted per axis, to ±0.099 N on the thrust axis.

**Absent:** blade section coordinates, which appear only as a figure; the duct profile as
coordinates; any Reynolds or Mach number; transition state; a grid-convergence index, apparent
order or numerical uncertainty, the three meshes being compared by inspecting one pressure
profile; and any experimental uncertainty for the thrust and power coefficients, the quoted
transducer accuracy being an instrument specification rather than an uncertainty statement for
the reported quantity.

**Directly relevant to this project:** the study measures **ducted-fan thrust and fan-rotor-only
thrust separately**, which is exactly the force-boundary distinction the design contract now
requires. Clearance was varied by changing the rotor diameter, so the rotor is **not the same
machine** between clearance conditions.

A paper being readable does not make its geometry reproducible. The blade sections and duct
profile would have to be recovered or re-specified before any computation could claim to
reproduce this rig, and that recovery is not attempted here.

## 4. The scale bridge is not closed

Transfer to a small physical rotor needs the following recorded for both ends. Values marked
*derived* are computed here from the paper's own numbers and are not stated by it.

| ratio | benchmark | small physical rotor |
| --- | --- | --- |
| clearance / blade height | 1.71% and 3.04% | open |
| clearance / tip chord | 0.058 *(derived)* | open |
| clearance / tip radius | 0.0132 *(derived)* | open |
| seam width / chord | not applicable, no seams | open |
| step / clearance | not applicable | open |
| blade count | 8 | open |
| tip Reynolds number | ≈ 4.3 × 10⁵ *(derived)* | open |
| tip Mach number | ≈ 0.30 *(derived)* | open |
| duct profile | partially specified | open |

This is a coverage table, not a similarity sweep. Matching one ratio does not match the flow
regime, and every right-hand entry depends on owner inputs that do not exist. **No computation
on the large rotor supplies an installed sensitivity for a small one without an evidenced
bridge, and no such bridge exists today.**
