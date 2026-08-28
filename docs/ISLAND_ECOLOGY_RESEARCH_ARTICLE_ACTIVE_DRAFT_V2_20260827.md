# Conditional response geometry under island pollinator reorganization

**Status:** active working manuscript v2 — not submission-ready  
**Updated:** 2026-08-27  
**Inference architecture:** synthetic primary analysis + comparative reality boundary + focal Izu empirical triangulation  
**Controlling state:** `docs/CHAPTER2_CANONICAL_STORY_20260827.md`, `data/design/chapter2_active_manuscript_mainline_20260827.json`, `data/results/chapter2_scientific_gate_final_20260827.json`

## Working title

**Conditional response geometry under island pollinator reorganization: from synthetic regime structure to source-state matching in the Izu Islands**

## Abstract

Island floras display recurrent reproductive and floral syndromes, yet comparative work also shows that the direction of island-associated responses differs among lineages and biogeographic contexts. This heterogeneity raises a mechanistic question distinct from asking whether island floras differ on average: when pollinator functional environments are reorganized, why can already-established plant lineages respond in opposite directions?

We first used a synthetic plant–pollinator model to map island-minus-mainland service across a standardized plant matching coordinate while holding pollinator-community realizations matched across starting positions. We then challenged the response geometry across a fixed 10-parameter Latin-hypercube design, decomposed starting-position and realized-community contributions, quantified directional sign changes under local interaction filtering, and tested whether autonomous reproductive assurance could reverse service-decline outcomes. A separate frozen source-readiness audit asked whether 25 existing research entries could support an outcome-independent external prediction challenge; none met the full predictor, target and chronology contract, so no cross-system classifier was fitted. Finally, we performed a source-locked secondary analysis in the Izu Islands using published plant floral-tube and pollinator proboscis information to ask whether source floral position and a broad island shift in pollinator functional composition organize realized trait matching.

Synthetic responses were non-monotonic. Forty-one of 96 matched community realizations contained both positive and negative responses across starting positions, while 42 were all-positive and 13 all-negative. Mixed mean geometry persisted at 16 of 48 points in the joint parameter design; greater partner loss and lower partner arrival had the largest sign-stable associations with a larger negative response region. In the baseline response matrix, community realization accounted for 80.17% of total sum of squares, starting-position-by-community non-additivity for 17.64%, and starting position alone for 2.18%. Local filtering altered response sign asymmetrically, whereas autonomous assurance produced no sign rescue among 580 eligible declines from 0.5× to 4× despite broadly reducing decline magnitude. In the Izu secondary analysis, a frozen source-state projection strongly tracked raw realized trait matching across 83 plant × island-site rows (slope = 0.567; 95% CI 0.298–0.836; 63/83 sign concordance), but exact island-specific centre magnitudes were not uniquely identified and the same projection did not explain the source paper’s null-corrected matching response (slope = 0.033; 95% CI −0.268–0.335).

Together these results support a conditional rather than universal account of post-establishment island response. Partner turnover defines a response regime, starting state organizes average geometry, realized community strongly conditions individual outcomes, and local interaction filtering reallocates branch identity. The Izu analysis provides an empirical echo of source-state and community-composition structure in realized matching, but not evidence for non-random partner sorting beyond background community composition or for causal floral evolution. Island response is therefore better treated as a state- and community-contingent geometry than as a single directional island syndrome.

**Keywords:** island syndrome; plant–pollinator interactions; functional matching; response heterogeneity; ecological networks; source state; Izu Islands; reproductive assurance

# Introduction

Islands are natural experiments in colonization, ecological simplification and the reorganization of biotic interactions. Plant reproduction is especially exposed to those changes because successful reproduction depends not only on abiotic conditions and mate availability but also on the identity, abundance and functional compatibility of pollinators. Comparative studies have therefore documented recurrent island-associated changes in breeding systems, pollination strategies and floral traits (Grossenbacher et al., 2017; Traveset & Navarro, 2018; Zell et al., 2025).

Yet an aggregate “island syndrome” can arise through several biologically distinct processes. Assembly can filter which lineages reach and persist on islands. Evolution after colonization can change floral and reproductive traits. Already-established populations can also respond ecologically when interaction partners are lost, replaced or redistributed. Conflating these processes creates a stronger expectation than the evidence warrants: that one broad island-associated perturbation should push all established lineages toward the same biological state.

