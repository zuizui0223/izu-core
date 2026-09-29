# Effective independence is a second-order coordinate, not a nonlinear ecological state

**Article type:** Letter  
**Target:** Ecology Letters  
**Running title:** Beyond effective independence  
**Working main-text words:** to be checked by CI  
**Figures:** 4  
**References:** 11

## Abstract

Ecologists often replace many correlated units by an effective number of independent units. Such reductions are exact for a chosen variance, but their sufficiency for nonlinear response is rarely tested. We show analytically that variance-equivalent effective independence fixes second moments but generically leaves third and higher cumulants free. In an exact quadratic state–community expansion, those higher moments alter community and state-by-community variance unless pure and mixed response curvatures satisfy a restrictive alignment condition. A plant–pollinator model and an adaptive consumer–resource model cross the resulting community–interaction boundary. A prespecified scalar-curvature prediction fails, whereas a fresh-seed intervention identifies state-adjustment feedback as a phase-shaping condition. Equal effective independence can therefore hide both higher-order distributional structure and discrete support. Aggregation and synchrony should remain separate axes when nonlinear ecological response is plausible.

**Keywords:** aggregation; community context; effective number; higher cumulants; interaction variance; nonlinear averaging; state–community feedback; stochastic synchrony

## Introduction

Ecology repeatedly compresses structured systems into scalar equivalents. Effective population size maps a real population to an idealized population that matches a specified rate of drift or inbreeding (Wang et al. 2016). Effective numbers of species transform diversity measures into the number of equally common species that would generate the same diversity (Jost 2006). Portfolio and synchrony theory reduces covariance structure to interpretable measures of aggregate stability (Loreau & de Mazancourt 2008; de Mazancourt et al. 2013). These quantities are not mathematically interchangeable, and we do not claim that they share one universal failure mode. They do share a useful design principle: a complex system is replaced by a scalar reference system that is equivalent for a specified property.

Our target is the narrower but common case in which equivalence is defined by a second moment. Spatial synchrony can reduce the effective number of independently fluctuating subpopulations (Keitt et al. 2002), and exchangeable correlation gives the familiar variance-equivalent count

`k_eff = k/[1+(k-1)rho]`.

For the mean of `k` equal-variance units with common pairwise correlation `rho`, this reduction is exact: its variance is the variance of `k_eff` independent units. The question is what, if anything, that scalar determines after a nonlinear ecological response operator acts on the pooled system.

Nonlinearity is routine in ecology. Functional responses saturate (Holling 1959), phenotypes and behaviours adjust to biotic context, and interaction outcomes change across environments and partner assemblages (Chamberlain et al. 2014). Jensen's inequality already shows that equal means do not imply equal mean responses under nonlinearity (Ruel & Ayres 1999). Synchrony likewise depends on environmental forcing, dispersal and trophic coupling (Liebhold et al. 2004), and recent metacommunity theory shows that aggregation and stochastic dispersal can alter synchrony and stability jointly (Townsend et al. 2025). What is missing is a sharp answer to a different question: **at what order does a variance-equivalent effective number stop being sufficient, and what response geometry makes that failure visible?**

We answer that question in four steps. First, a bilinear state–community model provides an exact null in which `k_eff` determines the full response decomposition. Second, a cumulant expansion shows that this sufficiency is generically limited to second order. Third, an exact quadratic mixed-response model identifies when higher moments change the ratio of community to state-by-community variation. Fourth, we confront those predictions with two nonlinear ecological response classes. We explicitly separate two mechanisms: a smooth higher-cumulant mechanism and a discrete support mechanism. We also retain a failed prespecified prediction rather than optimizing it away, then test the revised mixed-feedback condition on previously unused simulation seeds.

## Materials and methods

### Response decomposition

For response matrices `Y_ir`, indexed by focal state `i` and stochastic community realization `r`, we used the exact two-way decomposition

`SS_tot = SS_S + SS_C + SS_I`.

