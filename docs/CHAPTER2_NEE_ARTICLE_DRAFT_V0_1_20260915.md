# Ecological determinant rankings change across breadth–synchrony regimes

**Article type:** working Nature Ecology & Evolution Article candidate  
**Status:** V0.1 after frozen natural-regime route closure  
**Primary routing receipt:** `data/results/chapter2_natural_regime_six_source_checkpoint_20260915.json`  
**Search closure:** `data/results/chapter2_natural_regime_search_closure_20260915.json`

## Abstract

Ecology often asks which factor matters most, as though the ordering of determinants were an intrinsic property of a system. That assumption can fail when ecological responses are nonlinear and communities differ in both partner breadth and temporal synchrony. We first derive an exact null in which a variance-equivalent effective number of independent units is sufficient: community and state-by-community contributions share the same second-moment multiplier and cannot reverse rank. A cumulant expansion then shows why this sufficiency is generically limited to second order, and an exact quadratic state–community model identifies the mixed-response curvature condition under which higher moments alter determinant ordering. Two structurally distinct nonlinear ecological models cross this boundary. A prespecified scalar-curvature prediction fails, whereas a prospectively frozen feedback intervention produces 52 reversals of community versus interaction dominance in 108 comparisons and none without feedback. We then place 42 natural island interaction systems from six source studies and five island groups on independently measured partner-breadth and synchrony axes. The source-balanced regime plane spans both axes broadly and remains so after removing the largest study, satisfying a predeclared external-regime criterion. Yet a frozen audit of 25 island research entries finds no study that jointly measures the full outcome-independent determinant–response contract. Determinant rankings are therefore not safely transportable without measuring ecological regime coordinates first. Breadth and synchrony should be treated as separate context variables rather than compressed into a single effective-number description when nonlinear responses are plausible.

## Introduction

Ecologists routinely rank candidate determinants. Environment versus biotic interactions, diversity versus composition, initial state versus stochastic realization, and local versus regional processes are compared using effect sizes, variance partitions or predictive importance. The resulting ranking is often narrated as a property of the ecological system: one factor is said to dominate another.

That interpretation quietly assumes that the ranking is stable across the regime in which the system is observed. But ecological systems differ in the number and evenness of realized partners, in the synchrony of those partners through time, and in the strength of state-dependent feedback. Those differences can change not only the magnitude of ecological variation but the relative ordering of its sources.

A common response to this complexity is compression. Correlated units can be represented by an effective number of independent units; diversity can be expressed as an effective number of equally common types; covariance structure can be summarized by synchrony or portfolio measures. These reductions are valuable because they define a simpler reference system that is equivalent for a chosen property. The critical question is whether equivalence for one property is sufficient after a nonlinear ecological response operator acts on the system.

For second-moment equivalence the answer can be stated sharply. If `k` equal-variance community components have exchangeable correlation `rho`, then

`k_eff = k / [1 + (k-1)rho]`

is exactly variance-equivalent to `k_eff` independent components. In a bilinear state–community response, the same variance factor multiplies both additive community variation and state-by-community interaction variation. Their ordering is therefore invariant at fixed coefficients. A reversal of those components is evidence that the response depends on information not contained in the variance-equivalent scalar.

We build from that null in four steps. First, we show analytically where second-moment sufficiency breaks and identify the response geometry that exposes the break. Second, we test the resulting boundary in two nonlinear ecological model classes and retain a failed prespecified prediction rather than optimizing it away. Third, we prospectively test a mixed-feedback condition on unused simulations. Fourth, we ask whether real ecological systems occupy enough breadth–synchrony space for the regime dependence to matter outside the model, using a result-blind public-data search and a predeclared routing gate.

The empirical task is deliberately narrower than validating the synthetic mechanism in nature. Natural systems are not assigned a synthetic `k`, and their coordinates do not retune the models. They ask whether the two context dimensions required by the theory are independently estimable and broadly occupied. A separate frozen literature audit then asks a different question: whether existing island studies measure the complete determinant–outcome contract needed to transport a determinant ranking across systems.

Together these analyses lead to a general claim: **the identity of the dominant ecological determinant can be regime dependent, so determinant rankings should be conditioned on breadth and synchrony rather than treated as globally portable system properties.**

## Results

### A second-moment effective number has an exact sufficiency boundary

Let centered `X` denote focal state and `Zbar_k` the mean of `k` exchangeable centered community variables with variance `sigma^2` and common correlation `rho`. In the bilinear response

`Y = aX + b Zbar_k + c X Zbar_k`,

`tau_k = Var(Zbar_k) = sigma^2 [rho + (1-rho)/k] = sigma^2/k_eff`.

