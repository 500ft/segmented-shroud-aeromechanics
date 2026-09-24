# Design contract — Experiment 01 reference geometry, defect basis and comparison conditions

Status: **draft, 2026-09-22. Not frozen.** Backlog task SSY-03. This document is the contract the backlog asks for; it becomes a freeze only when the open inputs in §9 are closed and it is re-issued as `frozen`.

Governing documents: [research plan](research-plan.md), [Experiment 01 protocol](experiment-01-rigid-defect-duct.md), [measurement requirements](measurement-system-spec.md), [claim ledger](claim-ledger.md). Geometry that this contract specifies is realised under [CAD_PLAN.md](CAD_PLAN.md), whose tasks remain deferred.

**What this contract is for.** Uniform gap, ovality, seam and radial step are currently words. This turns them into equations with datums, tolerances and invalid-condition rules, so that one experiment changes topology while mean clearance and the reference conditions stay controlled.

## 1. The two rotors are not the same machine

This has to be said first, because it is the most likely source of a wrong claim later.

| | Study A, computational | Experiment 01, physical |
| --- | --- | --- |
| rotor | Caradonna–Tung, radius 1.143 m, chord 0.1905 m, two untwisted NACA 0012 blades | small-UAV scale, **not yet chosen** (open input IN-04) |
| why that rotor | it is the most reproduced hover-rotor validation case, so A0.2 validation transfers to it (work-order decision D3) | the project's distinctiveness rests on small-UAV ducted rotors, and on measurement rather than simulation |
| tip Reynolds number | order 10⁶ | order 10⁴–10⁵ |

**Consequence.** A Study A effect size is not a prediction of the Experiment 01 effect size. The two differ by one to two orders of magnitude in Reynolds number, and tip-leakage behaviour is Reynolds-sensitive. Study A can establish whether seam topology matters **in the computed configuration** and can rank descriptors; it cannot supply a number the rig should expect. Any sentence that carries a Study A magnitude into an Experiment 01 expectation without a stated scaling argument is prohibited by the [claim ledger](claim-ledger.md)'s evidence-state vocabulary, because it would present CFD evidence as measured evidence.

This contract therefore defines the geometry **parametrically in the rotor tip radius**, so the same equations serve both machines and neither inherits the other's numbers.

## 2. Coordinate system, datums and angular zero

- **Datum A**, rotor axis of rotation.
- **Datum B**, the rotor plane: the axial station of the blade-tip leading-edge/trailing-edge mid-chord at zero collective, normal to Datum A.
- **Datum C**, angular zero: a physical fiducial on the duct outer surface, at θ = 0, with θ increasing in the direction of rotor rotation.

All geometry is expressed in the cylindrical frame (r, θ, z) on A, B, C. Every insert carries a physical mark at Datum C, because the seam azimuth is a controlled variable and a volume check cannot detect that an insert was installed rotated.

## 3. Reference conditions

Four conditions form the reference set; every defect condition is compared against them.

| id | condition | purpose |
| --- | --- | --- |
| `REF-OPEN` | open rotor, no duct | isolates the duct's contribution |
| `REF-MONO` | monolithic duct, continuous wall, uniform clearance c̄₀ | the aerodynamic reference for every defect |
| `REF-SEG0` | segmented duct assembled with **zero** seam width and zero step | separates "assembled from segments" from "has a defect" |
| `REF-REPEAT` | `REF-MONO` re-installed after a full removal and re-fit | gives the installation repeatability that every difference is judged against |

`REF-SEG0` matters: without it, any measured difference could be attributed to segmentation as such rather than to the seam geometry under study.

## 4. Duct profile

The duct inner surface at the rotor plane has radius `R_d(θ)`. The rotor tip radius is `R_t`. Clearance is defined only where a wall exists:

```
c(θ) = R_d(θ) − R_t          for θ ∈ Ω_wall
c(θ) = undefined             for θ ∉ Ω_wall        (no wall, therefore no clearance)
```

The axial profile of the duct (inlet lip radius, diffuser angle, chord) is held constant across every condition and is **not** a variable of this experiment. It is an open input (GEO-05) and must be fixed before any insert is made, because changing it changes the baseline the defects are measured against.

## 5. Defect equations

All amplitudes are expressed as fractions of the target mean clearance `c̄₀`, which is open input IN-02.

### 5.1 Uniform reference

```
R_d(θ) = R_t + c̄₀                 →   c(θ) = c̄₀ ,  Ω_wall = [0, 2π)
```

### 5.2 Two-lobe ovality, equal mean by construction

```
c(θ) = c̄₀ + A₂ · cos(2(θ − φ₂))
```

The circumferential mean is exactly `c̄₀` because the integral of `cos 2θ` over a full turn is zero, so this family is equal-mean **analytically**, not by adjustment. Constraint `0 < A₂ < c̄₀` keeps the minimum clearance positive; the design limit is stated in §6.

### 5.3 Discrete seams

`n` seams of angular width `w`, centred at azimuths `ψ_k`:

