# Response geometry under community reorganization: richness-sensitive regimes and state-dependent branching

**Status:** active Chapter 2 scientific manuscript — synthetic mechanism mainline; field E3/E4 optional future validation
**Updated:** 2026-09-12
**Inference architecture:** conditional response geometry → realized-richness control → system-size determinant-rank crossover → bounded empirical claim ceiling
**Controlling state:** `docs/CHAPTER2_CANONICAL_STORY_20260827.md`, `docs/CHAPTER2_CLOSURE_20260906.md`, `THESIS_CHAPTER_POSITIONING.md`

## Abstract

Ecological responses to community reorganization are often summarized by a directional mean and explained by a fixed hierarchy of drivers. Both assumptions can fail when realized communities are finite and stochastic. We ask how the same broad pollinator-community reorganization can generate a coherent ensemble tendency while individual plant lineages take opposing response branches, and whether the dominant source of that variation changes as community sampling stabilizes.

Using a frozen plant–pollinator matching model, we separated realized-richness effects from compositional effects and partitioned response variation into starting-state, community-realization and state × community components. We then pooled independent community trajectories across `k={1,2,4,8,16}` while retaining the same response operator. World evidence was used only to bound biological plausibility and the empirical claim ceiling; no field system was used to calibrate the synthetic coordinate or crossover.

Across 96 baseline community realizations, 41 contained both positive and negative responses. Exact stepwise realized-richness matching shifted the ensemble mean geometry to all-positive in all six prespecified matching seeds, yet 51–65/96 individual realizations remained mixed and state × community non-additivity remained 42.72–48.51%. In the active-adjustment system-size audit, median starting-position share rose from 2.55% at `k=1` to 55.84% at `k=16`, while median community-realization share fell from 72.98% to 12.72%; starting position exceeded community realization in 6/6 seeds from `k=4` onward, while 28–42/96 realizations remained mixed at `k=16`.

These results show that community reorganization has no fixed determinant hierarchy. Realized richness helps position the ensemble regime, realized composition controls much of the variation in small stochastic communities, and starting state becomes increasingly important as community sampling stabilizes. Branching disappears only in the deterministic mean-field limit. Island syndromes can therefore be interpreted as ensemble-level regime shifts rather than deterministic lineage-level trait rules, with the source of among-lineage variation itself changing across ecological regimes.

## Keywords

community reorganization; response geometry; finite communities; plant–pollinator interactions; realized richness; community composition; non-additivity; island syndrome

# Introduction

A directional mean can summarize ecological change without identifying how individual lineages respond. This distinction matters whenever the same perturbation produces positive and negative responses among starting states or among realized communities. In such systems, two questions must be separated: what moves the ensemble into a different response regime, and what determines which response branch a particular lineage realizes within that regime.

Island plant–pollinator systems provide a useful setting for this problem because insularity can alter pollinator richness, functional diversity, partner identity, interaction structure and reproductive context at the same time. Comparative island studies document shifts in pollination networks, functional matching, breeding systems and floral traits, but these axes are neither interchangeable nor guaranteed to move in parallel (Traveset et al., 2016; Grossenbacher et al., 2017; Hiraiwa & Ushimaru, 2017, 2024; Hetherington-Rauth & Johnson, 2020). A directional island syndrome may therefore be a valid ensemble description while remaining a poor rule for predicting the response of an individual lineage.

We isolate one layer of that broader problem: the post-establishment response of plant lineages to pollinator-community reorganization. The model does not explain colonization, assembly, persistence or the historical origin of island biotas. Instead, it asks how a declared interaction perturbation propagates once a plant lineage and a pollinator community already exist. This distinction separates our question from the assembly and reproductive-filtering processes emphasized by Baker's law and island-colonization theory (Pannell et al., 2015; Grossenbacher et al., 2017; Zell et al., 2025).

The model represents each pollinator by a matching function over a standardized plant functional coordinate. The realized pollinator community defines a community interaction kernel. Partner turnover changes that kernel, plant starting state determines where the kernel is evaluated, and active plant adjustment can move the evaluation point through time. Local filtering and reproductive assurance operate downstream. The resulting response is therefore relational: it depends not only on the plant state or the community in isolation, but on where that state lies relative to the realized interaction kernel.

