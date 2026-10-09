# Chapter 2 — Post-outcome absolute occupancy versus far–near interaction (2026-10-09)

**Status: completed exploratory reanalysis, NOT an independent preregistered confirmation.**

## Provenance and verification

- Frozen independent visitor-history experiment: GitHub Actions [#37862121201](https://github.com/zuizui0223/izu-core/actions/runs/37862121201), successful; source SHA `868164c24b6a6f17e7530941600fcb50e7281342`.
- This post-outcome audit: GitHub Actions [#37863754455](https://github.com/zuizui0223/izu-core/actions/runs/37863754455), successful after correction of one synthetic float-equality assertion in the first attempt; **no new visitor simulations**.
- Original experiment's 64 future-shard artifacts were downloaded and all **2,048 individual future-record receipts** authenticated via SHA-256; all **57,344 terminal-occupancy cells** and 64 independent history-shard registries were required before estimates were computed.
- Reusable machine receipt: [`results/chapter2/order_absolute_posthoc_exploratory_20261009.json`](../results/chapter2/order_absolute_posthoc_exploratory_20261009.json).
- Parser and resampling code: [`scripts/chapter2_order_absolute_posthoc.py`](../scripts/chapter2_order_absolute_posthoc.py). Exact 64-history bootstrap (9,999 resamples, seed 2026100917); paired indices are reused across settings, budgets, and near/far comparisons.
- No biological source, evolutionary random-number stream, 2026-10-08 original expression-order experiment, or 2026-10-09 independent 3/4 resource-window decision was modified.

## Question disentangled

The prespecified original question concerned a **historical-environment interaction**:

`DID = [A_first - I_first]_(far) - [A_first - I_first]_(near)`.

This can vanish if both historical environments have similar small absolute advantages of A-first. Conversely, a negative DID does **not** imply A-first decreases far absolute occupancy. Accordingly, we now calculate *descriptively* the budget-weighted A-first minus I-first absolute 80-step terminal-occupancy contrast in each historical environment, plus its common mean and their DID.

Weights are inherited without modification from the frozen 7-budget log-grid; observations are paired within the same visitor history, demographic repeat, future-visitor environment, mating setting, and posthistory regime. The bootstrap unit is **64 independent visitor histories**, never 57,344 future branches. Both histories extinct before future transfer still enter with zero occupancy.

## Exploratory absolute-occupancy contrasts

All values are occupancy probabilities; multiply by 100 for percentage-point differences.

| Synthetic stress regime | near A-first − I-first [95% history bootstrap] | far A-first − I-first [95% history bootstrap] |
| --- | --- | --- |
| 8 founders / capacity 8 (original primary) | **+0.0165596 [0.0070932, 0.0263907]** | **+0.0076198 [0.0026792, 0.0127341]** |
| No bottleneck / capacity 48 | **+0.0131177 [0.0063412, 0.0200629]** | **+0.0053572 [0.0024435, 0.0085679]** |

In the primary eight-founder stress, the across-near/far common absolute contrast is **+0.0120897 [0.0067552, 0.0174591]**. The far-minus-near **DID is −0.0089397 [−0.0200984, +0.0020492]**. The no-bottleneck common contrast is **+0.0092374 [0.0054521, 0.0132107]**, and its DID is **−0.0077605 [−0.0150172, −0.0005138]**.

**Interpretation:** The random assignment of A-first temporary expression history is associated with a *small* positive absolute occupancy difference in both environments across both synthetic regimes. The primary far–near interaction has no resolved sign. The magnitude remains well below 0.05 occupancy, the previous declared practically meaningful effect scale, although **0.05 was preregistered for the original interaction, not for this newly chosen exploratory main effect**. These reanalysis confidence intervals do not turn a post-outcome estimand into prospective confirmation.

The earlier 64-history experiment already had small positive near/far absolute contrasts in its published full-grid readout. Cross-cohort direction agreement is descriptive and is not independent *prospective* confirmation of the now post hoc main-effect question.

## Mating-rule heterogeneity

In the eight-founder primary scenario:

| Reproductive rule | near effect [95% history interval] | far effect [95% history interval] |
| --- | --- | --- |
| `delayed_control` | +0.01552 [−0.00303, +0.03431] | +0.00643 [−0.00367, +0.01686] |
| `prior_selfing` | +0.02082 [+0.00599, +0.03562] | +0.01485 [+0.00475, +0.02483] |
| `pollen_discount` | +0.01827 [+0.00154, +0.03531] | +0.00624 [−0.00388, +0.01671] |
| `assurance_cost` | +0.01163 [−0.00123, +0.02431] | +0.00296 [−0.00676, +0.01324] |

Individual setting intervals often include zero; this table is not a multiplicity-adjusted 8-test discovery. There is no basis for claiming that one ecological cost regime universally mediates a causal survival gain.

## Resource floors and ceilings

At budget 0.5 or 1, all pooled absolute occupancy values are zero; at budget 8 most capacity-8 populations persist regardless of the assigned schedule. The largest unadjusted primary near difference is at budget 4: **+0.06836** absolute occupancy, with far difference **+0.00586**. This must **not** be relabeled a new confirmed threshold. The separate prospectively fixed intermediate-resource-window follow-up found **practical equivalence**, and the extra budget-3/4 term **did not beat the cubic smooth resource comparator**. The post-outcome budget-4 pattern therefore cannot rescue that failed confirmation.

## Scientific position after two completed cohorts

1. **Confirmed within the original preregistration:** The 64-history original full-grid far–near DID was practically equivalent under its ±0.05 criterion. This is not negated by a post hoc absolute-effect contrast.
2. **Failed independent follow-up:** The budget-3/4 localization hypothesis was not supported in a fresh 64-history cohort. Its negative result retains full rank.
3. **New exploratory observation:** A-first shows small, directionally positive **absolute** terminal-occupancy contrasts in both synthetic near/far environments; uncertainty was computed from 64 paired independent histories.
4. **Unanswered mechanism:** Is the small absolute difference due to maternal selfed recruitment, viable outcross offspring, paternal export, inherited genotype/variance, or nonlinear demographic translation from immediate reproductive payoffs? The present reanalysis did **not** identify genetic mediation or experimentally isolate any of these pathways.

### Next discriminator (not yet approved)

A follow-up should first contrast the **postshock t0 reproductive payoff and the 80-update realized selfed/outcross recruitment**, while keeping absolute effects, historical-environment interaction, and genotype realization separate. Such measurements can be explored from existing full future-case records, but mediation requires a new intervention/identification argument. If a confirmatory main-effect hypothesis is desired, independently freeze the precise effect scale, the 64-history bootstrap and the target resource integration **before** collecting another disjoint cohort. Do not reuse these exposed histories as confirmatory evidence.

**No extra prospective biological histories were simulated or authorized by this exploratory readout.**
