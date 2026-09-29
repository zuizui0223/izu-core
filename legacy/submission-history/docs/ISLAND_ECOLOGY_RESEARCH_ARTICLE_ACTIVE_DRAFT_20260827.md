# Conditional response geometry under island pollinator reorganization

**Status:** active working draft — not submission-ready  
**Updated:** 2026-08-27  
**Controlling state:** `docs/CURRENT_EVIDENCE_STATE.md`, `data/design/chapter2_active_manuscript_mainline_20260827.json`

## Working title

**Conditional response geometry under island pollinator reorganization: starting functional position and local context generate divergent post-establishment plant responses**

## Abstract

Island floras show recurrent reproductive and floral syndromes, but those aggregate patterns combine assembly filtering, evolutionary change after colonization and ecological responses of already-established lineages. Comparative evidence that isolation-associated multivariate response vectors differ among biogeographic contexts motivates a narrower question: when pollinator functional environments are simplified or reorganized, must established plant lineages respond in one direction, or can the sign of response depend on their starting functional position and realized interaction context?

We used a synthetic plant–pollinator model with an explicit one-dimensional matching coordinate, matched mainland-like and oceanic-island pollinator dynamics, a fixed visit-budget service function, local availability / interaction filtering, and a downstream autonomous-assurance route. Rather than treating initial-state dependence as a discovery by itself, we mapped island-minus-mainland functional-service response across the full plant starting-position axis, repeated the map across matched pollinator-community realizations, challenged the result across a fixed 10-parameter Latin-hypercube design, diagnosed which declared dimensions accompanied regime change, decomposed starting-position and community-realization variation, and quantified both the direction of local-filtering sign changes and the assurance multiplier required for sign rescue.

Response was non-monotonic. Forty-one of 96 matched pollinator-community realizations produced both positive and negative responses across starting positions, whereas 42 were all-positive and 13 all-negative. The mean response geometry was mixed-sign, with sign transitions around 0.30–0.35 and 0.65–0.70 on the synthetic starting-position axis. Mixed mean geometry persisted at 16 of 48 points in the fixed joint 10-parameter design; 22 points were all-positive and 10 all-negative. Greater partner loss and lower partner arrival had the largest sign-stable additive associations with the negative portion of the response surface, although leave-one-point-out predictive error remained substantial. In the baseline response matrix, community realization accounted for 80.17% of total sum of squares and starting-position-by-community non-additivity for 17.64%, compared with 2.18% for the starting-position main effect. Local availability / interaction filtering changed response sign for 737 lineage contrasts and did so asymmetrically: positive baselines crossed to non-positive more readily than negative baselines crossed to non-negative at every non-zero tested strength. In contrast, among 580 eligible baseline declines, the autonomous-assurance route produced no sign rescue at any multiplier from 0.5× through 4× while leaving upstream service unchanged and broadly attenuating decline magnitude.

These results support a conditional rather than universal view of post-establishment island response. The same broad pollinator reorganization can produce opposite plant responses because matching consequences depend on partner turnover, starting functional position, realized community state and their non-additive combination. In the present model, local filtering reallocates branch identity with a directional asymmetry, whereas autonomous assurance is a magnitude attenuator rather than a sign-changing rescue mechanism. The reported coefficients, variance shares, frequencies and thresholds describe the declared synthetic design and are not causal field estimates, ecological prevalence estimates or empirically calibrated trait thresholds.

**Keywords:** island syndrome; plant–pollinator interactions; functional matching; response heterogeneity; ecological networks; reproductive assurance; agent-based model

# Introduction

Islands are natural experiments in colonization, ecological simplification and the reorganization of biotic interactions. Plant reproductive systems are especially exposed to those changes because reproduction depends not only on abiotic conditions but also on mate availability and the abundance, identity and functional compatibility of pollinators. Comparative work has therefore identified recurrent island-associated patterns in breeding systems, pollination strategies and floral traits (Grossenbacher et al., 2017; Traveset & Navarro, 2018; Zell et al., 2025).