The key unresolved issue is not simply whether responses are heterogeneous. It is whether the *source* of that heterogeneity has a fixed ecological rank. Realized richness can alter the opportunity regime, but exact richness control need not eliminate compositional contingency. Likewise, a community-realization component that dominates in a small stochastic system need not remain dominant when independent community sampling is pooled. This formulation predicts a scale-dependent response architecture in which the dominant source of response variation need not be fixed: realized community composition should matter most when communities are small and stochastic, whereas starting state should gain relative importance as community sampling stabilizes.

We therefore ask four linked questions. First, can one broad community reorganization generate mixed, positive and negative response branches? Second, does exact control of realized richness eliminate that branching? Third, does the ordering of starting-state and community-realization contributions change as independent community trajectories are pooled? Fourth, which downstream processes alter branch allocation or response magnitude without being mistaken for the upstream mechanism?

The paper is deliberately synthetic in claim scope. Existing island studies establish that pollinator loss, functional reorganization, buffering and breeding-system change are biologically realistic processes (Feinsinger et al., 1982; Inoue & Amano, 1986; Inoue, 1988, 1990; Andrews et al., 2022), but the available literature rarely observes the full transition on matched units. World and Izu evidence are therefore retained as biological plausibility, falsification context and an empirical claim boundary rather than as calibration data for the synthetic model. Same-block visitor → effectiveness → dependency → mature-seed measurements remain an optional future validation programme, not a completion gate for the present manuscript.

# Materials and Methods

## Inference architecture and claim boundary

The primary analysis is a frozen synthetic plant–pollinator model. No empirical island outcome was used to tune seeds, synthetic thresholds or the system-size crossover. All synthetic frequencies, variance shares and coordinates are design diagnostics rather than natural prevalence estimates or calibrated field thresholds.

World evidence is used only to establish that partner turnover, reproductive buffering, branching and axis decoupling are biologically plausible and to identify the empirical measurement ceiling. Izu remains a future high-continuity validation system, but no Chapter 2 conclusion requires field confirmation of the synthetic rank crossover.

## Synthetic pollinator environments and matching

The baseline mainland-like scenario contained nine pollinator types, partner arrival probability 0.28, partner loss probability 0.015, trait dispersion 0.22, generalist fraction 0.35 and replacement fraction 0.05. The island-like scenario contained four pollinator types, partner arrival probability 0.12, partner loss probability 0.055, trait dispersion 0.16, generalist fraction 0.58 and replacement fraction 0.22. Generalist breadth was 0.42 and specialist breadth 0.16. Replacement partners received a multiplicative effectiveness penalty of 0.82.

For plant position `x` and pollinator position `p`, matching was

`match = exp(-(|x-p| / breadth)^2)`.

Under a fixed visitation budget, total service depended on mean extant-partner match rather than increasing automatically with richness:

`service = 1 - exp(-saturation × mean_match)`.

## Community interaction kernel and response coordinate

For environment `E`, plant state `x` and extant pollinator `j`, the match contribution is

`k_Ej(x) = a_Ej exp(-((x - p_Ej) / b_Ej)^2)`,

where `p_Ej` and `b_Ej` are pollinator position and breadth and `a_Ej` is the replacement penalty or 1. The community interaction kernel is `K_E(x)=mean_j k_Ej(x)`, with zero for an empty community, and service is a strictly increasing saturation of `K_E(x)`.

With active trait adjustment, the final plant state depends on the realized pollinator trajectory. The response coordinate is therefore relational: it compares the endpoint island-like and mainland-like kernels at their trajectory-conditioned plant states. Conditional on a realized pollinator trajectory, plant-state motion is deterministic.

## Matched response geometry

Starting positions were evaluated on a 21-point grid from 0 to 1. Within each realization, all starting positions experienced the same mainland-like and island-like pollinator trajectories. We generated 96 matched community realizations. A realization was mixed-sign when at least one starting position had a positive response and at least one had a negative response.

