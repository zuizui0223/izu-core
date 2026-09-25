# Chapter 2 post-freeze structural challenge — 2026-09-25

## Question

Does the Chapter 2 finite-aggregation determinant-order result depend on either:

1. the frozen 21-point starting-state grid; or
2. the hard service threshold plus best-partner state-update rule?

The design was frozen before execution in `data/design/chapter2_postfreeze_grid_update_rule_challenge_20260925.json`. The collision-free six-seed RNG hierarchy, 96 realizations per seed, `k={1,2,4,8,16}`, biological parameters and `trait_adjustment=0.03` were unchanged.

## Grid-resolution challenge: passed

Under the frozen threshold/best-partner rule, all three grids reproduced the same median winner topology:

| starting-state grid | k=1 | k=4 | k=16 |
|---:|---|---|---|
| 21 points | community | interaction | starting state |
| 41 points | community | interaction | starting state |
| 81 points | community | interaction | starting state |

The interaction-dominated finite-`k` regime is therefore not an artefact of the 0.05 spacing of the historical 21-point grid.

The normalized median fractions remain close as resolution increases. At `k=4`, `(S,C,I)` changes only from approximately `(0.247, 0.232, 0.508)` at 21 points to `(0.234, 0.236, 0.519)` at 81 points.

## Update-rule challenge: C/I reversal survives, S takeover does not

The structural alternative removed both discrete features of the historical plant update:

- no `service < 0.45` threshold;
- no switch to the single best current partner.

Instead, plant state moved every nonempty step by

`alpha * (1 - service)`

toward the encounter-weighted centroid of current partner traits.

The prespecified gate required at least 4/6 frozen seeds to start with `C>I` at `k=1` and cross to `I>C` at some later `k`. The result was **6/6**.

First observed later `I>C` values were:

| seed | first k with I>C |
|---:|---:|
| 20260826 | 16 |
| 20250101 | 2 |
| 20260833 | 16 |
| 20260827 | 4 |
| 999983 | 4 |
| 12345 | 4 |

At the across-seed median, the smooth rule is community-dominated at `k=1`, interaction-dominated at `k=4`, and community-dominated again at `k=8` and `k=16`. Starting-state share remains small.

Therefore:

> **The robust cross-rule result is a finite-scale community-to-interaction rank reversal / transient interaction-dominant regime. The later starting-state-dominant regime is not update-rule invariant.**

The full `C -> I -> S` sequence remains a property of the frozen threshold/best-partner plant response and of a subset of the structurally separate consumer-resource settings; it should not be stated as a general law of nonlinear averaging.

## Fixed-state negative control

With plant state held fixed, the median winner sequence is:

`C -> I -> I -> I -> I`

for `k=1,2,4,8,16`.

Thus plant movement is not required for `I` to overtake `C`. It is required for the frozen plant model's later starting-state takeover.

## Absolute sum-of-squares scaling

The crossover is not only a normalized-share artefact.

For the frozen threshold/best-partner rule, median per-cell SS log2 slopes across `k` are:

| grid | S slope | C slope | I slope |
|---:|---:|---:|---:|
| 21 | +0.106 | -1.513 | -0.839 |
| 41 | +0.063 | -1.525 | -0.839 |
| 81 | +0.039 | -1.530 | -0.837 |

Across all three resolutions, community SS contracts much faster than interaction SS, while starting-state SS is approximately flat over the audited finite range. This exposes interaction variance at intermediate `k` before the persistent state term becomes largest.

For the smooth weighted rule, the corresponding slopes are approximately:

- `S=-0.552`
- `C=-1.654`
- `I=-1.006`

Community SS again contracts faster than interaction SS, explaining why a C/I boundary can still be crossed even though the later S-dominant phase disappears.

## Paper-facing boundary

The defensible claims after this challenge are:

1. the C/I ordering is not fixed under finite aggregation;
2. transient interaction dominance is robust to 21/41/81 starting-state resolution;
3. C-to-I reversal persists after removing the hard threshold and best-partner update in all six frozen seeds;
4. the exact crossover `k` is model-specific;
5. the eventual starting-state takeover is update-rule dependent and must not be generalized;
6. synthetic `k` remains uncalibrated to visitor richness, Hill diversity or any other named natural-system coordinate.

The source artifact is recorded in `data/results/chapter2_postfreeze_grid_update_rule_challenge_closure_20260925.json`.
