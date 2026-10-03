# Directional similarity can mask opposite changes in historical repeatability in a generative island-floral model

**Status:** preferred journal candidate Evolution Letters; Ecology Letters fallback only after ecological recast; separate from the locked Oikos submission surface  
**Updated:** 2026-10-03  
**Inference boundary:** system-uncalibrated Model 3; natural islands are biological confrontation, not fitted targets

## Abstract

Repeated environments can generate recognizable evolutionary responses without producing identical trajectories, but apparent parallelism can refer to shared direction, shared magnitude or reproducible historical effects. Islands are useful because altered pollination recurs across archipelagos while proposed plant island-syndrome components remain heterogeneous.

We examined one eco-evolutionary Model 3 from reproductive selection through a conditional deterministic genotype-density closure, genetic accessibility and finite-population realization. The focal analyses comprised 19,968 audited island cases and a 24,576-case, 200-season isolation bridge.

At inbreeding depression 0.50, the finite ABM had a negative mean far-minus-near investment effect (-0.1446) and complete occupancy. An exploratory exact-source reanalysis of the frozen 3 × 128 × 8 start-by-history-by-demographic tensor showed that continuous visitor-history effects were reproducible despite noisy sign labels: eight-repeat history reliability was 0.621 and split-half correlation was 0.690. Increasing plant capacity and pooling visitor histories both nearly eliminated mixed-sign history labels (12→1 and 12→0), yet changed historical repeatability in opposite directions. Capacity increased eight-repeat reliability to 0.825, whereas visitor pooling reduced it to 0.103. A separate high-depression deterministic sensitivity entered quasi-extinction and was excluded from persisting-population inference.

Thus directional sign uniformity does not uniquely identify evolutionary repeatability or its mechanism. The same apparent increase in parallelism can accompany either a more reproducible historical imprint or its erosion by environmental averaging.

## Keywords

parallel evolution; nonparallel evolution; island syndrome; floral evolution; pollination; reproductive assurance; genetic accessibility; standing variation; finite populations; evolutionary predictability

# Introduction

Parallel evolution is compelling because replicated environmental change appears to reveal how predictable adaptation can be. Yet replicates often differ in direction, magnitude or genetic basis. Parallelism is therefore treated as quantitative rather than binary (Oke et al. 2017; Stuart et al. 2017; Bolnick et al. 2018). Direction and magnitude are already recognized as distinct trajectory properties, and recent measurement work explicitly warns that different parallelism metrics answer different questions (Venkataram & Kryazhimskiy 2023; Arendt et al. 2025). Common function can also coexist with non-parallel morphology through many-to-one mapping (Thompson et al. 2017).

Islands provide a natural arena for this problem. Isolation repeatedly alters dispersal, population size, biotic interactions and the availability or identity of pollinators. These recurring pressures motivate the idea of an island syndrome: predictable differences between island organisms and their mainland relatives. For plants, however, the syndrome is incomplete. A Pacific comparison of 556 species in 136 phylogenetically independent island–mainland contrasts found no general reduction in flower size, despite reductions in some archipelagos (Hetherington-Rauth & Johnson 2020). A recent review likewise found strongly uneven support among proposed plant island-syndrome components and called for explicitly multidimensional tests (Ciarle & Burns 2025). At the same time, individual archipelagos such as Ogasawara can show recognizable pollination-associated suites of traits and visitor shifts (Abe 2006). Recent work on island wrens further shows that parallel island-syndrome phenotypes can coexist with largely population-specific genomic differentiation (Jezierski et al. 2026). The unresolved issue is therefore not simply whether an island syndrome exists, or whether phenotype and genotype are equally parallel, but where along the causal path from ecology to realized evolution stronger forms of repeatability are first lost.

Pollination-mediated island evolution is well suited to separating these levels. A recurrent ecological problem can first alter reproductive returns through the amount and functional composition of visitors. Reproductive assurance and inbreeding depression can then change which trajectories remain viable. Even when selection is shared, the response can depend on which trait variation is genetically accessible. Finally, finite populations, immigration, chronology and extinction determine which accessible trajectories are realized. Existing theory and models establish many of these components individually; our question is whether one explicit biological engine can localize the loss of repeatability across them.

