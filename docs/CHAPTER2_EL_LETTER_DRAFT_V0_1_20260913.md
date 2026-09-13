# Effective independence is not a sufficient statistic for nonlinear ecological response

**Article type:** Letter  
**Target:** Ecology Letters  
**Running title:** Nonlinear failure of effective independence

## Abstract

Ecological aggregation is often expected to suppress stochastic realization effects according to an effective number of independent units. We show that this reduction is exact only under restrictive response structure. In a solvable bilinear model, aggregation size and synchrony enter through one variance coordinate, forcing a fixed interaction-to-community variance ratio. A nonlinear plant–pollinator model violates this invariant: community–interaction ordering reverses and interaction variance dominates at intermediate scale. A structurally separate adaptive consumer–resource model reproduces this phase across broad parameter regions. Most decisively, systems with identical variance-equivalent effective independence can occupy different determinant-order phases because aggregation changes realized support while synchrony changes dependence. Effective independence is therefore variance-equivalent, not generally sufficient, for nonlinear ecological response. Aggregation and synchrony should be treated as distinct ecological context axes.

**Keywords:** aggregation; community context; nonlinear averaging; stochastic synchrony; effective independence; interaction variance; consumer–resource dynamics; plant–pollinator interactions

## Introduction

Ecologists routinely average across individuals, populations, species or repeated community realizations to reduce stochastic variation. The intuition is powerful: if realizations are sufficiently independent, increasing the number of sampled units suppresses realization variance, making persistent differences among focal states easier to detect. The same logic underlies portfolio effects, community stability and many uses of replication in stochastic ecological systems. Yet natural units are rarely independent. Shared environmental forcing, dispersal and trophic coupling synchronize ecological dynamics across space and time (Liebhold et al. 2004; Loreau & de Mazancourt 2008), so the amount of independent information in a pool can be much smaller than its nominal size.

A common response is to combine unit number and correlation into an effective number of independent units. For exchangeable variables with common pairwise correlation `rho`, the variance of their mean is proportional to `rho + (1-rho)/k`, which can be written as the variance of `k_eff = k/[1+(k-1)rho]` independent units. This compression is exact for the variance of a mean. The ecological question is whether it is also sufficient for the response of a nonlinear system.

That distinction matters because ecological responses are rarely linear functions of averaged drivers. Functional responses saturate (Holling 1959), phenotypic and behavioural adjustment can move organisms across response surfaces, and interaction outcomes change with biotic and abiotic context (Chamberlain et al. 2014). Under nonlinear response, replacing a distribution by its mean or variance can change expected outcomes even when the first two moments appear well controlled; Jensen's inequality provides the simplest general warning (Ruel & Ayres 1999). More broadly, context dependence is not only variation in effect magnitude. It can change which source of variation dominates observed ecological response.

Here we ask whether aggregation size and stochastic synchrony can be reduced to a single effective-independence coordinate when ecological response is nonlinear. We partition response variation into three components: a persistent focal-state component `S`, a community-realization component `C`, and a state-by-community interaction component `I`. We first solve an exact bilinear model and show that `k_eff` is sufficient there: both `C` and `I` scale with the same pooled variance, so their ratio cannot change with aggregation or synchrony. We then challenge that reduction in two nonlinear ecological systems. The first is a plant–pollinator response model with active state adjustment; the second is a structurally separate adaptive consumer–resource model with trait-dependent attack and Holling-II saturation. Finally, we compare systems lying on exact equal-`k_eff` contours and use a second, identity-preserving correlation construction to test whether any failure depends on one particular implementation of shared stochasticity.

Our central result is not that averaging can reorder ecological determinants; that follows readily when one variance component shrinks and another persists. Instead, we show that the route of reordering can itself be nonlinear. Aggregation changes the support and composition of realized ecological inputs, whereas synchrony changes dependence among them. Equal variance-equivalent independence therefore need not imply equal response geometry.

## Materials and methods

### Variance decomposition

For a matrix of responses `Y_ir`, indexed by focal state `i` and stochastic community realization `r`, we used the exact two-way sum-of-squares decomposition

`SS_tot = SS_S + SS_C + SS_I`,

where `SS_S` is the additive focal-state component, `SS_C` is the additive community-realization component, and `SS_I` is the remaining state-by-community non-additivity. We report normalized shares

