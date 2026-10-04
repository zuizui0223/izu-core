# Directional similarity can mask opposite changes in historical repeatability in a generative island-floral model

**Status:** preferred journal candidate Evolution Letters; Ecology Letters fallback only after ecological recast; separate from the locked Oikos submission surface  
**Updated:** 2026-10-04  
**Inference boundary:** system-uncalibrated Model 3; natural islands are biological confrontation, not fitted targets

## Abstract

Repeated environments can yield similar evolutionary directions without identical trajectories. Islands are useful because pollination shifts recur while proposed plant island-syndrome traits remain heterogeneous.

We examined one Model 3 from reproductive selection to finite-population realization, using 19,968 audited cases and a 24,576-case isolation bridge. A post-hoc continuous reduction gave exact Price closure for additive trait means and an analytic investment threshold. We then froze a rare-mutant extension before execution; including maternal, paternal and selfed transmission, it showed that near-to-far isolation shifted joint selection toward lower floral investment and greater reproductive assurance. A separately frozen finite follow-up produced syndrome-direction endpoints but not alternative endpoint classes.

At inbreeding depression 0.50, finite mean far-minus-near investment was -0.1446 with complete occupancy. Exploratory reanalysis found that greater plant capacity and visitor-history pooling both increased sign uniformity but moved reproducible history structure oppositely. Prospective validation with new demographic seeds reproduced the predicted ranking. A second frozen validation used entirely new synthetic visitor histories (75001–75128). Across 9,216 trajectories, four-repeat reliability was 0.722 at capacity 192, 0.417 under natural demography and 0.154 after pooling; paired bootstrap intervals for capacity minus natural (+0.222 to +0.375) and pooled minus natural (-0.379 to -0.154) excluded zero. All arms remained occupied. A high-depression deterministic sensitivity entered quasi-extinction and was excluded from persisting-population inference.

Thus directional sign uniformity does not uniquely identify evolutionary repeatability or mechanism. The same increase in parallelism can accompany either a more reproducible historical imprint or its erosion by environmental averaging.

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

## Continuous reduction, Price closure and joint selection

This post-hoc theoretical reduction explains frozen results; it was not part of the original prospective campaign. The exact continuous counterpart retains a nonlocal maternal × paternal inheritance integral and is not a PDE. With mutation, immigration and survival set to zero, additive means obey `mean(z)'=mean(z)+Cov(z,w)/mean(w)`, where `w` is total parental-genome contribution. Investment selection is the fixed-resident derivative of rare-mutant parental-genome contribution, written B(i)-C(i). Both maternal and paternal outcross success and viable selfed transmission contribute. A previous whole-population derivative was corrected because it changes the resident environment and can reverse the invasion-gradient sign (Supporting Information).

Because assurance also changes paternal transmission, we had frozen a rare-mutant decision contract before execution, using `w_mut=0.5F_mut+0.5P_mut+S_mut` in a fixed resident environment. Delayed selfing was a structural control; prior selfing, pollen discounting and assurance cost supplied trade-offs. Shift and sign reversal were adjudicated separately, and a second frozen contract governed the finite follow-up. Derivations and decision rules are in Supporting Information.


## Standing variation and mutation

Prospective standing-variation experiments reduced founder variation on either the access or investment axis while holding the visitor environment, reproduction, inheritance and mutation rate fixed. This asks whether a selected response remains reachable when one trait axis begins with little selectable variation.

A later mutation-input analysis normalized de novo mutation to the founder additive-variance proxy because Model 3 contains no environmental variance and therefore does not identify literal mutational heritability. Low-standing populations were compared with a high-standing reference at years 400 and 800. Claims are restricted to the tested finite horizon.

A preregistered mutation–pleiotropy timing experiment failed its success criteria. Thresholds were not lowered and the horizon was not extended after inspection; the failed route remains part of the evidence.

## Prospective long-horizon diagnostic

A prospectively frozen 200–6,400-season extension tested temporal stability without outcome-dependent stopping. Because these stationary synthetic environments omit succession, coevolution and calibrated natural mutation rates, we treat the extension only as a persistence and accessibility stress test.

