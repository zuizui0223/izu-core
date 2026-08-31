# Chapter 2 relational robustness correction

Updated: 2026-08-31

## Decision

The historical 2026-08-27 freeze chain remains byte-auditable and is not rewritten. One interpretation sentence attached to the frozen two-way decomposition is superseded for active manuscript use.

### Superseded wording

> The non-additive remainder contains starting-position-by-community contingency plus cell-level simulation variation because the fixed design has one value per cell.

### Correct interpretation

For each matched community realization, the mainland-like and island-like pollinator trajectories are generated once and shared across all 21 plant starting positions. `endpoint_on_trajectory` contains no additional random draw. Conditional on the shared trajectory, every starting-position × community-realization response cell is therefore deterministic.

For the fixed response matrix

`Y(x, omega) = grand + starting-position main effect + community-realization main effect + non-additive remainder`,

the residual sum of squares is the exact starting-position × community-realization non-additive component of that fixed matrix. It is not mixed with within-cell simulation noise.

This correction does not promote the 17.64% baseline value to a population interaction-variance estimate. The 96 trajectories are a finite synthetic ensemble, so all numerical sum-of-squares shares remain design- and ensemble-specific diagnostics.

## Starting state is relational, not an additive percentage

A small additive starting-position sum-of-squares fraction does not mean that starting state is absent from response geometry. At zero trait adjustment the endpoint state remains `x0`, so the exact coordinate reduces to

`G_omega(x0) = K_I,T(x0) - K_M,T(x0)`.

Starting state therefore remains the input coordinate at which two realized community kernels are compared. When different communities alter the sign or shape of this relationship differently, state dependence appears in the starting-position × community non-additive term rather than in the additive starting-position main effect.

Trait adjustment can change how state dependence is partitioned between additive and non-additive components, but it must not be described as creating state dependence de novo if mixed geometry persists at zero adjustment.

## Headline inference after the audit

The active Oikos-facing headline is structural rather than magnitude-specific:

> Response direction is relational: it depends on organismal state evaluated against the community realized after reorganization. Starting state alone is a weak additive predictor, realized community is the larger additive component across the declared design, and state × community non-additivity remains consequential.

The historically frozen baseline values (2.18% starting position, 80.17% community realization, 17.64% non-additivity) remain reportable as one baseline decomposition, but not as stable population-like percentages.

## Structural constants being audited

The prespecified 2026-08-31 audit tests:

- model horizon `steps in {30, 60, 120, 240}`;
- trait adjustment `{0, 0.01, 0.03, 0.06}`;
- the historical seed plus five sensitivity seeds without seed replacement;
- equal initial mainland/island pollinator richness at 9/9 while retaining all other baseline scenario differences;
- direct-measurement availability across the frozen 25-entry source ledger.

The equal-richness result, if mixed geometry persists, supports only that **pollinator richness reduction is not necessary for mixed response geometry**. It does not remove partner-loss, arrival, dispersion, generalist-fraction or replacement differences and therefore cannot establish that the phenomenon is independent of island-like community reorganization more generally.

## External literature interpretation

The 25-entry audit should emphasize the asymmetry between abundant response measurement and sparse process measurement rather than the naked `0/25` contract count. In particular, the model identifies turnover balance as an important regime-level diagnostic, while the source ledger shows that arrival/replacement is among the least directly measured inputs. This converts the readiness stop into a measurement agenda without promoting the inventory to an independent-archipelago sample.
