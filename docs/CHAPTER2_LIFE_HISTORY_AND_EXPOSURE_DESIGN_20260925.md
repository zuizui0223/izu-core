# Life history and effective exposure: proposed model-3 extension

Status: design only, before model-3 simulation. Requested on 2026-09-25. It does not reinterpret the archived model's k as lifespan, patch count or generations, and does not postpone closure of the bounded Chapter 2 response-regime analysis.

Implementation update: the first calculation unit is now implemented in `scripts/model3_reproduction.py` and `scripts/model3_exposure.py`: delayed-selfing reproductive accounting, declared survival/flowering schedules and the scalar variance-equivalent exposure diagnostic. `scripts/verify_model3_reproduction_exposure.py` emits the source-matched mathematical receipt. This does not implement visitor-transfer generation, inheritance or an evolutionary population simulation. See `MODEL3_IMPLEMENTATION_LEDGER_20260925.md` for tests and review.

## Ecological question

Does life history change how a plant integrates fluctuating pollinator communities, and therefore the distribution of reproductive outcomes and selection on floral traits?

Treat life history as a biological modifier of exposure and demographic consequences, not a synonym for k. Lifespan, number of flowering episodes, reproductive weights, and correlation among those episodes are different quantities. An annual may experience many distinct visitor contexts within a long flowering season; a long-lived perennial may repeatedly encounter similar contexts or contribute most of its offspring in one season.

## Three clocks and a generational correction

1. Within-flowering-season intervals: visitor activity, access, pollen movement and fertilization opportunities.
2. Plant years or reproductive seasons: survival, maturity, flowering probability and allocation to reproduction; skipped reproduction is explicit.
3. Generational change: recruitment and inherited traits. With overlapping perennial generations, a year is not a generation and there is no single replacement of all adults at the end of each season.

The non-overlapping annual limit can use one life-cycle step per generation. A life-history extension requires a stage/age-structured seasonal or annual clock with rates defined for that interval. The old 120 uncalibrated steps do not automatically become 120 generations or years. Existing arrival/loss probabilities must not be transplanted to a new timescale without a separate assumption or calibration.

## Minimum declared life-history variables

| Variable | Biological role | Control needed |
|---|---|---|
| Flower lifespan and opening schedule | Determines exposure to within-season visitor variation | Same total floral effort spread over different schedules |
| Age/stage at first reproduction | Delays reproductive contribution | Separate maturity timing from adult survival |
| Adult survival and probability of flowering | Determines repeated opportunities and overlapping generations | Compare repeated reproduction at matched expected effort, then allow real effort differences |
| Effort across episodes | Determines which encounters contribute to offspring | Predeclare resource/flower-effort weights; do not choose weights using outcomes being predicted |
| Visitor temporal covariance | Determines how redundant successive experiences are | Same marginal community distribution, varied autocorrelation/cross-episode dependence |
| Seed survival/dormancy | Buffers lineages across years rather than giving an adult extra pollination encounters | Optional separate seed-bank module; do not add seed-bank years to adult exposure k |

Start with a declared annual versus iteroparous-perennial comparison. Keep seed-bank evolution, size-dependent maturation and resource storage as separate extensions unless the focal hypothesis requires them. Life-history differences should be empirically parameterized where possible and otherwise reported as scenarios, not taxonomic constants.

## How k is related, and why it is not identical

For a diagnostic scalar exposure X_t with equal marginal variance sigma squared, predetermined normalized weights w_t, and correlation matrix R, the weighted exposure has variance sigma squared times w-transpose R w. Define a **variance-equivalent exposure number**

`k_eff = 1 / (w^T R w)`

when the denominator is positive. For n equally weighted independent episodes this gives n; for perfectly correlated episodes it gives 1. Unequal weights can reduce effective exposure even with independence. Different variances require the full covariance expression and a declared reference variance. This is elementary variance accounting, not an equivalence theorem for ecological outcomes.

The original model concatenates independently generated visitor lists and weights them by their type counts. Its k is a computational intervention. The new k_eff would be a measured or model-derived diagnostic, not a replacement name for that intervention. A multidimensional community may need several covariance summaries; there may be no single sufficient k_eff. Female and male reproduction can also integrate episodes differently.

