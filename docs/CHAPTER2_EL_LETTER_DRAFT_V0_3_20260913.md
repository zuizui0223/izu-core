# Effective independence alone does not determine nonlinear ecological response

**Article type:** Letter  
**Target:** Ecology Letters  
**Running title:** Nonlinear effective independence  
**Working abstract words:** 113  
**Working main-text words:** 2449  
**Figures:** 4  
**References:** 9

## Abstract

Ecological aggregation suppresses realization variance when pooled units are independent, motivating variance-equivalent measures of effective independence. In a solvable bilinear model, aggregation and synchrony collapse exactly onto one coordinate, fixing the interaction-to-community variance ratio. Two nonlinear ecological response models break that reduction: community–interaction ordering reverses and interaction variance can dominate at intermediate aggregation. Along an exact equal-effective-independence contour, the full state/community/interaction decomposition changes substantially while realized support increases, and the mismatch persists under an identity-preserving correlation mechanism. Effective independence is therefore a variance-equivalent coordinate, not a sufficient descriptor of nonlinear ecological response. Aggregation and synchrony can act through different response geometry and should be treated as distinct ecological context axes.

**Keywords:** aggregation; community context; consumer–resource dynamics; effective independence; interaction variance; nonlinear averaging; plant–pollinator interactions; stochastic synchrony

## Introduction

Ecologists average across individuals, populations, species and repeated community realizations to reduce stochastic variation. If realizations are sufficiently independent, increasing the number of pooled units suppresses realization variance and makes persistent differences among focal states easier to detect. The same logic underlies portfolio effects and community stability. Yet ecological units are rarely independent: shared environmental forcing, dispersal and trophic coupling synchronize dynamics across space and time (Liebhold et al. 2004; Loreau & de Mazancourt 2008). Scaling analyses of geographically subdivided populations already recognized that spatial synchrony can reduce the effective number of independently fluctuating subpopulations (Keitt et al. 2002).

For exchangeable variables, a natural variance-equivalent compression combines nominal unit number `k` and common pairwise correlation `rho`. The variance of their mean is proportional to `rho + (1-rho)/k`, which equals the variance of `k_eff = k/[1+(k-1)rho]` independent units. This compression is exact for the variance of a mean. The ecological question is whether the same one-dimensional coordinate also determines the response of a nonlinear system.

Many ecological response functions are nonlinear. Functional responses saturate (Holling 1959), organisms adjust phenotypically or behaviourally across response surfaces, and interaction outcomes vary with biotic and abiotic context (Chamberlain et al. 2014). Jensen's inequality gives the simplest warning that a nonlinear response can distinguish distributions sharing the same mean (Ruel & Ayres 1999). Recent metacommunity theory likewise shows that spatial aggregation of temporally stochastic dispersal can alter synchrony and stability jointly rather than acting as a simple rescaling of connectivity (Townsend et al. 2025). These precedents motivate, rather than answer, our question: if two pooled systems have exactly the same variance-equivalent effective independence, must a nonlinear ecological response decompose in the same way?

We partition response variation into a persistent focal-state component `S`, a community-realization component `C`, and a state-by-community interaction component `I`. We first solve an exact bilinear model, in which `k_eff` is a sufficient coordinate for this decomposition. We then challenge that reduction in a plant–pollinator response model with active state adjustment and in a structurally separate adaptive consumer–resource response with Holling-II saturation. Finally, we compare exact equal-`k_eff` contours and use a second, identity-preserving correlation construction to test whether the failure depends on whole-trajectory sharing.

Our central result is not that averaging can reorder ecological determinants. That follows readily when one variance component shrinks and another persists. Instead, we show that the route of reordering can itself be nonlinear: equal variance-equivalent independence need not imply equal response geometry.

## Materials and methods

### Variance decomposition

For responses `Y_ir`, indexed by focal state `i` and stochastic realization `r`, we used the exact two-way sum-of-squares decomposition

`SS_tot = SS_S + SS_C + SS_I`,

