# Prior-Art Boundary

## 2026-09-08 source and metrology review

[Dated first-pass review](prior-art-search-2026-09-08.md) records executed queries,
10 screened primary records, exclusions, a measurement-method shortlist and
unavailable full texts. Broad prior art is confirmed; the rigid-defect experiment
remains a supported candidate gap within this retrieval, not established novelty.
SSY-D01 completes this bounded pass, not full SSY-01 or disclosure gate XC-02.

This source map defines what the repository must not overclaim. It is not an exhaustive systematic review or patent search.

## Established ingredients

| Area | Source | What it establishes for this project |
| --- | --- | --- |
| Tip-clearance sensitivity in a VTOL ducted fan | [Ryu et al., 2017](https://doi.org/10.2322/tjsass.60.1) | Average rotor-tip clearance already has established aerodynamic importance. |
| Ducted-fan clearance experiments | [Akturk and Camci, ASME GT2011-46356](https://cengizcamci.github.io/papers/GT2011_46356_DUCTED_FAN_1.pdf) | Controlled ducted-fan clearance experiments and associated flow measurements are established methods. |
| Large-clearance mitigation | [Hu et al., 2024](https://doi.org/10.1016/j.ast.2024.109226) | A grooved duct has already been studied for robustness to large clearance; generic robustness is not enough. |
| Non-axisymmetric clearance | [Second-harmonic casing-ovality study](https://doi.org/10.1016/j.ast.2023.108866) | Circumferential clearance harmonics and casing ovalization are established turbomachinery concerns. |
| Aeroelastic effects of ovality | [Non-axisymmetric clearance and stability](https://doi.org/10.1016/j.ast.2024.109457) | Nonuniform clearance can alter performance and aeroelastic behavior; ovality itself is not a new variable. |
| Self-locking deployable structures | [Lee et al., 2025](https://doi.org/10.1073/pnas.2409062121) | Experimentally validated self-locking deployable tubes already exist. |
| Segmented duct acoustics | [Segmented-duct computational study](https://www.mdpi.com/2624-8921/8/7/165) | Segmentation and acoustic consequences have recent computational treatment; acoustics is not the first-paper focus. |
| Small-UAV propeller enclosures | [Sub-250 g enclosure experiment](https://doi.org/10.3390/aerospace13020182) | Enclosures involve mass, power, and noise trade-offs; the comparison basis must be explicit. |

## Candidate gap

The working gap is not “folding duct” or “self-locking ring.” It is:

> Experimental propagation of repeated-deployment and closure variation into segmented-shroud seam, step, and harmonic defect fields, followed by held-out prediction of dynamic clearance, rubbing, and thrust-per-power at small-UAV scale.

This is a **candidate distinctiveness claim**, not proof of global novelty.

## Claims explicitly excluded

This repository will not claim invention of:

- Ducted fans or rotor shrouds
- Tip-clearance sensitivity
- Non-axisymmetric clearance or casing ovality
- Self-locking deployable structures
- Rotor guards
- Probabilistic engineering yield as a general method
- Acoustic effects of segmented ducts

## 2026-09-15 database-candidate triage (work order 2026-09-14)

The frozen top-25 candidates of the canonical 2026-09-11 public database export were dispositioned under the day-3 rubric's aboutness principle, with the rule committed before reading: [screening report](prior-art-search-2026-09-14-screening.md), [record](candidate-screening-2026-09-14.json), [evidence](../evidence/task-2026-09-14/README.md).

- Search strings: the frozen 18 (database, query) legs already logged in the export; no new query was added. Selection: the exporter's rank filter (non-anchor, triage score at least 4, ordered by score then identifier) capped at 25 of 136 qualifying records.
- Inclusion rule: include when the inspected title or retained abstract plausibly contributes to equal-mean-clearance defects, nonuniform clearance, relevant rotor/shroud comparisons, or dynamic-clearance metrology; exclude only when the text positively supports irrelevance to both; defer when neither can be supported. Access failure never counts as irrelevance.
- Outcome: 22 included for close reading (at most 19 distinct studies after version clusters), 3 excluded off topic, 0 deferred. No novelty-axis state was assigned; no axis verdict changes.

What this does and does not close for SSY-01: the dated scholarly database search and its inclusion rules are now recorded and linked; the evidence table for equal-mean-clearance defects and dynamic tip-clearance methods is still the day-3 table plus this triage, not a close-read table; instrument constraints are captured only as a metrology reading queue feeding the [measurement-requirements draft](measurement-system-spec.md). Still unfulfilled: close reading of the 22 includes; the 111 qualifying unselected records and the broader search boundary; the S2 and S3 full texts; and a dated patent search, which was not performed. The bounded "candidate distinctiveness claim" above keeps its original 2026-09-08 scope and is neither strengthened nor withdrawn by this triage.

## 2026-09-21 close reading of the first-tier competitors

Six queued competitors were taken from the [triage report](prior-art-search-2026-09-14-screening.md). One was read in full; five could not be obtained. Records, access attempts and per-axis states: [reading-records-2026-09-21.json](reading-records-2026-09-21.json). The day-3 reading file is unchanged.

**Read in full: `doi:10.1016/j.heliyon.2024.e25296`.** A transonic axial compressor study (NASA Stage 35), steady RANS with the Spalart–Allmaras model, grid-independent at 2.25 million cells, with the uniform baseline validated against published experimental efficiency and pressure ratio. Three nonuniform clearance schemes run at max 0.612 mm and min 0.204 mm against a uniform 0.408 mm prototype.

This read changes the claim boundary, and the change is a narrowing. The paper states that it designed its schemes "to control the circumferential leakage area of the tip gap to be the same as that of uniform type", and its three schemes share one maximum and minimum whose arithmetic mean equals the uniform value. **The idea of holding an equivalent clearance measure fixed while redistributing the gap is therefore disclosed in the literature, and this project may not present it as new.** The triage screen could not have found this: the abstract says "nonuniform tip clearance" and only the full text reveals both the equal-area constraint and the axis of variation.

What it does not disclose is equally specific. The variation is **axial**, along the blade chord, and the paper classifies its own subject as "axial nonlinear nonuniform blade tip clearance". There are no discrete circumferential seams, no duct, no small-UAV rotor, no deployment-induced defect, and no measurement of any nonuniform geometry. A circumferential seam at equal mean clearance remains outside what this source establishes.

**Not obtained: five ASME papers** (`97-gt-406`, `2000-gt-0416`, `1.4023468`, `gt2011-46356`, `1.4023469`). The publisher route returns HTTP 403 and the ASME Digital Collection presents a bot interstitial to an automated client, which was not worked around. One of the five is recorded as open access by an index, yet the host still refused automated retrieval, so open-access status did not translate into an obtainable copy. Every axis for all five stays **unresolved**; an abstract cannot establish what a full paper does or does not contain. An institutional subscription through a browser is the ordinary route and is available to the owner.

The consequence for SSY-01 is that the scholarly leg is still not closed: four of the first-tier competitors remain unread, the 111 qualifying unselected records are unreviewed, and the S2 and S3 full texts are still outstanding.

## Search questions still open

- Has a small-UAV experiment already isolated equal-mean-clearance seam, step, and harmonic defects?
- Has a repeatedly deployed segmented shroud been tested with dynamic clearance measurements near a rotating rotor?
- Has closure-mechanism variation been propagated into an aerodynamic yield model with held-out validation?
- Which sensing approaches can resolve the target clearance without disturbing the flow or creating a rotor hazard?

These questions require dated database searches and a patent review before the paper's novelty statement is frozen.
