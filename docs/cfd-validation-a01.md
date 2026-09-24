# A0.1 validation report — 2D NACA 0012

Status: Spalart–Allmaras arm complete, 2026-09-20. Work order: [plan](specs/research-programme/plan.md) task T06. Acceptance was frozen before any solution existed in [a01-acceptance.json](../evidence/task-a0-validation/a01-acceptance.json); the uncertainty treatment is the [uncertainty decision record](specs/research-programme/uncertainty-decision-record.md). Numbers below regenerate from [uncertainty.json](../results/generated/cfd/a0.1/uncertainty.json) and the per-case manifests beside it.

> **Correction, 2026-09-24.** An external review reproduced three errors in the interpretation below. They are corrected in place and the original calculations are preserved: no run, raw output or frozen acceptance record was changed. (1) The stated `U_val` combined only the known terms while a required component was unquantified, which treats an unknown as zero. (2) The spread across grit treatments was called repeatability; the grit sizes are different experimental conditions, not repeats of one. (3) The asymptotic-range ratio was presented as confirmation; it is algebraically `|phi_fine/phi_medium|` and confirms nothing. A fourth error, a universal "2 percent floor" for seam effects, is withdrawn in section 7.

**Verdict, Spalart–Allmaras: `INCOMPLETE_UNCERTAINTY`.** A complete validation uncertainty is not available, because the input component was never quantified and an unquantified component cannot be dropped. The comparison error is +0.0238 in lift coefficient against a **partial combination of the known terms** of 0.0047. That ratio of about five is worth reporting and is not a validation verdict.

Separately and more robustly: the same computation agrees with the published reference computations to within 0.4 percent. Those are different claims and are kept apart below.

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
| asymptotic-range ratio | 1.007 — **diagnostic only, see below** |
| Richardson extrapolated Cl | 1.100180 |
| grid-convergence index, fine | 0.153 % |
| `U_num` | 0.001684 |

The apparent order sits slightly above the formal second order of the schemes, which is ordinary on a systematically refined structured family, and the convergence is monotonic.

**The asymptotic-range ratio confirms nothing and no longer gates anything.** With equal refinement ratios and the order fitted from the same three values, `r^p = |(phi3−phi2)/(phi2−phi1)|` identically, and the ratio then reduces algebraically to `|phi_fine/phi_medium|`. The reported 1.00662 is exactly the fine-to-medium lift ratio, which a test now demonstrates. One three-grid set gives two *adjacent* pairs, not two independent triplets. Establishing asymptotic behaviour would need a further refinement level and stability across overlapping triplets, together with iterative-error, domain-extent and wall-treatment checks. The three-grid estimate is retained with its assumptions stated, and nothing here claims more than that.

## 4. Validation comparison

Reference: TMR's curated Ladson tripped data at Re 6 × 10⁶, M 0.15, the three grit conditions adjusted to 10.12° with the dataset's own lift-curve slope of 0.10077 per degree. Mean 1.07502, sample standard deviation 0.00441.

```
E                     = S − D = 1.098833 − 1.07502 = +0.023813     (+2.22 % of D)
U_num                 = 0.001684                                    numerical, three-grid index
U_input               = UNQUANTIFIED                                not zero
U_D                   = 0.00441                                     see the reclassification below
partial combination   = sqrt(U_num² + U_D²)         = 0.004721      KNOWN TERMS ONLY
U_val                 = null                                        a required component is missing
|E| / partial         = 5.04                        →  INCOMPLETE_UNCERTAINTY
```

The figure 0.004721 was previously reported as `U_val`. It is a partial combination of the terms that happen to be quantified, and it is now named as such. Dropping an unquantified component is equivalent to setting it to zero, which is the one value it is known not to have.

**The 0.00441 term is reclassified.** It was described as trip repeatability. The 80, 120 and 180 grit conditions are *different boundary-layer trips*, that is different experimental conditions, not repeated measurements under identical conditions. Their spread is **treatment sensitivity**, and the individual comparator values are preserved rather than collapsed into one number. Whether it also bounds measurement repeatability is unknown, and any interpolation or incidence adjustment applied in reaching a common angle carries its own uncertainty that has not been quantified.

The rule `|E| ≤ U_val` is this project's **consistency screen**, not a universal pass or fail. A wider band must never make a less informative computation look more accurate.

`U_input` is unquantified, not zero. The geometry comes from an exact analytic formula and the conditions are specified, so it is expected to be small, but expectation is not estimation and the calculation no longer proceeds as though it were.

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

## 5a. k-ω SST arm: incomplete, no verdict

Two of three levels completed. The fine grid was stopped at iteration 117 of 6,000 because the host had 63 MB of free memory and was swapping; the container was using 97 MB of its 3 GB limit on one saturated core, and the case was running at roughly 0.15 iterations per second against 4.6 for the same mesh under Spalart–Allmaras. That is a thrashing signature, not the cost of two extra transport equations, so it is recorded as host resource exhaustion rather than a solver or setup failure. It is retained with status `UNCONVERGED` and excluded from every reported quantity.

| grid | cells | iterations | Cl | Cd | status |
| --- | ---: | ---: | ---: | ---: | --- |
| coarse | 3,584 | 3,000 | 1.133621 | 0.003532 | PASS |
| medium | 14,336 | 4,000 | 1.105396 | 0.009416 | PASS |
| fine | 57,344 | 117 | — | — | UNCONVERGED, excluded |

