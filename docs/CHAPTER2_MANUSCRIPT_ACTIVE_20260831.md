# Response geometry under community reorganization

**Status:** active Chapter 2 scientific manuscript — relational-robustness revision; submission metadata still fail-closed
**Updated:** 2026-08-31
**Inference architecture:** model possibilities → world confrontation → identifiability bottleneck → focal Izu mechanistic-resolution zoom
**Controlling state:** `docs/CHAPTER2_CANONICAL_STORY_20260827.md`, `docs/CHAPTER2_RELATIONAL_ROBUSTNESS_CORRECTION_20260831.md`, `data/results/chapter2_scientific_gate_decision_frozen_20260827.json`, `data/results/chapter2_relational_robustness_audit_frozen_20260831.json`

## Working title

**Response geometry under community reorganization: from ecological possibility to mechanistic resolution in island plant–pollinator systems**

## Abstract

The same environmental change can produce opposite biological responses, yet mean effects do not identify the state–community relationship that determines response direction. We ask whether pollinator-community reorganization is better represented as a conditional response geometry and what resolution is required to distinguish its mechanisms.

We exposed the interaction kernel in a frozen matching model, mapped island-minus-mainland service across matched starting positions, diagnosed regime transitions, decomposed starting-state and community contributions, and separated local filtering from downstream assurance. We then confronted this vocabulary with a source-audited 25-entry island literature inventory and increased mechanistic resolution in Izu using source floral state, pollinator composition, raw matching and null-corrected matching.

Across 96 matched community realizations, 41 contained both positive and negative responses; mixed geometry also persisted when mainland-like and island-like initial pollinator richness was equalized (53/96). Partner loss and arrival were the strongest sign-stable regime associations. Across prespecified seed and time-horizon sensitivities, realized community remained the largest additive component, while starting state alone remained weak and state-by-community non-additivity consequential; mixed geometry persisted even with trait adjustment set to zero. Local filtering reallocated branches asymmetrically, whereas assurance produced no sign rescue among 580 eligible declines. Existing studies were outcome-rich but process-poor: responses were directly measured in 21/25 entries, but partner arrival/replacement in only 2/25, and no entry supplied the full outcome-independent contract. In Izu, the frozen projection tracked raw matching but not null-corrected matching.

Response direction is therefore relational rather than intrinsic: organismal state must be evaluated against the community realized after reorganization. World confrontation identifies the measurements needed to distinguish this geometry, while the Izu zoom localizes the current matching signal to source state plus background community composition rather than additional non-random sorting.

**Keywords:** community reorganization; response geometry; plant–pollinator interactions; functional matching; source state; realized community; identifiability; Izu Islands

# Introduction

Environmental change is often summarized by one mean directional effect. That summary becomes insufficient when the same perturbation produces positive and negative responses among biological starting states or community realizations. The central ecological problem is then not only how large the average response is, but what coordinate system represents alternative response branches and what information identifies the branch realized by a particular lineage.

Islands provide a stringent setting for this problem. Colonization, ecological simplification and interaction reorganization can alter plant reproduction through partner identity, functional compatibility and local realization. Comparative studies document recurrent island-associated changes in breeding systems, pollination strategies and floral traits (Grossenbacher et al., 2017; Traveset & Navarro, 2018; Zell et al., 2025), yet Baker's law concerns assembly during colonization rather than a uniform response among established populations (Pannell et al., 2015), flower-size responses vary with source size and pollination context (Hetherington-Rauth & Johnson, 2020; Ciarle et al., 2025), and network simplification need not impose the same functional-service change on every plant (Traveset et al., 2016; Hiraiwa & Ushimaru, 2017, 2024). A single directional island syndrome can therefore obscure the response architecture that generates heterogeneous outcomes.