We use a single eco-evolutionary Model 3 rather than separate response rules for different syndrome components. Plants carry diploid access/matching and floral-investment traits. Visitor functional types determine finite compatible pollen transfer; outcrossing and delayed selfing generate viable offspring; Mendelian inheritance transmits trait variation; and recruitment, survival, immigration and finite population size determine persistence and realized evolution. The traits are abstract functional coordinates, not literal corolla dimensions or colours, and no rule directly moves a population toward an island syndrome.

We ask four questions. First, can functional replacement redirect selection at fixed visitor number? Second, when finite outcomes become more uniform in sign, does reproducible visitor-history structure necessarily decline? Third, are genetic-accessibility effects persistent constraints or time-limited differences in response speed? Fourth, does a long stationary extension approach a biologically interpretable regime? These questions separate direction, magnitude, historical imprint and time rather than compressing them into one repeatability score.

# Materials and Methods

## One Model 3, four repeatability stages

All analyses use one Model 3 reproductive and inheritance operator. The frozen campaign contains 19,968 audited cases spanning assay, history, assurance, connectivity, founding, scaling, life-history, disturbance and recovery treatments. A prospectively frozen isolation bridge adds 24,576 cases crossing 128 independent visitor histories, eight demographic repeats, three starting investment states and four near–far interventions. Later experiments alter declared parameters or initial conditions while retaining the same operator.

We organize inference into four stages.

**Immediate reproductive selection** asks how plant state and visitor environment change marginal reproductive return before inheritance or demographic updating.

**Conditional deterministic propagation** follows the same reproduction and Mendelian inheritance operator as genotype densities without demographic sampling; it is a mechanistic closure, not the stochastic mean of the finite ABM.

**Genetic accessibility** changes standing variation or mutation input while holding the ecological operator fixed.

**Finite realization** exposes the inherited process to recruitment, survival, extinction, ancestry change, chronology and connectivity.

A result can therefore be repeatable at one stage and non-repeatable at the next.

## Claim hierarchy and simulation inference ceiling

The simulation is used to establish **sufficiency and separation**, not natural prevalence or necessity. We distinguish three claim levels.

1. **Model-established result.** At the occupied 200-season finite-population horizon, directional sign uniformity and reproducible visitor-history effects are distinct. Two interventions can both reduce mixed-sign histories while moving continuous history reliability in opposite directions.
2. **General logical implication.** An apparent increase in directional similarity does not, by itself, identify whether historical contingency has weakened, become more reproducible relative to demographic noise, or been averaged away.
3. **Empirical prediction.** Natural tests should measure both direction and reproducibility of population-specific effect magnitudes, while treating genetic-accessibility rankings as potentially time dependent.

The model does not estimate natural equilibrium time, how common any route is in nature, which route dominates a named archipelago, or the natural effect size or evolutionary rate of any transition.

**Table 1. Stage-specific repeatability diagnostics.** The stages are deliberately not reduced to one scalar because they measure different biological objects.

| Stage | Replicate/contrast unit | Repeatability diagnostic | What counts as loss of stronger repeatability |
|---|---|---|---|
| Immediate selection | starting floral state × controlled visitor environment | sign and magnitude of marginal reproductive gradient | shared visitor change does not preserve one gradient direction |
| Reproductive context | assurance × inbreeding depression × life history | persistence plus robustness of gradient/inherited sign | a route changes sign or fails across declared reproductive contexts |
| Conditional deterministic closure | independent visitor history × starting state | far-minus-near inherited response without demographic sampling | a closure-level direction changes across viable histories |
| Genetic accessibility | trait-specific standing variation and mutation input | attenuation of selected response on the constrained axis | shared ecology produces unequal reachable response among trait axes |
| Finite realization | demographic repeats, chronology and connectivity | direction, continuous history reliability and realized endpoint | sign uniformity and reproducible history structure change differently |


## Functional replacement versus visitor scarcity

The reduction audit crossed starting access states 0.20, 0.35, 0.50, 0.65 and 0.80 with three four-type visitor compositions and a broad eight-type reference. A same-count rematching intervention compared left- and right-shifted visitor compositions at identical visitor number. A duplication control doubled the number of visitor entries while holding total activity fixed, testing whether the operator responded to composition rather than the bookkeeping count of visitor types.

The relevant inference is directional and state dependent. The deliberately mirror-symmetric left/right construction is used as an operator test; equal-and-opposite magnitudes are not treated as discovered ecological thresholds.

## Reproductive context and robustness

