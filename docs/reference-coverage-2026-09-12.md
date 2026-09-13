# Reference coverage and seam-experiment distinctness — 2026-09-12 (SSY-R02)

Answers the sprint question *"is the proposed equal-mean-clearance seam experiment sufficiently
distinct?"* with a source-coverage report and an evidence-backed comparison of seams against other
clearance defects. Inaccessible details are left explicitly unresolved. No novelty, patent or owner
gate is closed by this.

## 1. Source coverage — every day-1 reference accounted for

`docs/source-eligibility-register.json` lists all 10 day-1 sources with resolved identifiers and an
eligibility decision; `scripts/reference_coverage.py` computes recall over eligible sources against
both exports under every DOI alias, and `--check` gates the committed result.

| | count | ids |
|---|---:|---|
| day-1 sources | 10 | S1–S10 |
| eligible for a scholarly-database export | 6 | S1–S6 |
| not eligible (stated, not dropped) | 4 | S7 NTRS report without DOI · S8–S10 patents |
| **recovered by day-2 historical export** | **4/6** | S1, S2, S3, S5 |
| **recovered by day-4 public export** | **4/6** | S1, S2, S3, S5 |
| missed by both | 2 | S4 (MDPI *Vehicles*), S6 (MDPI *Sensors*) |

**Correction to earlier figures.** Day 2 reported 1/6 and day 4 reported 3/3. The anchor sets were
incomplete and unequal: S3's DOI (`10.1016/j.ast.2026.111933`) had to be resolved from its PII, S6's
(`10.3390/s18082610`) from its PMC page, and S2's day-1 link carries PII `…7624` where Crossref's is
`…7629` (recorded, not altered). Both exports in fact returned S1, S2, S3 and S5. The historical
export's unlogged-provenance defect is unchanged and it stays rejected; this corrects the count.
Both MDPI items were missed by both routes — the one *named* "segmented ducted fan" among them.

## 2. Seams versus other clearance defects — what the sources establish

Reading records for all 10 sources are in `docs/day3-reading-records.json` (S1 and S6 read in full
text with hashes; S4 and S5 from complete publisher abstracts; S3 inaccessible; S7, S9, S10 stand on
their day-1 reads). Rubric: `docs/day3-reading-rubric.md`.

| defect class | what is established | source · grade | relation to the proposed seams |
|---|---|---|---|
| Uniform clearance sweep, ducted fan | Thrust and FOM fall with t/h from 1.80 % to 7.62 %; CFD sweep, wind-tunnel verification of the **baseline only**; all cases axisymmetric | S1 §2–3, Figs 10–14 · B | Baseline physics, not a competitor: no nonuniform or discrete case |
| Continuous nonuniform clearance (ovalization, blade-height variation) | Second-harmonic circumferential distributions change compressor performance (title/abstract; full text not read) | S2 · abstract-only | Nearest *continuous* analogue. Whether it holds mean clearance fixed is **unresolved** |
| Nonuniform clearance *layouts*, compressor, 2026 | Title only; paywalled | S3 · inaccessible | Could be the closest competitor on axis 1. **Unresolved until read** |
| Axially segmented duct (gaps between duct sections) | CFD only, 20–40 krpm, spacing 0–20 mm; acoustic power rises with gap; recommends ≤ 10 mm; no measurement; cannot resolve transients | S4 abstract · C | **Same word, different geometry.** Axial gaps, not circumferential seams at equal mean radial clearance. Must be cited and distinguished by name |
| Generic segmented/split duct disclosure | Segmentation disclosed; equal-mean-seam effect and guard claims not established by the inspected claim | S8 claims (day 3) | Prior disclosure of the *mechanism*, not of the aerodynamic question |
| Clearance metrology | Fibre and microwave sensors resolve < 25 µm at 2–5 mm standoff in rotating rigs | S5 abstract, S6 full text, S7 day-1 · B/C | **Enables the matched control**: "equal mean clearance" can be *measured* per seam, not assumed |