We isolate one layer of that architecture: post-establishment response of plant lineages to pollinator-community reorganization. Assembly and colonization determine which lineages and partners occur; evolution can alter floral states after establishment; post-establishment interaction change determines how established lineages experience a reorganized community. Our model addresses the third layer. It does not explain why an island acquired a particular biota, why a lineage began at a particular functional state or which historical process produced a regional interaction network.

A matching model suggests a mechanistic coordinate. Each pollinator contributes a Gaussian match function over plant functional state; the fixed-budget mean of those functions defines a community interaction kernel. Partner turnover deforms that kernel, plant starting state supplies the input coordinate, and the realized community trajectory determines both the endpoint kernel and, when trait adjustment occurs, the state at which it is evaluated. Local filtering subsequently restricts and reallocates realized interaction support. Autonomous reproduction operates further downstream. This architecture distinguishes perturbation regime, relational branch identity and response propagation instead of placing all context dependence into one undifferentiated modifier.

The paper follows five linked questions. **Possibility:** can the same broad interaction reorganization generate opposite biological responses? **Mechanism:** what controls response sign and branch identity? **Reality:** does empirical island ecology require a response vocabulary richer than one syndrome? **Identifiability:** do existing studies jointly measure the state, community, local context and comparable plant outcome required to distinguish those mechanisms? **Resolution:** what becomes distinguishable when analysis moves from global breadth to one data-rich island series?

We address possibility and mechanism with a frozen synthetic plant–pollinator model. Starting positions share matched mainland-like and island-like pollinator trajectories within each realization. A fixed joint parameter design tests whether mixed geometry persists and diagnoses transitions among all-positive, mixed and all-negative regimes. An exact response-matrix decomposition separates additive starting-position and community-realization components from state-by-community non-additivity. Local filtering and downstream assurance are varied in separate frozen envelopes. A later, prespecified structural audit varies seed ensemble, model horizon, trait adjustment and initial pollinator richness without replacing the historical baseline.

We then confront the response vocabulary with a source-audited comparative universe. Its purpose is first to ask whether real island responses require branching, propagation, buffering, axis decoupling and retained falsification as distinct states. Its second purpose is to identify which source-native measurements are missing when those mechanisms cannot be distinguished. We do not project systems into synthetic regimes from known outcomes, treat research entries as exchangeable archipelagos or reconstruct stopped predictors post hoc.

That audit motivates, rather than competes with, the Izu focal analysis. Izu was not selected as an outcome-independent winner from a global ranking. It is the island series in which source floral state, source and island pollinator composition, numeric pollinator traits, interaction structure, raw realized matching and null-corrected matching can be connected at higher resolution. The contrast between raw and corrected matching attacks a specific mechanistic distinction: background community-composition structure versus additional within-community non-random partner sorting. Chapter 2 ends at this distinction and at the measurements still required to connect matching to reproduction; Chapter 3 is the next measurement stage, not causal validation of the present model.

# Materials and Methods

## Inference architecture and claim boundary

The paper uses one synthetic mechanism layer and two empirical layers with deliberately different inferential roles.

1. **Synthetic primary analysis.** Response geometry, parameter-regime diagnostics and decomposition results are generated by a declared synthetic model. No empirical island outcome was used to fit response thresholds or select seeds after inspecting results.
2. **World confrontation and identifiability audit.** External island research entries test whether a one-direction vocabulary is empirically adequate and whether the joint measurements needed for formal comparison are available. They are not treated as a meta-analysis, prevalence sample or validation coverage.
3. **Focal Izu mechanistic-resolution zoom.** A source-locked secondary analysis uses published Izu plant–pollinator data to separate source-state/community-composition structure in raw matching from additional within-community sorting in null-corrected matching. Izu does not calibrate synthetic thresholds and is not an outcome-independent global ranking winner.

The synthetic plant coordinate is standardized to [0,1] and is not identified with a named empirical floral trait. Synthetic sign transitions, variance shares, realization frequencies and time horizons are design diagnostics rather than calibrated ecological thresholds or population parameters.

## Synthetic pollinator environments and matching