Several lines of evidence argue against that expectation. Baker’s law is fundamentally an assembly prediction about the capacity for uniparental reproduction during colonization, not a guarantee that established island populations will converge on uniformly high realized selfing (Pannell et al., 2015). Pacific island–mainland comparisons likewise do not support a universal direction of flower-size evolution; responses depend on source size, pollination mode and archipelago context (Hetherington-Rauth & Johnson, 2020; Ciarle et al., 2025). At the network level, island pollination networks may be smaller or functionally reorganized without every plant experiencing the same change in functional service (Traveset et al., 2016). Japanese island networks further indicate that losses in pollinator functional diversity and trait matching can be more informative than pollinator species richness alone (Hiraiwa & Ushimaru, 2017, 2024).

At the dissertation scale, the preceding comparative chapter supplies the when/where handoff: isolation-associated floral and reproductive filtering is detectable in multiple biogeographic contexts, but the observed multivariate response vectors differ. That result does not by itself identify why the vectors differ. It motivates a narrower post-establishment question: **when pollinator functional environments are reorganized in a broadly island-like direction, what determines whether an already-established plant lineage benefits or declines?**

A matching framework makes a clear prediction. The effect of partner loss or replacement depends on where a plant begins relative to the functional distribution of available partners. But starting state cannot be assumed to determine the realized outcome by itself. The actual community trajectory determines which partners persist, arrive or disappear, and local interaction filtering determines which parts of the feasible interaction set are realized. A downstream compensating route such as autonomous reproduction may then alter the magnitude of a service loss without necessarily changing its sign. The resulting object is not a single island effect but a **conditional response geometry**.

We therefore separate four levels of explanation. First, partner turnover can change the broad response regime. Second, plant starting functional state can organize the average response surface. Third, stochastic or historically contingent community realization can strongly condition cell-level outcomes. Fourth, local availability and interaction filtering can reallocate branch identity after the global community has been formed. Autonomous assurance is treated separately as a downstream modifier. This decomposition is intentionally narrower than a complete theory of island evolution: it addresses post-establishment response and does not identify the historical processes that produced a regional species pool, source state or colonization route.

The synthetic analysis asks five linked questions. (1) Across plant starting positions, where does the island-minus-mainland functional-service contrast change sign? (2) Does mixed-sign geometry persist across a declared joint parameter region, and which dimensions accompany transitions among all-positive, mixed and all-negative regimes? (3) How much response variation is associated with starting position, realized community and their non-additive combination? (4) At what strengths and in which direction does local interaction filtering change response sign? (5) Can a downstream autonomous-assurance route reverse negative reproductive outcomes while upstream service is held unchanged?

We then connect the synthetic result to empirical island ecology in two deliberately asymmetric ways. A source-audited external-system inventory is retained only as a **reality boundary**: real island systems exhibit branching, same-direction propagation, buffering, axis decoupling and retained falsification, so a universal one-direction model would already be too strong. We do not pool these systems as equivalent validation units. Instead, we focus empirical depth on the Izu Islands, where published floral and pollinator functional traits allow a frozen source-state analysis. This secondary analysis asks whether source floral position and a broad shift in pollinator functional composition organize realized trait matching. Crucially, it also tests the stronger alternative: whether the same projection explains null-corrected matching after background plant and pollinator community composition has been removed.

Our central prediction is therefore conditional, not universal: partner turnover changes the response regime; starting functional state organizes average matching geometry; realized community and non-additive state-by-community structure can dominate individual outcomes; local filtering can reallocate branch identity; and downstream assurance may attenuate losses without reversing them. The Izu analysis is treated as empirical triangulation of this source-state/community logic, not as proof that the synthetic coordinate is a calibrated floral trait or that a specific pollinator shift caused floral evolution.

# Materials and Methods

## Inference architecture and claim boundary

The paper has three evidence layers with different inferential roles.

1. **Synthetic primary analysis.** All response thresholds, parameter-regime diagnostics and decomposition results are generated by a declared synthetic model. No empirical island outcome was used to fit the reported response thresholds or to select seeds after inspecting results.
2. **Comparative reality boundary.** External island systems retained in the project registry demonstrate that real island responses occupy multiple qualitative states. They are not treated as a meta-analysis, prevalence sample or validation coverage of the synthetic model.
3. **Focal Izu empirical triangulation.** A source-locked secondary analysis uses published Izu plant–pollinator data to test whether source floral state and broad pollinator functional composition structure realized trait matching. This analysis is not used to calibrate the synthetic thresholds.

The synthetic plant coordinate is standardized to [0,1] and is not identified with a named empirical floral trait. Its sign transitions must not be interpreted as calibrated corolla-length, colour or nectar-guide thresholds.

