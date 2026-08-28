# Chapter 1 → Chapter 2 HOW/WHY audit

Updated: 2026-08-28

## Audit basis

- `izu-core` current `main` at the 2026-08-28 audit freeze: `98cbb6975295e8c2b8f72291a895d145dbf76f36`.
- Chapter 1 (`island`) current `main`: `9d6677d4ead4b331e327028fcd1a6d2a59c83e37`.
- Canonical Chapter 1 when/where workflow: run `32837335384`, successful at head `a3fe6d63e41cad37f0605b512762a599d64890b6`.
- Chapter 2 parent scientific gate: `data/design/chapter2_scientific_gate_run_20260827.json` and its frozen Phase 1–3 summaries.
- Additional diagnostic design, frozen before execution: `data/design/chapter2_conditional_why_diagnostics_freeze_20260827.json`.
- Additional diagnostic result: `data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json`.
- External-prediction readiness design and result: `data/design/chapter2_external_prediction_challenge_freeze_20260828.json` and `data/results/chapter2_external_prediction_readiness_frozen_20260828.json`.

## Current handoff

Chapter 1 is a **WHEN/WHERE** chapter. It establishes, within opportunistically observed floras, that isolation/source-pool-accessibility gradients are associated with floral and reproductive filtering in northern mid-latitude and tropical regions, that the signals persist in native non-endemic assemblages, and that the two regional multivariate response vectors differ. It does not identify the pollinator or historical mechanism that produced those vectors, and it does not reduce either vector to a named classical pollination syndrome.

Chapter 2 is a **mechanistic HOW plus proximal WHY** chapter. Its direct scope is post-establishment response: how a declared pollinator reorganization propagates through functional matching, realized local filtering, effective service and reproduction, and why lineages can occupy different response branches under the same broad perturbation.

The defensible bridge is therefore:

> Chapter 1 establishes that one broad geographic/source-pool gradient is expressed through different regional multivariate response vectors. Chapter 2 tests a model class in which one broad interaction perturbation can generate different response signs because matching consequences depend on starting functional position and realized community context.

This is a theoretical/mechanistic bridge, not an empirical assignment of the Chapter 1 northern-midlatitude and tropical vectors to particular Chapter 2 parameter regimes.

## HOW, proximal WHY and ultimate WHY

| Level | Question | Current Chapter 2 answer | Claim ceiling |
|---|---|---|---|
| HOW | Through which response architecture does interaction reorganization propagate? | Pollinator turnover and matching alter functional service; local filtering changes the realized branch; assurance changes downstream magnitude without sign rescue. | Directly represented within the declared synthetic model. |
| Proximal WHY | Why can the same broad perturbation yield opposite lineage responses? | The negative portion of the starting-position surface changes with the balance of partner loss and arrival and other matching dimensions; realized community state dominates cell-level variation; starting position and community combine non-additively; filtering changes positive and negative branches at different rates. | A diagnostic explanation within the fixed model design, not a field-estimated causal effect. |
| Ultimate WHY | Why did an island acquire its biota, starting states, interaction architecture or historical regional vector? | Not tested. Assembly, colonization, regional species pools, persistence and evolutionary history remain upstream alternatives. | Chapter 2 must not claim to explain formation of the Chapter 1 regional contexts or starting states. |

## External-prediction ceiling

The 25-entry source-readiness audit does not raise this handoff from model-conditional proximal WHY to an empirically general predictive WHY. Zero entries passed the full outcome-independent plant-response contract, so `H0`–`H4` comparison and held-out system/archipelago prediction are not evaluable. Chapter 2 therefore remains at Level 2: it explains within the frozen model why heterogeneous responses are possible, while external systems provide retrospective explanation, reality boundaries and retained falsification.

This stop protects the Chapter 1 → Chapter 2 bridge. Chapter 1 regional vectors are not assigned to the four model-derived axes (`T`, `D0`, `C`, `F`), and the absence of a formal external prediction set is not repaired by importing Chapter 3 phenotype or inferring predictors from observed outcomes.

## Frozen additional diagnostics

### Regime-boundary associations

