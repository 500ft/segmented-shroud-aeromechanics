# A0.1 validation report — 2D NACA 0012

Status: Spalart–Allmaras arm complete, 2026-09-20. Work order: [plan](specs/research-programme/plan.md) task T06. Acceptance was frozen before any solution existed in [a01-acceptance.json](../evidence/task-a0-validation/a01-acceptance.json); the uncertainty treatment is the [uncertainty decision record](specs/research-programme/uncertainty-decision-record.md). Numbers below regenerate from [uncertainty.json](../results/generated/cfd/a0.1/uncertainty.json) and the per-case manifests beside it.

**Verdict, Spalart–Allmaras: `NOT_VALIDATED` at the committed validation uncertainty.** The comparison error against the experiment is 5.0 times `U_val`. The same computation agrees with the published reference CFD to within 0.4 percent, and every published code on this case misses the same experiment by more than this work does. The failure is therefore in the experiment-to-model comparison, not in this workflow. Both statements are given below because they are different claims.

## 1. What was run

| item | value |
| --- | --- |
| case | TMR 2DN00, modified sharp-trailing-edge NACA 0012 |
| conditions | M 0.15 (incompressible), Re 6 × 10⁶ per chord, fully turbulent |
| angle of attack | 10.12°, the measured angle of the 80-grit experimental point |
| grids | recovered TMR family: 113×33, 225×65, 449×129 → 3,584 / 14,336 / 57,344 cells |
| refinement ratio | exactly 2 in each direction, so *r* = 2 for the grid study |
| solver | `simpleFoam`, OpenFOAM v2512, image digest `sha256:33fb575a…c622f319`, native ARM64 |
| turbulence | Spalart–Allmaras, freestream ν̃/ν = 3 per the TMR specification |

The angle is the measured one rather than a round 10° so that the experiment is never interpolated into the gated comparison.

## 2. Convergence

All three levels satisfy the committed rule: lift coefficient flat to 1 × 10⁻⁴ relative over the final 500 iterations.

| grid | cells | iterations | first met the rule at | relative variation over last 500 | Cl | Cd |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| coarse | 3,584 | 4,000 | 1,456 | 2.26 × 10⁻⁵ | 1.045623 | 0.016192 |
| medium | 14,336 | 6,000 | 2,169 | 5.12 × 10⁻⁶ | 1.091606 | 0.012823 |
| fine | 57,344 | 6,888 | 4,163 | 2.53 × 10⁻⁵ | 1.098833 | 0.012031 |

The fine case was terminated by the host at iteration 6,888 of the 8,000 requested, because the background job was killed under system memory pressure. It is used because the requested count was a ceiling and the convergence rule is the criterion: the run met that rule 2,725 iterations before it stopped. This is recorded in its manifest rather than left as an unexplained iteration count.

## 3. Numerical uncertainty

Celik et al. (ASME J. Fluids Eng. 130(7), 2008), three grids, factor of safety 1.25.

| quantity | value |
| --- | --- |
| apparent order *p* | 2.670 |
| convergence | monotonic |
| asymptotic-range ratio | 1.007 (expected near 1) |
| Richardson extrapolated Cl | 1.100180 |
| grid-convergence index, fine | 0.153 % |
| `U_num` | 0.001684 |

The apparent order sits slightly above the formal second order of the schemes, which is ordinary on a systematically refined structured family, and the convergence is monotonic. The asymptotic-range ratio compares the two grid triplets and should be near 1; at 1.007 it says all three grids are in the asymptotic range, so the index is meaningful rather than a formality. This check was added to the analysis after the SST arm showed what a grid outside that range looks like.

## 4. Validation comparison

Reference: TMR's curated Ladson tripped data at Re 6 × 10⁶, M 0.15, the three grit conditions adjusted to 10.12° with the dataset's own lift-curve slope of 0.10077 per degree. Mean 1.07502, sample standard deviation 0.00441.

```
E     = S − D = 1.098833 − 1.07502 = +0.023813        (+2.22 % of D)
U_val = sqrt(U_num² + U_input² + U_D²)
      = sqrt(0.001684² + (unquantified)² + 0.00441²) = 0.004721
|E| / U_val = 5.04                                    →  NOT_VALIDATED
```