The baseline mainland-like scenario contained nine pollinator types, partner arrival probability 0.28, partner loss probability 0.015, trait dispersion 0.22, generalist fraction 0.35 and replacement fraction 0.05. The island-like scenario contained four pollinator types, partner arrival probability 0.12, partner loss probability 0.055, trait dispersion 0.16, generalist fraction 0.58 and replacement fraction 0.22. Generalist breadth was 0.42 and specialist breadth 0.16. Replacement partners received a multiplicative effectiveness penalty of 0.82.

For plant position `x` and pollinator position `p`, matching was

`match = exp(-(|x-p| / breadth)^2)`.

Total pollinator richness did not automatically create greater total visitation. Service was computed from mean extant-partner match:

`service = 1 - exp(-saturation * mean_match)`.

The exact reproductive equations and parameter bounds are supplied in Supplementary Information and machine-readable design files.

## Community interaction kernel and response coordinate

For environment `E`, plant state `x` and extant pollinator `j`, the implemented match contribution is

`k_Ej(x) = a_Ej exp(-((x - p_Ej) / b_Ej)^2)`,

where `p_Ej` and `b_Ej` are pollinator position and breadth and `a_Ej` is the replacement penalty or 1. Under the fixed visit budget, the community interaction kernel is `K_E(x) = mean_j k_Ej(x)`, with zero assigned to an empty pollinator community, and service is `S_E(x) = 1 - exp(-saturation × K_E(x))`. Because the saturation map is strictly increasing, fixed-state service and kernel contrasts have identical signs.

The endpoint model permits environment-specific trait adjustment. Let `Phi_E,T(x0; omega_E)` be the final plant state from starting position `x0` under pollinator trajectory `omega_E`. The exact per-realization coordinate is

`G_omega(x0) = K_I,T(Phi_I,T(x0; omega_I)) - K_M,T(Phi_M,T(x0; omega_M))`.

A deterministic code-identity audit verifies that endpoint service is exactly the saturation of this composite kernel and that `sign(delta service) = sign(G_omega)` per realization. At zero trait adjustment, `Phi_E,T(x0)=x0`, so state remains the input coordinate through `K_I,T(x0)-K_M,T(x0)`. Trait adjustment can therefore alter how state dependence appears, but is not required to create state dependence. This analytic representation adds no empirical calibration.

## Matched response geometry

Starting positions were evaluated on a 21-point grid from 0 to 1 in increments of 0.05. Within each realization, every starting position experienced the same mainland-like pollinator trajectory and the same island-like trajectory. This common-random-number design separates starting-position effects from drawing a different pollinator history for every starting state.

We generated 96 matched community realizations. The primary response was final island-minus-mainland functional service. A realization was classified as mixed-sign when at least one starting position produced a positive response and at least one produced a negative response. Mean response was also calculated at every starting position across realizations.

## Joint parameter robustness and regime drivers

A fixed 48-point Latin-hypercube design simultaneously varied ten declared perturbation and matching dimensions: trait dispersion, generalist fraction, replacement fraction, partner loss, partner arrival, saturation, trait adjustment, generalist breadth, specialist breadth and replacement penalty. Each design point used 24 matched community realizations under a common seed ensemble.

Design points were classified as mixed, all-positive or all-negative according to mean response signs across the 21 starting positions. To diagnose rather than retune the fixed surface, the fraction of starting positions with negative mean response was regressed on all ten centered and range-scaled parameters in one additive ordinary-least-squares model. No model selection or post-hoc interaction search was used. We report full-range coefficients, leave-one-point-out coefficient sign stability, in-sample R² and leave-one-point-out RMSE.

## Starting-state × community-realization decomposition

