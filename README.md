# Izu Core — state-dependent island plant responses

`izu-core` is the reproducible analysis and manuscript repository for an island-ecology study asking:

> **Why does island-associated simplification or reorganization of pollinator function produce divergent plant responses rather than one universal post-establishment trajectory?**

The current manuscript is framed as an island-ecology paper, not a methods-first ABM paper. Its central result is that an aggregate plant **island syndrome** does not imply that all established island lineages follow the same ecological trajectory.

## Current paper

Working title:

> **One perturbation, multiple island responses: state-dependent branching under pollinator functional simplification**

Primary target: **Journal of Ecology**  
Fallbacks: **Functional Ecology**, **Oikos**

Primary manuscript:

- [`docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md`](docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md)
- Supporting Information: [`docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md`](docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md)
- Cover letter: [`docs/ISLAND_ECOLOGY_JECOLOGY_COVER_LETTER_20260824.md`](docs/ISLAND_ECOLOGY_JECOLOGY_COVER_LETTER_20260824.md)
- Canonical machine-readable state: [`data/design/simulation_study_mainline_20260824.json`](data/design/simulation_study_mainline_20260824.json)

The primary scientific hypotheses are closed for submission. No new simulation, field dataset, external-system search, or parameter retuning is required for the current paper.

## Ecological story

The paper separates three processes that are often grouped together under the term **plant island syndrome**:

1. **Colonization / assembly filtering** — traits alter arrival, establishment, and persistence, changing which lineages are represented in island floras.
2. **In-situ evolutionary change** — established island lineages evolve relative to mainland source lineages.
3. **Post-establishment interaction response** — established lineages respond to altered pollinator functional composition, network context, and reproductive buffering.

The current model addresses the third layer.

```text
MAINLAND SOURCE POOL
        |
        | dispersal, arrival, establishment
        v
COLONIZATION / ASSEMBLY FILTER
        | self-compatibility
        | lifespan / clonality
        | generalized reproductive accessibility
        v
ESTABLISHED ISLAND FLORA
        |
        | altered pollinator functional composition
        | interaction-network reorganization
        v
POST-ESTABLISHMENT RESPONSE
        |
        +--> starting functional state -> branch potential
        |
        +--> local interaction context -> branch allocation / rescue / worsening
        |
        +--> reproductive assurance -> magnitude attenuation
        v
OBSERVED LINEAGE TRAJECTORIES

Repeated filtering + evolution + response across lineages and time
        -> macroecological "island syndrome"
```

The resulting synthesis is:

> **Aggregate island syndromes can coexist with lineage-level branching because colonization and persistence determine which states arrive, while functional starting state and local ecological context determine how established lineages respond after pollinator environments change.**

## H1–H5

| Hypothesis | Prediction | Current result |
|---|---|---|
| **H1 — universal post-establishment response** | one island-like perturbation pushes lineages in one common direction | **rejected** |
| **H2 — state-dependent branching** | pre-existing functional-position heterogeneity is required for within-run sign branching | **supported within the declared ABM and independently replicated** |
| **H3 — context-dependent propagation** | local interaction context reallocates branch identity and can rescue or worsen responses | **supported bidirectionally** |
| **H4 — autonomous-assurance buffering** | assurance reduces downstream reproductive loss and may reverse sign | **partially supported: robust magnitude attenuation, no robust sign rescue** |
| **H5 — cross-island recurrence** | branching, propagation, and buffering/alternative states recur across independent island systems without retuning | **supported at the qualitative response-state level** |

## Main frozen results

### Branch generation

In the original residual block and an independently seeded replication, mixed-sign branching occurred in **0.4167** of matched runs. Removing pre-existing functional-position heterogeneity reduced within-run mixed-sign branching to **0**, whereas other tested residual single-factor removals retained branching.

Within the declared ABM, pre-existing lineage position in functional trait space is therefore the replicated minimal generator of response-sign branching.

