# Conditional island responses: from community response geometry to demographic and evolutionary realization

**Status:** active Chapter 2 scientific manuscript — unified Model 3 + source-audited natural confrontation
**Updated:** 2026-09-27
**Inference architecture:** fixed-state reproductive assay → deterministic genotype-density propagation → finite-population ABM → history/context interventions → source-audited natural confrontation / bounded empirical claim ceiling
**Controlling state:** `docs/CHAPTER2_CANONICAL_STORY_20260827.md`, `docs/CHAPTER2_CLOSURE_20260906.md`, `THESIS_CHAPTER_POSITIONING.md`

## Abstract

Island syndromes are often summarized as directional trait shifts, yet a recurrent functional pressure need not generate one phenotypic endpoint. We asked first how the same broad pollinator-community reorganization can generate opposing plant-response branches, and second how those conditional branches are propagated through reproduction, demography and inheritance.

Using one nested Model 3, we compared the same biological mechanism at three levels. A fixed-state assay measured reproductive-selection gradients before inheritance or demography; a deterministic genotype-density counterpart propagated the same reproduction and Mendelian operator without demographic sampling; and a finite-population ABM added stochastic recruitment, extinction, ancestry and standing-variation loss. A prospectively frozen reduction audit then crossed five starting floral states with fixed visitor compositions, followed by a completed 19,968-case island campaign spanning assurance, chronology, connectivity, founding, life history and recovery.

A source-audited metadata confrontation bounded natural interpretation rather than calibrating the model. Comparable plant responses occurred in 21/25 formally audited studies, direct partner arrival/replacement in 2/25, and full source-state → transition → realized-community → response contracts in 0/25. Existing Izu secondary analyses similarly combined support with failure: functional exposure robustly predicted corrected matching, but matching-to-pollen effects were not leave-one-island sign stable and a historical signed-position projection failed null correction.

Non-uniformity appeared before demographic stochasticity and survived its removal: all three tested four-type visitor compositions produced positive and negative fixed-state selection gradients across starting states, and all three retained mixed deterministic inherited trajectories. Exact duplication of the same functional types under fixed total activity changed the operator by only 1.78×10^-15, whereas changing composition at fixed count strongly changed response. The finite ABM retained the simple-design branching, while the broader island campaign showed that finite demography and history can further alter magnitude, persistence and trajectory. These results support a recurrent functional island syndrome without requiring phenotypic convergence.

## Keywords

community reorganization; response geometry; demographic history; reproductive assurance; floral evolution; plant–pollinator interactions; finite populations; island syndrome

# Introduction

A directional mean can summarize ecological change without identifying how individual lineages respond. This distinction matters whenever the same perturbation produces positive and negative responses among starting states or among realized communities. In such systems, two questions must be separated: what moves the ensemble into a different response regime, and what determines which response branch a particular lineage realizes within that regime.

Island plant–pollinator systems provide a useful setting for this problem because insularity can alter pollinator richness, functional diversity, partner identity, interaction structure and reproductive context at the same time. Comparative island studies document shifts in pollination networks, functional matching, breeding systems and floral traits, but these axes are neither interchangeable nor guaranteed to move in parallel (Traveset et al., 2016; Grossenbacher et al., 2017; Hiraiwa & Ushimaru, 2017, 2024; Hetherington-Rauth & Johnson, 2020). A directional island syndrome may therefore be a valid ensemble description while remaining a poor rule for predicting the response of an individual lineage.

We treat this as one nested post-establishment problem. Model 3 first asks how visitor composition and starting floral state determine reproductive return before demographic updating, then propagates the same reproductive and inheritance rules deterministically, and finally restores finite individuals and demographic stochasticity. Assurance, connectivity, chronology and recovery are interventions within that same model family. The model does not reconstruct the deep-time origin of an island biota or identify the historical cause of a named natural transition. This distinction separates our question from the full assembly problem emphasized by Baker's law and island-colonization theory (Pannell et al., 2015; Grossenbacher et al., 2017; Zell et al., 2025).

