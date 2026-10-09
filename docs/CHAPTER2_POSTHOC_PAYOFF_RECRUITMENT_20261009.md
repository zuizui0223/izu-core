# Chapter 2 — Existing-cohort payoff, recruitment and persistence decomposition (2026-10-09)

**Evidence status: POST-OUTCOME EXPLORATION; not prospectively confirmed causal mediation.**

## What was actually run

- Frozen independent 64-visitor-history order-expression experiment: [Run #37862121201](https://github.com/zuizui0223/izu-core/actions/runs/37862121201); source SHA `868164c24b6a6f17e7530941600fcb50e7281342`.
- Read-only payoff/recruitment analysis: [Run #37864432822](https://github.com/zuizui0223/izu-core/actions/runs/37864432822), **success**. The existing 64 future artifacts were downloaded; no additional biological history or future simulation was launched.
- Reused [`scripts/chapter2_order_absolute_posthoc.py`](../scripts/chapter2_order_absolute_posthoc.py) complete original-artifact verification before analyzing the detailed future cells. All 64 history-shard receipts, 2,048 ancestor-group JSON hashes and the 57,344 future cells were required.
- Exact exploratory result: [`results/chapter2/order_payoff_recruitment_posthoc_20261009.json`](../results/chapter2/order_payoff_recruitment_posthoc_20261009.json), which retains all four reproductive-setting breakdowns and budget-level contrasts.
- Code: [`scripts/chapter2_order_payoff_recruitment_posthoc.py`](../scripts/chapter2_order_payoff_recruitment_posthoc.py), plus synthetic-only tests. A temporary replay workflow was removed after the successful run.
- Inference: matched A-first minus I-first arms; integrate all seven frozen ovule budgets with their original log-interval weights, average the two future visitor regimes and two nested demographic replicates within each setting and visitor history; average four settings and near/far environments for the reported common contrast. Only **64 independent visitor histories** are bootstrapped, 9,999 draws, seed `2026100918`.

## Core finding — a reproductive allocation signature, not confirmed mediation

In the 8-founder, capacity-8 stress regime, the common A-first minus I-first contrasts averaged across historical near/far environments are:

| Observation channel | Mean contrast | 95% paired history-bootstrap |
| --- | ---: | --- |
| Initial source presence at future transfer | 0 | [0, 0] |
| Initial population size at transfer | 0 | [0, 0] |
| Initial viable maternal population output | **+0.1594** | [+0.0802, +0.2364] |
| Initial viable selfed maternal population output | **+0.3963** | [+0.3014, +0.4891] |
| Initial female outcross population output | **−0.2370** | [−0.3308, −0.1454] |
| Initial paternal pollen export population output | **−0.7985** | [−1.1515, −0.4551] |
| Cumulative realized selfed recruits over 80 future updates | **+10.6901** | [+7.6587, +13.6535] |
| Cumulative realized outcross recruits over 80 future updates | **−3.6301** | [−4.8943, −2.4546] |
| Cumulative total recruits over 80 updates | **+7.0600** | [+4.1742, +9.9222] |
| Final 80-update occupancy probability | **+0.01209** | [+0.00670, +0.01748] |

**Interpretation at the permitted evidence rank:** Randomly assigning the A-first rather than I-first *temporary expressed phenotype sequence* is associated with a small future terminal-occupancy advantage. The already-recorded raw future states show a simultaneous increase in viable selfed output and cumulative selfed recruits, and a decrease in viable outcross output, paternal pollen export, and cumulative outcross recruits. The increase in cumulative total recruits is consistent with a model-specific reproductive-assurance benefit **despite** a concurrent loss of outcross/paternal output.

The t0 output is computed as the recorded per-plant immediate future payoff multiplied by the *actual* t0 population. Extinct source populations contribute **zero population-level** reproductive output, not a fabricated per-capita payoff. The 80-update recruited counts are cumulative counts, **not rates**, and are inherently affected by how long the population survived. Do not compare their magnitudes directly with per-census t0 outputs or interpret cumulative recruitment as a causal mediator.

No postshock expression offsets remain. Nevertheless, different histories may have inherited-state/trait distributions and cohort structure; the present observational channel decomposition does not randomize genotype exchange, seed-vs-pollen pathways, or density feedback. Therefore **no specific genetic, demographic or reproductive channel has been causally isolated**.

## No-founder-bottleneck comparator

The same directions appear in capacity-48 trajectories:

| Common A-first minus I-first outcome | Mean | 95% history-bootstrap |
| --- | ---: | --- |
| Initial viable selfed population output | +2.4000 | [+1.8322, +2.9579] |
| Initial female outcross population output | −1.5524 | [−2.1523, −0.9657] |
| Initial paternal pollen export population output | −4.7846 | [−6.8483, −2.7651] |
| Cumulative selfed recruits | +64.5520 | [+49.2531, +79.9401] |
| Cumulative outcross recruits | −30.1423 | [−40.1574, −20.8639] |
| Cumulative total recruits | +34.4097 | [+21.3371, +47.7708] |
| Final occupancy probability | +0.00924 | [+0.00542, +0.01321] |

Counts differ sharply with capacity, so these are direction/robustness checks, not comparable natural effects across island populations.

## Why the far–near DID should not be conflated with survival gain

For the capacity-8 scenario, the common absolute final-occupancy A-first advantage is +0.01209, but the near effect is +0.01656 and far effect +0.00762, giving a far-minus-near DID **−0.00894** with paired bootstrap interval **[−0.02046, +0.00194]**. This DID does not establish a specifically far-environment survival rescue.

The capacity-48 DID is **−0.00776** [−0.01502, −0.00075]; again the absolute effect is positive in *both* historical environments. A negative DID is neither negative absolute survival nor genetic mediation.

## Scientific status / anti-overclaim boundary

1. PR #416 first preregistered 64-history whole-grid DID remained **practically equivalent** under its ±0.05 threshold.
2. The subsequent independent fixed budget-3/4 window confirmation also failed; selecting isolated budget 4 cannot rescue the negative gate.
3. This new channel decomposition is entirely **post-outcome**, including its bootstrap intervals. It is a useful mechanistic fingerprint and **not** preregistered independent confirmation of a new main effect.
4. “Selfed recruit gain exceeds outcross recruit decline” is an observation about cumulative realized counts. Counts are affected by differential persistence, so it is **not** proof that selfed recruitment caused the survival gain.
5. No natural-island risk is calibrated, and observed genetic first-change order was never experimentally assigned. The intervention here was assigned temporary phenotype-expression order.

## Next scientific test, not yet authorized

To identify cause rather than association, compare matched futures after separately controlling or transplanting the **same t400 complete diploid states**, while maintaining historical random streams; distinguish maternal-selfed recruitment, outcross/paternal contribution and density-dependent demographic feedback. Such a state intervention changes multivariate genotype and pedigree covariance, so its inferential target and parity tests must be preregistered explicitly before another new biological run. No new history is approved by this document.
