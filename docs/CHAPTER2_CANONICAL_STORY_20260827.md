# Chapter 2 canonical story

Updated: 2026-08-31

## One-sentence claim

> **Response direction under community reorganization is relational rather than intrinsic: partner turnover reshapes the response geometry, organismal starting state is evaluated against the community actually realized, state × community non-additivity remains consequential, local filtering reallocates branch identity, and downstream assurance mainly modifies magnitude; world comparison shows that outcomes are measured much more often than the processes needed to distinguish those branches, while Izu localizes the present empirical signal to source state plus background community composition rather than beyond-composition sorting.**

This is the canonical Chapter 2 story. Older `minimal generator`, `11/11 validation coverage`, beneficial `support`, prevalence-like simulation-frequency, assurance sign-rescue and stable-80.17%-magnitude framings are superseded for manuscript interpretation.

The active narrative order is:

```text
model possibilities
    -> relational response geometry
        -> world confrontation
            -> process-measurement / identifiability bottleneck
                -> Izu mechanistic-resolution zoom
                    -> Chapter 3 measurement handoff, not validation
```

The exact analytic coordinate is the trajectory-conditioned interaction-kernel difference `G_omega(x0)`. See `docs/CHAPTER2_INTERACTION_KERNEL_DERIVATION_20260828.md` and the interpretation correction in `docs/CHAPTER2_RELATIONAL_ROBUSTNESS_CORRECTION_20260831.md`.

## 1. The Chapter 2 problem

The broader programme shows that island-associated floral and reproductive responses do not form one identical multivariate response vector. Chapter 2 asks a narrower mechanistic question:

> **Why can a common broad interaction perturbation be expressed through different biological response directions?**

The paper isolates post-establishment ecological response to pollinator-community reorganization. It does not identify why an island acquired a particular species pool, source state, colonization history or interaction architecture.

## 2. Response sign is a relation between state and realized community

The model evaluates 21 starting positions against the same mainland-like and island-like pollinator trajectory within each realization. The implemented response coordinate is

`G_omega(x0) = K_I,T(Phi_I,T(x0; omega_I)) - K_M,T(Phi_M,T(x0; omega_M))`.

Thus response is not an intrinsic property of starting state or community in isolation. Starting state supplies the coordinate at which a realized community kernel is evaluated; the realized trajectory changes that kernel and, with trait adjustment, may also change the endpoint state.

At zero trait adjustment, `Phi_E,T(x0)=x0`, so state dependence remains explicitly in `K_I,T(x0)-K_M,T(x0)`. Trait adjustment therefore changes how state dependence is expressed; it does not create state dependence de novo.

## 3. Possibility and regime structure

Across the historical frozen baseline of 96 matched community realizations:

- mixed-sign: 41;
- all-positive: 42;
- all-negative: 13.

Across the fixed 48-point joint 10-parameter design:

- mixed mean geometry: 16;
- all-positive: 22;
- all-negative: 10.

Partner loss and arrival are the strongest sign-stable fixed-surface regime associations:

- loss coefficient `+0.634`;
- arrival coefficient `−0.626`;
- additive diagnostic `R² = 0.611`;
- leave-one-point-out RMSE `0.329`.

These are synthetic surface diagnostics, not field-causal coefficients or natural frequencies.

## 4. The decomposition headline is ordering, not one percentage

The historical 21 × 96 baseline decomposition is:

- starting-position additive main effect: `2.18%`;
- community-realization additive main effect: `80.17%`;
- starting-position × community-realization non-additivity: `17.64%`.

The earlier wording that the non-additive remainder also contained `cell-level simulation variation` was incorrect. Each community trajectory is generated once and shared across all starting positions; conditional on that trajectory each cell is deterministic. The 17.64% is therefore exact non-additivity in that fixed response matrix.

The exact percentages are not stable population parameters. A prespecified six-seed sensitivity gives:

- community realization `69.34–80.17%`;
- starting-position additive effect `2.17–3.14%`;
- non-additivity `17.64–27.91%`.

The historical seed is the upper end of the community range but remains the frozen baseline; it was not replaced after inspection.

Across `steps={30,60,120,240}`, community realization remains the largest component at every horizon, starting-position share ranges `0.59–4.26%`, and mixed geometry remains present (`65, 48, 41, 43` of 96). Across trait-adjustment values `0–0.06`, community realization is again largest. At adjustment `0`, mixed geometry is `64/96`, starting-position additive share is only `0.18%`, and non-additivity is `32.50%`.