A prospective causal knockout separated visitor scarcity, reproductive assurance and floral-investment cost. A broader robustness surface varied visitor activity, assurance, investment cost, inbreeding depression and annual/perennial life histories. The assurance-by-cost route was retained as a headline mechanism only if its declared sign and inherited-response criteria survived the full preregistered robustness rule.

The isolation backbone was separately propagated at inbreeding-depression values 0.25, 0.50 and 0.75 while retaining the frozen visitor histories, founders, trait grid and horizon. We distinguish an intervention-averaged mean direction from history-level direction across starting states.

## Standing variation and mutation

Prospective standing-variation experiments reduced founder variation on either the access or investment axis while holding the visitor environment, reproduction, inheritance and mutation rate fixed. This asks whether a selected response remains reachable when one trait axis begins with little selectable variation.

A later mutation-input analysis normalized de novo mutation to the founder additive-variance proxy because Model 3 contains no environmental variance and therefore does not identify literal mutational heritability. Low-standing populations were compared with a high-standing reference at years 400 and 800. Claims are restricted to the tested finite horizon.

A preregistered mutation–pleiotropy timing experiment failed its success criteria. Thresholds were not lowered and the horizon was not extended after inspection; the failed route remains part of the evidence.

## Prospective long-horizon diagnostic

After the focal analyses were complete, we prospectively froze a horizon extension before inspecting its outcomes. Selected deterministic-isolation and mutation-accessibility contrasts were evaluated at 200, 400, 800, 1,600, 3,200 and 6,400 reproductive seasons, with 6,400 fixed as the maximum horizon and no outcome-dependent extension. Stationarity required stability across both 1,600→3,200 and 3,200→6,400 intervals under predeclared tolerances.

These runs are stationary-environment stress tests, not reconstructions of geological island history. A model season is a reproductive season, not necessarily a calendar year, and the extension adds no succession, speciation, coevolution, changing source pool or calibrated natural mutation rate. We additionally tracked deterministic density mass because a frequency trajectory can remain mathematically defined after its expected population mass becomes biologically smaller than one individual.

## Finite realization and natural confrontation

Finite-population simulations retain the same reproductive and inheritance operator but add demographic sampling, survival, extinction, immigration and ancestry turnover. Chronology and connectivity interventions distinguish visitor-history effects from demographic/genetic input.

Because sign labels proved repeat-sensitive, we performed an explicitly exploratory exact-source reanalysis of the original verified bridge exports. For each intervention, the finite tensor contained three starts × 128 visitor histories × eight demographic repeats. A balanced crossed decomposition treated start as fixed, history and start×history as random, and repeat as residual. We report history-structured variance, single-trajectory ICC, reliability of the eight-repeat mean, and the correlation between history means from repeats 1–4 and 5–8. Uncertainty uses 1,999 visitor-history bootstrap resamples (seed 927032). This post-hoc diagnostic tests interpretation of the frozen outcomes; it is not a preregistered hypothesis test.

Natural island systems are used only for source-audited biological confrontation. They are not assigned to synthetic parameter cells, and cross-sectional island contrasts are not treated as measured historical trajectories.

# Results

## Functional repeatability already depends on ecological state

The immediate selection assay did not yield one universal floral response. Under each four-type visitor composition, fixed-state investment gradients included both positive and negative values across starting access states. Under the left-shifted composition, for example, the gradient was +1.5048 at starting access 0.20 but -0.8720 at 0.80; the direction reversed under the right-shifted composition.

Functional replacement mattered even when visitor number was unchanged. The maximum left-versus-right difference in the fixed-state gradient was 2.3768. Deterministic inherited-investment contrasts were +0.189 at starting access 0.20, approximately zero at the symmetric state 0.50 and -0.189 at 0.80. The symmetry of these magnitudes follows from the deliberately mirrored design, but the biological inference does not: changing functional composition at constant visitor number can redirect selection.

Duplicating each left-shifted visitor type to create eight visitor entries changed the fixed-state, deterministic and finite-population operators by at most 1.78 × 10^-15 when total activity was fixed. The model therefore distinguishes functional composition from simple visitor-entry count. A recurrent decline in pollinator service is not sufficient to specify a single selection direction unless the functional visitor environment and starting floral state are also specified.

## Directional similarity and historical repeatability separate in finite populations