A fixed 48-point Latin-hypercube design varied ten perturbation and matching dimensions. The fraction of starting positions with negative mean response was regressed on all ten centered and range-scaled parameters in one prespecified additive model. No post-hoc model selection was used.

## Starting-state × community-realization decomposition

For each 21 × 96 response matrix, total sum of squares was partitioned exactly into a starting-position additive component, a community-realization additive component and a starting-position × community non-additive remainder. Because each trajectory is generated once and shared across all starting positions, the non-additive remainder is not within-cell Monte Carlo noise.

## Realized-richness controls

Two controls were used. First, initial richness was equalized while retaining subsequent differences in loss and arrival. Second, a stronger hard control matched realized richness at every simulated step by uniformly subsampling only the larger of each mainland-like/island-like community pair to the smaller realized richness. Subsampling was response-blind and independent of plant state and pollinator traits. Six matching seeds were prespecified.

A separate equal-turnover control set island-like partner-arrival and partner-loss rates to the frozen mainland baseline while retaining all other scenario differences. Equalizing the baseline mainland–island partner-arrival and partner-loss rates therefore tests the necessity of the turnover-rate asymmetry specifically; it does not make the two scenarios identical.

## Finite-community system-size audit

The finite-community stochastic formulation was retained because among-realization community variation is itself a focal component. A deterministic mean-field reduction would average over community-realization variation by construction.

We pooled `k={1,2,4,8,16}` independent copies of mainland-like and island-like community trajectories before evaluating the same service function. One audit used zero trait adjustment to isolate finite-community sampling and permit exact finite-k moment calculations. A second prespecified audit retained the headline active plant-adjustment operator (`trait_adjustment=0.03`) and the existing six-seed ensemble to test whether the ordering of starting-position and community-realization variance components changes with system size.

For the zero-adjustment submodel, exact terminal count and kernel moments were computed and branch-class probability was approximated with a multivariate Gaussian. This is not presented as an exact Fokker–Planck or full linear-noise solution.

## Downstream modifiers

Local context was represented as availability and interaction filtering. Filtering strengths were 0, 0.10, 0.25, 0.40, 0.50, 0.60 and 0.75. Autonomous reproductive assurance was varied independently from 0× to 4×. Upstream effective service was required to remain invariant across assurance multipliers before interpreting downstream reproductive changes.

# Results

## Conditional response geometry is mixed rather than universally directional

Across 96 baseline matched community realizations, 41 were mixed-sign across starting positions, 42 were all-positive and 13 were all-negative. Mean response was approximately U-shaped across the starting-position axis. Across the fixed 48-point joint design, 16 points had mixed mean geometry, 22 were all-positive and 10 all-negative.

Partner loss and arrival were the strongest sign-stable full-range regime associations in the declared additive diagnostic: +0.634 for partner loss and −0.626 for partner arrival. The ten-parameter model explained `R²=0.611` of the negative-fraction surface. These coefficients diagnose movement inside the synthetic design; they are not field causal effect sizes.

For the baseline 21 × 96 matrix, starting position explained 2.18% of total sum of squares, community realization 80.17%, and the starting-position × community remainder 17.64%. Observed sign differed from the fitted additive sign in 271/2016 cells. The baseline therefore shows a relational response geometry: starting state organizes the mean boundary, but branch identity depends strongly on the realized community.

## Realized richness moves the coarse regime but does not eliminate branching

Equalizing initial richness alone retained 53/96 mixed-sign realizations, showing that the historical initial-richness difference was not necessary for individual branching. This control did not equalize subsequent realized richness.

The exact stepwise realized-richness control changed the ensemble mean result more strongly. Realized richness was matched at every simulated step in all six prespecified matching seeds, and the mean geometry became all-positive in 6/6 seeds. Individual response branches nevertheless persisted: 51–65 of 96 remained mixed-sign. Community-realization share remained 50.04–55.92%, starting-position share only 0.94–2.21%, and state × community non-additivity 42.72–48.51%.

