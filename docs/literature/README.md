# Literature

A catalogue of every source this project has identified, and a review of what the identified work does and does not settle. Built 2026-09-22.

**Read this first.** Of 1,736 distinct records, **11 have been read**, 24 carry a one-line disposition from an abstract, and 1,701 are records a logged query returned and nothing more. A record appearing below means it exists, its identifier resolves, and it looks relevant. It does not mean anyone has read it. Every entry carries its state, and the review says plainly where a claim rests on a title.

| state | meaning | count |
| --- | --- | ---: |
| `close_read` | a full or sectioned read exists with a locator and per-axis states | 11 |
| `triaged` | a 2026-09-14 disposition exists, from title or abstract only | 24 |
| `identified` | returned by a logged query; nothing more | 1,701 |

The machine-readable catalogue is [register.json](register.json). Rebuild it with `python scripts/literature_register.py --extension <export dir> --out docs/literature/register.json`.

## How the corpus was built

Three corpora, merged and deduplicated by canonical identifier.

1. **The day-1 screened set**, 10 sources, in [source-eligibility-register.json](../source-eligibility-register.json). These are the only sources with close readings.
2. **The frozen 2026-09-09 query set**, 450 records in the [canonical public export](../../evidence/task-2026-09-11-public/database-export.json). Six query themes, all about tip clearance, shroud seams, foldable ducts and clearance metrology. 25 were triaged; **111 more qualify under the same filter and have never been screened**.
3. **A thematic extension, 2026-09-22**, 1,377 records across eight themes the frozen set never reached. It reuses the repository's existing search machinery, so every record carries raw response text, a response hash, a per-query rank and a query log that distinguishes an error from a genuine zero. Its audit is clean on all six checks. Evidence: [task-literature-2026-09-22](../../evidence/task-literature-2026-09-22/).

Two honest limits on the extension. **One query leg failed** with HTTP 429 (`rotor guard impact protection unmanned aerial vehicle`, OpenAlex), recorded as an error rather than a zero, so the guard theme is under-sampled. And **citation counts could not be retrieved**: both Crossref and OpenAlex were rate-limiting this machine during the run, so ranking below uses the databases' own relevance rank and the exporter's concept score, not impact.

## 1. Tip-clearance sensitivity in ducted fans and shrouded rotors

*Why it matters:* the baseline premise of the whole project. The claim ledger already records this as established and forbids claiming it as new.

The strongest small-scale work sits in the Vertical Flight Society and AHS literature, which **the frozen query set never reached** — a real gap the extension closed.

| record | year | contributes | state |
| --- | --- | --- | --- |
| `doi:10.4050/vfs-f60-000155` | 2004 | Hover performance of a small-scale shrouded rotor for MAVs. The retained abstract names diffuser divergence angle, inlet lip radius and **blade tip clearance** as design variables at Reynolds numbers of 20,000–30,000 — the regime this project works in, and far below the compressor literature. | identified |
| `doi:10.1115/1.4023468`, `doi:10.1115/gt2011-46356` | 2013, 2011 | Ducted-fan VTOL UAV tip-clearance baseline, journal and conference versions of one study. | triaged |
| `doi:10.1115/1.4023469` | 2013 | Part II: CFD-designed tip treatments varied in chordwise location and circumferential width, with experimental verification. | triaged |
| `doi:10.4050/vfs-f66-000338` | 2010 | Tip clearance **and inlet flow distortion** together in a ducted fan. Verified to exist; not in the corpus, because no query reached it. | not in corpus |
| `doi:10.2514/1.c031477`, `doi:10.4050/jahs.56.042004` | 2012, 2011 | Shrouded-rotor MAV performance and flight testing in edgewise flow and gusts. | identified |
| `doi:10.1016/j.ast.2020.105895` | 2020 | Aerodynamic performance assessment of a ducted-fan UAV for VTOL. | identified |

*Unknown:* whether any of these hold mean clearance fixed while changing its distribution. None has been read for that.

## 2. Non-uniform clearance: circumferential versus axial

*Why it matters:* this is the competitive space, and it is where the claim has already been narrowed once.

**Settled against us.** A close read of `doi:10.1016/j.heliyon.2024.e25296` found it designs its cases "to control the circumferential leakage area of the tip gap to be the same as that of uniform type". Holding an equivalent clearance measure fixed while redistributing the gap **is already published**, and the [claim ledger](../claim-ledger.md) now forbids presenting the method as a contribution. Its variation is axial along the chord, on a transonic compressor stage, CFD-only for the nonuniform cases.

**The most important unread record in the whole corpus:**