The model represents each pollinator by a matching function over a standardized plant functional coordinate. The realized pollinator community defines a community interaction kernel. Partner turnover changes that kernel, plant starting state determines where the kernel is evaluated, and active plant adjustment can move the evaluation point through time. Local filtering and reproductive assurance operate downstream. The resulting response is therefore relational: it depends not only on the plant state or the community in isolation, but on where that state lies relative to the realized interaction kernel.

The key unresolved issue is not simply whether responses are heterogeneous. It is whether the *source* of that heterogeneity has a fixed ecological rank. Realized richness can alter the opportunity regime, but exact richness control need not eliminate compositional contingency. Likewise, a community-realization component that dominates in a small stochastic system need not remain dominant when independent community sampling is pooled. This formulation predicts a scale-dependent response architecture in which the dominant source of response variation need not be fixed: realized community composition should matter most when communities are small and stochastic, whereas starting state should gain relative importance as community sampling stabilizes.

We therefore ask five linked questions within one model. First, can the same visitor composition favour opposite reproductive responses depending on starting floral state? Second, does changing composition at fixed visitor count alter those responses when count itself is neutralized by a fixed-total-activity control? Third, does non-uniformity persist when demographic sampling is removed in the deterministic genotype-density counterpart? Fourth, how does the finite ABM depart from that deterministic trajectory? Fifth, how do assurance, chronology, connectivity, life history and recovery condition which inherited endpoint is realized?

The paper is deliberately synthetic in its primary inference but not isolated from natural evidence. Existing island studies establish that pollinator loss, functional reorganization, buffering and breeding-system change are biologically realistic processes (Feinsinger et al., 1982; Inoue & Amano, 1986; Inoue, 1988, 1990; Andrews et al., 2022). We therefore use source-audited world evidence and existing Izu secondary data as a **metadata confrontation layer**: positive observations establish that the modeled ingredients are biologically non-vacuous, while adverse and missing links define the empirical identifiability ceiling. These data do not calibrate synthetic `k`, branch frequencies or the crossover. The existing same-block visitor → effectiveness → dependency → mature-seed protocol is retained in repository provenance as an optional future validation programme; scientifically it is a post-Chapter-2 transport/falsification study, not a completion gate for the present manuscript.

# Materials and Methods

## Inference architecture and claim boundary

The primary analysis is a frozen synthetic plant–pollinator model. No empirical island outcome was used to tune seeds, synthetic thresholds or the system-size crossover. All synthetic frequencies, variance shares and coordinates are design diagnostics rather than natural prevalence estimates or calibrated field thresholds.

Natural evidence enters only after the synthetic objects and claim boundaries are defined. The confrontation layer combines a formal source audit of 25 research entries across 21 exact geographic labels, a broader source-verified descriptive programme that reached its geography-first stopping rule, source-native secondary reanalyses of compositional change, and existing Izu functional-network / pollen secondary analyses. The formal audit records whether each system directly observes comparable plant response, partner loss or arrival/replacement, realized community change and other mechanism-relevant coordinates without imputing missing axes from outcomes. The broader programme is used to assess biological vocabulary and search saturation, not to estimate natural prevalence.

The Izu secondary-data stress test is likewise deliberately asymmetric. We retain support when functional exposure predicts corrected trait matching, but also retain instability or failure when matching-to-pollen effects are not leave-one-island sign stable, historical signed-position projections fail null correction, or a bridge-state geographic contrast is not independently identified. The natural layer therefore constrains interpretation rather than selecting synthetic parameters.

No conclusion in the current paper requires field confirmation of the synthetic rank crossover. A future same-unit transition-linked study could test transport of the frozen architecture, but it cannot retrospectively define the present mechanism.

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

## Unified Model 3: nested reproductive, deterministic and finite-population levels

Model 3 is the single mechanistic model used for the current Chapter 2 inference. Its nested reductions were specified without using natural-island outcomes to tune parameters. Plants carry additive diploid loci for an abstract access/matching trait and floral investment. Finite compatible pollen delivery generates outcross offspring; delayed selfing can fertilize remaining ovules; inbreeding depression reduces viable selfed offspring; maternal and paternal contributions enter Mendelian inheritance before Poisson recruitment, density regulation and adult survival. No rule explicitly moves a floral trait toward the best visitor.