An island syndrome, however, can arise through several biologically distinct processes. Assembly can filter which lineages reach and persist on islands; evolutionary change can alter traits after colonization; and already-established populations can respond ecologically when their interaction environment changes. Conflating these processes encourages a stronger prediction than the evidence requires: that an island-associated perturbation should push all established lineages toward the same state.

The reproductive literature already suggests why that prediction is unsafe. Baker's law is fundamentally an assembly prediction about the capacity for uniparental reproduction during colonization rather than a guarantee of uniformly high realized selfing after establishment (Pannell et al., 2015). Floral morphology is likewise heterogeneous across island systems: Pacific island–mainland comparisons do not support a single universal flower-size direction, and recent work instead emphasizes dependence on starting size, pollination mode and archipelago context (Hetherington-Rauth & Johnson, 2020; Ciarle et al., 2025). At the network level, oceanic island pollination networks can be smaller and functionally reorganized without every plant experiencing the same change in service (Traveset et al., 2016). Japanese island networks further show that losses in pollinator functional diversity and trait matching can matter more than simple pollinator species counts (Hiraiwa & Ushimaru, 2017, 2024).

These observations motivate a post-establishment question that is distinct from asking whether islands contain more self-compatible plants or simpler interaction networks on average: **when the pollinator functional environment changes in a broadly island-like direction, what determines whether a particular established plant lineage benefits or declines?**

At the dissertation scale, the preceding comparative chapter supplies the when/where handoff: isolation-associated floral and reproductive filtering is detectable in both northern mid-latitude and tropical island floras, persists in native non-endemic assemblages and is expressed through different multivariate response vectors. The present model asks how one broad interaction perturbation can generate such qualitative response diversity. It does not assign either regional vector to a particular synthetic regime or identify why those regional biotas and starting states formed.

Matching geometry provides one candidate answer. A reduction or replacement of pollinator functional types need not have a uniform effect across plant trait space. A plant initially close to a lost functional centre may decline, while another plant at a different starting position may match the reorganized assemblage more closely. If so, the ecological response should be described by a response surface or sign geometry rather than by a single average island effect. Local interaction context can then modify that geometry by determining which portions of the globally feasible partner set are realized at a site. Finally, downstream reproductive filters can alter how service changes propagate into reproductive output without necessarily changing their sign.

We use a synthetic model to separate these roles. The model is deliberately narrower than a complete island-evolution model. It addresses the third layer of the island syndrome—post-establishment response to reorganized interactions. Trait adjustment is retained as a model component but is too weak in the current tested envelope to support a substantive claim about in-situ evolutionary dynamics.

The present analysis asks five linked questions. First, **response geometry:** across plant starting positions, where does the island-minus-mainland functional-service contrast change sign? Second, **joint robustness and regime drivers:** does mixed-sign geometry survive across a broad declared parameter region, and which declared dimensions accompany transitions among all-positive, mixed and all-negative regimes? Third, **state-by-realization decomposition:** how much cell-level response variation is associated with starting position, realized community and their non-additive combination? Fourth, **local context:** at what filtering strengths and in which direction does realized local context change response sign? Fifth, **autonomous assurance:** how strongly must the implemented compensating route be amplified before a service-decline lineage crosses the reproductive sign boundary?

Our central prediction is not that one mechanism universally generates branching. It is that island pollinator reorganization defines a conditional response geometry: starting functional position determines the direction of matching consequences, local context can reallocate branch identity, and downstream assurance can attenuate losses without necessarily reversing sign.

# Materials and Methods

## Scope and inference boundary

All primary results in this manuscript are synthetic model results. No empirical island outcome was used to fit the response thresholds reported here, select random seeds after inspecting results, or estimate the prevalence of response classes. External island systems remain comparative ecological grounding and retained boundaries, not validation coverage of a broad state vocabulary.

