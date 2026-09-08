# Finite-community to Gaussian to mean-field limit for Chapter 2

**Status:** CI-verified theory-layer audit, 2026-09-08  
**Parent Chapter 2 main:** `46e52082abda631e01c6cf41158ac3aa9f994c7f`  
**Freeze:** `data/design/finite_n_gaussian_limit_freeze_20260908.json`  
**Verified summary:** `data/results/finite_n_gaussian_mean_field_summary_20260908.json`

## Question

The Chapter 2 model deliberately retains finite stochastic pollinator communities because community realization is itself part of the response coordinate. The finite-community system-size audit showed that mixed branch geometry persists even after pooling 16 independent copies, when empty island-like communities have disappeared and count CV is much smaller. The remaining question is sharper:

> Is the branch geometry an asymptotically finite-community phenomenon, and if so, does a second-order Gaussian finite-size approximation recover the ABM before the deterministic mean-field limit is reached?

The audit is restricted to the **zero-trait-adjustment** submodel. This removes plant-state adaptation from the approximation problem while retaining the exact terminal interaction-kernel contrast. Because service is `1-exp(-saturation*K)`, a strictly increasing transformation, the sign of island-minus-mainland service is the sign of the terminal kernel contrast.

## 1. Exact finite-community count process

For one scenario let `l` be partner-loss probability, `a` partner-arrival probability and `q=1-l`. The pollinator count obeys

\[
N_{t+1}=\operatorname{Binomial}(N_t,q)+\operatorname{Bernoulli}(a).
\]

This is not approximated in the audit. The full terminal pmf is propagated exactly by binomial thinning and Bernoulli immigration. Its probability-generating function obeys

\[
G_{t+1}(z)=(1-a+az)\,G_t(l+qz).
\]

The first two moments therefore satisfy

\[
m_{t+1}=q m_t+a,
\]

\[
v_{t+1}=q^2v_t+q(1-q)m_t+a(1-a).
\]

At 120 steps, the exact single-copy terminal moments are:

| scenario | mean N | variance N | CV | P(N=0) |
|---|---:|---:|---:|---:|
| mainland-like | 17.0904 | 14.2881 | 0.2212 | 7.54e-9 |
| island-like | 2.18387 | 2.04925 | 0.6555 | 0.10486 |

For `k` independent pooled copies, mean and variance scale linearly in `k`, so count CV scales **exactly** as `k^{-1/2}` and empty-community probability is `P(N=0)^k`.

## 2. Exact finite-k interaction-kernel moments

For a fixed plant state `x`, let a terminal pollinator mark be

\[
Y(x)=A\exp[-((x-P)/B)^2],
\]

where `P`, `B` and `A` follow the unchanged Chapter 2 pollinator-generation distribution. Survival is mark-independent and arrivals use the same mark distribution, so conditional on terminal count `N=n>0`, terminal marks are iid from the same frozen distribution.

Let

\[
\mu=E[Y],\qquad \Sigma=\operatorname{Cov}(Y)
\]

for the 21-dimensional vector over the Chapter 2 trait grid. These moments are evaluated deterministically by quadrature over the clamped-normal pollinator trait distribution and the frozen generalist/specialist and introduced/native mixtures.

For the terminal community kernel

\[
K=\begin{cases}
N^{-1}\sum_{i=1}^N Y_i,&N>0,\\
0,&N=0,
\end{cases}
\]

write

\[
p=P(N>0),\qquad h=E[N^{-1}I(N>0)].
\]

Then the finite-k kernel moments are exact:

\[
E[K]=p\mu,
\]

\[
\operatorname{Cov}(K)=h\Sigma+p(1-p)\mu\mu^T.
\]

For the island-minus-mainland contrast `G=K_I-K_M`, the two scenarios are independently generated, so

\[
E[G]=E[K_I]-E[K_M],
\]

\[
\operatorname{Cov}(G)=\operatorname{Cov}(K_I)+\operatorname{Cov}(K_M).
\]

## 3. Deterministic mean-field limit

As `k -> infinity`, empty-community probability vanishes and kernel covariance goes to zero. The deterministic limit is therefore

\[
g_\infty(x)=\mu_I(x)-\mu_M(x).
\]

