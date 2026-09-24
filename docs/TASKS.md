# Segmented Shroud Yield — long-term research backlog

## CAD decomposition of the research backlog

[CAD_PLAN.md](CAD_PLAN.md) and [CAD_TASKS.csv](CAD_TASKS.csv) split SSY-04 into independently reviewable geometry and inspection tasks. SSY-CAD-01 through SSY-CAD-07 refine SSY-03/04; they do not duplicate completion status or close SSY-06. SSY-CAD-08/09 have details and estimates withheld until XC-02 closes. SSY-CAD-10 covers reproducible geometry tooling. The original 17 research-level tasks and dependency audit are unchanged; the ten CAD entries are a separate, currently parked work breakdown. Cross-ledger dependencies are checked through CAD_DEPENDENCIES.json. Owner authorized merging this PR's current documents to main; research/disclosure gates remain unresolved until their own evidence arrives.

The active 2026-09-05 integrity sprint is governed by [SPRINT_ROADMAP.md](SPRINT_ROADMAP.md)
and the sole status ledger [SPRINT_TASKS.csv](SPRINT_TASKS.csv). This document
retains long-term research dependencies; “executable now” means no intrinsic
hardware dependency, not completed predecessors. It is not the active ready queue.

> **Objective.** Produce the strongest, most honestly packaged evidence—not a finished flying
> shroud. Priority flows from causal isolation, measurement credibility, and executability. A
> simpler model or guard classification is allowed to win.

Informed by a [source-reviewed directed dependency audit](research-dependency-audit.md) of
commit `84b38ff`. Graphify supplied candidate relationships; only manually verified research
dependencies were retained. Repository navigation, CI, schemas, generated tasks, and raw
centrality counts are excluded from the published map. Novelty remains unresolved until SSY-01
closes. No dates or estimates appear, by design.

## Two finish lines

**Ceiling.** A defect-aware model predicts held-out rigid-duct behavior, replicated closure
mechanisms propagate measured deployment variation into that model, and joint aero-mechanical
yield supports performance-duct assessment. A protective-guard classification
additionally requires the independent SSY-17 evidence; otherwise protection is unknown.

**Floor.** A citable research-design package containing a closed novelty boundary, qualified
measurement requirements, parametric equal-mean-clearance defect CAD, an executable analysis
pipeline with non-evidence fixtures, and a frozen test protocol with **measurement pending**
stated plainly.

The floor is the finish line available without a rotor stand, fabrication access, or laboratory
approval. No planned specimen or synthetic fixture is counted as physical evidence.

_17 long-term project tasks · 6 Tier 0 · readiness requires completed predecessors._

**Gate types.** `preregister` — commit a decision before the data it judges; `external` —
requires a person, facility, fabrication process, or instrument outside this repository;
`build` — new implementation, model, CAD, or analysis; `hygiene` — reproducibility, search, or
packaging debt.

**Tiers.** 0 finish · 1 package · 2 park. A task whose required rig, instrument, specimen, or
positive result is not secured cannot be Tier 0, however visually impressive it might be.

---

## Tier 0 — finish

### SSY-01 · Close the exact-gap and measurement-method search

2026-09-08: [SSY-D01 first-pass source/metrology review](prior-art-search-2026-09-08.md)
is complete. Full close-competitor texts and the stated broader-search shortfalls
remain. SSY-01, SSY-02/03 and XC-02 are not automatically closed by this artifact.

2026-09-15: [top-25 database-candidate triage](prior-art-search-2026-09-14-screening.md)
is complete (ledger row SSY-R03): 22 included for close reading, 3 excluded, 0 deferred, under a
rule frozen before reading. SSY-01 stays open on close reading, the 111 qualifying unselected
records, the S2/S3 full texts, instrument constraints, and a dated patent search, which was not
performed.

`hygiene` · executable now

**Why it matters.** The current source map establishes clearance sensitivity, non-axisymmetric
distortion, self-locking mechanisms, and enclosure trade-offs. It is not yet a systematic search
for small-UAV seam and step defects, repeated-deployment propagation, dynamic clearance
metrology, or relevant patents.

**What it adds.** A defensible claim boundary and evidence-based shortlist of measurement
methods before hardware is designed around an unsuitable sensor.

**Done when.** `docs/prior-art.md` records dated database and patent searches, search strings,
inclusion and exclusion rules, an evidence table for equal-mean-clearance defects and dynamic
tip-clearance methods, instrument constraints, and a conclusion written as “supported candidate
gap” or “prior art found”—never “no one has done this.”

### SSY-02 · Freeze the measurement-system requirements and uncertainty budget

`preregister` · executable now · after SSY-01

