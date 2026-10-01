# Review index

What to review, and where each piece of evidence lives. The plan is in the
[roadmap](../ROADMAP.md) and the history in the [progress log](SPRINT_PROGRESS.md).
The earlier, longer version of this index is kept at
[commit e43cb15](https://github.com/500ft/segmented-shroud-aeromechanics/blob/e43cb15109cbe8aab30e3f3befbcc59f1d811a3b/docs/REVIEW_READY.md).

Nothing here has had an independent review.

## Review now

1. **The computational scope decision** ([decision log](decision-log.md#2026-09-29--finish-as-a-cadansys-computational-study))
   and the [roadmap](../ROADMAP.md). Worth checking: whether a useful study
   fits in the Fluent Student limit of 1M cells and 4 cores, and the reasons for
   choosing the Akturk–Camci ducted fan as the reference rotor
   ([decision](decision-log.md#2026-09-30--reference-rotor-the-akturkcamci-ducted-fan)).
2. **The ANSYS readiness record**
   ([record](../evidence/task-cad-ansys-2026-09-29/README.md)). Fluent starts,
   checks out its licence and exits cleanly. No case has been solved.
3. **The A0.1 airfoil validation** ([report](cfd-validation-a01.md)). The
   solver matches published reference computations within 0.4%; the full
   validation uncertainty is incomplete.

## Reproduce

Run the [README quick start](../README.md#quick-start): the repository
contract, the three record checks and the test suite. None of them needs a CAD
licence, solver or hardware.

## Evidence records

**CFD and computation**

| Folder | What it holds |
| --- | --- |
| [task-cad-ansys-2026-09-29](../evidence/task-cad-ansys-2026-09-29/README.md) | CAD host inventory and Fluent startup check |
| [task-compute-recovery-2026-09-25](../evidence/task-compute-recovery-2026-09-25/README.md) | Why the fine-grid SST rerun could not start (host memory) |
| [task-a0-validation](../evidence/task-a0-validation/README.md) | A0 airfoil validation runs, acceptance record and grid study |

**Literature and prior art**

| Folder | What it holds |
| --- | --- |
| [task-literature-repair-2026-09-25](../evidence/task-literature-repair-2026-09-25/README.md) | Corrections to the literature records |
| [task-literature-2026-09-22](../evidence/task-literature-2026-09-22/README.md) | Thematic literature catalogue |
| [task-2026-09-14](../evidence/task-2026-09-14/README.md) | Top-25 candidate triage and measurement-requirements draft |
| [task-2026-09-12](../evidence/task-2026-09-12/README.md) | Reference coverage of the known sources |
| [task-2026-09-11](../evidence/task-2026-09-11/README.md) and the `-clean-network`, `-public` folders | Clean re-acquisition of the database export |
| [task-2026-09-09-review](../evidence/task-2026-09-09-review/README.md), [task-2026-09-09](../evidence/task-2026-09-09/README.md) | Original search and its provenance correction |
| [task-day3-2026-09-09](../evidence/task-day3-2026-09-09/README.md) | Acquisition ledger and reading records |
| [task-2026-09-08](../evidence/task-2026-09-08/README.md) | First-pass source review |

**Setup**

| Folder | What it holds |
| --- | --- |
| [sprint-2026-09-05](../evidence/sprint-2026-09-05/) | First integrity sprint baseline |
| [presentation-2026-09-10](../evidence/presentation-2026-09-10/README.md) | README presentation checks |
