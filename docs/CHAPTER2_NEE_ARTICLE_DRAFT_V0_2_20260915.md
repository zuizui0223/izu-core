# Determinant rankings in nonlinear ecology depend on breadth and synchrony

**Article type:** Article  
**Target:** *Nature Ecology & Evolution*  
**Status:** V0.2 — NEE-oriented manuscript surface after frozen natural-regime closure  
**Format guard:** abstract ≤200 words; main text ≤3,500 words excluding Methods, references and legends; 4 display items  
**Primary route receipt:** `data/results/chapter2_natural_regime_six_source_checkpoint_20260915.json`  
**Search closure:** `data/results/chapter2_natural_regime_search_closure_20260915.json`

## Abstract

Ecologists often ask which determinant matters most and then treat the resulting ranking as a portable property of a system. We show that this ordering can instead depend on ecological response regime. An exact bilinear null makes a variance-equivalent effective number sufficient: community and state-by-community contributions share one second-moment multiplier and cannot reverse rank. Higher-order theory identifies how this sufficiency fails under nonlinear mixed response geometry. Two structurally distinct ecological models cross the resulting boundary. A prespecified scalar-curvature prediction fails, whereas a prospectively frozen feedback intervention produces 52 community-to-interaction reversals in 108 comparisons and none without feedback. We then place 42 natural island interaction systems from six studies and five island groups on separately measured partner-breadth and temporal-synchrony axes. Their source-balanced regime plane spans both axes and satisfies a predeclared promotion criterion after removal of the largest study. Yet a frozen audit of 25 island studies finds no complete outcome-independent determinant–response contract. Determinant rankings are therefore conditional statements: transporting them across systems requires measuring the regime coordinates on which nonlinear responses depend.

Ecology compares causes by ranking effect sizes, variance components and predictive importance. Such rankings are useful only if their meaning survives transport. A driver that dominates in one system is often discussed as though it should dominate in another, even when the receiving system differs in diversity, interaction structure, stochastic forcing or feedback. This practice turns a local ranking into a system property without first asking whether the ordering itself is context dependent.

The problem is especially sharp when ecological context is compressed. Effective numbers replace structured collections of correlated units with simpler reference systems that preserve a declared quantity. Hill numbers preserve diversity equivalence (Jost, 2006); synchrony and portfolio metrics summarize aggregate covariance (Loreau & de Mazancourt, 2008; de Mazancourt et al., 2013). These reductions are informative because they say exactly what is preserved. They need not preserve a nonlinear response to the underlying structure.

Consider `k` equal-variance community components with common pairwise correlation `rho`. Their mean has the same variance as the mean of

`k_eff = k / [1 + (k-1)rho]`

independent components. This equivalence is exact for that second moment. In a bilinear state–community response, the same variance factor multiplies additive community variation and state-by-community interaction variation, so those components cannot reverse order at fixed coefficients. Any such reversal therefore diagnoses information that the second-moment compression does not contain.

This gives a falsifiable route from mathematics to comparative ecology. First, identify the exact sufficiency boundary. Second, ask whether ecological nonlinearities cross it. Third, identify a phase-shaping condition prospectively rather than selecting a successful explanation from the same simulations. Finally, ask whether natural systems actually occupy distinct values of the context dimensions that the theory says should remain separate.

Island interaction systems provide a stringent external setting because insularity reorganizes partner breadth, composition, turnover and stochasticity, while island-syndrome studies often seek general directional or determinant-level conclusions. We do not test a universal island-syndrome effect. Instead, we use island systems to ask whether breadth and synchrony form a real two-dimensional context space and whether the existing literature measures enough of the determinant–outcome chain to transport rankings across that space.

We combine exact analysis, two nonlinear model classes, a failed prespecified prediction, a fresh-seed intervention, a result-blind natural-data search and a frozen 25-entry identifiability audit. The resulting claim is deliberately conditional: **dominant ecological determinants can change rank across response regimes, so determinant rankings should be indexed to the breadth and synchrony context in which they were estimated.**

## Results

### A second-moment effective number has an exact sufficiency boundary

Let centered `X` denote focal state and `Zbar_k` the mean of `k` exchangeable centered community variables with variance `sigma^2` and common correlation `rho`. For

`Y = aX + b Zbar_k + c X Zbar_k`,

