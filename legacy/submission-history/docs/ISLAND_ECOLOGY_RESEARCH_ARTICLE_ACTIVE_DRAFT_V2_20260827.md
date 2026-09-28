# Response geometry under community reorganization

**Status:** active working manuscript v2 — mechanistic-funnel reconstruction; not submission-ready
**Updated:** 2026-08-28
**Inference architecture:** model possibilities → world confrontation → identifiability bottleneck → focal Izu mechanistic-resolution zoom
**Controlling state:** `docs/CHAPTER2_CANONICAL_STORY_20260827.md`, `data/design/chapter2_active_manuscript_mainline_20260827.json`, `data/results/chapter2_scientific_gate_final_20260827.json`

## Working title

**Response geometry under community reorganization: from ecological possibility to mechanistic resolution in island plant–pollinator systems**

## Abstract

The same environmental change can produce opposite biological responses, yet mean effects do not identify the state and community information that determines branch identity. We ask whether pollinator-community reorganization is better represented as a response geometry and what resolution is required to distinguish its mechanisms.

We exposed the interaction kernel in a frozen matching model, mapped island-minus-mainland service across matched starting positions, diagnosed fixed joint-design regime transitions, decomposed state and community contributions, and separated local filtering from downstream assurance. We then confronted this vocabulary with a source-audited 25-entry comparative universe and increased resolution in Izu using source floral state, pollinator composition, raw matching and null-corrected matching.

The exact per-realization sign coordinate was a trajectory-conditioned kernel difference. Of 96 matched community realizations, 41 were mixed, 42 all-positive and 13 all-negative; among 48 joint-design points, 16 mean geometries were mixed, 22 all-positive and 10 all-negative. Partner loss and arrival had the largest sign-stable regime associations. Realized community accounted for 80.17% of response-matrix sums of squares, non-additivity for 17.64% and starting position alone for 2.18%. Local filtering reallocated branches asymmetrically, whereas assurance produced zero sign rescues among 580 eligible declines. The comparative universe contained propagation, branching, buffering, axis decoupling and retained falsification, but zero entries jointly satisfied the outcome-independent state–community–context–outcome contract; formal external comparison was not evaluable. In Izu, the frozen projection tracked raw matching (slope 0.567, 95% CI 0.298–0.836) but not null-corrected matching (slope 0.033, 95% CI −0.268–0.335).

Community reorganization can therefore define a response regime without determining branch identity. World confrontation establishes the need for this richer response vocabulary but exposes a joint-measurement bottleneck. Increasing resolution in Izu localizes the current matching signal to source state plus background community composition, not additional non-random partner sorting. The resulting framework is model conditional, not a calibrated island predictor or an ultimate historical explanation.

**Keywords:** community reorganization; response geometry; plant–pollinator interactions; functional matching; realized community; identifiability; Izu Islands; reproductive assurance

# Introduction

Environmental change is often represented by a mean directional effect. That summary becomes insufficient when the same perturbation changes sign across biological starting states or community realizations. The central ecological problem is then not only how large the average response is, but what coordinate system represents the alternative response branches and what information identifies the branch realized by a particular lineage.

Islands provide a stringent setting for this problem. Colonization, ecological simplification and interaction reorganization can change plant reproduction through partner identity, functional compatibility and local realization. Comparative studies document recurrent island-associated changes in breeding systems, pollination strategies and floral traits (Grossenbacher et al., 2017; Traveset & Navarro, 2018; Zell et al., 2025), yet Baker's law concerns assembly during colonization rather than uniform response among established populations (Pannell et al., 2015), flower-size responses vary with source size and pollination context (Hetherington-Rauth & Johnson, 2020; Ciarle et al., 2025), and network simplification need not impose the same functional-service change on every plant (Traveset et al., 2016; Hiraiwa & Ushimaru, 2017, 2024). A single directional island syndrome can therefore obscure the response architecture that generates heterogeneous outcomes.

