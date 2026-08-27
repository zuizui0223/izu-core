# Chapter 2 manuscript tables

Updated: 2026-08-27

Tables 1–4 are generated from the frozen Chapter 2 synthetic gate outputs. Frequencies and thresholds are synthetic robustness/sensitivity descriptors, not natural ecological prevalence or empirically calibrated thresholds. Table 5 reports the separately source-locked Izu secondary analysis and its structural negative control.

## Table 1. Baseline scenario and lineage parameterization

| Quantity | Mainland-like | Oceanic-island | Status |
|---|---:|---:|---|
| Initial pollinator types | 9 | 4 | generic island-direction scenario |
| Partner arrival probability / step | 0.28 | 0.12 | generic island-direction scenario |
| Partner loss probability / extant partner / step | 0.015 | 0.055 | generic island-direction scenario |
| Pollinator trait dispersion | 0.22 | 0.16 | generic sensitivity choice |
| Generalist fraction | 0.35 | 0.58 | generic island-direction scenario |
| Replacement fraction | 0.05 | 0.22 | generic island-direction scenario |
| Generalist breadth | 0.42 | 0.42 | generic matching choice |
| Specialist breadth | 0.16 | 0.16 | generic matching choice |
| Replacement match multiplier | 0.82 | 0.82 | generic matching choice |

| Lineage/design quantity | Value | Status |
|---|---|---|
| Initial functional trait | truncated Normal(0.5, 0.18) | generic sensitivity choice |
| Pollinator dependency | Uniform(0.35, 0.95) | generic sensitivity choice |
| Assurance ceiling | Uniform(0.10, 0.90) | generic sensitivity choice |
| Assurance responsiveness | Uniform(0.004, 0.035) | generic sensitivity choice |
| Trait-adjustment scale | Uniform(0.01, 0.055) | generic sensitivity choice |
| Initial assurance state | 0.08 | generic sensitivity choice |
| Lineages | 24 | design choice |
| Steps | 120 | design choice |
| Saturation | 1, 2, 3 | sensitivity values |

## Table 2. Response geometry and joint robustness

| Result | Count / interval | Interpretation |
|---|---|---|
| Matched pollinator-community realizations | 96 | fixed synthetic design |
| Mixed-sign realizations | 41 of 96 | robustness descriptor, not prevalence |
| All-positive realizations | 42 of 96 | one-direction regime also occurs |
| All-negative realizations | 13 of 96 | one-direction regime also occurs |
| Mean sign switch 1 | 0.30–0.35 | synthetic starting-position coordinate |
| Mean sign switch 2 | 0.65–0.70 | synthetic starting-position coordinate |
| Joint Latin-hypercube points | 48 | 10 parameters varied jointly |
| Mixed mean geometry | 16 of 48 | nontrivial but non-universal region |
| All-positive mean geometry | 22 of 48 | regime boundary retained |
| All-negative mean geometry | 10 of 48 | regime boundary retained |
| Mixed-realization fraction across joint points | 0.0417–0.9167 | design-space robustness range |

## Table 3. Local-context and assurance threshold summaries

### Local availability / interaction filtering

| Filtering strength | Sign changes | Negative→non-negative | Positive→non-positive | Fraction of 864 contrasts |
|---:|---:|---:|---:|---:|
| 0.0 | 0 | 0 | 0 | 0.0% |
| 0.1 | 114 | 25 | 89 | 13.2% |
| 0.25 | 270 | 41 | 229 | 31.2% |
| 0.4 | 379 | 42 | 337 | 43.9% |
| 0.5 | 416 | 32 | 384 | 48.1% |
| 0.6 | 506 | 47 | 459 | 58.6% |
| 0.75 | 635 | 132 | 503 | 73.5% |

Any sign change across the declared envelope: **737 lineage contrasts**. Median first sign-change strength among those contrasts: **0.40**.

### Autonomous assurance