`S = SS_S/SS_tot`, `C = SS_C/SS_tot`, and `I = SS_I/SS_tot`.

The labels `S`, `C` and `I` therefore refer to variance components of the response matrix, not fitted causal coefficients. Their rank order (for example, CIS or ISC) summarizes which component explains the largest, second-largest and smallest share in a declared stochastic regime.

### Exact bilinear baseline

Let `X` be a centered focal-state variable and `Zbar_k` the average of `k` exchangeable community variables with variance `sigma^2` and pairwise correlation `rho`. For

`Y_k = aX + b Zbar_k + c X Zbar_k`,

define

`tau_k = Var(Zbar_k) = sigma^2 [rho + (1-rho)/k]`.

For centered, mutually independent `X` and `Zbar_k`, the three exact variance components are

`S_k = a^2 Var(X)`, `C_k = b^2 tau_k`, and `I_k = c^2 Var(X) tau_k`.

Hence

`I_k/C_k = c^2 Var(X)/b^2`,

which is independent of both `k` and `rho`. Correlation and aggregation affect the decomposition only through `tau_k`. Writing

`k_eff = k/[1+(k-1)rho]`

gives `tau_k = sigma^2/k_eff`, so `k_eff` is an exact sufficient coordinate for this bilinear decomposition.

This exact result provides two useful constraints. First, the relative ordering of `C` and `I` cannot reverse as `k` or `rho` changes. Second, the constant `S` component can cross `C` and `I` separately, so fixed `C/I` ordering can still yield as many as three complete rank-order regions. Thus a three-region trajectory is not itself evidence of nonlinear failure; a `C/I` reversal is.

For a smooth nonlinear response `Y=f(X,Zbar_k)`, a first-order expansion around the mean community state gives `C_k=A_C tau_k+O(tau_k^2)` and `I_k=A_I tau_k+O(tau_k^2)`. Consequently, `I/C` approaches `A_I/A_C` as `tau_k -> 0`. Outside the bilinear case this is a leading-order asymptotic statement, not an exact finite-`k` invariant.

### Nonlinear plant–pollinator system

The first nonlinear system is the frozen plant–pollinator response model developed independently for a separate ecological analysis. Plant starting state is represented on a 21-point standardized trait grid. Pollinator communities are stochastic sets of partner identities with trait positions, specialist or generalist interaction breadths, arrival and loss dynamics and partner-specific effectiveness. Plant service is a saturating function of mean trait matching within the realized pollinator community. When service is below a fixed threshold, plant state can adjust incrementally toward the best-matching current partner. Thus the final response depends both on the starting state and on the full realized community trajectory.

We pooled `k={1,2,4,8,16}` independent community trajectories before evaluating response. For each `k`, 96 stochastic realizations were generated for each of six pre-existing seeds, and the resulting state-by-realization matrices were decomposed into `S`, `C` and `I`. The seed ensemble and active adjustment rate were fixed before the present Lane-B analysis; no seed was selected on the basis of the determinant order reported here.

### Structurally separate nonlinear consumer–resource system

To test whether an interaction-dominated intermediate phase was specific to the pollination mechanism, we constructed an exploratory second response class. Resource traits were drawn from `Beta(2,2)`. A consumer with state `X` assigned Gaussian trait-dependent attack weights to the realized resources and moved iteratively toward the weighted resource-trait centroid. Final intake followed a Holling-II saturating response.

We evaluated the full Cartesian grid of two resource counts per copy (2, 4), three matching widths (0.12, 0.18, 0.25), three handling values (1, 2, 4) and three adaptation rates (0.05, 0.15, 0.30), for 54 settings. Each setting was evaluated at `k={1,2,4,8,16}`, using the same six-seed ensemble and 256 realizations per seed. Because this second model was constructed after observing the plant–pollinator pattern, it is treated as a post-hoc structural generalization, not a preregistered confirmation.

### Exact equal-`k_eff` phase-map challenge

We next constructed correlation in a way that gives an exact pairwise copy correlation. For a pool of `k` trajectories, each copy uses one common trajectory with probability `q=sqrt(rho)` and otherwise uses an independently generated trajectory from the same marginal process. Two copies therefore share the common trajectory with probability `q^2=rho`, giving exact pairwise correlation `rho` for any scalar trajectory-level statistic under this mixture.

This construction also separates variance-equivalent independence from realized support. The expected number of distinct trajectories in the pooled community is