| record | year | why it is first in the queue | state |
| --- | --- | --- | --- |
| `doi:10.1016/j.ast.2023.108162` | 2023 | *Effects of **circumferentially** non-uniform clearance on the spanwise flow characteristics in a transonic compressor rotor.* Circumferential, not axial. This is closer to the project's question than anything previously found, including the source that already narrowed the claim. **No abstract was retained; the judgement rests on the title.** | identified |
| `doi:10.1115/97-gt-406` | 1997 | Non-axisymmetric tip clearance on compressor performance and stability; the abstract states stall-margin loss exceeded an average-clearance estimate and that the circumferential length scale mattered. Attempted 2026-09-21 and **not obtainable**. | triaged |
| `doi:10.1115/2000-gt-0416` | 2000 | Analytical flow redistribution from asymmetric tip clearance. Not obtainable. | triaged |
| `doi:10.1016/j.ast.2026.111933` | 2026 | The day-1 source S3, nonuniform clearance layouts, paywalled since 2026-09-12 and still unread. | identified |

There is a coherent body of *Aerospace Science and Technology* papers on non-uniform clearance. Two of them are unread and either could narrow the claim further.

*Unknown, and load-bearing:* whether any circumferential study uses **discrete seams** rather than a smooth distribution, and whether any holds the mean fixed. Until those are read, "distinct from accessible prior work" is the strongest permitted phrasing.

## 3. Casing treatment: the adjacent literature nobody flagged

*Why it matters:* a circumferential groove in a casing is a deliberate, discrete, circumferential geometric feature near the blade tip. That is geometrically close to a seam, even though the intent is opposite — grooves are added to improve stall margin, seams are a defect to be tolerated. This literature was **not** in the project's prior-art map and the extension surfaced it.

| record | year | contributes | state |
| --- | --- | --- | --- |
| `doi:10.1115/gt2023-101077` | 2023 | Compares axial and circumferential casing grooves in a transonic compressor, with stall-margin gain weighed against efficiency penalty near design. | identified |
| `doi:10.1115/1.4025575` | 2013 | A **single** circumferential groove: influence of its location and depth on flow instability. Single-feature sensitivity is directly analogous to single-seam sensitivity. | identified |
| `doi:10.21014/acta_imeko.v10i1.874` | 2021 | Single mid-chord groove in a linear cascade **at different tip clearances**, RANS, loss generation. | identified |

*Consequence:* the project should decide explicitly whether it cites this body. If a groove at a given clearance behaves like a seam, the novelty argument needs to address it; if not, the reason belongs in the prior-art boundary.

## 4. Dynamic clearance metrology

*Why it matters:* feeds open input **IN-09**, the dynamic-clearance method, and the five installed uncertainty contributors **IN-06**. The measurement-requirements draft says a published sensor class never establishes achievable uncertainty on this rotor and fixture.

| record | year | sensing route | state |
| --- | --- | --- | --- |
| `doi:10.3390/s130607385` | 2013 | Optical fibre bundle for clearance **and** tip timing in a turbine rig. Same class as day-1 source S5. | identified |
| `doi:10.29008/etc2017-217` | 2017 | High-temperature eddy-current clearance system. | identified |
| `doi:10.1016/j.measurement.2026.122186` | 2026 | Eddy-current and fibre-optic **composite** sensor, simultaneous clearance and vibration. | identified |
| `doi:10.3390/s17051097` | 2017 | Microwave blade tip timing. | identified |
| `doi:10.1016/j.measurement.2024.115777`, `doi:10.2139/ssrn.4820937` | 2025, 2024 | Blade tip timing accounting for speed variation and blade-by-blade clearance. Journal and preprint of one study. | triaged |
| `doi:10.1063/1.4964858` | 2016 | Magnetoresistive sensor; reviews optical, capacitive, eddy-current and microwave probes and notes that different instruments give different answers on the same test. | triaged |

*Unknown:* none of these is at small-UAV scale or on a ducted fan. The scale gap between turbomachinery metrology and a 0.15 m-class rotor is unquantified and is a real risk to **IN-09**.

## 5. CFD validation and verification practice

*Why it matters:* directly feeds A0 and Study A. [A0.1](../cfd-validation-a01.md) is already complete and its result constrains everything downstream.

| record | year | contributes | state |
| --- | --- | --- | --- |
| `doi:10.1115/1.2960953` | 2008 | Celik et al., the grid-convergence-index procedure **already used** in the A0.1 analysis. Now catalogued with a verified identifier rather than cited from memory. | identified |
| `doi:10.17118/11143/20872` | 2023 | High-order simulation of the **Caradonna and Tung rotor in hover** — the exact A0.2 case. Directly useful for the comparison A0.2 will need. | identified |
| `doi:10.1115/1.4053854` | 2022 | Eça et al. on the interpretation and scope of the ASME V&V 20 standard, whose structure the [uncertainty decision record](../specs/research-programme/uncertainty-decision-record.md) follows. Verified; not in the corpus. | not in corpus |
| `doi:10.2514/6.2009-332` | 2009 | PIV measurements **and** computation of a 5-inch ducted fan — measurement plus simulation at this project's scale. | identified |
| `doi:10.1115/gt2022-80456` | 2022 | A data-driven modification to Spalart–Allmaras because the standard model over-predicts compressor blockage and under-predicts stall margin. Independent evidence that SA has a known directional bias near the tip. | identified |