We isolate one layer of that architecture: the post-establishment response of plant lineages to pollinator-community reorganization. Assembly and colonization determine which lineages and partners occur; evolution can alter floral states after establishment; and post-establishment interaction change determines how established lineages experience a reorganized community. Our model addresses the third layer. It does not explain why an island acquired a particular biota, why a lineage began at a particular functional state or which historical process produced a regional interaction network.

A matching model suggests a mechanistic coordinate. Each pollinator contributes a Gaussian match function over plant functional state; the fixed-budget mean of those functions defines a community interaction kernel. Partner turnover deforms that kernel, plant starting state supplies an input coordinate, and the realized community trajectory determines both the endpoint kernel and, under weak trait adjustment, the state at which it is evaluated. Local filtering subsequently restricts and reallocates realized interaction support. Autonomous reproduction operates further downstream. This architecture distinguishes perturbation regime, branch identity and response propagation instead of placing all context dependence into one undifferentiated modifier.

The paper follows five questions. **Possibility:** can the same broad interaction reorganization generate opposite biological responses? **Mechanism:** what controls response sign and branch identity? **Reality:** does empirical island ecology require a response vocabulary richer than one syndrome? **Identifiability:** do existing studies jointly measure the state, community, local context and comparable plant outcome required to distinguish those mechanisms? **Resolution:** what becomes distinguishable when the analysis moves from global breadth to one data-rich island series?

We address possibility and mechanism with a frozen synthetic plant–pollinator model. Starting positions share matched mainland-like and island-like pollinator trajectories within each realization. A fixed joint parameter design tests whether mixed geometry persists and diagnoses transitions among all-positive, mixed and all-negative regimes. An exact response-matrix decomposition separates starting-position, community-realization and non-additive components. Local filtering and downstream assurance are varied in separate frozen envelopes so that branch reallocation is not conflated with reproductive magnitude attenuation.

We then confront the response vocabulary with a source-audited comparative universe. Its purpose is first to test whether real island responses actually require branching, propagation, buffering, axis decoupling and retained falsification as distinct states. Its second purpose is to ask what source-native information would be needed to distinguish the mechanisms implied by the synthetic architecture. We do not project systems into synthetic regimes from known outcomes, treat registry entries as exchangeable archipelagos or reconstruct stopped predictors post hoc.

That audit motivates, rather than competes with, the Izu focal analysis. Izu was not selected as an outcome-independent winner from a global ranking. It is the island series in which source floral state, source and island pollinator composition, numeric pollinator traits, interaction structure, raw realized matching and null-corrected matching can be connected at higher resolution. The contrast between raw and corrected matching attacks a specific mechanistic distinction: background community-composition structure versus additional within-community non-random partner sorting. Chapter 2 ends at this distinction and at the measurements still required to connect matching to reproduction; Chapter 3 is the next measurement stage, not causal validation of the present model.

# Materials and Methods

## Inference architecture and claim boundary

The paper uses one synthetic mechanism layer and two empirical layers with deliberately different inferential roles.

1. **Synthetic primary analysis.** All response thresholds, parameter-regime diagnostics and decomposition results are generated by a declared synthetic model. No empirical island outcome was used to fit the reported response thresholds or to select seeds after inspecting results.
2. **World confrontation and identifiability audit.** External island research entries test whether a one-direction vocabulary is empirically adequate and whether the full state–community–context–outcome contract needed for formal comparison is available. They are not treated as a meta-analysis, prevalence sample or validation coverage of the synthetic model.
3. **Focal Izu mechanistic-resolution zoom.** A source-locked secondary analysis uses published Izu plant–pollinator data to separate source-state/community-composition structure in raw matching from additional within-community sorting in null-corrected matching. This analysis is not used to calibrate synthetic thresholds and Izu is not an outcome-independent global ranking winner.

The synthetic plant coordinate is standardized to [0,1] and is not identified with a named empirical floral trait. Its sign transitions must not be interpreted as calibrated corolla-length, colour or nectar-guide thresholds.

## Synthetic pollinator environments and matching