The additive ten-parameter diagnostic explained `R² = 0.611` of variation in the fraction of the 21-point starting-position grid with negative mean response. Leave-one-point-out RMSE was `0.329`, so the fit is explanatory/descriptive rather than a precise regime predictor.

The two largest full-range coefficients were:

- partner-loss multiplier: `+0.634`, with the same sign in all 48 leave-one-point-out fits;
- partner-arrival multiplier: `−0.626`, also sign-stable in all 48 leave-one-point-out fits.

Thus, within the declared joint design, greater partner loss and lower partner arrival accompany a larger negative portion of the response surface. The positive-to-mixed boundary was most separated by replacement penalty (Cliff's delta `−0.574`) and partner loss (`+0.506`); the mixed-to-all-negative boundary was most separated by partner arrival (`−0.550`). These are design-space associations, not causal field estimates.

### Starting position × community realization

For the baseline `21 × 96` response matrix, the two-way sum-of-squares partition was:

- starting-position main effect: `2.18%`;
- community-realization main effect: `80.17%`;
- starting-position-by-community non-additive remainder: `17.64%`.

Observed response sign differed from the fitted additive sign in `271/2016 = 13.44%` of cells. Starting position therefore organizes the mean U-shaped sign boundary, but it is not the dominant source of cell-level variation. Realized community state is the largest component, and a material non-additive remainder shows that the effect of starting position cannot be reduced to an additive shift shared by every community realization. Because the fixed matrix contains one simulated value per cell, the non-additive remainder also contains cell-level simulation variation and is not a pure interaction variance estimate.

Across the 48 joint points, median additive-sign mismatch was highest in the mixed regime (`18.06%`) compared with all-positive (`13.59%`) and all-negative (`11.61%`) regimes. This is consistent with greater sign contingency near a mixed surface, but the overlap across points prevents a deterministic regime rule.

### Directional asymmetry of local filtering

At zero filtering, the 864 fixed lineage contrasts contained 268 negative and 596 positive responses. At every non-zero filtering strength, positive baselines crossed to non-positive at a higher conditional rate than negative baselines crossed to non-negative.

| Filtering strength | Negative → non-negative / 268 | Positive → non-positive / 596 | Rate difference |
|---:|---:|---:|---:|
| 0.10 | 9.33% | 14.93% | −5.60 percentage points |
| 0.25 | 15.30% | 38.42% | −23.12 percentage points |
| 0.40 | 15.67% | 56.54% | −40.87 percentage points |
| 0.50 | 11.94% | 64.43% | −52.49 percentage points |
| 0.60 | 17.54% | 77.01% | −59.48 percentage points |
| 0.75 | 49.25% | 84.40% | −35.14 percentage points |

Among contrasts that changed sign somewhere in the envelope, the median first transition was `0.60` for baseline-negative responses and `0.40` for baseline-positive responses. Local filtering is therefore bidirectional but strongly asymmetric toward loss of positive branch identity in this fixed design. This refines the earlier neutral `branch allocator` description; it does not turn the synthetic rates into ecological frequencies.

## Required manuscript positioning

The Chapter 2 manuscript should now state all four boundaries explicitly:

1. Chapter 1 motivates the problem by establishing different regional multivariate vectors; Chapter 2 does not explain those particular regional vectors directly.
2. Chapter 2 supplies the mechanistic HOW and a proximal, model-conditional WHY.
3. Community realization and state-by-realization non-additivity are part of the explanation, so starting position alone must not be promoted as a universal generator.
4. Ultimate/historical WHY remains outside the current simulation and requires assembly, colonization, persistence or evolutionary evidence.

## Prohibited promotion

- Do not interpret 16/48 regimes, 41/96 realizations or any filtering transition rate as natural prevalence.
- Do not call the additive coefficients causal ecological effects.
- Do not assign northern-midlatitude or tropical Chapter 1 vectors to model regimes without a source-native mapping analysis.
- Do not treat the 17.64% non-additive remainder as a pure empirical interaction variance component.
- Do not retune seeds, parameter ranges, trait grids, realization counts or filtering strengths after these results.
- Do not claim an ultimate explanation for why the observed island contexts formed.
- Do not call the current 25-entry audit formal external prediction or treat its geographic-overlap labels as independent archipelago replication.
