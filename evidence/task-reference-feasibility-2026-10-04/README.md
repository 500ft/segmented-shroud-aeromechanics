# Reference feasibility result

`BLOCKED_GEOMETRY`: nine blade stations and one isolated tip contour are
recoverable, but the inspected sources do not define a complete rotor and duct
assembly. The executed [comparison](geometry-comparison.json) reproduces all
four preserved exports byte for byte. No CFD was run; compute capacity remains
unmeasured.

## What was executed

The [geometry record](../../data/reference/akturk-camci/geometry.json) pins the
paper URLs, retrieval dates, hashes, figure locations and extraction allowances.
Selected CSVs, the exporter and its tests were reused from the recorded WIP
commit. The papers were retrieved again and their hashes verified. The native
journal Figure 2 and its trace overlay were inspected without re-picking points.
The original preservation branch and the separate formatting commit remain intact.

[The audit script](../../scripts/audit_reference_geometry.py) independently
transforms the existing image points into a chord frame, compares regenerated
exports with the preserved hashes, and calculates the consequences of printed
precision and the quoted torque accuracy. Its output records the input hashes.
The local frame starts at the leading edge, points along the chord, and places
the image-upper contour above the image-lower contour. It does not supply the
section's position in the rotor assembly.

```bash
python scripts/export_reference_geometry.py --output-dir /tmp/shroud-reference-export
python scripts/audit_reference_geometry.py --check
python -m unittest discover -s tests -p 'test_reference_geometry.py' -v
```

The generated CSV and XYZ file use millimetres; the SVG is an inspection view.
Their sensitivity columns sample corners of declared extraction ranges. They
are neither confidence intervals nor manufacturing tolerances. Source figures,
PDFs and visual overlays remain outside git. ASME copyright applies to the
papers; an explicit data reuse licence was not found. Attribution and that
unresolved status are retained separately from the project's MIT software licence.

## What changed in the interpretation

- The nominal clearance computed from printed radii differs from the printed
  clearance label. The label falls within the half-last-digit sensitivity
  range in the comparison result. Rounding can explain this discrepancy;
  an exact manufacturing clearance still cannot be inferred.
- The metric and inch tip thicknesses disagree. The comparison retains both
  and reports the difference without choosing one.
- Conference Figure 5 contains a scaled meridional mesh view. It constrains
  part of the duct shape, which the earlier record overlooked. Complete
  contour coordinates, wall transitions and assembly datums remain absent.
- The separately plotted rotor and duct thrust in Figure 11 are computed
  components. They do not provide independently measured component validation.
  The rotor-only experiment uses a different assembly.

## Reference comparison inputs

[reference.json](reference.json) is the source for the inspected uncertainty
values, their definitions, operating speeds and endpoint conventions. Quoted
force and moment accuracy has no stated confidence or coverage factor. The
reported random pressure-coefficient uncertainty does not supply the missing
thrust or power uncertainty. Pressure acquisition duration also cannot be
assigned to the force/torque measurements.

Shaft power is `Q * Omega`, with angular speed in rad/s. The comparison computes
only the power sensitivity to quoted torque accuracy with speed held exact.
RPM uncertainty, repeatability, covariance and the full measurement uncertainty
remain unreported. The existing electrical-input analysis uses a different
endpoint and supplies no CFD shaft-power result.

The nominal facility speed differs from the plotted reference speeds. Pressure
profiles and performance curves have different operating-point information;
no CFD comparison point has been selected. Clearance is normalized by blade
height, while thrust and power coefficients use casing inner diameter. Total
thrust requires the same included bodies and tare convention as the source rig.

This is a development audit. No final-test evaluation, data split, fitted
performance model or acceptance threshold was introduced. A future reference
comparison must carry experimental, digitization, geometry and numerical
uncertainties, with correlations where known. A seam result remains unresolved
if its comparison uncertainty cannot distinguish it from the smooth case.

## Missing inputs and conditional compute route

The precise geometry gaps and required source material are in
[geometry.json](../../data/reference/akturk-camci/geometry.json), under
`missing_geometry`: lower-span blade coordinates and stacking/root definitions;
complete duct contour and assembly placement; exposed hub, motor and supports;
and clarification of conflicting dimensions. New source coordinates or a
separately approved approximate study would change the mesh verdict.

OpenFOAM is the preferred route once those inputs exist. Neither the earlier
airfoil tutorial nor available CPU counts measure the cost of this rotor case.
No mesh size, RAM, wall time or convergence result is asserted here.

[NYU access findings](nyu-access.json) link the official account, software and
container documentation. The current pages describe Torch; Greene availability,
project sponsorship/allocation and OpenFOAM support are unverified. Generic
Apptainer support establishes only a possible route. The file contains an
unsent PI sponsorship question. No account request, login or job was attempted.

## Reproduce and explain

Run the comparison command above. Derive the torque-only power sensitivity
from the recorded angular speed and instrument accuracy, then explain which
missing terms prevent calling it a complete power uncertainty. Use the
matched-thrust interpolation formula in `reference.json` to explain why each
geometry needs its own bracketing thrust points. There is no shroud convergence
plot to assess yet.