`D(k,rho) = k(1-sqrt(rho)) + 1 - (1-sqrt(rho))^k`

for `rho>0`, with `D(k,0)=k`.

We evaluated a dense grid with `k={1,2,4,8,16}`, `rho={0,0.1,0.25,0.5,0.75,0.9}`, six seeds and 48 realizations per seed. We additionally evaluated exact equal-`k_eff` contours. The primary challenge used `k_eff=2` at `(k,rho)=(2,0),(4,1/3),(8,3/7),(16,7/15)`. A second contour fixed `k_eff=4`.

We reject `k_eff` as a sufficient statistic for the nonlinear response decomposition if one exact equal-`k_eff` contour contains more than one median determinant order under the same response operator.

### Identity-preserving correlation robustness

Whole-trajectory sharing changes identity support directly, so we also used a second correlation mechanism. Pollinator identities and trait draws remained independent among copies. Only arrival and loss events shared Gaussian common shocks. Pairwise correlation was then estimated from realized final pollinator counts rather than assumed from the latent event correlation, and a count-variance-equivalent `k_eff` was calculated from that realized correlation.

We evaluated `k=16` across four latent shared-event correlation levels, with six seeds, 32 response realizations per seed and 400 realizations for count-correlation calibration. This analysis asks whether near-equal variance-equivalent independence recovers the same response decomposition when identities remain independently generated.

## Results

### Exact linearized theory fixes the community–interaction ordering

The bilinear solution shows that `C_k` and `I_k` share the same multiplicative factor `tau_k`. Their ratio is therefore invariant to both aggregation and synchrony, whereas `S_k` remains constant. Aggregation can make `S` overtake the realization-driven components, but it cannot reverse `C` and `I`. In the first-order smooth extension, the same restriction emerges asymptotically because both `C` and `I` are leading-order proportional to the pooled community variance.

Thus the exact theory predicts rank crossover but constrains its route: a system can move across boundaries involving `S`, whereas a finite-scale reversal between `C` and `I` identifies response structure not captured by the one-coordinate bilinear reduction.

### The plant–pollinator model crosses the forbidden C/I boundary

The nonlinear plant–pollinator system did not simply exchange community dominance for state dominance. Median component shares across the six frozen seeds changed from `(S,C,I)=(0.026,0.730,0.247)` at `k=1`, through `(0.273,0.235,0.495)` at `k=4`, to `(0.558,0.127,0.320)` at `k=16`. Corresponding median orders were CIS, CIS, ISC, SIC and SIC over `k=1,2,4,8,16`. The interaction-to-community ratio increased from 0.34 to 2.52, reversing the `C>I` ordering present at small `k`.

The interaction component therefore became the largest variance component at intermediate aggregation. This phase is not a simple consequence of an `O(1)` state component overtaking `O(1/k)` realization variance: it requires the two realization-linked components themselves to separate.

### A second nonlinear response class reproduces the intermediate interaction phase

Across the 54-setting adaptive consumer–resource grid and six seeds, 255 of 324 setting-by-seed trajectories contained an interaction-dominated intermediate scale. A `C/I` ordering reversal occurred in 111 of 324 trajectories, and 68 of 324 showed the full sequence from a C-dominated small-system regime through an I-dominated intermediate regime to an S-dominated large-system regime.

At the setting level, an intermediate I winner occurred in at least four of six seeds for 42 of 54 settings. A `C/I` reversal occurred in at least four seeds for 18 of 54 settings. The complete C-to-I-to-S sequence occurred in at least four seeds for 10 settings and in all six seeds for nine settings.

One illustrative central setting moved from median CIS at `k=1`, to ICS at `k=2`, ISC at `k=4` and `k=8`, and SIC at `k=16`. These results do not establish universality, but they show that the intermediate interaction phase is not unique to one plant–pollinator parameterization or one response function.

### Equal effective independence does not preserve nonlinear phase

The exact `k_eff=2` contour provides the direct counterexample to one-dimensional reduction. At `(k,rho)=(2,0)`, the median decomposition was approximately `(S,C,I)=(0.109,0.437,0.434)`, with median order CIS. Holding `k_eff` exactly equal to 2 while increasing nominal aggregation changed the median order to ICS: `(4,1/3): (0.120,0.358,0.520)`, `(8,3/7): (0.165,0.296,0.538)`, and `(16,7/15): (0.178,0.287,0.521)`.