Therefore the defensible structural claim is:

> **Starting state alone is a weak additive predictor, but state remains essential as a coordinate evaluated relative to the realized community. Community realization is the larger additive component and state × community non-additivity is consequential.**

## 5. Mixed geometry does not require reduced initial richness

A prespecified equal-richness sensitivity sets the mainland-like and island-like initial pollinator counts to `9` and `9`, retaining all other baseline differences in loss, arrival, trait dispersion, generalist fraction and replacement fraction.

The result is:

- mixed-sign `53/96`;
- all-positive `31/96`;
- all-negative `12/96`.

Therefore:

> **Reduced initial pollinator richness is not necessary for mixed response geometry.**

Do not strengthen this to “island restructuring is unnecessary”; other scenario differences remain.

## 6. Local filtering and assurance act at different levels

Local availability / interaction filtering changes branch identity bidirectionally but asymmetrically. At synthetic filtering strength `0.40`:

- negative → non-negative: `15.67%`;
- positive → non-positive: `56.54%`.

Autonomous assurance acts downstream. Among 580 eligible declines, multipliers through `4×` yield zero sign rescues while commonly attenuating decline magnitude.

Hence filtering reallocates branches; assurance modifies propagation magnitude in the declared envelope.

## 7. World confrontation is outcome-rich but process-poor

The 25 research entries are not 25 independent archipelagos. They establish response breadth and reveal a measurement asymmetry.

Direct measurements are available for:

- response outcome: `21/25`;
- community functional shift: `13/25`;
- local filtering: `9/25`;
- richness / functional-diversity change: `8/25`;
- source functional state: `5/25`;
- partner loss: `5/25`;
- reproductive assurance: `5/25`;
- partner arrival / replacement: `2/25`.

This is the stronger interpretation than the naked `0/25` full-contract count. The synthetic theory says turnover balance matters, while existing island literature most rarely measures the arrival/replacement side of that balance.

The full outcome-independent plant-response contract still passes in `0/25`, so `H0–H4`, leave-one-system/archipelago-out evaluation and permutation remain `not_evaluable`. No predictor is reconstructed from observed outcome state.

## 8. Why Izu matters

Izu is a focal mechanistic-resolution system, not a formal global ranking winner or validation set. It connects source floral state, mainland/source and island pollinator composition, numeric pollinator traits, interaction structure, raw realized matching and null-corrected matching.

The defensible hierarchy is:

```text
source floral state + broad community composition
    -> realized raw matching                         supported

exact island-centre magnitudes / ordering
    -> additional identification                    weak / non-unique

signed source position
    -> null-corrected non-random partner sorting    unsupported
```

A prespecified Oshima-source bridge is also unsupported, showing that source regimes are not interchangeable.

Thus Izu increases resolution by locating the current signal at source state plus background community composition rather than treating a raw positive association as proof of within-community sorting or causal floral evolution.

## 9. Handoff to Chapter 3

Chapter 2 identifies the measurement contract that broad comparisons do not jointly satisfy and that the current Izu secondary analysis only partly resolves:

```text
source state
    + partner loss and arrival/replacement
        + community assembly
            + realized partner sorting
                + partner effectiveness
                    + reproductive dependency / outcome
```

Chapter 3 advances to higher-resolution focal measurement in the same Izu series. No Chapter 3 phenotype is used as Chapter 2 validation, Bombus-causation proof, pollinator-selection proof or external prediction success.

## Claim ceiling

Do not claim that:

- starting position alone determines response;
- a small starting-position additive percentage means state is unimportant;
- trait adjustment creates state dependence de novo;
- `80.17%` is a stable population variance parameter;
- the old `cell-level simulation variation` wording remains valid;
- `41/96`, `53/96`, `16/48`, filtering rates or step sensitivities are natural frequencies or empirical thresholds;
- equal initial richness removes all island-like community differences;
- partner-loss/arrival coefficients are causal field effects;
- assurance is a sign-rescue mechanism in the tested envelope;
- the 25 entries are independent archipelago replicates or formal external prediction;
- Izu was selected by an outcome-independent ranking;
- raw matching establishes beyond-composition sorting;
- Chapter 3 phenotype proves Chapter 2 mechanism; or
- the model explains the historical origin of island biotas or source states.