For the baseline 21 × 96 response matrix, total sum of squares was partitioned exactly into a starting-position additive component, a community-realization additive component and a non-additive remainder. Each pollinator-community trajectory is generated once per realization and shared across all 21 starting positions; `endpoint_on_trajectory` makes no additional random draw. Conditional on that trajectory, every matrix cell is deterministic. The residual sum of squares is therefore the exact starting-position × community-realization non-additive component of the fixed matrix, not a mixture with within-cell simulation noise. Because the 96 trajectories remain a finite synthetic ensemble, the numerical shares are ensemble-specific design diagnostics rather than population variance parameters. We also recorded cell-level sign disagreement between observed response and the fitted additive value.

## Prespecified relational-robustness audit

After an independent code audit identified model horizon and ensemble dependence as unreported sensitivities, we froze an additional structural audit before execution. The historical baseline (`seed=20260826`, `steps=120`, trait adjustment 0.03) was retained and could not be replaced after inspection. We evaluated `steps={30,60,120,240}`, trait adjustment `{0,0.01,0.03,0.06}`, and the historical seed plus five prespecified sensitivity seeds. We separately equalized initial pollinator richness at 9 mainland-like versus 9 island-like types while retaining all other baseline differences in loss, arrival, trait dispersion, generalist fraction and replacement fraction. The equal-richness sensitivity therefore tests only whether richness reduction is necessary for mixed geometry.

The audit was designed to test structural statements rather than stabilize one percentage: whether mixed geometry remained possible, whether community realization remained the largest additive component, whether starting position alone became dominant, and whether state dependence persisted when trait adjustment was zero.

## Local filtering and autonomous assurance

Local context was represented as availability and interaction filtering, not added beneficial support. Filtering strengths were 0, 0.10, 0.25, 0.40, 0.50, 0.60 and 0.75 under common seed ensembles. The fixed threshold design used saturation 1, 2 and 3; 12 replicates per saturation; four local contexts; 24 lineages; and 120 steps. For every lineage contrast, we recorded the first filtering strength at which the reproduction-response sign differed from the zero-filtering baseline and retained the full baseline-sign → current-sign transition table.

The autonomous-assurance route was varied independently with multipliers 0, 0.5, 1, 1.5, 2, 3 and 4. A lineage was eligible for sign rescue when both island-minus-mainland effective service and reproduction were negative at multiplier 0. Upstream effective service was required to remain invariant across assurance multipliers before interpreting reproductive rescue.

## World confrontation and external identifiability audit

The source-audited comparative universe contains 13 strict external state challenges and 12 additional analytical or model-development entries; these 25 research entries are not independent archipelagos. We retained the qualitative state vocabulary already present in the registry—same-direction propagation, branching, buffering, axis decoupling and retained falsification—as a reality-necessity test. Known outcomes were not used to infer missing predictors or assign systems to synthetic regimes.

For a stronger external-prediction claim, four model-derived coordinates were frozen without refitting: turnover imbalance `T=z_loss-z_arrival`, standardized source functional displacement `D0`, standardized realized-community shift `C`, and local filtering `F=1-realized opportunity/feasible opportunity`. Assurance remained a downstream modifier. Five alternatives were frozen: universal direction (`H0`), starting-state-only (`H1`), turnover-only (`H2`), source-state-by-community matching (`H3`) and `H3` plus local filtering (`H4`). Formal comparison required at least four geographically de-duplicated systems with one comparable plant-response target, matched outcome-independent inputs sufficient for `H0`–`H3`, and no imputation from observed response state.

We also summarized source-native **direct measurements** for each required process dimension. This separates an outcome-rich literature from a process-rich literature and avoids treating proxy availability or research-entry counts as independent replication.

## Izu mechanistic-resolution zoom

We recovered and byte-locked the supplementary source associated with Hiraiwa & Ushimaru (2017). Against the current 2024 named-pollinator archive, 202 of 209 taxa (96.65%) received a safe numeric join using exact or whitespace-normalized names; no fuzzy, family, guild, body-size or midpoint substitution was allowed. The 2017 and 2024 sources agreed on all 532 matching taxon × site presences among safely joined taxa.