`S=SS_S/SS_tot` is persistent focal-state variation, `C=SS_C/SS_tot` is additive community-realization variation, and `I=SS_I/SS_tot` is the state-by-community non-additive remainder. The decomposition is descriptive rather than causal. A label such as CIS orders the normalized shares from largest to smallest.

### Exact bilinear null

Let centered `X` denote focal state and `Zbar_k` the mean of `k` exchangeable centered community variables with variance `sigma^2` and common pairwise correlation `rho`. For

`Y = aX + b Zbar_k + c X Zbar_k`,

write

`tau_k = Var(Zbar_k) = sigma^2[rho+(1-rho)/k] = sigma^2/k_eff`.

With `X` independent of `Zbar_k`,

`S = a^2 Var(X)`,  
`C = b^2 tau_k`,  
`I = c^2 Var(X) tau_k`.

Hence `I/C = c^2 Var(X)/b^2`: `C` and `I` share exactly the same `tau_k` multiplier. Aggregation or synchrony can make the constant `S` component cross them, but cannot reverse `C` and `I` at fixed model coefficients. This defines the reduction that a nonlinear model must violate.

### Where variance-equivalent sufficiency first breaks

For a smooth scalar response to a centered pooled coordinate `Z`,

`E[f(mu+Z)] = f(mu) + f''(mu) kappa_2/2 + f'''(mu) kappa_3/6 + f''''(mu)(kappa_4+3 kappa_2^2)/24 + ...`.

A variance-equivalent coordinate fixes `kappa_2` but does not generally fix `kappa_3`, `kappa_4`, or higher cumulants. Thus it is sufficient through second order only. If source skewness and `f'''` are nonzero, the first smooth difference is third order; if symmetry forces `kappa_3=0`, the first difference moves to the next nonzero cumulant.

This can be made explicit under a common-factor construction

`Z_j = sqrt(rho) U + sqrt(1-rho) W_j`,

with independent centered `U` and `W_j`. For the pooled mean,

`kappa_2(Zbar) = kappa_2 [rho+(1-rho)/k]`,

`kappa_3(Zbar) = kappa_3 [rho^(3/2)+(1-rho)^(3/2)/k^2]`,

and

`kappa_4(Zbar) = kappa_4 [rho^2+(1-rho)^2/k^3]`,

when common and idiosyncratic sources share the same corresponding cumulant. Along a contour with fixed `K=k_eff`,

`rho=(k-K)/[K(k-1)]`.

The variance factor is exactly `1/K`, while the third- and fourth-cumulant factors vary with `k`. Equal `k_eff` therefore does not specify the pooled distribution beyond second order.

### Exact condition for C/I failure

A scalar Taylor expansion is not enough to predict `C/I`, because `I` is generated by **mixed state–community response geometry**. We therefore used the centered quadratic extension

`Y = aX + bZ + cXZ + (d/2)(Z^2-tau) + (e/2)X(Z^2-tau)`,

where `tau=Var(Z)`. Its functional-ANOVA components are exact:

`C = b^2 tau + b d mu_3 + (d^2/4) Var(Z^2)`,

`I = Var(X)[c^2 tau + c e mu_3 + (e^2/4) Var(Z^2)]`,

with `Var(Z^2)=kappa_4+2tau^2`. At fixed `tau`, higher moments alter `C` and `I` differently. For symmetric `Z` (`mu_3=0`),

`sign[d(I/C)/d Var(Z^2)] = sign(e^2 b^2 - c^2 d^2)`.

Thus second-moment sufficiency survives this order only under the restrictive curvature-alignment condition `e^2 b^2=c^2 d^2`, or when the relevant higher moment itself does not change. This identifies a response-level condition rather than merely observing a simulation counterexample.

### Nonlinear ecological systems

