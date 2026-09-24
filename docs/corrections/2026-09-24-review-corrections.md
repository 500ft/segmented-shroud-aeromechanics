# Correction record — 2026-09-24

An external review of `main` and of the then-open PRs #28 and #29 reproduced several errors by
counterexample. This record states what was wrong, what changed, and what was deliberately left
alone. **No raw run, solver output, or frozen acceptance record was rewritten.** The original
calculations stand; their interpretation is corrected in place with this record as the pointer.

| # | What was wrong | Where | Now |
| --- | --- | --- | --- |
| 1 | A universal "2 percent floor" for seam effects, inferred from a disagreement in two-dimensional airfoil lift | A0.1 report, literature review, design contract | **Withdrawn.** Different quantity, geometry and conditions; errors in a paired comparison may cancel, differ or compound. Replaced by a requirement that Study A assess its own paired difference. |
| 2 | `U_val` reported as a number while a required component was unquantified | uncertainty record, analysis script, A0.1 report | `U_val` is **null** when a component is missing; the missing ones are named; the combination of known terms is reported as partial. Verdict is `INCOMPLETE_UNCERTAINTY`. |
| 3 | Spread across grit treatments called repeatability | A0.1 report, acceptance record | Reclassified as **treatment sensitivity**: different trips are different conditions, not repeats. |
| 4 | The asymptotic-range ratio presented as confirmation | analysis script, A0.1 report | It is algebraically `\|phi_fine/phi_medium\|` for equal refinement with a fitted order. **Diagnostic only**, gates nothing, and a test pins the identity. |
| 5 | "Every published code misses this experiment by more than this work does" | A0.1 report | **False.** The report's own table gives SST references at 1.40 and 1.98 percent, below this work's 2.24 percent. Corrected to the claim the table supports. |
| 6 | The harmonic-fit intercept labelled the mean clearance | analysis pipeline | On a masked domain the basis is not orthogonal to the constant: 100 against 98 on the reviewer's case. The wall mean is now an angle-weighted integral, reported beside the intercept. |
| 7 | A baseline of intercept plus mean clearance | analysis pipeline | Rank-deficient exactly when the proposed equal-mean experiment runs. Falls back to intercept-only where clearance does not vary. |
| 8 | Row-first error scoring; splits that could share a specimen | analysis pipeline | Specimen-first scoring; the split reports whether specimens are disjoint. |
| 9 | Only two outcomes, so an unresolved effect read as a null | analysis pipeline | Three outcomes. An effect inside its own uncertainty is `INCONCLUSIVE`; equivalence needs a bound declared in advance. |
| 10 | Seam count varied at fixed width, confounding count with open area | design contract, pipeline descriptors | Count, individual width and total opening are separate; two named contrasts, with fixed-opening redistribution primary. |
| 11 | "Matched thrust" unqualified | design contract | **Matched total assembly thrust** with one declared force boundary, since the shroud carries force itself. |

## Not changed, and why

The A0.1 grid study, its runs and its numbers are untouched: the arithmetic was right and only its
interpretation was over-reached. The original acceptance record is not retuned to obtain a pass.
The Caradonna–Tung baseline decision stands as the owner's, with the transfer limitation recorded
rather than the decision reversed.

## Still open after this correction

The design matrix, its aliasing and run count are unregistered. The scale bridge from the large
computational rotor to a small physical one needs evidence rather than assertion. The 20 percent
improvement and 10 percent error gates remain provisional engineering choices. Graf et al. (1997)
is recorded on its indexed abstract only and remains unread here, so no absence claim about
discrete seams follows from it.