The island campaign crossed predeclared families for visitor-history transport, fixed-state reproductive assays, reproductive assurance, seed and pollinator connectivity, founding state, trait-grid representation, population scaling, life history, disturbance chronology and recovery. The completed campaign contains 19,968 audited cases across 80 production cells plus six held-out transport rows. All cases passed state/receipt audit and 80 predeclared deterministic replay checks. Extinct endpoints remained undefined rather than coded as zero.

Model 3 is interpreted at a bounded level. Its time step is a reproductive year, distances are standardized dispersal coordinates rather than kilometres, visitor types are functional agents rather than insect counts, and the floral-investment coordinate is not calibrated to colour, size or nectar-guide strength. Several numerical refinement contrasts remain outside the narrow prespecified tolerance, so qualitative directional contrasts and explicit survival outcomes receive greater inferential weight than exact effect magnitudes.
## Source-audited empirical confrontation

The empirical confrontation was frozen as a secondary evidence layer rather than used to tune the synthetic model. For the formal source audit, the research entry was the bookkeeping unit. Each entry was scored separately for directly observed plant response, partner loss or arrival/replacement, realized community change and downstream filtering or reproductive-assurance information. Unavailable coordinates remained unavailable; they were not imputed from reported outcomes, floral syndromes or narrative interpretation. Geography-first expansion used the separately declared stopping rule and did not alter the frozen 25-entry denominator.

For the two source-native network contrasts promoted to the main Results, we used matched plant species rather than treating plants as geographic replicates. Pollinator-richness change was summarized as a per-plant log response ratio, `ln(R_B/R_A)`, and assemblage reorganization as Morisita–Horn turnover, `1 − similarity`. We report medians across matched plant species with exact nonparametric bootstrap percentile intervals. The Wanshan–Yongxing comparison used seven shared plant species from the continental–oceanic island pair (Wang et al., 2025); the two island networks were sampled in different years. The Anijima comparison used eight matched plant species after taking within-plant medians across shared seasons for spatially distinct green-anole presence/absence forest contexts (Quitián et al., 2026). These bootstrap intervals describe plant-level heterogeneity within one geographic contrast and do not provide independent archipelago replication or randomized causal effects. We therefore did not pool the two systems into a universal island coefficient.

The Izu confrontation used the existing source-locked secondary analyses only. We retained the prespecified functional-exposure → corrected-matching coefficients and their leave-one-island sign diagnostics, the matching → pollen coefficients and their weaker leave-one-island stability, the response directions of eight shared lower-matching targets, and the null-corrected signed-position and Oshima-bridge falsification results. No Chapter 3 focal phenotype was used to select or validate these Chapter 2 relations.

# Results

## Unified reduction audit: branching predates demography and survives deterministic inheritance

The prospective reduction audit crossed starting access states `0.20, 0.35, 0.50, 0.65, 0.80` with three four-type visitor compositions and a broad eight-type reference. Under each four-type composition, the fixed-state reproductive assay contained both positive and negative total investment gradients. For example, under `left4`, the gradient was `+1.5048` at starting access `0.20` but `-0.8720` at `0.80`; the signs reversed under `right4`.

Composition mattered at fixed count. The maximum left-versus-right difference in fixed-state total gradient was `2.3768`. By contrast, duplicating each `left4` functional type to produce eight visitor entries changed the fixed-state, deterministic and ABM operators by at most `1.78e-15` under fixed total activity. This is an operator control, not a claim that field species richness is irrelevant.

The deterministic genotype-density counterpart retained mixed positive and negative inherited investment changes in all three four-type visitor contexts, with a maximum left-versus-right endpoint difference of `0.1891`. Demographic stochasticity is therefore not necessary for response branching in this model.

The finite-population ABM also retained mixed signs in all three contexts. In this deliberately simple reduction audit, deterministic-density and mean-ABM response signs agreed in all evaluable cells. The larger island campaign nevertheless shows substantial ABM–density sign disagreement under chronology, assurance, life-history and recovery manipulations, indicating that finite demography modifies rather than creates the upstream branch.

