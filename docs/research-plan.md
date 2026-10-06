# Research Plan

> Project closed at owner request. The material below is retained history;
> unfinished tasks and input requests are discontinued. See the [closure record](../ROADMAP.md).

## Position

Ducted-fan tip clearance, non-axisymmetric casing distortion, deployable structures, self-locking mechanisms, and rotor guards are established research areas. This project does not claim any of those ingredients as new.

The candidate contribution is their deployment-specific causal chain at small-UAV scale:

\[
\text{closure and joint variation}
\rightarrow
\text{seams, steps, ovality, and clearance harmonics}
\rightarrow
\text{dynamic minimum clearance}
\rightarrow
\text{rubbing risk and thrust-per-power}.
\]

## Unit of analysis

Each experimental identity is:

> shroud specimen + closure mechanism + deployment cycle + environmental condition + rotor operating point

Repeated cycles from one specimen are repeated measures, not independent specimens.

## Research questions

### RQ1 — Defect topology

At equal mean clearance, do ovality, seam openings, or radial steps cause different aerodynamic or rubbing outcomes?

### RQ2 — Model value

Does a defect-aware model predict a held-out defect family better than a model using only mean clearance?

### RQ3 — Mechanism propagation

How do closure preload, centering behavior, and joint tolerances change the distribution of deployed defect fields?

### RQ4 — Joint yield

What fraction of deployments simultaneously lock, preserve safe dynamic clearance, and retain positive thrust-per-power benefit?

## Falsifiable hypotheses

- **H1:** At equal mean clearance, at least one deployment-specific defect produces a response difference greater than measurement uncertainty.
- **H2:** A defect-aware model reduces held-out prediction error relative to a mean-clearance baseline.
- **H3:** A self-centering, preload-controlled closure reduces deployment-to-deployment radial reconstruction variance relative to an ordinary over-center closure at matched mass and nominal geometry.
- **H4:** Within a registered operating envelope, the joint aero-mechanical yield can be estimated with uncertainty narrow enough to assess performance-duct qualification. Protective-guard qualification is a separate hypothesis requiring independent impact, containment, deflection, deployment and aerodynamic-penalty evidence.

Any hypothesis may fail and remains in the report.

## Yield definition

The component-level outcome is:

\[
Y_{AM}=P(D\cap L\cap C\cap A),
\]

where:

- \(D\): deployment completes,
- \(L\): the interface remains locked through the proof-load condition,
- \(C\): dynamic minimum clearance exceeds the registered safe clearance,
- \(A\): thrust-per-power exceeds the registered reference condition.

Mass, packed volume, deployment time, impact protection, acoustic emissions, and vehicle endurance are reported separately. They are not silently folded into the yield definition.

## Primary observables

- Circumferential clearance field \(c(\theta)\)
- Dynamic minimum clearance \(c_{min}(t,\mathrm{RPM},T)\)
- Seam opening, local step, two- and three-lobe harmonic amplitudes
- Latch preload and deployed-ring stiffness
- Deployment success and lock retention
- Thrust, RPM, voltage, current, electrical power, and temperature
- Vibration and any rubbing/contact event

## Minimum comparison set

1. Open rotor
2. Monolithic reference duct
3. Adjustable rigid duct with uniform clearance
4. Adjustable rigid duct with equal-mean-clearance ovality
5. Adjustable rigid duct with a seam or local radial step

The deployable mechanism is not part of the minimum aerodynamic experiment. It proceeds only if defect topology matters.

## Analysis principles

- Qualify the measurement system before testing the hypothesis.
- Compare at matched thrust; report electrical and aerodynamic quantities separately.
- Randomize condition order and record warm-up and temperature.
- Use specimens as independent experimental units and cycles as repeated measures.
- Hold out a defect family, not merely random rows from the same condition.
- Report model calibration and uncertainty, not only point prediction error.
- Freeze final acceptance thresholds after a pilot; exclude pilot observations from confirmation.

### Model-identifiability gate before family holdout

Register the predictor basis, training support and prediction-error denominator
before choosing the held-out family. A seam-only predictor that is zero in every
training condition has an unidentified empirical coefficient; a held-out seam
test cannot validate a coefficient that was never estimated.

For empirical models, cover every fitted descriptor in training and hold out
specified combinations, amplitudes or specimens. Claim whole-family transfer
only when a preregistered physical model constrains the unseen mechanism, or
explicitly report the family as an extrapolation challenge with its parameter
identifiability limitation. Do not relabel a random-row split as family holdout.
If neither route is justified, stop the transfer claim and report within-support
prediction only. This gate must close before confirmatory data are generated.

Primary percentage prediction error means absolute electrical-power prediction
error divided by observed electrical power at matched thrust, aggregated first
by independent specimen and then by held-out condition. Define operating-point
weights prospectively. It is not error divided by a potentially near-zero duct
benefit. Relative model improvement uses the same endpoint and is undefined when
the mean-clearance baseline error is zero.

## Scope

### In the minimum publishable core

- One rotor scale and operating envelope
- Rigid, adjustable defect geometry
- Uniform, harmonic, seam, and step defects
- Mean-clearance and defect-aware predictive models
- Held-out defect-family validation
- Honest null result if mean clearance is sufficient

### Outside the minimum core

- Free-flight integration
- In-flight transformation
- Full annular-wing aircraft
- Acoustics as a headline contribution
- Universal duct infeasibility claims
- Second-scale validation unless time and facilities permit

## Honest outcomes

- **Performance-duct path:** deployment and lock succeed, clearance remains safe, and positive aerodynamic benefit survives with adequate yield.
- **Guard path:** structure deploys and protects reliably, but aerodynamic benefit is absent or insufficient. This requires separate impact and penalty tests.
- **Simpler-model result:** mean clearance explains the tested response; deployment-specific defect descriptors add little.
- **Nonviable mechanism:** closure variation or dynamic deformation makes the safe operating envelope impractically small.