The first system was the frozen plant–pollinator response model used in the companion Chapter 2 ecological analysis. Plant state was evaluated on 21 standardized starting positions. Stochastic pollinator communities varied in partner identity, trait position, interaction breadth, arrival, loss and effectiveness. Service saturated with mean trait matching; when service was low, plant state adjusted toward the best current partner. We pooled `k={1,2,4,8,16}` independent trajectories, using 96 realizations for each of six pre-existing seeds.

The structurally separate system was an adaptive consumer–resource model. Resource traits followed `Beta(2,2)`. A consumer assigned Gaussian trait-dependent attack weights to resources, adjusted toward their weighted trait centroid, and received a Holling-II intake `A/(1+hA)`. The existing exploratory grid crossed resources per copy `{2,4}`, matching width `{0.12,0.18,0.25}`, handling `{1,2,4}`, adaptation rate `{0.05,0.15,0.30}`, five aggregation levels, six seeds and 256 realizations per seed, yielding 54 settings and 324 setting-by-seed trajectories.

### Prespecified curvature test and fresh feedback validation

Before reading the 54 setting-level outcome map, we froze a scalar-curvature prediction. Because the raw resource distribution `Beta(2,2)` is symmetric, its third cumulant vanishes. We therefore used the integrated absolute fourth derivative of the Holling-II response,

`H4(h) = integral_0^1 |g''''(A)| dA = 6h^2[1-(1+h)^(-4)]`,

and predicted more `C/I` reversals at larger `h`. The test compared `h=4` with `h=1` within all 18 matched combinations of resource count, width and adaptation rate. No retuning was permitted after opening those setting-level results.

That prediction failed. We then revised the mechanism at the level implied by the exact bivariate result: the relevant distinction is pure community curvature versus **mixed state–community curvature**, not scalar saturation alone. The state update

`x_(t+1)=x_t+alpha[target(x_t,Z)-x_t]`

introduces feedback-dependent mixed derivatives through the chain rule. We therefore froze a second test before execution on six previously unused seeds (`310001, 310019, 310043, 310049, 310081, 310111`). Across the complete 18 combinations of resource count, width and handling, we compared `alpha=0` with `alpha=0.15`; each condition retained `k={1,2,4,8,16}`, 10 adjustment steps and 256 realizations. The primary outcome was a `C/I` reversal: `C>I` at `k=1` and `I>C` at any later `k`. The prediction was directional only: active feedback would generate more reversals than the feedback knockout across the 108 paired block-by-seed comparisons.

### Support and cumulant mechanisms are distinct

The existing equal-`k_eff` phase challenge used a clone mixture: each of `k` trajectories used a common trajectory with probability `q=sqrt(rho)` and otherwise an independent trajectory. Pairwise correlation is exactly `rho`, but expected distinct support is

`D(k,rho)=k(1-sqrt(rho))+1-(1-sqrt(rho))^k`.

This is a discrete support counterexample and does not require smooth cumulant theory. We therefore do not interpret it as evidence for a cumulant mechanism.

A second correlation construction preserved independent partner identities and trait draws while sharing Gaussian shocks in arrival and loss events. Its mismatch with independent systems at similar variance-equivalent `k_eff` demonstrates that failure is not confined to changing identity support. Together, the two constructions separate support-based non-equivalence from smooth distributional non-equivalence.

## Results

### Equal effective independence fixes variance, not higher cumulants

Along the exact `k_eff=2` contour `(k,rho)=(2,0),(4,1/3),(8,3/7),(16,7/15)`, the variance factor was exactly 0.5 at every point. The corresponding third-cumulant multipliers were 0.250, 0.226, 0.287 and 0.320, and fourth-cumulant multipliers were 0.125, 0.118, 0.184 and 0.218. At `k_eff=4`, the variance factor likewise remained exactly 0.25 while both higher-cumulant factors changed. The departure need not be monotonic at small `k`; the key result is non-identity at fixed variance.

