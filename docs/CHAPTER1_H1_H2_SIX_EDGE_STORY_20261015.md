# Chapter 1: two families, six pairwise links (2026-10-15)

**Status: editorial proposal.** The author's revised structure supersedes the earlier proposal to renumber the four historical H1–H4 results in ordinal order. Original code/results, source hypothesis IDs, source-specific inference families and main manuscript are unchanged. **No statistical or evolutionary causality is newly identified by this schema.**

## Research question

Four conceptual variables: D = corrected geographic isolation, R = reproductive traits, F = floral traits, P = experimental pollen limitation.

- **H1: Isolation associations (3 spokes):** H1.1 D–R, H1.2 D–F, H1.3 D–P.
- **H2: Relationships among responses (3 edges):** H2.1 R–F, H2.2 R–P, H2.3 F–P.

The result is the six undirected edges of a four-variable graph, **not** a tested four-variable joint structural-equation model. Their measurements, specimens and uncertainty units differ. The statement “downstream” is conceptual grouping, not historical temporal ordering.

## Exact connection to completed Chapter 1 source families

| Proposed narrative ID | What it asks | Existing source readout | Evidence status, no overclaim |
|---|---|---|---|
| **H1.1** | Does geographic isolation co-vary with reproductive traits? | Former **H1** seven-trait region-specific island association for SC, selfing mating system and autonomous selfing; H2a selfing_core is auxiliary | SC slope is recurrent across four regions/sensitivity scopes. Not a causal distance intervention, universal selfing-rate increase or six-locus model outcome. |
| **H1.2** | Does geographic isolation co-vary with flower colour/architecture/accessibility? | Former **H1** region-specific floral atomic outcomes. Former **H2** conditional isolation slope \`F ~ D + selfing_core + area + climate\` belongs here as **sensitivity/conditional isolation effect** | Floral direction/support depends on region and trait. Conditional distance association is not proof of direct selection independent from selfing. |
| **H1.3** | Does geographic isolation co-vary with current measured pollen limitation? | Former **H3** adjusted GloPL geographic gradient | β=+0.09191, SE=0.03806, p=0.01594, 2,969 published experiments; neither pollinator number nor historical selection identified. |
| **H2.1** | Do reproductive traits co-vary with floral traits after ecological/geographic adjustment? | Former **H2** regressions estimate coefficients for selfing_core when predicting generalized_accessible or plain_colour with distance, area and climate | **Partly calculable from saved models, but not yet frozen as an independent primary H2.1 hypothesis.** Previous confirmatory/primary claim concerned the distance slope after conditioning, not its selfing coefficient. Sign and significance vary by region/trait. Need an explicit predictor/response, denominator and multiplicity decision before promoting a new H2.1 primary. |
| **H2.2** | Does current pollen limitation co-vary with reproductive traits? | Former **H4**, exact-species Direct-only selfing_core–GloPL comparison | β=−0.29830, p=0.00417, 455 species, 409 publications; post-hoc functional compatibility. SC atomic alone is imprecise; score is not identical to SC. |
| **H2.3** | Does current pollen limitation co-vary with floral traits? | Former **H4**, exact-species Direct-only generalized_accessible–GloPL comparison | β=−0.29566, p=0.02334, 143 species, 143 publications; post-hoc functional compatibility. Does not support a general effect of all colours/shapes. |

**Historical ID–new narrative map:** old H1 reproduction → H1.1; old H1 flower traits → H1.2; old H2 selfing-adjusted **isolation coefficient** → H1.2 conditional analysis; old H2 **selfing_core conditional coefficient** → candidate H2.1 descriptive association; old H3 → H1.3; old H4 selfing_core → H2.2; old H4 generalized_accessible → H2.3. The old H2 model cannot be assigned to H2.1 in full without silently changing its original estimand.

Source of truth: [Chapter 1 current frozen contract](https://github.com/zuizui0223/island/blob/main/config/chapter1_submission_current.json), [the accepted source manuscript](https://github.com/zuizui0223/island/blob/main/submission/chapter1_current/MANUSCRIPT.md), [evidence map](https://github.com/zuizui0223/island/blob/main/submission/chapter1_current/H1_H4_EVIDENCE_MAP.md). The companion editorial implementation is [island PR #319](https://github.com/zuizui0223/island/pull/319).

## Causal interpretation and hypotheses, not tested causal arrows

**Observed:** D↔R, D↔F, D↔P within the relevant subsets. R↔P and F↔P in separately exact-species matched published pollen-addition data (post-hoc, with different sample sizes). R↔F terms are estimable within the existing conditional island-aggregated H2 model but are not a predeclared new primary six-edge test.

**Not demonstrated:** \`D → past pollinator loss → pollen limitation → independent evolution of R/F → improved fecundity → population persistence\`, and not a mediation analysis. The six associations are estimated in **different datasets/grains**: area/climate-adjusted island flora fractions, publication/site GloPL LRR, and exact matched species-level trait/pollen records. They cannot be joined into an inferred one-population causal triangle without a new source-compatible join and causal design.

**Relationship of existing Chapter 2 Q1–Q4**

- **Q1 selection/reproductive payoff** is most directly motivated by H1.3 and supplies a *model-internal* conditional route compatible with H1.1/H1.2 and the H2 edges. Evolving autonomous selfing capacity A is not required for low-supply investment I reduction; evolving A changes between-replenishment differences. Model Q1 has no calibrated GloPL LRR, no measured coastline isolation and no literal H1 SC or floral-colour phenotype.
- **Q2 sequence** addresses **temporal order**, which cannot be inferred from any of these six cross-sectional correlations. Placing H2.1 after H1.1 and H1.2 does not imply R evolves before F.
- **Q3 genetic realization** concerns the transition from conditional parent contributions to transmitted alleles, relevant to the possibility of region-specific floral responses, but not a fitted explanation for observed H1.2 directions.
- **Q4 occupancy/persistence** is a **fifth outcome not present in these six Ch1 pairwise edges**. Its separate synthetic demographic interventions are not validations of H2.2/H2.3, where the observed outcome is contemporaneous pollen-limitation LRR.

The proposed headings for a Chapter 1 paper are **H1 Isolation-related ecological and reproductive patterns** (H1.1 reproductive traits / H1.2 floral traits / H1.3 pollen limitation), then **H2 Associations among reproductive responses** (H2.1 reproduction–flower / H2.2 reproduction–pollen limitation / H2.3 flower–pollen limitation), followed by a synthesis asking how these different associations might arise. Statistical Methods/Results can retain primary/secondary labels separately; do not portray all six as equally confirmatory.

**Migration contract:** This is reader-facing nomenclature only until manuscript+SI+figures+test references have been coherently migrated with old/new keys and numerical table identity checks. Keep all frozen H1–H4 IDs for reproduction; do not rename source data or retrospectively preregister H2.1 or H2.2/H2.3.