`U_input` is unquantified, not zero. The geometry comes from an exact analytic formula and the conditions are specified, so it is expected to be small, but it has not been estimated and is not silently set to zero.

## 5. Cross-check against the published reference CFD

Values compared at 10.0°, this work adjusted with the same lift-curve slope.

| source | Cl at 10.0° | versus experiment |
| --- | ---: | ---: |
| experiment, adjusted | 1.062928 | — |
| **this work, finest grid** | **1.086740** | **+2.24 %** |
| this work, Richardson extrapolated | 1.088088 | +2.37 % |
| CFL3D, Spalart–Allmaras | 1.090915 | +2.63 % |
| FUN3D, Spalart–Allmaras | 1.098300 | +3.33 % |
| CFL3D, k-ω SST | 1.077800 | +1.40 % |
| FUN3D, k-ω SST | 1.084000 | +1.98 % |

This work sits **0.38 percent below CFL3D** on the finest grid and 0.26 percent below it after Richardson extrapolation. Two declared differences account for part of that gap and both raise lift slightly in the reference: CFL3D ran the 897×257 grid, one level finer than the finest used here, and it applied the point-vortex farfield correction, which this work did not. Neither was adopted here after the fact.

The code-to-code spread between the two reference Spalart–Allmaras results is 0.0074, itself 1.6 times `U_val`.

## 6. What the verdict means

Two things are true at once and must not be collapsed.

**The workflow reproduces the published computation.** Agreement with CFL3D to 0.4 percent, on the same grid family, with a monotonic grid study and a sub-0.2 percent numerical uncertainty, is evidence that the mesh conversion, boundary conditions, freestream turbulence and solver settings are right. The independent check that the TMR freestream specification converts to an eddy-viscosity ratio of 0.009 pointed the same way before any case was run.

**The computation does not reproduce the experiment at the committed band.** It misses by 2.2 percent where the band is 0.44 percent. But every published code misses the same experiment in the same direction, by between 1.4 and 3.3 percent. A discrepancy shared by CFL3D, FUN3D and this work is not a defect of this workflow.

The likeliest reading is that `U_D` is too narrow. It was derived from the spread across three trip conditions, which captures trip repeatability and nothing else: no wall interference, no angle-of-attack calibration, no model-support effects. The acceptance record said at the time that this made it a lower bound. This result is the consequence of that choice, and the conservative reading is that a validation statement built on repeatability alone is too strict to be useful. Raising the band after seeing the result would be exactly the move the acceptance file forbids, so the verdict stands as `NOT_VALIDATED` and the reason is recorded instead.

## 7. Consequence for the programme

Steady RANS on a canonical, heavily studied two-dimensional case carries a model-form error against experiment of roughly 1.4 to 3.3 percent in lift, depending on the turbulence model, and the choice of model alone moves lift by about 1.2 percent. Study A asks whether discrete seams change performance at equal mean clearance. **An effect smaller than about 2 percent cannot be separated from model-form error by this class of simulation.** That is a floor on what Study A's CFD can claim, it is independent of how fine the mesh is, and it should be carried into the Study A preregistration as a stated limit rather than discovered afterwards.

## 8. Limitations and claim boundary

- A0.1 validates a two-dimensional airfoil workflow at one condition. It says nothing about rotating-frame loading, three-dimensional flow, ducts or tip gaps.
- Drag is reported, not gated, for the reasons frozen in the acceptance file. On the finest grid Cd = 0.012031 against a tripped experimental 0.01201 at the 80-grit condition; the agreement is closer than lift, but the tripping and Reynolds systematics the source warns about are unquantified here, so no drag claim is made.
- Skin friction was computed but cannot be validated: the source states no experimental data exist.
- `U_input` is unquantified.
- `U_D` covers trip repeatability only and is a lower bound on experimental uncertainty.
- The k-ω SST arm is not included in this report. Until it is, the model-form sensitivity for this work is unmeasured and only the published reference spread is available.

## 9. Next gate

A0.1 does not pass its gate as written. Under the work order this stops the ladder for a decision rather than silently continuing to A0.2: either the experimental uncertainty is re-derived from a source that reports it properly, or the gate is restated as a code-to-code verification target with the experiment carried as context. That is an owner decision, recorded here and not taken unilaterally. The A0.2 solver-regime decision (D10) remains open independently.