When `X` and `Zbar_k` are independent, the exact functional decomposition is

`S = a^2 Var(X)`,  
`C = b^2 tau_k`,  
`I = c^2 Var(X) tau_k`.

Thus

`I/C = c^2 Var(X)/b^2`.

Aggregation and synchrony may cause the constant state component `S` to overtake both `C` and `I`, but they cannot reverse the ordering of `C` and `I`. This is the exact null: if a nonlinear system reverses community and state-by-community contributions while holding the second-moment coordinate fixed, a variance-equivalent effective number is not a sufficient ecological state descriptor.

A smooth-response expansion identifies the missing information. For a centered pooled variable `Z`,

`E[f(mu+Z)] = f(mu) + f''(mu)kappa_2/2 + f'''(mu)kappa_3/6 + f''''(mu)(kappa_4+3kappa_2^2)/24 + ...`.

Variance equivalence fixes `kappa_2`, not `kappa_3`, `kappa_4` or higher cumulants. Under the common-factor construction

`Z_j = sqrt(rho)U + sqrt(1-rho)W_j`,

the pooled variance depends on `rho+(1-rho)/k`, whereas the third- and fourth-cumulant multipliers depend on `rho^(3/2)+(1-rho)^(3/2)/k^2` and `rho^2+(1-rho)^2/k^3`. Along a contour of constant `k_eff`, the second moment is fixed while higher cumulants vary.

A scalar expansion alone cannot determine which variance component changes rank, because interaction variation is generated by mixed state–community geometry. We therefore used the exact centered quadratic response

`Y = aX + bZ + cXZ + (d/2)(Z^2-tau) + (e/2)X(Z^2-tau)`.

Its community and interaction components are

`C = b^2 tau + bd mu3 + (d^2/4) Var(Z^2)`

and

`I = Var(X)[c^2 tau + ce mu3 + (e^2/4) Var(Z^2)]`.

For symmetric `Z`, changing the fourth-order term at fixed variance changes `I/C` with sign

`sign[d(I/C)/d Var(Z^2)] = sign(e^2 b^2 - c^2 d^2)`.

Second-moment sufficiency therefore survives this order only under a restrictive alignment of pure and mixed response curvature. The null is exact, but it is not generic once mixed nonlinear response geometry is admitted.

### Two nonlinear ecological systems cross the bilinear determinant-order boundary

We next asked whether this mathematical possibility occurs in ecological response models with different internal structures.

The first model describes a plant state responding to stochastic pollinator communities. Plant performance depends on realized partner identity, trait matching, interaction breadth, arrival, loss and effectiveness; service saturates, and low service permits state adjustment toward the best current partner. Across the frozen six-seed analysis, median normalized `(S,C,I)` shifted from approximately `(0.026, 0.730, 0.247)` at `k=1` to `(0.273, 0.235, 0.495)` at `k=4` and `(0.558, 0.127, 0.320)` at `k=16`. The ratio `I/C` increased from 0.34 to 2.52. The realization-linked components therefore reversed order; the result was not merely a later takeover by persistent state variance.

A separate adaptive consumer–resource model generated the same qualitative boundary crossing without sharing the plant–pollinator architecture. Across 54 parameter settings and six frozen seeds, 255 of 324 setting-by-seed trajectories contained an interaction-dominated intermediate scale, 111 crossed the `C/I` boundary, and 68 followed a community-dominated to interaction-dominated to state-dominated winner sequence. At the setting level, 18 of 54 settings showed a `C/I` reversal in at least four of six seeds.

These simulations do not establish a natural threshold at any particular `k`. They establish that determinant ordering can be a property of the regime traversed by the system rather than a fixed ranking attached to the system itself.

### A prespecified scalar-curvature explanation fails

The first attempted mechanism was intentionally simple. Because the consumer–resource source distribution was symmetric, we froze a prediction based on fourth-order curvature of the Holling-II response before opening the 54-setting outcome map. The integrated absolute fourth derivative increased strongly with handling parameter `h`, so the frozen prediction was that high `h` would produce more `C/I` reversals.

The prediction failed in the opposite direction. Summed reversal counts were 41 at `h=1`, 38 at `h=2` and 32 at `h=4`. Across the 18 matched `h=4` versus `h=1` blocks, zero increased, 16 tied and two decreased. Scalar saturation curvature alone was therefore not the phase-setting condition.

The failure points back to the exact bivariate result: determinant reordering depends on mixed state–community response geometry, not on scalar nonlinearity in isolation.

### A fresh intervention identifies feedback as a phase-shaping condition

