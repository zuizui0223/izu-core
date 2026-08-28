# Chapter 2 model specification for manuscript

Updated: 2026-08-28

This document extracts the exact model rules needed to finish the active Research Article Methods. It is a manuscript specification, not a new model and not an empirical calibration.

## 1. Baseline pollinator environments

Mainland-like scenario:

- initial pollinator types: 9
- partner arrival probability per step: 0.28
- partner loss probability per extant partner per step: 0.015
- pollinator trait dispersion: 0.22
- generalist fraction: 0.35
- replacement / introduced fraction: 0.05

Oceanic-island scenario:

- initial pollinator types: 4
- partner arrival probability per step: 0.12
- partner loss probability per extant partner per step: 0.055
- pollinator trait dispersion: 0.16
- generalist fraction: 0.58
- replacement / introduced fraction: 0.22

Pollinator traits are generated around 0.5 on the bounded synthetic matching axis [0,1].

## 2. Plant-lineage distributions

For the broader lineage simulations:

- initial synthetic functional trait: truncated Normal(mean 0.5, SD 0.18)
- pollinator dependency `d`: Uniform(0.35, 0.95)
- assurance ceiling `c`: Uniform(0.10, 0.90)
- assurance responsiveness `r`: Uniform(0.004, 0.035)
- trait-adjustment scale `a`: Uniform(0.01, 0.055)
- initial assurance state: 0.08

The principal threshold design uses 24 lineages and 120 steps. These are synthetic design choices, not fitted demographic quantities.

## 3. Trait matching

For plant trait `x`, pollinator trait `p`, and pollinator breadth `b`:

`mismatch = |x - p|`

`raw_match = exp(-(mismatch / b)^2)`

with:

- generalist breadth `b = 0.42`
- specialist breadth `b = 0.16`

If the partner is introduced/replacement, the match is multiplied by 0.82.

All resulting match values are bounded to [0,1].

## 4. Fixed visit-budget service in the response-geometry model

For an extant pollinator assemblage with match values `m_j`:

`mean_match = mean_j(m_j)`

`service = 1 - exp(-saturation * mean_match)`

If no pollinator remains, service is zero.

This formulation prevents pollinator richness from automatically increasing total visitation opportunity: richness changes partner composition while service uses the mean match under a fixed budget.

Equivalently, for environment `E` and fixed plant state `x`, define the community interaction kernel

`K_E(x) = mean_j[a_Ej * exp(-((x - p_Ej) / b_Ej)^2)]`,

where `a_Ej` is the replacement penalty or 1. Then

`S_E(x) = 1 - exp(-saturation * K_E(x))`.

Because the saturation map is strictly increasing, a fixed-state service contrast has the same sign as `K_island(x) - K_mainland(x)`. The implemented endpoint geometry also permits trait adjustment, so its exact coordinate is instead the trajectory-conditioned composite

`G_omega(x0) = K_island,T(Phi_island,T(x0)) - K_mainland,T(Phi_mainland,T(x0))`,

where `Phi_E,T` is the final plant state under environment `E`. The shortcut `K_island(x0) - K_mainland(x0)` is not exact when the two trajectories change final plant state. Per-realization sign equivalence also does not allow the nonlinear mean service contrast to be replaced by a difference of mean kernels. The full derivation and executable identity audit are in `docs/CHAPTER2_INTERACTION_KERNEL_DERIVATION_20260828.md` and `data/results/chapter2_interaction_kernel_audit_frozen_20260828.json`.

## 5. Trait adjustment

When current service is below 0.45 and at least one pollinator is extant, the plant moves toward the currently best-matching pollinator:

`x_(t+1) = clamp[x_t + a * (p_best - x_t), 0, 1]`

where `a` is the lineage-specific trait-adjustment scale.

The current manuscript must state that this process is weak in the tested envelope and is not used as evidence for in-situ evolutionary dynamics.

## 6. Weighted opportunity network used for local-context analyses

For each plant lineage, the weighted opportunity row is constructed from final encounter scores under the fixed visit-budget identity:

`w_j = match_j / N_pollinators`

so that

`sum_j(w_j) = mean_j(match_j)`.

Thus the weighted-network row total equals the pre-saturation mean match used by the v4 service model.

## 7. Local availability / interaction filtering hierarchy

`support_strength = s` is filtering stress, not beneficial support. The same generic sensitivity strength is used in the nested plant, pollinator and pair availability layers; it is not an empirical assertion that those biological probabilities are equal.

### Plant availability

Each positive feasible plant/resource row is independently locally active with probability:

`P(plant active) = 1 - s`.

Zero active plants are allowed; the draw is not repaired or redrawn.

### Pollinator availability

Each island-feasible pollinator is locally active with probability:

`P(pollinator active) = 1 - s`.