## Synthetic pollinator environments and matching

The baseline mainland-like scenario contained nine pollinator types, partner arrival probability 0.28, partner loss probability 0.015, trait dispersion 0.22, generalist fraction 0.35 and replacement fraction 0.05. The island-like scenario contained four pollinator types, partner arrival probability 0.12, partner loss probability 0.055, trait dispersion 0.16, generalist fraction 0.58 and replacement fraction 0.22. Generalist breadth was 0.42 and specialist breadth 0.16. Replacement partners received a multiplicative effectiveness penalty of 0.82.

For plant position x and pollinator position p, matching was

`match = exp(-(|x-p| / breadth)^2)`.

Total pollinator richness did not automatically create greater total visitation. Service was computed from the mean extant-partner match using

`service = 1 - exp(-saturation * mean_match)`.

The exact model specification, reproductive equations and parameter bounds are frozen in the accompanying Supplementary Information and machine-readable design files.

## Matched response geometry

Starting positions were evaluated on a 21-point grid from 0 to 1 in increments of 0.05. Within each realization, every starting position experienced the same mainland-like pollinator trajectory and the same island-like trajectory. This matched design separates the average effect of starting position from differences created by drawing a different pollinator history for each starting state.

We generated 96 matched community realizations. The primary response was final island-minus-mainland functional service. A realization was classified as mixed-sign when at least one starting position produced a positive response and at least one produced a negative response. Mean response was also calculated at every starting position across realizations.

## Joint parameter robustness and regime drivers

A fixed 48-point Latin-hypercube design simultaneously varied ten declared perturbation and matching dimensions: trait dispersion, generalist fraction, replacement fraction, partner loss, partner arrival, saturation, trait adjustment, generalist breadth, specialist breadth and replacement penalty. Each design point used 24 matched community realizations under a common seed ensemble.

Design points were classified as mixed, all-positive or all-negative according to the sign of the mean response across the 21 starting positions. To diagnose rather than retune the fixed surface, the fraction of starting positions with negative mean response was regressed on all ten centered and range-scaled parameters in a single additive ordinary-least-squares model. No model selection or post-hoc interaction search was used. We report full-range coefficients, leave-one-point-out coefficient sign stability, in-sample R² and leave-one-point-out RMSE.

## Starting-state and community-realization decomposition

For the baseline 21 × 96 response matrix, and analogously for each joint-design matrix, total sum of squares was partitioned exactly into a starting-position main component, a community-realization main component and a non-additive remainder. Because there is one simulated value per cell, the remainder is not interpreted as a pure empirical interaction variance component. We also recorded cell-level sign disagreement between the observed response and the fitted additive value.

## Local filtering and autonomous assurance

Local context was represented as availability and interaction filtering, not as an added beneficial support process. Filtering strengths were 0, 0.10, 0.25, 0.40, 0.50, 0.60 and 0.75 under common seed ensembles. The fixed threshold design used saturation 1, 2 and 3; 12 replicates per saturation; four local contexts; 24 lineages; and 120 steps. For every lineage contrast, we recorded the first filtering strength at which the reproduction-response sign differed from the zero-filtering baseline and retained the full baseline-sign → current-sign transition table.

The autonomous-assurance route was varied independently with multipliers 0, 0.5, 1, 1.5, 2, 3 and 4. A lineage was eligible for sign rescue when both island-minus-mainland effective service and reproduction were negative at multiplier 0. We required upstream effective service to remain invariant across assurance multipliers before interpreting any reproductive rescue.

## Comparative external-system boundary

The project maintains a source-audited comparative universe larger than the strict manuscript challenge set. The strict set contains 13 external state challenges, while 12 additional analytical and model-development targets are retained separately; these 25 research entries are not interpreted as independent archipelagos.

After freezing the synthetic model, we conducted a separate source-readiness audit for a stronger external-prediction claim. Four model-derived coordinates were declared without refitting: turnover imbalance `T = z_loss - z_arrival`; standardized source functional displacement `D0`; standardized realized-community shift `C`; and local filtering `F = 1 - realized opportunity / feasible opportunity`. Assurance remained a downstream modifier rather than a sign-regime axis. We defined five alternatives: a universal-direction baseline (`H0`), starting-state-only (`H1`), turnover-only (`H2`), source-state-by-community matching (`H3`) and `H3` plus local filtering (`H4`). Formal comparison required at least four geographically de-duplicated systems with one comparable plant-response target, matched outcome-independent inputs sufficient for `H0`–`H3`, and no imputation from observed response state. If this gate failed, model comparison, leave-one-system/archipelago-out evaluation and permutation were declared not evaluable rather than run on a repaired data set.

