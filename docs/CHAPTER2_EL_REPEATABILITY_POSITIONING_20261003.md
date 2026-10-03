# Chapter 2 — repeatability framing

**Date:** 2026-10-03  
**Status:** candidate framing on a separate branch; **preferred journal candidate: Evolution Letters**. Ecology Letters remains a fallback only if the paper is recast around a general ecological contribution. This does not replace the locked Oikos submission surface.  
**Parent scientific object:** unified Model 3 integrated syndrome candidate.

## Journal-fit decision — 2026-10-03

### Preferred candidate: Evolution Letters

The current paper asks an evolutionary question: when an apparent increase in directional similarity reflects stronger repeatability versus when it arises through opposite changes in reproducible historical structure. The plant–pollinator island model is the biological testbed, not the final ecological endpoint.

Current official fit:
- *Evolution Letters* publishes theoretical and empirical work across evolutionary biology that substantially advances the field or has broad interest;
- a typical Letter is approximately 5,000 words excluding display items, with an abstract up to 300 words;
- the current draft is 4,697 main-text words and 218 abstract words.

### Fallback: Ecology Letters

*Ecology Letters* requires a substantial nexus with general ecology and notes that purely evolutionary contributions are rarely published. Its Letter format allows 5,000 main-text words but only a 150-word abstract.

The current manuscript should therefore **not** be submitted there unchanged. An Ecology Letters route would require recentering the contribution on ecological history averaging, partner-community composition and finite-population ecology, plus abstract compression.

### Decision boundary

This is a **journal-fit recommendation**, not a submission action. The branch remains draft and the active Oikos surface remains unchanged until an explicit promotion/submission decision.

## Editorial-level question

> **When does greater directional similarity actually mean greater evolutionary repeatability, and when can it mask a persistent historical imprint?**

The island connection is not decorative. Island floral syndromes are treated as a natural class of repeated ecological problems: altered pollinator service, functional replacement, restricted connectivity and finite populations recur across islands, yet detailed floral outcomes are heterogeneous.

## Evidence hierarchy

The manuscript keeps different biological objects separate rather than estimating one universal repeatability coefficient.

1. **Immediate reproductive selection** — functional matching/rematching can redirect selection across starting floral states.
2. **Conditional deterministic closure** — the same reproduction and inheritance operator can be propagated without demographic sampling, but this layer is not the stochastic mean of the finite ABM.
3. **Occupied finite-population realization at the focal horizon** — this is the core comparison. The natural bridge has a negative aggregate mean and complete occupancy, but sign labels are repeat-sensitive. An exact-source exploratory decomposition shows a reproducible continuous visitor-history component beneath demographic noise.
4. **Genetic accessibility** — reduced standing variation slows early response on the constrained axis; continuing mutation narrows and eventually reverses that early ranking.
5. **Persistence boundary** — a prospectively frozen depression scan shows that the isolation-driven deterministic closure remains negative-only among every tested history whose three starts and both near/far arms retain terminal mass >=1. Mixed deterministic labels appear only after at least one endpoint crosses below one expected individual.

The result is not “island syndrome is universal.” It is:

> **Within the occupied 200-season finite ABM, directional sign uniformity and reproducibility of visitor-history effects are distinct properties.**

The broader logical implication is:

> **Greater directional similarity does not, by itself, identify weaker historical contingency or a more repeatable evolutionary mechanism.**

Natural-island prevalence, effect sizes, long-run attractors and route ordering remain empirical questions.

## Finite-history signal diagnostic

Because mean sign labels were unstable across demographic repeats, we reanalysed the exact verified finite-ABM bridge tensors as an explicitly **post-hoc exploratory diagnostic**.

Under natural visitor histories:
- history-structured variance: **0.00549**;
- demographic residual variance: **0.02677**;
- single-trajectory ICC: **0.170**;
- reliability of the declared eight-repeat mean: **0.621** (95% bootstrap interval 0.549–0.681);
- first-four versus last-four history correlation: **0.690** (0.592–0.770).

Two interventions both made directional sign labels more uniform but changed historical structure in opposite directions.

- **Plant capacity 48→192:** mixed histories 12→1; repeat-label disagreement 97→31; eight-repeat reliability **0.621→0.825**; split-half history correlation **0.690→0.852**.
- **Pooling visitor histories:** mixed histories 12→0; repeat-label disagreement remains 77; eight-repeat reliability **0.621→0.103**; split-half history correlation **0.690→0.214**.

Thus fewer mixed-sign histories can mean either that demographic noise has fallen while history-specific magnitudes become more reproducible, or that environmental averaging has erased the history signal. Sign uniformity alone is not a sufficient repeatability metric.

## Prospective new-demographic-seed validation