Realized richness differences therefore help position the ensemble mean regime, but they do not explain away response branching across realized community compositions.

The equal-turnover control strengthened rather than erased branching. Equalizing the baseline mainland–island partner-arrival and partner-loss rates produced 70/96 mixed individual realizations and 65.61% state × community non-additivity. The baseline turnover-rate asymmetry is therefore not required for branching, although other scenario differences remain.

## Determinant ordering changes with finite-community system size

At zero trait adjustment, pooling independent communities sharply reduced finite-community sampling variation without immediately eliminating branching. Across six prespecified seeds, island-like final-community coefficient of variation fell from 0.575–0.691 at `k=1` to 0.134–0.172 at `k=16`, and empty final island-like communities fell from 7.3–13.5% to 0%. The additive community-realization share declined from 51.4–67.3% to 20.3–34.5%. Mixed individual response geometry nevertheless remained in 44–60/96 realizations at `k=16`, with state × community non-additivity still 50.6–65.4%. Finite-community sampling contributes materially to realization variance but does not by itself generate response branching over the audited finite range.

The exact finite-k moment analysis resolved the asymptote. The deterministic mean-field kernel contrast was all-positive across all 21 starting states, with minimum contrast 0.0208. A multivariate Gaussian approximation based on the exact finite-k kernel mean and covariance increasingly matched the pooled six-seed mixed fraction: absolute error fell from 0.0689 at `k=1` to 0.00654 at `k=16`. Branching is therefore finite-community in the asymptotic sense but is not a rare-extinction or N≈2 artifact.

With active plant adjustment retained, the variance hierarchy itself reversed. Median starting-position share increased monotonically from 2.55% at `k=1` to 10.33%, 27.33%, 42.52% and 55.84% at `k=2,4,8,16`. Median community-realization share fell from 72.98% to 48.03%, 23.52%, 18.26% and 12.72%. Starting position exceeded community realization in 0/6 seeds at `k=1`, 0/6 at `k=2`, and 6/6 seeds at `k=4`, `k=8` and `k=16`. Mixed branching still persisted at `k=16` in 28–42/96 realizations.

The ordering of response determinants is itself regime dependent. Community realization dominates in small stochastic communities; starting state becomes dominant in a larger finite-community regime while branching persists; and the deterministic mean-field limit removes branching. The numerical crossover is model-specific and is not proposed as a natural threshold.

## Local filtering reallocates branches; assurance changes magnitude

Across the fixed filtering design, 737 lineage contrasts changed sign at least once. Filtering was bidirectional but asymmetric. At filtering strength 0.40, negative → non-negative transitions occurred in 42/268 contrasts (15.67%), whereas positive → non-positive transitions occurred in 337/596 (56.54%). Local filtering therefore acts as a branch allocator rather than as uniformly beneficial support.

Among 580 eligible baseline reproductive declines, assurance multipliers from 0.5× through 4× produced zero sign rescues while upstream effective service remained unchanged. Assurance attenuated decline magnitude but did not create a second sign-changing branch in the tested envelope.

## Empirical evidence bounds plausibility and identifiability rather than validating the crossover

The frozen external audit was outcome-rich but process-poor: direct plant responses were available in 21/25 research entries, whereas direct partner arrival/replacement was available in only 2/25, and no entry supplied the full matched source-state → transition → realized-community → plant-response contract. Geography-first expansion later reached an outcome-independent zero-novelty stopping rule without closing that longitudinal contract.

This empirical programme therefore supports biological plausibility and defines the causal claim ceiling. It does not assign natural systems to synthetic `k`, estimate a field crossover near `k=4`, or validate the synthetic determinant hierarchy. Izu remains a useful future high-continuity system for same-block visitor → effectiveness → dependency → mature-seed measurements, but those measurements are not required for the present paper.

# Discussion

## Community reorganization has two separable consequences

The first result is a separation of ensemble displacement from lineage-level branch identity. Exact realized-richness matching moved the ensemble mean geometry decisively, demonstrating that richness can control the coarse opportunity regime. Yet mixed responses and large state × community non-additivity persisted after realized richness was equalized. Richness therefore changes where the response distribution sits without uniquely determining which side of that distribution an individual lineage occupies.

