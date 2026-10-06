# A0.1 validation report — 2D NACA 0012

Status: Spalart–Allmaras arm complete, 2026-09-20. Work order: [plan](specs/research-programme/plan.md) task T06. Acceptance was frozen before any solution existed in [a01-acceptance.json](../evidence/task-a0-validation/a01-acceptance.json); the uncertainty treatment is the [uncertainty decision record](specs/research-programme/uncertainty-decision-record.md). Original numerical outputs are in [uncertainty.json](../results/generated/cfd/a0.1/uncertainty.json) and the per-case manifests beside it. Current interpretation follows the [uncertainty revision](../results/generated/cfd/a0.1/uncertainty.revision-2026-09-25.json) and [status revision](../results/generated/cfd/a0.1/status-revision-2026-09-29.json). Those revisions preserve the original files.

> **Correction, 2026-09-24.** An external review reproduced three errors in the interpretation below. They are corrected in place and the original calculations are preserved: no run, raw output or frozen acceptance record was changed. (1) The stated `U_val` combined only the known terms while a required component was unquantified, which treats an unknown as zero. (2) The spread across grit treatments was called repeatability; the grit sizes are different experimental conditions, not repeats of one. (3) The asymptotic-range ratio was presented as confirmation; it is algebraically `|phi_fine/phi_medium|` and confirms nothing. A fourth error, a universal "2 percent floor" for seam effects, is withdrawn in section 7.

**Verdict, Spalart-Allmaras: `INCOMPLETE_UNCERTAINTY`.** Both `U_input` and
experimental `U_D` are unquantified in the revision. The grit-treatment spread
cannot supply experimental standard uncertainty. Only `U_num` remains in the
eligible partial combination; no complete `U_val` exists.

The separate code comparison is agreement with the CFL3D Spalart-Allmaras
reference lift coefficient after the incidence adjustment in section 5. Other
reference computations have different discrepancies.

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

**The safety factor is a sourced assumption whose condition was not checked.** Celik et al. prescribe 1.25 where the observed order is close to the formal order. The observed order here is 2.6697 against a formal order near 2, and the procedure does not limit it. Across the defensible combinations the fine-grid index is 0.153 % as reported, 0.368 % at a factor of 3.0, 0.274 % with the order limited to 2, and 0.658 % with both. The comparison error below is 2.22 % of the reference, between 3.4 and 14.5 times the index across those choices, so **no combination changes the conclusion of this case**. Registered as [`GCI-SAFETY-FACTOR`](canonical-quantities.json); the arithmetic is in the [provenance audit](number-provenance-audit-2026-09-25.md) and is recomputed from the committed record by `tests/test_canonical_quantities.py`.
The numerical term is `U_num_absolute` in the linked result record.

The apparent order sits slightly above the formal second order of the schemes, which is ordinary on a systematically refined structured family, and the convergence is monotonic.

**The asymptotic-range ratio confirms nothing and no longer gates anything.** With equal refinement ratios and the order fitted from the same three values, `r^p = |(phi3−phi2)/(phi2−phi1)|` identically, and the ratio then reduces algebraically to `|phi_fine/phi_medium|`. The reported 1.00662 is exactly the fine-to-medium lift ratio, which a test now demonstrates. One three-grid set gives two *adjacent* pairs, not two independent triplets. Establishing asymptotic behaviour would need a further refinement level and stability across overlapping triplets, together with iterative-error, domain-extent and wall-treatment checks. The three-grid estimate is retained with its assumptions stated, and nothing here claims more than that.

## 4. Validation comparison

Reference: TMR's curated Ladson tripped data at Re 6 × 10⁶, M 0.15, the three grit conditions adjusted to 10.12° with the dataset's own lift-curve slope of 0.10077 per degree. Mean 1.07502, sample standard deviation 0.00441.

The [current revision](../results/generated/cfd/a0.1/uncertainty.revision-2026-09-25.json)
retains the comparison error `E = S - D` and numerical term. It records both
`U_D` and `U_input` as null, so `U_val` and `abs_E_le_U_val` remain null. The
previous combination of numerical uncertainty and grit-treatment spread is
preserved under `partial_combination_of_known_terms_superseded`; it cannot
serve as the comparison interval. The eligible partial combination is now
`U_num` alone. An unquantified term cannot be assumed to be zero.

**The 0.00441 term is reclassified.** It was described as trip repeatability. The 80, 120 and 180 grit conditions are *different boundary-layer trips*, that is different experimental conditions, not repeated measurements under identical conditions. Their spread is **treatment sensitivity**, and the individual comparator values are preserved rather than collapsed into one number. Whether it also bounds measurement repeatability is unknown, and any interpolation or incidence adjustment applied in reaching a common angle carries its own uncertainty that has not been quantified.

The rule `|E| ≤ U_val` is this project's **consistency screen**, not a universal pass or fail. A wider band must never make a less informative computation look more accurate.

`U_input` remains unquantified. Specified geometry and nominal conditions do not determine the uncertainty of comparing this computation with the experiment.

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