```
Ω_seam = ⋃_k [ψ_k − w/2 , ψ_k + w/2] ,   Ω_wall = [0, 2π) \ Ω_seam
open fraction = n·w / 2π          (w in radians)
```

Over a seam there is no wall. The clearance is **undefined there, not large**: assigning a finite radius inside a seam would fabricate a measurement.

**Angular width and physical width are different quantities.** `w` is an angle; the physical gap along the wall is `g ≈ w · (R_t + c̄₀)`. A width in degrees cannot be divided by a clearance in micrometres, and every registered level records both with the radius used to convert.

**Seam count and total opening are separate variables and must not be varied together by accident.** Increasing `n` at fixed `w` also increases the open fraction, so a "count effect" measured that way is confounded with an opening effect. The design therefore carries two distinct contrasts, and neither is a substitute for the other:

| contrast | held fixed | varied | what it can support |
| --- | --- | --- | --- |
| **A — defect burden** | individual width `w` | count `n`, and therefore total opening | the practical question: what does adding seams of a given size cost? It does **not** isolate a count effect. |
| **B — redistribution at fixed opening** | total opening `n·w` | count `n`, so `w` changes with it | whether *distributing* a fixed opening differently matters. It does **not** isolate a width effect. |

Contrast **B is primary**, because the project's question is about seam topology rather than about how much wall is missing. An isolated count effect may be claimed only with a matched-distribution contrast or an explicit model, never from A alone.

**Through-wall seam versus closed recess.** A segment seam is a **through-wall opening**: it breaks azimuthal symmetry and communicates with the flow outside the duct. A circumferential casing groove is typically **axisymmetric and blind-bottomed**, communicating only with the passage. These are different boundary conditions, and the casing-treatment literature is relevant by analogy only. Geometric equivalence is not established by sharing the word "groove", and this contract does not assume it. Every registered condition states: axial extent, through-wall or blind, wall thickness, corner treatment, whether the exterior domain is included, and the sign of any step.

### 5.4 Radial step at segment joints

Segment `j` spans the wall between consecutive seams and carries its own offset `δ_j`:

```
c(θ) = c̄₀ + δ_j        for θ in segment j
```

The wall-region mean is preserved exactly when the length-weighted offsets sum to zero:

```
Σ_j  δ_j · L_j  =  0            where L_j is the angular length of segment j
```

For `n` equal segments the simplest compliant realisation alternates the offset, `δ_j = (−1)^j · s/2`, which preserves the mean exactly **when `n` is even**. For odd `n` the offsets must be solved from the constraint above and recorded per segment; they are not equal in magnitude. This is a real manufacturing consequence of choosing an odd seam count and is called out here rather than discovered at assembly.

### 5.5 Combined conditions

A condition may carry seams and a step together. Ovality and seams are not combined in the pilot, because the pilot cannot separate two simultaneous topology changes with the number of runs available.

## 6. Equal-mean construction, and which mean