The quadratic mixed-response model converts that distributional non-identity into an exact condition on response geometry. At fixed variance and symmetric source noise, changing `kappa_4` changes `I/C` whenever `e^2b^2 != c^2d^2`, with direction given by the sign of that difference. The bilinear invariant is therefore the aligned special case of a broader response expansion, not a generic nonlinear law.

### Both nonlinear ecological systems cross the bilinear boundary

In the frozen plant–pollinator model, median `(S,C,I)` changed from `(0.026,0.730,0.247)` at `k=1` to `(0.273,0.235,0.495)` at `k=4` and `(0.558,0.127,0.320)` at `k=16`. `I/C` increased from 0.34 to 2.52, so the two realization-linked components reversed order rather than merely being overtaken by persistent state variance.

Across the original 54-setting consumer–resource grid, 255/324 setting-by-seed trajectories had an interaction-dominated intermediate scale, 111/324 crossed the `C/I` boundary, and 68/324 followed a C-dominated to I-dominated to S-dominated winner sequence. At the setting level, 18/54 settings had a `C/I` reversal in at least four of six seeds.

### Scalar saturation curvature does not explain which settings reverse

The prespecified fourth-order Holling prediction failed in the direction opposite to expectation. Summed reversal counts across the six frozen seeds were 41 at `h=1`, 38 at `h=2` and 32 at `h=4`, although `H4(h)` increased sharply from 5.625 to 23.704 to 95.846. In the 18 matched `h=4` versus `h=1` blocks, the reversal count increased in 0 blocks, was unchanged in 16 and decreased in 2; the mean paired difference was -0.5 seeds. Scalar response curvature is therefore not the setting-level condition for the phase transition.

### Fresh seeds identify state–community feedback as a phase-shaping condition

The revised mixed-feedback prediction was supported without retuning. Across 108 paired block-by-seed comparisons, `alpha=0` produced **0** C/I reversals, whereas `alpha=0.15` produced **52**. All 52 discordant pairs were in the predicted direction and none were opposite; 56 pairs were ties.

The intervention did not simply amplify interaction variance. With `alpha=0`, all 108 cases were already `I>C` at `k=1`, with median `(S,C,I)=(0.324,0.016,0.657)`. Active adjustment reorganized the small-system geometry: at `alpha=0.15`, 52/108 cases became `C>I` at `k=1`, and the median decomposition was `(0.101,0.412,0.487)`. By `k=4`, all 108 active-feedback cases were `I>C`, with median `(0.294,0.132,0.545)`. Thus feedback creates a low-aggregation community-dominated regime that aggregation can exit through the interaction-dominated phase. It changes **phase topology**, not merely the magnitude of `I`.

### Equal k_eff remains insufficient under two different mechanisms

Along the clone-mixture `k_eff=2` contour, median decomposition changed from `(0.109,0.437,0.434)` at `(2,0)` to `(0.178,0.287,0.521)` at `(16,7/15)`, an L1 change of 0.307, while expected distinct support increased from 2.00 to 6.07. This is direct support non-equivalence at fixed variance-equivalent independence.

Under the identity-preserving shared-event construction, correlated `k=16` communities with realized-count `k_eff≈3.90` remained SIC in all six seeds while the frozen independent `k=4` system was ISC. At realized-count `k_eff≈2.33`, correlated `k=16` again remained SIC in all six seeds while independent `k=2` was CIS. The mismatch therefore persists when partner identities are generated independently, consistent with the broader result that second-moment equivalence does not identify nonlinear response geometry.

## Discussion

The central result is now sharper than a simulation counterexample. `k_eff` is an exact coordinate for a second moment. It becomes an exact coordinate for response only when the response operator discards the distributional information that `k_eff` discards. A cumulant expansion identifies the first missing information: generically skewness at third order, or the next nonzero higher cumulant under symmetry. The quadratic mixed-response model then shows exactly how that information reaches the ecological quantity measured here. Community and state-by-community variance respond differently unless pure and mixed curvatures are proportionally aligned.