For the frozen Chapter 2 zero-adjustment model, `g_infinity` is **positive at all 21 starting states**:

- minimum contrast = **0.0207650** at the edge of the trait grid;
- maximum contrast = **0.149396** at `x=0.5`;
- deterministic mean-field classification = **all-positive**.

Thus mixed branch geometry does **not** survive the exact deterministic mean-field limit. In the asymptotic sense, branch identity is a finite-community realization phenomenon.

That conclusion does not imply that the Chapter 2 result is a rare-extinction artefact. The rate at which finite-community composition fluctuations disappear matters.

## 4. Gaussian finite-size layer

The second-order approximation uses the **exact finite-k mean and covariance above** and only approximates the shape of the 21-dimensional kernel-contrast distribution:

\[
G_k\approx \mathcal N(m_k,C_k).
\]

The Gaussian branch probabilities were evaluated with the prespecified RNG and 200,000 draws per `k`. No parameter, seed or `k` value was selected after inspection.

Comparison with the existing six-seed ABM system-size audit gives:

| k | ABM mixed fraction | Gaussian mixed probability | absolute error |
|---:|---:|---:|---:|
| 1 | 0.71354 | 0.78241 | 0.06887 |
| 2 | 0.77604 | 0.81404 | 0.03799 |
| 4 | 0.73611 | 0.76765 | 0.03153 |
| 8 | 0.67014 | 0.68136 | 0.01122 |
| 16 | 0.56424 | 0.57078 | **0.00654** |

The approximation is poorest in the most discrete regime and becomes quantitatively accurate as system size increases. At `k=16`, the island-like empty-community probability is approximately `2.14e-16`, yet more than half of ABM realizations remain mixed and the Gaussian approximation predicts almost exactly the same fraction.

This separates two effects:

1. **rare empty-community / very-small-N events** are important at `k=1` but are not required for branching;
2. **finite composition fluctuations around a single-signed mean-field kernel** remain sufficient to generate branch heterogeneity at much larger finite system size.

## 5. Covariance scaling

The exact contrast covariance trace approaches

\[
\operatorname{tr}(C_k)\sim \frac{C}{k},
\]

with

\[
C=0.989454.
\]

Numerically, `k * tr(C_k)` moves from 1.535 at `k=1` to 1.014 at `k=16`, 1.001 at `k=32` and 0.9898 at `k=1024`, directly recovering the expected `1/k` finite-size scaling.

The Gaussian extrapolation consequently moves toward the deterministic all-positive limit:

| k | Gaussian mixed | Gaussian all-positive |
|---:|---:|---:|
| 32 | 0.4377 | 0.5623 |
| 64 | 0.2841 | 0.7159 |
| 128 | 0.1320 | 0.8680 |
| 256 | 0.0342 | 0.9658 |
| 512 | 0.00266 | 0.99735 |
| 1024 | 0.000025 | 0.999975 |

These rows are approximation-based extrapolations, not additional ABM runs and not natural abundance predictions.

## 6. Interpretation for Chapter 2

The finite-community model choice can now be stated more precisely.

- A deterministic mean-field model would erase the focal community-realization branch distribution because its limiting response is all-positive.
- The full ABM is necessary in the small-N regime, where Gaussian approximation error is material and empty-community discreteness is non-negligible.
- By `k=8-16`, a second-order Gaussian description already tracks ABM branch probability closely, showing that branch heterogeneity is not dependent on rare extinction events.
- Branching is therefore **finite-community in the asymptotic sense but relational-compositional rather than merely extinction-noise driven**.

This sharpens, rather than replaces, the Chapter 2 hierarchy:

\[
\text{richness/opportunity sets the coarse regime}
\rightarrow
\text{finite realized composition × starting state selects branches}
\rightarrow
\text{downstream channels propagate contingently}.
\]

## 7. What this is not

This audit does not claim to solve the full master equation for the marked adaptive process, and it is not a formal Fokker–Planck or van Kampen LNA derivation for the trait-adjusting model. The exact layer is the terminal count distribution and finite-k kernel moments in the zero-adjustment submodel; the branch-probability layer is Gaussian. `k` is a system-size device, not an estimate of natural pollinator abundance.

A full adaptive LNA/PDE treatment remains a separate theory project.