At depression 0.50 and season 200, the finite ABM mean far-minus-near investment effect was -0.1446 (95% history-bootstrap interval -0.1588 to -0.1306), and all 3,072 near and 3,072 far cases were occupied. Mean-over-eight sign labels were mixed in 12/128 histories at deadband 0, but 97/128 histories showed disagreement among repeat-specific labels. Sign counts alone therefore did not identify a stable history effect.

The exploratory exact-source variance diagnostic showed that a reproducible continuous history signal nevertheless existed. Under the natural visitor histories, history-structured variance was 0.00549 (95% bootstrap interval 0.00405–0.00718) against demographic residual variance 0.02677. One finite trajectory was noisy (ICC 0.170), but the declared eight-repeat mean had reliability 0.621 (0.549–0.681), and independent first-four versus last-four history means correlated at 0.690 (0.592–0.770).

Crucially, the two interventions that nearly eliminated mixed-sign histories changed this continuous history signal in opposite directions. Increasing plant capacity from 48 to 192 reduced mixed histories from 12 to 1 and repeat-label disagreement from 97 to 31, while residual variance fell to 0.01489 and history-structured variance rose to 0.00875. Eight-repeat reliability increased to 0.825 and split-half correlation to 0.852. Pooling visitor histories also reduced mixed histories, from 12 to 0, but history-structured variance fell to 0.00042 while residual variance remained 0.02916; reliability fell to 0.103 and split-half correlation to 0.214. Thus the same increase in directional sign uniformity can accompany either a stronger reproducible historical imprint or its erosion by environmental averaging. This ordering was invariant across all 35 balanced 4-versus-4 splits of the eight demographic repeats: capacity-192 history correlation exceeded natural in 35/35 splits, whereas visitor-pooled correlation was lower in 35/35.

The deterministic closure is retained as a mechanistic comparator rather than a finite-population expectation. At depression 0.50 its endpoint mass remained at capacity, but a high-depression sensitivity crossed a persistence boundary. A prospectively frozen scan from depression 0.50 through 0.74 found no mixed or positive deterministic history among histories whose three starts and both near/far endpoints all retained mass >=1; mixed labels appeared only after sub-individual mass was reached.
## Reproductive assurance preserves trajectories but does not provide a universal reduction mechanism

The focal assurance-by-cost knockout initially produced a plausible route to reduced pollinator-facing investment under low service. At visitor activity 0.05, assurance 0.5 and investment cost 0.5, the total investment gradient was -0.393, deterministic investment change was -0.0726 and the finite-population mean was -0.0721 with full terminal occupancy. Removing assurance or removing investment cost shifted the gradient upward by approximately one gradient unit, while restoring visitor activity to 0.4 moved the gradient to +1.681.

The preregistered robustness surface prevented this route from becoming a universal explanation. At assurance 0.5 and investment cost 0.5, the activity value at which the gradient crossed zero shifted from about 0.182 at inbreeding depression 0.25 to 0.096 at 0.50 and 0.040 at 0.75. Annual inherited responses became positive at high depression, and with adult survival 0.75 the finite-population mean was already positive at depression 0.50 and 0.75. A lifetime-budget-matched perennial sensitivity remained negative, but the declared all-life-history rule failed.

Reproductive assurance is therefore robust here as persistence insurance, not as a universal mechanism forcing one floral endpoint. Retaining this failed headline route is important for the repeatability argument: reproductive context can move the stage at which a shared ecological problem stops producing a shared direction.

## Genetic accessibility selectively erodes trait-level repeatability

When standing genetic variation was reduced on one trait axis, response was selectively attenuated on that axis even though the ecological operator was unchanged. Reducing access standing SD from 0.15 to 0.03 decreased its mean absolute deterministic response by 0.1136 and the finite-population response by 0.0961. Reducing investment standing SD from 0.15 to 0.03 decreased absolute deterministic investment response by 0.1054 and the finite-population response by 0.0830.

The within-environment comparison shows why this matters for syndrome components. Under the left-shifted visitors, equal-high standing variation produced deterministic changes of -0.150 in access and +0.119 in investment. Constraining access reduced access change to -0.0428 while investment remained +0.106. Constraining investment left access at -0.148 while investment fell to +0.0104. Shared selection can therefore produce asynchronous trait responses because ecological selection and genetic accessibility are separate stages.