The inherited v6 pollinator layer conditions on at least one globally active feasible pollinator.

### Pair availability

Within globally active pollinators, every positive feasible plant–pollinator pair is independently retained with probability:

`P(pair active | feasible, pollinator active) = 1 - s`.

The pair draw is not repaired if it creates partnerless plants or an empty local network.

### Projection and row-budget conservation

The final pair mask is the intersection of the independently drawn plant mask and the inherited pollinator/pair mask. For every retained positive plant row, surviving pair weights are rescaled so that the row total equals the original global opportunity total. Partnerless positive plants are removed locally rather than assigned manufactured service. No new plant, pollinator or pair can be created.

At `s = 0`, the filtering projection is bypassed exactly.

## 8. Local weight realization

After support projection, the inherited local-context weight layer multiplies each retained pair by a positive random affinity. At context-strength `h`:

`factor_j = (1 - h) + h * U(0.1, 1.9)`.

The row is then normalized back to its exact pre-context row total. The Chapter 2 effective-service simulations use `h = 0.5`.

This layer redistributes weight within retained support; it does not create links or change the plant's total opportunity budget.

## 9. Partner effectiveness and effective service

For local realized pollinator `j`, the quality multiplier at quality strength 1 is:

`q_j = 1 + U(-0.8, 0.8)`

so `q_j` lies in [0.2,1.8]. The quality draw is geography-independent and acts only on existing positive pair weights.

For plant row weights `w_j`:

`effective_score = sum_j(w_j * q_j)`

`effective_service = 1 - exp(-saturation * effective_score)`.

The local-context and assurance threshold analyses use quality strength 1.

## 10. Reproductive propagation and assurance

Let:

- `d` = pollinator dependency
- `S` = current effective service
- `c` = assurance ceiling
- `A` = current assurance state.

The pollinator-dependent route is:

`P = d * S`.

The autonomous route is:

`U = (1 - d) * c * A`.

The combined reproductive output is:

`R = 1 - (1 - P) * (1 - U)`

bounded to [0,1].

If `R < 0.50`, assurance state increases as:

`A_(t+1) = min(c, A_t + r)`

where `r` is the lineage-specific assurance responsiveness.

This architecture intentionally adds a compensating downstream route. Therefore magnitude attenuation is partly structural; sign rescue is the stronger discriminating outcome.

## 11. Assurance sensitivity multiplier

For multiplier `k >= 0`:

`c_k = min(1, c * k)`

`r_k = min(1, r * k)`.

The fixed sensitivity envelope is:

`k in {0, 0.5, 1, 1.5, 2, 3, 4}`.

A lineage is eligible for sign rescue only when, at `k = 0`, both island-minus-mainland effective-service and reproduction contrasts are negative. A sign rescue requires the reproduction contrast to become non-negative while upstream service remains unchanged.

In the final fixed run, no eligible lineage crossed that sign boundary at any non-zero multiplier through 4×.

## 12. Response-geometry matched design

The starting-position grid is:

`x_0 in {0.00, 0.05, ..., 1.00}`.

Within each realization, every starting position receives the same mainland pollinator trajectory and the same island pollinator trajectory. This common-random-number design separates starting-position effects from community-realization differences.

The primary fixed run uses 96 matched pollinator-community realizations.

## 13. Joint robustness design

The fixed joint sensitivity analysis uses:

- 48 Latin-hypercube points
- 10 simultaneously varied parameter dimensions
- 24 matched community realizations per point
- fixed seed ensemble

The ten dimensions are trait dispersion, generalist fraction, replacement fraction, partner loss, partner arrival, saturation, trait adjustment, generalist breadth, specialist breadth and replacement penalty.

Each point is classified from the mean starting-position geometry as mixed-sign, all-positive or all-negative.

## 14. Local-context threshold design

The fixed threshold envelope is:

`support_strength in {0, 0.10, 0.25, 0.40, 0.50, 0.60, 0.75}`

with:

- saturations 1, 2, 3
- 12 replicates per saturation
- 4 local contexts
- 24 lineages
- 120 steps
- common seed ensemble across strength values.

For each lineage, the first non-zero strength at which the sign of island-minus-mainland reproduction differs from the `s = 0` sign is recorded.

## 15. Interpretation boundary

None of the following are empirically identified by this specification:

- the numerical location of the synthetic trait sign-switch boundaries;
- the median local-filtering first-sign-change strength 0.40;
- the frequency of mixed, all-positive or all-negative design points;
- the tested assurance multiplier needed in any real plant lineage;
- 24 lineages, 120 steps, or saturation values as natural demographic quantities.

These are synthetic model sensitivity and robustness quantities. Empirical claims remain controlled by `docs/CURRENT_EVIDENCE_STATE.md`.
