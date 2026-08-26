# Izu Core — island plant response architecture under reassessment

`izu-core` studies why island-associated pollinator reorganization can produce different plant responses rather than one universal post-establishment trajectory.

## Current state

**Chapter 2 has been reopened for scientific reassessment. Do not submit the current Journal of Ecology Research Article yet.**

The previous `complete_and_frozen_for_submission` status is superseded by:

- [`docs/SCIENTIFIC_REASSESSMENT_AFTER_CRITIQUE_20260826.md`](docs/SCIENTIFIC_REASSESSMENT_AFTER_CRITIQUE_20260826.md)
- [`data/design/manuscript_reassessment_gate_20260826.json`](data/design/manuscript_reassessment_gate_20260826.json)

The existing simulations, literature screen and manuscript drafts remain valid provenance. What changed is **their claim role**.

## Conceptual core that survives

The strongest idea is the three-layer decomposition of the plant island syndrome:

1. **Colonization / assembly filtering** — which lineages arrive, establish and persist.
2. **In-situ evolutionary change** — how established island lineages evolve relative to source lineages.
3. **Post-establishment interaction response** — how established lineages respond when pollinator functional composition and local interaction context change.

The current model addresses the third layer. This distinction remains the conceptual core of Chapter 2.

## Scientific reassignment after critique

### H2 — demoted from headline discovery

The frozen v12 endpoint identity is

```text
sign(Δ reproduction) = sign(Δ service) = sign(Δ functional opportunity)
```

so downstream transforms preserve rather than create response sign.

Removing initial functional-position heterogeneity eliminated mixed-sign branching in the tested residual model, while trait-adjustment and assurance-ceiling heterogeneity remained. This is **not a pure algebraic tautology**, because trait-adjustment heterogeneity can still generate different endpoint traits and opportunity contrasts. However, the result only shows that initial position dominates the other tested heterogeneity sources **under the declared parameterization**.

The previous `replicated_minimal_generator` wording is therefore no longer a main-paper claim. The independent seed block is retained as a model-specific robustness check, not as independent evidence for a new ecological principle.

### H3 — retained, but renamed

The old term `local support ON` was misleading. In the implementation, increasing `support_strength` removes locally available plant/resource rows and then projects pollinator/pair support. It is a **local context / availability filtering** parameter, not extra beneficial support.

The useful result is that matched local-context filtering can change response direction in both directions:

- 16/96 eligible declines crossed the sign boundary;
- 11/96 worsened;
- many others changed only in magnitude.

This bidirectionality is retained, but requires broader robustness analysis before becoming a headline Research Article result.

### H4 — retained as a structural distinction, not a discovery

Autonomous assurance is explicitly implemented as a compensating reproductive route that increases when reproduction is low. Magnitude attenuation is therefore largely structural.

The useful distinction is narrower:

> **magnitude buffering is not the same as qualitative sign rescue.**

The current tested envelope produced strong attenuation but no robust sign rescue. This remains useful, but it is not treated as an emergent ecological discovery.

### H5 — demoted from validation

The 13-system external set remains a source-audited comparative resource, but `11/11 covered or sign-compatible` is no longer used as validation. The broad state vocabulary is too inclusive for that coverage count to be strongly falsifiable.

The systems are retained as **comparative grounding and boundary examples**. Dominica remains a genuine failure of the more specific signed-position projection and was not retuned.

## Numerical reporting

Do not use `0.4167` as if it were a precise ecological frequency. The relevant frozen result is **5 of 12 matched runs** in each of two model blocks. Those runs span three saturation settings and are not a random sample from a natural population.

Similarly, 16/96, 11/96 and related counts are design-specific capability summaries, not natural prevalence estimates.

## Model assumptions that must be exposed in the next manuscript

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

The Research Article needs one nontrivial quantitative result beyond the three-layer conceptual decomposition.

### Active scientific gate

**Response geometry / parameter robustness**:

1. Map when pollinator-community change produces positive, negative or sign-switching functional-opportunity responses across plant starting position.
2. Sweep the key perturbation and matching parameters rather than relying on one frozen scenario.
3. Determine whether mixed-sign response is a stable region of parameter space or an artefact of particular stochastic partner realizations.
4. Quantify when local context filtering changes sign versus only magnitude.
5. Quantify the assurance threshold for sign rescue instead of treating attenuation as a discovery.

If a stable, interpretable response map emerges, the Research Article can be rebuilt around that result. If not, the stronger product is a conceptual Review/Mini-review centered on the three-layer island-syndrome decomposition.

## Current manuscript status

The following are retained as historical/pre-reassessment drafts and **must not be submitted as-is**:

- `docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md`
- editorial V3 generated by `scripts/build_island_ecology_manuscript_v3.py`
- `docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md`

The submission-bundle machinery remains in the repository for later reuse, but the current scientific reassessment gate overrides the previous metadata-only submission gate.

## Reference and prose cleanup already identified

Before the next manuscript version:

- remove the import-path failure / seed-search narrative from Methods;
- report `5 of 12` rather than `0.4167` in prose;
- explain the full model equations and scenario values;
- remove or explicitly cite Lord (2015) and Méndez (2025);
- replace beneficial-sounding `local support` language with neutral `local context filtering` / `local availability filtering`;
- reduce `frozen`, `predeclared`, `protected`, `gate`, and similar procedural language in the scientific narrative.

## Positive contribution to preserve

> **Island syndromes conflate assembly filtering, in-situ evolution and post-establishment interaction response. The third process is conditional rather than monotonic: pollinator reorganization is filtered through plant–pollinator matching geometry, local interaction context can redirect outcomes in either direction, and downstream reproductive assurance changes magnitude without necessarily changing sign.**

The next task is to determine whether this architecture has a stable quantitative response geometry strong enough for a Research Article.