The spread between the reference codes is a code/model sensitivity. It cannot be expressed as a multiple of `U_val`, which remains unknown.

## 5a. k-ω SST arm: incomplete, no verdict

Two of three levels completed. The fine grid was stopped at iteration 117 of 6,000 because the host had 63 MB of free memory and was swapping; the container was using 97 MB of its 3 GB limit on one saturated core, and the case was running at roughly 0.15 iterations per second against 4.6 for the same mesh under Spalart–Allmaras. That is a thrashing signature, not the cost of two extra transport equations, so it is recorded as host resource exhaustion rather than a solver or setup failure. The original manifest records `UNCONVERGED`; the [status revision](../results/generated/cfd/a0.1/status-revision-2026-09-29.json) corrects this to `TERMINATED_BEFORE_ASSESSMENT`, because the run was shorter than the assessment window. It remains excluded from the convergence and validation comparison.

| grid | cells | iterations | Cl | Cd | status |
| --- | ---: | ---: | ---: | ---: | --- |
| coarse | 3,584 | 3,000 | 1.133621 | 0.003532 | PASS |
| medium | 14,336 | 4,000 | 1.105396 | 0.009416 | PASS |
| fine | 57,344 | 117 | — | — | TERMINATED_BEFORE_ASSESSMENT, excluded |

**No grid-convergence index and no verdict are issued for SST**, because the procedure needs three converged levels and there are two.

The completed coarse and medium SST values differ substantially, particularly
in drag. Under-resolution is a possible explanation, but these runs do not
isolate grid, wall-treatment and setup effects. They provide no converged SST
estimate or completed comparison of model sensitivity.

No restart is authorized by this report. The [roadmap](../ROADMAP.md) sets current work.

## 6. What the verdict means

The code comparison in section 5 supports the airfoil workflow at the stated
conditions. Agreement with another code does not prove that setup errors are
absent. The observed experimental discrepancy remains unresolved because the
required experimental and input uncertainties are missing.

The comparison table also rules out the earlier claim that every reference
code misses the experiment by more than this work does. The SST reference
results have smaller discrepancies. Neither that ranking nor the spread
across codes identifies the cause of the disagreement.

The old experimental term describes changing the trip treatment. It is not a
bound on measurement uncertainty and excludes tunnel, incidence and support
effects. The existing revision withdraws its use as `U_D`; no acceptance band
has been widened after seeing the result. No model-error floor for a shroud
power difference follows from this airfoil comparison.

## 7. Consequence for the programme

**The universal "2 percent floor" asserted here is withdrawn.** The earlier text said that a seam effect below roughly 2 percent could not be separated from model-form error by this class of simulation, at any mesh density, and that figure propagated into the design contract and the literature review.

The inference does not hold. This report observes a discrepancy in **absolute lift on a two-dimensional airfoil** at one condition. A seam study reports a **difference in ducted-rotor power between two configurations**. Those are different quantities, different geometry and different operating conditions. Errors in a paired comparison may cancel, differ or compound, and cancellation has to be investigated rather than presumed. Two turbulence models cannot bound every shared modelling error either.

What survives is a requirement, not a number: **Study A must estimate the numerical and model sensitivity of the paired difference it will actually report, at its own conditions**, before its amplitudes are frozen. The rig's floor comes from its own budget. Neither may be inherited from this case.

## 8. Limitations and claim boundary

- A0.1 exercises a two-dimensional airfoil workflow at one condition. It supplies numerical evidence for that workflow and a comparison against published computations. The comparison against the experiment is unresolved, because a required uncertainty component is unquantified. It says nothing about rotating-frame loading, three-dimensional flow, ducts or tip gaps.
- Drag is reported, not gated, for the reasons frozen in the acceptance file. On the finest grid Cd = 0.012031 against a tripped experimental 0.01201 at the 80-grit condition; the agreement is closer than lift, but the tripping and Reynolds systematics the source warns about are unquantified here, so no drag claim is made.
- Skin friction was computed but cannot be validated: the source states no experimental data exist.
- Both `U_input` and experimental `U_D` are unquantified, so no complete validation uncertainty exists for this case.
- The asymptotic-range ratio is a diagnostic with a known algebraic identity, not evidence.
- The 0.00441 term is a sensitivity to the grit treatment, not `U_D`. It is neither an upper nor a lower bound on experimental uncertainty, and no experimental standard uncertainty is available for this case.
- The k-ω SST arm is incomplete (two of three levels), so it carries no index and no verdict. The model-form sensitivity **for this work** is therefore unmeasured; only the published reference spread is available, and its individual computed values do not supply a completed model-sensitivity comparison.

## 9. Next gate

A0.1 does not pass its gate as written. Under the work order this stops the ladder for a decision rather than silently continuing to A0.2: either the experimental uncertainty is re-derived from a source that reports it properly, or the gate is restated as a code-to-code verification target with the experiment carried as context. That is an owner decision, recorded here and not taken unilaterally. The A0.2 solver-regime decision (D10) remains open independently.