The baseline mainland-like scenario contained nine pollinator types, partner arrival probability 0.28, partner loss probability 0.015, trait dispersion 0.22, generalist fraction 0.35 and replacement fraction 0.05. The island-like scenario contained four pollinator types, partner arrival probability 0.12, partner loss probability 0.055, trait dispersion 0.16, generalist fraction 0.58 and replacement fraction 0.22. Generalist breadth was 0.42 and specialist breadth 0.16. Replacement partners received a multiplicative effectiveness penalty of 0.82.

For plant position x and pollinator position p, matching was

`match = exp(-(|x-p| / breadth)^2)`.

Total pollinator richness did not automatically create greater total visitation. Service was computed from the mean extant-partner match using

`service = 1 - exp(-saturation * mean_match)`.

The exact model specification, reproductive equations and parameter bounds are frozen in the accompanying Supplementary Information and machine-readable design files.

## Community interaction kernel and response coordinate

For environment `E`, plant state `x` and extant pollinator `j`, we wrote the implemented match contribution as

`k_Ej(x) = a_Ej exp(-((x - p_Ej) / b_Ej)^2)`,

where `p_Ej` and `b_Ej` are pollinator position and breadth and `a_Ej` is the replacement penalty or 1. Under the fixed visit budget, the community interaction kernel is `K_E(x) = mean_j k_Ej(x)`, with zero assigned to an empty pollinator community, and service is `S_E(x) = 1 - exp(-saturation × K_E(x))`. Because this saturation map is strictly increasing, a fixed-state service contrast and fixed-state kernel contrast have identical signs.

The endpoint model permits weak environment-specific trait adjustment. Let `Phi_E,T(x0; omega_E)` be the final plant state from starting position `x0` under pollinator trajectory `omega_E`. The exact per-realization coordinate is therefore

`G_omega(x0) = K_I,T(Phi_I,T(x0; omega_I)) - K_M,T(Phi_M,T(x0; omega_M))`.

We verified in a deterministic code-identity audit that endpoint service is exactly the saturation of this composite kernel and that `sign(delta service) = sign(G_omega)` per realization. The unchanged-state shortcut `K_I(x0) - K_M(x0)` is not exact when trait adjustment produces different final states, and nonlinear saturation prevents replacement of the mean service contrast by a difference of mean kernels. This analytic representation adds no simulation evidence or empirical calibration.

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

## World confrontation and external identifiability audit

The project maintains a source-audited comparative universe larger than the strict manuscript challenge set. The strict set contains 13 external state challenges, while 12 additional analytical and model-development targets are retained separately; these 25 research entries are not interpreted as independent archipelagos. We first retained the qualitative state vocabulary already present in the registry—same-direction propagation, branching, buffering, axis decoupling and retained falsification—as a reality-necessity test. We did not use those known states to infer missing predictors or assign systems to synthetic regimes.

After freezing the synthetic model, we conducted a separate source-readiness audit for a stronger external-prediction claim. Four model-derived coordinates were declared without refitting: turnover imbalance `T = z_loss - z_arrival`; standardized source functional displacement `D0`; standardized realized-community shift `C`; and local filtering `F = 1 - realized opportunity / feasible opportunity`. Assurance remained a downstream modifier rather than a sign-regime axis. We defined five alternatives: a universal-direction baseline (`H0`), starting-state-only (`H1`), turnover-only (`H2`), source-state-by-community matching (`H3`) and `H3` plus local filtering (`H4`). Formal comparison required at least four geographically de-duplicated systems with one comparable plant-response target, matched outcome-independent inputs sufficient for `H0`–`H3`, and no imputation from observed response state. If this gate failed, model comparison, leave-one-system/archipelago-out evaluation and permutation were declared not evaluable rather than run on a repaired data set.

## Izu mechanistic-resolution zoom

We recovered and byte-locked the supplementary source associated with Hiraiwa & Ushimaru (2017). Against the current 2024 named-pollinator archive, 202 of 209 taxa (96.65%) received a safe numeric join using exact or whitespace-normalized names; no fuzzy, family, guild, body-size or midpoint substitution was allowed. The 2017 and 2024 sources agreed on all 532 matching taxon × site presences among the safely joined taxa.