where `SS_S` is the additive focal-state component, `SS_C` is the additive community-realization component, and `SS_I` is the state-by-community non-additive remainder. We report normalized shares

`S = SS_S/SS_tot`, `C = SS_C/SS_tot`, and `I = SS_I/SS_tot`.

These are variance components of the response matrix, not fitted causal coefficients. A label such as CIS orders the three shares from largest to smallest.

### Exact bilinear baseline

Let `X` be a centered focal-state variable and `Zbar_k` the average of `k` exchangeable community variables with variance `sigma^2` and pairwise correlation `rho`. For

`Y_k = aX + b Zbar_k + c X Zbar_k`,

define

`tau_k = Var(Zbar_k) = sigma^2[rho + (1-rho)/k]`.

For centered independent `X` and `Zbar_k`,

`S_k = a^2 Var(X)`,  
`C_k = b^2 tau_k`,  
`I_k = c^2 Var(X) tau_k`.

Hence

`I_k/C_k = c^2 Var(X)/b^2`,

independent of both `k` and `rho`. Because `tau_k = sigma^2/k_eff`, where

`k_eff = k/[1+(k-1)rho]`,

the full bilinear decomposition is determined by `k_eff`. The relative order of `C` and `I` cannot reverse as aggregation or synchrony changes. The constant `S` component can still cross `C` and `I` separately, so a three-region rank trajectory is possible; a `C/I` reversal is the stronger violation.

For a smooth nonlinear response `Y=f(X,Zbar_k)`, first-order expansion around the mean community state gives `C_k=A_C tau_k+O(tau_k^2)` and `I_k=A_I tau_k+O(tau_k^2)`. Thus `I/C -> A_I/A_C` as `tau_k -> 0`. This is an asymptotic leading-order result, not an exact finite-`k` invariant outside the bilinear case.

### Nonlinear plant–pollinator system

The first nonlinear system was a frozen plant–pollinator response model developed independently for a separate ecological analysis. Plant starting state was evaluated on a 21-point standardized trait grid. Pollinator communities were stochastic sets of partner identities with trait positions, interaction breadths, arrival and loss dynamics and partner-specific effectiveness. Plant service was a saturating function of mean trait matching within the realized community. When service fell below a fixed threshold, plant state adjusted incrementally toward the best-matching current partner.

We pooled `k={1,2,4,8,16}` independent community trajectories. For each `k`, 96 realizations were generated for each of six pre-existing seeds, and the state-by-realization matrices were decomposed into `S`, `C` and `I`. The seed ensemble and adjustment operator predated the present analysis.

### Structurally separate nonlinear consumer–resource system

To examine whether the intermediate interaction phase was specific to the pollination mechanism, we constructed an exploratory adaptive consumer–resource response after observing the original pattern. Resource traits followed `Beta(2,2)`. A consumer with state `X` assigned Gaussian trait-dependent attack weights to realized resources, adjusted toward their weighted trait centroid, and then received a Holling-II saturating intake response.

We evaluated the complete 54-setting Cartesian grid of resource count per copy (2, 4), matching width (0.12, 0.18, 0.25), handling (1, 2, 4) and adaptation rate (0.05, 0.15, 0.30), across `k={1,2,4,8,16}`, the same six seeds and 256 realizations per seed. Because this response class was constructed post hoc, it is a structural generalization diagnostic rather than a preregistered confirmation.

### Equal-`k_eff` phase challenge

To create an exact pairwise copy correlation, each of `k` pooled trajectories used one common trajectory with probability `q=sqrt(rho)` and otherwise used an independently generated trajectory from the same marginal process. Two copies share the common trajectory with probability `q^2=rho`, giving pairwise correlation `rho` for any scalar trajectory-level statistic under this mixture.

This construction separates variance-equivalent independence from realized support. The expected number of distinct trajectories is

`D(k,rho) = k(1-sqrt(rho)) + 1 - (1-sqrt(rho))^k`

for `rho>0`, with `D(k,0)=k`.