The change became seed-stable along the contour: all six seeds were ICS at `k=8` and `k=16`. Meanwhile, expected distinct trajectory support increased from 2.00 to 2.66, 3.76 and 6.07. Variance-equivalent independence was fixed, but the support presented to the nonlinear response operator was not.

Failure was not inevitable on every contour. The exact `k_eff=4` contour retained median order ISC across its evaluated points. This is precisely the distinction between an insufficient statistic and a useless statistic: `k_eff` can organize part of the response surface without uniquely determining it.

### The failure persists when identities remain independent

Under the identity-preserving shared-event construction, correlated `k=16` communities with realized-count `k_eff≈3.90` remained SIC in all six seeds, whereas the frozen independent `k=4` regime was ISC. At realized-count `k_eff≈2.33`, correlated `k=16` again remained SIC in all six seeds, whereas independent `k=2` was CIS.

The interaction-to-community ratio also varied under this correlation implementation rather than remaining strictly correlation-invariant. We therefore treat `I/C` as a diagnostic of departure from the exact bilinear reduction, not as a universal invariant of nonlinear ecological systems.

## Discussion

Averaging stochastic ecological units does more than reduce variance when the response operator is nonlinear. In the exact bilinear system, aggregation size and synchrony are interchangeable after compression to `k_eff`: once pooled variance is known, the full `S/C/I` decomposition follows. The nonlinear systems break this equivalence. Equal variance-equivalent independence can correspond to different realized supports, different community–interaction ordering and different dominant response components.

This distinction separates our result from a law-of-large-numbers argument. The decline of a realization-driven variance component with independent averaging is not surprising. Nor is a crossover with a persistent state component. The nontrivial result is that community and state-by-community variance need not contract together. In both nonlinear response classes, their relative ordering changed over finite aggregation scales, and interaction variance became transiently dominant. The determinant hierarchy therefore contains information about response geometry that is lost when aggregation and dependence are compressed to a single variance coordinate.

The mechanism is consistent with a broader ecological lesson from nonlinear averaging. Jensen's inequality makes clear that a nonlinear response can distinguish distributions sharing the same mean (Ruel & Ayres 1999). Our results extend that intuition from mean response to variance decomposition: two pooled communities can have the same variance-equivalent effective independence while differing in support, higher-order composition or identity geometry. If adaptation, matching or saturation acts on those differences, the response matrix need not be preserved.

Synchrony is therefore not merely a nuisance correction to nominal replication. Shared environmental forcing, dispersal and trophic coupling generate spatial and temporal synchrony across ecological populations (Liebhold et al. 2004), and synchrony is itself a central determinant of aggregate community stability (Loreau & de Mazancourt 2008; de Mazancourt et al. 2013). Plant–pollinator communities also exhibit substantial variation in within-year synchrony among sites: in 20 Mallorca communities, Lázaro et al. (2022) reported pollinator synchrony ranging from 0.11 to 0.67 and interaction synchrony from 0.04 to 0.33. Those empirical synchrony measures are not numerically equivalent to the exchangeable `rho` in our models, but they establish that shared temporal structure is neither absent nor constant in a natural interaction network.

The result also refines ecological ideas about context dependence. Species interaction outcomes often change in sign or magnitude across biotic and abiotic contexts (Chamberlain et al. 2014). Here, context changes not only the magnitude of a response but the identity of the dominant variance source. A community may be realization-dominated at small scale, interaction-dominated at intermediate scale and state-dominated at larger scale. Describing such systems with one global hierarchy of "important drivers" can therefore be misleading even when every component is measured correctly.

For study design, aggregation and synchrony should be retained as separate axes whenever nonlinear ecological response is plausible. Increasing the number or breadth of realized partners is not equivalent to obtaining the same nominal gain in `k_eff` by reducing shared stochasticity. Conversely, a high nominal richness or replication count does not guarantee the response geometry expected under independent averaging. This matters for experiments that pool interaction opportunities, spatial samples or repeated temporal windows and then interpret a single effective sample-size correction as an ecological state variable.

