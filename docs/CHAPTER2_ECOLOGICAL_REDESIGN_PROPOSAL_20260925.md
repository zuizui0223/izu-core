# Reframing Q2: when does island community reassembly cause floral convergence or divergence?

Status: research-design proposal, not an executed model, frozen numerical protocol, or replacement of the archived simulation. User requested reconsideration of the evolutionary question on 2026-09-25. Local and remote baseline checked at `6fb643911a26ce4d94cbb4981715345dbc794ff6`; main remained `c788c740e9e103972ddc8d790829af595c4aa3ec`.

Subsequent scope decision: retain this as a proposed **third model class**, not a replacement of Chapter 2's archived plant model or a condition for finishing the current paper. The completed [response-regime control audit](CHAPTER2_RESPONSE_REGIME_REAPPRAISAL_20260925.md) preserves mixed individual responses under all tested richness-matched rules while narrowing turnover and mean-flip claims. The requested [life-history extension](CHAPTER2_LIFE_HISTORY_AND_EXPOSURE_DESIGN_20260925.md) separates seasonal exposure, individual survival and overlapping generations; the single-generation clock below applies only to the non-overlapping baseline.

## Purpose and decision

Retain the ambitious ecological question: **under what conditions does island-induced reassembly of pollinator communities generate recurring floral shifts, and under what conditions does it generate different regional responses?** Do not make a C→I→S ordering the desired outcome. A credible answer can include convergence, divergence, persistence or reproductive failure.

Three approaches were considered:

1. Keep best-partner/centroid updates and rename their interpretation: insufficient, because neither rule derives from reproductive success.
2. Derive a quantitative-genetic response from a declared fitness function: a useful diagnostic and potentially efficient approximation, but mixed mating, male function, genetic covariance and frequency dependence need explicit treatment.
3. **Recommended destination: a minimal sexual life cycle linking pollen transfer, offspring survival and inheritance.** This is more work, but directly addresses the mechanism that was previously imposed by a movement rule. Build and verify its reproductive accounting first; use the gradient approximation as a cross-check in the weak-selection/outcrossing limit, not an interchangeable biological truth.

This proposal does not require a complete ecosystem, explicit pollinator coevolution, every plant trait or a full genetic-load model. It does require that traits affecting mating be evaluated through both maternal and paternal success. It does not promise that the new model will explain the observed four-region pattern.

## The central change

Old causal chain:

visitor list → mean compatibility → service threshold → manually chosen trait target.

Proposed causal chain:

visitor supply and functional composition → attraction and access → compatible pollen transfer → outcrossed/selfed offspring and survival → inheritance → next-generation floral distribution.