Before fitting the target response, the source regime was frozen as the study-defined three continental sites pooled by source-recorded visits. The resulting continental pollinator functional centre was 7.32665 mm. For plant species occurring in the continental source and at least one Izu island, initial signed position was defined as

`initial position = continental source tube mean - continental pollinator centre`.

Thirty plant species met the eligibility rule. For each island, the broad pollinator-centre shift relative to the continental source was used to form the preregistered geometric projection

`predicted matching change = abs(initial position) - abs(initial position - centre shift)`.

The primary raw target was the published species-level realized trait-matching response, analysed across 83 plant × island-site rows with island fixed effects and plant-cluster-robust inference. Reproductive outcomes were not used to choose the mapping.

We then applied four structural attacks without retuning the frozen projection: (1) the source paper’s null-corrected species-level matching response was used as the target; (2) initial source positions were permuted among plant identities 10,000 times while retaining island coverage and outcomes; (3) all 5! = 120 assignments of the observed island centre shifts to island labels were enumerated; and (4) a source-position-only model was compared with the full centre-shift projection on the same rows. These attacks separate raw realized geometry from claims about uniquely identified island centres or non-random partner sorting beyond background community composition.

# Results

## Possibility: the same reorganization generated opposite responses

Across 96 matched community realizations, 41 contained both positive and negative island-minus-mainland service responses across the starting-position grid. Forty-two were positive across the full grid and 13 negative across the full grid (Fig. 2).

The mean response geometry was mixed-sign. Mean response was positive approximately from 0.00–0.30 and 0.70–1.00 and negative from 0.35–0.65, with sign transitions between 0.30–0.35 and 0.65–0.70. These locations describe the declared synthetic coordinate only.

## Mechanism: turnover moved the system among response regimes

Of the 48 fixed joint parameter points, 16 produced mixed mean geometry, 22 all-positive mean geometry and 10 all-negative mean geometry. The model therefore contains a genuine transition surface rather than forcing branching under every parameter combination.

The ten-parameter additive diagnostic explained R² = 0.611 of variation in the negative fraction of the starting-position grid, with leave-one-point-out RMSE = 0.329. Partner-loss multiplier had the largest positive full-range coefficient (+0.634) and partner-arrival multiplier the largest negative coefficient (−0.626); both retained their signs in all 48 leave-one-point-out fits. These quantities diagnose the declared surface and are not field-calibrated causal effects.

## Mechanism: realized community dominated branch identity

In the baseline 21 × 96 response matrix, starting position accounted for 2.18% of total sum of squares, community realization for 80.17% and the non-additive remainder for 17.64% (Fig. 3). Thus starting state organizes the mean geometry but does not determine individual outcomes by itself. The realized community trajectory is the dominant source of cell-level variation within this design.

## Mechanism: local filtering reallocated branches asymmetrically

Across the fixed threshold design, 737 lineage contrasts changed sign at least once as filtering strength increased. Sign switching was directional: positive baselines crossed to non-positive more readily than negative baselines crossed to non-negative at every non-zero tested strength. The median first sign-change strength was 0.40 across all contrasts that switched. These values are synthetic design descriptors rather than ecological thresholds.

## Mechanism: downstream assurance attenuated magnitude without rescuing sign

Among 580 lineages with both negative baseline service and negative reproduction contrasts, no assurance multiplier from 0.5× through 4× produced sign rescue. Upstream effective service was identical across assurance multipliers. Nevertheless, most eligible declines improved in magnitude, with magnitude improvement remaining above 92% even at the largest tested multiplier. In this implementation, autonomous assurance is therefore a downstream magnitude attenuator, not a general sign-changing rescue mechanism.

## Reality: the comparative universe required more than one response state

The source-audited comparative universe retained examples of same-direction propagation, branching, buffering, reproductive-axis decoupling and explicit falsification. These states arose from heterogeneous outcomes and study designs and were not treated as exchangeable draws. Their supported role is qualitative but consequential: a universal one-direction syndrome would discard response structures already present in real island research, whereas the conditional architecture can represent their distinction without claiming that one synthetic mechanism generated every case.