## 3. Distinctness verdict, bounded

On the inspected material the proposed experiment — *fixed mean tip clearance, discrete
circumferential seam count as the manipulated variable, measured (not simulated) aerodynamic
response, with a smooth-duct control at the same measured mean clearance* — is distinct from every
source read in full or in abstract: S1 is uniform, S4 is axial segmentation by CFD, S5–S7 are
instruments, S8 is a mechanism disclosure. The distinctness rests on three things the experiment
must actually do: hold and **verify** mean clearance with a sensor of the S5/S6 class, use
circumferential seams rather than axial gaps, and measure rather than simulate.

**Two sources could still collapse axis 1 and are unresolved:** S3 (2026 nonuniform *layouts*,
paywalled) and S2's full text (whether its second-harmonic comparison is at fixed mean clearance).
Neither can be read from this environment; both need institutional access. Until then the claim is
"distinct from all accessible prior work", not "distinct from prior work".

## 4. Explicitly unresolved
- S3 full text; S2 full text; S4 full text (mdpi.com returns 403 to this client — not circumvented; the abstract is complete).
- Patent claims S8–S10 were read as public text on day 1; not legal clearance.
- Day-4 public export flagged `10.1016/j.ast.2023.108866` as an anchor; that is S2, now recorded under its DOI.


## Review repair (SSY-R02b, same day) — one provenance-bound record, axes tied to inspection

**Provenance.** Coverage now credits an export only for hits traceable to a logged successful query. The 2026-09-09 export has 50 of 499 rows with no such line (all arXiv, from the throttled re-run); they are excluded from credit and the export is marked **rejected** and retained. The 2026-09-11 public export is provenance-clean (450/450) and is the **canonical** record. Recall is unchanged by the exclusion — none of the anchor hits was among the untraceable rows — but the number is now bound to what the export can show it searched. `SSY-D02` is closed against this record; no successor task was created.

**Novelty axes, by inspection status.** `narrowed_by_disclosure` = an inspected source discloses the axis; `supported_bounded` = no inspected source discloses it, with the unresolved sources named; nothing is "supported" by an abstract.

| axis | status | disclosed by | not found in inspected sections of | unresolved for |
|---|---|---|---|---|
| `equal_mean_seams` | **supported_bounded** | — | S1, S8 | S2 |
| `guard_validation` | **supported_bounded** | — | S1, S8 | — |
| `equal_mean_clearance_discrete_seams` | **supported_bounded** | — | S1, S6 | S3, S4, S5, S7 |
| `measured_vs_cfd` | **supported_bounded** | — | S1, S6 | S3, S4, S5 |
| `generic_segmentation` | **narrowed_by_disclosure** | S8 | — | — |
| `deployment_vs_fixed` | **supported_bounded** | — | S6 | S3, S4, S5 |
| `matched_controls` | **supported_bounded** | — | S6 | S3, S4, S5, S7 |
| `held_out_prediction` | **supported_bounded** | — | S6 | S3, S4, S5 |
| `guard_claims` | **supported_bounded** | — | S6 | S3, S4, S5 |

What this measures: overlap with a small known-reference set and disclosure in the sections inspected. It is not exhaustive literature recall and not established novelty.

**Matched-clearance feasibility (Stage A as a computation).** `scripts/clearance_uncertainty_budget.py` evaluates the experiment's own stop rule — k·u_c < minimum effect of interest — over `docs/clearance-measurement-budget.csv`. The S5/S6 sensor accuracy (≤ 25 µm) is carried as a `literature_bound` and **never enters the combination**: a published sensor class does not establish achievable uncertainty on this rotor and fixture. Five project terms (in-situ sensor calibration, dynamic runout, thermal growth, fixture deflection under thrust, seam-setting repeatability) plus the target mean clearance and the minimum effect of interest are `pending`, so the verdict is `INPUTS_PENDING`; the SSY-S08 sitting fills them. Nothing is estimated in their place. `FEASIBLE`, when reached, is a budget verdict and authorises no rotor test.