This also clarifies why scalar nonlinearity alone was the wrong predictor. Our frozen handling-time prediction failed. A stronger Holling nonlinearity did not produce more C/I reversals. What mattered in the fresh intervention was feedback between focal state and realized community. In functional-ANOVA language, `C` is controlled by the response shared across focal states, whereas `I` is controlled by state-dependent departures from that shared response. Active adjustment changed the balance between those channels: it generated a C-dominated small-system regime, after which aggregation exposed an I-dominated regime. The relevant object is therefore mixed response geometry, not a one-dimensional curvature index.

The support result and cumulant result should likewise not be conflated. The clone-mixture construction changes the number of distinct trajectories even at exactly fixed `k_eff`; it is a discrete support mechanism. The common-factor calculation shows a different mathematical route: even when variance is fixed, higher cumulants of a pooled coordinate are not. The identity-preserving event construction demonstrates that the nonlinear mismatch is not an artifact of cloning identities. These are two routes to the same limitation of a second-moment scalar, not two measurements of one mechanism.

The wider effective-number literature helps delimit the claim. Effective population size is explicitly defined relative to a chosen idealized process, and different effective sizes can differ when the matched process differs (Wang et al. 2016). Hill/Jost effective species numbers are defined by diversity equivalence, not by response equivalence (Jost 2006). We therefore do **not** argue that effective numbers are generally misleading. The lesson is the opposite: equivalence should be respected at the level at which it is defined. A variance-equivalent number is safe for variance accounting; promoting it to a sufficient ecological state descriptor requires an additional response-sufficiency argument.

That distinction matters for ecological synchrony and portfolio effects. Shared environmental forcing, dispersal and trophic coupling create covariance among populations and interactions (Liebhold et al. 2004), while synchrony is a central determinant of aggregate stability (Loreau & de Mazancourt 2008; de Mazancourt et al. 2013). Natural plant–pollinator networks show substantial and variable synchrony among pollinators and interactions (Lázaro et al. 2022). Our result says that matching the variance consequence of that synchrony need not match the response consequence when state adjustment, nonlinear matching or other mixed feedbacks are present.

The design implication is concrete. Aggregation or support breadth and synchrony or shared stochasticity should remain separate pre-outcome axes whenever nonlinear response is plausible. Their compression can be justified after demonstrating response sufficiency, not assumed because they give the same variance. The same logic suggests a diagnostic workflow: identify the property used to define an effective number, derive which higher moments or structural features it leaves unconstrained, and test whether the ecological response contains pure and mixed derivatives that are sensitive to those omitted features.

Several boundaries remain. The original consumer–resource class and equal-`k_eff` challenges were motivated after the plant–pollinator pattern was known. The handling-only test was prospective only with respect to the unopened setting-level map, and it failed. The subsequent mixed-feedback prediction was motivated by that failure but was then frozen and tested on six previously unused seeds across the full 18-block intervention. This is fresh synthetic validation, not empirical confirmation. Neither correlation construction is claimed to be a literal model of natural synchrony, synthetic `k` is not a natural richness threshold, and the observed fraction of positive settings is not an ecological prevalence estimate.

The useful boundary is therefore simple. Effective independence is an exact second-order coordinate. Nonlinear ecological response can require more: higher cumulants, discrete support, and mixed state–community geometry. When those matter, one effective number cannot stand in for the axes from which it was constructed.

## Data and code availability

Simulation code, frozen design objects, failed and successful prediction receipts, and machine-readable result summaries are maintained in `izu-core`. A permanent archived release and DOI will replace this repository-only statement before submission.

## Figure legends

**Figure 1. Where effective-independence sufficiency breaks.** Equal-`k_eff` contours fix the second cumulant exactly while leaving third and fourth cumulants unconstrained. The quadratic mixed-response extension shows that higher moments change `I/C` unless pure and mixed response curvatures satisfy the alignment condition `e^2b^2=c^2d^2`.

