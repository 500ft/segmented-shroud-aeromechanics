# Traceability index
Date: 2026-09-25 · Ledger row SSY-R21

One row per consequential decision: what it answers, where its reasoning lives, which registered
inputs it depends on, and what would validate it. **No equation is repeated here.** Follow the
link to the analysis; this page only says where to look and how far the evidence goes.

Status vocabulary: **supported** means the reasoning is recorded and its inputs exist ·
**provisional** means a value is in force that nothing derives · **blocked** means a required
input does not exist · **unresolved** means it is open by decision.

| Decision | Objective it serves | Reasoning lives in | Registered inputs | Validation | Status |
| --- | --- | --- | --- | --- | --- |
| A0.1 numerical uncertainty | Bound solver error before any comparison | [validation report §3](cfd-validation-a01.md) | `GCI-SAFETY-FACTOR`, `PLATEAU-RELATIVE`, `PLATEAU-WINDOW` | Three converged grids, order computed not assumed. Sensitivity to the factor recomputed by test | **supported**, with the factor's condition unchecked and its effect shown not to matter |
| A0.1 comparison against experiment | Establish whether the workflow reproduces the measurement | [validation report §4](cfd-validation-a01.md) | `A01-REFERENCE-LIFT`, `A01-REFERENCE-ANGLE`, `A01-GRIT-SPREAD` | Cannot complete: no experimental standard uncertainty exists | **blocked** — verdict `INCOMPLETE_UNCERTAINTY` |
| A0.1 SST model-form sensitivity | Separate turbulence-model error from mesh error | [validation report §5a](cfd-validation-a01.md), [recovery record](../evidence/task-compute-recovery-2026-09-25/README.md) | `PLATEAU-RELATIVE`, `PLATEAU-WINDOW` | Two of three grids only; restart diagnosed and blocked on host memory | **blocked** |
| A0.2 solver regime (D10) | Decide whether sectional pressure can support a claim | [plan D10](specs/research-programme/plan.md), [case definitions](specs/research-programme/a0-validation-cases.md) | — | Compressible workflow recommended, not adopted | **unresolved**, owner decision |
| What each validation case may be cited for | Stop a case supporting more than it tested | [scope map](specs/research-programme/validation-scope-map.md) | — | Assessment complete even where evidence is absent | **supported** |
| Scale bridge to a small rotor | Transfer any computed sensitivity to hardware | [scope map §4](specs/research-programme/validation-scope-map.md) | — | Ratio table with every small-rotor entry open | **blocked** — no evidenced bridge exists |
| Study A factor structure and run count | Know what the experiment can estimate | [candidate design](specs/research-programme/study-a-candidate-design.md) | design file, physical levels open | Rank, conditioning and aliasing audited; manufactured surfaces recovered by test | **supported as a dimensionless candidate**, physical levels **blocked** |
| Study A acceptance gates | Decide whether a defect-aware model earns its place | [proposal, Study D](specs/research-programme/proposal.md) | `GATE-IMPROVEMENT`, `GATE-RELATIVE-ERROR` | None. Enforced in code, derived nowhere | **provisional** |
| Descriptor identifiability | Refuse a model whose coefficients cannot be estimated | [analysis pipeline](../scripts/analysis_pipeline.py) | `RANK-TOLERANCE` | Exactly dependent and near-dependent designs both refused, by test | **supported** |
| Steady versus transient claim | Say when a screening trend may be believed | [transient acceptance](specs/research-programme/transient-acceptance.md) | — | Branches tested on synthetic inputs; numerical tolerance `TOLERANCE_NOT_FROZEN` | **provisional** by design, pending the effect size |
| Attempt dispositions and yield denominator | Stop survivor-only reporting | [dispositions](../scripts/ingestion_dispositions.py) | — | Eight required behaviour cases tested | **supported as a contract**, no measurement exists |
| Clearance-setting requirement (IN-01) | Size the metrology | [proposal, Study B](specs/research-programme/proposal.md) | IN-01 to IN-03, unset | Derivation from a large-rotor derivative withdrawn | **blocked**, owner decision |
| Sensor method selection | Choose how clearance is measured | [proposal, Study C](specs/research-programme/proposal.md), [budget](clearance-measurement-budget.csv) | budget register | Universal kill threshold withdrawn; per-method installed plans required | **blocked** |
| Novelty position | Say what this work contributes | [literature review](literature/README.md), [claim ledger](claim-ledger.md) | — | Claim boundary frozen; the equal-mean method is refuted as a contribution | **supported**, and narrower than it was |

## Where the provenance vocabularies live

| register | governs | checked by |
| --- | --- | --- |
| [canonical quantities](canonical-quantities.json) | numbers used in more than one place, or that gate a decision | `scripts/check_quantities.py`, `tests/test_canonical_quantities.py` |
| [A0 source inventory](../evidence/task-a0-validation/source-inventory.json) | A0 case parameters recovered from sources | `tests/test_cfd_records.py` |
| [clearance budget](clearance-measurement-budget.csv) | measurement uncertainty contributors | `scripts/clearance_uncertainty_budget.py` |
| [claim ledger](claim-ledger.md) | what may be said out loud, and on what evidence | review |
| [reading records](reading-records-2026-09-25.json) | literature access status and evidence grade, kept on separate axes | `tests/test_literature_repair.py` |

These are deliberately separate. Each governs one kind of artifact, and merging them would make
every one of them vaguer.

## What a complete row does not mean

A decision can be fully traceable and still wrong, and an unresolved decision with a complete
provenance chain is still unresolved. Nothing in this index is physical validation: this project
has made **no measurement**, so no row can be marked as physically tested.