### Legacy reduced response-geometry analyses

The following sections retain the earlier abstract response-geometry results for robustness and provenance. They use a different synthetic reduction with heuristic plant adjustment and, in its deterministic mean-field limit, average external community realization. These analyses are not a second required biological mechanism and are candidates for Supporting Information in the journal version.
### Legacy conditional response geometry is mixed rather than universally directional

Across 96 baseline matched community realizations, 41 were mixed-sign across starting positions, 42 were all-positive and 13 were all-negative. Mean response was approximately U-shaped across the starting-position axis. Across the fixed 48-point joint design, 16 points had mixed mean geometry, 22 were all-positive and 10 all-negative.

Partner loss and arrival were the strongest sign-stable full-range regime associations in the declared additive diagnostic: +0.634 for partner loss and −0.626 for partner arrival. The ten-parameter model explained `R²=0.611` of the negative-fraction surface. These coefficients diagnose movement inside the synthetic design; they are not field causal effect sizes.

For the baseline 21 × 96 matrix, starting position explained 2.18% of total sum of squares, community realization 80.17%, and the starting-position × community remainder 17.64%. Observed sign differed from the fitted additive sign in 271/2016 cells. The baseline therefore shows a relational response geometry: starting state organizes the mean boundary, but branch identity depends strongly on the realized community.

### Legacy realized-richness control

Equalizing initial richness alone retained 53/96 mixed-sign realizations, showing that the historical initial-richness difference was not necessary for individual branching. This control did not equalize subsequent realized richness.

The exact stepwise realized-richness control changed the ensemble mean result more strongly. Realized richness was matched at every simulated step in all six prespecified matching seeds, and the mean geometry became all-positive in 6/6 seeds. Individual response branches nevertheless persisted: 51–65 of 96 remained mixed-sign. Community-realization share remained 50.04–55.92%, starting-position share only 0.94–2.21%, and state × community non-additivity 42.72–48.51%.

Realized richness differences therefore help position the ensemble mean regime, but they do not explain away response branching across realized community compositions.

The equal-turnover control strengthened rather than erased branching. Equalizing the baseline mainland–island partner-arrival and partner-loss rates produced 70/96 mixed individual realizations and 65.61% state × community non-additivity. The baseline turnover-rate asymmetry is therefore not required for branching, although other scenario differences remain.

### Legacy synthetic system-size and response-geometry limit

At zero trait adjustment, pooling independent communities sharply reduced finite-community sampling variation without immediately eliminating branching. Across six prespecified seeds, island-like final-community coefficient of variation fell from 0.575–0.691 at `k=1` to 0.134–0.172 at `k=16`, and empty final island-like communities fell from 7.3–13.5% to 0%. The additive community-realization share declined from 51.4–67.3% to 20.3–34.5%. Mixed individual response geometry nevertheless remained in 44–60/96 realizations at `k=16`, with state × community non-additivity still 50.6–65.4%. Finite-community sampling contributes materially to realization variance but does not by itself generate response branching over the audited finite range.

The exact finite-k moment analysis resolved the asymptote. The deterministic mean-field kernel contrast was all-positive across all 21 starting states, with minimum contrast 0.0208. A multivariate Gaussian approximation based on the exact finite-k kernel mean and covariance increasingly matched the pooled six-seed mixed fraction: absolute error fell from 0.0689 at `k=1` to 0.00654 at `k=16`. Branching is therefore finite-community in the asymptotic sense but is not a rare-extinction or N≈2 artifact.

With active plant adjustment retained, the variance hierarchy itself reversed. Median starting-position share increased monotonically from 2.55% at `k=1` to 10.33%, 27.33%, 42.52% and 55.84% at `k=2,4,8,16`. Median community-realization share fell from 72.98% to 48.03%, 23.52%, 18.26% and 12.72%. Starting position exceeded community realization in 0/6 seeds at `k=1`, 0/6 at `k=2`, and 6/6 seeds at `k=4`, `k=8` and `k=16`. Mixed branching still persisted at `k=16` in 28–42/96 realizations.