Several boundaries are important. First, the second nonlinear response class and dense phase map were motivated after the original plant–pollinator pattern was known; they are structural generalization and mechanism diagnostics, not prospective confirmations. Second, the clone-mixture phase map intentionally provides exact `rho` and an analytic support calculation, while the identity-preserving shared-event analysis shows that the qualitative failure is not confined to whole-trajectory cloning. Neither implementation is claimed to be a literal model of natural synchrony. Third, our models do not estimate a universal natural crossover or map synthetic `k` to species richness. Fourth, `I/C` is exact only in the bilinear model and asymptotically constrained at first order; its nonlinear correlation sensitivity prevents treating it as a universal field invariant.

These limitations define a sharper empirical prediction rather than weakening the result. Natural tests should measure aggregation or support breadth separately from synchrony or shared stochasticity, instead of preregistering one combined effective-independence score as sufficient. The theoretical expectation is not that the two axes must always produce different outcomes, but that nonlinear ecological response allows them to do so.

Effective independence remains a useful description of variance reduction. It is simply not, in general, a sufficient description of nonlinear ecological response.

## Data and code availability

All simulation code, frozen design objects and machine-readable result summaries used for this Letter are maintained in the `izu-core` repository. A permanent archived release and DOI should be deposited before submission; the final citation will replace this statement.

## Figure legends

**Figure 1. Exact bilinear phase structure.** Determinant-order regions under the solvable bilinear model. Community and interaction components share the same pooled-variance factor, fixing their relative order. Starting-state variance can cross each realization-linked component as effective independence changes, but the C/I boundary cannot be crossed by changing aggregation or synchrony alone.

**Figure 2. Nonlinear trajectories violate the bilinear C/I constraint.** Trajectories of state-to-community and interaction-to-community variance ratios across aggregation for the plant–pollinator system and an illustrative adaptive consumer–resource setting. Both nonlinear systems cross the C/I equality boundary, generating an interaction-dominated intermediate regime.

**Figure 3. Equal effective independence does not preserve nonlinear phase.** Determinant-order map over aggregation size and pairwise trajectory correlation. The exact `k_eff=2` contour crosses from median CIS to ICS while expected distinct trajectory support increases, directly demonstrating that variance-equivalent effective independence is not sufficient for the nonlinear response decomposition.

**Figure 4. I/C as a diagnostic of nonlinear reduction failure.** Interaction-to-community variance ratio across independent aggregation and identity-preserving shared-event correlation. The exact bilinear ratio is invariant; nonlinear systems show strong finite-scale departures. I/C is therefore treated as a diagnostic, not a universal nonlinear invariant.

## References

Chamberlain, S.A., Bronstein, J.L. & Rudgers, J.A. (2014). How context dependent are species interactions? *Ecology Letters*, 17, 881–890. https://doi.org/10.1111/ele.12279

de Mazancourt, C., Isbell, F., Larocque, A., Berendse, F., De Luca, E., Grace, J.B., Haegeman, B., Polley, H.W., Roscher, C., Schmid, B., Tilman, D., van Ruijven, J., Weigelt, A., Wilsey, B.J. & Loreau, M. (2013). Predicting ecosystem stability from community composition and biodiversity. *Ecology Letters*, 16, 617–625. https://doi.org/10.1111/ele.12088

Holling, C.S. (1959). Some characteristics of simple types of predation and parasitism. *The Canadian Entomologist*, 91, 385–398. https://doi.org/10.4039/Ent91385-7

Lázaro, A., Gómez-Martínez, C., González-Estévez, M.A. & Hidalgo, M. (2022). Portfolio effect and asynchrony as drivers of stability in plant–pollinator communities along a gradient of landscape heterogeneity. *Ecography*, 2022, e06112. https://doi.org/10.1111/ecog.06112

Liebhold, A., Koenig, W.D. & Bjørnstad, O.N. (2004). Spatial synchrony in population dynamics. *Annual Review of Ecology, Evolution, and Systematics*, 35, 467–490. https://doi.org/10.1146/annurev.ecolsys.34.011802.132516

Loreau, M. & de Mazancourt, C. (2008). Species synchrony and its drivers: neutral and nonneutral community dynamics in fluctuating environments. *The American Naturalist*, 172, E48–E66. https://doi.org/10.1086/589746

Ruel, J.J. & Ayres, M.P. (1999). Jensen's inequality predicts effects of environmental variation. *Trends in Ecology & Evolution*, 14, 361–366. https://doi.org/10.1016/S0169-5347(99)01664-X