We then froze a directional test of state-adjustment feedback before running six previously unused seeds. Across the complete 18-block factorial surface, we compared a feedback knockout (`alpha=0`) with active adjustment (`alpha=0.15`), giving 108 paired block-by-seed comparisons.

The knockout produced **0/108** `C/I` reversals. Active feedback produced **52/108**. All 52 discordant pairs were in the predicted direction, with no opposite discordance and 56 ties.

The intervention did not simply increase interaction variance. Without feedback, all 108 cases were already `I>C` at `k=1`. Active feedback instead created a community-dominated low-aggregation regime in 52 cases; every one crossed to `I>C` by `k=4`. Feedback therefore changed phase topology: it created a regime boundary that aggregation could cross.

This result separates a mechanistic phase condition from the descriptive observation that nonlinear systems can reverse determinant rank.

### Real island interaction systems occupy a broad two-dimensional regime plane

The theory makes a measurement requirement rather than a literal natural prediction for synthetic `k`: realized partner breadth and temporal synchrony must be measured separately if determinant rankings are to be transported.

We froze a natural-regime admission and analysis protocol before candidate extraction. Eligible public systems required machine-readable quantitative biotic interactions, stable site and partner identity, at least six aligned source-native time bins, at least three nonconstant partner series, known/equal/normalizable sampling effort and a reconstructible time-by-partner matrix. Natural breadth was defined as pooled effort-standardized Hill `D1`; synchrony was the Loreau–de Mazancourt `phi`. Systems within one study were not treated as independent studies. Dispersion summaries were source balanced.

The final primary plane contains **42 systems from six studies and five island or archipelago groups**: Hawaii (1), Mallorca (19), Tenerife (4), Cabrera (5), Martinique (10) and Great Britain/England STEP (3). Mallorca and Cabrera are separate studies but one Balearic archipelago group.

The predeclared external-regime gate was passed without retuning. Source-balanced breadth had `D1 q90/q10 = 4.521`, exceeding the frozen minimum of 2.0. Synchrony spanned `phi q90-q10 = 0.352`, exceeding the minimum of 0.20. The absolute source-balanced Spearman correlation between `log D1` and `phi` was 0.325, below the maximum of 0.80, and 26.2% of systems occupied the joint interquartile interior of the two axes, above the 20% minimum.

The result did not depend on the largest study. Removing all 19 Mallorca systems left 23 systems from five studies and five island groups. Breadth dispersion remained high (`D1 q90/q10 = 5.494`), synchrony span remained 0.352, interior occupancy was 26.1%, and `|rho_s| = 0.454`. Every predeclared dispersion criterion still passed.

The last admitted source is important methodologically because it expanded the synchrony axis. EuPPollNet had classified the Roberts England study as an island study before this analysis. Before its coordinates were opened, we froze the source-native design as four rounds per year in 2012 and 2013 with equal 30-minute, 300-m2 site-round effort, and admitted only the three sites with complete 4+4 outcome-independent flower-count schedules. Their subsequent synchrony estimates were high (`phi = 0.414–0.635`). Because admission preceded coordinate calculation, these systems were not selected for their location on the regime plane.

Once the full NEE routing criteria and leave-largest-source-out criterion were satisfied, the predeclared stop-early rule closed candidate hunting. Unresolved Aegean, Ireland and Sicily candidates remained unopened, and transport-blocked Mahé and Giannutri candidates were not reclassified as biological negatives.

The natural result is therefore not that the synthetic determinant crossover has been observed in these 42 systems. It is that real systems occupy the two-dimensional context space in which a one-coordinate determinant ranking would be expected to lose transportability under nonlinear response.

### Existing island literature does not measure the full determinant–outcome contract

A separate literature audit was frozen before the natural-regime search and remains unchanged by it. The formal universe contains 25 research entries representing 21 exact geographic-overlap labels. Direct comparable plant response is available for 21/25 entries and direct partner arrival or replacement for 2/25, but **0/25** provide the full outcome-independent source-state → transition → local realization → plant-response contract. Formal external prediction of the full synthetic mechanism is therefore `not_evaluable` from that audit.

The later natural-regime analysis closes a different measurement gap: it demonstrates that breadth and synchrony can be reconstructed from a subset of public repeated-interaction datasets. It does not add matched plant-response outcomes to those systems and therefore does not alter the frozen 0/25 result.

This distinction matters. The natural regime plane shows that the theoretical context dimensions are ecologically non-vacuous and broadly occupied. The identifiability audit shows why existing literature cannot tell us whether a determinant ranking estimated in one part of that plane should transport to another.

## Discussion