write

`tau_k = Var(Zbar_k) = sigma^2[rho + (1-rho)/k] = sigma^2/k_eff`.

With `X` independent of `Zbar_k`, the exact functional decomposition is

`S = a^2 Var(X)`,  
`C = b^2 tau_k`,  
`I = c^2 Var(X) tau_k`.

Hence `I/C = c^2 Var(X)/b^2`. Aggregation and synchrony can make the constant state component `S` overtake both realization-linked components, but cannot reverse `C` and `I`. This is the null against which nonlinear response is tested.

The first missing information is higher order. For a smooth response to centered pooled variation `Z`,

`E[f(mu+Z)] = f(mu) + f''(mu)kappa_2/2 + f'''(mu)kappa_3/6 + f''''(mu)(kappa_4+3kappa_2^2)/24 + ...`.

Variance equivalence fixes `kappa_2`, but not `kappa_3`, `kappa_4` or higher cumulants. Under a common-factor construction, equal `k_eff` therefore leaves higher cumulants free even when the pooled variance is identical.

A scalar expansion is insufficient to predict component rank because `I` is generated by mixed state–community geometry. In the exact centered quadratic extension

`Y = aX + bZ + cXZ + (d/2)(Z^2-tau) + (e/2)X(Z^2-tau)`,

the community and interaction components are

`C = b^2 tau + bd mu_3 + (d^2/4)Var(Z^2)`

and

`I = Var(X)[c^2 tau + ce mu_3 + (e^2/4)Var(Z^2)]`.

For symmetric `Z`, the sign of the change in `I/C` with fourth-order variation is the sign of `e^2 b^2 - c^2 d^2`. Second-moment sufficiency thus survives this order only under a restrictive alignment of pure and mixed response curvature.

### Two nonlinear ecological systems reverse determinant order

We next tested whether the analytical boundary is crossed in ecological models with different internal structures.

In a plant–pollinator response model, plant state interacts with stochastic partner identity, trait matching, breadth, arrival, loss and effectiveness. Across six frozen seeds, median normalized `(S,C,I)` changed from `(0.026, 0.730, 0.247)` at `k=1` to `(0.273, 0.235, 0.495)` at `k=4` and `(0.558, 0.127, 0.320)` at `k=16`. `I/C` increased from 0.34 to 2.52. Community and interaction contributions therefore reversed order rather than merely being overtaken by state variation.

A structurally separate adaptive consumer–resource model crossed the same boundary. Across 54 settings and six frozen seeds, 255/324 setting-by-seed trajectories contained an interaction-dominated intermediate scale, 111/324 crossed the `C/I` boundary and 68/324 followed a community-dominated → interaction-dominated → state-dominated winner sequence. Eighteen of 54 settings reversed `C/I` in at least four of six seeds.

These model results establish regime-dependent rank, not a natural threshold at a particular synthetic `k`.

### A failed prediction isolates the wrong level of nonlinearity

We first froze a scalar mechanism based on fourth-order curvature of the Holling-II response before opening the consumer–resource setting map. The curvature index increased strongly with handling parameter `h`; the prediction was therefore that larger `h` would produce more `C/I` reversals.

It did not. Summed reversal counts were 41 at `h=1`, 38 at `h=2` and 32 at `h=4`. Among 18 matched high- versus low-`h` blocks, zero increased, 16 tied and two decreased. Scalar saturation curvature was therefore not the phase-setting condition.

The failure is informative because the exact theory points to a different object: mixed state–community geometry. A response can be strongly nonlinear in one scalar while lacking the mixed derivatives needed to reorganize the relative contribution of state and realized community.

### A fresh intervention identifies feedback as a phase-shaping condition

Guided by that failure, we froze a directional feedback test before running six previously unused seeds. Across the complete 18-block factorial surface, a feedback knockout (`alpha=0`) was compared with active state adjustment (`alpha=0.15`), giving 108 paired block-by-seed comparisons.

The knockout produced **0/108** `C/I` reversals. Active feedback produced **52/108**. All discordant pairs were in the predicted direction and none were opposite. The intervention did not simply inflate interaction variance: without feedback, all 108 cases were already `I>C` at `k=1`; active feedback instead created a community-dominated low-aggregation regime in 52 cases, and every one crossed to `I>C` by `k=4`.

