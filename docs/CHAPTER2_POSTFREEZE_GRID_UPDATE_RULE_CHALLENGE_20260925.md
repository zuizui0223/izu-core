# Chapter 2 post-freeze grid and update-rule challenge — 2026-09-25

## Status

**Completed.** Focused workflow run `36101465237` passed the focused tests, the full 96-realization × six-seed audit, and artifact upload. The result artifact is pinned by SHA-256 digest `c395bee8d3e6f9c20196c12186073936cc1152744fbee5d1f5328c3594ff8e64`.

This is a **post-freeze structural challenge**, not a redefinition of the frozen Chapter 2 design.

## 1. The 21-point grid is not driving the rank sequence

The prespecified grid challenge passed at all three resolutions:

| starting-state grid | k=1 | k=4 | k=16 |
|---:|---|---|---|
| 21 | community | interaction | starting state |
| 41 | community | interaction | starting state |
| 81 | community | interaction | starting state |

The median winner topology is therefore unchanged when spacing is refined from 0.05 to 0.025 and 0.0125.

The numerical fractions move modestly, as expected, but the ordering does not. At k=4 the median interaction share is 0.508 on the 21-point grid, 0.515 on the 41-point grid and 0.519 on the 81-point grid.

**Conclusion:** the intermediate interaction-dominated regime is not a coarse-grid artefact.

## 2. Removing the hard threshold and best-partner switch does not remove the C/I reversal

The alternative smooth rule removes both arbitrary-looking discontinuities in the frozen plant update:

- no service threshold at 0.45;
- no winner-take-all move toward one best partner.

Instead, plant state moves continuously by `alpha * (1-service)` toward the encounter-weighted centroid of the current pollinator traits.

The prespecified criterion required a community-dominated k=1 state and a later I>C crossover in at least 4/6 seeds.

**Observed: 6/6 seeds passed.**

First crossover k by seed:

- 20260826: 16
- 20250101: 2
- 20260833: 16
- 20260827: 4
- 999983: 4
- 12345: 4

The crossover location is therefore **not** stable, but the existence of a finite-k C/I ordering reversal is.

At the ensemble-median level under the smooth rule:

| k | S | C | I |
|---:|---:|---:|---:|
| 1 | 0.0036 | 0.8681 | 0.1279 |
| 4 | 0.0155 | 0.4707 | 0.5118 |
| 16 | 0.0409 | 0.4893 | 0.4683 |

**Conclusion:** the C/I reversal does not depend on the hard 0.45 threshold or best-partner update.

## 3. The important absolute-variance result: I does not grow; C collapses faster

Normalized shares alone can obscure the mechanism. The audit therefore stored raw SS and per-cell SS.

For the frozen threshold-best rule on the 21-point grid:

| component | k=1 per-cell SS | k=4 | k=16 | log2 slope vs k |
|---|---:|---:|---:|---:|
| S | 0.002293 | 0.003272 | 0.002980 | +0.106 |
| C | 0.057870 | 0.003009 | 0.000747 | **-1.513** |
| I | 0.017086 | 0.006751 | 0.001751 | **-0.839** |

The same contrast is nearly unchanged at 41 and 81 grid points:

- C slope: -1.525, -1.530
- I slope: -0.839, -0.837
- S slope: +0.063, +0.039

So the intermediate I dominance is **not interaction amplification**. I itself contracts with aggregation. It becomes dominant because additive community variance contracts substantially faster.

The same ordering of contraction rates appears under both alternative rules:

| rule | S slope | C slope | I slope |
|---|---:|---:|---:|
| threshold-best | +0.106 | -1.513 | -0.839 |
| smooth-weighted | -0.552 | -1.654 | -1.006 |
| fixed state | -0.028 | -1.410 | -1.052 |

Across all three, **C contracts faster than I**.

This is the strongest general statement produced by the challenge:

> **aggregation can reverse determinant rank because additive realization variance and state × realization nonadditivity contract at different rates.**

## 4. The eventual S takeover is not equally robust

The full frozen sequence is C → I → S, but the structural challenge separates its two transitions.

- **C → I:** robust to grid refinement and to replacing the threshold/best-partner update with smooth weighted feedback.
- **I → S:** not rule-invariant.

Under smooth weighted feedback, k=16 remains C/I dominated rather than S dominated. Under the fixed-state negative control, the median winner sequence is:

`C → I → I → I → I` for k = 1,2,4,8,16.

This means the eventual S takeover relies on how plant-state feedback preserves or builds between-state variance. It should remain a result of the frozen response operator, not be advertised as a universal consequence of averaging.

## 5. Mechanistic interpretation after the challenge

The defensible hierarchy is now:

1. **Strongest / most general:** community and interaction variance can contract at different rates under aggregation.
2. **Robust nonlinear consequence:** that differential contraction can create a finite intermediate interaction-dominated regime.
3. **Plant-model-specific:** under the frozen threshold-best operator, starting-state variance is retained strongly enough to dominate at larger finite k.
4. **Not supported as universal:** one fixed numerical crossover k, or a universal C → I → S sequence for every state-update rule.

The novelty wording should therefore emphasize **scale-dependent driver attribution caused by unequal contraction of variance components**, not a novel pollination rule and not interaction amplification.

## Claim boundary

These are synthetic post-freeze diagnostics. They do not calibrate k to visitor richness, Hill diversity, island size or any named natural threshold. Failure or success here changes the strength of the mechanistic interpretation only; it does not license retuning the frozen biological parameters.