The ordering of response determinants is itself regime dependent. Community realization dominates in small stochastic communities; starting state becomes dominant in a larger finite-community regime while branching persists; and the deterministic mean-field limit removes branching. The numerical crossover is model-specific and is not proposed as a natural threshold.

### Legacy downstream response-geometry modifiers

Across the fixed filtering design, 737 lineage contrasts changed sign at least once. Filtering was bidirectional but asymmetric. At filtering strength 0.40, negative → non-negative transitions occurred in 42/268 contrasts (15.67%), whereas positive → non-positive transitions occurred in 337/596 (56.54%). Local filtering therefore acts as a branch allocator rather than as uniformly beneficial support.

Among 580 eligible baseline reproductive declines, assurance multipliers from 0.5× through 4× produced zero sign rescues while upstream effective service remained unchanged. Assurance attenuated decline magnitude but did not create a second sign-changing branch in the tested envelope.

## Model 3 shows historical contingency and assurance-dependent realization

Model 3 did not collapse conditional response into one inherited island phenotype. Under the declared chronology experiment, all compared populations experienced the same final 120-year environment, yet terminal investment differed by history: uninterrupted trajectories changed by +0.2115, early visitor absence by -0.1603, and late visitor absence by +0.0322. All 256 populations survived in each of these three arms. The result therefore demonstrates model-conditional historical contingency rather than a simple mapping from current environment to current trait.

Reproductive assurance changed whether an endpoint existed. Under the declared long visitor-absence schedule, fixed zero assurance yielded 0/256 terminal survivors, whereas fixed 0.5, fixed 0.9 and the corresponding evolving-assurance treatments retained 256/256. This survival contrast is conditional on the model's complete visitor absence, adult replacement schedule and lack of external seed rescue; it is not an empirical extinction probability.

Connectivity also separated into different routes. Increasing pollinator-distance while seed-distance was fixed could reverse the direction of investment change, whereas increasing seed-distance under a fixed pollinator regime altered the response differently. Seed immigration modifies demographic and genetic input; pollinator connectivity modifies the reproductive environment. A single geographic-isolation axis therefore need not represent both processes inside the model.

Transport tests further separated structural ordering from quantitative prediction. The descriptive S/C/I ordering C > I > S was retained in held-out transport cells, but same-regime marginal predictions had mean absolute error 0.0150 and 0.0106, whereas transport across disturbance regimes increased errors to 0.1581 and 0.1417. Similar determinant ordering therefore does not guarantee transport of the trait response itself.
## Metadata confrontation supports biological ingredients while bounding attribution

The frozen formal source audit was outcome-rich but process-poor: direct comparable plant responses were available in 21/25 research entries, direct partner arrival/replacement in only 2/25, and no entry supplied the full matched source-state → transition → realized-community → plant-response contract. Geography-first expansion later reached its outcome-independent stopping rule without closing that longitudinal contract; the broader descriptive programme reached 42 research entries across 37 exact geographic labels without reopening the formal prediction gate.

Two source-native network contrasts provide the narrow external confrontation required for the richness-versus-composition distinction. In the Wanshan–Yongxing matched seven-plant networks, median pollinator assemblage turnover was 0.980 (95% plant-level bootstrap interval 0.944–1.000), whereas the pollinator-richness log response ratio was −0.105 (−1.322 to 0.288; Wang et al., 2025). In the spatially structured Anijima comparison, median turnover was 0.682 (0.497–0.965), whereas the corresponding richness log response ratio was −0.315 (−0.875 to 0.405; Quitián et al., 2026). These intervals quantify heterogeneity among matched plant species inside one geographic contrast; they are not independent geographic replication or causal island effects. We therefore retain them only as evidence that major partner reorganization can occur without a correspondingly decisive richness contrast, not as validation of the synthetic mechanism or a universal island coefficient.