Before fitting the target response, the source regime was frozen as the study-defined three continental sites pooled by source-recorded visits. The continental pollinator functional centre was 7.32665 mm. For plant species occurring in the continental source and at least one Izu island,

`initial position = continental source tube mean - continental pollinator centre`.

Thirty species met the eligibility rule. For each island,

`predicted matching change = abs(initial position) - abs(initial position - centre shift)`.

The primary raw target was the published species-level realized trait-matching response across 83 plant × island-site rows with island fixed effects and plant-cluster-robust inference. Reproductive outcomes were not used to choose the mapping.

Four structural attacks were then applied without retuning: the source paper's null-corrected matching response as target; 10,000 permutations of source positions among plant identities; all 120 assignments of observed island centre shifts to island labels; and a source-position-only comparator. A prespecified Oshima-source bridge was retained as an independent source-regime sensitivity rather than substituted after seeing the continental-source result.

# Results

## Possibility: the same reorganization generated opposite responses

Across 96 matched community realizations, 41 contained both positive and negative island-minus-mainland service responses across the starting-position grid; 42 were positive across the full grid and 13 negative across the full grid (Fig. 2). Mean response was positive approximately at 0.00–0.30 and 0.70–1.00 and negative at 0.35–0.65 on the declared synthetic coordinate.

Mixed response geometry was not a mechanical consequence of reduced initial pollinator richness. When island-like initial pollinator richness was increased from four to nine, matching the mainland-like initial richness while all other scenario differences remained unchanged, 53/96 realizations were mixed-sign, 31 all-positive and 12 all-negative. Thus richness reduction is not necessary for mixed response geometry; the sensitivity does not remove other forms of community reorganization.

## Mechanism: turnover moved the system among response regimes

Of 48 fixed joint parameter points, 16 produced mixed mean geometry, 22 all-positive mean geometry and 10 all-negative mean geometry. The model therefore contains a transition surface rather than forcing branching under every parameter combination.

The ten-parameter additive diagnostic explained R²=0.611 of variation in the negative fraction of the starting-position grid, with leave-one-point-out RMSE=0.329. Partner loss had the largest positive full-range coefficient (+0.634) and partner arrival the largest negative coefficient (−0.626); both retained their signs in all 48 leave-one-point-out fits. These coefficients diagnose the declared synthetic surface and are not field-calibrated causal effects.

## Mechanism: response direction was relational rather than a stable state-only effect

The historically frozen baseline decomposition was 2.18% starting-position main effect, 80.17% community-realization main effect and 17.64% starting-position × community-realization non-additivity. The 17.64% remainder is exact non-additivity in the fixed response matrix, not within-cell simulation noise.

The exact percentages were ensemble dependent. Across the six prespecified seeds, the community component ranged 69.34–80.17%, the starting-position component 2.17–3.14% and non-additivity 17.64–27.91%; the historical seed produced the largest community share in this sensitivity ensemble but was retained rather than reselected. Across model horizons of 30, 60, 120 and 240 steps, the community component remained largest at every horizon, while the starting-position share ranged 0.59–4.26% and mixed-sign realizations remained present (65, 48, 41 and 43 of 96, respectively).

State dependence did not require trait adjustment. With trait adjustment fixed at zero, 64/96 realizations remained mixed-sign; the additive starting-position share fell to 0.18% while state × community non-additivity rose to 32.50%. Across adjustment values 0–0.06, community realization remained the largest component. These results show why the small additive state percentage cannot be read as absence of state dependence: response direction depends on starting state evaluated relative to the realized community, and adjustment changes how that relation is partitioned between additive and non-additive terms.

## Mechanism: local filtering reallocated branches asymmetrically

