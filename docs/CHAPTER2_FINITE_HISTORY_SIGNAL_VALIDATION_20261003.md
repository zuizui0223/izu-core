# Chapter 2 finite-history signal validation — 2026-10-03

**Status:** prospectively frozen validation of a post-hoc discovery, completed with new demographic seeds.

## What was frozen before validation

The original exact-source bridge reanalysis was exploratory. After that discovery, but **before any new demographic execution**, the validation design fixed:

- all original 128 visitor histories;
- the same three starting states;
- natural, visitor-pooled and capacity-192 interventions;
- exactly four new demographic seeds: **201–204**;
- 200 seasons and inbreeding depression 0.50;
- the primary statistic: correlation across 128 histories between the fixed discovery history mean and the new-seed validation history mean;
- the ordering prediction **capacity 192 > natural > visitor pooled**;
- a strong-success rule requiring both paired bootstrap differences from natural to exclude zero in the predicted directions;
- no seed extension, replacement, threshold tuning or outcome-based stopping.

The discovery remains post-hoc. The new-seed test is a prospective validation of its fixed prediction.

## Execution

Using the exact source snapshot from the original bridge, validation ran:

**128 histories × 3 starts × 6 finite arms × 4 new demographic seeds = 9,216 finite trajectories.**

All six arms had **100% terminal occupancy**. Minimum terminal population was 48 in natural/pooled arms and 192 in the large-capacity arms.

A full `simulate()` implementation check for history 74001, start 0.3 and demographic seed 201 matched the compact validation runner in all six arms: terminal populations were identical and the maximum absolute investment-change difference was **1.61 × 10^-15**.

## Primary validation

| Intervention | discovery → new-seed history correlation | 95% history-bootstrap interval |
|---|---:|---:|
| Natural | **0.732** | 0.633–0.805 |
| Visitor pooled | **0.165** | 0.008–0.326 |
| Capacity 192 | **0.918** | 0.893–0.941 |

The prospectively frozen ordering was observed:

> **capacity 192 > natural > visitor pooled**

Paired history-bootstrap contrasts were:

- capacity 192 − natural: **+0.186**, 95% interval **+0.120 to +0.283**;
- visitor pooled − natural: **−0.567**, 95% interval **−0.732 to −0.401**.

Both intervals exclude zero in the predeclared direction. The validation therefore meets the frozen **strong-success** rule.

## Secondary checks

The new four-repeat validation means remained directionally much more uniform after the two interventions:

- natural, epsilon 0: **103 negative / 23 mixed / 2 positive**;
- visitor pooled: **127 negative / 1 mixed / 0 positive**;
- capacity 192: **124 negative / 4 mixed / 0 positive**.

Yet continuous history predictability remained opposite.

Validation-only history-structured variance / demographic residual variance were:

- natural: **0.00485 / 0.02748**;
- visitor pooled: **0.000916 / 0.02812**;
- capacity 192: **0.01131 / 0.01472**.

With four validation repeats, the corresponding mean-history reliability was **0.414**, **0.115** and **0.754**.

The validation-on-discovery slopes were 0.749 (natural), 0.233 (pooled) and 1.054 (capacity 192), again showing that pooled histories retain little of the discovery history ranking while capacity scaling preserves it strongly.

## Scientific consequence

The paper no longer has to rely on the post-hoc variance decomposition alone.

The discovery generated a fixed prediction, and **new demographic realizations reproduced the predicted ordering strongly**. Therefore the bounded model-level result is:

> **Greater directional similarity can accompany opposite changes in the reproducibility of history-specific evolutionary effects.**

For the larger population, direction becomes more uniform while history-specific magnitude becomes more predictable across new demographic realizations. Under visitor-history pooling, direction also becomes more uniform, but the original history ranking is largely erased.

## Claim boundary

This is not a new ecological-history replication: the same 128 synthetic visitor histories are used in discovery and validation. It validates the response to **new demographic stochasticity**, not transfer to new environmental histories or natural islands. The original discovery remains exploratory; only the new-seed prediction test was prospectively frozen.