2026-09-15: a [measurement-requirements draft](measurement-system-spec.md) exists (ledger row
SSY-R04) with every channel, the budget-register mapping, qualification procedures and an
open-input register IN-01 to IN-12. It is a draft: requirements are not frozen, no numerical
target or sensor is chosen, and installed qualification (SSY-12) has not been performed.

**Why it matters.** If clearance, thrust, power, RPM, temperature, or alignment uncertainty is
as large as the smallest effect of interest, no later model can recover the experiment.

**What it adds.** A quantitative gate that the stand and instruments must pass before hypothesis
data are allowed.

**Done when.** A committed specification defines the minimum resolvable defect and performance
effect, maximum allowable bias and repeatability for every channel, calibration references,
warm-up and drift tests, synchronization tolerance, dynamic-clearance method, sample unit, and a
PASS/FAIL measurement-system analysis that precedes performance runs.

### SSY-03 · Freeze the reference geometry, defect basis, and comparison conditions

`preregister` · executable now · after SSY-01, SSY-02

2026-09-22: a [design contract](design-contract-experiment-01.md) exists (ledger row SSY-R09) with
datums, defect equations whose equal-mean construction is verified by test, tolerance classes,
comparison conditions and invalid-condition rules. It is a **draft, not the freeze this task asks
for**: twelve inputs are open, four of them the owner's. It also records that the Study A
computational rotor and the Experiment 01 physical rotor are different machines, so a computed
effect size is not a prediction for the rig.

**Why it matters.** Uniform gap, ovality, seam, and radial step are presently words rather than
manufacturable treatments. Comparing at matched RPM instead of matched thrust could also turn a
changed operating point into a false duct benefit.

**What it adds.** One causal experiment in which topology changes while mean clearance and the
registered reference conditions remain controlled.

**Done when.** A committed design contract defines the rotor and operating envelope, open-rotor
and monolithic references, duct profile, uniform and two-lobe equations, seam and step geometry,
equal-mean-clearance construction, amplitude levels, inspection datums, matched-thrust primary
comparison, matched-RPM secondary diagnostic, randomized order, and invalid-condition rules.

### SSY-04 · Build the parametric rigid-insert CAD and inspection package

`build` · executable now · after SSY-03

**Why it matters.** The decisive first experiment requires interchangeable defects whose actual
geometry can be verified. Hand-modified ducts would confound topology, mean clearance, surface
finish, and alignment.

**What it adds.** Manufacturable experimental treatments that encode the registered geometry
rather than approximate it by eye.

**Done when.** Parameterized source CAD generates the monolithic, uniform, two-lobe, seam, and
step conditions; equal-mean-clearance is checked computationally; drawings include datums,
tolerances, material and process notes, rotor/stand interfaces, static-clearance checks, and
inspection points; exported files are labeled **CAD, fabrication pending**.

### SSY-05 · Build the data and analysis pipeline against synthetic fixtures

`build` · executable now · after SSY-02, SSY-03

2026-09-24: revised after external review (see the correction record). The wall-domain mean is
now an angle-weighted integral reported separately from the harmonic intercept, because on a
masked domain those are different quantities; the baseline falls back to intercept-only when mean
clearance does not vary, which is the design this project actually proposes; scoring is
specimen-first; and an effect inside its own uncertainty is reported INCONCLUSIVE rather than as a
null.

2026-09-23: implemented (ledger row SSY-R10) as
[`scripts/analysis_pipeline.py`](../scripts/analysis_pipeline.py) with
[synthetic fixtures](../data/fixtures/synthetic/README.md) and 21 tests. It refuses a wrong unit,
a clearance inside a seam, a walled sample with no value, extrapolation past the measured thrust
range, and a descriptor that is constant or collinear in training. The verdict is judged against
the roadmap's registered 20 percent improvement and 10 percent error gate, not against whether the
number happens to be positive. **Still open:** real channel formats are unknown until instruments
exist, so the ingestion schema is provisional.

**Why it matters.** Writing the analysis after seeing physical results invites silent choices in
matched-thrust interpolation, harmonic extraction, repeated-measure handling, and held-out
selection.

**What it adds.** A tested pipeline whose behavior is known before it touches experimental data.

**Done when.** Code validates the specimen manifest, ingests synchronized channels, calculates
the clearance field and registered defect descriptors, performs matched-thrust interpolation,
computes electrical thrust-per-power, preserves specimen/cycle/run hierarchy, fits the mean-only
and defect-aware models, enforces a held-out family, and passes analytic positive, null, missing-
data, and unit-error fixtures explicitly labeled **synthetic test data—not evidence**.

### SSY-06 · Write the floor research package