**No grid-convergence index and no verdict are issued for SST**, because the procedure needs three converged levels and there are two.

The two that exist are still informative. On the coarse grid SST gives a drag of 0.003532 against Spalart–Allmaras's 0.016192 on the identical mesh, a factor of 4.6, where the published values for the two models agree to within 0.4 percent. The medium grid moves most of the way back, to 0.009416. That is the signature of a grid outside the asymptotic range rather than a broken setup: the two-equation model needs more resolution than the one-equation model before its wall treatment behaves, and the coarsest TMR level does not provide it. The solver log confirms `kOmegaSST` was selected with standard coefficients and no warnings, and the eddy-viscosity ratio reaches 1,376 against 1,988 for Spalart–Allmaras, so turbulence is developing.

Adjusted to 10.12°, the published CFL3D SST value is 1.0899; the medium grid here gives 1.105396, 1.4 percent high, which is the direction and magnitude an under-resolved two-equation model would give. Nothing further should be read into it.

This arm is the first item for the next working session.

## 6. What the verdict means

Two things are true at once and must not be collapsed.

**The workflow reproduces the published computation.** Agreement with CFL3D to 0.4 percent, on the same grid family, with a monotonic grid study and a sub-0.2 percent numerical uncertainty, is evidence that the mesh conversion, boundary conditions, freestream turbulence and solver settings are right. The independent check that the TMR freestream specification converts to an eddy-viscosity ratio of 0.009 pointed the same way before any case was run.

**The computation does not reproduce the experiment within the known terms.** It misses by 2.2 percent where the partial combination is 0.44 percent.

An earlier version of this section said every published code misses this experiment by more than this work does. **That is false**, and the table above shows it: the SST reference results are 1.40 and 1.98 percent, both **below** this work's 2.24 percent. What the table does support is narrower: every code listed misses in the same direction, by between 1.4 and 3.3 percent, and this work sits inside that range rather than outside it.

Agreement with another code is cross-code evidence, not proof that workflow errors are absent. Nor may tunnel uncertainty be declared the cause before geometry, Mach number, incidence adjustment, wall treatment, farfield placement and turbulence model have been separated. The likeliest single contributor remains that the comparison band is built from an incomplete uncertainty budget, which is now stated rather than assumed.

The likeliest reading is that `U_D` is too narrow. It was derived from the spread across three trip conditions, which captures trip repeatability and nothing else: no wall interference, no angle-of-attack calibration, no model-support effects. The acceptance record said at the time that this made it a lower bound. This result is the consequence of that choice, and the conservative reading is that a comparison band built on one treatment contrast alone is too narrow to support a validation statement. Raising the band after seeing the result would be exactly the move the acceptance file forbids, so the band is left as committed and the reason is recorded instead. The verdict is `INCOMPLETE_UNCERTAINTY`, as section 3 sets out: with `U_input` unquantified there is no `U_val` for `|E|` to be judged against, so `NOT_VALIDATED` is not available here and the earlier text asserting it is withdrawn.

## 7. Consequence for the programme

**The universal "2 percent floor" asserted here is withdrawn.** The earlier text said that a seam effect below roughly 2 percent could not be separated from model-form error by this class of simulation, at any mesh density, and that figure propagated into the design contract and the literature review.

The inference does not hold. This report observes a discrepancy in **absolute lift on a two-dimensional airfoil** at one condition. A seam study reports a **difference in ducted-rotor power between two configurations**. Those are different quantities, different geometry and different operating conditions. Errors in a paired comparison may cancel, differ or compound, and cancellation has to be investigated rather than presumed. Two turbulence models cannot bound every shared modelling error either.

What survives is a requirement, not a number: **Study A must estimate the numerical and model sensitivity of the paired difference it will actually report, at its own conditions**, before its amplitudes are frozen. The rig's floor comes from its own budget. Neither may be inherited from this case.

## 8. Limitations and claim boundary

- A0.1 validates a two-dimensional airfoil workflow at one condition. It says nothing about rotating-frame loading, three-dimensional flow, ducts or tip gaps.
- Drag is reported, not gated, for the reasons frozen in the acceptance file. On the finest grid Cd = 0.012031 against a tripped experimental 0.01201 at the 80-grit condition; the agreement is closer than lift, but the tripping and Reynolds systematics the source warns about are unquantified here, so no drag claim is made.
- Skin friction was computed but cannot be validated: the source states no experimental data exist.
- `U_input` is unquantified, so no complete validation uncertainty exists for this case.
- The asymptotic-range ratio is a diagnostic with a known algebraic identity, not evidence.
- `U_D` covers trip repeatability only and is a lower bound on experimental uncertainty.
- The k-ω SST arm is incomplete (two of three levels), so it carries no index and no verdict. The model-form sensitivity **for this work** is therefore unmeasured; only the published reference spread is available, and the SST numbers above must not be quoted as a result.

## 9. Next gate

A0.1 does not pass its gate as written. Under the work order this stops the ladder for a decision rather than silently continuing to A0.2: either the experimental uncertainty is re-derived from a source that reports it properly, or the gate is restated as a code-to-code verification target with the experiment carried as context. That is an owner decision, recorded here and not taken unilaterally. The A0.2 solver-regime decision (D10) remains open independently.