Across the fixed threshold design, 737 lineage contrasts changed sign at least once as filtering strength increased. Positive baselines crossed to non-positive more readily than negative baselines crossed to non-negative at every non-zero strength. At filtering strength 0.40, negative→non-negative transitions occurred in 15.67% of baseline negatives whereas positive→non-positive transitions occurred in 56.54% of baseline positives. The median first sign-change strength was 0.40 among contrasts that switched. These are synthetic design descriptors, not ecological thresholds.

## Mechanism: downstream assurance attenuated magnitude without rescuing sign

Among 580 lineages with both negative baseline service and negative reproduction contrasts, no assurance multiplier from 0.5× through 4× produced sign rescue. Upstream effective service was identical across assurance multipliers. Most eligible declines nevertheless improved in magnitude. Autonomous assurance is therefore a downstream magnitude attenuator in this implementation, not a general sign-changing rescue mechanism.

## Reality: the comparative universe required more than one response state

The source-audited comparative universe retained examples of same-direction propagation, branching, buffering, reproductive-axis decoupling and explicit falsification. These states arose from heterogeneous outcomes and study designs and were not treated as exchangeable draws. Their supported role is qualitative but consequential: a universal one-direction syndrome would discard response structures already present in real island research, whereas the conditional architecture can represent their distinction without claiming that one synthetic mechanism generated every case.

## Identifiability: the literature was outcome-rich but process-poor

Direct response outcomes were available in 21/25 research entries and direct community functional shifts in 13/25. Direct local filtering was available in 9/25 and richness/functional-diversity change in 8/25. In contrast, source functional state and partner loss were each directly measured in only 5/25, reproductive assurance in 5/25, and partner arrival/replacement—the process paired with loss in the strongest synthetic regime diagnostic—in only 2/25 (Fig. 4A).

These marginal measurements did not coincide on a common response family, matched transition unit and outcome-independent mapping. None of the 25 entries therefore passed the frozen full plant-response contract. Twelve remained retrospective explanatory tests, eight reality boundaries and five source-gated or unusable for this question. Because no response family met the frozen minimum of four geographically de-duplicated prospective-like entries, `H0`–`H4` comparison, leave-one-system/archipelago-out evaluation and permutation were not evaluable. No classifier was fitted and no missing predictor was reconstructed from outcome state. The bottleneck is thus joint process measurement rather than a scarcity of recorded outcomes.

## Resolution: Izu localized the raw signal to source state and composition

The frozen Izu projection was positively associated with realized raw trait matching across 83 plant × island-site rows and 30 plant clusters: slope=0.5669, cluster-robust SE=0.1316 and 95% CI=0.2977–0.8361 (Fig. 4B). Correct plant source-state identity mattered: none of 10,000 fixed-seed source-position permutations reached the observed raw slope.

The raw association did not uniquely identify exact island-specific pollinator-centre magnitudes. Across all 120 assignments of the five observed centre shifts to island labels, 13 produced slopes at least as large as the real assignment. A source-position-only model with island fixed effects also described raw response at least as well as the full centre-shift geometry (R²=0.409, AIC=362.1 versus R²=0.365, AIC=368.1). The strongest raw information therefore resides in source floral state plus broad community composition.

The prespecified Oshima-source bridge was unsupported (Appendix), showing that source regimes are not interchangeable and preventing the continental source from being treated as a generic substitute for any island source state.

## Resolution: Izu null-corrected matching did not support beyond-composition sorting

Using the same frozen predictor and rows, the source paper's background-community-corrected matching response was unsupported: slope=0.0333, cluster-robust SE=0.1473, 95% CI=−0.2680–0.3346, and 3918/10,000 null source-position permutations were at least as large as the observed corrected slope.

Thus the Izu reanalysis supports source-state/community-composition structure in realized raw matching, but not non-random partner sorting beyond the source paper's background-community null. Increasing resolution therefore localizes where the present information resides instead of being treated as validation of the synthetic transition surface.

# Discussion

## Response direction is relational rather than intrinsic