Mutation narrowed the early accessibility gap. Under the central mutation input, the response ratio between high-standing/no-mutation and low-standing/mutation populations declined from 2.56 at season 400 to 1.49 at season 800. The prospective long-horizon extension showed that this was a difference in response timing rather than persistent dominance: the ratio fell below one by season 1,600 (0.91), then to 0.68 at 3,200 and 0.56 at 6,400. Thus standing variation supplied an early response advantage, whereas continuing mutation eventually caught and overtook the fixed high-standing reference in this model.

The first preregistered mutation–pleiotropy timing test failed: coordinated sustained two-trait crossings were zero in every summarized cell, and the investment-axis crossing statistic was effectively censored at the 400-year horizon. We retained the failure rather than lowering the threshold. It therefore cannot be used as evidence for a general pleiotropic ordering of syndrome components.

## Long-horizon stress testing identifies a persistence boundary, not a stationary syndrome

The prospectively fixed 6,400-season extension is informative primarily as a failure diagnostic. It followed the depression-0.75 deterministic closure, for which the far arm was already overwhelmingly below one expected individual at season 200. The subsequent decay of the far-minus-near density contrast toward zero therefore cannot be interpreted as adaptive convergence or as evidence about a stationary island-syndrome endpoint.

This distinction matters because the original depression-0.50 focal bridge occupies a different population regime: deterministic mass remained at capacity and all finite populations survived to season 200. The long-horizon depression-0.75 trajectory consequently does not invalidate the focal finite-population result, but neither can it establish how that focal response behaves over thousands of seasons.

The separate mutation-accessibility extension remains temporally informative because it directly follows finite populations under fixed visitor environments. There, the early high-standing advantage narrowed, disappeared and reversed as continuing mutation accumulated. Time therefore changes the accessibility ranking in this model, but a long-run syndrome-level repeatability trajectory remains unidentified.

## Finite realization adds contingency downstream of deterministic expectation

The deterministic and finite-population levels share the same biological operator but not the same realized trajectories. Controlled visitor compositions showed that demographic stochasticity was unnecessary for response branching: both deterministic density and finite populations retained mixed signs across the reduction audit. In the broader island campaign, however, chronology, assurance, life history and recovery produced substantial finite-versus-density sign disagreement.

Visitor chronology also retained different inherited endpoints under a common final environment, while visitor connectivity and seed connectivity altered trajectories through biologically distinct routes. Geographic isolation therefore compresses at least two processes: a change in the functional pollination environment and a change in demographic/genetic input. They cannot be assumed to produce the same evolutionary effect.

The stage decomposition is consequently cumulative. State dependence can weaken parallel selection; reproductive context can alter persistence and sign boundaries; genetic accessibility can attenuate selected axes; and finite realization can further separate trajectories through ancestry turnover, extinction and demographic sampling.

## Natural island evidence supports the question but not quantitative transfer

The source-audited island archive contains systems that occupy different pieces of this causal architecture. Izu provides upstream variation in functional matching with divergent downstream pollen and tube responses. Ogasawara provides a more coherent access-to-pollen-to-reproduction example, whereas Hawaii and Puerto Rico–Mona include buffering and Dominica retains a counterdirectional case. Direct-history systems document founding, partner loss or reintroduction.

What the archive does not contain is equally important. No complete same-unit record links a measured visitor transition to inherited longitudinal change and finite-demographic realization across the full causal chain. Existing island comparisons also differ in response scale, exposure definition and independent unit. We therefore do not estimate natural branch prevalence, assign islands to Model 3 cells or interpret synthetic trait magnitudes as natural effect sizes.

# Discussion

## Directional similarity does not identify historical repeatability

The strongest result is not the count of mixed histories. It is the separation between **directional similarity** and **reproducibility of history-specific effect magnitude**. In the natural finite bridge, individual trajectories were noisy, yet averaging the eight declared demographic repeats recovered a reproducible visitor-history signal.

The capacity and pooling interventions expose why this distinction matters. Both made mean history labels almost uniformly negative. Larger plant populations did so while demographic residual variance fell and history reliability increased; visitor-history pooling did so while the reproducible history component collapsed. The same apparent gain in directional similarity therefore arose once because historical effects became clearer relative to demographic noise and once because environmental-history structure was averaged away.

This makes sign uniformity an incomplete diagnostic of evolutionary repeatability. A population set can become more parallel in direction while retaining, strengthening or losing reproducible differences in magnitude. For natural systems, repeated populations should therefore be compared with replicated estimates of effect magnitude, not classified only by whether they move in the same direction.