## Izu source-state empirical triangulation

We recovered and byte-locked the supplementary source associated with Hiraiwa & Ushimaru (2017). Against the current 2024 named-pollinator archive, 202 of 209 taxa (96.65%) received a safe numeric join using exact or whitespace-normalized names; no fuzzy, family, guild, body-size or midpoint substitution was allowed. The 2017 and 2024 sources agreed on all 532 matching taxon × site presences among the safely joined taxa.

Before fitting the target response, the source regime was frozen as the study-defined three continental sites pooled by source-recorded visits. The resulting continental pollinator functional centre was 7.32665 mm. For plant species occurring in the continental source and at least one Izu island, initial signed position was defined as

`initial position = continental source tube mean - continental pollinator centre`.

Thirty plant species met the eligibility rule. For each island, the broad pollinator-centre shift relative to the continental source was used to form the preregistered geometric projection

`predicted matching change = abs(initial position) - abs(initial position - centre shift)`.

The primary raw target was the published species-level realized trait-matching response, analysed across 83 plant × island-site rows with island fixed effects and plant-cluster-robust inference. Reproductive outcomes were not used to choose the mapping.

We then applied four structural attacks without retuning the frozen projection: (1) the source paper’s null-corrected species-level matching response was used as the target; (2) initial source positions were permuted among plant identities 10,000 times while retaining island coverage and outcomes; (3) all 5! = 120 assignments of the observed island centre shifts to island labels were enumerated; and (4) a source-position-only model was compared with the full centre-shift projection on the same rows. These attacks separate raw realized geometry from claims about uniquely identified island centres or non-random partner sorting beyond background community composition.

# Results

## Synthetic response geometry was non-monotonic

Across 96 matched community realizations, 41 contained both positive and negative island-minus-mainland service responses across the starting-position grid. Forty-two were positive across the full grid and 13 negative across the full grid.

The mean response geometry was mixed-sign. Mean response was positive approximately from 0.00–0.30 and 0.70–1.00 and negative from 0.35–0.65, with sign transitions between 0.30–0.35 and 0.65–0.70. These locations describe the declared synthetic coordinate only.

## Mixed geometry persisted across joint perturbation but was not universal

Of the 48 fixed joint parameter points, 16 produced mixed mean geometry, 22 all-positive mean geometry and 10 all-negative mean geometry. The model therefore contains a genuine transition surface rather than forcing branching under every parameter combination.

The ten-parameter additive diagnostic explained R² = 0.611 of variation in the negative fraction of the starting-position grid, with leave-one-point-out RMSE = 0.329. Partner-loss multiplier had the largest positive full-range coefficient (+0.634) and partner-arrival multiplier the largest negative coefficient (−0.626); both retained their signs in all 48 leave-one-point-out fits. These quantities diagnose the declared surface and are not field-calibrated causal effects.

## Realized community dominated cell-level response variation

In the baseline 21 × 96 response matrix, starting position accounted for 2.18% of total sum of squares, community realization for 80.17% and the non-additive remainder for 17.64%. Thus starting state organizes the mean geometry but does not determine individual outcomes by itself. The realized community trajectory is the dominant source of cell-level variation within this design.

## Local filtering reallocated response branches asymmetrically

Across the fixed threshold design, 737 lineage contrasts changed sign at least once as filtering strength increased. Sign switching was directional: positive baselines crossed to non-positive more readily than negative baselines crossed to non-negative at every non-zero tested strength. The median first sign-change strength was 0.40 across all contrasts that switched. These values are synthetic design descriptors rather than ecological thresholds.

## Autonomous assurance attenuated magnitude without rescuing sign

Among 580 lineages with both negative baseline service and negative reproduction contrasts, no assurance multiplier from 0.5× through 4× produced sign rescue. Upstream effective service was identical across assurance multipliers. Nevertheless, most eligible declines improved in magnitude, with magnitude improvement remaining above 92% even at the largest tested multiplier. In this implementation, autonomous assurance is therefore a downstream magnitude attenuator, not a general sign-changing rescue mechanism.

## Izu raw matching carried strong source-state and community-composition structure

The frozen Izu projection produced a positive association with realized raw trait matching across 83 plant × island-site rows and 30 plant clusters: slope = 0.5669, cluster-robust SE = 0.1316 and 95% CI = 0.2977–0.8361. Pearson r was 0.570, Spearman rho 0.527 and sign concordance 63/83 = 75.9%. All five leave-one-island slopes were positive.