## Identifiability: no entry supplied the full comparative contract

None of the 25 audited entries passed the frozen plant-response contract. Twelve were retained as retrospective explanatory tests, eight as reality boundaries and five as source-gated or unusable for this question (Fig. 4A). Direct or source-derived source state was available in 10 entries, community functional shift in 18, local filtering in 20 and a response quantity in 21, but those fields did not coincide on a comparable response family, matched transition unit and outcome-independent mapping. The complete-contract count was therefore zero.

Because no response family met the frozen minimum of four geographically de-duplicated, prospective-like entries, `H0`–`H4` comparison, leave-one-system/archipelago-out evaluation and permutation were not evaluable. No classifier was fitted and no missing predictor was reconstructed from outcome state. The result is a data-readiness and identifiability stop: it identifies a joint-measurement bottleneck in the current research inventory but does not estimate literature-wide prevalence or failed predictive accuracy.

## Resolution: Izu raw matching localized source-state and composition structure

The frozen Izu projection produced a positive association with realized raw trait matching across 83 plant × island-site rows and 30 plant clusters: slope = 0.5669, cluster-robust SE = 0.1316 and 95% CI = 0.2977–0.8361 (Fig. 4B). Pearson r was 0.570, Spearman rho 0.527 and sign concordance 63/83 = 75.9%. All five leave-one-island slopes were positive.

Correct plant source-state identity mattered. In 10,000 fixed-seed permutations of initial source positions among plant identities, no null slope reached the observed raw slope; the empirical one-sided probability was 1/10001.

However, the raw association did not uniquely identify exact island-specific pollinator-centre magnitudes. Across all 120 assignments of the five observed centre shifts to island labels, 13 assignments produced slopes at least as large as the real assignment. Moreover, a source-position-only model with island fixed effects described raw response at least as well as the full centre-shift geometry (R² = 0.409, AIC = 362.1 versus R² = 0.365, AIC = 368.1). The strongest raw information therefore resides in source floral state plus broad community composition rather than precise identification of five island centre magnitudes.

## Resolution: Izu null-corrected matching did not support beyond-composition sorting

Using the exact same frozen predictor and rows, the source paper’s background-community-corrected matching response was not associated with the signed-position projection: slope = 0.0333, cluster-robust SE = 0.1473, 95% CI = −0.2680–0.3346, Pearson r = 0.061, Spearman rho = 0.099 and sign concordance 42/83 = 50.6%. In the plant-position permutation, 3918 of 10,000 null slopes were at least as large as the observed corrected slope.

Thus the Izu reanalysis supports a source-state/community-composition structure in realized raw matching, but not non-random partner sorting beyond the source paper’s background-community null. This distinction is central to the empirical interpretation.

# Discussion

## Possibility becomes a response coordinate, not a universal syndrome

The synthetic analysis rejects a one-direction description of post-establishment response within the declared model. The same broad pollinator reorganization can yield positive, mixed or negative response regimes. Mixed mean geometry persists across part of the joint parameter design but disappears under other combinations, providing a meaningful failure boundary rather than a branching pattern guaranteed by construction. The interaction-kernel derivation clarifies what is common across those outcomes: response sign records which of two trajectory-conditioned community kernels provides greater endpoint service at a given starting position.

This result changes the level at which an “island syndrome” should be interpreted. A recurrent aggregate pattern can coexist with heterogeneous lineage-level consequences. Partner turnover defines the broad response regime; starting functional state organizes the average mapping of plants onto that regime; realized community trajectory strongly determines cell-level outcomes; and local filtering further reallocates branch identity. A universal island effect is therefore not required even when the broad direction of community simplification is shared.

## The proximal WHY is a hierarchy of regime, position and realization

The additional diagnostics clarify what the model does and does not explain. Starting position alone accounts for little cell-level variance, so the result cannot be reduced to “plants at one end benefit and plants at the other decline.” Instead, partner loss and arrival reshape the response surface, starting state places a plant on that surface, and the realized community determines much of the actual outcome. Non-additivity remains substantial. The proximal explanation is therefore hierarchical: **regime × starting state × realized community**, followed by local filtering.