We evaluated a two-dimensional grid with `k={1,2,4,8,16}`, `rho={0,0.1,0.25,0.5,0.75,0.9}`, six seeds and 48 realizations per seed, plus exact equal-`k_eff` contours. The primary contour fixed `k_eff=2` at `(k,rho)=(2,0),(4,1/3),(8,3/7),(16,7/15)`; a second contour fixed `k_eff=4`.

The phase-map analysis was documented after the original nonlinear pattern was known. Its initially documented display criterion asked whether median determinant order changed along an equal-`k_eff` contour. Because the independent `k_eff=2` endpoint lay near a `C/I` tie, manuscript inference does not rely on that categorical switch alone. We also report the continuous `S/C/I` decomposition along the same exact contour. This additional diagnostic is post hoc and is derived from the frozen phase-map output without new simulation.

### Identity-preserving correlation robustness

Whole-trajectory sharing directly changes identity support, so we also used a second correlation mechanism. Pollinator identities and trait draws remained independent among copies; only arrival and loss events shared Gaussian common shocks. Pairwise correlation was estimated from realized final pollinator counts and converted to a count-variance-equivalent `k_eff`.

We evaluated `k=16` at four latent shared-event correlation levels, using six seeds, 32 response realizations per seed and 400 realizations for count-correlation calibration. This analysis asks whether near-equal variance-equivalent independence recovers the same response decomposition when identities remain independently generated.

## Results

### Bilinear theory fixes community–interaction ordering

In the bilinear system, `C_k` and `I_k` share the same multiplicative factor `tau_k`; their ratio is invariant to aggregation and synchrony, whereas `S_k` is constant. Aggregation can therefore make `S` overtake realization-driven components but cannot reverse `C` and `I`. The first-order smooth extension imposes the same restriction asymptotically.

### The plant–pollinator system crosses the C/I boundary

Median component shares across the six frozen seeds changed from `(S,C,I)=(0.026,0.730,0.247)` at `k=1`, through `(0.273,0.235,0.495)` at `k=4`, to `(0.558,0.127,0.320)` at `k=16`. Median orders over `k=1,2,4,8,16` were CIS, CIS, ISC, SIC and SIC. `I/C` increased from 0.34 to 2.52, reversing the small-system `C>I` ordering.

Interaction variance therefore became largest at intermediate aggregation. This phase cannot be explained solely by a persistent `O(1)` state component overtaking realization variance: the two realization-linked components themselves separate.

### A second nonlinear class reproduces the intermediate phase

Across the 54-setting adaptive consumer–resource grid and six seeds, 255/324 setting-by-seed trajectories contained an interaction-dominated intermediate scale. A `C/I` reversal occurred in 111/324 trajectories, and 68/324 showed a C-dominated small-system regime, an I-dominated intermediate regime and an S-dominated large-system regime.

At the setting level, an intermediate I winner appeared in at least four of six seeds for 42/54 settings, a `C/I` reversal for 18/54, and the complete C-to-I-to-S winner sequence for 10/54, including 9/54 in all six seeds. This does not establish universality, but it rejects the interpretation that the intermediate interaction phase is peculiar to one plant–pollinator parameterization.

### Exact equal effective independence does not preserve the decomposition

Along the exact `k_eff=2` contour, the median decomposition changed from `(S,C,I)=(0.109,0.437,0.434)` at `(k,rho)=(2,0)` to `(0.120,0.358,0.520)`, `(0.165,0.296,0.538)` and `(0.178,0.287,0.521)` as nominal aggregation increased to `k=4,8,16` with compensating correlation.

The first point is close to a `C/I` tie, so the categorical median switch from CIS to ICS is not the primary evidence. The continuous decomposition changes by an L1 distance of 0.307 between the first and last points: `S` rises by 0.069, `C` falls by 0.150 and `I` rises by 0.087. The `I-C` margin moves from -0.003 to +0.234. At `k=8` and `k=16`, all six seeds were ICS. Meanwhile, expected distinct trajectory support increased from 2.00 to 2.66, 3.76 and 6.07 although `k_eff` remained exactly 2.

