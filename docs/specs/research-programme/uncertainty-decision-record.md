# Uncertainty decision record

Status: decision, 2026-09-19. Supersedes decision **D4** of the [work order](plan.md) as it was merged in PR #20. Applies to every CFD result the programme produces.

## What this corrects

PR #20's D4 defined a single band

    U = sqrt(GCI^2 + clocking^2 + model^2)

and used it both as the validation comparison band and as the Study A decision band. That is not defensible, for two separate reasons, and the review handoff of 2026-09-19 was right to flag it.

1. **The three terms are not the same kind of quantity.** A grid-convergence index is an estimate of discretisation *uncertainty* and carries an intended coverage interpretation. The spread between two turbulence models is a *discrete sensitivity* over two modelling choices, with no distribution and no sample. The spread over rotor clocking positions is a *deterministic physical sensitivity*: each clocking position is a different configuration, not a repeated measurement of one configuration. Adding them in quadrature asserts independence and randomness that none of them has, and reporting the result as if it were a confidence interval overstates what is known.
2. **One band cannot do two jobs.** Comparing a simulation against measured data and deciding whether a seam effect is resolvable are different questions with different error structures. The first needs experimental uncertainty in it; the second has no experiment in it at all.

## Decision

### Band 1 — validation comparison, `U_val`

Used only where measured data exist (A0.1, A0.2, and any later validation rung).

    E      = S - D                                   comparison error, simulation minus data
    U_val  = sqrt(U_num^2 + U_input^2 + U_D^2)

- `U_num` — numerical uncertainty from the grid-convergence procedure of Celik et al. (ASME J. Fluids Eng. 130(7), 2008): at least three systematically refined grids, refinement ratio at least 1.3, observed order of convergence computed rather than assumed, factor of safety 1.25 where the observed order is close to formal.
- `U_input` — uncertainty from inputs that are derived or assumed rather than verified. Where an input is labelled `DERIVED_FROM_SOURCE` or `ASSUMED_FOR_MESH_ONLY` in the [source inventory](../../../evidence/task-a0-validation/source-inventory.json) and its influence has not been quantified, `U_input` is reported as **unquantified**, never as zero.
- `U_D` — experimental uncertainty as reported by the source. Where the source does not report it, `U_D` is **unquantified** and the verdict is downgraded accordingly (see below).

Quadrature is justified here because all three are uncertainty estimates about independent error sources.

**Verdict vocabulary.** `VALIDATED_AT_U_VAL` when `|E| <= U_val` and every component of `U_val` is quantified. `NUMERICALLY_BOUNDED` when `|E|` is within the numerical band but `U_D` or `U_input` is unquantified, so a full validation statement is not available. `NOT_VALIDATED` when `|E| > U_val`. `INCONCLUSIVE` when convergence is non-monotonic or the observed order is not usable. A result may never be reported as "CFD validated" without the rung's scope qualifier.

### Band 2 — Study A decision envelope, `E_dec`

Used where no measured data exist and the question is whether a configuration difference is resolvable. There is no experiment in this comparison, so it is not a validation band and is never called one.

    E_dec = U_num(delta) + R_clock + R_model            linear, worst case

- `U_num(delta)` — numerical uncertainty **computed on the difference itself**, not on the two absolute values. Configurations sharing a mesh family, solver and settings share part of their discretisation error, which cancels in the difference. Estimating `U_num(delta)` as `sqrt(2) * U_num(P)` would therefore be wrong in the conservative direction and would hide a real effect. The grid study is run on the control and on at least one seam configuration and the index is computed on the difference.
- `R_clock` — the full range of the difference over the declared rotor clocking positions. Reported as a range, not a standard deviation. No distribution is asserted over clocking angle.
- `R_model` — the range of the difference over the declared turbulence models. Reported per model as well as as a range.

The terms are added **linearly** because the last two are deterministic sensitivities with no justified distribution. Linear addition is deliberately conservative; it is the price of not inventing a probability model. A narrower combination becomes available only if a future record declares and defends a distribution for clocking and a model-form weighting, and that record must exist before the band is narrowed, not after a result is seen.

**Decision rule.** A seam effect is `RESOLVABLE` only if `|delta| > E_dec`. Otherwise the result is `NOT_RESOLVABLE_AT_THIS_FIDELITY`, which means this mesh, solver and model set cannot separate the effect from its own sensitivities. It does **not** mean the physical effect is absent, and no sentence in this repository may report it that way.

### Reporting rule

Every CFD report states `U_num`, `U_input`, `U_D`, `R_clock` and `R_model` **separately and with units** before any combined band is quoted. A reader must be able to recompute both bands from the reported components. Turbulence-model results are reported per model; they are never averaged.

## Consequences for the current work order

- D4 of the work order is superseded by this record.
- A0.1: `U_D` for forces comes from the Ladson tripped dataset if the source reports it; if not, A0.1's best available verdict is `NUMERICALLY_BOUNDED`.
- A0.2: the source inventory records that no experimental uncertainty was located in the retrieved text, so A0.2's ceiling verdict is `NUMERICALLY_BOUNDED` until that is found.
- Study A remains blocked until this record is in force, which it now is, and until the remaining release-gate conditions in the work order are met.

## Amendment, 2026-09-24

An external review found that this record was applied incorrectly, and in one place stated
incorrectly. Four changes, none of which rewrites the original decision above.

**An unquantified component may not be dropped.** The record said `U_input` is "reported as
unquantified, never as zero", and then the implementation combined the remaining terms and
called the result `U_val`. Combining only what is known *is* setting the unknown to zero. Where
any required component is unquantified, `U_val` is **null**, the missing components are named,
and the combination of the known terms is reported under its own name so it cannot be mistaken
for a complete validation uncertainty.

**Spread across treatments is not repeatability.** A0.1's `U_D` came from the spread across
three grit conditions. Those are different boundary-layer trips, that is different experimental
conditions, not repeated measurements of one. That spread is **treatment sensitivity**. The
individual comparator values are preserved rather than collapsed, and any interpolation or
incidence adjustment used to reach a common angle carries its own unquantified uncertainty.

**Every combined term needs its measurement model stated.** For each contribution: the measurand,
the sensitivity coefficient, whether it is standard or expanded, its coverage convention and any
covariance assumption. A grid-convergence index with a safety factor is not automatically a
one-standard-deviation quantity, and combining it in quadrature with something that is requires
saying so.

**`|E| ≤ U_val` is this project's consistency screen, not a universal pass or fail.** A wider
band must never make a less informative computation look more accurate. A separate
fitness-for-purpose tolerance, if one is wanted, is declared prospectively and on its own terms.

**Unestimated is not zero, for model spread either.** Where only one turbulence model is usable,
the model-form range is reported as unestimated rather than 0.0, and the incomplete arm stays
visible without being accepted.
