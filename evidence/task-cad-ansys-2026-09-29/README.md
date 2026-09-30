# CAD–ANSYS execution readiness

Evidence: **executed software check**, not CAD acceptance or a CFD result.
The owner selected the [computational finish line](../../docs/decision-log.md#2026-09-29--finish-as-a-cadansys-computational-study).
This record completes the first execution-route check and identifies the next task.

## Observed result

The configured Windows CAD host was reached over SSH. A read-only inventory found
SOLIDWORKS, Fluent and CFX. Fluent then started in batch mode, obtained its Student
license, connected its compute node, read [the exit journal](exit.jou) and exited.
The launcher returned successfully, and the Fluent-generated transcript independently
shows the journal and clean stop. A [redacted excerpt](startup-excerpt.txt) is retained.

[readiness.json](readiness.json) is the canonical home for host resource measurements,
product version, launch command, timing, license limits, source links and the original
transcript's hash/location. Free memory and disk are time-specific observations, not
reserved capacity. No case was loaded and no performance prediction was produced.

An initial detached launch left empty redirected logs and no transcript. It is retained
as **NOT_VERIFIED**. Keeping SSH attached with PowerShell `Start-Process -Wait`
produced the successful run. Fluent wrote an auto-transcript while stdout/stderr stayed
empty: use that transcript to assess startup rather than relying on the launcher alone.

## Reproduction

Use the private host configuration described by the pinned
[engineering-audit briefing](https://github.com/500ft/engineering-audit/blob/6e55653246ecf39f6b40927a4697d0218027b719/docs/cad_agent_briefing.md);
credentials and host identity are not committed here. The read-only inventory used
PowerShell `Get-CimInstance` for the OS, processor and fixed disks, `Test-Path` for
the installed executables, and `Get-Process` to check for active solver processes.

For startup, create a fresh run directory, copy `exit.jou`, and adapt only the
installation/directory paths in the recorded launch command. Keep the session attached;
capture the launcher status and read Fluent's generated transcript. Do not overwrite
the recorded attempts. `Get-FileHash -Algorithm SHA256` supplied the original transcript
hash; its published excerpt omits machine identity and unrelated banner text.

The launch options follow the [Fluent startup guide](https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/flu_ug/flu_ug_startramp.html).
The [Student product limits](https://ansys.synopsys.com/academic/students/ansys-student)
are recorded as published restrictions, not measured capacity. The native CAD workflow
must supply neutral exports; the Student product's geometry-export restriction is not
an export capability. Nothing here establishes CFD suitability under the mesh ceiling.

## Next task

Verify the existing reference candidate's published rotor geometry and usable comparison
data, resolve the source ambiguities, then register nominal reference/duct inputs and
the clearance convention before building CAD. Execute a baseline geometry import and
mesh-feasibility trial before releasing the defect sweep. Measure the actual memory,
wall time and mesh sensitivity; a startup timing is not a solver-throughput estimate.
If tip-gap resolution cannot fit the license/host, record the failed feasibility result
and a scoped alternative. Do not hide that limit by removing the defect or using a
sector that lacks the actual geometry's symmetry.

## Verification of this change

Run from the repository root with Python 3.11 in a temporary environment installed
from the unchanged `requirements.txt`. Every command below exited successfully:

```text
python scripts/check_repo_contract.py
python scripts/check_quantities.py
python scripts/study_a_design.py --check
python scripts/acquisition_ledger.py --check
python scripts/reference_coverage.py --check
python scripts/clearance_uncertainty_budget.py --check
python -m unittest discover -s tests
python tools/check_presentation.py . "Segmented Shroud Aeromechanics" segmented-shroud-aeromechanics
python tools/test_presentation.py
git diff --check
```

The unit suite passed all 237 tests; presentation negative controls passed all four.
The suite emitted existing unclosed-file `ResourceWarning` messages without failures.
The budget retains `INPUTS_PENDING`. Historical result/source files, requirements,
scripts and tests are unchanged. These checks do not assess aerodynamic accuracy.
Hosted CI is reported on the PR's actual head rather than inferred from these local runs.

No new checker, synthetic fixture, CAD framework, dependency change or solver result
is added. The executed host startup is a separate software-readiness observation.