The temporal accessibility result is distinct: standing variation accelerated early response, but continuing mutation caught and overtook that reference. The high-depression long-horizon density stress test crossed quasi-extinction and cannot identify a persisting long-run syndrome trajectory.
## This differs from treating parallel evolution as a single continuum score

Direction-versus-magnitude measurement is not our novelty. Oke et al. (2017), Venkataram & Kryazhimskiy (2023) and Arendt et al. (2025) already show that repeatability depends on which trajectory property is measured; Arendt et al. further caution that a general direction metric should not simply be equated with geometric parallelism. Bisschop et al. (2026) additionally showed experimentally that environmental and demographic heterogeneity can reduce evolutionary repeatability. Our contribution is narrower and mechanistic: within one operator and endpoint, two interventions produce nearly the same gain in directional sign uniformity while driving reproducible visitor-history structure in opposite directions.

Repeatability is therefore multidimensional rather than one latent score. Direction, continuous magnitude, historical imprint and demographic realization need not rank interventions identically. The deterministic closure also remained directionally uniform throughout the tested viable isolation envelope, so finite history structure cannot be read simply as deterministic branches revealed by sampling.

Many-to-one mapping provides another important precedent. Thompson et al. (2017) showed that common biomechanical function can be associated with less parallel morphology when multiple forms produce similar function. Model 3 does not establish literal many-to-one mapping for real flowers, but it reaches a related general point through a different route: common ecological function can coexist with non-unique phenotype because selection, accessibility and realization are separate filters.

## Pollinator loss and pollinator replacement should not be treated as the same island pressure

The same-count rematching result gives the island framing a mechanistic core. Reduced visitor number and changed visitor identity are often both described as pollination limitation, yet they are not equivalent evolutionary perturbations. In Model 3, composition can redirect selection at identical visitor number, and the sign depends on the starting floral state.

This distinction is especially important on islands, where depauperate communities, functional replacement, invasion and local extinction can all alter pollination. An empirical test of island floral repeatability should therefore measure at least visitor amount, functional composition and effective pollen transfer. Species richness alone cannot identify the relevant selective problem.

## Genetic accessibility predicts asynchronous syndrome components

The standing-variation experiment shows how one ecological transition can produce asynchronous early responses. When only one trait axis had little available variation, the constrained axis initially responded weakly while another trait retained a large response. The long-horizon extension then showed why this should not be recast as a persistent accessibility hierarchy: continuing mutation erased and eventually reversed the early standing-variation advantage.

The empirical prediction is therefore explicitly temporal. Lineages or trait modules that differ in standing variation, mutational target size or genetic covariance may differ most strongly early after a pollination shift, with those rankings changing as new variation accumulates. The standing-variation result is a mechanism for response timing, not a universal ranking of evolvability.

## Failure of the assurance route strengthens rather than weakens the stage argument

A simple story in which pollinator loss favors reproductive assurance and assurance universally reduces pollinator-facing investment would have produced a cleaner syndrome narrative. The prospective robustness test rejected that stronger claim. Its sign boundary moved with inbreeding depression and failed across the declared life-history treatments.

That negative result is informative because it identifies reproductive context as an earlier possible break in repeatability. A shared decline in pollination can generate different selection once the value of selfed versus outcrossed offspring and the life-history budget differ. The model therefore does not need genetic or demographic contingency to explain every departure from parallelism; divergence can begin before those stages.

## Scope and empirical tests

The model is mechanistic but uncalibrated. Traits are abstract, seasons are not geological time and distances are synthetic. A 6,400-season stationary run does not reconstruct island history, and the model cannot predict a named flora, historical Bombus transition, colour or corolla dimension.

Its structural prediction is measurable: natural studies should quantify pollinator amount and composition, reproductive response, inherited change, repeated population-level effect magnitudes, genetic accessibility and demographic history. Such longitudinal data could distinguish directional similarity from reproducible historical differences rather than conditioning only on survivors.

The logic may extend beyond islands, but islands remain useful because recurrent ecological perturbations and an explicit syndrome literature make incomplete repeatability a concrete empirical problem.

# Conclusion

At the occupied 200-season finite-population window, directional sign uniformity and reproducible history-specific magnitude were distinct properties. Increasing plant capacity and pooling visitor histories both made direction more uniform, yet the former increased history reliability while the latter nearly erased it.

