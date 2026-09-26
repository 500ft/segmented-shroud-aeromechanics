# Provenance audit of consequential numbers
Date: 2026-09-25 · Ledger row SSY-R21

Every number that could change a decision should say where it came from. This audit finds where
that chain is broken. It is an audit of **documentation and traceability**, not a re-derivation
of the engineering: no CAD, requirement, acceptance threshold or solver setting was changed by
producing it.

## Scope and method

Swept the decision documents and every module-level constant and defaulted numeric threshold in
`scripts/`. Each finding below was read at its current location rather than recalled. Where this
audit computes something, the computation is shown and labelled.

**Retrospective assessment.** Where a value exists but its original reasoning is not recorded,
this audit assesses the value as it now stands. It does not reconstruct what the author intended,
and an assessment made today is not evidence of the reasoning used then.

## What already exists

The repository has three provenance vocabularies, each scoped to one artifact:

| vocabulary | where | covers |
| --- | --- | --- |
| `VERIFIED_FROM_SOURCE`, `VERIFIED_FROM_ARCHIVE`, `DERIVED_FROM_SOURCE`, `ASSUMED_FOR_MESH_ONLY`, `MISSING` | `evidence/task-a0-validation/source-inventory.json` | A0 case parameters |
| `pending`, `literature_bound`, `measured`, `calibration_record`, `protocol`, `owner_decision` | `docs/clearance-measurement-budget.csv` | clearance budget terms |
| Literature, Planned, CAD, FEA/CFD, Measured | `docs/claim-ledger.md` | project-level claims |

They are good and they stay. **The gap is that nothing covers a number used in more than one
place**, so a repeated quantity has no single definition and no way to detect divergence.

## Findings

Severity: **1** changes a conclusion · **2** changes a margin or a gate · **3** traceability only.

