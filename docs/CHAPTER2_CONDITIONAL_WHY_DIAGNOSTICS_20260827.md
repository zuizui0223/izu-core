# Chapter 2 conditional-WHY diagnostics

Updated: 2026-08-27
Status: frozen complete

## Design identity

The design was frozen in `data/design/chapter2_conditional_why_diagnostics_freeze_20260827.json` before execution. The analysis reused:

- seed `20260826`;
- 96 baseline matched pollinator-community realizations;
- the same 21 starting positions;
- the same 48-point, 10-parameter Latin-hypercube surface with 24 matched realizations per point;
- the same 864 local-filtering lineage contrasts and strengths 0–0.75.

No model rule, parameter range, point, seed, replicate count or threshold was changed. All 12 recomputation checks matched the previous frozen Chapter 2 results.

## 1. Regime-boundary driver diagnostic

The continuous response was the fraction of the starting-position grid with negative mean island-minus-mainland service at each joint-design point. All ten range-scaled parameters entered one additive model without selection or interaction terms.

- in-sample `R²`: `0.611`;
- leave-one-point-out RMSE: `0.329`;
- partner-loss full-range coefficient: `+0.634`;
- partner-arrival full-range coefficient: `−0.626`;
- saturation full-range coefficient: `+0.265`.

The three coefficient signs were unchanged in all 48 leave-one-point-out fits. Greater partner loss and lower partner arrival therefore accompanied a larger negative portion of the response surface within the fixed design. The predictive error remains too large to treat the model as a precise regime classifier.

For adjacent regimes, the largest all-positive-to-mixed contrasts were replacement penalty (Cliff's delta `−0.574`) and partner loss (`+0.506`). The largest mixed-to-all-negative contrast was partner arrival (`−0.550`). These are multivariate design-space associations, not causal ecological effects.

## 2. Starting-position × community-realization decomposition

The baseline `21 × 96` response matrix partitioned as:

| Component | Sum-of-squares fraction |
|---|---:|
| Starting position | 2.18% |
| Community realization | 80.17% |
| Starting position × community non-additive remainder | 17.64% |

Observed and additive-fitted signs differed in `271/2016 = 13.44%` of cells. Starting position organizes the mean U-shaped response boundary, while realized community state dominates cell-level variation and combines non-additively with starting position.

Across joint points, median additive-sign mismatch was 13.59% in all-positive, 18.06% in mixed and 11.61% in all-negative regimes. Ranges overlapped; mismatch is therefore not a deterministic regime classifier.

The non-additive remainder also contains cell-level simulation variation because the design has one value per cell. It is not a pure interaction variance estimate.

## 3. Local-filtering directional asymmetry

The zero-filtering baseline contained 268 negative and 596 positive contrasts. Positive-to-non-positive rates exceeded negative-to-non-negative rates at every non-zero strength.

| Strength | Negative → non-negative | Positive → non-positive |
|---:|---:|---:|
| 0.10 | 9.33% | 14.93% |
| 0.25 | 15.30% | 38.42% |
| 0.40 | 15.67% | 56.54% |
| 0.50 | 11.94% | 64.43% |
| 0.60 | 17.54% | 77.01% |
| 0.75 | 49.25% | 84.40% |

Among contrasts that changed sign, median first change was 0.60 for baseline-negative and 0.40 for baseline-positive responses. Local filtering is therefore bidirectional but directionally asymmetric in the fixed model design: it erodes positive branch identity earlier and more often than it rescues negative branch identity.

## Claim ceiling

These diagnostics strengthen the **proximal WHY** claim: turnover balance, community realization and state-by-realization contingency explain why the same declared perturbation can occupy different sign regimes. They do not explain the **ultimate WHY** for why a natural island biota, regional response vector, starting state or local community formed.

Do not interpret coefficients as causal field effects, variance shares as empirical interaction estimates, design counts/rates as natural prevalence, or filtering strengths as calibrated ecological thresholds.