## Finite realization and natural confrontation

Finite-population simulations retain the same reproductive and inheritance operator but add demographic sampling, survival, extinction, immigration and ancestry turnover. Chronology and connectivity interventions distinguish visitor-history effects from demographic/genetic input.

Because sign labels were repeat-sensitive, we conducted a post-hoc exact-source decomposition of the original 3 starts × 128 histories × 8 repeats tensor, treating start as fixed, history and start×history as random and repeat as residual. We report history-structured variance, single-trajectory ICC, eight-repeat reliability and split-half history correlation.

Before further simulation, we froze two validations. First, the same histories were rerun with new demographic seeds 201–204 (9,216 arm trajectories); strong success required the predicted capacity 192 > natural > visitor-pooled discovery-to-validation correlation ordering and paired bootstrap intervals excluding zero in the predicted directions. Second, visitor histories were replaced wholesale (74001–74128 → 75001–75128) with demographic seeds 301–304 (another 9,216 trajectories). Here strong success required the same ordering in four-repeat reliability, paired intervals excluding zero and >=0.95 occupancy in every arm. No seeds, thresholds or stopping rules were changed after execution began.

Natural island systems are used only for source-audited biological confrontation. They are not assigned to synthetic parameter cells, and cross-sectional island contrasts are not treated as measured historical trajectories.

# Results

## Functional repeatability already depends on ecological state

The immediate selection assay did not yield one universal floral response. Under each four-type visitor composition, fixed-state investment gradients included both positive and negative values across starting access states. Under the left-shifted composition, for example, the gradient was +1.5048 at starting access 0.20 but -0.8720 at 0.80; the direction reversed under the right-shifted composition.

Functional replacement mattered even when visitor number was unchanged. The maximum left-versus-right difference in the fixed-state gradient was 2.3768. Deterministic inherited-investment contrasts were +0.189 at starting access 0.20, approximately zero at the symmetric state 0.50 and -0.189 at 0.80. The symmetry of these magnitudes follows from the deliberately mirrored design, but the biological inference does not: changing functional composition at constant visitor number can redirect selection.

Duplicating each left-shifted visitor type to create eight visitor entries changed the fixed-state, deterministic and finite-population operators by at most 1.78 × 10^-15 when total activity was fixed. The model therefore distinguishes functional composition from simple visitor-entry count. A recurrent decline in pollinator service is not sufficient to specify a single selection direction unless the functional visitor environment and starting floral state are also specified.

## The directional backbone survives phenotype reduction

The Price update matched exact next-generation mean investment in all 25 controlled cells. The reduced replicator equation retained all 25 directions over 60 seasons (mean absolute error 0.00434) and all 9 frozen bridge signs; condition means correlated 0.987 with exact density effects, with slope 0.586.

Across five access × three investment states, all 128 natural near–far histories shifted `B(i)-C(i)` toward lower investment. Pooling strengthened the shift; response-blind richness matching removed the universal negative shift, leaving mixed signs and small mean differences. The direction therefore arises from visitor-mediated marginal return, not an imposed island optimum.

## The same visitor histories rotate joint floral–assurance selection

Across 45 resident states × 128 histories, all four assurance settings passed the frozen joint-shift criterion: selection moved toward lower investment and greater assurance in >=127/128 histories. At the central state, far-minus-near shifts were (-0.537,+0.788) in the structural delayed-selfing control, (-0.398,+0.703) under prior selfing, (-0.428,+0.769) with pollen discounting and (-0.537,+0.689) with assurance cost. Thus the joint shift itself was not trade-off specific. Mixed investment–assurance curvature was negative throughout.

The multivariate Price identity matched all three next-generation means in 48/48 cells (maximum error 7.2 × 10^-16). Full-covariance `G beta` passed 46/48 strict gates (not complete response fidelity), with mean cosine 0.9995 and lower error than diagonal `G` in 48/48.

