# Candidate screening and measurement requirements — revised implementation plan

Status: merged plan (PR #16); implemented 2026-09-15 on `task/day-2026-09-14`, see [evidence](../../../evidence/task-2026-09-14/README.md). Checkboxes below record the build.
Reviewed: 2026-09-15. The directory retains the original work-order date; subsequent evidence must record its actual execution date.
Base: `main` at `bfde78cc07310e5da40f09e3ff86a0b352a40087`.
Replaces the plan at PR #15 commit `8f6da7f84adebaebc20cd8c313cdc9df330f9178`.

This PR changes only this plan. The proposed build starts from the revision merged to `main`, on `task/day-2026-09-14`, unless separately instructed. Review, merge, implementation, and physical qualification are distinct events. Plan approval does not supply missing measurements or disclosure decisions.

## Outcome and scope

Deliver two bounded artifacts: **a disposition for each of the frozen top-25 candidate identifiers**, and **a draft measurement-requirements specification with every unresolved input assigned an owner and an exit condition**. Complete the artifacts without waiting for unavailable laboratory measurements. Keep SSY-01 and SSY-02 open wherever their full acceptance criteria remain unmet.

The [backlog](../../TASKS.md), [experiment protocol](../../experiment-01-rigid-defect-duct.md), [reading rubric](../../day3-reading-rubric.md), and [contribution rules](../../../CONTRIBUTING.md) govern the scientific claims. The [sprint ledger](../../SPRINT_TASKS.csv) remains the authority for research-task status. Checkboxes below track implementation steps only.

Close reading, a new literature acquisition, a patent search, novelty-axis reconciliation, numerical sensor selection, analysis code, CAD, and physical work are outside this build. Their unresolved acceptance criteria remain visible; they are not silently declared complete by this narrower scope.

## Review of PR #15

| Issue | Why it matters | Severity | Fix in this plan | Stronger acceptance |
| --- | --- | --- | --- | --- |
| Outcome and D5 call the scholarly leg complete after 25 screens | The exporter selects only the top 25; close reading and known competing full texts remain outstanding | Major | Name the deliverable as top-25 triage; retain all SSY-01 residuals | Report 450 export identifiers, 136 qualifying for the rank filter, 25 selected, and 111 qualifying but unselected; do not treat these as independent studies |
| D2/T08 exclude unavailable metadata | Access failure does not establish irrelevance | Major | Replace `exclude_metadata_only` with `defer_insufficient_evidence`; permit title-based inclusion | Every insufficient-text case stays in the follow-up queue with its access evidence |
| D1/T04 copy close-reading fields into triage | Abstracts cannot establish detailed negative findings; premature axis states could contaminate later synthesis | Major | Use a separate, smaller screening record; make no new novelty-axis judgments | Preserve the day-3 records and all derived historical evidence byte-for-byte |
| Outcome/T16 say the specification is complete except for two numbers | Five installed-system budget terms, channel limits, performance-effect requirements, and method decisions are also unresolved | Major | Separate draft completeness, SSY-02 requirements freeze, and SSY-12 installed qualification | Draft can finish; requirements freeze and physical qualification each retain their own unresolved conditions |
| T14 supplies only a clearance stop rule | The primary matched-thrust comparison needs a power uncertainty criterion; micrometres cannot qualify watts | Major | Specify a separate matched-thrust power endpoint and its uncertainty contributors | Clearance, power, synchronization, and supporting-channel gates have dimensionally valid criteria |
| T01 lacks a committed input-specific freeze/amendment checkpoint | The merged plan versions the rule, but a local timestamp alone does not bind later corpus/procedure changes | Minor | Commit the corpus identity and applied rule before new candidate inspection | Reading records cite that freeze commit; amendments retain their order and affected identifiers |
| T02/T03/T15 checks can miss duplicates, source changes, and spec contradictions | Set equality discards duplicates; word presence does not establish a usable specification | Major | Add bounded negative controls to the two planned test files | Duplicated/substituted IDs, bad evidence references, and altered budget units/states are rejected |
| D5 generalizes an old access failure to every patent database | Current public-page access is possible; an unperformed search is not a demonstrated external block | Major | Record access per route and keep the patent-search task unperformed | No blanket access claim, and no patent-leg completion from opening one known record |
| Commands, ordering, and concurrency are inconsistent | System `python3` lacks the dependency here; package-style unittest invocation fails; five title-only records are not in the last batch | Minor | Use the verified interpreter/discovery commands, explicit dependencies, and sequential writes | Every task has an executable check or a specific inspectable artifact; no concurrent edits to one JSON file |

The original separation of screening from historical reading records, use of the existing rubric, and exclusion of CAD are retained. The repository's [AGENTS.md](../../../AGENTS.md) favors the fewest working files: reuse the native audit and budget logic, add no dependencies or general screening framework, and use only the two focused test files proposed below.

## Verified baseline and source boundary

The following are observations from this review, not results of the proposed screening:

- Baseline unit suite: **54 tests pass** using Python 3.11.8 at `/Users/redhose/ENTER/bin/python`. `python3` in this environment fails to import `jsonschema`; select an interpreter explicitly. `python -m unittest tests.test_repo_contract` fails to import the module; discovery succeeds.
- Canonical acquisition: [public export](../../../evidence/task-2026-09-11-public/database-export.json), 450 identifier records and 18 logged database/query legs. SHA-256: `d7ca70193a82f67eea761b5dec3becfd9a71f2919d922f7801e4e836da5bad52`.
- Screening input: [public candidate CSV](../../../evidence/task-2026-09-11-public/candidates-unscreened.csv), SHA-256 `184c3fb682af669e8e00c994809174e63d6b4c1d4b8aced43bc3c914180eacd1`. The [exporter](../../../evidence/task-2026-09-09/rerun_search.py) selects the first 25 non-anchor hits with `triage_score >= 4`, ordered by `(-triage_score, id)`. There are **136** such hits before the cap, leaving **111** outside this work order; another 314 export identifiers are outside that rank-filter population. These groups are not relevance verdicts.
- The D04 candidate file contains the same 25 identifiers, with different bytes and some different abstract text. It contributes **zero additional identifiers** to this batch. Do not splice its text into the canonical source silently.
- Twenty selected rows contain abstract text; five are title-only, at positions **2, 3, 10, 11, 12** in the frozen order. Four abstracts are exactly 1,500 characters, consistent with the exporter's truncation cap. Treat retained abstract text as an **excerpt unless completeness is separately verified**.
- Some titles suggest conference/journal or preprint/published versions of related work. Preserve all 25 identifiers; flag possible relationships without asserting 25 independent studies or silently deduplicating them.
- The [budget register](../../clearance-measurement-budget.csv) has seven pending inputs: five uncertainty contributors, target mean clearance, and minimum clearance effect. Its `--check` can pass while the recorded verdict remains `INPUTS_PENDING`.
- The existing [US5131603A public page](https://patents.google.com/patent/US5131603A/en) was readable through the web tool during this review. This establishes access to that page only; no new patent search, technical-overlap assessment, or legal conclusion was performed.

Freeze these inputs at build start. If their hashes, selection rule, IDs, or baseline change, reconcile the difference before screening; do not substitute a new top 25 under the same frozen procedure. Preserve both historical acquisitions and their existing limitations.

## Resolved implementation decisions

### D1 — One separate screening record and one readable report

Create `docs/candidate-screening-2026-09-14.json` with exactly two top-level keys, `metadata` (object) and `records` (list). Create `docs/prior-art-search-2026-09-14-screening.md` for the table and follow-up queues. The date in these paths identifies the work order; timestamps inside record actual work.

Metadata contains `schema_version: 1`, `candidate_csv_path`, `candidate_csv_sha256`, `export_path`, `export_sha256`, `rule_commit`, frozen ordered `candidate_ids`, and `screening_scope: "ranked_top_25"`. Paths are repository-relative. The rule text and commands live in `evidence/task-2026-09-14/README.md`. Do not add screening records to `docs/day3-reading-records.json`, alter the eligibility register, or regenerate historical ledgers/coverage from this work.

Each record contains:

| Field | Contract |
| --- | --- |
| `source_id`, `title`, `year`, `triage_score` | Copy ID/title/year as CSV strings and score as an integer; score controls order only; do not silently correct source metadata |
| `decision` | `include_for_close_reading`, `exclude_off_topic`, or `defer_insufficient_evidence`; null only during unfinished execution |
| `reason` | Nonempty source-specific rationale tied to the screening rule, including the relevant research question or metrology use |
| `aboutness` | Integer 0–3, or null when insufficient evidence prevents grading |
| `basis` | `title`, `abstract_excerpt`, `abstract`, or `full_text`; describe only what was actually inspected |
| `locator` | Object with `path_or_url`, `section`, and `sha256`; for a retained export use its path/hash plus identifier and field, for fresh content use the retained local text/hash plus original URL in the access attempt |
| `screened_utc` | Actual UTC timestamp; never reuse the acquisition timestamp as the screening date |
| `access_attempts` | List of actual attempts with UTC, URL, tool/route, outcome, and optional retained-content path/hash; empty is valid when the retained export supplied sufficient evidence |
| `possible_related_ids` | List of other selected IDs flagged as possible versions/related reports from inspected metadata; no self-reference and no automatic removal from the corpus |

For newly inspected public content, retain the smallest sufficient source excerpt or structured retrieval evidence under `evidence/task-2026-09-14/`, with URL, version/identifier, timestamp, locator, and hash. Hashes bind retained content; they do not independently certify the source. Do not republish full third-party papers. Keep quoted material minimal and use a paraphrased decision rationale.

### D2 — Relevance is independent of access

Use the day-3 rubric's aboutness principle without citation/prestige inputs. Operational anchors: 0 = outside both the aerodynamic question and required metrology; 1 = background that can inform the question; 2 = useful adjacent defect/control or measurement-method evidence; 3 = direct evidence for the proposed defect comparison or its installed measurement needs. A score is descriptive, not an automatic exclusion threshold.

- **Include** if inspected title/text supports a plausible contribution to equal-mean-clearance defects, nonuniform clearance, relevant rotor/shroud comparisons, or dynamic-clearance/associated metrology. A clearly relevant title is sufficient to queue close reading; lack of an abstract is not an exclusion.
- **Exclude off topic** only when the inspected material positively supports irrelevance to both research and metrology questions. Record the exact basis and reason. Ambiguous titles stay deferred.
- **Defer insufficient evidence** when available material cannot support either decision. Preserve any access failure and the next needed source. This is a completed triage disposition, not a completed reading or a negative novelty result.

Do not populate `axis_states`, an evidence grade, or detailed full-paper negative conclusions during this triage. If an abstract explicitly describes competing work, flag it in the reason and prioritize close reading. A skim of an accessible full text for relevance still does not count as a rubric-complete close read.

### D3 — Use existing evidence first; bounded public retrieval when necessary

Inspect canonical retained metadata before making network calls. If needed, attempt the publisher route and one legitimate open alternative, such as an author/institutional repository or a matching preprint. Record version differences; verify identifier/title correspondence. A publisher 403 does not prohibit a separate legitimate open copy, and a single failed route does not establish global inaccessibility.

Maximum two new routes per identifier in this pass; record rate limits, paywalls, transport failures, and identity mismatches separately. Exhausting the retrieval allowance leads to a reasoned include or defer, never a fabricated zero result or irrelevant verdict. Do not bypass access controls, buy access, or contact authors. New discoveries outside the frozen 25 are noted for later intake and do not replace selected rows.

### D4 — Two small tests, with counterexamples

Use `tests/test_candidate_screening.py` and `tests/test_measurement_spec.py` with standard-library `unittest`; reuse the existing native-response audit and budget loader. No new CLI, schema package, dependency, scraper, or general Markdown parser.

The screening test checks exact cardinality **and** ID uniqueness/set equality, frozen hashes/order, native audit success, copied source fields, valid dispositions, nonempty rationales, permitted aboutness, and usable source locators. It checks local source paths/hashes and that the named export record/field exists. Title-only inclusion is valid. Whether an exclusion is actually justified by its text is reviewed in T06, not inferred from a passing structural test.

Keep parsing/validation helpers local to that test module, with input arguments so negative cases use copied data or temporary paths. Demonstrate rejection of a duplicate, a missing/substituted ID, altered source bytes, a missing/foreign locator, a blank exclusion reason, and an unrecognized decision. Demonstrate acceptance of a title-based include and a deferred access failure. Do not mutate tracked inputs during tests.

### D5 — Research status follows the remaining acceptance criteria

SSY-R03 is named **“Disposition the frozen top-25 database candidates”** and becomes `done` only when all 25 have valid, reviewed dispositions and both includes and deferrals are handed off. Its completion does not close SSY-01 or its scholarly leg.

SSY-01 retains separate remaining work: the 111 qualifying unselected records and broader search boundaries; included/deferred candidates awaiting close reading; known S2/S3 competing full texts and other recorded source limits; instrument constraints; and a dated patent search. The latter is **not performed in this build**. Any future access blocker must name an attempted route and date. Do not require the owner to supply patent-database access before an agent can even test a public route.

SSY-R04 is named **“Draft SSY-02 measurement requirements and unresolved-input register”** and becomes `done` when the draft meets this plan's documentation criteria. SSY-02 remains open pending its prerequisite SSY-01 and accepted quantitative requirements. SSY-12 remains the separate installed measurement-system qualification task. Do not mark a delivered draft `blocked` merely to encode its parent's unfinished research gate.

### D6 — A specification draft, with explicit measurement models

Create `docs/measurement-system-spec.md`. Label it `planned`, `draft`, and **“requirements not frozen; installed qualification not performed.”** Cross-link it from Experiment 01; refer to the budget CSV without editing its schema or adding prose to the CSV. The draft contains the following five parts.

1. **Measurands and operating envelope.** Define measured circumferential mean clearance, dynamic minimum clearance, and electrical power at matched thrust as separate quantities. State rotor/material, speed/thrust/temperature envelope, sensor target compatibility, spatial coverage near seams, sample unit, and remaining method choices. Do not assign a finite radial clearance where a seam has no wall; require an averaging domain and treatment of missing/occluded samples before equal-mean claims. Distinguish physical runout/thermal displacement from uncertainty in measuring or correcting it; do not automatically count the same effect twice.
2. **Channel requirements.** Separate rows for mean-clearance geometry, dynamic tip clearance, thrust, voltage, current, derived electrical power, RPM, ambient temperature, duct temperature, vibration, alignment, and acquisition timing. Each row gives units, intended range, allowable bias, repeatability statistic/limit, resolution, bandwidth/sample-rate needs, calibration reference/method, qualification procedure, acceptance criterion, and status. Unknowns are named decisions with responsible roles and exit evidence, not all relabeled “owner number.” Vibration monitoring alone does not prove absence of rubbing; define how contact, probe dropout, and invalid runs are detected and retained.
3. **Budget register mapping.** Include a delimited Markdown table with exactly one row per current CSV `term` and columns `term`, `unit`, `value`, `evidence_state`, `source`, `interpretation`, `next_input`. Preserve blank values as `pending`; copy existing values/states/source strings without rounding. All nine rows are represented, including the excluded literature bound and coverage factor. Clearly distinguish protocol choices from five project-specific uncertainty contributors. Describe the existing calculator as a provisional clearance-only root-sum-of-squares model, not the complete measurement-system analysis.
4. **Qualification procedures and endpoint uncertainty.** Define warm-up/reference repeats, drift/tare checks, calibration at the intended range, synchronization/latency checks, alignment checks, missing/saturated signal rules, installed inlet/containment effects, and data retention. Each procedure has a required observation, acceptance rule, and explicit unresolved parameters (duration, repeat count, bandwidth, tolerance) before it can be executed. A successful file-consistency check is not a measurement PASS.
5. **Open-input register and release criteria.** One table with stable input IDs, needed value or decision, unit, responsible role, source/method, and the condition that closes it. Separate requirements freeze from later physical qualification. List what can be prepared now, what needs an owner choice, and what requires installed measurements.

The mathematical contract in part 4 is symbolic; this build supplies no numerical operating point or effect threshold:

- For clearance, retain `k * u_c < minimum_effect_of_interest` as the existing calculator's rule and preserve its `INPUTS_PENDING` / `STOP_INSTRUMENTATION_REDESIGN` / `FEASIBLE` semantics. State that root-sum-of-squares requires comparable standard uncertainties, justified sensitivity coefficients and negligible covariance. Record how bounds become standard uncertainties and how correlated terms would be handled before accepting the installed model. A reported physical displacement is not automatically a standard uncertainty. The general propagation basis is [NIST TN 1297, Appendix A](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty); this is a methodological reference, not a certification claim.
- For electrical power, define the measurement boundary and averaging window: `P = mean(V(t) * I(t))` for synchronized samples, or a documented equivalent power measurement. Do not silently use `mean(V) * mean(I)` when ripple/correlation matters. Define `Delta P(T*) = P_defect(T*) - P_reference(T*)` in watts and an independently specified minimum resolvable power difference. If a relative threshold is used, name its reference denominator. Propagate voltage/current calibration, covariance, thrust error, interpolation, drift, and repeated-reference uncertainty; numerical interpolation/fitting belongs to the later analysis pipeline.
- Define how uncertainty of a **difference between conditions** is assessed for both equal-mean matching and power comparisons, including shared calibration and repeated-reference covariance. A single-condition clearance budget does not establish equality between two means or qualify dynamic minimum clearance over all unobserved angles/times.
- Requirements for synchronization and bandwidth must follow the signal/rotor envelope and permitted error, with their own units. A value in micrometres cannot be used as a power, thrust, temperature, or timing limit. The provisional 10% model error and 20% improvement gates are not measurement-accuracy specifications.

The spec test parses only the table between literal HTML comments `<!-- budget-register:start -->` and `<!-- budget-register:end -->`, using the standard library. Use plain cells for copied data; only the value cell maps an empty CSV value to `pending`, while an empty source stays empty. Check exact term coverage, duplicate rejection, units, current values (including pending), states, and sources against the CSV; use a deliberately changed unit/state/value or removed row as negative controls. This protects one structured contract. Channel adequacy, uncertainty assumptions, and acceptance logic require the explicit T16 review below; a word-presence test cannot establish them.

## Inputs and ownership

Drafting proceeds with missing inputs exposed. No owner silence or untouched default line is recorded as an approval.

| Input/decision | Responsible role | What closes it | Effect of remaining open |
| --- | --- | --- | --- |
| Minimum clearance effect and target mean clearance | Owner, with agent-prepared rationale | Explicit sourced values in `um`, tied to the question and reference geometry | Clearance requirements remain unfrozen |
| Minimum meaningful power difference at matched thrust | Owner accepts scientific target; agent derives requirements | Value in W or a defined relative endpoint, operating point, reference, and rationale | Performance-measurement requirements remain unfrozen |
| Provisional rotor/stand/sensor envelope | Owner identifies available resources; agent records compatibility questions | Dated named resources or an explicit design-only choice; actual access distinguished from nominal selection | Numeric range, bandwidth, calibration, and fit assumptions remain provisional |
| Channel allocations, synchronization, repetition/drift procedures | Agent drafts; responsible experiment reviewer accepts | Dimensionally consistent limits and methods derived from the endpoint targets | SSY-02 cannot freeze; not an owner-data-entry task alone |
| Five installed clearance uncertainty contributors | Qualified operator/metrology provider | Calibration/measurement records, statistical interpretation, covariance treatment, source and units | SSY-12 and the installed clearance verdict remain unresolved |
| XC-02 disclosure path | Owner | Evidence required by the existing XC-02 done-condition | Implementation-sensitive mechanism/CAD detail remains deferred |

If owner values arrive during drafting, record the decision in the new spec/input register. Updating the historical budget CSV and its committed derived record requires a separately identified change and compatible test updates; this build's preservation checks must not silently rewrite the seven-pending-input baseline. Two accepted numbers alone do not qualify Stage A.

## Build outputs and checks

All paths below are proposed artifacts, not existing results:

- New: `docs/candidate-screening-2026-09-14.json`, `docs/prior-art-search-2026-09-14-screening.md`, `docs/measurement-system-spec.md`.
- New: `tests/test_candidate_screening.py`, `tests/test_measurement_spec.py`.
- New: `evidence/task-2026-09-14/README.md`, command logs, and only the source excerpts actually needed for new decisions.
- Modify: `docs/prior-art.md`, `docs/TASKS.md` (dated scoped status notes), `docs/experiment-01-rigid-defect-duct.md` (spec link), `docs/SPRINT_TASKS.csv`, `docs/SPRINT_PROGRESS.md`, `docs/REVIEW_READY.md`, and this plan's implementation checkboxes.

Use Python 3.11 with `requirements.txt` installed. Locally, `python` currently resolves to the verified environment; record `sys.executable`, version, dependency version, baseline commit and eventual build commit. Use `sys.executable` for subprocesses in tests. If another interpreter is selected, verify its dependency import before running gates. There is no separate configured lint, typecheck, or package-build command.

Run each command separately from the repository root and retain its exit code and full output:

```sh
python -m unittest discover -s tests -v
python scripts/check_repo_contract.py
python scripts/reference_coverage.py --check
python scripts/acquisition_ledger.py --check
python scripts/clearance_uncertainty_budget.py --check
python evidence/task-2026-09-09/rerun_search.py --audit evidence/task-2026-09-11-public/database-export.json
python tools/check_presentation.py . "Segmented Shroud Aeromechanics" segmented-shroud-aeromechanics
python tools/test_presentation.py
git diff --check
```

Targeted commands once the new files exist:

```sh
python -m unittest discover -s tests -p 'test_candidate_screening.py' -v
python -m unittest discover -s tests -p 'test_measurement_spec.py' -v
```

Require a nonzero discovered-test count and assertion failures for intended negative controls; an import failure or zero tests is not a successful test-first step. A green budget `--check` means the pending record is reproducible. Do not run the budget generator without `--check` against its default register during this build.

The repository contract checker crawls all Markdown files for local target existence but strips anchor fragments; the presentation checker covers only its configured files. Reuse the contract check for file paths and explicitly inspect anchors in the new/modified documents. An intended future path in this plan is code-formatted, not a broken link to a nonexistent artifact.

## Tasks

T00–T21 are ordered work units. Each unit targets one reviewable concern, normally 2–5 minutes; repeat T05 per candidate and T12 per channel rather than compressing 25 inspections or 12 channel decisions into a fictional five-minute task. Retrieval latency and resolving a scientific decision are not included in those estimates. Record actual progress and remaining work instead of promising completion within one calendar day.

### [x] T00 — Establish the build baseline

- Files: `evidence/task-2026-09-14/README.md` and gate logs (new).
- Do: verify the merged plan revision, clean worktree, interpreter/dependency, and all baseline commands above.
- Done when: logs retain each command, exit code, suite count and pending budget verdict; unexpected failures are resolved or explicitly stop dependent work.

### [x] T01 — Freeze the corpus and procedure before candidate inspection

- Files: evidence README (modify).
- Depends on: T00.
- Do: record input hashes, native audit, actual ordered IDs, 450/136/25/111 counts, D1–D3, and unchanged historical files; commit this procedure before new screening.
- Done when: the commit exists and the recorded selection reproduces from retained JSON. A changed corpus requires a dated amendment before affected decisions, never a backdated freeze.

### [x] T02 — Initialize the screening record

- Files: screening JSON (new); evidence README (modify).
- Depends on: T01.
- Do: generate metadata and one skeleton per selected ID using a recorded inline standard-library snippet; record T01's actual commit. Initialize decision/aboutness to null and attempts/related IDs to empty lists.
- Done when: 25 records, 25 unique IDs, exact ordered equality to the selection, and copied source fields match. No skeleton is counted as screened.

### [x] T03 — Add screening completeness and provenance checks

- Files: `tests/test_candidate_screening.py` (new).
- Depends on: T02.
- Do: implement D4 checks using existing acquisition-audit logic and local input-accepting helpers.
- Done when: targeted discovery loads tests and fails on unfinished decisions with named IDs; captured failure is an assertion, not an import error.

### [x] T04 — Prove the screening checks reject misleading records

- Files: screening test (modify).
- Depends on: T03.
- Do: add D4's focused counterexamples using copied records/temporary paths; keep incomplete live records separate from these synthetic controls.
- Done when: negative controls reject their intended defects and title-based inclusion/deferred access are accepted; the live corpus completeness check remains red until disposition is complete.

### [x] T05 — Disposition each selected identifier

- Files: screening JSON (modify); source evidence only when newly retrieved.
- Depends on: T04.
- Do: repeat for each of the 25 IDs, in the frozen order. Inspect available evidence, apply D2/D3, and record the actual basis, rationale, locator, timestamp and possible related versions. One writer updates the JSON sequentially.
- Done when: each ID has a supported disposition. Checkpoint after every five IDs and on interruption; at completion targeted screening discovery passes. Do not expect missing-abstract cases to occupy a particular batch.

### [x] T06 — Review all exclusions and deferrals

- Files: screening JSON and evidence README (modify only if needed).
- Depends on: T05.
- Do: re-read the cited basis for every exclusion/deferral; check that missing access was not converted into irrelevance. Check inclusion rationales for title/excerpt overclaims and possible duplicate-study counting.
- Done when: a per-ID review disposition is recorded for exclusions/deferrals, unresolved cases are queued, and the targeted suite remains green. Label this as a self-review unless a separate reviewer actually performs it.

### [x] T07 — Produce the screening summary

- Files: screening report (new).
- Depends on: T06.
- Do: render the 25-row table from JSON with a recorded inline snippet; include access/basis, decision, rationale/locator and aboutness. Report counts from the data and explicit corpus limits.
- Done when: decision counts sum to 25, every ID appears once, and the report states that triage is not close reading, novelty clearance, a patent search, or a census of 450 studies. No minimum include-count target.

### [x] T08 — Hand off the unresolved source work

- Files: screening report (modify).
- Depends on: T07.
- Do: derive queues for every include and defer, with priority/reason and next source needed; name the 111 unselected qualifying records and existing S2/S3 reading gaps separately. Prioritize likely direct competitors, then instrument feasibility, then background; preserve the full queue.
- Done when: queue-ID sets exactly match the JSON and no deferred item disappears. The remaining export population and broader search remain unreviewed, not excluded.

### [x] T09 — Update the prior-art boundary without inventing closure

- Files: `docs/prior-art.md`, `docs/TASKS.md` (modify).
- Depends on: T08.
- Do: add the actual execution date, source-report link, frozen query-log reference, selection caps and inclusion rules. State which SSY-01 criteria are still unfulfilled, including patent search and close reading.
- Done when: wording preserves any earlier bounded “supported candidate gap” or “prior art found” assessment with its original source scope. Screening alone supplies no new per-axis verdict and does not earn those phrases merely by inserting them into a paragraph.

### [x] T10 — Create the specification structure and open-input register

- Files: `docs/measurement-system-spec.md` (new).
- Depends on: T01.
- Independent lane: specification; may proceed while screening waits on retrieval, without editing screening files.
- Do: add D6's five sections, draft/evidence labels, the ownership table's input IDs and exit evidence.
- Done when: draft acceptance, SSY-02 requirements freeze and SSY-12 physical qualification are explicitly separate; every unknown has an accountable role rather than a fabricated number.

### [x] T11 — Define the measurands and admissible observations

- Files: measurement spec (modify).
- Depends on: T10.
- Do: write D6 part 1 and preserve matched-thrust comparison, actual averaging domain, minimum-clearance coverage, missing-wall semantics, sample hierarchy, and contact/dropout dispositions.
- Done when: a reviewer can distinguish physical geometry, measured values, systematic corrections, measurement uncertainty, and unobserved regions. Unmade design choices are in the input register.

### [x] T12 — Specify each channel's requirements

- Files: measurement spec (modify).
- Depends on: T11.
- Do: repeat D6 part 2 for each of the 12 named channels; assign unresolved range/limit/method/timing decisions to input IDs.
- Done when: each row has units, a method and acceptance structure, or a named unresolved decision for every required field. Literature sensors are candidates, not selected hardware or installed accuracy.

### [x] T13 — Bind the budget mapping to its source register

- Files: measurement spec (modify).
- Depends on: T12.
- Do: build D6's delimited nine-row budget table from the current CSV; describe the five uncertainty terms and pending verdict.
- Done when: values/units/states/sources agree with the register, literature accuracy is excluded from the combination, and the limits of the current clearance calculator are explicit.

### [x] T14 — Define qualification and endpoint-uncertainty procedures

- Files: measurement spec (modify).
- Depends on: T13.
- Do: write D6 part 4 using the symbolic clearance/power contracts and dimensionally consistent channel criteria; split into one procedure per work unit if necessary.
- Done when: each procedure names observations, pass/stop/pending conditions and unresolved parameters; difference uncertainty, synchronization and repeated-reference handling are addressed. No planned input or passing software check can be called installed qualification.

### [x] T15 — Test the specification/register contract

- Files: `tests/test_measurement_spec.py` (new).
- Depends on: T13.
- Do: implement the bounded table comparison and D6's negative controls; include wrong value/unit/state/source, duplicate/missing term, and pending-to-numeric substitution cases in memory.
- Done when: targeted discovery passes for the draft table, every counterexample is rejected, and tests leave the CSV/committed budget untouched.

### [x] T16 — Review the requirements as an experiment contract

- Files: measurement spec and evidence README (modify).
- Depends on: T14, T15.
- Do: review every D6 requirement and SSY-02 done-condition, including performance effect, channel limits, calibration references, drift, synchronization, sample unit, and qualifying actual installed behavior. Record satisfied-as-draft / unresolved with an input ID and next action.
- Done when: no acceptance criterion is represented only by a mentioned keyword; neither SSY-02 freeze nor Stage A PASS is claimed. Recheck targeted tests after any table correction.

### [x] T17 — Add the Experiment 01 reading route

- Files: `docs/experiment-01-rigid-defect-duct.md` (modify).
- Depends on: T16.
- Do: add a link under Stage A describing the spec as a draft of requirements with open inputs.
- Done when: the link resolves and its caption cannot be read as an installed qualification result; the budget CSV remains unchanged.

### [x] T18 — Reconcile bounded task status

- Files: `docs/SPRINT_TASKS.csv`, `docs/TASKS.md` (modify).
- Depends on: T09, T17.
- Do: add unique rows SSY-R03 and SSY-R04 with their D5 scopes, owner Agent, P1, dependency SSY-R02, actual execution date, deliverable/verification/evidence fields and estimates clearly labeled as estimates. Use `done` only after their artifact checks pass; list parent residuals explicitly.
- Done when: CSV parses, IDs are unique, verification commands use discovery, and no prior done row is reclassified. SSY-01/SSY-02/SSY-S08/XC-02 retain their own unmet conditions; ledger and dated backlog notes agree.

### [x] T19 — Update the handoff

- Files: `docs/SPRINT_PROGRESS.md`, `docs/REVIEW_READY.md` (modify).
- Depends on: T18.
- Do: add a dated current section with actual decision counts, draft-spec outcome, remaining work by responsible role and links to the new evidence.
- Done when: both summaries agree with JSON and ledger and explicitly distinguish completed top-25 triage from unfinished scholarly review, and delivered requirements draft from unfrozen requirements/physical qualification.

### [x] T20 — Run integration and preservation checks

- Files: evidence README/logs and plan checkboxes (modify).
- Depends on: T19.
- Do: run the full command set, check new/changed documentation links, and compare historical inputs against T00's build base. Record actual suite totals and all acceptance decisions.
- Done when: commands pass and no diffs exist in historical acquisition folders, `docs/day3-reading-records.json`, `docs/source-eligibility-register.json`, `docs/clearance-measurement-budget.csv`, or their prior derived evidence. Expected unresolved research inputs remain reported as unresolved. No new measurement/novelty result is inferred from green checks.

### [x] T21 — Deliver the implementation PR

- Files: no additional product files; PR body and evidence links.
- Depends on: T20.
- Do: commit the bounded build, push its branch, open one implementation PR against `main`, and identify the merged plan revision. Verify CI on the exact PR head.
- Done when: the PR exists, CI passes on its current commit, and the body lists actual outcomes and every remaining SSY-01/02 input. Keep it unmerged unless separately instructed; do not mark a planned push or stale CI result as delivery.

## Traceability and finish lines

| Requirement | Implementation tasks | Acceptance in this build | Remaining research gate |
| --- | --- | --- | --- |
| Frozen query/source provenance and bounded population | T00–T04, T07 | Audited retained export; exact 25-ID/hash binding; visible selection limits | Broader coverage and 111 qualifying unselected records unresolved |
| Rule-before-reading relevance triage | T01, T05–T08 | 25 justified dispositions; includes and deferrals retained | Full close reading and source-level evidence grades/axes deferred |
| SSY-01 dated scholarly/patent search, inclusion rules and evidence table | T07–T09 | Existing scholarly search linked; new triage table and precise residuals | No new patent search, full scholarly closeout, or novelty verdict |
| SSY-01 instrument constraints | T08, T11–T12, T16 | Relevant metrology queue and source-bounded draft questions | Method compatibility and full-source conclusions unresolved |
| SSY-02 minimum defect **and performance** effect | T10–T14, T16 | Separate dimensionally correct endpoints and assigned input decisions | Quantitative targets and accepted allocation still needed |
| SSY-02 every-channel bias, repeatability and calibration | T12–T16 | Complete draft fields, methods and open-input register | Numeric limits, chosen methods/references and acceptance remain open |
| SSY-02 warm-up, drift, timing, sample unit, PASS/FAIL MSA | T11, T14, T16 | Reviewable procedures and pass/stop/pending logic | Parameter freeze, then SSY-12 installed execution |
| Budget/spec consistency without historical drift | T13, T15, T20 | Exact table contract and negative controls | Five installed contributors and model assumptions remain unresolved |
| Honest task status and reproducible delivery | T17–T21 | Artifact-scoped ledger rows, current handoff, exact-head CI | Owner/lab/disclosure decisions not supplied by this PR |

The build is complete when the two bounded artifacts and their checks are delivered. The larger research floor still requires accepted requirements, a closed source boundary, parametric CAD and an analysis pipeline. Close-reading reconciliation and a dated patent search should be planned from the resulting queues; CAD remains subject to its existing research/disclosure prerequisites. This work order does not reopen those parked tasks.

## Verification of this plan revision

The replacement PR is documentation only. Review reproduced the 25-ID equality between candidate files, rank-cap counts, abstract-presence positions and truncation evidence, and the seven-pending-input budget. Baseline unit discovery passed 54 tests. The PR records the final contract, derived-record, presentation, local-link and whitespace checks on this revised file. These checks verify plan consistency and repository health; the two proposed test files and all T00–T21 build outputs remain unimplemented.