The synthetic plant trait is a standardized relative matching coordinate on [0,1]. It is not identified with one named empirical floral trait and the response thresholds on this coordinate must not be interpreted as calibrated corolla-length, colour, nectar-guide or other biological thresholds.

## Mainland-like and island-like pollinator environments

The baseline mainland-like scenario contained nine pollinator types, partner arrival probability 0.28, partner loss probability 0.015, pollinator trait dispersion 0.22, generalist fraction 0.35 and replacement fraction 0.05. The oceanic-island scenario contained four pollinator types, partner arrival probability 0.12, partner loss probability 0.055, trait dispersion 0.16, generalist fraction 0.58 and replacement fraction 0.22.

Pollinator trait values were drawn around the centre of the standardized matching axis and bounded to [0,1]. Generalist breadth was 0.42 and specialist breadth 0.16. For a plant with trait value `x` and pollinator with trait value `p`, the encounter match declined with absolute mismatch according to

`match = exp(-(|x-p| / breadth)^2)`.

Introduced/replacement partners received a multiplicative effectiveness penalty of 0.82 in this matching layer.

## Fixed visit-budget service

Pollinator richness was not allowed to act automatically as greater total visitation. For a plant and the extant pollinator assemblage, the model calculated the mean partner match and converted it to service with a saturating transform:

`service = 1 - exp(-saturation * mean_match)`.

The main sensitivity design used saturation values 1, 2 and 3. These are model sensitivity values rather than fitted empirical estimates.

## Plant-lineage parameters

In the broader model, initial plant trait values are drawn from a truncated Normal distribution with mean 0.5 and SD 0.18. Pollinator dependency is Uniform(0.35, 0.95), assurance ceiling Uniform(0.10, 0.90), assurance responsiveness Uniform(0.004, 0.035), and trait-adjustment scale Uniform(0.01, 0.055). Simulations use 24 lineages and 120 steps in the main envelope. Those counts are design choices, not empirically identified demographic quantities.

When current service falls below 0.45 and extant partners exist, the plant trait moves a fraction of the distance toward the best-matching extant pollinator according to the declared trait-adjustment scale. Previous ablation results show that trait-adjustment heterogeneity has little influence on response sign within the tested envelope; we therefore do not interpret the current model as evidence for evolutionary dynamics.

## Matched response-geometry analysis

To isolate starting-position effects from stochastic differences in pollinator histories, every plant starting position was evaluated against the **same pollinator trajectory within a realization**. Starting positions were evaluated on a 21-point grid from 0 to 1 in increments of 0.05.

For each of 96 matched pollinator-community realizations, we generated one mainland-like and one island-like pollinator trajectory and propagated every starting position through those same trajectories. The primary response was final island-minus-mainland functional service. We classified a realization as mixed-sign when at least one starting position had a positive response and at least one had a negative response. We also averaged response by starting position across realizations to identify sign transitions in the mean response geometry.

This matched design replaces the earlier interpretation of a small set of mixed-sign run counts as a prevalence-like quantity. It asks directly where and when sign changes occur.

## Joint parameter-robustness analysis

We next tested whether mixed mean geometry occupied a substantial region of the declared model space. A fixed 48-point Latin-hypercube design simultaneously varied ten declared perturbation/matching parameters: trait dispersion, generalist fraction, replacement fraction, partner loss, partner arrival, saturation, trait adjustment, generalist breadth, specialist breadth and replacement penalty. Each point used 24 matched community realizations under a common seed ensemble.

Each design point was classified as mixed mean geometry, all-positive mean geometry or all-negative mean geometry across the starting-position grid. Fractions of the 48 design points are reported only as robustness descriptors of this synthetic design.

Without changing the design points or rerunning a denser surface, we diagnosed regime boundaries using the negative fraction of the 21-point starting-position grid as a continuous response. All ten parameters were centred and scaled by their declared ranges and entered together in one additive ordinary-least-squares model with no selection or interaction terms. We report full-range coefficients, leave-one-point-out coefficient sign stability, in-sample `R²`, leave-one-point-out RMSE and pairwise all-positive-to-mixed and mixed-to-all-negative parameter contrasts. These quantities are descriptive multivariate associations within the fixed design, not causal effects.

