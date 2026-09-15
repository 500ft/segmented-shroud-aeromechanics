# Measurement-system requirements — draft

Status: `planned` · `draft` · **requirements not frozen; installed qualification not performed.**
Work order: [plan 2026-09-14](specs/day-2026-09-14/plan.md), decision D6. Drafted 2026-09-15. Backlog task: SSY-02 (requirements freeze), which stays open; SSY-12 is the separate installed qualification.

This document says what must be measured, how well, and how that will be shown, for [Experiment 01](experiment-01-rigid-defect-duct.md). It contains no numerical operating point, no effect threshold and no sensor selection. Every such value is an input in the [open-input register](#5-open-input-register-and-release-criteria) with a responsible role and the evidence that closes it. Three events are kept separate throughout: this **draft** (delivered), the **SSY-02 requirements freeze** (needs the register's inputs and an accepted allocation), and **SSY-12 installed qualification** (needs measurements on the built rig). A passing software check is none of the three.

## 1. Measurands and operating envelope

### 1.1 Three separate quantities

| symbol | quantity | unit | definition |
| --- | --- | --- | --- |
| c̄ | measured circumferential mean clearance | µm | mean of the radial clearance over the averaging domain of §1.3, per condition, at the reference operating state. Equal-mean conditions are equal in c̄ within its difference uncertainty (§4.5). |
| c_min(t) | dynamic minimum clearance | µm | smallest valid clearance sample over the observed angles and the run, per blade passage or per revolution as chosen in IN-08. Unobserved angles are reported as unobserved, never as the minimum. |
| P(T\*) | electrical power at matched thrust | W | `P = mean(V(t) · I(t))` over synchronized samples in the averaging window at thrust T\*, or a documented equivalent power measurement. `mean(V) · mean(I)` is not accepted unless ripple and V–I correlation are shown negligible for the window. |

The primary comparison is ΔP at matched thrust (§4.6). The clearance quantities qualify the geometry that comparison depends on; a micrometre limit says nothing about a watt limit and the two are budgeted separately.

### 1.2 Operating envelope

All entries are pending IN-04 (rotor, stand and sensor envelope) and are recorded here as the fields that must be filled, not as values: rotor diameter and blade count; rotor and duct materials with thermal-expansion data; speed range and the reference speeds; thrust range and the matched-thrust set-points T\*; ambient and duct temperature range; sensor target compatibility (blade-tip material, tip geometry, surface finish for capacitive, optical or eddy-current targets); rig containment and its inlet effect (§4.7).

### 1.3 Averaging domain and the missing-wall rule

A seam opening has no duct wall over its angular extent. There is no finite radial clearance there, and the averaging domain must say what is done about it before any equal-mean claim is made. Three treatments are admissible; the choice is IN-08:

1. **Wall-only domain.** c̄ is the mean over angles where a wall exists; the seam's angular width is reported as a separate geometric parameter. Equal-mean then means equal wall-region mean, and the comparison between a seamed and an unseamed duct carries the seam width as a nuisance variable that must be declared.
2. **Fixed angular grid with declared occlusion.** c̄ is the mean over a fixed set of measurement angles; samples in the seam are marked occluded and excluded from c̄, with the occluded fraction reported per condition. Conditions are equal-mean only if the occluded fractions are also matched or the effect of the mismatch is bounded.
3. **Both reported.** Required if the pilot cannot show that 1 and 2 give the same ranking of conditions.

The same rule governs probe dropout (§1.5): a dropped sample is reported as missing, not interpolated into c̄ or c_min.

### 1.4 Physical displacement versus measurement uncertainty

Runout, thermal growth and fixture deflection are physical displacements. They change the true clearance and are corrected for, or measured through, by the clearance channel. Their entries in the budget register are the **uncertainty of measuring or correcting** each one, not the displacement itself. A measured 30 µm runout with a 3 µm measurement uncertainty contributes 3 µm to the budget, unless the correction is not applied, in which case the whole uncorrected displacement is a bias and is treated in §4.4. The same effect is not counted twice: a contributor already inside the dynamic clearance sensor's calibrated reading (for example runout seen directly by an in-situ probe at speed) is not added again as a separate term. Which contributors are inside which reading is decided per installed method and is part of IN-09.

### 1.5 Contact, dropout and invalid runs

Vibration monitoring alone does not establish absence of rubbing. A run is valid only if all of the following are recorded: no contact indication from the chosen contact detector (IN-10: options are a witness coating or rub pin on the duct wall, an acoustic-emission or current-signature event detector, and post-run inspection; the coating or pin is the minimum), no probe dropout above the declared fraction (IN-10), and static clearance verified before the condition per the experiment protocol's safety controls. Invalid runs are retained with their reason and excluded from the analysis by rule, never by result.

### 1.6 Sample unit

Specimen → condition (insert set) → run (one operating-point sweep) → block (randomised order within a block). The unit of replication for the hypothesis is the condition-within-block; repeated runs of one condition estimate within-condition repeatability, not the effect. Registration of aggregation and weights happens before confirmation, as the experiment protocol already requires.

## 2. Channel requirements

Every row lists the fields SSY-02 must eventually fix. A field showing an input ID is unresolved and assigned; nothing in this table is an installed accuracy. Literature sensors (S5, S6 class fibre-bundle and capacitive probes; the tip-timing and capacitive methods in the 2026-09-14 screening queue) are candidates, not selected hardware.

| channel | quantity, unit | intended range | allowable bias | repeatability (statistic, limit) | resolution | bandwidth / sample rate | calibration reference and method | qualification procedure | acceptance criterion | status / input |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mean-clearance geometry (static) | c̄ per condition, µm | IN-02 ± the defect amplitudes | ≤ a declared fraction of IN-01 | std. dev. of repeated settings, limit ≤ `seam_setting_repeatability` | ≤ 1/10 of IN-01 | static; one map per setting | gauge blocks or a calibrated bore gauge traceable to a length standard; map over the §1.3 grid | §4.3 repeated-setting test | k·u_c(c̄) < IN-01 per the calculator | pending IN-01, IN-02, IN-08 |
| dynamic tip clearance | c(θ, t), c_min, µm | IN-02 minus runout allowance to IN-02 plus defect amplitude | ≤ `sensor_calibration_on_fixture` bias term | blade-passage repeatability at fixed speed, limit from IN-01 | ≤ 1/10 of IN-01 | must resolve blade passage: sample rate ≥ N_blades · f_rot · oversampling factor, oversampling ≥ 10 (IN-11 sets the factor) | in-situ calibration against a gauge block or micrometer stage on THIS duct, cold and, if feasible, warm | §4.2 calibration at range; §4.3 drift; §4.4 correction residuals | five installed contributors recorded with units and statistics; budget verdict FEASIBLE | pending IN-06, IN-09, IN-11 |
| thrust | T, N | 0 to max thrust of IN-04 with margin | ≤ a declared fraction of the thrust step between set-points | std. dev. of repeated tares and reference runs | ≤ 1/20 of the smallest thrust difference between conditions at T\* | ≥ 10 × the rotor-rpm ripple frequency or low-pass filtered with declared cutoff | dead-weight or calibrated load cell, at least five points across range, before and after the campaign | §4.2, §4.3 | interpolation error at T\* bounded and propagated to ΔP (§4.6) | pending IN-03, IN-04, IN-05 |
| voltage | V(t), V | supply range of IN-04 | ≤ declared fraction of the ΔP target's voltage share | std. dev. over the averaging window | per ADC specification, recorded | synchronized with current at the §4.6 rate | calibrated reference meter or source, at range | §4.2 | V and I calibrations and their covariance recorded | pending IN-03, IN-05 |
| current | I(t), A | 0 to max current of IN-04 | as voltage | as voltage | as voltage | as voltage | shunt or transducer calibrated against a reference at range; phase alignment with V verified | §4.2, §4.5 synchronization | as voltage | pending IN-03, IN-05 |
| electrical power (derived) | P(T\*), W | derived | derived from V, I, timing | repeated-reference std. dev. at T\* | derived | window length and sample rate fixed by IN-11 | none directly; derived per §1.1 with the covariance of V and I | §4.6 | u(ΔP) < IN-03 | pending IN-03, IN-11 |
| RPM | f_rot, Hz | speed range of IN-04 | ≤ 0.1 % of reading or as set by IN-05 | std. dev. at steady state | one pulse per revolution minimum; per-blade if used for tip timing | phase-locked to the clearance channel | optical or hall once-per-revolution against a calibrated counter | §4.5 | timing jitter budget met | pending IN-05, IN-11 |
| ambient temperature | T_amb, °C | facility range | ≤ 0.5 °C or as set by IN-05 | — | 0.1 °C | ≥ 1 Hz | calibrated thermometer | §4.3 drift correlation | drift explained or bounded | pending IN-05 |
| duct temperature | T_duct, °C, one or more locations | cold to warm operating | as ambient | — | 0.1 °C | ≥ 1 Hz | contact sensor calibrated at two points | §4.4 thermal growth correction | growth correction residual recorded | pending IN-05, IN-06 |
| vibration | a(t), m/s² at duct and stand | per IN-04 | not a measurement channel for the hypothesis; abort and diagnostic only | — | — | ≥ 10 × blade-passage frequency | accelerometer calibrated per manufacturer, recorded | §1.5 abort rule | abort thresholds predefined | pending IN-04, IN-10 |
| alignment | rotor axis to duct axis, offset µm and tilt mrad | within the defect amplitude budget | ≤ declared fraction of IN-01 | repeat-mount std. dev. | per method | static per mount | dial indicator or the clearance probe itself over a full revolution at low speed | §4.3 repeated-setting | alignment residual folded into c̄ uncertainty | pending IN-05, IN-08 |
| acquisition timing | common time base, s | whole run | ≤ declared latency between clearance, RPM, V and I | jitter std. dev. | per DAQ | master clock; all channels timestamped or hardware-triggered | loop-back or common-event test | §4.5 | latency and jitter below IN-11 | pending IN-11 |

## 3. Budget register mapping

The rows below copy [clearance-measurement-budget.csv](clearance-measurement-budget.csv) exactly; a test keeps them in step. The calculator behind it, `scripts/clearance_uncertainty_budget.py`, is a provisional clearance-only root-sum-of-squares of five installed contributors with a coverage factor, gated by the minimum effect of interest. It is not the complete measurement-system analysis: it carries no power channel, no difference-uncertainty term, no covariance, and no sensitivity coefficients.

<!-- budget-register:start -->
| term | unit | value | evidence_state | source | interpretation | next_input |
| --- | --- | --- | --- | --- | --- | --- |
| sensor_accuracy_literature | um | 25 | literature_bound | S5 doi:10.1155/2017/4168150 (reflective fibre bundle; accuracy 25 um or better on a rotor rig) | Published accuracy of one sensor class on another rig. Carried for reference; never combined. | IN-09 method selection; then replaced in the combination by sensor_calibration_on_fixture |
| sensor_calibration_on_fixture | um | pending | pending |  | Bias and repeatability of the chosen sensor calibrated in situ against a reference on this duct. First of the five installed contributors. | IN-06: calibration record on the installed sensor |
| rotor_radial_runout | um | pending | pending |  | Blade-tip radius variation at speed. A physical displacement; enters the budget only as the uncertainty of measuring or correcting it, not as the displacement itself. | IN-06: dynamic runout measurement and its stated uncertainty |
| thermal_growth_at_speed | um | pending | pending |  | Tip-radius and duct-radius change between the cold static datum and the operating condition. Same rule as runout: correction uncertainty, not the growth. | IN-06: measured growth with correction model and residual |
| fixture_deflection_under_thrust | um | pending | pending |  | Duct-to-rotor relative displacement under peak thrust, from a stiffness measurement. | IN-06: stiffness measurement record; FEA alone does not close it |
| seam_setting_repeatability | um | pending | pending |  | Repeatability of re-establishing a seam opening or two-lobe distortion at equal mean clearance. | IN-06: repeated-setting record on the built inserts |
| target_mean_clearance | um | pending | pending |  | The mean clearance every condition is set to. A design choice tied to the reference geometry. | IN-02: owner decision with rationale |
| minimum_effect_of_interest | um | pending | pending |  | Smallest clearance-equivalent difference the experiment must resolve. Written before Stage A; a measurement cannot supply it. | IN-01: owner decision with rationale |
| coverage_factor_k | - | 2 | protocol | docs/experiment-01-rigid-defect-duct.md Stage A | Protocol coverage factor for the expanded uncertainty. Governed range 1-3 by the calculator. | none: protocol value already recorded |
<!-- budget-register:end -->

Protocol choices in that table: `coverage_factor_k`. Owner decisions: `minimum_effect_of_interest`, `target_mean_clearance`. Installed contributors, all five pending: `sensor_calibration_on_fixture`, `rotor_radial_runout`, `thermal_growth_at_speed`, `fixture_deflection_under_thrust`, `seam_setting_repeatability`. The literature bound is recorded and excluded from the combination, as the calculator already enforces.

## 4. Qualification procedures and endpoint uncertainty

Each procedure names what is observed, what passes, what stops, and what is still unset. None can be executed until its unset parameters are filled; a file-consistency check passing is not a measurement PASS.

### 4.1 Uncertainty model for clearance

Retained rule from the calculator: `k · u_c < minimum_effect_of_interest`, else `STOP_INSTRUMENTATION_REDESIGN`; while any required term is pending or at an ineligible evidence state, `INPUTS_PENDING`. The root-sum-of-squares `u_c = sqrt(Σ u_i²)` is valid only when each `u_i` is a standard uncertainty in the same unit, the sensitivity coefficient of each contributor to the clearance reading is 1 or has been justified, and the contributors are uncorrelated. Before the installed model is accepted, the following must be recorded for each term: how the observed bound or spread was converted to a standard uncertainty (Type A standard deviation of repeats, or a Type B assumed distribution with its divisor), the sensitivity coefficient, and any known correlation, with correlated pairs combined through the covariance term rather than assumed independent. The general basis is [NIST TN 1297, Appendix A](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty), used as method, not as certification. A reported physical displacement is not a standard uncertainty (§1.4).

### 4.2 Calibration at the intended range

Observed: at least five reference points spanning the intended range for clearance (gauge stage), thrust (dead weight or reference cell), voltage and current (reference meter), before and after the campaign. Pass: residuals after the fitted calibration within the allowable bias for that channel, before and after, with no drift between the two beyond the repeatability limit. Stop: residuals outside the bias limit, or a post-campaign shift larger than the limit, which invalidates the runs between the two calibrations until re-analysed with the shift as a bias. Unset: the bias limits (IN-01, IN-03, IN-05), the reference standards available (IN-04).

### 4.3 Warm-up, drift, tare and repeated setting

Observed: the reference condition run at the start of every block and after warm-up, with tare of the thrust channel before each run; the same insert set removed and re-set N times with c̄ re-mapped each time. Pass: reference-run thrust and power within the repeated-reference standard deviation used in §4.6; c̄ re-setting standard deviation ≤ `seam_setting_repeatability`; drift over a block explained by the temperature channels or bounded below the repeatability limit. Stop: drift larger than the limit and not explained by temperature. Unset: warm-up duration, N, block length, the drift limit (IN-12).

### 4.4 Corrections and their residuals

Observed: runout measured over a full revolution at each reference speed; thermal growth as the change in c̄ between cold datum and thermal equilibrium at each speed, with duct and ambient temperature; fixture deflection as the change in rotor-to-duct position under static or equivalent load from a stiffness measurement. Pass: each correction's residual after application, expressed as a standard uncertainty, entered as the register term. Stop: a correction that cannot be applied leaves its whole displacement as a bias, and the bias must then be smaller than the effect of interest on its own. Unset: which contributors are already inside the installed clearance reading (IN-09), the load and speed points (IN-04).

### 4.5 Synchronization, latency and alignment

Observed: a common-event test (a single edge seen by the clearance, RPM, V and I channels) and a loop-back of the trigger; alignment measured per mount by the §2 method. Pass: inter-channel latency and jitter below the timing limit; alignment residual within the fraction of IN-01 set for it. Stop: latency that cannot be corrected by a fixed offset. Unset: the timing limit and the oversampling factor (IN-11), the alignment fraction (IN-05).

### 4.6 Power endpoint at matched thrust and the uncertainty of a difference

Endpoint: `ΔP(T*) = P_defect(T*) − P_reference(T*)` in W, at each matched-thrust set-point T\*. The minimum meaningful power difference is a separate, independently specified target (IN-03). If a relative endpoint is used instead, its denominator is named (the reference-condition power at T\*, not the small duct-minus-open-rotor difference, per the experiment protocol). Contributors to `u(ΔP)`: voltage and current calibration and their covariance; thrust measurement error mapped through the local slope dP/dT at T\*; interpolation to T\* (the interpolation method itself belongs to the analysis pipeline and is not chosen here); drift within a block; repeated-reference variability. Because both conditions share calibrations and the block's reference runs, the difference uncertainty is not the quadrature sum of two single-condition uncertainties: shared calibration terms cancel in the difference and are entered once through the covariance, while repeated-reference variability enters for both. The same reasoning applies to the equal-mean claim: `c̄_defect − c̄_reference` has its own uncertainty from two settings that share the gauge calibration, and "equal mean" means that difference is smaller than its expanded uncertainty and smaller than the fraction of IN-01 set for it. A single-condition budget establishes neither. Pass: `k · u(ΔP) < IN-03` at every T\*. Unset: IN-03, the set-points (IN-04), the window and rate (IN-11).

### 4.7 Installed inlet and containment effects

Observed: reference-condition thrust and power with and without the containment in place at low-energy commissioning, or with the containment's inlet blockage documented if it cannot be removed. Pass: the containment's effect on the reference is measured and either negligible against IN-03 or constant across conditions. Unset: the commissioning points (IN-04).

### 4.8 Data retention

Every run keeps its raw channel records, timestamps, calibration in force, temperature trace, contact-detector state, dropout fraction, and validity disposition with reason. Invalid runs are retained. Derived quantities are regenerated from raw records by the analysis pipeline, not stored as the only copy.

## 5. Open-input register and release criteria

| ID | needed value or decision | unit | responsible role | source or method | closes when |
| --- | --- | --- | --- | --- | --- |
| IN-01 | minimum clearance effect of interest | µm | Owner, with agent-prepared rationale | tied to the hypothesis and the reference geometry; written before Stage A | sourced value in the register with `owner_decision` |
| IN-02 | target mean clearance | µm | Owner | design choice against the reference duct and rotor | sourced value in the register with `owner_decision` |
| IN-03 | minimum meaningful power difference at matched thrust, or the relative endpoint and its denominator | W or declared ratio | Owner accepts the target; agent derives channel requirements from it | scientific target for the primary comparison | value, operating point, reference and rationale recorded |
| IN-04 | provisional rotor, stand, sensor and containment envelope | — | Owner identifies resources; agent records compatibility questions | dated named resources, or an explicit design-only choice | actual access distinguished from nominal selection, entered in §1.2 |
| IN-05 | channel bias, repeatability and alignment fractions; RPM and temperature limits | per channel | Agent drafts; experiment reviewer accepts | derived from IN-01 and IN-03 by allocation | dimensionally consistent limits entered in §2 |
| IN-06 | the five installed clearance contributors | µm, as standard uncertainties | qualified operator or metrology provider | calibration and measurement records on the built rig (§4.2–§4.4) | register rows move to `measured` or `calibration_record` with sources |
| IN-07 | XC-02 disclosure path | — | Owner | evidence required by XC-02's done-condition | recorded in the decision log |
| IN-08 | averaging domain and missing-wall treatment (§1.3), aggregation of c_min | — | Agent proposes; experiment reviewer accepts | choice among the three admissible treatments | recorded here and in the experiment protocol before Stage B |
| IN-09 | dynamic-clearance method and which contributors it already includes | — | Agent shortlist; owner and facility choose | screening queue metrology candidates; S5/S6 class | method named, inclusion map recorded (§1.4) |
| IN-10 | contact detector, dropout fraction limit, abort thresholds | — | Agent proposes; safety reviewer accepts | §1.5 options | rule recorded before commissioning |
| IN-11 | timing limit, oversampling factor, averaging window and rate | s, —, s, Hz | Agent derives from the rotor envelope | blade-passage frequency of IN-04 and permitted error | entered in §2 and §4.5 |
| IN-12 | warm-up duration, repeat count N, block length, drift limit | s, —, —, per channel | Agent proposes; experiment reviewer accepts | §4.3 | entered in §4.3 |

Release criteria, kept separate:

- **This draft is complete** when the five parts above exist with every unresolved field carrying an input ID. Delivered 2026-09-15.
- **SSY-02 requirements freeze** needs IN-01 to IN-05 and IN-08 to IN-12 closed, an accepted allocation, and SSY-01's source boundary; then the limits in §2 become numbers and the document is re-issued as `frozen`.
- **SSY-12 installed qualification** needs IN-06 measured on the built rig, the procedures of §4 executed with their observations retained, and the calculator reporting `FEASIBLE` together with `k · u(ΔP) < IN-03`. Only then is Stage A passed.

What can be prepared now without inputs: the analysis-pipeline interfaces for the sample hierarchy of §1.6 and the raw-record schema of §4.8. What needs an owner choice: IN-01, IN-02, IN-03, IN-04, IN-07. What requires installed measurements: IN-06 and every §4 pass.