The exact `k_eff=4` contour retained median order ISC across its evaluated points. Thus `k_eff` remains informative about part of the response surface, but it does not uniquely determine the nonlinear decomposition.

### The mismatch persists with independent identities

Under the identity-preserving shared-event construction, correlated `k=16` communities with realized-count `k_eff≈3.90` remained SIC in all six seeds, whereas frozen independent `k=4` was ISC. At realized-count `k_eff≈2.33`, correlated `k=16` again remained SIC in all six seeds, whereas independent `k=2` was CIS.

`I/C` also varied under this correlation implementation. We therefore use `I/C` as a diagnostic of departure from the exact bilinear reduction, not as a universal nonlinear invariant.

## Discussion

Averaging stochastic ecological units does more than reduce variance when the response operator is nonlinear. In the exact bilinear system, aggregation size and synchrony are interchangeable after compression to `k_eff`: once pooled variance is known, the full `S/C/I` decomposition follows. The nonlinear systems break this equivalence. Equal variance-equivalent independence can correspond to different realized supports and different response decompositions.

This distinction separates the result from a law-of-large-numbers argument. Declining realization variance under independent averaging is expected, as is a crossover with a persistent state component. The nontrivial result is that community and state-by-community variance need not contract together. In both nonlinear response classes their relative ordering changed over finite aggregation scales, and interaction variance became transiently dominant.

The mechanism extends a familiar lesson from nonlinear averaging. Jensen's inequality shows that nonlinear responses can distinguish distributions sharing the same mean (Ruel & Ayres 1999). Here, equal variance-equivalent independence also fails to identify the response decomposition because pooled communities can differ in support, higher-order composition or identity geometry. Adaptation, matching and saturation can act on those differences.

Synchrony is therefore not merely a correction to nominal replication. Shared environmental forcing, dispersal and trophic coupling generate ecological synchrony (Liebhold et al. 2004), and synchrony is central to aggregate community stability (Loreau & de Mazancourt 2008; de Mazancourt et al. 2013). In 20 Mallorca plant–pollinator communities, pollinator synchrony ranged from 0.11 to 0.67 and interaction synchrony from 0.04 to 0.33 (Lázaro et al. 2022). These empirical measures are not numerically equivalent to the exchangeable `rho` used here, but they show that shared temporal structure is neither absent nor constant in a natural interaction network.

The result also refines ecological context dependence. Interaction outcomes vary in sign and magnitude across biotic and abiotic contexts (Chamberlain et al. 2014). Our models show that context can additionally change the identity of the dominant variance source. A system may be realization-dominated at small aggregation, interaction-dominated at intermediate aggregation and state-dominated at larger aggregation. A single global hierarchy of “important drivers” can therefore be misleading even when each component is measured correctly.

For study design, aggregation or support breadth and synchrony or shared stochasticity should be retained as separate axes whenever nonlinear response is plausible. Increasing the number or breadth of realized partners is not equivalent to obtaining the same variance reduction by lowering shared stochasticity. A one-dimensional effective-independence correction may remain useful for variance accounting without being an ecological state descriptor.

Several boundaries are essential. The second nonlinear response class, equal-`k_eff` phase map and continuous contour diagnostic were all motivated after the original plant–pollinator pattern was known. They are structural generalization and mechanism diagnostics, not prospective confirmations. The clone-mixture phase map provides exact `rho` and an analytic support calculation, while the identity-preserving shared-event analysis shows that qualitative mismatch is not confined to whole-trajectory cloning. Neither mechanism is claimed to be a literal model of natural synchrony. Synthetic `k` is not a natural richness threshold, and `I/C` is not proposed as a universal field invariant.

These limits define a direct empirical prediction: natural tests should measure aggregation or support breadth separately from synchrony or shared stochasticity rather than preregistering one combined effective-independence score as sufficient. The expectation is not that the two axes must always differ, but that nonlinear ecology permits them to do so.

Effective independence remains useful for describing variance reduction. Alone, it does not generally determine nonlinear ecological response.

