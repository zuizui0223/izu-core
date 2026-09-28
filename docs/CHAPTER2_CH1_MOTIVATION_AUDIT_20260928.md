# Chapter 1 motivation audit for the independent Chapter 2 island study

Date: 2026-09-28. Scope: source-bound interpretation audit; no reanalysis, simulations or literature campaign.

## Authoritative sources

The local island repository was read through Git objects only; its working tree was not edited. Its current `origin/main` resolves to **9780d9a17ab060848c39a7418f02652cfd1f84a2**. Sources at that immutable commit:

- [Current submission contract](https://github.com/zuizui0223/island/blob/9780d9a17ab060848c39a7418f02652cfd1f84a2/config/chapter1_submission_current.json): selects the corrected 2026-09-24 geography baseline, superseding the older v14 result lock.
- [Current manuscript](https://github.com/zuizui0223/island/blob/9780d9a17ab060848c39a7418f02652cfd1f84a2/submission/chapter1_current/MANUSCRIPT.md): contemporary flora composition, H1–H4, conditional rather than causal decomposition.
- Model 3 comparison sources: `docs/MODEL3_CH2_BRIDGE_ECOLOGICAL_RESULTS_20260928.md`, `docs/CHAPTER1_OPEN_PROBLEMS_TO_UNIFIED_MODEL3_20260927.md`, `docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md`, and `docs/CHAPTER1_MODEL3_ISOLATION_CHANNEL_BRIDGE_20260927.md` at the current izu-core baseline. This audit does not independently revalidate every controlled-assay or natural-case source cited by those documents.

## What Chapter 1 actually establishes

The database contains 8,264 island units and 106,295 accepted angiosperm species, with 222,688 resolved raw trait cells; the primary H1 union contains 4,379 islands. Database coverage must not be presented as the denominator of every trait model.

| Finding | Current support | Interpretation allowed |
|---|---|---|
| H1: multivariate recurrence | Seven-response vector FDR-supported in all four regions; 26/28 primary coefficients positive | Recurrent response structure, not all traits uniformly changing or all regional component effects individually significant |
| H2: accessibility after assurance adjustment | Positive estimates in all four regions; FDR support in northern high latitudes (q=.000847) and tropics (.01616), not northern mid-latitudes (.1703) or southern extratropics (.2873) | Measured assurance does not statistically absorb all accessibility associations; direct pollinator selection is not identified |
| H2 robustness | Tropical Direct-only p=.0448 but q=.1196 | Tropical FDR support is evidence-scope dependent |
| H3: pollen limitation | 2,969 experiments; distance beta=.09191, p=.01575; supplemental-only beta=.04410, p=.31082 | Isolation-associated reproductive constraint, not directly observed pollinator decline or an effect equally supported under all measurement definitions |
| H4: exact-species functional association | Assurance score beta=-.29830, p=.00396 (455 species); accessibility beta=-.29566, p=.02187 (143 species) | Post-hoc contemporary associations, not historical mediation, observed selection or proof that the traits evolved to compensate for isolation |

Regional heterogeneity is substantive. The southern shallow/open-tube coefficient is negative (-.2166, p=.000370); northern high-latitude blue/purple architecture associations remain negative; tropical Direct evidence retains a positive yellow/orange × butterfly/deep-tube combination (q=.03949). These are trait associations, not measurements of the visitors that caused them. The manuscript's four geographic strata motivate a question about contingent responses; they are not four Model 3 calibration targets.

The manuscript itself leaves the historical edge missing: past pollen conditions → selection, sorting or persistence → present flora composition. It does not separate colonization filtering, community sorting and within-lineage evolution. Current pollen limitation includes pollen quantity, quality and mate availability, so replacing it throughout with “pollinator scarcity” would narrow its meaning without evidence.

## Research motivation in the user's first person

> Chapter 1で私が見いだしたのは、隔離に伴う繁殖戦略の変化には地域を越えて繰り返す部分がある一方、花の色や構造は一つの方向に揃わないということです。また、測定した繁殖保証で調整しても、花のアクセス性の関連は一部の地域で残りました。しかし、この比較だけでは、送粉環境の変化が実際に花の進化へどう伝わるのか、到着・消失の順序や植物集団の状態が何を変えるのかは分かりません。そこでChapter 2では、Chapter 1の地域差を再現するために設定を合わせるのではなく、島で植物と送粉者が出会い、失われ、再び到着する過程を独立に操作し、同じ現在の環境でも進化と存続がなぜ違いうるのかを調べたいと考えました。

This is proposed author wording derived from the conversation and current study findings. It does not assert undocumented field experiences, a personal discovery chronology, or that every proposed Chapter 2 comparison is already completed.

## Fixed assurance is a crucial boundary

Holding assurance ability at 0.5 rules out **evolution of that ability** in the bridge. It neither removes selfing nor fixes realized selfing. Visitor limitation can alter the fraction of offspring produced by selfing even when ability is constant. Hence:

- justified: floral-selection or inherited-investment responses can differ without evolving assurance ability in this model;
- not justified: assurance is unnecessary, selfing has no causal role, or the response is caused exclusively by direct pollinator selection;
- also not justified: increased realized selfing in a fixed-ability factorial demonstrates evolution of reproductive assurance.

Floral investment is an abstract costly trait, not the Chapter 1 plain-colour contrast or all floral architecture. The bridge also does not identify a cost-only mechanism because a cost-removal counterfactual was not part of that experiment.

## Exact overclaim / stale-completion locations in the existing bridge documents

Line numbers refer to files inspected in this audit; those files were not edited.

| Existing location and wording | Problem | Required claim ceiling |
|---|---|---|
| `CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md:15`, “Chapter 2 answers that problem with one nested Model 3.” | Could imply explanation of observed regional history | Model 3 tests compatible mechanisms; the historical Chapter 1 causes remain unidentified |
| Canonical bridge :58, “assurance is not required to create that floral-selection branch” | Fixed assurance is present, not absent | Evolution of assurance ability is not required under the specified fixed-assurance assay |
| Canonical bridge :101, “pollinator isolation repeatedly strengthens reproductive assurance” | Supporting paragraph reports realized selfing, not an increase in inherited assurance ability | Pollinator isolation increases realized reliance on selfing in that factorial |
| `CHAPTER1_OPEN_PROBLEMS_TO_UNIFIED_MODEL3_20260927.md:62`, “This directly resolves why Chapter 1 can retain a selfing-adjusted display signal” | A model possibility cannot identify the cause of comparative residuals | Offers a mechanism compatible with, but not identified by, the residual associations |
| Open problems :177, “resolved inside Model 3”; canonical bridge :80, “controls are now resolved” | Computational completion is conflated with mechanism identification | Counterfactual experiments completed; richness matching changes persistence too; stable latent branching and variance rankings remain unresolved |
| Open problems :182, “stronger than Chapter 1 observations → Chapter 2 possible mechanism” | No calibrated or longitudinal link establishes actual regional causation | Mechanistic evidence within the model is stronger; cross-chapter empirical linkage remains a possible mechanism |
| Canonical bridge :78, “resolves the apparent H3/H4 tension” | Logically reconciles findings but does not fill the historical causal edge | Stress and buffering are logically compatible; historical compensation remains untested |
| Canonical bridge :128, “natural islands already occupy multiple response modes predicted” | May sound like quantitative external prediction validation | Case evidence can support selected process links; cross-sectional mapping is not a same-unit evolutionary reconstruction |
| Open problems :13, “recur ... across all four” | Directional recurrence can be misread as universal component-level support | Joint H1 recurrence is supported; H2 accessibility adjusted support is concentrated in two regions and sensitivity dependent |

The current bridge result remains useful: natural isolation lowers inherited investment on average, a response-blind community intervention reverses the relative contrast, and larger plant populations change its magnitude. These are model-conditional findings. They should not be promoted into proof that selfing is unimportant, that all island floral reduction has one cause, or that Chapter 1's four regional patterns have been reproduced.

## Independent Chapter 2 question

**How do the timing and continuity of pollinator arrival, together with plant reproductive assurance and finite population history, determine which floral evolutionary responses and persistence outcomes can be realized on islands?**

Chapter 1 supplies the motivating discrepancy and measurement vocabulary. Chapter 2 must define its own interventions, comparisons and falsifiable predictions before new outcomes are examined. Natural island confrontation should test measured process links or independent predictions, retain failed and unavailable cases, and avoid assigning the four Chapter 1 regions to convenient synthetic regimes.