The exploratory diagnostic generated a fixed prediction. Before any new demographic execution, we froze seeds **201–204**, retained all 128 original visitor histories and three starts, and declared the ordering **capacity 192 > natural > visitor pooled** for discovery-to-validation history correlation. Strong success additionally required the paired bootstrap intervals for capacity minus natural to remain above zero and pooled minus natural below zero.

The validation ran **9,216 finite trajectories** with 100% terminal occupancy.

- **Capacity 192:** discovery→validation history correlation **0.918** (0.893–0.941).
- **Natural:** **0.732** (0.633–0.805).
- **Visitor pooled:** **0.165** (0.008–0.326).
- Capacity minus natural: **+0.186**, paired 95% interval **+0.120 to +0.283**.
- Pooled minus natural: **−0.567**, **−0.732 to −0.401**.

The frozen strong-success rule therefore passed. This upgrades the mechanism from a post-hoc pattern to a **prospectively validated prediction across new demographic realizations**. It does not validate transfer to new visitor histories or natural islands; the discovery remains post-hoc.

## Critical population-scale audit

The prospective long-horizon work exposed an important distinction between two depression settings.

### Original focal bridge: depression 0.50

Exact-source rerun of all 128 histories × three starting states showed:

- deterministic far density mass at season 200: **48.0 in every history × start cell** to floating-point precision;
- finite far population in demographic replicate 101: mean **47.992**, median **48**, 100% occupied;
- frozen bridge: all **3,072 far** and **3,072 near** finite cases occupied.

Therefore the original -0.4510 deterministic headline is **not** a sub-individual-mass artefact.

### Later sensitivity: depression 0.75

At season 200:

- far deterministic density mass median: **0.000301**;
- **98.18%** of far history × start cells have density mass <1;
- in demographic replicate 101, **384/384 finite far populations were extinct**, median extinction season 61.

Therefore the previously reported 116 negative-only / 11 mixed / 1 positive-only deterministic history labels are retained only as a mathematical closure sensitivity. They are **not** population-level repeatability evidence.

## Deterministic closure boundary

The density implementation is explicitly a **conditional deterministic closure, not the stochastic mean** of the finite ABM.

Consequences:

- the -0.1446 finite versus -0.4510 density magnitude gap is not a finite-population attenuation coefficient;
- the capacity-48 → 192 movement numerically closes 41.5% of that trait-effect gap, but this is descriptive rather than convergence to a stochastic expectation;
- capacity effects on mixed-label and repeat instability remain valid finite-demographic sensitivity results.

## Measurement-literature boundary

### Oke et al. 2017 / Arendt et al. 2025 / Bisschop et al. 2026
DOIs: 10.1086/691989; 10.1086/736845; 10.1093/evlett/qrag017

Established: direction, angle and magnitude/length are distinct properties of evolutionary trajectories; Arendt et al. caution that general direction metrics are not automatically geometric parallelism measures; and Bisschop et al. show that environmental and demographic heterogeneity can reduce repeatability.

### Venkataram & Kryazhimskiy 2023
DOI: 10.1098/rstb.2022.0047

Established: repeatability is an ensemble property; directional similarity captures only one aspect and can ignore evolutionary rate/magnitude.

**Consequence for novelty:** do not claim that direction and magnitude are newly separated, or that environmental/demographic variation affecting repeatability is new. The remaining contribution is mechanistic: within one explicit eco-evolutionary operator, two interventions that both increase directional sign uniformity move reproducible visitor-history structure in opposite directions.

## Why this is not already Bolnick/Stuart/Thompson

### Bolnick et al. 2018 — (Non)Parallel Evolution
DOI: 10.1146/annurev-ecolsys-110617-062240

Established: parallel evolution is a continuum and ecological/genetic processes can alter parallelism.

Chapter 2 contribution: separate aggregate recurrence from realized trajectory-level heterogeneity inside one explicit eco-evolutionary operator and identify where ecological, reproductive, genetic and demographic filters enter.

### Stuart et al. 2017 — environment + genetics
DOI: 10.1038/s41559-017-0158

Established: environmental heterogeneity and gene flow jointly explain departures from parallel phenotypic evolution.

Chapter 2 contribution: manipulate visitor environment, reproductive context and genetic accessibility prospectively while retaining one reproductive/inheritance operator.

### Thompson et al. 2017 — many-to-one form–function mapping
DOI: 10.1111/evo.13357

Established: common function can coexist with non-parallel morphology when multiple forms map to similar function.

Chapter 2 contribution: a complementary route in which aggregate recurrence can coexist with non-uniform realized histories because selection, genetic accessibility and finite realization are distinct filters.

## Why islands remain central

Plant island syndromes are empirically heterogeneous rather than a single law.