The synthetic analysis rejects a one-direction description of post-establishment response within the declared model. The same broad pollinator reorganization can yield positive, mixed or negative regimes, and mixed geometry persists when initial pollinator richness is held equal between mainland-like and island-like scenarios. The interaction-kernel derivation clarifies the common object across these outcomes: response sign records which of two trajectory-conditioned community kernels provides greater endpoint service for a given starting state.

This changes the level at which context dependence should be interpreted. Starting state is not a stable additive predictor whose percentage can be read independently of community. At zero trait adjustment, the additive state component is nearly absent while mixed geometry and substantial state × community non-additivity remain. State therefore matters relationally: it identifies where a lineage is evaluated against a particular realized community. Trait adjustment changes how this relation is expressed through additive and non-additive components; it does not create state dependence de novo.

The structural audit also changes what should be treated as robust. The historically frozen 80.17% community share is an upper-end value within the prespecified six-seed sensitivity and should not serve as a population-like headline. What survives is the ordering: community realization remained the largest component across all six seeds, all four audited horizons, all four trait-adjustment values and the equal-richness sensitivity, while starting position alone remained a weak additive component. The general inference is therefore structural rather than magnitude-specific.

## The proximal WHY separates regime, relational branch identity and downstream propagation

Partner loss and arrival organize movement among response regimes in the declared joint design. Within a regime, starting state evaluated against the realized community determines relational opportunity, with consequential state × community non-additivity. Local filtering acts later by deleting and reweighting feasible support, allowing branch identity to change asymmetrically. Autonomous assurance operates downstream again: it attenuates reproductive decline magnitude without changing upstream service and without sign rescue in the tested envelope.

Separating these levels prevents a generic “context matters” explanation. Turnover changes the geometry available; state and realized community determine where a lineage lies within it; filtering changes which local opportunities remain; assurance modifies propagation after service. The model does not identify the ultimate historical reason that any island acquired its source state or community architecture.

## World confrontation establishes necessity and a measurement agenda

The broader comparative programme matters because real island systems do not collapse into one outcome vocabulary. Source-audited cases include branching, same-direction propagation, buffering, reproductive-axis decoupling and retained falsification. These cases establish the empirical necessity of a richer response vocabulary without constituting validation coverage or a prevalence sample.

The stronger contribution of the source audit is its measurement asymmetry. Outcomes are commonly recorded, whereas the causal-side coordinates needed by the response geometry are much rarer. Most strikingly, partner arrival/replacement is directly measured in only 2/25 entries even though arrival opposes loss in the strongest synthetic regime diagnostic. Source state and loss are also sparse. The literature inventory is therefore outcome-rich but process-poor for this particular mechanistic question.

This makes the zero full-contract count interpretable rather than merely disappointing. Existing studies often document that a response occurred but do not jointly observe source state, loss, arrival/replacement, community functional change, local filtering and a comparable response on the same transition unit. Formal external prediction remains `not_evaluable`; the audit instead specifies what future comparative work must measure if conditional response geometry is to be tested rather than retrospectively narrated.

## Izu increases resolution and localizes the present signal

Izu supplies the deepest current bridge because the same archipelago contains published floral traits, pollinator functional traits and contemporary interaction structure. This is a transparent data-depth rationale, not an outcome-independent ranking. The raw signed-position result initially mirrors the relational logic: correct plant source identity organizes realized matching change across islands.

The structural attacks narrow that interpretation. Exact island-centre magnitudes are non-unique, a source-position-only model is at least as descriptive as the full centre-shift projection, the Oshima bridge is unsupported, and the association disappears for null-corrected matching. Thus the present empirical information lies primarily in source state plus broad community composition rather than identified within-community partner sorting.

This is mechanistic resolution rather than failed validation. The global confrontation shows that response diversity exists and identifies a process-measurement bottleneck; Izu then separates two processes that broad comparison cannot. The remaining question—whether composition and matching propagate through visitor effectiveness into reproduction—belongs to a prospective plant-linked test rather than retrospective strengthening of the current model.