The bounded principle is therefore sharper: **greater directional similarity does not uniquely identify greater evolutionary repeatability or its mechanism.** Historical imprint can become more reproducible, less reproducible or temporally reweighted while the aggregate direction looks increasingly parallel. Natural variance components, long-run attractors and route prevalences remain empirical quantities rather than outputs of this uncalibrated model.

# Figure captions

**Figure 1. Repeatability depends on biological level.** The same island-like pollination problem is followed from visitor environment and immediate reproductive selection through conditional deterministic inheritance and finite-population realization. The figure distinguishes aggregate response from history-level realized trajectories and does not treat the deterministic closure as the stochastic mean of the finite ABM.

**Figure 2. Repeatability can fail at the ecological-selection stage.** Same-count functional rematching redirects the investment gradient across starting access states, while duplicating visitor entries at fixed total activity leaves the operator unchanged. The panel separates visitor amount from functional composition and shows why identical losses in visitor number need not imply identical selection.

**Figure 3. The same directional similarity can conceal opposite changes in history signal.** Natural, visitor-pooled and capacity-192 finite bridges are compared using mixed-sign history counts, demographic residual variance, history-structured variance, eight-repeat reliability and split-half history correlation. Pooling and larger capacity both nearly eliminate mixed-sign mean labels, but pooling suppresses reproducible history structure whereas larger capacity strengthens it relative to demographic noise. A small inset marks the deterministic persistence boundary that excludes the high-depression closure from population-level inference.

**Figure 4. Finite realization and empirical claim boundary.** Chronology, pollinator connectivity, seed connectivity, demographic sampling and extinction further diversify inherited endpoints. Source-audited natural island systems confront individual causal layers but do not provide a complete same-unit longitudinal chain; no named island is fitted to a synthetic Model 3 cell.

# Core references for framing

Oke KB, Rolshausen G, LeBlond C, Hendry AP. 2017. How Parallel Is Parallel Evolution? A Comparative Analysis in Fishes. *The American Naturalist* 190:1–16. doi:10.1086/691989.

Venkataram S, Kryazhimskiy S. 2023. Evolutionary repeatability of emergent properties of ecological communities. *Philosophical Transactions of the Royal Society B* 378:20220047. doi:10.1098/rstb.2022.0047.

Arendt JD, Travis J, Reznick DN. 2025. On Measurements of Phenotypic Parallel Evolution. *The American Naturalist* 206:198–205. doi:10.1086/736845.

Bisschop K, et al. 2026. Additive effects of environmental and demographic variation shape the repeatability of evolution across replicated experiments. *Evolution Letters* 10:382–395. doi:10.1093/evlett/qrag017.

Abe T. 2006. Threatened pollination systems in native flora of the Ogasawara (Bonin) Islands. *Annals of Botany* 98:317–334. doi:10.1093/aob/mcl117.

Bolnick DI, Barrett RDH, Oke KB, Rennison DJ, Stuart YE. 2018. (Non)Parallel Evolution. *Annual Review of Ecology, Evolution, and Systematics* 49:303–330. doi:10.1146/annurev-ecolsys-110617-062240.

Ciarle R, Burns KC. 2025. The island syndrome in plants on New Zealand’s outlying islands: a review. *New Zealand Journal of Botany* 63:2300–2324. doi:10.1080/0028825X.2024.2377418.

Hetherington-Rauth MC, Johnson MTJ. 2020. Floral Trait Evolution of Angiosperms on Pacific Islands. *The American Naturalist* 196:87–100. doi:10.1086/709018.

Jezierski MT, Dunn JC, Chagas CRF, Smith WJ. 2026. Parallel evolution of island syndromes coincides with limited parallel genetic differentiation in a passerine bird. *Evolutionary Journal of the Linnean Society* 5:kzag008. doi:10.1093/evolinnean/kzag008.

Stuart YE, Veen T, Weber JN, et al. 2017. Contrasting effects of environment and genetics generate a continuum of parallel evolution. *Nature Ecology & Evolution* 1:0158. doi:10.1038/s41559-017-0158.

Thompson CJ, Ahmed NI, Veen T, Peichel CL, Hendry AP, Bolnick DI, Stuart YE. 2017. Many-to-one form-to-function mapping weakens parallel morphological evolution. *Evolution* 71:2738–2749. doi:10.1111/evo.13357.