`build` · executable now · after SSY-04, SSY-05

**Why it matters.** Rotor access may never materialize. Without an explicit floor, the repository
would read as an abandoned hardware promise rather than a completed, reviewable research design.

**What it adds.** A defensible portfolio artifact even while every physical result remains
pending.

**Done when.** One indexed package links the source boundary, causal diagram, measurement
requirements, parametric CAD, specimen schema, safety boundary, executable analysis fixtures,
registered gates, and positive/null/pivot branches; every visual states its evidence class and
no synthetic output appears in a Results section.

---

## Tier 1 — package

### SSY-07 · Build result shells and figure generators before measurement

`build` · executable now · after SSY-05

**Why it matters.** Selecting plots after seeing which one looks persuasive encourages outcome-
driven presentation and makes negative findings harder to retain.

**What it adds.** A preregistered visual grammar for measurement-system performance, defect
geometry, matched-thrust response, model comparison, interval calibration, and the final
classification.

**Done when.** Generator tests create clearly watermarked fixture-only versions of every planned
figure and table; captions state sample unit, condition, uncertainty, and evidence state; the
figure manifest records inputs, generator command, output, and claim; generated fixture images
are not represented as results.

### SSY-08 · Prepare the fabrication, commissioning, and risk-review packet

`build` · executable now · after SSY-02, SSY-04

**Why it matters.** A rotor experiment cannot be improvised from CAD. Containment, remote
shutdown, current limits, static clearance, vibration aborts, and inspection sequencing are part
of the apparatus, not administrative details.

**What it adds.** A package a laboratory can review and either approve or reject without filling
in hidden engineering assumptions.

**Done when.** The packet contains drawings and BOM, stand load and speed envelope, containment
rating evidence needed, arming and shutdown diagram, current protection, exclusion zone,
calibration plan, low-energy commissioning sequence, pre-run inspection, temperature/current/
vibration/contact aborts, operator roles, and required approvals; it remains labeled **not
authorized** until signed by the responsible facility.

### SSY-09 · Prepare the PI and facility decision packet

`build` · executable now · after SSY-01, SSY-06, SSY-08

**Why it matters.** The project's feasibility depends on metrology, fabrication, and rotor-stand
resources. A broad concept pitch does not let a PI judge whether the decisive test fits the lab.

**What it adds.** A concise request tied to one falsifiable experiment rather than an open-ended
request to build a morphing UAV.

**Done when.** The packet states the candidate gap, exact first experiment, required instrument
resolution and operating envelope, safety controls, expected positive and null contributions,
requested resources, authorship/data questions, and the rule that closure-mechanism work waits
for the rigid-defect gate.

---

## Tier 2 — park

### SSY-10 · Secure the rotor stand, instruments, fabrication path, and safety ownership

`external` · **blocked-on-lab-access** · after SSY-08, SSY-09

**Why it matters.** No physical result can exist without a contained stand, qualified sensing,
fabricated treatments, and a person responsible for approving the procedure.

**What it adds.** Legitimate access and safety authority for leaving the research-design stage.

**Done when.** A named facility confirms the speed/thrust envelope, containment, dynamic-
clearance method, load/electrical/RPM instrumentation, calibration access, fabrication route,
operators, data ownership, and written risk-review process.

### SSY-11 · Fabricate and inspect the rigid reference and defect conditions

`external` · **blocked-on-fabrication** · after SSY-04, SSY-10

**Why it matters.** Nominal CAD is not the treatment. Actual mean clearance, harmonic amplitude,
seam, step, alignment, and surface condition determine what the rotor experiences.

**What it adds.** Traceable specimens whose measured geometry can enter the analysis instead of
ideal design values.

**Done when.** Every reference and defect insert has a unique specimen ID, material/process and
geometry revision, inspection record with uncertainty, photographs, manifest, PASS/FAIL fit
check, and a disposition for out-of-tolerance parts; no aerodynamic claim is made.

### SSY-12 · Qualify the complete measurement system

`external` · **blocked-on-bench** · after SSY-10, SSY-11

**Why it matters.** This is the gate beneath every later result. Calibration certificates alone
do not quantify installed bias, repeatability, drift, alignment, synchronization, or the effect
of containment.

**What it adds.** Evidence that the apparatus can resolve the registered effect before the
hypothesis is tested.

**Done when.** The installed system completes the frozen bias, repeatability, warm-up, drift,
alignment, synchronization, dynamic-clearance, and reference-repeat tests; each channel is
scored against SSY-02; failed channels stop performance data collection rather than weakening
the requirement.

### SSY-13 · Run the rigid-duct pilot without using it as confirmation

`external` · **blocked-on-bench** · after SSY-12

