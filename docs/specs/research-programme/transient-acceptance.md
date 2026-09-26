# Transient confirmation: acceptance specification
Date: 2026-09-25 · Review item R09 · Ledger row SSY-R17

Registered before any transient case is run. The decision branches are implemented in
`scripts/transient_acceptance.py` and exercised on synthetic inputs in
`tests/test_transient_acceptance.py`, so the rules are executable rather than only written down.

Writing this specification validates nothing. It fixes what would count as evidence.

## 1. Estimand

`ΔP_shaft` at matched **time-averaged total assembly thrust** `T*`, with the rotor and duct
force contributions retained separately and summed, against one declared force boundary. The
averaging window and the thrust-matching procedure must be identical across configurations, or
the difference is between two different things.

`P_shaft = Q·Ω` and `P_electrical = mean(V·I)` stay distinct quantities. They may be compared
only with a stated treatment of motor and controller losses over speed, torque and temperature.
A single constant efficiency does not transfer between matched-thrust settings.

## 2. Phase interval

Derived from the full rotor, duct and support geometry with its boundary conditions, not
inherited. **A0.2's periodic sector does not carry over**: an axisymmetric benchmark's symmetry
is not the symmetry of a duct carrying one seam or an incompatible seam pattern. Where a smaller
interval cannot be justified from the actual geometry, the interval is a full revolution.

## 3. Phase sampling refinement

Nested 4, 8 and, if needed, 16 positions over that interval. The phase-averaged endpoint and its
extrema are compared as sampling is refined. **Four frozen positions are an initial budget, not
a converged time average**, and a single sampling level demonstrates nothing.

## 4. Case selection

The reference, the consequential non-zero screening case, and where resources allow a case near
the decision boundary. The selection rule is committed **before** screening outcomes are seen.
Where only one defect can be confirmed, that limit is recorded with the result.

## 5. Time resolution

Set from the narrowest **seam encounter duration**, the blade passing period, interface and
Courant constraints, and the quantities being resolved. A universal steps-per-blade-passage
figure is an initial choice, not an acceptance criterion: a narrow seam is encountered far
faster than a blade passes.

## 6. Convergence

Demonstrated, not assumed, across successive time-step levels and post-transient averaging
windows: cycle-to-cycle drift in force and torque, the matched-thrust residual, and interface
conservation. Numerical convergence and statistical sampling precision are separate claims, and
correlated time steps within one run are not independent repeats.

## 7. Tolerances

Absolute, in units, allocated prospectively from the decision-relevant effect size. That size
depends on owner inputs that do not exist, so this specification is **complete while its
numerical acceptance is `TOLERANCE_NOT_FROZEN`**. The classifier refuses to decide anything
without a registered tolerance, which is what prevents an attractive percentage being chosen
after the result is seen.

## 8. Interpretation

Three outcomes, no fourth:

- **Steady trend supported over the tested cases**, when the transient mean agrees within the
  registered tolerance. The qualifier is part of the claim.
- **Steady trend overturned**, when the transient mean differs beyond tolerance, or when it
  reverses the sign of the difference at any magnitude.
- **Unresolved**, when the numerical evidence is unusable, or when the effect lies inside its own
  sampled uncertainty. An effect smaller than its uncertainty is not evidence that seam topology
  does not matter.

## 9. The envelope is not a bound

`U_num(Δ) + R_clock + R_model` summarises the choices that were sampled. It is reported with its
components kept separate and is **never** described as a worst case on physical model error or as
a confidence interval. Interactions can exceed an additive main-effect construction, and bias
shared by every model sampled is invisible to it. Error cancellation in a paired difference is a
possibility to investigate, not a property to assume.

## 10. Cost

Estimated by summing measured memory and wall time per case over the grid levels, model variants,
phase positions, operating points and thrust iterations actually planned, plus transient averaging
periods and restarts. A0.1 timings are a smoke test, not calibrated throughput for a full-annulus
moving-mesh rotor, and old laptop figures are not schedule evidence.
