# Graph Report - /Users/redhose/Segmented-Shroud-Yield  (2026-09-03)

## Corpus Check
- Corpus is ~4,800 words - fits in a single context window. You may not need a graph.

## Summary
- 197 nodes · 222 edges · 15 communities (14 shown, 1 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Specimen Manifest Core|Specimen Manifest Core]]
- [[_COMMUNITY_Defect Experiment and Claims|Defect Experiment and Claims]]
- [[_COMMUNITY_Yield Decisions and Roadmap|Yield Decisions and Roadmap]]
- [[_COMMUNITY_Method Overview|Method Overview]]
- [[_COMMUNITY_Prior Art and Rigid Study|Prior Art and Rigid Study]]
- [[_COMMUNITY_Research Hypotheses and Analysis|Research Hypotheses and Analysis]]
- [[_COMMUNITY_Data and Evidence Provenance|Data and Evidence Provenance]]
- [[_COMMUNITY_Instrument Schema|Instrument Schema]]
- [[_COMMUNITY_CI and Contribution Governance|CI and Contribution Governance]]
- [[_COMMUNITY_Defect-Field Schema|Defect-Field Schema]]
- [[_COMMUNITY_Operating-Point Schema|Operating-Point Schema]]
- [[_COMMUNITY_Rotor-System Schema|Rotor-System Schema]]
- [[_COMMUNITY_Closure Schema|Closure Schema]]
- [[_COMMUNITY_Repository Contract|Repository Contract]]
- [[_COMMUNITY_Contract Tests|Contract Tests]]