For the baseline `21 × 96` response matrix and each joint-design `21 × 24` matrix, we partitioned total sum of squares into starting-position, community-realization and non-additive starting-position-by-community components. With one simulated value per cell, the non-additive remainder also contains cell-level simulation variation and cannot be interpreted as a pure empirical interaction variance component. We additionally recorded the fraction of cell signs that differed from the sign predicted by the fitted additive value.

## Local-context filtering threshold map

Local context was represented as an availability / interaction-filtering process, not as added beneficial support. We evaluated filtering strengths 0, 0.10, 0.25, 0.40, 0.50, 0.60 and 0.75 using common seed ensembles across threshold values. The fixed threshold run used saturation values 1, 2 and 3; 12 replicates per saturation; four local contexts; 24 lineages; and 120 steps.

For each lineage contrast, we recorded whether the reproduction-response sign differed from its zero-filtering baseline and the first non-zero filtering strength at which that change occurred. We retained complete baseline-sign to current-sign transition tables at each strength and calculated negative-to-non-negative transitions among baseline-negative contrasts separately from positive-to-non-positive transitions among baseline-positive contrasts. The 864 contrasts enumerate the fixed synthetic design and were not treated as independent biological replicates; no inferential p-values were attached.

## Autonomous-assurance sensitivity map

The autonomous-assurance route was tested as a downstream modifier while holding upstream effective service invariant. Baseline lineage templates were multiplied by assurance factors 0, 0.5, 1, 1.5, 2, 3 and 4, with ceiling and responsiveness bounded at 1. A lineage was eligible for sign rescue when both its baseline island-minus-mainland effective-service contrast and reproduction contrast were negative at assurance multiplier 0.

We recorded the first multiplier at which reproduction became non-negative, the number of eligible declines that improved in magnitude, and any mismatch in upstream effective service across assurance multipliers. This distinguishes a structural magnitude-attenuation effect from genuine sign rescue.

# Results

## Response sign depended non-monotonically on starting functional position

Across 96 matched pollinator-community realizations, 41 contained both positive and negative island-minus-mainland service responses across the starting-position grid. Forty-two realizations were positive across the full grid and 13 were negative across the full grid.

Averaging response at each starting position revealed a mixed-sign mean geometry. Starting positions approximately from 0.00 to 0.30 and from 0.70 to 1.00 had positive mean island-minus-mainland service responses, whereas the central region approximately from 0.35 to 0.65 had negative mean responses. The mean sign changed between 0.30–0.35 and again between 0.65–0.70.

The pattern is therefore not a one-sided threshold in starting state. Under the baseline perturbation, the synthetic response surface is approximately U-shaped: both outer parts of functional space tend to improve relative to the mainland-like counterpart while central starting positions tend to decline.

## Mixed geometry persisted across the joint parameter design but was not universal

In the 48-point fixed joint 10-parameter design, 16 points produced mixed mean geometry across starting positions. Twenty-two produced all-positive mean geometry and 10 all-negative mean geometry.

Thus the model admits three broad regimes—mixed, uniformly positive and uniformly negative—and the mixed regime was not restricted to the baseline setting or one vanishingly narrow corner of the declared joint design. Conversely, mixed geometry was not universal. Parameter combinations can collapse the response surface to one direction.

This result is the main robustness basis for retaining a Research Article route: the qualitative geometry survives joint perturbation, while the coexistence of one-direction regimes provides a meaningful failure boundary rather than forcing branching by construction.

## Partner turnover balance accompanied regime transitions