Feedback therefore changes phase topology. It creates a determinant-order boundary that aggregation can traverse.

### Natural island systems broadly occupy separate breadth and synchrony axes

The theory does not license literal substitution of natural diversity for synthetic `k`. It instead yields a measurement requirement: partner breadth and temporal synchrony should be measured separately before determinant rankings are transported.

We froze a public-data admission and analysis protocol before candidate extraction. Eligible systems required machine-readable quantitative biotic interactions, stable local-system and partner identity, at least six aligned source-native time bins, at least three nonconstant partner series, known or normalizable sampling effort and a reconstructible time-by-partner matrix. Breadth was pooled effort-standardized Hill `D1`; synchrony was Loreau–de Mazancourt `phi`. Multiple systems from one study did not count as independent studies, and cross-system summaries were source balanced.

The final primary plane contains **42 systems from six studies and five island or archipelago groups**: Hawaii, Mallorca, Tenerife, Cabrera, Martinique and Great Britain. The source-balanced `D1` q90/q10 ratio was **4.521**, the `phi` q90–q10 span was **0.352**, the absolute source-balanced Spearman correlation between `log D1` and `phi` was **0.325**, and **26.2%** of systems occupied the joint interquartile interior. All exceeded the predeclared external-regime criteria.

The formal robustness criterion also passed. Removing all 19 systems from Mallorca, the largest study, left 23 systems from five studies and five island groups; `D1` q90/q10 was **5.494**, `phi` span remained **0.352**, interior occupancy was **26.1%** and `|rho_s|` was **0.454**.

The last admitted source, England STEP, expanded the high-synchrony edge. Its island-study classification came from the source compilation before our analysis. Before coordinates were opened, we froze four source-native rounds in each of 2012 and 2013, equal 30-minute and 300-m2 effort, and admitted only three sites with complete 4+4 outcome-independent survey schedules. Their `phi` values were 0.450, 0.635 and 0.414. An independent reconstruction reproduced every committed `D1` and `phi` exactly; removing zero-interaction rounds only for diagnosis retained high `phi` values of 0.411, 0.618 and 0.364.

An additional post-promotion all-source leave-one-study-out diagnostic reveals where replication is still thin. Removing England reduces the source-balanced `phi` span to **0.162**, below the predeclared 0.20 promotion threshold; removing Martinique lowers interior occupancy to **18.75%**. These diagnostics do not redefine the frozen promotion rule, which required removal of the largest study, but they show that the present natural plane does not redundantly sample every region from multiple sources. We therefore interpret the plane as evidence that the two-dimensional regime space is real and broadly occupied, not as evidence that each part of that space is source-invariant.

Candidate searching stopped under the predeclared early-stop rule once the full criterion and largest-source robustness passed. Unresolved sources remained unopened rather than being pursued to strengthen the route.

### Existing island literature cannot yet transport determinant rankings

A separate formal audit, frozen before the natural-regime search, contains 25 research entries across 21 exact geographic-overlap labels. Direct comparable plant responses were available in **21/25** entries and direct partner arrival or replacement in **2/25**, but **0/25** supplied the complete outcome-independent source-state → transition → realized-community → plant-response contract.

The natural-regime reconstruction closes only the context side of that measurement problem. It shows that breadth and synchrony can be estimated from suitable public repeated-interaction data, but it does not add matched plant-response outcomes to those systems and therefore does not change the 0/25 result.

Together, the two natural layers set the empirical boundary. Island interaction systems occupy distinct breadth–synchrony regimes, but existing studies do not yet provide the matched outcome structure required to test whether a determinant ranking measured in one regime transports to another.

## Discussion

Our results change the interpretation of “what matters most” in nonlinear ecology. A determinant ranking can be stable under an exact bilinear null yet reverse when response geometry retains information beyond the second moment used to compress community structure. In that setting, the ranking is not an intrinsic label attached to the system. It is a conditional statement about the regime in which the system was observed.

The analytical result also clarifies what effective numbers can and cannot do. Effective numbers are not flawed approximations; they are equivalence coordinates. `k_eff` is exact for the variance property it is defined to preserve, and Hill numbers are exact diversity equivalents for their chosen order. The error is to promote an equivalence coordinate to a complete nonlinear state descriptor without showing response sufficiency. Higher cumulants and discrete identity support can remain unconstrained, and mixed state–community curvature determines whether those omitted features matter for determinant order.