The result was directional, not bistable. Maximum syndrome-endpoint frequencies were 16.4% in the structural delayed-selfing control, 10.2% under prior selfing, 21.3% with pollen discounting and 43.0% with assurance cost; the opposite endpoint stayed below 3%. Endpoint occurrence alone therefore did not diagnose a trade-off effect: prior selfing was below the control and pollen discounting only modestly above it, whereas assurance cost produced the marked increase. The frozen follow-up branching criterion failed.

## Directional similarity and historical repeatability separate in finite populations

At depression 0.50 and season 200, the finite ABM mean far-minus-near investment effect was -0.1446 (95% history-bootstrap interval -0.1588 to -0.1306), and all 3,072 near and 3,072 far cases were occupied. Mean-over-eight sign labels were mixed in 12/128 histories at deadband 0, but 97/128 histories showed disagreement among repeat-specific labels. Sign counts alone therefore did not identify a stable history effect.

The exploratory exact-source variance diagnostic showed that a reproducible continuous history signal nevertheless existed. Under the natural visitor histories, history-structured variance was 0.00549 (95% bootstrap interval 0.00405–0.00718) against demographic residual variance 0.02677. One finite trajectory was noisy (ICC 0.170), but the declared eight-repeat mean had reliability 0.621 (0.549–0.681), and independent first-four versus last-four history means correlated at 0.690 (0.592–0.770).

Crucially, the two interventions that nearly eliminated mixed-sign histories changed this continuous history signal in opposite directions. Increasing plant capacity from 48 to 192 reduced mixed histories from 12 to 1 while eight-repeat reliability increased from 0.621 to 0.825. Pooling visitor histories reduced mixed histories from 12 to 0 while reliability fell to 0.103. This ordering was invariant across all 35 balanced 4-versus-4 splits of the discovery repeats.

The prospectively frozen new-seed validation met its strong-success rule. Discovery-to-validation history correlations were 0.918 (95% bootstrap interval 0.893–0.941) for capacity 192, 0.732 (0.633–0.805) under natural demography and 0.165 (0.008–0.326) after visitor pooling. The paired correlation difference was +0.186 for capacity minus natural (0.120–0.283) and -0.567 for pooled minus natural (-0.732 to -0.401). All 9,216 validation trajectories remained occupied. Mean sign labels under the new seeds were still much more uniform for pooled and large-capacity histories (1 and 4 mixed histories at epsilon 0) than under natural demography (23 mixed, with two positive-only). Thus the same increase in directional sign uniformity can accompany either strong preservation of history-specific magnitude across new demographic realizations or near-erasure of that history ranking.

The independent visitor-history validation also met its frozen strong-success rule. With entirely new history seeds 75001–75128, four-repeat history reliability was 0.722 (0.661–0.766) for capacity 192, 0.417 (0.334–0.493) under natural demography and 0.154 (0.071–0.226) after visitor pooling. The paired reliability difference was +0.305 for capacity minus natural (0.222–0.375) and -0.263 for pooled minus natural (-0.379 to -0.154). The same ordering held in all three predeclared balanced 2-versus-2 split-half checks: capacity correlations were 0.799–0.818, natural 0.447–0.535 and pooled 0.069–0.205. All six arms had 100% terminal occupancy. Directional labels again became more uniform under both interventions: at epsilon 0, mixed histories were 19/128 under natural demography, 2/128 after visitor pooling and 1/128 at capacity 192. Thus the opposite history-reliability ordering transfers to new stochastic visitor histories generated independently from the same frozen ecological process. A post-hoc secondary paired bootstrap of the predeclared variance endpoint showed that this was not only a consequence of reliability normalization: absolute history-structured variance increased by 0.00411 under capacity 192 relative to natural demography (95% interval 0.00194–0.00595) and decreased by 0.00348 after visitor-history pooling (-0.00539 to -0.00187).