## Data and code availability

Simulation code, documented design objects and machine-readable result summaries are maintained in `izu-core`. A permanent archived release and DOI will replace this repository-only statement before submission.

## Figure legends

**Figure 1. Exact bilinear phase structure.** Determinant-order regions under the solvable bilinear model. Community and interaction components share the same pooled-variance factor, fixing their relative order. Starting-state variance can cross each realization-linked component as effective independence changes, but the C/I boundary cannot be crossed by aggregation or synchrony alone.

**Figure 2. Nonlinear trajectories violate the bilinear C/I constraint.** State-to-community and interaction-to-community variance ratios across aggregation in the plant–pollinator system and an illustrative adaptive consumer–resource setting. Both nonlinear systems cross the C/I equality boundary and contain an interaction-dominated intermediate regime.

**Figure 3. Equal effective independence does not preserve nonlinear decomposition.** Two-dimensional determinant map over aggregation and pairwise trajectory correlation. Along the exact `k_eff=2` contour, expected distinct support increases and the continuous `S/C/I` vector changes substantially despite fixed variance-equivalent independence; determinant order is shown as a visual summary rather than the sole diagnostic.

**Figure 4. I/C diagnoses nonlinear reduction failure.** Interaction-to-community variance ratio under independent aggregation and identity-preserving shared-event correlation. The exact bilinear ratio is invariant; nonlinear systems show finite-scale departures. I/C is a diagnostic, not a universal nonlinear invariant.

## References

Chamberlain, S.A., Bronstein, J.L. & Rudgers, J.A. (2014). How context dependent are species interactions? *Ecology Letters*, 17, 881–890. https://doi.org/10.1111/ele.12279

de Mazancourt, C., Isbell, F., Larocque, A., Berendse, F., De Luca, E., Grace, J.B., Haegeman, B., Polley, H.W., Roscher, C., Schmid, B., Tilman, D., van Ruijven, J., Weigelt, A., Wilsey, B.J. & Loreau, M. (2013). Predicting ecosystem stability from community composition and biodiversity. *Ecology Letters*, 16, 617–625. https://doi.org/10.1111/ele.12088

Holling, C.S. (1959). Some characteristics of simple types of predation and parasitism. *The Canadian Entomologist*, 91, 385–398. https://doi.org/10.4039/Ent91385-7

Keitt, T.H., Amaral, L.A.N., Buldyrev, S.V. & Stanley, H.E. (2002). Scaling in the growth of geographically subdivided populations: invariant patterns from a continent-wide biological survey. *Philosophical Transactions of the Royal Society B: Biological Sciences*, 357, 627–633. https://doi.org/10.1098/rstb.2001.1013

Lázaro, A., Gómez-Martínez, C., González-Estévez, M.A. & Hidalgo, M. (2022). Portfolio effect and asynchrony as drivers of stability in plant–pollinator communities along a gradient of landscape heterogeneity. *Ecography*, 2022, e06112. https://doi.org/10.1111/ecog.06112

Liebhold, A., Koenig, W.D. & Bjørnstad, O.N. (2004). Spatial synchrony in population dynamics. *Annual Review of Ecology, Evolution, and Systematics*, 35, 467–490. https://doi.org/10.1146/annurev.ecolsys.34.011802.132516

Loreau, M. & de Mazancourt, C. (2008). Species synchrony and its drivers: neutral and nonneutral community dynamics in fluctuating environments. *The American Naturalist*, 172, E48–E66. https://doi.org/10.1086/589746

Ruel, J.J. & Ayres, M.P. (1999). Jensen's inequality predicts effects of environmental variation. *Trends in Ecology & Evolution*, 14, 361–366. https://doi.org/10.1016/S0169-5347(99)01664-X

Townsend, D.L., Gouhier, T.C. & Guichard, F. (2025). Aggregated dispersal reduces spatial synchrony but promotes instability and extinction risk. *Oikos*, 2025, e11032. https://doi.org/10.1111/oik.11032