| # | Decision / quantity | Where | Current value | Evidence and its limits | What is missing | Consequence if wrong | Sev | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Stage 2 exit gate: held-out error and improvement over mean-clearance | `proposal.md` §Study D, `analysis_pipeline.py` defaults `min_improvement=0.20`, `max_rel_error=0.10`, `TASKS.md` | 20 % and 10 % | Registered in the roadmap and enforced in code. **No derivation anywhere**: nothing states what decision either number would change | The decision each gate protects, and the smallest difference worth acting on | A study passes or fails on numbers nobody justified. Already flagged provisional by the 2026-09-24 review (R10) and still provisional | 1 | Keep enforcing, label provisional at every appearance, and record what evidence would fix them |
| F2 | Grid-convergence safety factor | `cfd_grid_convergence.py:17` `FS = 1.25` | 1.25 | Sourced to Celik et al. 2008, which prescribes 1.25 **where the observed order is close to formal**. A0.1's observed order is 2.6697 against a formal order near 2, 33 % above it. The condition is never checked and the order is never limited | A stated applicability test, and a rule for when the observed order is far from formal | Numerical uncertainty is scaled by an unjustified factor. **Quantified below: it does not change the A0.1 conclusion** | 2 | Record the sensitivity and the unchecked condition beside the result |
| F3 | Convergence criterion | `cfd_grid_convergence.py:24-25` `PLATEAU_REL = 1e-4`, `PLATEAU_WINDOW = 500` | 1e-4 over 500 iterations | Selected. **Sensitivity now computed, 2026-09-26** (see below) | A stated tolerance on the reported quantity, from which the criterion could be derived | Decides `PASS` against `UNCONVERGED`. Less than one order of headroom, and it does **not** distinguish a run that failed from one that stopped too early to judge | 2 | Sensitivity done; the selection itself is still undesived |
| F4 | Identifiability and rank tolerances | `analysis_pipeline.py` `RANK_TOL = 1e-10`, `tol=1e-9`, `collinearity_tol=1e-8`, `AMPLITUDE_EPS = 1e-9` | as listed | Selected numerical tolerances | Justification and sensitivity | They decide whether a descriptor is refused as unidentifiable, which silently changes the model that gets fitted | 2 | Label as selected; note that `RANK_TOL` is relative to the largest singular value |
| F5 | Freestream turbulence quantities | `make_case.py:20-22` | `K_INF = 9e-9·a²`, `OMEGA_INF = 1e-6·a²/ν`, `NUTILDA_INF = 3ν` | The module docstring says these follow the TMR specification and are not guesses, and an independent check converted them to an eddy-viscosity ratio of 0.009 before any case ran. Good provenance, but **not carried in a machine-readable label** | A provenance label alongside the constants | Low: the values are traceable in prose | 3 | Cross-reference the canonical register |
| F6 | Experimental reference and angle | `cfd-validation-a01.md` | `Cl = 1.07502` at `10.12°` | Measured input from the source of record; the angle is the measured one specifically so the experiment is never interpolated. Well provenanced | Nothing | None | 3 | Register as the canonical measured input |
| F7 | Experimental standard uncertainty for A0.1 | `cfd-validation-a01.md`, `uncertainty.revision-2026-09-25.json` | **does not exist** | The 0.00441 grit spread is a treatment sensitivity and is not eligible. Correctly refused by the tool since 2026-09-25 | A source that reports experimental uncertainty, or a measurement model | The comparison against the experiment cannot be completed at any mesh density | 1 | Already recorded; no further action in this audit |
| F8 | Study A factor ranges | `candidate-design-2026-09-25.json` | `F_low`, `F_high`, `s_high` all open | Correctly marked open; the design is dimensionless and no constraint can be evaluated | Owner inputs | No physical level can be set and no run released | 1 | Already tracked; register the identifiers |
| F9 | Owner inputs IN-01 to IN-12 | `measurement-system-spec.md` §5 | unset | Correctly pending. IN-01's derivation from IN-03 was withdrawn 2026-09-25 | Owner decisions | Budget stays `INPUTS_PENDING`, no instrument qualified | 1 | Already tracked |
| F10 | Synthetic fixture constants | `make_synthetic_fixtures.py:106-107` | `C_BAR_TARGET = 1000.0`, `noise_W = 0.35` | Labelled synthetic and not evidence throughout | Nothing, but `1000.0 µm` is a plausible real mean clearance and could be misread as a target | Someone could cite a fixture constant as a project value | 3 | Note explicitly that it is not IN-02 |
| F11 | Benchmark transfer ratios | `validation-scope-map.md` | Mtip ≈ 0.30, Re ≈ 4.3e5, gap ratios | Derived by this project from the paper's own numbers, already labelled derived and listed as absent from the source | Nothing | None | 3 | Register with a `derived` provenance |
| F12 | No canonical register | repository-wide | — | Three partial vocabularies, none covering a repeated quantity | One definition per repeated quantity, with a checker | Two documents can state different values for the same thing and nothing notices | 2 | **Implemented by this work** |

## The three kinds of gap, kept apart

- **Missing documentation for a supported decision:** F5, F6, F11. The reasoning exists; only a
  machine-readable pointer is absent.
- **Needs engineering justification:** F1, F2, F3, F4. A number is in force and nothing derives it.
- **Cannot be assessed yet:** F7, F8, F9. The input does not exist, so no analysis closes them.

## Retrospective assessment: the safety-factor choice (F2)

**Question.** Does the unchecked applicability condition on `FS` change any A0.1 conclusion?

**Inputs**, all read from the committed record, none re-solved:

| quantity | value | provenance |
| --- | --- | --- |
| fine, medium, coarse lift | 1.098833, 1.091606, 1.045623 | calculated result, committed |
| refinement ratios | r21 = r32 = 2.000 | selected grid family |
| observed order | 2.6697 | calculated result |
| formal order of the scheme | ≈ 2 | sourced |
| comparison error, absolute | +0.023813 | calculated result |