### “What matters most?” is incomplete without a regime coordinate

Variance partitions and variable-importance rankings are often treated as summaries of ecological causation. Our results show a more limited interpretation is necessary. Even when the variables being partitioned do not change, their rank can change as community breadth, synchrony and state-dependent feedback alter the response geometry.

This is not a generic objection to ranking determinants. The bilinear null identifies conditions under which ranking is stable. When the response is effectively bilinear and second-order equivalence captures the relevant community distribution, `C` and `I` share a common multiplier and cannot reverse. The problem appears when nonlinear response retains information beyond the equivalence property used for compression.

The practical implication is that a determinant ranking should be indexed to the ecological regime in which it was estimated. A statement such as “community composition dominates initial state” is transportable only if the receiving system occupies a sufficiently comparable breadth–synchrony regime and if the relevant mixed response geometry is stable.

### Effective numbers are equivalence coordinates, not universal state variables

The argument is not that effective numbers are defective. They are exact for the properties they are defined to preserve. `k_eff` is exact for the variance of the pooled mean under the stated covariance model. Hill numbers are exact diversity equivalents for their corresponding diversity measure. Synchrony indices summarize aggregate covariance structure. Problems arise only when an equivalence coordinate is silently promoted to a complete nonlinear ecological state descriptor.

Our common-factor calculation makes this failure explicit: fixing the variance-equivalent coordinate leaves higher cumulants free. The quadratic state–community result then shows how those higher moments enter pure and mixed response terms differently. The discrete-support counterexamples retained in the repository provide a second, distinct route to non-equivalence: systems can share a second-moment effective number while differing in realized identity support.

Breadth and synchrony therefore should not be collapsed into a single natural “effective k” in this manuscript. They are measured independently because they encode different forms of ecological information.

### The natural regime map is an external constraint, not a mechanism validation

The 42-system analysis plays a precise role. It tests whether the axes required by the theory are estimable and meaningfully occupied in real island interaction systems. The answer is yes under a predeclared admission rule, and the result is not carried by Mallorca, the largest source.

It does not test whether the same `C/I` crossover occurs in nature. Doing so would require repeated breadth and synchrony estimates together with matched focal-state and outcome measurements on the same source-native units. The frozen 0/25 audit shows that this contract is currently absent from the formal island evidence universe.

This separation protects against two opposite errors: treating simulations as biologically self-validating, and treating heterogeneous natural examples as though they directly estimate the synthetic mechanism. The correct synthesis is narrower. Nonlinear theory shows why determinant order can depend on regime; two models establish that the boundary can be crossed and identify a feedback condition; natural systems show that the required regime space is real and broad; metadata show that full transport of determinant rankings remains empirically unidentified.

### Failed predictions are informative about the level of mechanism

The failed Holling-curvature prediction is central rather than embarrassing. It distinguishes scalar nonlinearity from mixed state–community geometry. A model can be strongly nonlinear in a scalar response while lacking the mixed derivatives needed to change the relative contribution of state and community realization. The fresh feedback intervention then targets the missing level directly and succeeds on unused seeds.

This sequence provides a stronger causal interpretation than selecting a successful correlational diagnostic from the original parameter grid. It also suggests an empirical design principle: if determinant-rank change is of interest, measure feedback pathways capable of coupling focal state to realized community context rather than relying only on scalar response curvature.

### A measurement agenda for comparative ecology

The combined results suggest a simple order of operations for comparative ecological studies.

First, define the equivalence property of any scalar compression being used. Second, measure context coordinates that can vary independently under the hypothesized response operator. For community-mediated responses, partner breadth and synchrony are natural candidates. Third, estimate determinant rankings within that declared regime rather than assuming global portability. Finally, collect matched outcome data if transport across regimes is the inferential target.

The 0/25 audit shows that the final step is uncommon in the present island literature, even though many individual ingredients are well documented. The natural-regime reconstruction shows that the context side of the contract is already recoverable in some public datasets. Future studies can therefore close the missing link prospectively rather than by adding more cross-sectional examples.

## Methods

### Variance decomposition and analytical null

For response matrices `Y_ir`, indexed by focal state `i` and stochastic community realization `r`, we used the exact two-way sum-of-squares decomposition `SS_tot = SS_S + SS_C + SS_I`. Normalized shares were `S`, `C` and `I`. The decomposition is descriptive; labels do not imply causal identification by themselves.

The bilinear null, common-factor cumulant calculation and exact quadratic state–community extension are specified in the frozen higher-order sufficiency design and implemented in `scripts/audit_chapter2_el_higher_order_sufficiency.py`.

