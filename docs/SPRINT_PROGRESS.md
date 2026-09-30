# Progress log

What changed and when, newest first, one line per change that matters. The
plan is in the [roadmap](../ROADMAP.md). The earlier, longer version of this
log is kept at
[commit e43cb15](https://github.com/500ft/segmented-shroud-aeromechanics/blob/e43cb15109cbe8aab30e3f3befbcc59f1d811a3b/docs/SPRINT_PROGRESS.md).

## Week of 2026-09-28

- **09-30** Roadmap for the computational finish: the Fluent Student licence
  caps a model at 1M cells and 4 cores, so the baseline mesh study decides how
  the rotor is modelled. The Akturk–Camci ducted fan is recommended as the
  reference rotor ([#44](https://github.com/500ft/segmented-shroud-aeromechanics/pull/44)).
- **09-30** The owner chose a CAD and ANSYS computational finish in place of
  freezing the project or funding a thrust stand. Fluent Student starts on the
  CAD host and checks out its licence
  ([#43](https://github.com/500ft/segmented-shroud-aeromechanics/pull/43)).
- **09-29** A CFD run stopped before its assessment window is now recorded as
  terminated, not failed, and the identifiability basis is stated
  ([#36](https://github.com/500ft/segmented-shroud-aeromechanics/pull/36)).

## Week of 2026-09-21

- **09-26** Convergence-criterion sensitivity answered: the criterion has less
  than one order of magnitude of headroom, and the fine-grid SST run was never
  assessed rather than failed. The hardware CAD tasks were all found to depend
  on open inputs ([#35](https://github.com/500ft/segmented-shroud-aeromechanics/pull/35)).
- **09-26** Provenance audit of the consequential numbers, with a register that
  CI checks against the code
  ([#34](https://github.com/500ft/segmented-shroud-aeromechanics/pull/34)).
- **09-25** The fine-grid SST rerun could not start: the host ran out of memory,
  and no job was launched
  ([record](../evidence/task-compute-recovery-2026-09-25/README.md)).
- **09-24 to 09-26** External review corrections applied, then copied into the
  documents that had not been reviewed
  ([#30](https://github.com/500ft/segmented-shroud-aeromechanics/pull/30),
  [#31](https://github.com/500ft/segmented-shroud-aeromechanics/pull/31)). The
  A0.1 airfoil verdict became `INCOMPLETE_UNCERTAINTY`: the solver matches
  published reference computations within 0.4%, but one uncertainty component
  was never quantified.
- **09-24** Analysis pipeline for the eventual comparison written and tested on
  synthetic data ([#29](https://github.com/500ft/segmented-shroud-aeromechanics/pull/29)).
  Draft reference geometry, defect basis and comparison conditions
  ([#28](https://github.com/500ft/segmented-shroud-aeromechanics/pull/28)).
- **09-22** Literature catalogue: 1,736 records, of which 11 were read in full
  ([#24](https://github.com/500ft/segmented-shroud-aeromechanics/pull/24)).
  Closest competitors close-read and the claim narrowed
  ([#23](https://github.com/500ft/segmented-shroud-aeromechanics/pull/23)).
- **09-20 to 09-21** A0.1 CFD validation on a 2D NACA 0012 airfoil: grid study
  complete, workflow checked against reference CFD
  ([#21](https://github.com/500ft/segmented-shroud-aeromechanics/pull/21),
  [#22](https://github.com/500ft/segmented-shroud-aeromechanics/pull/22)).

## Week of 2026-09-14

- **09-19** Owner chose to validate the CFD workflow on standard wing cases
  first ([#20](https://github.com/500ft/segmented-shroud-aeromechanics/pull/20)).
- **09-16** Research programme proposed, with four directions and a Study A0
  work order ([#18](https://github.com/500ft/segmented-shroud-aeromechanics/pull/18)).
  Entry documents brought up to date
  ([#19](https://github.com/500ft/segmented-shroud-aeromechanics/pull/19)).
- **09-15** Top 25 literature candidates triaged under a fixed rule: 22 queued
  for close reading, 3 excluded. Measurement-requirements draft
  ([#17](https://github.com/500ft/segmented-shroud-aeromechanics/pull/17);
  plan [#16](https://github.com/500ft/segmented-shroud-aeromechanics/pull/16)).
- **09-14** Checker scripts rewritten and simplified
  ([#12](https://github.com/500ft/segmented-shroud-aeromechanics/pull/12),
  [#13](https://github.com/500ft/segmented-shroud-aeromechanics/pull/13),
  [#14](https://github.com/500ft/segmented-shroud-aeromechanics/pull/14)).

## Week of 2026-09-07

- **09-12 to 09-13** Literature database export re-acquired with a clean query
  log; it recovers 4 of 6 known sources. The coverage record was tightened
  twice ([#7](https://github.com/500ft/segmented-shroud-aeromechanics/pull/7) to
  [#11](https://github.com/500ft/segmented-shroud-aeromechanics/pull/11)).
- **09-11** README and presentation rewrite
  ([#6](https://github.com/500ft/segmented-shroud-aeromechanics/pull/6)).
- **09-09 to 09-10** Search provenance corrected; the candidate question
  narrowed to an equal-mean-clearance seam comparison
  ([#3](https://github.com/500ft/segmented-shroud-aeromechanics/pull/3),
  [#4](https://github.com/500ft/segmented-shroud-aeromechanics/pull/4),
  [#5](https://github.com/500ft/segmented-shroud-aeromechanics/pull/5)).
- **09-07** Research question, specimen schema and CAD plan set up
  ([#1](https://github.com/500ft/segmented-shroud-aeromechanics/pull/1),
  [#2](https://github.com/500ft/segmented-shroud-aeromechanics/pull/2)).