| Assurance multiplier | Sign rescues | Magnitude improvements | Fraction improved among 580 eligible declines |
|---:|---:|---:|---:|
| 0.0 | 0 | 0 | 0.0% |
| 0.5 | 0 | 565 | 97.4% |
| 1.0 | 0 | 555 | 95.7% |
| 1.5 | 0 | 545 | 94.0% |
| 2.0 | 0 | 545 | 94.0% |
| 3.0 | 0 | 541 | 93.3% |
| 4.0 | 0 | 539 | 92.9% |

Eligible baseline declines: **580**. Sign rescues anywhere through 4×: **0**. Upstream effective-service mismatches: **0**.

## Table 4. Conditional-WHY diagnostics from the unchanged frozen design

| Diagnostic | Result | Interpretation boundary |
|---|---:|---|
| Additive 10-parameter model `R²` | 0.611 | descriptive fit to 48 fixed design points |
| Leave-one-point-out RMSE | 0.329 | substantial predictive error; not a precise classifier |
| Partner-loss full-range coefficient | +0.634 | association with negative trait-grid fraction |
| Partner-arrival full-range coefficient | -0.626 | association with negative trait-grid fraction |
| Starting-position SS fraction | 2.2% | baseline 21 × 96 synthetic matrix |
| Community-realization SS fraction | 80.2% | baseline 21 × 96 synthetic matrix |
| Non-additive SS fraction | 17.6% | includes cell-level simulation variation |
| Additive-sign mismatch | 271 of 2016 (13.4%) | state-by-realization contingency diagnostic |
| Baseline filtering signs | 268 negative; 596 positive | fixed 864-contrast enumeration |
| Strength 0.40: negative → non-negative | 15.7% | denominator is 268 baseline-negative contrasts |
| Strength 0.40: positive → non-positive | 56.5% | denominator is 596 baseline-positive contrasts |
| Median first change, baseline negative / positive | 0.60 / 0.40 | synthetic filtering strengths, not field thresholds |

## Table 5. Focal Izu empirical triangulation and structural audit

| Analysis | Rows / plants | Slope | 95% CI | Additional diagnostic | Interpretation |
|---|---:|---:|---:|---|---|
| Frozen source-position × island-centre projection → raw `delta_TM_sp` | 83 / 30 | +0.5669 | +0.2977 to +0.8361 | sign concordance 63/83; all five leave-one-island slopes positive | realized raw matching is structured by correct source state plus community composition |
| Plant-source-position permutation, raw target | 10,000 draws | — | — | 0/10,000 null slopes ≥ observed; empirical one-sided p = 1/10001 | correct plant source identity carries information |
| Exact island-centre reassignment | 120 assignments | observed +0.5669 | range +0.4133 to +0.6078 | 13/120 assignments ≥ observed | exact five island-centre magnitudes/order are not uniquely identified |
| Source-position-only raw comparator | 83 / 30 | -0.2033 | — | R² 0.4091; AIC 362.1 vs full geometry R² 0.3649; AIC 368.1 | raw signal is strongly source-state structured |
| Same frozen projection → null-corrected `delta_TM_sp_z` | 83 / 30 | +0.0333 | -0.2680 to +0.3346 | sign concordance 42/83; permutation p = 0.3919 | no support for beyond-composition non-random matching |
| Prespecified Oshima-source sensitivity | 62 / 22 | +0.2808 | -0.3980 to +0.9596 | sign concordance 48.4%; one LOO slope slightly negative | source baseline is not interchangeable |

The Izu analysis is a same-system secondary triangulation, not an external validation of the synthetic model. The active claim ceiling is source floral state plus broad background community composition; historical Bombus causation, causal floral evolution, plant-specific partner centres and reproductive propagation remain untested.

## Interpretation boundary

Table 1 values define the synthetic model. Table 2 frequencies describe the declared stochastic and Latin-hypercube designs. Table 3 thresholds describe the declared sensitivity envelope. Table 4 coefficients, variance shares and transition rates are diagnostics of the unchanged frozen synthetic design. Table 5 is a source-locked empirical secondary analysis with an explicit null-corrected negative result. None of the synthetic quantities is a causal field estimate, an estimate of natural prevalence or an empirically identified island threshold; the Izu quantities do not validate the synthetic coordinate or identify causal floral evolution.