The deterministic closure is retained as a mechanistic comparator rather than a finite-population expectation. At depression 0.50 its endpoint mass remained at capacity, but a high-depression sensitivity crossed a persistence boundary. A prospectively frozen scan from depression 0.50 through 0.74 found no mixed or positive deterministic history among histories whose three starts and both near/far endpoints all retained mass >=1; mixed labels appeared only after sub-individual mass was reached.
## Reproductive assurance preserves trajectories but does not provide a universal reduction mechanism

The assurance-by-cost knockout produced reduced investment under one focal low-service condition, but the preregistered robustness surface rejected it as a universal route. With assurance 0.5 and investment cost 0.5, the activity crossing moved from ~0.182 at inbreeding depression 0.25 to ~0.096 at 0.50 and ~0.040 at 0.75. Annual and some perennial inherited responses changed sign, so the declared all-life-history rule failed.

Reproductive assurance therefore remains persistence insurance and a context-dependent modifier rather than a mechanism forcing one floral endpoint. This failed headline route is retained because reproductive context can determine where a shared ecological problem first loses a shared direction.

## Genetic accessibility selectively erodes trait-level repeatability

Reducing standing variation on one trait axis selectively attenuated that axis while leaving the ecological operator unchanged. Lowering access SD from 0.15 to 0.03 reduced mean absolute deterministic and finite responses by 0.1136 and 0.0961; the corresponding investment reductions were 0.1054 and 0.0830. Under left-shifted visitors, constraining access left most investment response intact, whereas constraining investment nearly removed its response. Shared selection can therefore produce asynchronous syndrome components.

Mutation made this accessibility ranking temporary: the high-standing/no-mutation to low-standing/mutation response ratio fell from 2.56 at season 400 to 1.49 at 800 and below one by 1,600. The preregistered mutation–pleiotropy timing route failed its success criteria and was not rescued by changing thresholds.

## Long-horizon stress testing identifies a persistence boundary, not a stationary syndrome

The 6,400-season high-depression extension began after the far deterministic closure had already entered a sub-individual regime, so its later decay cannot identify adaptive convergence or a stationary syndrome. By contrast, the focal depression-0.50 bridge remained at capacity in density and fully occupied in finite populations. The separate mutation-accessibility extension showed only that early standing-variation advantages can reverse with time; long-run syndrome repeatability remains unidentified.

## Finite realization and deterministic closure differ

Demographic stochasticity was not required for response branching, because controlled deterministic and finite runs both retained mixed directions. It nevertheless altered realized trajectories: chronology, life history, recovery and connectivity produced finite-versus-density disagreements, and common final visitor environments could retain different inherited endpoints after different histories. Isolation therefore combines changes in functional pollination with changes in demographic and genetic input, so each stage can add a distinct source of non-repeatability.

## Natural island evidence supports the question but not quantitative transfer

The source-audited archive contains island systems illustrating functional replacement, buffering, counterdirectional responses and direct histories, but no same-unit record spans the full visitor-to-inheritance-to-demography chain. We therefore use natural systems to motivate and confront mechanisms, not to estimate branch prevalence, map named islands onto Model 3 cells or transfer synthetic effect sizes.

# Discussion

## Directional similarity does not identify historical repeatability

The strongest result is the separation between **directional similarity** and **reproducibility of history-specific effect magnitude**. The exploratory contrast was recovered prospectively both under new demographic stochasticity and across new synthetic visitor histories.

Both interventions made direction more uniform, but by opposite routes. Larger populations reduced demographic residual variance while history reliability increased; visitor-history pooling largely erased the reproducible history component. Sign uniformity is therefore incomplete as a repeatability diagnostic. The out-of-history validation remains within the same frozen history generator, not a different ecological process or natural islands. Natural tests should pair directional responses with replicated effect-magnitude estimates.

The temporal accessibility result is distinct: standing variation accelerated early response, but continuing mutation caught and overtook that reference. The high-depression long-horizon density stress test crossed quasi-extinction and cannot identify a persisting long-run syndrome trajectory.
## This differs from treating parallel evolution as a single continuum score