This distinction matters for interpreting island syndromes. Comparative island ecology often asks whether insularity shifts a trait or reproductive strategy on average, and such mean shifts can be real (Grossenbacher et al., 2017; Hetherington-Rauth & Johnson, 2020). Our result identifies a different inferential level: an ensemble tendency does not imply a deterministic lineage-level rule. The same island-like community reorganization can produce opposing responses because plant state is evaluated against a realized interaction environment rather than against richness alone.

The result is also not that richness is irrelevant. Realized richness helps position the ensemble mean regime, whereas realized composition and starting state determine much of the within-regime response geometry. Treating these as separate operations avoids forcing richness, composition and lineage state into one undifferentiated explanation.

## The rank of ecological determinants is itself conditional

The strongest new result is that the hierarchy of determinants changes as community stochasticity is reduced. In the baseline finite-community regime, community realization dominates much of the additive variance. Under active-adjustment system-size pooling, starting-state share rises and community-realization share falls until their ordering reverses in every prespecified seed from `k=4` onward.

This does not identify a universal threshold at `k=4`. Synthetic `k` pools independent pollinator trajectories; it is not visitor richness, Hill diversity or a directly observable island-system coordinate. What is transferable is the qualitative statement that the dominant source of response variation need not be fixed. A factor that appears primary in one ecological regime can become secondary in another without changing the underlying response operator.

That point is broader than the particular island contrast used here. Variance partitioning is often read as if the largest component identifies a stable property of the system. Our system-size audit shows why that interpretation can fail when one component is generated by finite sampling of an interaction community. As stochastic compositional variation contracts, previously masked differences among starting states become increasingly important. The ecological question is therefore not only *which factor matters most?* but *under what sampling regime does each factor become dominant?*

The zero-adjustment asymptotic analysis adds a second boundary. Finite-community branching persists well beyond the disappearance of empty-community events and remains closely reproduced by second-order Gaussian structure at `k=16`, but the deterministic mean-field contrast is all-positive. Thus branching is genuinely finite-community in the asymptotic sense while remaining ecologically broad across intermediate finite regimes. This separates a finite-community mechanism from a trivial rare-extinction artefact.

## Downstream modifiers occupy different causal positions

Local filtering and reproductive assurance do not simply add more context to the same mechanism. They operate at different positions in the response chain. Filtering changes which interaction opportunities remain locally available and can therefore reallocate response branches. Assurance acts after effective service and changes reproductive magnitude without sign rescue in the tested envelope.

This ordering matters because otherwise several biologically distinct processes can be collapsed into the phrase “context dependence.” In the present architecture, turnover and richness help move the coarse geometry, realized composition and starting state allocate branches within it, local filtering can reallocate those branches, and assurance changes downstream magnitude. The distinction parallels empirical island systems in which pollinator-network restructuring, functional compensation and mating-system responses can occur together but need not represent the same causal step (Inoue & Amano, 1986; Hiraiwa & Ushimaru, 2017, 2024; Andrews et al., 2022).

## Empirical incompleteness limits attribution, not the synthetic result

Existing island studies contain many pieces of the proposed response chain, but rarely on the same transition units. The frozen audit makes that asymmetry explicit: plant outcomes are common, direct observations of partner replacement are rare, and the full source-state → transition → realized-community → response sequence is absent. The unresolved matched historical transition therefore bounds causal attribution rather than invalidating the synthetic mechanism.

This is why the present manuscript stops short of claiming that historical *Bombus* loss caused a particular Izu phenotype, that a natural threshold corresponding to `k≈4` exists, or that any current diversity metric is literally synthetic system size. Historical Izu work is valuable precisely because it records linked changes in pollinators, mating systems and population differentiation (Inoue & Amano, 1986; Inoue, 1988, 1990; Inoue & Kawahara, 1990), but those records do not supply the matched longitudinal estimand required to validate the rank crossover.

