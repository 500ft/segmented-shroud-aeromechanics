# Segmented-shroud aeromechanics — adaptive plan
Date: 2026-09-16. Companion to [proposal.md](proposal.md). Status lives in the sprint ledger; this file says what earns a build and when.

## Must-have (v1 = the programme's floor: a CFD-bounded answer and a budget with numbers)
- Study A0, CFD credibility on a measured ducted fan — without it no seam prediction is evidence under the claim ledger.
- Study A, steady screening with GCI ⊕ clocking ⊕ model uncertainty band, both averaging rules — the cheapest test of H1 and the only way to decide IN-08 before hardware.
- Preregistration of A's design, uncertainty definition and held-out configuration in the repository before the first variant runs.
- Study B, owner decisions IN-01 to IN-03 recorded as `owner_decision` rows with CFD-cited rationale; budget re-run — turns the stop rule into an instrumentation requirement.
- Prior-art closeout to a systematic standard: close-read the 22 includes into a new dated reading record; second frozen batch for the 111 qualifying unselected records; dated patent search with routes and dates recorded — without these the novelty table cannot leave "bounded to accessible prior work".

## Nice-to-have (post-v1 queue, by value/effort)
- Descriptor model fitted on the screening set with an in-CFD held-out seam count — cheap, pre-tests H2's identifiability before any rig.
- Unsteady sliding-mesh confirmation on the control and the largest-effect case — high value, days of compute each; do two, three at most.
- Motor-efficiency map plan for the electrical-to-shaft power bridge — small document, needed before Study C anyway.
- A case-manifest schema and one check for CFD runs, reusing the existing manifest validator pattern — only once there are more than three cases to keep straight.

## Maybe-later (trigger-gated)
- Study C pilot rig · Trigger: Study B's required u_c is met by a named sensor with an in-situ calibration plan, IN-04 filled with actual resources, and Stage 1 commissioning authorised · Why wait: the budget exists precisely to stop a rig being built that cannot see the effect.
- Acoustic observable (URANS + FW-H in CFD, microphones on the rig) · Trigger: Study A shows |ΔP| or |ΔT| > U and Study C is funded with an acoustic channel · Why wait: steady CFD produces no tone; acoustics is excluded as a headline by the research plan.
- Study D decisive, held-out prediction of an unbuilt configuration · Trigger: Study C positive and funding secured against Study B's instrumentation list · Why wait: needs multiple geometries and the roadmap's Stage 2 gate.
- Closure-mechanism studies (RQ3, RQ4, H3, H4) · Trigger: roadmap Stage 2 exit gate passed and XC-02 closed · Why wait: the research plan makes the mechanism conditional on topology mattering, and the disclosure gate is open.
- Second rotor scale · Trigger: Study D complete and a second rotor/stand available · Why wait: scale changes Reynolds number, motor and manufacturing uncertainty at once.
- Cluster or cloud compute · Trigger: A0 shows the finest mesh cannot fit in 16 GB or a steady case exceeds 6 h · Why wait: the screening design is sized for the laptop; buy compute only when a measured bottleneck says so.

## Out
- Free-flight or in-flight transformation — outside the minimum core by the research plan.
- Any protective-guard claim — prohibited by the claim ledger without independent impact, containment and penalty tests.
- Acoustics as a headline contribution — excluded by the research plan.
- Closure-mechanism geometry or fabrication detail in this public repository while XC-02 is open.
- Global novelty statements — the axis table is bounded to inspected sources.
- Setting the minimum effect of interest from CFD output directly — MEI is an owner decision informed by CFD, per the budget register's own rule.

## Milestone watch
- **A0 validation number.** Check: thrust error vs published value and GCI on the finest mesh, in A0's record. Fires A, or the kill.
- **Study A band test.** Check: for each factor, is max |ΔP| > U? In A's record. Fires B with a CFD-informed range, or the CFD-bounded null.
- **Owner inputs.** Check: `owner_decision` rows for IN-01, IN-02, IN-03 in the budget CSV and a re-run record. Fires the instrumentation requirement.
- **Required u_c vs sensor class.** Check: budget output u_c requirement against the S5/S6 25 µm literature bound and any in-situ calibration evidence. Fires or blocks Study C.
- **Compute bottleneck.** Check: A0 timings and peak memory in its record. Fires the cluster/cloud item.