Direction-versus-magnitude measurement is not our novelty (Oke et al. 2017; Venkataram & Kryazhimskiy 2023; Arendt et al. 2025). Arendt et al. further caution that a general direction metric should not simply be equated with geometric parallelism; Bisschop et al. (2026) show that environmental and demographic heterogeneity can reduce evolutionary repeatability. Our narrower contribution is mechanistic: within one operator, interventions that similarly increase sign uniformity drive reproducible visitor-history structure in opposite directions.

The phenotype reduction sharpens this distinction. The full-history comparison uses a discrete phenotype map; the continuous-time check is a controlled D=0 replicator ODE. The one-generation additive mean satisfies the Price identity, but this does not close multigeneration phenotype dynamics. Identical phenotype distributions with different genotypes produce different offspring variances (Supporting Information). History reliability is not a second-moment statistic, but a compact directional law need not close the higher-order inheritance structure shaping effect magnitude. This complements many-to-one precedents in which common function coexists with nonparallel form (Thompson et al. 2017).

## Pollinator loss and pollinator replacement should not be treated as the same island pressure

The same-count rematching result gives the island framing a mechanistic core. Reduced visitor number and changed visitor identity are often both described as pollination limitation, yet they are not equivalent evolutionary perturbations. In Model 3, composition can redirect selection at identical visitor number, and the sign depends on the starting floral state.

This distinction is especially important on islands, where depauperate communities, functional replacement, invasion and local extinction can all alter pollination. An empirical test of island floral repeatability should therefore measure at least visitor amount, functional composition and effective pollen transfer. Species richness alone cannot identify the relevant selective problem.

## Genetic accessibility predicts asynchronous syndrome components

Standing variation altered early response asymmetrically across trait axes, but continuing mutation erased and eventually reversed that early advantage. The prediction is therefore temporal: differences in standing variation, mutational target size or genetic covariance should matter most early after a pollination shift, not define a permanent hierarchy of evolvability.

## Joint selection gives the directional result a mechanistic boundary

The corrected investment threshold links selection to female and male reproductive returns and ovule cost in a fixed resident environment. Earlier activity crossings in the assurance-by-cost experiment remain numerical observations; the retired whole-population derivative does not establish their invasion mechanism. The rare-mutant analysis and full-covariance calculation connect reproductive accounting to one-generation response, with two failed near-zero component signs retained.

These ingredients are not new selfing theory; automatic transmission, selfing timing, pollen discounting, pollen-limitation thresholds and floral-display/mating-system coupling have substantial precedent (Lloyd 1979; Lande & Schemske 1985; Porcher & Lande 2005; Harder & Aizen 2010; Goodwillie et al. 2010). The contribution is their connection within one visitor-transfer operator. With fixed inbreeding depression and no purging feedback, Model 3 supports a syndrome-directed shift but not common alternative selfing/outcrossing endpoints.

## Scope and empirical tests

The model is mechanistic but uncalibrated: traits, distances and seasons are abstract. Natural tests should measure visitor amount and composition, reproductive response, inherited change, repeated effect magnitudes, genetic accessibility and demographic history rather than map named islands directly onto synthetic cells.

# Conclusion

At the occupied 200-season finite-population window, directional sign uniformity and reproducible history-specific magnitude were distinct properties. A post-hoc discovery predicted that capacity scaling would preserve history structure more strongly than natural demography while visitor-history pooling would erase it. Prospectively frozen validation reproduced that ordering first across new demographic realizations and then across entirely new synthetic visitor histories, with both paired contrasts excluding zero in both validation stages.

The bounded principle is therefore sharper: **greater directional similarity does not uniquely identify greater evolutionary repeatability or its mechanism.** In Model 3, additive trait means have an exact Price closure, floral investment has a marginal pollination-benefit versus investment-cost threshold, and the same visitor histories rotate rare-mutant selection jointly toward lower investment and greater assurance. Yet exact sexual inheritance remains nonlocal, higher-order structure does not close in the same way, and the finite joint follow-up did not produce two common alternative endpoint classes. Historical imprint can therefore become more reproducible, less reproducible or temporally reweighted while the aggregate direction looks increasingly parallel. Natural variance components, long-run attractors and route prevalences remain empirical quantities rather than outputs of this uncalibrated model.