The local-filtering result adds a second asymmetry. Filtering is not simply a buffer that occasionally rescues negative lineages. It changes branch identity in both directions but more readily converts positive baselines to non-positive states over the tested range. Downstream autonomous assurance plays a different role: it commonly reduces the magnitude of negative reproductive consequences yet never reverses their sign in the tested 0.5×–4× envelope. Treating these mechanisms separately prevents a generic “context matters” explanation from obscuring where sign changes actually enter the response chain.

## World confrontation establishes necessity, not validation coverage

The broader comparative programme is useful precisely because real island systems do not collapse into one outcome vocabulary. Source-audited cases include branching, same-direction propagation, buffering, reproductive-axis decoupling and retained falsification. These cases establish the empirical necessity of a richer response architecture and discipline model interpretation: a synthetic mechanism that could only produce one direction would be poorly matched to the diversity of observed island responses.

But this comparative universe is not a random sample of archipelagos, and different systems expose different outcomes, scales and uncertainty structures. We therefore do not interpret the fraction of systems assigned to a response state as ecological prevalence, and we do not claim that the synthetic model explains all admitted systems. Reality necessity is weaker than validation but stronger than a decorative case list: it rejects an impoverished one-state vocabulary while preserving counterexamples and failure states.

## The identifiability bottleneck is joint measurement, not missing outcomes alone

None of the 25 audited entries passed the paper's full plant-response contract. Twelve were retained as retrospective explanatory tests, eight as reality boundaries and five as source-gated or unusable for this question. Earlier pre-target chronology exists for four narrower tests, but Dominica tested a publication-aware signed-position/selection-gradient direction and Menorca, Cabrera and Giannutri tested network architecture or local realization without a linked plant-response target.

Marginal predictor availability was not the limiting quantity by itself: direct or source-derived source state was available in 10 entries, community functional shift in 18, local filtering in 20 and a response quantity in 21 (Fig. 4; Fig. S3). Those fields did not coincide on a common response family, matched transition unit and outcome-independent mapping. The number of geographically de-duplicated, prospective-like systems with complete `H0`–`H3` inputs was therefore zero, below the frozen minimum of four. We did not fit `H0`–`H4`, compute cross-system accuracy or run leave-one-system/archipelago-out and permutation tests. Current island-pollination research is rich in outcomes within this inventory but sparse in jointly measured state–community–outcome contracts required to identify conditional response geometry. This is a bounded data-readiness result, not a field-wide census or failed fitted model.

## Izu increases mechanistic resolution and localizes the present signal

The Izu Islands provide the deepest current empirical bridge because the same archipelago contains published floral traits, pollinator functional traits and contemporary interaction structure. This is a transparent data-depth rationale, not the result of an outcome-independent global ranking: candidate eligibility, scoring criteria, weights and missingness rules were not frozen before Izu became the focal programme. The frozen signed-position analysis initially appears to mirror the synthetic logic: correct plant source identity strongly organizes realized raw trait-matching change, and the result is distributed across five islands rather than produced by one island alone.

The structural audit is more informative than the raw positive slope by itself. Exact island-specific pollinator-centre magnitudes are not uniquely identified, and source starting position alone explains at least as much raw variation as the full geometric projection. Most importantly, the association disappears for the source paper’s null-corrected matching metric. Therefore the current empirical result does not identify non-random partner choice or a pollinator-centre selection mechanism beyond background community composition.

This is not a failed validation because Izu was not admitted as a validation of the synthetic threshold surface. Increasing resolution makes two mechanisms distinguishable and localizes the present signal: **source state and background community composition structure raw matching, while additional beyond-composition interaction sorting remains unsupported**. The Izu result is therefore a mechanistic-resolution result, not external validation of the synthetic thresholds.

## Chapter 2 hands a measurement contract to Chapter 3