*Already settled by our own work:* A0.1 showed every published code misses the canonical 2D experiment by 1.4–3.3 %, and turbulence-model choice alone moves lift by about 1.2 %. **A seam effect below roughly 2 % cannot be separated from model-form error by steady RANS at any mesh density.**

## 6. Measurement-system uncertainty

*Why it matters:* feeds **SSY-02** and inputs IN-01 to IN-12.

| record | year | contributes | state |
| --- | --- | --- | --- |
| `doi:10.1002/9781119417989` | 2018 | *Experimentation, Validation, and Uncertainty Analysis for Engineers* — the standard treatment of the propagation the budget performs. | identified |
| `doi:10.1016/j.measurement.2009.01.011` | 2009 | A computational system for uncertainty propagation of measurement results. | identified |

*Unknown:* the corpus contains nothing specific to **thrust-stand uncertainty at small-UAV scale**, which is what the budget actually needs. This theme's queries did not reach it.

## 7. Defect-aware and surrogate modelling

*Why it matters:* RQ2 and H2 — whether a defect-aware model beats a mean-clearance model on a held-out family.

| record | year | contributes | state |
| --- | --- | --- | --- |
| `doi:10.20944/preprints202405.0980.v1` | 2024 | Data-driven model for compressor aerodynamics aimed at rapid prediction. | identified |
| `doi:10.5293/ijfms.2009.2.2.179` | 2009 | Surrogate-based optimisation for turbomachinery aerodynamic design. | identified |
| `doi:10.1007/s00158-015-1395-9` | 2016 | Kriging surrogates for high-dimensional design models. | identified |

*Unknown:* nothing found that performs a **held-out family** test of the kind H2 requires, as opposed to a random split. The [identifiability gate](../research-plan.md#model-identifiability-gate-before-family-holdout) already anticipates this; the literature has not been shown to solve it.

## 8. Deployable mechanisms and guards — two themes that did not work

Honest result: **these two extension themes failed.** The queries pulled drone-application papers, geology surveys and ship-landing work rather than mechanism repeatability or blade containment. Of 180 deployable records, roughly one is on point (`doi:10.1109/icra.2015.7139635`, a self-deployable origami structure with a buckling-induced locking mechanism). Of 112 guard records, effectively none is. One guard query leg also failed with HTTP 429.

Both themes need re-querying with different terms before anything can be concluded. Nothing in this section should be cited as coverage. These feed **RQ3**, **RQ4** and the guard branch, all of which sit behind gates that are not open, so the gap is not currently blocking.

## What the literature already settles against this project

Two findings, both narrowing, both from work already done rather than from titles:

1. **The equal-mean comparison method is not new.** Published work holds an equivalent clearance measure fixed while redistributing the gap. Distinctiveness now rests on the combination of discrete circumferential seams, a small-UAV ducted rotor, and measurement rather than simulation.
2. **Steady RANS cannot resolve a sub-2 % effect** on a canonical case, so Study A's CFD has a floor independent of mesh density.

## Reading queue

In priority order, with the route that would actually get each one.

1. `doi:10.1016/j.ast.2023.108162` — circumferentially non-uniform clearance, 2023. **Highest priority in the corpus.** Could narrow the claim again. Elsevier; needs institutional access.
2. `doi:10.1016/j.ast.2026.111933` — day-1 source S3, nonuniform layouts. Paywalled since 2026-09-12.
3. `doi:10.1115/97-gt-406` and `doi:10.1115/2000-gt-0416` — non-axisymmetric and asymmetric clearance. ASME blocks automated retrieval; needs a browser with institutional access.
4. `doi:10.1115/1.4023468` with `doi:10.1115/gt2011-46356` and `doi:10.1115/1.4023469` — the ducted-fan VTOL trilogy, read together and counted once.
5. `doi:10.4050/vfs-f60-000155` — shrouded-rotor MAV hover performance at the project's Reynolds number.
6. `doi:10.1115/1.4025575` and `doi:10.1115/gt2023-101077` — single circumferential groove, to decide whether casing-treatment literature must be addressed.
7. `doi:10.17118/11143/20872` — Caradonna–Tung high-order simulation, before A0.2 runs.

Items 1 to 4 need access the agent does not have. **This is the binding constraint on closing SSY-01**, not search coverage.

## Gaps in the corpus itself

- **111 qualifying records from the frozen query set have never been screened**, plus 314 outside its rank filter.
- **Thrust-stand uncertainty at small scale** is absent.
- **Deployable mechanisms and guards** are effectively unsearched, as above.
- **Citation counts are missing** throughout, because both APIs were rate-limiting during the build.
- The corpus is **English-language and DOI-indexed only**. No patent literature: the dated patent search required by SSY-01 has still not been performed.
