# Ecology Letters positioning — Chapter 2

Updated: 2026-09-12

## Editorial object

Do not pitch this as an island-pollination simulation with an interesting `k` threshold.

Pitch it as a general ecological result:

> The identity of the dominant determinant of ecological response can itself change across stochastic community regimes because realization-driven variance averages down while persistent state-dependent contrasts remain. This rank reversal can occur while state-by-community interaction remains substantial at finite system size.

The Chapter 2 pollination model is the mechanistic demonstration; the generic smooth-response derivation and exact bilinear case supply the general sufficient conditions and the correlated-community countercondition.

## General principle

For `Y_k=f(X,Zbar_k)`, independent averaging gives a generic asymptotic separation:

- starting-state main effect: `S_k = S_inf + O(1/k)`;
- community-realization main effect: `C_k = A_C/k + o(1/k)`;
- state-by-community interaction: `I_k = A_I/k + o(1/k)` to first order.

If `S_inf>0` and the small-system regime initially has `C_1>S_1`, a determinant-rank crossover must occur at some finite scale.

The ecologically relevant scaling coordinate is not raw richness. It is the degree to which community stochasticity is independently averaged.

## Countercondition

For correlated community units,

`Var(Zbar_k)=sigma^2[rho+(1-rho)/k]`.

Shared stochastic forcing leaves a realization-variance floor. In the exact bilinear case, asymptotic starting-state dominance requires

`a^2 Var(X) > b^2 sigma^2 rho`.

Thus synchronous or spatially correlated communities can retain community-realization dominance despite increasing nominal size.

This countercondition is essential for an Ecology Letters framing because it turns the result from a model-specific monotonic pattern into a falsifiable statement about when averaging should and should not reorder ecological determinants.

## Chapter 2 demonstration

The admitted active-adjustment audit provides the motivating nonlinear ecological case:

- median starting-position share: `2.55% -> 55.84%` from `k=1` to `k=16`;
- median community-realization share: `72.98% -> 12.72%`;
- starting > community in `6/6` prespecified seeds from `k=4` onward;
- mixed-sign realizations persist at `k=16`: `28–42/96`;
- median non-additivity is `49.47%` at `k=4` and remains `31.99%` at `k=16`.

The numerical crossover near `k=4` remains model-specific and must never be presented as a natural threshold.

## Strongest manuscript claim

> Community averaging can reverse the ranking of ecological response determinants when realization-driven variance decays faster than persistent state-dependent differences, without requiring relational interaction structure to disappear at the finite-community crossover.

A companion negative claim is equally important:

> Rank reversal is not guaranteed when shared community stochasticity produces a variance floor larger than the persistent state effect.

## Connection to Chapter 1

Chapter 1 establishes that a broadly shared geographic/source-pool gradient can be associated with different regional multivariate floral/reproductive response vectors.

Chapter 2 must not claim to have causally explained those empirical regional differences. Instead, it supplies a general response architecture showing why a common broad perturbation need not produce a common response vector: the relative dominance of starting state and realized community can itself vary among regimes, while interaction remains finite-system relevant.

## Proposed Ecology Letters title

Preferred:

**Community averaging reverses the hierarchy of ecological response determinants**

Alternatives:

- **The dominant determinants of ecological response change across stochastic community regimes**
- **Ecological determinant hierarchies are regime dependent**

## Five-part Letter architecture

1. **Problem (<100 words):** Ecology commonly ranks drivers as if their importance were intrinsic; ask whether driver ranking can itself depend on the stochastic regime.
2. **General condition:** smooth-response derivation plus exact bilinear case; define persistent state contrast versus averaging realization variance.
3. **Nonlinear ecological demonstration:** Chapter 2 plant–pollinator response model, exact richness control, active-adjustment rank crossover and finite-k interaction persistence.
4. **Failure condition:** correlated/synchronous community stochasticity produces a floor and can block crossover.
5. **Ecological consequence (<200-word conclusion):** context dependence can involve changes in the identity of the dominant determinant, not merely changes in effect magnitude.

## Main-text compression for EL

Keep at most four main figures:

- Fig. 1 — general theory: `S_k`, `C_k`, `I_k`, crossover and correlated countercondition;
- Fig. 2 — Chapter 2 nonlinear response geometry and exact realized-richness control;
- Fig. 3 — active-adjustment rank crossover including non-additivity and mixed-sign persistence;
- Fig. 4 — general ecological interpretation / empirical claim boundary, or move this to SI if word/figure economy requires.

Filtering, assurance, world-island audit detail and Izu prospective field design should move largely to Supporting Information unless they are needed to establish the general mechanism boundary.

## Admission gate before changing the manuscript title

Promote the EL framing only if:

1. the generic audit frozen in `data/design/chapter2_el_rank_crossover_generalization_freeze_20260912.json` passes unchanged;
2. existing Chapter 2 scientific gates remain green;
3. the manuscript explicitly distinguishes finite-k interaction persistence from asymptotic interaction persistence;
4. no natural interpretation of model-specific `k=4` is introduced.