- Hetherington-Rauth & Johnson (2020; DOI 10.1086/709018) tested 556 species in 136 phylogenetically independent island–mainland contrasts and found no global reduction in flower size, although some archipelagos showed it.
- Ciarle & Burns (2025; DOI 10.1080/0028825X.2024.2377418) reviewed plant island-syndrome components and found strongly uneven support across traits.
- Abe (2006; DOI 10.1093/aob/mcl117) documented an island pollination syndrome in the Ogasawara flora.
- Jezierski et al. (2026; DOI 10.1093/evolinnean/kzag008) showed that parallel island-syndrome phenotypes in British Isles wrens can coexist with largely population-specific genomic differentiation, blocking novelty claims based only on phenotype–genome decoupling.

## Safe novelty statement

> Measurement theory already separates direction from magnitude. Model 3 contributes a specific mechanistic counterexample: **the same increase in directional similarity can accompany either stronger reproducibility of history-specific effects or erosion of the history signal by environmental averaging.**

Do **not** claim:
- first connection between island syndrome and parallel evolution;
- first mechanism for non-parallel evolution;
- first phenotype–genome decoupling in an island syndrome;
- literal prediction of colour, corolla dimensions or named-island trajectories;
- universal ordering of genetic versus ecological constraints;
- one scalar repeatability parameter across unlike biological stages;
- depression-0.75 deterministic history labels as evidence about persisting populations;
- a stationary long-run island-syndrome attractor;
- sign-uniformity counts as a complete measure of repeatability;
- the finite-history variance diagnostic as preregistered rather than exploratory.

## Internal compact-format target

Evolution Letters is the preferred candidate but no submission action has been taken. Maintain these compact-format constraints:

- main text: <= 5,000 words (official Evolution Letters guide);
- abstract: <= 300 words (official Evolution Letters maximum);
- figures: 4 main figures.

These are internal drafting targets, not attributed journal requirements.

## Claim ceiling

1. **Established by simulation:** at the occupied depression-0.50 finite horizon, capacity scaling and visitor-history pooling both increase directional sign uniformity but generate opposite persistence of history-specific magnitude; the ordering was prospectively validated with new demographic seeds 201–204.
2. **General implication:** directional similarity alone does not identify whether historical contingency has weakened, become more reproducible relative to demographic noise, or been averaged away.
3. **Natural prediction:** repeated-population studies should estimate both response direction and reproducibility of effect magnitude; temporal accessibility rankings may additionally change as new variation accumulates.

The natural archive does not identify natural branch frequencies, transition rates, equilibrium times, effect sizes or a universal stage ordering.

## Figure 1 — biological-level repeatability map

**Panel A:** recurrent island-like pollination problem.

**Panel B:** state-dependent reproductive selection under functional rematching.

**Panel C:** conditional deterministic closure as a mechanistic comparator, explicitly not the stochastic mean.

**Panel D:** occupied finite-population bridge: sign uniformity versus continuous visitor-history reliability.

**Panel E:** genetic accessibility and finite demographic/history filters.

The visual should make the main distinction obvious: a population set can have one aggregate direction without every realized history sharing that direction.

## Main-text result spine

1. **A recurrent ecological problem does not imply one selection direction.**
2. **At the occupied focal finite-population window, directional sign uniformity and reproducible history-specific magnitude are different objects.**
3. **The deterministic closure is a comparator, not a finite-population expectation; depression 0.75 crosses a persistence boundary and is excluded from the repeatability headline.**
4. **Standing variation changes early response speed; continuing mutation can erase and reverse that ranking.**
5. **The same apparent gain in directional similarity can result from reduced demographic noise or from erasure of environmental-history structure; the universal assurance-by-cost route still fails its preregistered robustness rule.**

## Submission-order firewall

The locked Oikos surface remains untouched by this branch. Promotion requires a separate decision after:
- the population-scale audit is fully propagated;
- Figure 1 is regenerated;
- citations are source-checked;
- retained failed tests remain visible;
- journal target is chosen explicitly;
- submission gates are rerun.


### Persistence-boundary refinement

The original depression-0.75 mixed-history result was followed by a prospectively frozen exact-source scan at 0.55, 0.60, 0.65 and 0.70, then a separately frozen refinement at 0.71–0.74.

- depression 0.50–0.70: every one of 128 histories is negative-only; through 0.70 all histories retain all six terminal near/far starting-state masses >=1;
- depression 0.71: some start-arm cells cross below mass 1, but all 128 histories remain negative-only;
- depression 0.72: one mixed history appears, but its minimum terminal mass is 0.550; all 102 histories retaining all six masses >=1 remain negative-only;
- depression 0.73: one mixed history appears with minimum mass 0.0129; all 60 mass-valid histories remain negative-only;
- depression 0.74: eight mixed histories at epsilon 0 (two at epsilon 0.01), all in low-mass histories; the five histories retaining all six masses >=1 are all negative-only.

Therefore no deterministic history-level nonparallelism was observed among pre-quasi-extinction histories in the tested range. The depression-0.75 pattern is retained only as a persistence-boundary/closure diagnostic, not as evidence that deterministic evolutionary trajectories diverge among persisting populations.