Correct plant source-state identity mattered. In 10,000 fixed-seed permutations of initial source positions among plant identities, no null slope reached the observed raw slope; the empirical one-sided probability was 1/10001.

However, the raw association did not uniquely identify exact island-specific pollinator-centre magnitudes. Across all 120 assignments of the five observed centre shifts to island labels, 13 assignments produced slopes at least as large as the real assignment. Moreover, a source-position-only model with island fixed effects described raw response at least as well as the full centre-shift geometry (R² = 0.409, AIC = 362.1 versus R² = 0.365, AIC = 368.1). The strongest raw information therefore resides in source floral state plus broad community composition rather than precise identification of five island centre magnitudes.

## Izu null-corrected matching did not support beyond-composition sorting

Using the exact same frozen predictor and rows, the source paper’s background-community-corrected matching response was not associated with the signed-position projection: slope = 0.0333, cluster-robust SE = 0.1473, 95% CI = −0.2680–0.3346, Pearson r = 0.061, Spearman rho = 0.099 and sign concordance 42/83 = 50.6%. In the plant-position permutation, 3918 of 10,000 null slopes were at least as large as the observed corrected slope.

Thus the Izu reanalysis supports a source-state/community-composition structure in realized raw matching, but not non-random partner sorting beyond the source paper’s background-community null. This distinction is central to the empirical interpretation.

# Discussion

## Island response is better represented as conditional geometry than a universal syndrome

The synthetic analysis rejects a one-direction description of post-establishment response within the declared model. The same broad pollinator reorganization can yield positive, mixed or negative response regimes. Mixed mean geometry persists across a substantial part of the joint parameter design but disappears under other combinations, providing a meaningful failure boundary rather than a branching pattern that is guaranteed by construction.

This result changes the level at which an “island syndrome” should be interpreted. A recurrent aggregate pattern can coexist with heterogeneous lineage-level consequences. Partner turnover defines the broad response regime; starting functional state organizes the average mapping of plants onto that regime; realized community trajectory strongly determines cell-level outcomes; and local filtering further reallocates branch identity. A universal island effect is therefore not required even when the broad direction of community simplification is shared.

## The proximal why is hierarchical

The additional diagnostics clarify what the model does and does not explain. Starting position alone accounts for little cell-level variance, so the result cannot be reduced to “plants at one end benefit and plants at the other decline.” Instead, partner loss and arrival reshape the response surface, starting state places a plant on that surface, and the realized community determines much of the actual outcome. Non-additivity remains substantial. The proximal explanation is therefore hierarchical: **regime × starting state × realized community**, followed by local filtering.

The local-filtering result adds a second asymmetry. Filtering is not simply a buffer that occasionally rescues negative lineages. It changes branch identity in both directions but more readily converts positive baselines to non-positive states over the tested range. Downstream autonomous assurance plays a different role: it commonly reduces the magnitude of negative reproductive consequences yet never reverses their sign in the tested 0.5×–4× envelope. Treating these mechanisms separately prevents a generic “context matters” explanation from obscuring where sign changes actually enter the response chain.

## Comparative systems are a reality boundary, not validation coverage

The broader comparative program is useful precisely because real island systems do not collapse into one outcome vocabulary. Source-audited cases include branching, same-direction propagation, buffering, reproductive-axis decoupling and retained falsification. These cases establish empirical breadth and discipline model interpretation: a synthetic mechanism that could only produce one direction would be poorly matched to the diversity of observed island responses.

But this comparative universe is not a random sample of archipelagos, and different systems expose different outcomes, scales and uncertainty structures. We therefore do not interpret the fraction of systems assigned to a response state as ecological prevalence, and we do not claim that the synthetic model explains all admitted systems. Their role is to bound over-generalization and motivate a focused system in which more of the causal chain can be measured.

## Existing sources did not admit a formal external prediction challenge

None of the 25 audited entries passed the paper's full plant-response contract. Twelve were retained as retrospective explanatory tests, eight as reality boundaries and five as source-gated or unusable for this question. Earlier pre-target chronology exists for four narrower tests, but Dominica tested a publication-aware signed-position/selection-gradient direction and Menorca, Cabrera and Giannutri tested network architecture or local realization without a linked plant-response target.