### Local interaction context

Local support is not required to create branching, but it strongly reallocates branch identity.

- local-support removal changed **105/288** paired lineage response signs;
- in the independent network-context block, support produced **16/96** sign rescues;
- **85/96** eligible declines were attenuated;
- **11/96** were worsened.

The stable interpretation is therefore:

> **network context is a bidirectional branch allocator with buffering capacity, not a universal buffer.**

### Autonomous assurance

Among **216** lineages with upstream service decline, autonomous assurance attenuated reproductive decline in **207/216** cases but produced **0** sign rescues in the independent block. A broadened envelope likewise produced **0/525** sign rescues.

The stable interpretation is:

> **autonomous assurance mainly attenuates response magnitude rather than reliably reversing response sign.**

## External island challenge

The literature screen retained **54 geographic/system units**. Thirteen met the strict external state-challenge contract.

| External state | Systems |
|---|---:|
| branching | 3 |
| same-direction propagation | 6 |
| buffering / alternative | 2 |
| reproductive-axis decoupling constraint | 1 |
| retained falsification | 1 |
| **total** | **13** |

All **11 generative challenges** were covered or sign-compatible with response classes already present in the frozen model. The external set is a **strict challenge set, not a prevalence sample**.

Protected exceptions are retained:

- **Puerto Rico–Mona `Guaiacum sanctum`** — reproductive axes decouple; it is not collapsed into a generic whole-reproduction buffer state.
- **Dominica `Heliconia`** — the predeclared signed-position projection failed and was not retuned.

Cross-island recurrence therefore supports the generality of the **response architecture**, not one shared empirical mechanism across all islands.

## Island-syndrome literature synthesis

The manuscript now uses a deeper literature review rather than treating the island syndrome as a single causal trajectory.

Canonical review:

- [`docs/ISLAND_SYNDROME_DEEP_LITERATURE_REVIEW_20260824.md`](docs/ISLAND_SYNDROME_DEEP_LITERATURE_REVIEW_20260824.md)
- Machine-readable claim matrix: [`data/design/island_syndrome_literature_claim_matrix_20260824.json`](data/design/island_syndrome_literature_claim_matrix_20260824.json)

Key literature conclusions:

- **Baker's law** is most defensibly treated as a colonization advantage of uniparental reproductive capacity, not as a universal prediction of high realized selfing after colonization.
- Self-compatibility is strongly enriched in island floras, consistent with assembly filtering.
- Flower-size evolution is not universally directional; comparative Pacific studies show archipelago-, lineage-, starting-size-, and pollination-mode dependence.
- Oceanic pollination networks are often smaller or functionally reorganized, but simplification does not imply that every network metric or plant response changes in the same direction.
- Pollinator **functional diversity and trait matching**, rather than species richness alone, provide the strongest empirical bridge to the upstream perturbation represented in the model.
- Proposed plant island-syndrome components have heterogeneous evidence strength and should not be treated as one universal evolutionary package.

## Main paper architecture

The main figures are ecology-first:

1. **Fig. 1 — ecological response architecture**  
   common pollinator-functional change → starting state → local context → response states
2. **Fig. 2 — minimal branch generator**  
   original and independent ablation evidence for pre-existing functional position
3. **Fig. 3 — downstream propagation**  
   network-context branch allocation versus assurance attenuation
4. **Fig. 4 — cross-island challenge**  
   branching, propagation, buffering/alternative states, axis decoupling, and retained failure

Detailed state-separability diagnostics are Supporting Information only (`Fig. S1` / `Table S2`). They are inference guards, not the primary biological novelty.

Figure and table routing is declared in:

- [`data/design/simulation_manuscript_figure_layout_v1.json`](data/design/simulation_manuscript_figure_layout_v1.json)
- [`data/design/island_ecology_jecology_submission_manifest.json`](data/design/island_ecology_jecology_submission_manifest.json)

## What this paper does not claim

This study does **not** claim that:

- plant island syndromes are false;
- all island plants follow one post-establishment reproductive trajectory;
- all 13 external systems share one empirical mechanism;
- the 13-system challenge set estimates global prevalence of response states;
- the synthetic functional coordinate is automatically corolla length, colour, nectar guides, FDQ, or any other named empirical trait;
- visitor richness, visitor identity, or visitation rate alone measures effective pollination service;
- state compatibility constitutes empirical causal identification;
- Dominica should be retuned until it fits.

## Future empirical translation

Three high-value empirical tracks remain open, but they are **not submission blockers** for the current paper:

1. **real signed functional starting position** — define an outcome-blind, source-native plant position relative to a pollinator functional centre;
2. **real network context → effective service** — link partner context to rate-weighted direct effectiveness rather than visitation alone;
3. **complete causal bridge** — close `pollinator functional change → effective service → dependency/assurance → downstream response` on compatible matched units.

These are prospective tests generated by the present paper, not missing data that must be filled before submission.

## Reproducibility

Primary numerical claims are stored in frozen JSON artifacts, and manuscript figures are rendered deterministically from those artifacts.

Key result files include:

- [`data/results/constraint_mechanism_abm_v11_factorial_summary_frozen.json`](data/results/constraint_mechanism_abm_v11_factorial_summary_frozen.json)
- [`data/results/constraint_mechanism_abm_v12_residual_trait_causes_frozen.json`](data/results/constraint_mechanism_abm_v12_residual_trait_causes_frozen.json)
- [`data/results/abm_v12_branch_generator_independent_robustness_frozen.json`](data/results/abm_v12_branch_generator_independent_robustness_frozen.json)
- [`data/results/network_context_buffering_capability_robustness_frozen.json`](data/results/network_context_buffering_capability_robustness_frozen.json)
- [`data/results/constraint_mechanism_abm_v14_assurance_buffering_robustness_frozen.json`](data/results/constraint_mechanism_abm_v14_assurance_buffering_robustness_frozen.json)
- [`data/results/system_agnostic_abm_multi_system_validation_v2_frozen.json`](data/results/system_agnostic_abm_multi_system_validation_v2_frozen.json)

Cross-platform frozen-artifact paths are normalized to POSIX-style relative paths so committed metadata remains stable across operating systems.

For anonymous review, the repository contains a review-archive builder:

```bash
python scripts/build_island_ecology_review_archive.py
```

The archive intentionally excludes title-page and author-identifying material.

## Submission status

Completed:

- scientific H1–H5 closure;
- independent branch-generator replication;
- 54-unit global screen and 13-system strict challenge;
- protected negative results and claim boundaries;
- island-syndrome literature synthesis;
- Journal of Ecology V2 anonymous manuscript;
- expanded Methods and Fig./Table cross-references;
- Supporting Information;
- cover-letter draft;
- figure captions, references, and submission manifest;
- anonymous review-archive routing.

Still external to the scientific analysis:

- final title-page author/affiliation metadata;
- final immutable public archive/DOI before publication;
- final submission-system metadata.

## Historical material

The repository contains older field-design, channel-identification, empirical-bridge, and method-first manuscript work. Those files remain useful as provenance and for future empirical translation, but they are **not the current manuscript mainline** when they conflict with the canonical state above.

In particular:

- Issue #91 field work is a future empirical-translation programme, not a blocker for the present synthetic island-ecology paper;
- method-first MEE drafts are archived alternative framings;
- state-separability is a supporting inference layer rather than the headline contribution.

When older documentation conflicts with the current paper state, prefer:

1. [`data/design/simulation_study_mainline_20260824.json`](data/design/simulation_study_mainline_20260824.json)
2. [`docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md`](docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md)
3. [`docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md`](docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md)
4. [`data/design/island_syndrome_literature_claim_matrix_20260824.json`](data/design/island_syndrome_literature_claim_matrix_20260824.json)