At the dissertation scale, Chapter 1 asks when and where isolation-associated response vectors differ. Chapter 2 asks how a broad interaction reorganization can generate different outcomes, confronts that response space with empirical diversity, identifies why existing comparisons cannot distinguish its mechanisms and shows in Izu how composition-level and beyond-composition matching signals can be separated.

The remaining contract is prospective and plant linked: source state, community assembly, realized partner sorting, effectiveness and reproductive propagation must be measured on comparable units. Chapter 3 advances to higher-resolution focal measurement in the same island series. Its phenotype and any future effectiveness or dependency observations are not used here as model validation, Bombus-causation proof, pollinator-selection proof or external prediction success.

## Limits and decisive next measurement

Several boundaries remain essential. The synthetic thresholds are not empirical trait thresholds. The joint-design coefficients are not field causal effects. The external-system registry is not a prevalence sample or a held-out prediction set. The source audit does not support placing systems into synthetic regimes from their observed outcomes. The Izu secondary analysis lacks plant-specific partner-weighted functional centres because the required legacy interaction-weight workbook has not been recovered through the current public route. The pollinator trait table is also not a complete site-exact numeric matrix for every taxon.

Most importantly, the current Izu analysis stops at realized matching. It does not show that the source-state/community geometry propagates through pollinator effectiveness into reproduction. The decisive prospective test is therefore plant-linked and preregistrable:

`visitor identity + exact/new proboscis + plant-specific visitor weights -> frozen plant-specific signed position -> single-visit pollen deposition -> direct reproductive dependency / mature seed outcome`.

A successful test would connect source-state/community geometry to reproductive function. A null result would retain the assembly/community-composition interpretation while rejecting a stronger functional-propagation claim.

# Conclusion

Community reorganization can define a response regime without determining one biological outcome. In the synthetic model, a trajectory-conditioned interaction-kernel difference represents response sign; turnover deforms that geometry, starting state locates the lineage, realized community and non-additivity condition branch identity, local filtering reallocates branches, and assurance acts downstream. World confrontation shows why a one-syndrome vocabulary is insufficient, but the frozen source audit also shows that existing comparisons do not jointly identify the required state–community–context–outcome contract. Increasing resolution in Izu localizes the current raw-matching signal to source state plus background community composition and rejects a stronger claim of additional null-corrected sorting. The resulting contribution is a mechanistic coordinate system and measurement agenda for conditional post-establishment response—not a calibrated island predictor, a natural-frequency estimate or an ultimate historical explanation.

## Main figure captions

**Figure 1. Breadth-to-depth mechanistic-resolution funnel.** The synthetic model defines ecological possibilities and an interaction-kernel coordinate; comparative research entries establish response diversity but expose a zero-contract identifiability bottleneck; the Izu zoom separates source-state/community-composition structure from unsupported null-corrected sorting; the remaining effectiveness-to-reproduction contract is handed to Chapter 3 without validation claims.

**Figure 2. Conditional response geometry.** Mean island-minus-mainland functional service across the 21-point starting-position grid under 96 matched community realizations. Realization counts describe the frozen synthetic design and are not frequencies in nature.

**Figure 3. Proximal-WHY hierarchy.** Fixed-surface parameter associations, starting-position/community-realization decomposition, direction-specific local-filtering transitions at synthetic strength 0.40, and magnitude improvement versus sign rescue across the assurance envelope. Driver coefficients are associations within the declared design, and filtering values are not empirical thresholds.

**Figure 4. From global breadth to Izu mechanistic resolution.** (A) Admission classes among 25 source-audited research entries and the zero full-contract result. (B) The same frozen Izu projection is associated with raw realized matching but not null-corrected matching; exact island-centre magnitudes remain non-unique. Panel A is an identifiability audit, not predictive performance; panel B does not establish beyond-composition sorting or causal floral evolution.

## References

Use the source-audited active reference ledger in `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md`. Hiraiwa & Ushimaru (2017, 2024) are the empirical sources for the Izu triangulation. External-system references remain in the comparative-grounding supplement and are not presented as validation coverage.
