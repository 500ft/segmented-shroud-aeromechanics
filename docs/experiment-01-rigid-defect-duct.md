# Experiment 01 — Adjustable Rigid Defect Duct

## Objective

Determine whether deployment-like defect topology carries predictive information beyond average rotor-tip clearance.

This experiment intentionally excludes a deployable mechanism. It isolates the aerodynamic premise before mechanism complexity is introduced.

## Hypothesis

At equal mean clearance, a two-lobe distortion or discrete seam produces a repeatable change in thrust-per-power or dynamic minimum clearance greater than measurement uncertainty.

## Timebox

One to two weeks after the rotor stand, sensors, and containment system pass commissioning.

## Stage A — Measurement-system qualification

Before collecting hypothesis-test data:

- Calibrate thrust and electrical measurements over the intended range.
- Estimate clearance measurement bias, repeatability, and resolution.
- Record stand drift through warm-up and repeated reference runs.
- Confirm RPM, temperature, and vibration synchronization.
- Establish that the containment system does not interfere with the measured inlet condition.

If measurement uncertainty is not smaller than the minimum effect of interest, the experiment stops for instrumentation redesign.

The [measurement-system requirements draft](measurement-system-spec.md) states these requirements channel by channel with every unresolved input assigned; it is a draft with open inputs, not an installed qualification result.

## Stage B — Pilot conditions

Use interchangeable rigid inserts to create:

1. Uniform reference clearance
2. Two-lobe clearance variation with the same mean clearance
3. One discrete seam opening with the same mean clearance

Include open-rotor and monolithic-duct reference conditions. Randomize condition order within operating blocks.

## Variables

| Type | Variables |
| --- | --- |
| Deliberately varied | Duct condition, defect family, defect amplitude, matched-thrust operating point |
| Measured | Circumferential geometry, minimum dynamic clearance, thrust, RPM, voltage, current, temperature, vibration, rubbing/contact |
| Held constant | Rotor, motor, controller, nominal duct profile, inlet arrangement, sensor locations, and analysis procedure |

## Comparison basis

The primary aerodynamic comparison is electrical power required at matched thrust. RPM-matched results may be reported as a secondary diagnostic but do not substitute for the matched-thrust comparison.

## Analysis

- Fit a mean-clearance baseline model using training conditions.
- Fit a defect-aware model using mean clearance plus registered seam and harmonic descriptors.
- Before family holdout, close the model-identifiability gate in docs/research-plan.md: fitted descriptors need training support; an unseen mechanism requires a specified physical extrapolation model. Otherwise restrict the claim to supported conditions.
- Compare held-out prediction error and interval coverage.
- Report response differences relative to measurement uncertainty.
- Inspect residuals by temperature, operating point, and randomized test order.

Prediction error is normalized by observed electrical power at matched thrust,
not by the small difference between duct and open-rotor performance. Register
specimen-level aggregation and operating-point weights before confirmation.
If the mean-clearance baseline error is zero, relative improvement is undefined,
not an infinite gain. No protective-guard conclusion follows from this experiment.

## Provisional engineering gates

- **Continue to mechanism work:** defect-aware held-out error is below 10% and at least 20% lower than the mean-clearance baseline.
- **Repeat or redesign instrumentation:** observed differences are comparable to measurement-system uncertainty.
- **Pivot:** defect descriptors do not improve held-out prediction; publish the simpler tolerance finding and stop mechanism integration.

These thresholds are project gates, not achieved outcomes. Final confirmatory thresholds are frozen only after the pilot and before new validation data are collected.

## Safety controls

- Structurally rated rotor enclosure and debris containment
- Remote arming, emergency stop, and current protection
- Low-energy commissioning before full operating points
- Verified static clearance before every condition
- Exclusion zone, eye protection, and hearing protection
- Predefined abort thresholds for vibration, temperature, current, and rubbing
- Facility approval and named test operator

No rotor test begins from this document alone; a site-specific risk assessment and operating procedure are required.