The failed Holling prediction is important for the same reason. Scalar nonlinearity alone did not identify the phase boundary. A prospectively frozen feedback intervention did. This directs mechanistic attention toward pathways that couple focal state to realized community context, rather than toward one-dimensional curvature indices.

The natural regime plane gives the theory an external ecological constraint. Six independent source studies occupy a broad two-dimensional breadth–synchrony space under a result-blind admission protocol, and the predeclared criterion survives removal of the largest source. The additional all-source sensitivity analysis is less reassuring and more informative: the high-synchrony edge is currently supplied by England STEP, while Martinique contributes materially to interior coverage. The strongest natural claim is therefore about **existence and occupancy of the regime space**, not universal redundancy of that occupancy across sources. Replication should now target those under-redundant regions prospectively rather than reopen candidate hunting post hoc.

This framing has a direct implication for island-syndrome research. Conflicting mean shifts or driver rankings across island studies need not imply that one study is wrong or that a single universal syndrome is merely noisy. They may arise because studies sample different response regimes. Our data do not test that explanation for any particular floral, reproductive or life-history syndrome, so it remains a prediction. But the 0/25 audit explains why the prediction is currently difficult to evaluate: outcome-rich island studies rarely measure the transition and context coordinates needed to transport a determinant ranking.

The same logic extends beyond islands. Comparative ecology often aggregates across systems that differ in interaction breadth, synchrony, feedback and stochastic realization. Meta-analytic heterogeneity is usually treated as residual variation to be modeled after the fact. A regime-based approach instead asks whether a ranking should have been expected to transport at all. The practical sequence is simple: define what a scalar compression preserves; measure context coordinates that can vary independently under the response operator; estimate determinant rankings within declared regimes; and collect matched outcomes when cross-regime transport is the inferential target.

Several boundaries remain. The natural systems do not validate the synthetic `C/I` crossover, and natural Hill `D1` is not synthetic `k`. The NEE routing threshold is an internal, predeclared manuscript-promotion criterion rather than a biological boundary. The all-source diagnostic shows that the natural plane still has source-specific leverage. The consumer–resource generalization was motivated after the original plant–pollinator pattern, although the feedback intervention itself used unused seeds after prospective freezing. These boundaries are part of the result: they distinguish a falsifiable claim about regime-dependent determinant order from a universal claim that the available evidence does not support.

Determinant rankings should therefore be reported as conditional ecological objects. When nonlinear response is plausible, breadth and synchrony are not nuisance descriptors to compress away; they are coordinates of the regime in which “what matters most” is defined.

## Methods

### Response decomposition and analytical null

For response matrices `Y_ir`, indexed by focal state `i` and stochastic community realization `r`, total variation was partitioned exactly as `SS_tot = SS_S + SS_C + SS_I`. Normalized shares `S`, `C` and `I` represent additive focal-state variation, additive community-realization variation and the non-additive state-by-community remainder. The decomposition is descriptive rather than a causal identification scheme.

The bilinear null, common-factor cumulant expansion and exact quadratic mixed-response model were fixed in the higher-order sufficiency design. The bilinear null identifies the invariant `I/C`; the higher-order calculations identify distributional information omitted by variance equivalence and the mixed-curvature condition under which it changes component rank.

### Nonlinear model classes and prospective intervention

The plant–pollinator model evaluated 21 focal starting states across stochastic community realizations and pooled independent trajectories over `k={1,2,4,8,16}`. The structurally separate adaptive consumer–resource model crossed resource number, matching width, handling, adaptation and aggregation levels over six frozen seeds. The failed handling-curvature prediction was frozen before opening its setting-level outcome map.

The later mixed-feedback test was frozen before execution on six previously unused seeds. Across 18 matched factorial blocks, `alpha=0` and `alpha=0.15` were compared using 256 realizations at each audited aggregation level. The primary outcome was defined in advance as `C>I` at `k=1` followed by `I>C` at any later `k`.

### Natural-regime admission and provenance