### Nonlinear ecological models and prospective intervention

The plant–pollinator and adaptive consumer–resource models, seed sets, parameter grids and decomposition outputs were frozen before the higher-order interpretation. The scalar Holling fourth-curvature prediction was frozen before opening the setting-level outcome map and retained after failure. The mixed-feedback validation used six previously unused seeds and compared `alpha=0` with `alpha=0.15` over the complete 18-block factorial surface. A reversal was defined before execution as `C>I` at `k=1` and `I>C` at any later audited `k`.

### Natural-regime admission

The natural-regime gate was frozen on 13 September 2026 before candidate extraction. Public data had to predate the freeze and provide machine-readable quantitative biotic interactions, stable local-system identity, stable partner identity, at least six aligned source-native time bins, at least three nonconstant partner series, known/equal/normalizable sampling effort and a reconstructible time-by-partner matrix. Time bins, sites or taxa could not be selected from their eventual coordinates.

Each study received equal total weight in cross-system dispersion summaries. Multiple sites from one study contributed systems but not independent-study counts. Mallorca and Cabrera were treated as separate studies but the same Balearic archipelago group.

### Natural breadth and synchrony

For each system, interaction values were standardized by the source-native effort scalar frozen at admission. Pooled partner shares `p_j` defined breadth as

`D1 = exp[-sum_j p_j log(p_j)]`.

Synchrony was

`phi = Var_t(sum_j x_tj) / [sum_j SD_t(x_tj)]^2`

using nonconstant partner series. We also retained observed richness, `D1/richness`, median time-bin `D1`, mean pairwise correlation and the exchangeable-equivalent `rho_eq` as secondary descriptors. `rho_eq` was descriptive and was never interpreted as a literal natural pairwise correlation.

Uncertainty was assessed by 1,000 bootstrap resamples of source-native time bins with the prespecified seed. At least 800 valid synchrony replicates were required.

### Predeclared external-regime criterion

The NEE candidate gate required at least 12 systems, three independent source studies and two island/archipelago groups; source-balanced `D1 q90/q10 >= 2.0`; source-balanced `phi q90-q10 >= 0.20`; absolute source-balanced Spearman correlation between `log D1` and `phi <= 0.80`; at least 20% interior occupancy of the joint 25th–75th percentile rectangle; and survival of the numerical dispersion criteria after dropping the largest source study. The candidate search stopped early when these conditions were satisfied and leave-one-source-out robustness was evaluable.

### Frozen island identifiability audit

The formal metadata audit retained 25 research entries and was not renormalized after the natural-regime search. It classified whether each entry supplied comparable plant responses, direct partner arrival/replacement and the full outcome-independent Chapter 2 contract. The frozen result was 21/25 direct responses, 2/25 direct arrival/replacement and 0/25 full contracts. Later descriptive world-breadth extensions remain outside that denominator.

## Figure plan

**Figure 1 — Why determinant ranking can change.** Bilinear invariant, fixed-`k_eff` higher-cumulant divergence, and exact quadratic mixed-curvature condition.

**Figure 2 — Two nonlinear systems and a prospective mechanism test.** Plant–pollinator and consumer–resource determinant-order crossovers; failed scalar-curvature prediction; fresh feedback knockout versus active-feedback reversal counts.

**Figure 3 — Natural breadth–synchrony regime plane.** Forty-two systems, source-coded but source-balanced summaries; marginal distributions; thresholds shown as prespecified audit criteria rather than biological boundaries; inset showing leave-Mallorca-out result.

**Figure 4 — What current natural evidence can and cannot identify.** Measurement contract, 21/25 response coverage, 2/25 arrival/replacement, 0/25 full contracts, and prospective study-design handoff.

## Claim ceiling

Allowed:
- determinant ordering is regime dependent in the frozen nonlinear models;
- second-moment effective independence is an exact but restricted equivalence coordinate;
- mixed state–community feedback can create the phase boundary prospectively tested here;
- admitted natural island systems broadly occupy separate breadth and synchrony axes under the frozen measurement protocol;
- the regime-plane result survives removal of the largest source study;
- existing island literature lacks the full matched contract needed to claim natural transport of the synthetic determinant crossover.

Not allowed:
- a universal natural determinant ranking;
- a natural threshold corresponding to synthetic `k=4` or any other model value;
- literal substitution of natural Hill `D1` for synthetic `k`;
- claim that the 42-system regime map validates the synthetic `C/I` crossover in nature;
- historical Bombus-loss causation;
- renormalization of the frozen 25-entry audit using post-freeze sources;
- further candidate hunting to improve route metrics after the predeclared stop-early condition was met.