## Chapter 2 hands a measurement contract to Chapter 3

At the dissertation scale, Chapter 1 asks when and where isolation-associated response vectors differ. Chapter 2 asks how a broad interaction reorganization can generate different outcomes, confronts that response geometry with empirical diversity, identifies why existing comparisons cannot distinguish its mechanisms and shows in Izu how composition-level and beyond-composition matching signals can be separated.

The remaining contract is prospective and plant linked: source state, community assembly, realized partner sorting, effectiveness and reproductive propagation must be measured on comparable units. Chapter 3 advances to higher-resolution focal measurement in the same island series. Its phenotype and any future effectiveness or dependency observations are not used here as model validation, Bombus-causation proof, pollinator-selection proof or external prediction success.

## Limits

The synthetic coordinate and sign transitions are not empirical trait thresholds. The joint-design coefficients are not field causal effects. The audited horizon and seed ensembles are sensitivity sets, not natural time scales or population sampling distributions. Equalizing initial pollinator richness leaves other mainland-like/island-like scenario differences intact. The external-system registry is not a prevalence sample or held-out prediction set. The Izu secondary analysis lacks plant-specific partner-weighted functional centres and stops at realized matching; it does not show propagation through pollinator effectiveness into reproduction.

# Conclusion

Community reorganization can define a response geometry without determining one biological outcome. Turnover deforms that geometry; response direction emerges from organismal state evaluated against the realized community; local filtering reallocates branches; and assurance modifies downstream magnitude. This relational architecture survives changes in seed ensemble and model horizon, persists without trait adjustment, and does not require reduced initial pollinator richness. World confrontation shows why a one-syndrome vocabulary is insufficient while exposing an outcome-rich, process-poor measurement structure—especially for partner arrival/replacement. Increasing resolution in Izu localizes the present matching signal to source state plus background community composition and rejects a stronger claim of additional null-corrected sorting. The contribution is therefore a mechanistic coordinate system and measurement agenda for conditional post-establishment response, not a calibrated island predictor, natural-frequency estimate or ultimate historical explanation.

## Main figure captions

**Figure 1. Breadth-to-depth mechanistic-resolution funnel.** The synthetic model defines ecological possibilities and a trajectory-conditioned interaction-kernel coordinate; comparative research establishes response diversity and exposes an outcome-rich/process-poor identifiability bottleneck; the Izu zoom separates source-state/community-composition structure from unsupported null-corrected sorting; the remaining effectiveness-to-reproduction contract is handed to Chapter 3 without validation claims.

**Figure 2. Conditional response geometry.** Mean island-minus-mainland functional service across the 21-point starting-position grid under 96 matched community realizations. Realization counts describe the frozen synthetic design and are not frequencies in nature. A prespecified equal-richness sensitivity shows that reduced initial pollinator richness is not necessary for mixed geometry.

**Figure 3. Proximal-WHY hierarchy and relational robustness.** Fixed-surface turnover associations; frozen baseline starting-position/community decomposition with seed-ensemble sensitivity; direction-specific local-filtering transitions; and magnitude improvement versus sign rescue across the assurance envelope. Exact variance shares and filtering strengths are synthetic diagnostics, while component ordering is the primary structural claim.

**Figure 4. From outcome-rich literature to Izu mechanistic resolution.** (A) Direct-measurement availability across 25 source-audited research entries: response outcomes are common whereas source state, loss and especially arrival/replacement are sparse; zero entries meet the full joint contract. Counts are research-entry availability, not independent-archipelago frequencies. (B) The same frozen Izu projection is associated with raw realized matching but not null-corrected matching; exact island-centre magnitudes remain non-unique and the prespecified Oshima bridge is unsupported.

## References

Use the source-audited active reference ledger in `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md`. Hiraiwa & Ushimaru (2017, 2024) are the empirical sources for the Izu triangulation. External-system references remain in the comparative-grounding supplement and are not presented as validation coverage.