**Model.** The Celik three-grid index, `GCI = FS·e_a21 / (r21^p − 1)`, with `e_a21` the relative
difference between the two finest grids. It applies because three systematically refined levels
exist at a refinement ratio above 1.3 and convergence is monotonic.

**Sensitivity** across the defensible choices:

| choice | fine-grid index |
| --- | --- |
| as reported, p = 2.6697, FS = 1.25 | 0.153 % |
| p = 2.6697, FS = 3.0 | 0.368 % |
| p limited to formal 2, FS = 1.25 | 0.274 % |
| p limited to formal 2, FS = 3.0 | 0.658 % |

**Unit check.** Every entry is a dimensionless fraction of the fine-grid lift, as is the
comparison error, so the two are comparable.

**Result.** The index spans a factor of 4.3 across these choices. The comparison error is
**2.22 %** of the reference, which is between 3.4 and 14.5 times the largest of them.

**Decision.** The A0.1 conclusion does not turn on the safety factor. It is recorded as an
unjustified selected value with its condition unchecked, and it is **not** treated as a defect in
the result. Note separately that with `U_input` unquantified there is no validation uncertainty
at all, so this term is not the binding constraint on the comparison in any case.

**Validation.** None required. This is arithmetic on committed values, reproducible from the
record. It is **not** physical validation of anything.

## What this audit does not claim

It does not make any prediction in this repository a measurement, and it does not close any
research task. A complete provenance chain around an unresolved decision leaves the decision
unresolved.

## Follow-up, 2026-09-26: the convergence criterion (F3)

**Question.** Would a different flatness criterion reclassify any recorded A0.1 case?

**Method.** Re-ran the criterion over the committed convergence histories at a grid of tolerances
and windows. No solver was run. Record:
[`convergence-sensitivity-2026-09-26.json`](../results/generated/cfd/a0.1/convergence-sensitivity-2026-09-26.json),
reproduced from the histories by `tests/test_convergence_sensitivity.py`.

**Limitation, which governs every number here.** The committed histories are downsampled to about
one sample per 50 iterations, so each spread is a **lower bound** on what the full history would
show. Pass verdicts are therefore optimistic. Failures and unassessable runs are sound.

**Results.**

| case | recorded | spread over the last 500 iterations | flips at 1e-5 | flips at a 2000-iteration window |
| --- | --- | --- | --- | --- |
| `g1_SA` | PASS | 1.23e-05 | **yes** | no |
| `g1_SST` | PASS | 9.26e-08 | no | no |
| `g2_SA` | PASS | 3.32e-06 | no | no |
| `g2_SST` | PASS | 1.29e-05 | **yes** | no |
| `g3_SA` | PASS | 2.20e-05 | **yes** | **yes** |
| `g3_SST` | UNCONVERGED | not assessable | — | — |

**Three findings.**

1. **Loosening changes nothing.** Every passing case still passes at 1e-3, so no result depends
   on the criterion being as strict as it is.
2. **The headroom is under one order of magnitude.** Three of five passing cases fail at 1e-5,
   with spreads between 1.2e-05 and 2.2e-05 against a 1e-4 threshold. The criterion is closer to
   its margin than its round value suggests, and the window matters too: `g3_SA` also fails when
   the window is lengthened to 2000 iterations.
3. **The stalled case was never assessed, not assessed and failed.** `g3_SST` reached iteration
   117, well short of a single 500-iteration window, so the criterion could never be applied. It
   is recorded as `UNCONVERGED`, which reads as a judgement that was never made. This is the same
   distinction the [compute-recovery record](../evidence/task-compute-recovery-2026-09-25/README.md)
   flagged as unresolved, and it is now resolved: the run terminated before assessment.

**Decision.** The criterion stays as it is: no recorded conclusion changes, and altering it after
seeing results is the move the acceptance discipline forbids. Both values remain **selected**, now
with their sensitivity recorded rather than unknown. The status vocabulary should gain a third
term so a terminated run is not reported as a failed one; that is registered, not done here.

**Validation.** None. This is arithmetic on committed histories and is not physical validation.