Marginal predictor availability was not the limiting quantity by itself: direct or source-derived source state was available in 10 entries, community functional shift in 18, local filtering in 20 and a response quantity in 21 (Fig. S3). Those fields did not coincide on a common response family, matched transition unit and outcome-independent mapping. The number of geographically de-duplicated, prospective-like systems with complete `H0`–`H3` inputs was therefore zero, below the frozen minimum of four. We did not fit `H0`–`H4`, compute cross-system accuracy or run leave-one-system/archipelago-out and permutation tests. The result is a data-readiness and identifiability stop, not a failed fitted model.

## Izu provides depth, but the depth points to source state and community composition

The Izu Islands provide the deepest current empirical bridge because the same archipelago contains published floral traits, pollinator functional traits and contemporary interaction structure. This is a transparent data-depth rationale, not the result of an outcome-independent global ranking: candidate eligibility, scoring criteria, weights and missingness rules were not frozen before Izu became the focal programme. The frozen signed-position analysis initially appears to mirror the synthetic logic: correct plant source identity strongly organizes realized raw trait-matching change, and the result is distributed across five islands rather than produced by one island alone.

The structural audit is more informative than the raw positive slope by itself. Exact island-specific pollinator-centre magnitudes are not uniquely identified, and source starting position alone explains at least as much raw variation as the full geometric projection. Most importantly, the association disappears for the source paper’s null-corrected matching metric. Therefore the current empirical result does not identify non-random partner choice or a pollinator-centre selection mechanism beyond background community composition.

This is not a failure of the Chapter 2 framework. It locates the empirical signal at the same level highlighted by the synthetic variance decomposition: **source state and realized community structure matter strongly, while a stronger beyond-composition interaction mechanism remains unproven**. The Izu result is thus an empirical echo of conditional response geometry, not an external validation of the synthetic thresholds.

## From Chapter 1 to Chapter 3

At the dissertation scale, Chapter 1 asks when and where isolation-associated response vectors differ. Chapter 2 asks how a broad interaction reorganization can produce different outcomes and why source state and realized community must be retained in that explanation. The Izu bridge then motivates a deeper phenotypic question rather than closing the causal chain.

Chapter 3 examines one Izu lineage, *Campanula microdonta*, at higher phenotypic resolution. Current analyses indicate a large shared size/investment trajectory together with selected departures beyond common allometry. That structure is consistent with the broader lesson of Chapter 2—responses need not be uniform across axes—but it is not treated as proof that the Chapter 2 pollinator mechanism caused the observed floral divergence. Historical assembly, demographic history, abiotic environment and other selective agents remain viable explanations.

## Limitations and decisive next test

Several boundaries remain essential. The synthetic thresholds are not empirical trait thresholds. The joint-design coefficients are not field causal effects. The external-system registry is not a prevalence sample or a held-out prediction set. The source audit does not support placing systems into synthetic regimes from their observed outcomes. The Izu secondary analysis lacks plant-specific partner-weighted functional centres because the required legacy interaction-weight workbook has not been recovered through the current public route. The pollinator trait table is also not a complete site-exact numeric matrix for every taxon.

Most importantly, the current Izu analysis stops at realized matching. It does not show that the source-state/community geometry propagates through pollinator effectiveness into reproduction. The decisive prospective test is therefore plant-linked and preregistrable:

`visitor identity + exact/new proboscis + plant-specific visitor weights -> frozen plant-specific signed position -> single-visit pollen deposition -> direct reproductive dependency / mature seed outcome`.

A successful test would connect source-state/community geometry to reproductive function. A null result would retain the assembly/community-composition interpretation while rejecting a stronger functional-propagation claim.

# Conclusion

Island-associated interaction change should not be expected to generate one universal post-establishment plant response. In the synthetic model, partner turnover creates distinct response regimes; starting state organizes average geometry; realized community dominates cell-level variation; local filtering reallocates branch identity; and autonomous assurance attenuates decline magnitude without providing general sign rescue. A broad comparative island inventory preserves the empirical diversity and falsification boundary of this claim, but the current sources do not support formal cross-system prediction. In the Izu Islands, source floral state and broad community composition strongly structure raw realized matching, but the signal does not survive the source paper’s background-community correction and does not uniquely identify island-specific pollinator centres. The strongest current synthesis remains conditional and hierarchical: **island response emerges from the interaction of source state, community realization and local filtering, not from isolation alone and not from one universal syndrome.**

## References

Use the source-audited active reference ledger in `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md`. Hiraiwa & Ushimaru (2017, 2024) are the empirical sources for the Izu triangulation. External-system references remain in the comparative-grounding supplement and are not presented as validation coverage.
