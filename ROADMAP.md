# Research Roadmap

The project advances only when the preceding measurement or model gate closes.

## Stage 0 — Research contract

**Status:** complete for the concept repository.

- Define the segmented-shroud causal chain.
- Separate established clearance and deployable-mechanism research from the candidate gap.
- Register hypotheses, baselines, observables, and failure branches.
- Define specimen and data manifests.

**Exit gate:** a cold reader can distinguish planned work from evidence and identify the smallest experiment that could reject the direction.

## Stage 1 — Measurement-system qualification

**Status:** not started. A [measurement-requirements draft](docs/measurement-system-spec.md) exists with its inputs open; no channel has been calibrated or qualified.

- Establish clearance resolution and repeatability.
- Calibrate thrust, voltage, current, RPM, and temperature channels.
- Quantify stand drift, warm-up behavior, and alignment uncertainty.
- Complete guarded low-energy commissioning.

**Exit gate:** measurement uncertainty is smaller than the minimum defect and performance difference the experiment is intended to resolve.

## Stage 2 — Adjustable rigid defect duct

**Status:** blocked on Stage 1.

- Compare open rotor, monolithic duct, and adjustable rigid duct.
- Test uniform clearance, two-lobe ovality, seam opening, and local step conditions.
- Randomize condition order and compare at matched thrust.
- Close the model-identifiability gate in docs/research-plan.md before choosing a family holdout. Distinguish supported empirical interpolation from physically constrained extrapolation.

**Exit gate:** a defect-aware model improves held-out error by at least 20% over a mean-clearance model and reaches below 10% prediction error.

**Failure branch:** if topology adds no value beyond uncertainty, publish the simpler mean-clearance tolerance result and stop deployable-mechanism integration.

## Stage 3 — Closure-mechanism repeatability

**Status:** blocked on Stage 2.

- Compare an ordinary over-center closure with a self-centering, preload-controlled interface.
- Match nominal geometry and ring mass.
- Measure deployment success, preload, seams, ovality, energy barrier, stiffness, and proof-load margin.
- Treat specimens—not cycles—as the primary independent units.

**Exit gate:** the mechanism changes the defect distribution enough for the Stage 2 model to predict a meaningful yield difference.

## Stage 4 — Coupled aero-mechanical yield

**Status:** blocked on Stage 3.

- Freeze the defect-to-performance model.
- Predict held-out mechanism specimens or an unseen defect family.
- Estimate deployment, lock, clearance, performance, and joint yield with uncertainty.
- Assess performance-duct qualification under registered aero-mechanical criteria. Failed aerodynamic qualification leaves protective performance unknown.

**Independent guard gate:** a protective-guard label requires separate registered
impact, containment, deflection, deployment/lock and power-penalty tests. Those
tests may be deferred only if the guard claim is also deferred. An aerodynamic
null result does not establish protection.

## Stage 5 — Optional extensions

These do not block the minimum publishable core:

- Second rotor scale
- Thermal and vibration aging
- Guard impact and blade-containment testing (optional project extension; mandatory before any protective-guard claim)
- Acoustics
- Free-flight integration
- In-flight transformation
