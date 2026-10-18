# Joint Q3 analysis: bounded four-arm method check and executable decision code

**19 October 2026. One paper, PR #590; method work on PR #597. Not a registered or started biological confirmation.**

## What advanced

The 18 October 96,000-trial method package tested a ternary paired contrast for both endpoints. That is a legitimate submodel, but survival's four-arm interaction can take -2,-1,0,1,2. It also did not simulate the two endpoint arrays together. This follow-up checks the selected candidate method on that full interaction support and on explicitly correlated G/S pairs. No original finding or source experiment is overwritten.

The six follow-up scenarios and seeds were frozen in Git **1cba5710e6bafd9ef72b948df48279420895a33c** before new statistical outcomes. The local frozen-plan bytes match Git blob `7807c5a297a66eb11878e555f1c88435ff47026c` (SHA-256 `683520d2551b30a60d208df7de9654e4f8292dcef82b9ee405052a46014883db`). Code was tested before execution; the pre-outcome plan commit is not an independent external registration.

## Actual estimands and implementation

`scripts/q3_joint_inference_20261019.py` accepts complete founder-by-visitor arrays:

- Genetic outcome: first living founder-relative HIGH-I support loss before extinction, one binary indicator per historical A policy. The upstream raw-genotype and competing-event audit is still necessary.
- Survival: binary final occupancy for both policies under each of B8 and B4.5, with all original assignments retained, including deaths before the fork.

The returned contrasts are `G=G_E-G_F` and `S=(alive_E45-alive_F45)-(alive_E8-alive_F8)`. Neither survivors alone nor nested future streams are independent background units. The code preserves the full [-2,+2] interaction, computes two 97.5% marginal intervals with a t reference, and reports positive/negative/unresolved directions separately from exceeding the proposed .10 margin. Zero estimated variance is marked `degenerate_unresolved`, not automatic significance or equivalence.

The variance equals the exact conditional row-column empirical-bootstrap variance. The t interval itself does not have exact finite-sample coverage. For row deviations r, column deviations c and residuals e of a complete F-by-V array:

`V = sum(r^2)/F^2 + sum(c^2)/V^2 + sum(e^2)/(F^2 V^2)`.

Small 2-by-3 arrays were checked against all 108 ordered row-column resamples, independently of this formula.

## Executed follow-up: 60,000 complete statistical experiments

Each scenario has 10,000 trials on **160 independent levels per axis**, using fresh numerical seeds; no Model3 operators or reserved biological population seeds are used. G and S share row, column and cell random inputs. Their means therefore correlate rather than being implicitly independent.

The full-range scenarios have exact marginal projection variances .05 founder, .05 visitor and .85 residual at both endpoints. S assigns positive mass to both -2 and +2 and is asymmetric. These extremes are deliberately adversarial method stresses, not a claim that the previously derived B8 survival ceiling is false. The near-boundary scenarios use S mean .95 with variance components (.002,.002,.0435), yielding S in {0,1}; that is a statistical sensitivity, not a fitted source prediction.

| Scenario | True G,S | Correlation of estimated means | Both-positive detection | MC-adjusted lower bound |
|---|---|---:|---:|---:|
| Full range, aligned | .10,.10 | +.752 | 90.18% | 89.30% |
| Full range, opposed | .10,.10 | -.769 | 87.07% | 86.08% |
| Near-boundary survival | .10,.95 | -.182 | 93.42% | 92.68% |

| True-null check | Probability of any false rejection of a true null | MC-adjusted upper bound |
|---|---:|---:|
| Both null, aligned | 3.15% | 3.68% |
| Both null, opposed | 3.07% | 3.60% |
| G null but S=.95 | 2.00% | 2.43% |

Twelve Monte Carlo binomial intervals (six scenarios times two summaries) use a Bonferroni simultaneous error budget .05. These intervals quantify numerical simulation error, NOT uncertainty in the biological effects or DGP assumptions. The scenarios were fixed in advance; the method was selected using earlier checks and receives this fresh follow-up rather than being called independently chosen a priori.

All predeclared alternative-scenario lower bounds exceed .80; all applicable false-rejection upper bounds are below .05. This permits **continued method review of 160x160 with this specific rule**, not confirmation authorization. No claim covers every non-Gaussian, heterogeneous or degenerate array distribution. Two-way cluster methods do require distributional conditions; exact conditional variance alone is not universal coverage (Owen & Eckles 2012, doi:10.1214/12-AOAS547; Menzel 2021, doi:10.3982/ECTA15383).

## Candidate biological design is not silently activated

The existing 136x136 candidate, .10 proposed resolution choice, biological seed registry and #585 validator remain unchanged. A 160x160x1 candidate has 51,200 policy prefixes of 35 updates and 102,400 branches of 45 updates: **6,400,000 unique updates** (8,192,000 as the deliberately overcounted rectangular ceiling).

This package supplies working endpoint-analysis code and a bounded joint-method test. It does not supply an externally endorsed scientific margin, proof that the adverse scenario bounds Model3, an independent method-review approval, a approved biological runner/archive budget, or permission to consume confirmation seeds. `execution_authorized=false` remains explicit. Actual flower recovery following returning pollinators is not part of these two primary endpoints and remains a separate biological calibration.

## Verification and reproducibility

Six unit tests passed after an initial missing-implementation failure. The earlier ten OC tests also passed unchanged. The six saved NPZ files contain all 60,000 replicate means and variances, both endpoints; an independent script importing neither producer nor inference code exactly reconstructed all integer rejection/coverage counts and checked Monte Carlo intervals within 1e-12. The data generator itself was not independently reimplemented. No new biological histories were run.

One shell session stopped after its first completed scenario. The remaining scenarios were resumed individually with the previously frozen seeds and no overwriting of completed outputs; any partial duplicate computation does not add independent replicates.

```text
python -m pytest -q tests/test_q3_joint_inference_20261019.py
python -m scripts.validate_q3_joint_oc_20261019 --scenario full_opposed_alt --plan-sha 683520d2551b30a60d208df7de9654e4f8292dcef82b9ee405052a46014883db --out NEW_DIRECTORY
python evidence/verify_joint_statistics.py
```

The conversation bundle contains the frozen plan, code, raw scalar statistics, independent decision audit and test logs. The repository stores code, protocol and compact result. Repository-wide CI is distinct from local verification and may be pending at publication.