Existing Izu secondary data supplied a deliberately adversarial within-region stress test rather than a validation label. Functional exposure predicted corrected trait matching with positive coefficients in both the five-Izu-island and post-Oshima analyses (`+1.9426` and `+2.0590`), with leave-one-island coefficient signs remaining positive. Translation from matching to pollen receipt was positive on average (`+0.0353` and `+0.0342`) but not leave-one-island sign stable. Among eight shared targets with lower corrected matching, floral responses divided into three shorter, four longer and one unchanged tube response, while pollen receipt divided evenly into four lower and four higher responses. The historical signed-position projection was not supported after null correction, and the Oshima bridge state could not be separated from an Oshima-specific geographic effect.

The confrontation therefore establishes two things simultaneously. First, interaction reorganization, relational matching and heterogeneous downstream responses are biologically non-vacuous. Second, present metadata do not identify a universal natural crossover, historical *Bombus* causation or a complete transition-linked mechanism. The natural evidence closes the present claim ceiling rather than calibrating synthetic `k` or validating the full determinant hierarchy.

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

## Demography turns functional branching into historical contingency

The unified reduction audit establishes that one Model 3 operator already creates multiple functional/reproductive branches before demographic updating, and that these branches persist under deterministic inheritance. The finite ABM adds a distinct statement: even after the same branch enters reproduction and inheritance, the endpoint is not determined by the current pollination environment alone. Timing of visitor loss, reproductive assurance, life history, connectivity and finite demographic sampling alter persistence and inherited investment trajectories.

This makes reproductive assurance a bridge rather than a universal endpoint. In reduced reproductive contrasts it can alter the marginal return to floral investment; in full finite-population trajectories it can determine whether a population persists long enough for an inherited floral endpoint to be defined. Thus the recurrent assurance signal in Chapter 1 can be interpreted as a broadly useful insurance function without implying that every lineage should converge on the same floral morphology or even remain observable under the same demographic conditions.

Historical contingency is equally important for the island-syndrome interpretation. Early and late visitor loss can end in different inherited states despite a common final environment. Consequently, a present-day trait difference need not be invertible to one present-day pollinator state, and convergence of present environments does not imply convergence of histories. Source immigration can also alter the endpoint partly through ancestry replacement, preventing every apparent recovery from being labelled resident adaptation.

These results do not establish natural priority effects, extinction rates or evolutionary timescales. They show that once reproduction and finite demography are made explicit, a functional island syndrome can coexist with multiple historical phenotypic realizations even within one fixed model family.
## Metadata confrontation constrains natural transport without leaving a missing empirical gate

The source-audited natural evidence is informative precisely because it contains both support and failure. The two source-native network contrasts show that strong partner replacement can occur without a sharply identified richness decrease, while the formal audit shows that response outcomes are common and directly observed transition processes are rare. The broader search then reached its stopping rule without closing the missing longitudinal contract. Existing Izu secondary analyses add a within-region hierarchy: a relationship can be robust at one mechanistic step—functional exposure to corrected matching—while becoming unstable or branching at downstream steps. This combination is consistent with interaction reorganization that cannot be compressed into one universal response axis, but it does not estimate the synthetic interaction term or determinant crossover in nature.

The adverse results matter equally. Matching-to-pollen effects are not leave-one-island sign stable; the historical signed-position projection fails null correction; and the Oshima bridge state is not an independently replicated causal boundary. Retaining those failures prevents the simulation from being narrated as a story selected because every natural comparison agrees. Instead, the metadata layer establishes the strongest defensible conclusion: the ingredients and heterogeneous response vocabulary are real, while the complete historical transition and natural determinant-rank crossover remain unidentified.

This is why the present manuscript stops short of claiming that historical *Bombus* loss caused a particular Izu phenotype, that a natural threshold corresponding to `k≈4` exists, or that any current diversity metric is literally synthetic system size. The missing same-unit historical transition limits attribution; it is not a missing result needed to complete the synthetic-plus-metadata argument.

A future same-block visitor exposure → single-visit effectiveness → reproductive dependency → mature-seed study could confront transport of the frozen architecture directly. Such work is a post-Chapter-2 falsification test: positive, null or adverse results would refine external transport, but none is required to create the present response-geometry result.