# Figure captions

**Figure 1. Repeatability depends on biological level.** The same island-like pollination problem is followed from visitor environment and immediate reproductive selection through conditional deterministic inheritance and finite-population realization. The figure distinguishes aggregate response from history-level realized trajectories and does not treat the deterministic closure as the stochastic mean of the finite ABM.

**Figure 2. Repeatability can fail at the ecological-selection stage.** Same-count functional rematching redirects the investment gradient across starting access states, while duplicating visitor entries at fixed total activity leaves the operator unchanged. The panel separates visitor amount from functional composition and shows why identical losses in visitor number need not imply identical selection.

**Figure 3. The same directional similarity can conceal opposite persistence of history signal.** The main panel uses the prospectively frozen independent visitor-history validation. Capacity 192 and visitor pooling both produce highly uniform directional labels, but four-repeat history reliability is high for capacity 192, intermediate under natural demography and weak after visitor pooling. Validation-only history-structured and demographic residual variances show the same mechanistic contrast. The exploratory discovery and same-history new-demography validation are retained as the hypothesis-generation and first-validation layers.

**Figure 4. Finite realization and empirical claim boundary.** Chronology changes realized inherited endpoints, while reproductive assurance determines whether some trajectories remain observable at all. Source-audited natural island systems show propagation, branching, buffering and counterdirectional responses across model layers, but they do not provide a complete same-unit longitudinal A→B→C chain; no named island is fitted to a synthetic Model 3 cell.

# Data and code availability

Code, frozen design contracts, committed result summaries, validation receipts and figure generators are available in the public repository `zuizui0223/izu-core`. The validated scientific theory revision is `cfa0754823817591fab15ef1b36eecd7a3a3ef10`. A persistent archive identifier will replace the GitHub-only locator in the final publication package.

# Author contributions

**REQUIRES AUTHOR INPUT.** Insert final CRediT roles before submission.

# Funding

**REQUIRES AUTHOR INPUT.**

# Conflict of interest

**REQUIRES AUTHOR CONFIRMATION.**

# Acknowledgements

**REQUIRES AUTHOR INPUT if applicable.** Include any journal-required AI-use disclosure only after the author confirms its exact scope.

# Core references for framing

Price G. 1970. Selection and Covariance. *Nature* 227:520–521. doi:10.1038/227520a0.

Lloyd DG. 1979. Some reproductive factors affecting the selection of self-fertilization in plants. *The American Naturalist* 113:67–79. doi:10.1086/283365.

Porcher E, Lande R. 2005. The evolution of self-fertilization and inbreeding depression under pollen discounting and pollen limitation. *Journal of Evolutionary Biology* 18:497–508. doi:10.1111/j.1420-9101.2005.00905.x.

Lande R, Schemske DW. 1985. The evolution of self-fertilization and inbreeding depression in plants. I. Genetic models. *Evolution* 39:24–40. doi:10.1111/j.1558-5646.1985.tb04077.x.

Harder LD, Wilson WG. 1998. A clarification of pollen discounting and its joint effects with inbreeding depression on mating system evolution. *The American Naturalist* 152:684–695. doi:10.1086/286199.

Goodwillie C, Sargent RD, Eckert CG, et al. 2010. Correlated evolution of mating system and floral display traits in flowering plants and its implications for the distribution of mating system variation. *New Phytologist* 185:311–321. doi:10.1111/j.1469-8137.2009.03043.x.

Harder LD, Aizen MA. 2010. Floral adaptation and diversification under pollen limitation. *Philosophical Transactions of the Royal Society B* 365:529–543. doi:10.1098/rstb.2009.0226.

Teixido AL, Aizen MA. 2019. Reproductive assurance weakens pollinator-mediated selection on flower size in an annual mixed-mating species. *Annals of Botany* 123:1067–1077. doi:10.1093/aob/mcz014.

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