**The averaging convention is open input IN-08 and it governs geometry, simulation and rig alike.** The [measurement requirements](measurement-system-spec.md#13-averaging-domain-and-the-missing-wall-rule) define three admissible treatments. Until IN-08 is decided, this contract is written against **treatment 1, wall-only mean**, as the default:

```
c̄ = (1 / |Ω_wall|) ∫_{Ω_wall} c(θ) dθ  =  c̄₀
```

Two conditions are equal-mean when their `c̄` agree within the difference uncertainty of §7 **and** their occluded fractions are either matched or their mismatch is bounded. Seam width is therefore reported as a declared nuisance variable on every seamed condition, never absorbed into the mean.

**A warning that follows from the literature.** Holding an equivalent clearance measure fixed while redistributing the gap is already published, so the [claim ledger](claim-ledger.md) forbids presenting the equal-mean method as a contribution. This contract's construction is a method for running the experiment, not a claim.

## 7. Tolerances, and the floor that sets them

Three quantities are kept separate and must never be added together or substituted for one another:

| quantity | what it is | set by |
| --- | --- | --- |
| numerical geometry tolerance | agreement between the CAD model and its own definition | the CAD acceptance contract |
| fabrication tolerance | agreement between the made part and the CAD model | the fabrication route, GEO-06 |
| measurement uncertainty | how well the built clearance field can be measured | the [budget](clearance-measurement-budget.csv), IN-06 |

**The amplitude floor, and what it is not.** Amplitude levels must be chosen so that the smallest level is expected to produce an effect the relevant study can actually resolve. That expectation does not exist yet.

An earlier draft of this contract asserted a universal floor of about two percent, taken from [A0.1](cfd-validation-a01.md)'s disagreement in **airfoil lift**. **That inference is withdrawn.** A discrepancy in absolute lift on a two-dimensional airfoil at one condition is not a bound on the smallest resolvable **difference in ducted-rotor power** between two seam configurations. They are different quantities, different geometry and different operating conditions, and errors in a paired comparison may cancel, differ or compound; cancellation has to be investigated, not presumed. Two turbulence models also cannot bound every shared modelling error.

What replaces it is a requirement rather than a number. Before Study A's amplitudes are frozen, that study must estimate the numerical and model sensitivity **of the paired difference it will actually report**, at its own conditions. For the rig, the corresponding floor comes from the budget's `k · u_c`, which is `INPUTS_PENDING`. Neither floor may be inherited from a different quantity.

## 8. Comparison conditions

- **Primary comparison: electrical power at matched TOTAL thrust.** `T*` is the **net axial force on the declared propulsion assembly**, not the force on the rotor alone. A shroud carries force itself, so two conditions matched on rotor thrust can be delivering different useful total thrust and the comparison would then be between different operating states. The contract fixes one force boundary: the assembly comprising rotor, duct and their supporting structure up to the declared tare plane, with the same load path in every condition. Any surface excluded from that boundary is named. In simulation the rotor and duct contributions are retained **separately and reported as a sum**, so the split can be inspected and a case where duct force changes while rotor thrust does not is visible rather than hidden. Each condition is iterated on rotor speed until its total thrust matches `T*` within the tolerance of GEO-08; the achieved thrust and the speed required are both recorded, and the speed required is itself a result.
- **Electrical and shaft power stay distinct.** The rig measures `P_electrical = mean(V(t)·I(t))`. Simulation yields `P_shaft = Q·Ω`. They are never substituted for one another, and if they are compared the motor and controller loss treatment across speed, torque and temperature is stated; a single constant efficiency is not transferable between matched-thrust settings. In hover, `T/P` is power loading; no propulsive-efficiency claim of the form `T·V/P` is available at zero forward speed.
- **Secondary diagnostic: matched RPM.** Reported, never substituted for the primary. Comparing at matched RPM alone can turn a changed operating point into an apparent duct benefit.
- **Operating points.** A set of matched-thrust set-points spanning the envelope, fixed in GEO-07 before any condition is run.
- **Randomised order.** Conditions are run in randomised order **within** operating blocks, with the randomisation seed recorded before the first run. Reference conditions are re-run at the start of every block, and `REF-REPEAT` at least once per campaign.
- **Replication.** Each condition is installed and measured more than once, so that installation repeatability is estimated rather than assumed. The count is GEO-09.

## 9. Open inputs

Nothing in this contract may be frozen while any of these is open. The first four already exist in the measurement requirements and are not duplicated here; they are listed because this contract cannot close without them.

| id | needed | responsible | closes when |
| --- | --- | --- | --- |
| IN-01 | minimum clearance effect of interest | Owner | sourced value in the budget register |
| IN-02 | target mean clearance `c̄₀` | Owner | sourced value in the budget register |
| IN-04 | rotor, stand and duct envelope for the **physical** experiment | Owner | dated named resources, or an explicit design-only choice |
| IN-08 | averaging convention and missing-wall treatment | Agent proposes, experiment reviewer accepts | recorded here and in the protocol before any insert is made |
| GEO-01 | seam count levels `n` | Agent proposes | registered level set with a rationale |
| GEO-02 | seam width levels `w` | Agent proposes | registered as a fraction of `c̄₀` and of the blade pitch |
| GEO-03 | radial step levels `s` | Agent proposes | registered, with the odd-`n` offset solution if applicable |
| GEO-04 | two-lobe amplitude levels `A₂` and phase `φ₂` | Agent proposes | registered |
| GEO-05 | duct axial profile: inlet lip radius, diffuser angle, chord | Owner or design reviewer | fixed drawing, held constant across conditions |
| GEO-06 | fabrication route and its tolerance | Owner | named process with a stated achievable tolerance |
| GEO-07 | matched-thrust set-points | Agent proposes from IN-04 | registered before the first run |
| GEO-08 | thrust-match tolerance for `T*` | Agent derives from IN-03 | dimensionally consistent value |
| GEO-09 | replication count per condition | Agent proposes | registered with a rationale |

## 10. Invalid-condition rules

A run is invalid, and is retained with its reason rather than deleted, when any of the following holds:

1. A contact or rubbing event is indicated by the contact detector defined in the measurement requirements.
2. Clearance-probe dropout exceeds the declared fraction over the averaging window.
3. Static clearance was not verified before the condition.
4. The achieved thrust is outside the GEO-08 tolerance at any recorded set-point.
5. Duct or ambient temperature leaves the band registered for the block.
6. An insert's Datum C mark does not align with the duct fiducial, i.e. the insert was installed rotated.
7. The measured `c̄` of the installed condition differs from its design `c̄₀` by more than the combined fabrication and measurement allowance. **This is the equal-mean check, and it is performed on the installed hardware, not assumed from the drawing.**

Invalid runs are excluded by rule and before the response is inspected. A run may never be excluded because its result is inconvenient.

## 11. What this contract does not do

It does not choose numbers that belong to the owner, authorise fabrication, or establish that any defect family matters. It defines geometry parametrically, fixes what must be held constant, and states the rules that make a comparison valid. **No condition may be manufactured from this document in its current state**, because it is a draft with twelve open inputs and the CAD branch remains deferred behind its own entry conditions.