## Island syndrome as a shifted response distribution

Together, the two model layers support a functional-and-historical interpretation of island syndromes. Insularity can shift the distribution of functional responses without imposing one phenotype on every lineage, and reproduction plus demography can preserve different inherited trajectories even when final environments converge. The syndrome is therefore better treated as a recurrent functional regime with conditional phenotypic realization than as one universal island phenotype.

The more general implication is that ecological heterogeneity has structure. When communities are small and stochastic, among-lineage variation may be dominated by which partners happen to be realized. As community sampling stabilizes, differences among starting states can become more important while relational non-additivity remains substantial. The source of among-lineage variation is therefore itself a biological quantity that can change across regimes.

That perspective changes what comparative studies should try to measure. Reporting only mean trait displacement or partner richness cannot distinguish a shifted ensemble regime from a change in branch allocation. Mechanistic comparison instead requires at least three separable coordinates: the coarse opportunity regime, the realized interaction composition and the lineage state on which that composition acts. The present model shows why those coordinates can change both the sign of individual responses and the apparent ranking of their determinants.

# Conclusion

Pollinator-community reorganization produces conditional rather than fixed plant responses within one nested Model 3. Starting floral state × visitor composition already changes reproductive-selection direction before demography; deterministic inheritance retains the non-uniformity; and finite population dynamics, assurance, connectivity and history determine whether populations persist and how inherited floral investment changes.

The central contribution is therefore not a new universal island phenotype, but an explanation for how a recurrent functional island syndrome can coexist with phenotypic non-uniformity. A shared broad pressure can generate recurrent insurance or accessibility functions while lineage-level direction remains conditional at both the interaction and demographic/evolutionary stages.

Neither model supplies calibrated natural rates or a historical reconstruction of a named island. Source-audited world evidence and existing Izu secondary data make the modeled ingredients biologically non-vacuous while retaining explicit adverse results and the `0/25` full-contract boundary. Same-block Izu E3/E4 measurements remain an optional future falsification/transport programme rather than a prerequisite for the present Chapter 2 claim.

# Figure captions

**Figure 1. One Model 3, three nested levels.** Fixed-state reproductive assays identify pre-demographic selection branching; the deterministic genotype-density counterpart propagates the same reproduction and inheritance rules without demographic sampling; the finite-population ABM restores stochastic recruitment, extinction, ancestry and standing-variation loss.

**Figure 2. Prospective unification audit.** Across five starting access states, each tested four-type visitor composition generates both positive and negative fixed-state gradients and deterministic inherited responses. Changing composition at fixed count changes response strongly, whereas duplicating the same functional types under fixed total activity is identical to machine precision. The finite ABM retains the same simple-design sign branching.

**Figure 3. Full island realization.** The 19,968-case campaign contrasts deterministic genotype density with the finite ABM and tests assurance-dependent persistence, early versus late visitor loss, seed versus pollinator connectivity, life history, founding and recovery. Finite-population departures are interpreted as modifiers of an upstream branch already present in the deterministic operator.

**Figure 4. Metadata confrontation and empirical claim ceiling.** The formal source audit is outcome-rich but transition-process-poor (`21/25` direct comparable responses, `2/25` direct partner arrival/replacement and `0/25` full matched contracts). Two source-native contrasts provide the narrow composition-versus-richness confrontation: Wanshan–Yongxing turnover was 0.980 with richness LRR −0.105 (95% interval −1.322 to 0.288), and Anijima turnover was 0.682 with richness LRR −0.315 (−0.875 to 0.405); these are matched-plant contrasts, not independent causal island effects. The synthetic-to-natural boundary explicitly excludes a natural `k≈4` threshold or literal mapping from visitor diversity to synthetic system size. Existing Izu secondary data provide both support and failure: functional exposure predicts corrected matching robustly, matching-to-pollen translation is not leave-one-island sign stable, the historical signed-position projection is unsupported after null correction, and the Oshima bridge is not independently identified as a causal boundary. Prospective same-block visitor → effectiveness → dependency → mature-seed measurements are post-Chapter-2 transport/falsification rather than a missing present result.