Izu remains useful as a future validation system because same-block visitor exposure, legitimate contact, single-visit deposition, reproductive dependency and mature seed can in principle be linked within one regional series. Positive or negative results from such a study would extend the mechanism empirically; neither is required for the current paper to make its conditional-response claim.

## Island syndrome as a shifted response distribution

Together, the results support an ensemble interpretation of island syndromes. Insularity can shift the distribution of possible responses without imposing one phenotype on every lineage. In this view, the syndrome is therefore the shifted response regime and its variance architecture, not a universal phenotype.

The more general implication is that ecological heterogeneity has structure. When communities are small and stochastic, among-lineage variation may be dominated by which partners happen to be realized. As community sampling stabilizes, differences among starting states can become more important while relational non-additivity remains substantial. The source of among-lineage variation is therefore itself a biological quantity that can change across regimes.

That perspective changes what comparative studies should try to measure. Reporting only mean trait displacement or partner richness cannot distinguish a shifted ensemble regime from a change in branch allocation. Mechanistic comparison instead requires at least three separable coordinates: the coarse opportunity regime, the realized interaction composition and the lineage state on which that composition acts. The present model shows why those coordinates can change both the sign of individual responses and the apparent ranking of their determinants.

# Conclusion

Pollinator-community reorganization produces conditional rather than fixed plant responses. Realized richness helps place the coarse response regime, but plant starting state evaluated against realized community composition retains substantial branch contingency. More importantly, the hierarchy governing that variation is itself conditional: community realization dominates in small stochastic communities, starting state becomes increasingly important as community sampling stabilizes, and deterministic mean-field averaging ultimately removes finite-community branching.

The central contribution is therefore not a new universal island syndrome, but a reason such universal rules can fail. Ensemble shifts, lineage-level branch allocation and the ranking of their determinants are distinct ecological properties. A factor can dominate variation in one finite-community regime and lose that dominance in another without any change to the underlying response operator.

The result is a response geometry, not a calibrated field threshold. Local filtering and assurance occupy downstream positions in that architecture, and current world evidence bounds biological plausibility and historical identifiability rather than calibrating the synthetic crossover. Same-block Izu E3/E4 measurements remain an optional future validation programme, not a prerequisite for current-paper closure.

# Figure captions

**Figure 1. Conditional-response architecture and scale-dependent determinant hierarchy.** The inference chain separates coarse regime placement from within-regime branch identity. Realized richness moves the ensemble regime; starting state × realized composition allocates branches. System-size scaling then shows that this within-regime hierarchy is itself conditional: community realization dominates in small stochastic communities, starting state becomes dominant in a larger finite-community regime while branching persists, and the deterministic mean-field limit removes branching.

**Figure 2. Baseline response geometry and structural controls.** Baseline matched community realizations contain mixed, all-positive and all-negative response worlds. Exact realized-richness matching shifts the ensemble mean to all-positive in all six prespecified seeds while retaining 51–65/96 mixed individual realizations. The equal-turnover control yields 70/96 mixed realizations and 65.61% state × community non-additivity. The finite-community system-size audit reduces island-like final-count CV from 0.575–0.691 at `k=1` to 0.134–0.172 at `k=16` while retaining 44–60/96 mixed realizations. With active adjustment, the rank crossover shifts median starting/community shares from 2.55%/72.98% at `k=1` to 55.84%/12.72% at `k=16`.

**Figure 3. Proximal mechanism and downstream modifiers.** Partner loss and arrival organize coarse regime movement on the frozen joint design; starting-state and community-realization components plus their non-additive remainder quantify branch structure. Local filtering reallocates branches bidirectionally but asymmetrically, whereas reproductive assurance attenuates decline magnitude without sign rescue in the declared envelope.

**Figure 4. Empirical claim boundary and future validation.** World evidence establishes that branching, turnover, buffering and axis decoupling occur in island systems but does not supply a matched longitudinal contract sufficient to validate the synthetic determinant hierarchy. The prospective Izu visitor → effectiveness → dependency → mature-seed chain is retained as optional future validation, not as a current manuscript completion gate.