[Aigner (2001)](https://doi.org/10.1034/j.1600-0706.2001.950121.x) shows why adaptation cannot simply target the most effective pollinator: gains from one partner must be evaluated against losses from others. [Sargent & Otto (2006)](https://doi.org/10.1086/498433) supplies an explicit population-genetic precedent linking pollinator abundance/efficiency and local plant abundance to specialization; its self-incompatible system does not by itself justify a mixed-mating extension.

## Biological entities and accounting

**Plant population:** heritable variation in floral access geometry and attraction investment. Autonomous-selfing capacity is a separately declared trait/context, not equated with self-compatibility. Genetic effects are theoretical, not claimed molecular identifications. The initial mechanistic tests hold mating-system parameters fixed; a joint selfing-evolution analysis requires the completed mixed-mating inheritance module.

**Colour:** attraction investment is not hue. A white flower is not intrinsically low investment or invisible to insects. Actual Q1 colour-category predictions require a separate spectral/category representation and independently justified visitor preference functions. Never place red, yellow and blue in an arbitrary ordered 0–1 variable. Until this input gate is met, report access/investment predictions separately from untested colour predictions.

**Pollinator community:** functional identity, activity/visitation supply, access traits, pollen-transfer effectiveness and temporal occurrence. Species richness, activity and matching are separate variables. Introduced status does not automatically incur an efficiency penalty; efficiency follows measured or explicitly varied functional properties. Do not transfer the old universal 0.82 multiplier as established biology.

**Visitation:** allocate finite visitor activity among available flowers through attraction and access. A normalized allocation must account for competing flowers and non-visits; adding another visitor type must not reduce all service merely by enlarging the denominator of an unweighted mean. Cross fixed-total-activity and varying-total-activity experiments to separate composition from quantity.

**Pollen transfer:** track donor → compatible recipient delivery, pollen availability, loss/carryover and contact effectiveness at the level required by the focal comparison. Visiting, depositing pollen and successfully siring offspring are different events. Count maternal outcross success, paternal outcross success and viable selfed offspring separately; one outcrossed offspring has one mother and one father, not two independent offspring.

**Reproductive assurance:** compare a declared delayed-selfing route with an alternative timing where selfing competes for ovules. Include inbreeding depression and the opportunity cost to pollen export when applicable. Do not enforce a universal selfing optimum. [Herlihy & Eckert (2002)](https://doi.org/10.1038/416320a) empirically demonstrates that increased seed production through assurance need not imply a net genetic advantage.

**Investment costs:** represent a declared resource budget linking display/access investment to ovule and/or pollen production. Cost shape is an assumption requiring alternatives, including a no-cost contrast; do not build reduced display into the result. A cost applied to both resources needs a single budget, not accidental double charging.

**Inheritance:** generate offspring from the realized maternal/paternal contributors under an explicit small diploid genetic model, including selfing and segregation. Track viability and recruitment. Fix or vary recruitment regulation explicitly; do not normalize a reproductively failed population back to full size. Drift is a separate control, not evidence of adaptive divergence. Population failure remains an outcome.

**Time:** one evolutionary step becomes one complete modeled reproductive generation. Within-generation flowering/visitor observations are separate ecological intervals. A theoretical generation is not a calendar year; the old 120 steps and arrival/loss probabilities are not automatically reusable as annual or generational rates.

## Mainland–island intervention and the role of k

Start paired mainland/island populations from the same declared inherited variation, then alter arrival/persistence, functional composition and activity through separate interventions plus a combined scenario. Use standardized functional-community contrasts before region-specific inputs. Each numerical rate requires a declared unit, origin and range.

The old k remains an archived aggregation experiment. For the new model, explicitly schedule visitor exposures within a generation and environmental changes across generations. Hold total effort constant when increasing the number of exposure intervals; otherwise extra samples also add extra visits. Cross temporal correlation and turnover separately. Reproduction must be computed in its actual order: in general, averaging visitor communities and then computing seed production differs from computing each interval's contributions and then integrating them.

## Q1 needs two mechanisms distinguished

Q1 measures island floristic trait composition; it is not a longitudinal observation of the same lineage evolving. The new model must distinguish:

- **Ecological sorting:** different pre-existing plant types establish, reproduce or persist differently while their traits remain fixed.
- **Evolution:** heritable trait distributions change within a lineage.

Use a sorting-only baseline and an evolution-enabled counterpart with comparable starting pools. A combined community projection is a later stage requiring plant establishment/persistence and abundance/occupancy outputs matching Q1's weighting. Do not equate abundance-weighted simulated means with species-presence-based Q1 proportions. Convergence within a lineage, convergence among regional means and loss of floral diversity are different endpoints.

## Hypotheses to distinguish, not desired answers

| Hypothesis | Intervention needed | Discriminating response |
|---|---|---|
| Reproductive assurance changes investment incentives | Hold visitor function fixed; vary autonomous-selfing capacity, timing and costs | Investment/access change attributable to assurance versus preserved outcrossing benefit |
| Functional filtering causes region-specific selection | Hold total visits and mating context fixed; alter visitor access/effectiveness distribution | Different gradients, inherited trajectories or endpoints despite comparable activity |
| Temporal reliability changes which strategies persist | Hold marginal visitor supply comparable; alter temporal sequence/correlation | Reproductive and trait outcomes depend on exposure structure, not simply type count |
| Apparent regional evolution is ecological sorting | Disable inheritance change while allowing declared establishment/persistence differences | Floristic patterns arise without within-lineage evolution |

Expected possibilities include reduced attraction investment when its marginal reproductive benefit falls, retention of restricted access when compatible partners reward it, and different changes in attraction versus access. These are conditional hypotheses, not predictions established by the present evidence.

## The four-region connection

Retain the observed regional combinations and their analysis scopes from the [Q1 bridge document](CHAPTER1_FOUR_REGION_TO_CHAPTER2_DISCUSSION_20260925.md): northern midlatitude attraction/handling changes; northern high-latitude structural changes within blue/purple; tropical deep-tube increase within yellow/orange in the direct-only conditional contrast; southern extratropical plain-colour increase alongside shallow/open-tube decline.

The test is whether independently specified local visitor function and source flora help predict these *combinations*, rather than whether four arbitrary regional parameter sets can reproduce them. Region names are evaluation strata, not mechanisms. Tube/access predictions can be tested before hue predictions. Q1 categories may also be coarse proxies for the modeled traits; observation functions must be specified before comparison.

Because these four Q1 patterns have already informed this design, agreement with them is a retrospective explanation, not an untouched confirmation set. Freeze predictions for independent islands, taxa or newly acquired observations before inspecting their outcomes. Compare against selfing-only, sorting-only and region-agnostic alternatives. If independent visitor data are unavailable, retain a theoretical phase diagram rather than label synthetic regimes as fitted regional reconstructions.

H2 motivates separating assurance from visitor-mediated pathways; an adjusted association alone is not proof of direct selection. H3/H4 motivate asking whether an adverse visitor environment and compensating traits can coexist; the new model can evaluate this within its causal interventions without relabeling observed associations as causal estimates.

## Outputs and evaluation before any simulation campaign

Primary outputs: changes in inherited access/investment, within- and among-population trait dispersion, compatible pollen delivery, viable selfed/outcrossed offspring, paternal contributions and population persistence. Predefine convergence as a change in a declared trait-distance statistic, and divergence using the same metric; distinguish endpoints from transient trajectories. Choose the horizon, scaling, replication, uncertainty treatment and numerical tolerances in a separate prospective execution contract.

S/C/I can describe a fully crossed starting-state × community-history experiment afterward, separately for each named response. They are not causal fractions and their old service values are not comparable to new fitness/trait shares. Do not require any rank reversal for the model to count as informative.

Essential verification: reproductive and pollen-budget accounting; Mendelian transmission and self/outcross parentage; no evolution without heritable variation (apart from declared demographic sorting); neutral-drift baseline; no visitors/assurance-off failure; genetic and numerical boundary checks; deterministic weak-selection comparison to an independently derived gradient; robustness to genetic architecture, costs, mating timing, activity normalization and pollen-transfer kernels. No mechanism is supported merely because all software tests pass.

Reject or narrow the explanatory claim if regional fit requires tuning to the observed floral outcomes, if sorting alone explains the same pattern, if predictions reverse across equally supported kernels, or if field inputs cannot distinguish the proposed mechanisms. Preserve all such results. This is not a search for parameters that recover the old rank transition.

## Delivery sequence and current status

1. Review this causal design and the primary-source note; decide the smallest reproductive ledger that answers the question.
2. Specify the numerical life cycle, genetics, input evidence and validation contract before running outcome comparisons.
3. Verify fixed-mating reproductive surfaces and parentage accounting, then enable inheritance; add joint selfing evolution only after its own accounting passes.
4. Run frozen interventions and sorting controls, then independent regional/field evaluation where data permit.

No simulation equations, existing frozen results, poster claims or evolutionary conclusions were changed by this document. This is a proposed new model alongside the archived one, not a relabeling of an uncalibrated service update as evolution.