The natural-data gate was frozen on 13 September 2026 before candidate extraction. Data had to be public before the freeze and provide quantitative biotic interactions, stable local-system and partner identity, at least six aligned source-native time bins, at least three nonconstant partner series, known/equal/normalizable sampling effort and a reconstructible time-by-partner matrix. Unavailable data were not biological negatives. Candidate searching followed a result-blind source order and stopped when the predeclared early-stop criterion was satisfied.

Systems from one study were retained as systems but not counted as independent studies. Mallorca and Cabrera are separate source studies but one Balearic island group. Great Britain retained the island-study classification assigned by the source compilation before our route result was known.

### Natural breadth and synchrony

Within each system, interaction values were standardized by the source-native effort scalar fixed at admission. Pooled partner shares `p_j` defined breadth as

`D1 = exp[-sum_j p_j log(p_j)]`.

Synchrony was

`phi = Var_t(sum_j x_tj) / [sum_j SD_t(x_tj)]^2`

using nonconstant partner series. Systems passing the six-bin minimum were retained according to the frozen precision rule. Uncertainty was estimated with 1,000 bootstrap resamples of source-native time bins.

For cross-system summaries, each source study received equal total weight. The predeclared promotion criterion required at least 12 systems, three studies and two island groups; source-balanced `D1` q90/q10 ≥2.0; `phi` q90–q10 ≥0.20; absolute source-balanced Spearman correlation between `log D1` and `phi` ≤0.80; at least 20% joint interquartile interior occupancy; and persistence of the numerical dispersion criteria after removing the single largest study.

### Literature identifiability audit

The formal island audit retained the original denominator of 25 research entries. Each entry was scored for directly observed comparable plant response, direct partner arrival or replacement and the full outcome-independent Chapter 2 measurement contract. Missing axes were not inferred from outcomes or narrative interpretation. Later descriptive source expansion and the natural-regime search did not alter this denominator.

### Reproducibility and claim control

Admission records, source hashes, adapters, frozen analysis plans, route checkpoints, search closure and post-promotion diagnostics are versioned in the repository. The England source was admitted and its adapter frozen before its coordinates were opened. A second implementation independently reconstructed its `D1` and `phi` values exactly. The all-source leave-one-study-out analysis was performed only after the promotion decision and is reported as a transparency diagnostic, not as a retroactive route rule.

## Data and code availability

All analysis code, source-lock records, frozen design objects, failed and successful prediction receipts, natural-regime coordinates and routing diagnostics are maintained in `izu-core`. A permanent archived release and DOI will replace this repository-only statement before submission. Public source datasets retain their original licences and citations.

## Figure plan

**Figure 1 | Exact sufficiency boundary for determinant rank.** Bilinear `I/C` invariant; fixed-`k_eff` higher-cumulant divergence; exact quadratic mixed-curvature condition.

**Figure 2 | Nonlinear determinant-order transitions and prospective mechanism test.** Plant–pollinator and consumer–resource rank trajectories; failed scalar-curvature prediction; fresh feedback knockout versus active-feedback reversal counts.

**Figure 3 | Natural breadth–synchrony regime plane.** Forty-two systems coded by source and island group; source-balanced marginal summaries; predeclared promotion criteria shown as analysis thresholds, not biological boundaries; leave-Mallorca-out inset.

**Figure 4 | Measurement ceiling and transportability.** Full determinant–response contract, 21/25 direct response coverage, 2/25 direct arrival/replacement and 0/25 complete contracts, linked to the prospective cross-regime design.

## Claim ceiling

Allowed:
- determinant order is regime dependent in the frozen nonlinear models;
- the bilinear second-moment reduction has an exact sufficiency boundary;
- mixed state–community feedback creates the prospectively tested phase boundary;
- admitted natural island interaction systems broadly occupy separate breadth and synchrony axes under the frozen protocol;
- the predeclared natural-plane criterion survives removal of the largest source;
- additional all-source diagnostics show where source redundancy is incomplete;
- existing island literature does not identify natural transport of the synthetic determinant crossover.

Not allowed:
- a universal natural determinant ranking;
- a biological threshold at `D1`, `phi` or synthetic `k`;
- literal substitution of natural Hill `D1` for synthetic `k`;
- a claim that the 42-system plane validates the synthetic `C/I` crossover in nature;
- a claim that every region of the natural plane is robust to deletion of every source;
- historical pollinator-loss causation from the present analyses;
- reopening candidate hunting after the predeclared early-stop closure.