## God Nodes (most connected - your core abstractions)
1. `Segmented Shroud Yield` - 13 edges
2. `Experiment 01: Adjustable Rigid Defect Duct` - 13 edges
3. `Research Plan` - 11 edges
4. `Claim Ledger` - 10 edges
5. `Prior-Art Boundary` - 10 edges
6. `Research Roadmap` - 8 edges
7. `Data and Figure Contract` - 6 edges
8. `Rotor Interaction` - 6 edges
9. `Contributing Guide` - 5 edges
10. `Decision Log` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Stage 2: Adjustable Rigid Defect Duct` --conceptually_related_to--> `Experiment 01: Adjustable Rigid Defect Duct`  [INFERRED]
  ROADMAP.md → docs/experiment-01-rigid-defect-duct.md
- `Contributing Guide` --references--> `Repository Contract Check`  [EXTRACTED]
  CONTRIBUTING.md → .github/workflows/ci.yml
- `Contributing Guide` --references--> `Unit Test Discovery`  [EXTRACTED]
  CONTRIBUTING.md → .github/workflows/ci.yml
- `Segmented Shroud Yield` --references--> `Contributing Guide`  [EXTRACTED]
  README.md → CONTRIBUTING.md
- `Segmented Shroud Yield` --references--> `Claim Ledger`  [EXTRACTED]
  README.md → docs/claim-ledger.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Stage-Gated Research Program** — roadmap_stage_1_measurement_system_qualification, roadmap_stage_2_adjustable_rigid_defect_duct, roadmap_stage_3_closure_mechanism_repeatability, roadmap_stage_4_coupled_aero_mechanical_yield [EXTRACTED 1.00]
- **Research Questions and Falsifiable Hypotheses** — docs_research_plan_rq1_defect_topology, docs_research_plan_rq2_model_value, docs_research_plan_rq3_mechanism_propagation, docs_research_plan_rq4_joint_yield, docs_research_plan_h1_defect_response, docs_research_plan_h2_defect_aware_prediction, docs_research_plan_h3_self_centering_closure, docs_research_plan_h4_joint_yield_classification [EXTRACTED 1.00]
- **Repository Evidence Governance System** — contributing_evidence_state_labels, docs_claim_ledger_evidence_state_vocabulary, docs_data_and_figures_figure_evidence_rules, results_readme_result_traceability [INFERRED 0.85]
- **Aero-Mechanical Yield Research Sequence** — assets_segmented_shroud_overview_closure_variation, assets_segmented_shroud_overview_deployed_defects, assets_segmented_shroud_overview_rotor_interaction, assets_segmented_shroud_overview_honest_classification [EXTRACTED 1.00]

## Communities (15 total, 1 thin omitted)

### Community 0 - "Specimen Manifest Core"
Cohesion: 0.07
Nodes (28): additionalProperties, minimum, type, enum, type, $id, type, type (+20 more)

### Community 1 - "Defect Experiment and Claims"
Cohesion: 0.12
Nodes (21): Claim Ledger, Defect-Aware Model Transfer, Defect Topology Beyond Mean Clearance, Deployment-Generated Defect Hypothesis, Evidence-State Vocabulary, Non-Axisymmetric Clearance Claim, Performance-Duct Classification, Self-Centering Mechanism Yield Hypothesis (+13 more)

### Community 2 - "Yield Decisions and Roadmap"
Cohesion: 0.14
Nodes (17): Protective-Guard Classification, Decision Log, Isolate Defects Before Testing Mechanisms, Independent Guard Result Path, Use Aero-Mechanical Yield Instead of Cycle Count Alone, Keep the Minimum Paper to One Rotor Scale, Joint Aero-Mechanical Yield, H4: Joint-Yield Classification (+9 more)

### Community 3 - "Method Overview"
Cohesion: 0.16
Nodes (16): Closure Variation, Rubbing or Strike Risk, Defect Topology, Deployed Defects, Deployment Cycle, Dynamic Clearance, Honest Classification, Joint Tolerance (+8 more)

### Community 4 - "Prior Art and Rigid Study"
Cohesion: 0.12
Nodes (16): Akturk and Camci GT2011-46356 Ducted-Fan Clearance Experiments, Hu et al. 2024 Large-Clearance Mitigation Study, Lee et al. 2025 Self-Locking Deployable Structures, Non-Axisymmetric Clearance and Stability Study, Prior-Art Boundary, Ryu et al. 2017 VTOL Ducted-Fan Tip-Clearance Study, Second-Harmonic Casing-Ovality Study, Segmented-Duct Computational Acoustics Study (+8 more)

### Community 5 - "Research Hypotheses and Analysis"
Cohesion: 0.20
Nodes (14): Deployment-to-Aerodynamic-Yield Candidate Gap, Dated Database and Patent Search Requirement, Deployment-Specific Causal Chain, Experimental Unit of Analysis, H1: Deployment-Specific Defect Response, H3: Self-Centering Closure Variance Reduction, Held-Out Defect-Family Validation, Honest Outcome Paths (+6 more)

### Community 6 - "Data and Evidence Provenance"
Cohesion: 0.18
Nodes (12): Data Guidance, Immutable Raw Measurements, No Collected Observations, Processed-Data Provenance, Data and Figure Contract, Planned Data Lineage, Figure Evidence Rules, Required Experimental Metadata (+4 more)

### Community 7 - "Instrument Schema"
Cohesion: 0.17
Nodes (12): type, type, type, items, type, properties, required, type (+4 more)

### Community 8 - "CI and Contribution Governance"
Cohesion: 0.20
Nodes (11): GitHub Actions Checkout, Python 3.11 Setup, Repository Contract CI Workflow, Repository Contract Check, Unit Test Discovery, Auditable, Reproducible, and Falsifiable Research, Contributing Guide, Evidence-State Labels (+3 more)

### Community 9 - "Defect-Field Schema"
Cohesion: 0.18
Nodes (11): properties, required, type, enum, exclusiveMinimum, type, type, defect_field (+3 more)

### Community 10 - "Operating-Point Schema"
Cohesion: 0.20
Nodes (10): enum, properties, required, type, control_basis, operating_point, target_units, target_value (+2 more)

### Community 11 - "Rotor-System Schema"
Cohesion: 0.20
Nodes (10): type, type, controller_id, motor_id, rotor_id, rotor_system, type, properties (+2 more)

### Community 12 - "Closure Schema"
Cohesion: 0.22
Nodes (9): properties, required, type, minimum, type, closure, preload_n, type (+1 more)

### Community 13 - "Repository Contract"
Cohesion: 0.60
Nodes (4): Path, local_markdown_links(), main(), run_checks()

## Knowledge Gaps
- **82 isolated node(s):** `$schema`, `$id`, `title`, `type`, `additionalProperties` (+77 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Segmented Shroud Yield` connect `Prior Art and Rigid Study` to `Defect Experiment and Claims`, `Yield Decisions and Roadmap`, `Research Hypotheses and Analysis`, `Data and Evidence Provenance`, `CI and Contribution Governance`?**
  _High betweenness centrality (0.169) - this node is a cross-community bridge._
- **Why does `properties` connect `Specimen Manifest Core` to `Instrument Schema`, `Defect-Field Schema`, `Operating-Point Schema`, `Rotor-System Schema`, `Closure Schema`?**
  _High betweenness centrality (0.151) - this node is a cross-community bridge._
- **Why does `Research Plan` connect `Research Hypotheses and Analysis` to `Yield Decisions and Roadmap`, `Prior Art and Rigid Study`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Experiment 01: Adjustable Rigid Defect Duct` (e.g. with `Isolate Defects Before Testing Mechanisms` and `Stage 2: Adjustable Rigid Defect Duct`) actually correct?**
  _`Experiment 01: Adjustable Rigid Defect Duct` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `$id`, `title` to the rest of the system?**
  _94 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Specimen Manifest Core` be split into smaller, more focused modules?**
  _Cohesion score 0.06896551724137931 - nodes in this community are weakly interconnected._
- **Should `Defect Experiment and Claims` be split into smaller, more focused modules?**
  _Cohesion score 0.11904761904761904 - nodes in this community are weakly interconnected._