**Why it matters.** The current 10% error and 20% improvement gates are provisional. Pilot data
must reveal variance, contact behavior, achievable defect amplitude, thermal drift, and invalid-
run frequency before confirmation is sized and frozen.

**What it adds.** The empirical basis for a feasible confirmatory design.

**Done when.** Randomized pilot blocks cover all valid references and pilot defect conditions at
registered operating points; raw data and manifests remain immutable; actual geometry replaces
nominal geometry; variance components and anomalies are reported; pilot specimens and runs are
excluded from held-out confirmation.

### SSY-14 · Freeze the confirmatory defect and analysis contract

`preregister` · **blocked-on-pilot** · after SSY-13

**Why it matters.** Choosing the held-out family, error metric, interval method, sample size,
practical effect, or rub definition after viewing confirmation data would make the headline
comparison post hoc.

**What it adds.** A defect-aware model that can lose fairly to mean clearance.

**Done when.** A dated commit fixes specimen count, deployment/cycle structure, randomization,
held-out defect family, model forms and allowed tuning, matched-thrust interpolation, primary and
secondary outcomes, uncertainty model, missing/abort handling, rubbing definition, prediction-
error and interval-calibration gates, and every positive/null decision branch before new
validation data are collected.

### SSY-15 · Run held-out rigid-defect validation and take the registered branch

`external` · **blocked-on-bench** · after SSY-14

**Why it matters.** This is the minimum paper's decisive result. Training fit cannot show that
deployment-specific descriptors transfer beyond the geometries used to construct the model.

**What it adds.** Either a validated defect-aware predictor or evidence that average clearance
is the adequate engineering rule in the tested envelope.

**Done when.** The held-out family is revealed only after model freeze; prediction error,
interval coverage, matched-thrust response, clearance/contact outcomes, and uncertainty are
reported; the decision log records defect-aware, simpler-model, or inconclusive outcome without
moving a gate.

### SSY-16 · Compare closure mechanisms and estimate joint yield only after SSY-15 passes

`build` · **blocked-on-positive-gate-and-fabrication** · after SSY-15

**Why it matters.** An ordinary versus self-centering closure comparison matters aerodynamically
only if the defects those mechanisms produce matter. Starting earlier combines two unanswered
questions and risks pseudoreplication across cycles.

**What it adds.** The full causal link from mechanism variation to deployed geometry to predicted
rotor outcome.

**Done when.** Multiple independent specimens per mechanism are matched on nominal geometry and
ring mass; preload, energy barrier, stiffness, proof load, seams, harmonics, and reconstruction
variance are measured over registered cycles; a hierarchical model propagates specimen and
cycle uncertainty into deployment, lock, clearance, performance, and joint yield.

### SSY-17 · Execute the protective-guard branch only under its own criteria

`external` · **blocked-on-guard-pivot** · after SSY-15 or SSY-16

**Why it matters.** A structure that lacks aerodynamic benefit is not automatically a successful
guard. Protection, containment, deflection, mass, and power penalty require separate evidence.

**What it adds.** A defensible negative-result branch rather than a renamed failed duct.

**Done when.** A separately preregistered comparison measures impact energy, maximum inward
deflection, blade containment, deployment and lock reliability, mass, and matched-thrust power
penalty against appropriate fixed/open references; the final classification is performance
duct, protective guard, or neither under the registered rules.

---

## Cross-cutting

These tasks are not included in the 17 project-task count.

### XC-01 · Reconcile the repository, portfolio, resume, and any paper abstract

`hygiene` · executable later · after SSY-15

**Why it matters.** A simpler-model result or guard pivot changes the project's public identity.
Conflicting descriptions would turn disciplined iteration into apparent overclaiming.

**What it adds.** One evidence state and one result classification everywhere a reviewer can
encounter the project.

**Done when.** Every public claim, image, and number traces to the same committed artifact and
evidence label; “performance duct” or “protective guard” appears only if its registered evidence
exists.

### XC-02 · Record the publication and disclosure path before adding implementation-sensitive detail

`external` · executable now · before implementation-sensitive public disclosure

**Why it matters.** This repository is public. A website publication can affect patent options,
especially outside the United States, while ownership and disclosure obligations can depend on
where and how future work is performed. Making a repository private later does not erase an
earlier public disclosure.

**What it adds.** A deliberate public-first, publication-first, or counsel-reviewed path instead
of letting repository activity make the decision accidentally.

**Done when.** The owner records the repository's first-public date and either records that no
patent review is being pursued or consults the appropriate university technology-transfer office
or qualified counsel before adding potentially enabling mechanism, geometry, or fabrication
detail. This task is a process gate, not legal advice.