Do not average communities first and then compute a nonlinear reproductive outcome. Compute visits → pollen transfer → fertilization/offspring for each episode, respecting carryover/resource state, then combine demographic contributions. A lifetime sum of offspring and multiplicative lineage growth across generations are different quantities; neither can be substituted by an arithmetic community average. Where survival or effort depends on prior reproduction, weights are endogenous model outputs and cannot be treated as fixed independent input weights without qualification.

## Intuitive contrasts to illustrate

- One short flowering episode: a plant has limited opportunities to escape an unfavourable visitor realization.
- Several similarly weighted episodes with different visitor contexts: episodes may compensate for each other.
- Several strongly correlated episodes: repeated flowering may supply little environmental diversification.
- Long life but one dominant reproductive episode: nominal repetition can exceed effective repetition.

These are predictions to test after nonlinear fertilization, selfing and survival are included. Compensation may be weak, absent or outweighed by costs. A long-lived species is not automatically less pollen limited or more buffered.

## Prospective hypotheses, not predetermined results

H-L1: At matched marginal exposure and expected reproductive effort, distributing effort over weakly correlated episodes reduces variance of the linear exposure diagnostic. Whether it reduces reproductive failure or mixed functional responses is an additional biological test.

H-L2: Stronger temporal correlation or concentrated reproductive effort weakens the above diversification; nominal flowering count alone predicts less than the joint schedule/covariance description.

H-L3: Autonomous selfing changes the consequences of poor visitor episodes, conditional on timing, inbreeding depression and seed/pollen discounting. Its interaction with life history is not assumed monotonic.

H-L4: Delayed or overlapping reproduction changes the relationship between elapsed years and evolutionary response; changes in floral traits must be compared both at calendar horizons and at declared demographic/generational summaries.

H-S (conditional, model 3): Under a smooth single-attractor fitness landscape and adequate evolutionary time/standing variation, dependence on initial traits may weaken relative to the original best-target model. Alternatives are persistent starting-state dependence under multiple attractors, genetic constraints, weak selection or finite time. A centroid result does not prove S must disappear. S measures variation in the specified outcome, not simply preservation of traits.

These qualitative hypotheses are recorded before model-3 execution. A numerical protocol must still specify the exact life cycle, parameter/source ranges, horizons, replication and endpoints before outcomes are inspected. Do not choose G, survival or episode counts to obtain a desired S/C/I ordering.

## Field and Q1 connection

Link repeated tagged-plant measurements of flowering schedule and survival to effort-standardized visitor records, single-visit pollen deposition, pollination treatments and mature offspring. E3/E4-style pollen/reproduction measurements are relevant but alone do not identify lifetime demographic contribution or paternal fitness. Multi-year survival/reproduction and, where male genetic success is claimed, paternity evidence are additional data.

For Q1, compare floral patterns across life-history strata only after verifying coverage and observation scale. Region is not a lifespan proxy; current adult flowering schedules do not automatically reveal historical evolution. Evaluate interactions among floral traits, visitor context and measured life history without assigning regions to k values. Maintain the distinction between within-lineage change and floristic sorting.

## Primary-source grounding

- [Xu et al. (2021), The evolution of flower longevity in unpredictable pollination environments](https://doi.org/10.1111/jeb.13936): theoretical connection between pollination uncertainty, flower longevity and temporal exposure. It does not equate species lifespan with k.
- [Life-History Evolution in Uncertain Environments: Bet Hedging in Time (2006)](https://doi.org/10.1086/506258): explicit life-history theory links environmental uncertainty and life-history delays; this motivates stage structure, not a universal benefit of perenniality.
- [Ehrlen & Lehtila (2002), How perennial are perennial plants?](https://doi.org/10.1034/j.1600-0706.2002.980212.x): demographic estimates across perennial plants emphasize that perennial status alone does not specify longevity.

The weighted covariance formula above is a direct diagnostic derivation. It is not attributed as an empirical finding of these studies. Source support here is at the accessible primary abstract/text level; the exact nonlinear model is still to be designed.
