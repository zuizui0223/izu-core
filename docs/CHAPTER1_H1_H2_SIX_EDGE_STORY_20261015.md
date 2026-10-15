# Chapter 1: two families, six pairwise links (2026-10-15)

**Status: editorial proposal.** The author's revised structure supersedes the earlier proposal to renumber the four historical H1–H4 results in ordinal order. Original code/results, source hypothesis IDs, source-specific inference families and main manuscript are unchanged. **No statistical or evolutionary causality is newly identified by this schema.**

## How to present and answer all six questions

For the actual Chapter 1 reader-facing wording, existing sample denominators, one-sentence answers and recommended figure grouping, see the [Chapter 1 six-question reader guide](https://github.com/zuizui0223/island/blob/docs/hypothesis-story-order-20261015/submission/chapter1_current/SIX_QUESTIONS_READER_GUIDE_20261015.md) on the matching editorial [island PR #319](https://github.com/zuizui0223/island/pull/319).

The crucial biological interpretation is **not a six-step causal chain**. Isolation and contemporaneous pollen limitation are positively associated (old H3), and island floras show recurrent SC but contingent floral changes (old H1); separately, exact-species reproductive-assurance and accessibility scores are associated with *lower* contemporary pollen limitation (old H4). This is compatible with a background reproductive constraint coexisting with compensatory-function differences, but **actual buffering mediation is not estimated** because source sample units differ. The R–F coefficient in old H2b is the source for H2.1 only as a conditional descriptive finding; the same old model's *isolation coefficient* is H1.2 evidence. For example, the tropical all-analysis R coefficient for accessibility was **−0.0458**, whereas Direct-only was **+0.0239** (different evidence scopes, not a preregistered H2.1 family test).

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

## Where Q4 belongs: a distinct population-level outcome, not a missing Ch1 edge

The six Ch1 relationships exhaust pairwise **associations among D (distance), R (reproductive traits), F (floral traits), and P (contemporaneous pollen limitation)**. They do **not** address **S (future population occupancy or persistence)**. Q4 keeps S visible as the distinct demographic endpoint after conditional expression/genetic-history preparation.

**Corrected three-level story:**

1. **Ch1 H1.1–H1.3:** how observed island isolation relates to R, F and P (different source universes/denominators).
2. **Ch1 H2.1–H2.3:** R–F, R–P and F–P associations; no measured historical arrow among the three, and H2.2/H2.3 are post hoc GloPL associations.
3. **Ch2 Q1–Q4:** how synthetic visitor limitation changes reproductive returns (**Q1**), what order of responses is realized (**Q2**), whether finite inheritance retains the alleles necessary for a specified response (**Q3**), and whether *different inherited/prepared reproductive states* change **future population occupancy S under imposed conditions (**Q4**).

Q4 conceptually addresses how **persistence filtering** could affect the contemporary species/trait composition seen in Ch1 H1.1/H1.2 even when phenotypic evolution and colonization are different processes. **This is a hypothesis about unobserved assembly history, not a measured link.** It does **not** become Ch1 H2.4: Ch1 lacks matched longitudinal occupancy S and therefore cannot fit an S edge to R/F/P or estimate the causal survival contribution to island flora.

The original Chapter 2 Q4 is narrower than generic "breeding system improves persistence." An independently prespecified, **assigned phenotype-expression-order × viable-selfed-seed treatment** experiment showed a small K8-versus-K48 contrast of treatment sensitivities with the pollen background B fixed at 48: **+0.0077457 occupancy-probability units**, 95% paired visitor-history bootstrap **[+0.0024972,+0.0130155]**. Its original near/far assigned-order effect was practically equivalent within its specified margin; separate resource-window and late-vs-early timing primary decisions did not pass. Other preparation/initial-mean results have distinct source cohorts and unresolved mediation. **Do not infer the future benefit of spontaneously evolving A first, or the origin of geographic SC/flower trait distribution from this result.**

**Difference from Ch1 H2.2/H2.3:** those source coefficients predict **current pollen-addition log response ratio P**, not probability S of occupied population after 80 model updates. A reduction in current pollen limitation can coexist with no detectable occupancy gain under ceiling/floor or demographic regulation; the studies do not estimate an empirical P→S effect. The model's demographic capacity K is not geographic island area.

**Reader-facing Japanese close:**
> Q1–Q3の結果から、選択される形質と実際に遺伝する形質は一致しない場合がある。Q4はさらに、進化・準備された繁殖状態が集団の存続に及ぼす影響も人口学的条件に依存することを、別の操作実験として検証する。ただし、Ch1で観察した植物相がQ4による存続選別で形成されたという因果関係は未特定である。

See the parallel [Ch1 six-question guide and explicit Q4 placement](https://github.com/zuizui0223/island/blob/docs/hypothesis-story-order-20261015/submission/chapter1_current/SIX_QUESTIONS_READER_GUIDE_20261015.md).

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
