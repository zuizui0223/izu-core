# Appendix S21. Exact finite-community moments and Gaussian mean-field limit

This appendix formalizes the zero-trait-adjustment system-size audit without changing the Chapter 2 empirical claim ceiling. The design was fixed before execution in `data/design/finite_n_gaussian_limit_freeze_20260908.json`; the CI-verified result is summarized in `data/results/finite_n_gaussian_mean_field_summary_20260908.json`.

## S21.1 Exact terminal count process

For partner-loss probability `l`, partner-arrival probability `a`, and `q=1-l`, the pollinator count obeys

`N_(t+1) = Binomial(N_t, q) + Bernoulli(a)`.

The terminal count pmf was propagated exactly. The first two moments satisfy

`m_(t+1) = q m_t + a`,

`v_(t+1) = q^2 v_t + q(1-q)m_t + a(1-a)`.

At 120 steps the exact single-copy terminal values are:

| scenario | mean N | variance N | CV | P(N=0) |
|---|---:|---:|---:|---:|
| mainland-like | 17.0904 | 14.2881 | 0.2212 | 7.54e-9 |
| island-like | 2.18387 | 2.04925 | 0.6555 | 0.10486 |

For `k` independent pooled copies, mean and variance are multiplied by `k`, so count CV decreases exactly as `k^(-1/2)` and empty-community probability is `P(N=0)^k`.

## S21.2 Exact terminal kernel moments

At plant state `x`, one pollinator contributes

`Y(x) = A exp(-((x-P)/B)^2)`.

The 21-dimensional first moment `mu` and covariance `Sigma` over the frozen trait grid were evaluated by deterministic quadrature over the unchanged clamped-normal pollinator trait distribution and the frozen generalist/specialist and introduced/native mixtures.

For a terminal community kernel

`K = mean_i Y_i` when `N>0`, and `K=0` when `N=0`, define

`p = P(N>0)` and `h = E[I(N>0)/N]`.

Then

`E[K] = p mu`,

`Cov(K) = h Sigma + p(1-p) mu mu^T`.

These finite-`k` moments are exact. Mainland-like and island-like terminal communities are independently generated, so the island-minus-mainland kernel-contrast covariance is the sum of their covariance matrices.

## S21.3 Deterministic mean-field limit

As `k -> infinity`, empty-community probability and kernel variance vanish. The deterministic limit is therefore the difference in expected single-pollinator kernel contributions.

Across all 21 Chapter 2 starting states, this mean-field contrast is positive:

- minimum = **0.0207650**;
- maximum = **0.149396**;
- classification = **all-positive**.

Mixed response geometry therefore does not survive the deterministic mean-field limit in the zero-adjustment submodel.

## S21.4 Gaussian finite-size approximation

We next approximated the finite-`k` kernel-contrast vector by a 21-dimensional Gaussian having the **exact finite-`k` mean and covariance** above. The Gaussian layer therefore approximates only distributional shape, not the count process or first two kernel moments.

With the prespecified 200,000 Gaussian draws per `k`, comparison to the existing six-seed ABM system-size audit was:

| k | ABM mixed fraction | Gaussian mixed probability | absolute error |
|---:|---:|---:|---:|
| 1 | 0.71354 | 0.78241 | 0.06887 |
| 2 | 0.77604 | 0.81404 | 0.03799 |
| 4 | 0.73611 | 0.76765 | 0.03153 |
| 8 | 0.67014 | 0.68136 | 0.01122 |
| 16 | 0.56424 | 0.57078 | **0.00654** |

The Gaussian approximation becomes increasingly accurate as system size increases. At `k=16`, island-like empty-community probability is approximately `2.14e-16`, yet the ABM remains mixed in 56.4% of pooled realizations and the Gaussian approximation predicts 57.1%.

## S21.5 1/k covariance scaling and asymptotic collapse of branching

The exact kernel-contrast covariance trace approaches

`tr(C_k) ~ C/k`, with `C = 0.989454`.

The Gaussian extrapolation then approaches the all-positive deterministic limit:

| k | Gaussian mixed | Gaussian all-positive |
|---:|---:|---:|
| 32 | 0.4377 | 0.5623 |
| 64 | 0.2841 | 0.7159 |
| 128 | 0.1320 | 0.8680 |
| 256 | 0.0342 | 0.9658 |
| 512 | 0.00266 | 0.99735 |
| 1024 | 0.000025 | 0.999975 |

These are approximation-based system-size extrapolations, not additional ABM observations or natural abundance predictions.

## S21.6 Interpretation boundary

The result separates two statements that should not be conflated.

1. Mixed branch identity is **finite-community in the asymptotic sense** because the deterministic mean-field contrast is all-positive.
2. Mixed branching is **not a rare empty-community or N≈2 artefact**: it remains common after empty communities effectively disappear, and a second-order Gaussian approximation reproduces the ABM branch frequency closely by `k=16`.

This is not an exact Fokker–Planck solution and not a full van Kampen linear-noise approximation for the adaptive plant-state model. The exact layer is the terminal count distribution and finite-`k` kernel moments for the zero-trait-adjustment submodel; the branch-probability layer is Gaussian.
