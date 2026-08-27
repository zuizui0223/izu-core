# Izu Core — conditional island plant response geometry

`izu-core` studies why island-associated pollinator reorganization can produce different plant responses rather than one universal post-establishment trajectory.

## Current state

**The Chapter 2 scientific surface is assembled as a conditional-response-geometry Research Article candidate with focal Izu empirical triangulation and an explicit structural negative control. The synthetic gate is closed, the source-locked Izu implementation/audit is present on the active branch, and actual submission is blocked only by author metadata/declarations plus a final fail-closed bundle build.**

The current manuscript surface and controlling state are:

- [`docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md`](docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md)
- [`docs/CHAPTER2_CANONICAL_STORY_20260827.md`](docs/CHAPTER2_CANONICAL_STORY_20260827.md)
- [`data/design/chapter2_active_manuscript_mainline_20260827.json`](data/design/chapter2_active_manuscript_mainline_20260827.json)
- [`data/results/chapter2_scientific_gate_decision_frozen_20260827.json`](data/results/chapter2_scientific_gate_decision_frozen_20260827.json)
- [`data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json`](data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json)
- [`data/design/izu_signed_position_source_gate_20260827.json`](data/design/izu_signed_position_source_gate_20260827.json)
- [`docs/IZU_SIGNED_POSITION_STRUCTURAL_AUDIT_20260827.md`](docs/IZU_SIGNED_POSITION_STRUCTURAL_AUDIT_20260827.md)

Earlier simulations, literature screens and retired manuscript drafts remain provenance only. The active claim is conditional response geometry, not a universal minimal generator or external-state coverage validation.

## Conceptual core that survives

The strongest idea is the three-layer decomposition of the plant island syndrome:

1. **Colonization / assembly filtering** — which lineages arrive, establish and persist.
2. **In-situ evolutionary change** — how established island lineages evolve relative to source lineages.
3. **Post-establishment interaction response** — how established lineages respond when pollinator functional composition and local interaction context change.

The current model addresses the third layer. This distinction remains the conceptual core of Chapter 2.

## Scientific reassignment after critique

### H2 — reassigned to conditional response geometry

The frozen v12 endpoint identity is

```text
sign(Δ reproduction) = sign(Δ service) = sign(Δ functional opportunity)
```

so downstream transforms preserve rather than create response sign.

Removing initial functional-position heterogeneity eliminated mixed-sign branching in the tested residual model, while trait-adjustment and assurance-ceiling heterogeneity remained. This is **not a pure algebraic tautology**, because trait-adjustment heterogeneity can still generate different endpoint traits and opportunity contrasts. However, the result only shows that initial position dominates the other tested heterogeneity sources **under the declared parameterization**.

The previous `replicated_minimal_generator` wording is therefore no longer a main-paper claim. The active analysis maps the full starting-position response geometry: 41 of 96 matched community realizations are mixed-sign, and the mean surface has positive outer regions and a negative central region. Across the fixed 48-point joint design, 16 points are mixed, 22 all-positive and 10 all-negative.

The frozen conditional-WHY diagnostic further shows that starting position organizes the mean boundary but does not dominate cell-level variation: community realization accounts for 80.17% of baseline total sum of squares and the non-additive starting-position-by-community remainder for 17.64%, compared with 2.18% for the starting-position main effect.

### H3 — retained, but renamed

The old term `local support ON` was misleading. In the implementation, increasing `support_strength` removes locally available plant/resource rows and then projects pollinator/pair support. It is a **local context / availability filtering** parameter, not extra beneficial support.

The useful result is that matched local-context filtering can change response direction in both directions. In the fixed 864-contrast threshold design:

- 737 contrasts changed sign somewhere in the 0–0.75 envelope;
- the median first sign-change strength was 0.40;
- positive baselines crossed to non-positive at a higher conditional rate than negative baselines crossed to non-negative at every non-zero strength.

Local filtering is therefore retained as a bidirectional but directionally asymmetric branch allocator. The counts and strengths remain synthetic design diagnostics, not ecological frequencies or field thresholds.

### H4 — retained as a structural distinction, not a discovery

Autonomous assurance is explicitly implemented as a compensating reproductive route that increases when reproduction is low. Magnitude attenuation is therefore largely structural.

The useful distinction is narrower:

> **magnitude buffering is not the same as qualitative sign rescue.**

The current tested envelope produced strong attenuation but no robust sign rescue. This remains useful, but it is not treated as an emergent ecological discovery.

### H5 — demoted from validation

The 13-system external set remains a source-audited comparative resource, but `11/11 covered or sign-compatible` is no longer used as validation. The broader research universe is larger than the strict 13-system manuscript set and is tracked separately.

The systems are retained as **comparative grounding, falsification and boundary examples**. They are not a prevalence sample and are not used to fit the synthetic model.