The additive ten-parameter diagnostic explained `R² = 0.611` of the variation in negative trait-grid fraction, with leave-one-point-out RMSE `0.329`. Partner-loss multiplier had the largest positive full-range coefficient (`+0.634`) and partner-arrival multiplier the largest negative coefficient (`−0.626`); both retained the same sign in all 48 leave-one-point-out fits. Saturation ranked third (`+0.265`). Thus, within the declared design, greater partner loss and lower partner arrival accompanied a larger negative portion of the response surface, but the predictive error precludes a precise classifier.

Boundary contrasts refined this result. Relative to all-positive points, mixed points had lower replacement penalty values (Cliff's delta `−0.574`; a harsher penalty because lower values reduce replacement-partner match) and higher partner-loss multipliers (`+0.506`). Relative to mixed points, all-negative points had lower partner-arrival multipliers (`−0.550`). These are transition-surface associations, not evidence that any one axis causally determines a natural island regime.

## Community realization dominated cell-level variation and combined non-additively with starting position

In the baseline `21 × 96` response matrix, the starting-position main effect accounted for `2.18%` of total sum of squares, community realization for `80.17%` and the non-additive starting-position-by-community remainder for `17.64%`. Observed response sign differed from the fitted additive sign in `271/2016 = 13.44%` of cells.

Starting position therefore organizes the mean U-shaped sign boundary but is not the dominant source of cell-level response variation. Which pollinator community is realized is more important for the magnitude of an individual cell, and a material non-additive remainder shows that the starting-position effect is not a common additive shift across all realizations. Across the joint design, median additive-sign mismatch was `18.06%` for mixed points, compared with `13.59%` for all-positive and `11.61%` for all-negative points, with substantial overlap among regimes.

## Local availability filtering frequently changed branch identity

Across the declared local-filtering envelope, 737 lineage contrasts changed response sign at least once relative to their zero-filtering baseline. Among those contrasts, the median first sign-change strength was 0.40.

The fraction of lineage contrasts showing a sign change increased with filtering strength: approximately 13.2% at strength 0.10, 31.3% at 0.25, 43.9% at 0.40 and 73.5% at 0.75. Because this axis removes or restricts locally realized opportunity, these changes must not be described as the effect of adding support.

The zero-filtering baseline contained 268 negative and 596 positive lineage contrasts. Directional rates were asymmetric at every non-zero strength. At strength 0.40, `42/268 = 15.67%` of baseline-negative contrasts became non-negative, whereas `337/596 = 56.54%` of baseline-positive contrasts became non-positive. At strength 0.75 the corresponding rates were `49.25%` and `84.40%`. Among contrasts that changed sign somewhere in the envelope, the median first change was 0.60 for baseline-negative responses and 0.40 for baseline-positive responses.

The result therefore shows that local realization can reallocate branch identity in both directions, but not symmetrically. Within this fixed design, filtering eroded positive branch identity more readily and earlier than it rescued negative branch identity. Local context is a bidirectional, directionally asymmetric branch allocator rather than a universal buffer.

## Autonomous assurance attenuated magnitude but did not rescue sign

There were 580 eligible baseline declines in the fixed assurance-threshold analysis. Across every tested non-zero multiplier from 0.5× through 4×, the number of sign rescues was zero. Upstream effective service remained identical across assurance multipliers, with zero mismatches.

Magnitude attenuation nevertheless remained broad. At 0.5×, 565 of 580 eligible declines became less negative; at 4×, 539 of 580 did so. The reduced count at higher multipliers does not create a hidden sign-rescue regime: no eligible contrast crossed the non-negative boundary anywhere in the tested envelope.

The implemented assurance route should therefore be interpreted as a robust magnitude attenuator in this model, not as a strong alternative branch capable of reversing the qualitative response.

# Discussion

## Island response is better represented as geometry than as one directional effect

The central result is that one broad pollinator reorganization does not map to one plant response. Its mean sign depends on where a lineage begins in functional matching space, but cell-level response also depends strongly on which pollinator community is realized and on the non-additive combination of position and realization. This moves the inference away from a categorical claim that one heterogeneity component is a universal generator and toward a quantitative question about the geometry and realization of the perturbation.

The approximately U-shaped baseline response shows why an average island effect can conceal mechanistically distinct outcomes. If lineages occupy different regions of functional space before pollinator reorganization, the same change in partner richness, turnover, generalization and replacement can improve matching for some lineages while reducing it for others. The decomposition adds an important qualification: the relevant unit is the position of a lineage relative to the particular realized community, not starting position or island status alone.

This interpretation fits the broader island literature better than a universal post-establishment trajectory. Island assembly can still enrich floras for particular reproductive strategies, and repeated island-associated changes in network structure can still exist at the community level. Neither implies that every established lineage must move in the same downstream direction.

## Mixed, all-positive and all-negative regimes are all part of the result

The joint parameter analysis is important because it prevents the response-geometry result from collapsing into an illustration of one chosen baseline parameterization. Mixed mean geometry occurred across a substantial portion of the declared design, but all-positive and all-negative regimes were also common.

This regime structure is more informative than a single branching count. It implies that bidirectional response is conditional on the combined geometry of partner traits, breadth, turnover, replacement and service saturation. The fixed-surface diagnostic identifies partner loss and arrival as the strongest sign-stable multivariate associations with the negative portion of the surface, while replacement penalty and partner loss distinguish the positive-to-mixed boundary and partner arrival distinguishes the mixed-to-negative boundary most strongly. Because leave-one-point-out predictive error remains substantial, these associations explain the current design better than they predict an unobserved regime. No denser surface or parameter retuning was used after seeing the result.

## Local context changes which branch is realized

The local-context analysis shows that global opportunity alone does not determine downstream response. Filtering of locally available plants, pollinators and interaction pairs can change the sign of a lineage contrast under the same broad island perturbation.

The direction is not universally protective. Independent robustness work already showed both sign rescue and worsening, and the threshold map confirms that sign changes become more common as filtering intensifies. The direction-specific denominators further show a consistent asymmetry: positive branches are lost at a higher conditional rate than negative branches are rescued at every non-zero strength. We therefore use the neutral language **local availability / interaction filtering** and interpret the process as a directionally asymmetric branch allocator. Calling it `support` in a beneficial sense would reverse the actual implementation semantics.

## Reproductive assurance is a propagation filter, not a sign-changing branch in this model

Autonomous assurance is biologically important, but its model role must be stated carefully. The implementation adds a compensating reproductive route when reproduction is low, so attenuation of decline magnitude is partly structural. The informative result is that even large sensitivity multipliers did not convert negative responses to non-negative ones.

This separates two ideas that are often blurred: buffering the magnitude of a decline and changing the qualitative sign of a response. In the present parameterization, assurance does the first and not the second. A natural island lineage with strong autonomous reproduction could of course behave differently; that would require empirical parameterization or a different biologically justified model, not post-hoc amplification of the current route until sign rescue appears.

## Relation to the three layers of the plant island syndrome

The broader conceptual framework distinguishes assembly filtering, in-situ evolution and post-establishment interaction response. The present simulation supports only the third layer directly. It therefore supplies mechanistic HOW and a model-conditional proximal WHY, not the ultimate WHY for why a particular island biota, regional response vector, starting state or local interaction architecture formed.

Assembly predictions such as Baker's law can generate recurrent island syndromes by changing which reproductive strategies colonize and persist. Evolution after colonization can generate additional trait shifts. The present model instead asks what happens to already-established lineages when their interaction environment changes. Keeping those layers separate allows recurrent macroecological island patterns to coexist with heterogeneous local responses without contradiction.

## Empirical boundary

The model result is not yet a completed cross-system causal synthesis. The current canonical evidence state contains source-locked focal channels and several partial external mechanism bridges, but no complete external mechanism bridge and no formal cross-system mechanism fit. Historical Bombus loss is not causally identified, and a general Izu-flora rule is not supported by the current focal calibration.

External island systems should therefore be used here to motivate and delimit ecological response diversity, not to claim that a broad response-state vocabulary has been validated because previously screened cases can be assigned to it. The retained Dominica signed-position failure is especially important as evidence that a more specific empirical mapping can fail and should remain failed rather than be retuned.

## Limitations

First, the matching coordinate is abstract. The sign-switch intervals are model coordinates, not calibrated thresholds for a named floral trait. Second, the baseline mainland-like and island-like scenarios encode directional ecological assumptions but are not fitted estimates of one real archipelago. Third, 24 lineages, 120 steps and the saturation envelope are synthetic design choices. Fourth, the additive driver model uses only 48 fixed points for ten main effects; its coefficients diagnose the declared surface and do not establish causal parameter effects or a precise classifier. Fifth, the non-additive sum-of-squares remainder cannot be separated from cell-level simulation variation. Sixth, the current trait-adjustment component is too weak to support conclusions about evolutionary dynamics. Seventh, the local-context threshold and directional rates are properties of the declared filtering implementation, not field-estimated habitat thresholds or natural frequencies. Finally, no empirical system currently closes the full chain from matched local interaction context through visitor-specific rate and direct per-visit effectiveness to reproductive outcome.

# Conclusions

Post-establishment island response is not inherently monotonic. In the declared model, pollinator reorganization produces a response geometry in which starting functional position organizes the mean sign boundary, partner turnover balance accompanies movement among response regimes, and realized community state plus position-by-community non-additivity govern much of the cell-level outcome. That geometry persists across part of a broad joint parameter design while collapsing to uniformly positive or negative responses elsewhere. Local availability / interaction filtering can change branch identity with a consistent directional asymmetry, whereas autonomous assurance attenuates response magnitude without generating sign rescue in the tested envelope.

The resulting picture is a conditional island response architecture: **common broad perturbation, turnover-dependent regime, position-by-community matching consequence, directionally asymmetric local branch reallocation, and downstream magnitude filtering**. This supplies a mechanistic HOW and a proximal WHY within the model; it does not supply the ultimate historical explanation for observed island contexts. Its next gate is not additional seed search or mechanism tuning, but empirical admission of directly measured mechanisms where the broader comparative programme requires them.

# Figures to regenerate

1. **Fig. 1 — Conceptual architecture.** Three island-syndrome layers, highlighting that the current simulation tests post-establishment interaction response.
2. **Fig. 2 — Response geometry.** Mean island-minus-mainland service across the 0–1 starting-position grid, with realization variability and sign-transition intervals.
3. **Fig. 3 — Joint regime map.** The 48 Latin-hypercube points classified as mixed, all-positive or all-negative mean geometry; parameter-effect diagnostics in supplements.
4. **Fig. 4 — Local context and assurance.** Filtering-strength sign-change curve beside assurance multiplier sign-rescue/magnitude-attenuation curves.
5. **Fig. S1+ — External comparative grounding and retained falsification.** Descriptive only; no `11/11 coverage` validation panel.
6. **Fig. S2 — Conditional-WHY diagnostics.** Fixed-surface parameter coefficients, response-matrix decomposition and direction-specific filtering transition rates.

# Tables to regenerate

- **Table 1.** Full baseline scenario and lineage parameterization with source/status labels (`empirically motivated direction` versus `generic sensitivity choice`).
- **Table 2.** Response-geometry and joint-regime summary counts.
- **Table 3.** Local-context and assurance threshold summaries with explicit synthetic interpretation boundary.
- **Table 4.** Regime-driver, starting-position × community-realization and filtering-directionality diagnostics.
- **Table S1.** One-factor sensitivity sweeps.
- **Table S2.** External systems as comparative grounding / boundary examples, retaining Dominica as a failed specific projection.

# Reference-state note

This draft preserves only literature framing already present in the repository's prior Journal of Ecology draft. The reference list must be regenerated from the source-audited citation matrix before submission; no citation in this working draft should be treated as newly verified by manuscript reassembly alone. Lord (2015) and Méndez (2025) require explicit citation justification or removal at the next audit.