**Figure 2. Nonlinear ecological systems cross the bilinear C/I boundary.** Aggregation trajectories in the frozen plant–pollinator system and the adaptive consumer–resource model. The bilinear null fixes `I/C`; both nonlinear systems show finite-scale C/I reversal and an interaction-dominated intermediate regime.

**Figure 3. A failed scalar predictor and a successful fresh feedback intervention.** The prespecified Holling fourth-order predictor increases with handling time but does not predict reversal frequency in the frozen 54-setting grid. In six fresh seeds, feedback knockout (`alpha=0`) yields no C-to-I reversals, whereas active adjustment (`alpha=0.15`) yields 52/108 paired reversals and creates the C-dominated low-aggregation regime.

**Figure 4. Equal variance-equivalent independence can fail by two routes.** Along the exact clone-mixture `k_eff=2` contour, realized support and `S/C/I` geometry change together. Under identity-preserving shared-event correlation, response geometry still differs from independent systems at similar variance-equivalent `k_eff`, separating discrete support non-equivalence from the broader higher-order distributional limitation.

## References

Chamberlain, S.A., Bronstein, J.L. & Rudgers, J.A. (2014). How context dependent are species interactions? *Ecology Letters*, 17, 881–890. https://doi.org/10.1111/ele.12279

de Mazancourt, C., Isbell, F., Larocque, A., Berendse, F., De Luca, E., Grace, J.B., Haegeman, B., Polley, H.W., Roscher, C., Schmid, B., Tilman, D., van Ruijven, J., Weigelt, A., Wilsey, B.J. & Loreau, M. (2013). Predicting ecosystem stability from community composition and biodiversity. *Ecology Letters*, 16, 617–625. https://doi.org/10.1111/ele.12088

Holling, C.S. (1959). Some characteristics of simple types of predation and parasitism. *The Canadian Entomologist*, 91, 385–398. https://doi.org/10.4039/Ent91385-7

Jost, L. (2006). Entropy and diversity. *Oikos*, 113, 363–375. https://doi.org/10.1111/j.2006.0030-1299.14714.x

Keitt, T.H., Amaral, L.A.N., Buldyrev, S.V. & Stanley, H.E. (2002). Scaling in the growth of geographically subdivided populations: invariant patterns from a continent-wide biological survey. *Philosophical Transactions of the Royal Society B: Biological Sciences*, 357, 627–633. https://doi.org/10.1098/rstb.2001.1013

Lázaro, A., Gómez-Martínez, C., González-Estévez, M.A. & Hidalgo, M. (2022). Portfolio effect and asynchrony as drivers of stability in plant–pollinator communities along a gradient of landscape heterogeneity. *Ecography*, 2022, e06112. https://doi.org/10.1111/ecog.06112

Liebhold, A., Koenig, W.D. & Bjørnstad, O.N. (2004). Spatial synchrony in population dynamics. *Annual Review of Ecology, Evolution, and Systematics*, 35, 467–490. https://doi.org/10.1146/annurev.ecolsys.34.011802.132516

Loreau, M. & de Mazancourt, C. (2008). Species synchrony and its drivers: neutral and nonneutral community dynamics in fluctuating environments. *The American Naturalist*, 172, E48–E66. https://doi.org/10.1086/589746

Ruel, J.J. & Ayres, M.P. (1999). Jensen's inequality predicts effects of environmental variation. *Trends in Ecology & Evolution*, 14, 361–366. https://doi.org/10.1016/S0169-5347(99)01664-X

Townsend, D.L., Gouhier, T.C. & Guichard, F. (2025). Aggregated dispersal reduces spatial synchrony but promotes instability and extinction risk. *Oikos*, 2025, e11032. https://doi.org/10.1111/oik.11032

Wang, J., Santiago, E. & Caballero, A. (2016). Prediction and estimation of effective population size. *Heredity*, 117, 193–206. https://doi.org/10.1038/hdy.2016.43
