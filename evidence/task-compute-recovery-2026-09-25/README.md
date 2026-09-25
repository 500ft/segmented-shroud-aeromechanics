# A0.1 fine-grid SST recovery: decision record
Date: 2026-09-25 · Lane C1 · Ledger row SSY-R20

**Outcome: BLOCKED, with the barrier diagnosed. No solver job was launched.** A job launched is
not a job completed, and on this evidence a job launched today would not complete.

D10 is **not** a prerequisite for this work item. D10 governs A0.2. This recovery's prerequisites
are case identity, checkpoint integrity, resource headroom and the existing A0.1 run protocol.

## 1. What the prior attempt recorded

| case | status | cells | mesh sha256 | image digest |
| --- | --- | --- | --- | --- |
| `g1_SST_a10.12` | PASS | 3584 | `eb1260dee8c128d3…` | `sha256:33fb575aa998…` |
| `g2_SST_a10.12` | PASS | 14336 | `2d17abcdc49389d9…` | `sha256:33fb575aa998…` |
| `g3_SST_a10.12` | **UNCONVERGED** | 57344 | `851e63ada6efcf68…` | `sha256:33fb575aa998…` |

Two of three levels converged. Two levels cannot carry an apparent order or a grid-convergence
index, so this arm has no verdict and the model-form sensitivity for A0.1 stays unmeasured.

The manifest records the stop as unconverged. It does **not** by itself separate an iteration
ceiling from a genuine convergence failure, and the earlier diagnosis of host memory exhaustion
was made from live observation rather than from a preserved log. That residual diagnostic
uncertainty is recorded rather than resolved.

## 2. Resume is not available

No checkpoint, no mesh and no raw solver output survive. Searched: no `polyMesh` directory, no
`*.msh`, no `postProcessing/.../coefficient.dat` anywhere on this host. What survives is the
committed manifests and convergence summaries.

A restart would therefore be a **fresh run**, not a resume. It is possible in principle because
the inputs survive: the three Plot3D grids are in `evidence/task-a0-validation/tmr-grids/`, the
finest being `n0012_449-129.p2dfmt.gz`, and the solver image is pinned by digest.

**Case identity condition.** A regenerated mesh must hash to `851e63ada6efcf68…`. If it does not,
the new run is a different case and may not be combined with the existing `g1` and `g2` results
into one grid family. That check comes before any solve.

## 3. Why not today: host resources

Measured on this host at the time of writing.

| quantity | value |
| --- | --- |
| physical memory | 16.0 GB |
| free | 0.08 GB |
| inactive, reclaimable | 2.43 GB |
| wired | 3.48 GB |
| occupied by the compressor | 6.91 GB |
| effectively available | ≈ 2.5 GB |
| swap used | 20.75 GB of 21.50 GB |
| disk free | 28 GB |
| active container runtime | Docker Desktop context `desktop-linux`; `colima` reports not running |

Swap is 96 percent consumed and 6.9 GB sits compressed. **This is worse than the state in which
the fine grid originally stalled.** Starting a 57344-cell shear-stress-transport solve now would
compete for memory the host does not have, and the most likely outcome is a repeat of the
original failure plus disruption to unrelated work already resident in that swap.

No resource setting was changed and no process was terminated to make room. Doing either silently
would be the wrong trade against someone else's running work.

## 4. What would make this runnable

1. Host memory headroom measured, not assumed, with the machine otherwise quiet.
2. The container runtime deliberately chosen and started, rather than inherited from whichever
   context happens to be active.
3. Mesh regenerated from the surviving Plot3D input and its hash checked against the recorded
   value **before** the solve.
4. A new attempt record referencing the failed one, which is preserved rather than replaced.
5. Declared convergence and resource stopping rules, so the run stops on a rule rather than
   because an output file appeared.
6. Peak memory and elapsed time recorded for the cost model, since A0.1 timings are the only
   throughput evidence this project has and they are a smoke test, not a calibrated rate.

## 5. What completing it would and would not establish

It would give the SST arm three usable levels, an apparent order, an index, and a measured
model-form sensitivity between the two turbulence models.

It would **not** produce an experimental validation. A0.1 has no experimental standard
uncertainty: the grit spread is a treatment sensitivity and is not eligible to supply it. The
comparison against the experiment stays unresolved however many grids finish.