## Focal empirical depth: Izu Islands

Chapter 2 v2 adds one empirical layer that is deliberately deeper than the broad comparative inventory.

A frozen source-state projection based on the study-defined continental source and published floral/pollinator functional traits is associated with **raw realized trait matching** across 83 plant × island-site rows (slope `+0.5669`, 95% CI `+0.2977 .. +0.8361`, sign concordance `63/83`). Permuting plant source positions shows that correct plant source identity matters.

However, the structural audit prevents a stronger interpretation:

- exact island-specific pollinator-centre magnitudes/order are not uniquely identified;
- source starting position alone describes raw matching at least as well as the full centre-shift geometry;
- the same frozen predictor does **not** explain the source paper's null-corrected trait matching (`slope = +0.0333`, 95% CI `-0.2680 .. +0.3346`).

The defensible empirical reading is therefore:

> **source floral state and broad background community composition structure realized raw matching in Izu, but a beyond-composition non-random partner-sorting or causal pollinator-selection mechanism is not established.**

Izu is the focal empirical triangulation and deep mechanistic anchor because the source state, pollinator functional composition and matching response can be placed on the same archipelago-level measurement chain. It is not treated as validation of the synthetic [0,1] coordinate or its thresholds.

## Numerical reporting

Do not use `0.4167` as if it were a precise ecological frequency. The relevant frozen result is **5 of 12 matched runs** in each of two model blocks. Those runs span three saturation settings and are not a random sample from a natural population.

Similarly, 41/96, 16/48, filtering transition rates, regression coefficients and variance shares are design-specific capability/diagnostic summaries, not natural prevalence estimates or causal field effects.

## Model assumptions exposed in the active manuscript and supporting information

Current v4 scenario values include:

| Parameter | mainland-like | oceanic-island |
|---|---:|---:|
| pollinator types | 9 | 4 |
| partner arrival | 0.28 | 0.12 |
| partner loss | 0.015 | 0.055 |
| pollinator trait dispersion | 0.22 | 0.16 |
| generalist fraction | 0.35 | 0.58 |
| replacement fraction | 0.05 | 0.22 |

Lineage defaults include initial trait `Normal(0.5, 0.18)` clipped to [0,1], dependency `U(0.35,0.95)`, assurance ceiling `U(0.10,0.90)`, assurance responsiveness `U(0.004,0.035)`, and trait adjustment `U(0.01,0.055)`.

Matching is Gaussian-like in trait distance; introduced partners receive a 0.82 multiplier. Fixed visit budget uses mean partner match followed by a saturating service transform.

The ecological meanings of 24 lineages, 120 steps and saturation values 1/2/3 are not empirically identified and must be treated as model-design/sensitivity choices unless separately justified.

## What is actually unresolved now

The synthetic response-geometry gate and conditional-WHY diagnostics are complete. Chapter 2 is mechanistic **HOW** plus model-conditional **proximal WHY**: it resolves how pollinator reorganization propagates through matching, local filtering and reproduction, and why established lineages can respond differently under the same broad perturbation. It does not claim the **ultimate WHY** of why island biotas, interaction environments or lineage starting states arose.

The v2 manuscript reports the audited Izu empirical triangulation, including its null-corrected negative result, and the source-locked implementation/source gate/structural audit are part of the active paper branch. After repository CI and the fail-closed archive/bundle checks pass, only author-supplied identity metadata and submission declarations remain unresolved.

## Current manuscript status

The active manuscript surface is:

- `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md`
- `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUPPORTING_INFORMATION_20260827.md`
- `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_TABLES_20260827.md`
- `data/design/chapter2_active_manuscript_mainline_20260827.json`

The following are retained as historical/pre-v2 drafts and **must not be submitted as-is**:

- `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_20260827.md`
- `docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md`
- editorial V3 generated by `scripts/build_island_ecology_manuscript_v3.py`
- `docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md`

The submission-bundle machinery routes only the active v2 post-reassessment surface and fails closed if the frozen scientific identities or required author metadata are incomplete. The anonymous review archive includes the Izu source-recovery state, source gate, signed-position implementation and structural audit.

## Positive contribution to preserve

> **Island syndromes conflate assembly filtering, in-situ evolution and post-establishment interaction response. The third process is conditional rather than monotonic: partner turnover defines a response regime, plant source state organizes mean matching geometry, realized community strongly conditions individual outcomes, local interaction context can redirect branch identity, and downstream reproductive assurance changes magnitude without necessarily changing sign. In Izu, source state and community composition are visible in realized raw matching, but not as an identified beyond-composition sorting mechanism.**

This is a conditional mechanistic result with focal empirical triangulation. It is not a natural-frequency estimate, a calibrated regional mapping, or an ultimate explanation of island assembly and evolutionary history.
