# Q1→Q2 initial-response clock: paired-seed exploratory verification

**Date:** 2026-10-13. **Status:** Source-matched retrospective *exploration* in original synthetic Model 3; **not** an independent biological confirmation, causal genetic-clock demonstration, preregistered result or a new manuscript. This follows the strictly source-verified 2,304 history t0 audit and does **not** modify the frozen ecological experiment, manuscript conclusions or model operators.

## Scientific question

Can a quantity available before any ecological update—specifically the original diploid parental reproductive-return response at t0—improve the probabilities assigned to six later genetic response categories compared with ecological exposure and inherited standing variance alone?

This is a **necessary but insufficient bridge** from Q1 to Q2. The source genotype at t0 has equal expressed A=0.5 in every parent, so the t0 *expected selection response of A is exactly zero in every one of the 18 founder/context combinations*. Its potential unmutated F1 Mendelian segregation variance is 0.001953125 in **all** combinations. Consequently the 2,304-case cohort has no independent variation in A accessibility with which to identify an assurance access-delay effect or a genuine two-trait ratio of first-passage times. A t0 one-stage `0.05 / response_A` clock is undefined for all contexts. We do not assign a fabricated A time.

## Admission and independent units

The original 2026-10-13 GitHub biological run `38312090996` consists of nine original provider ZIPs, exactly 256 case archives per ZIP (2 founder genotype blocks × 128 stochastic repeats). The repeated seed index remains paired across all **nine** ecological contexts for each founder. The **original 2,304 NPZ case-byte SHA-256 values and nine provider SHA-256 values** were rechecked against original `_COMPLETION.json` receipts, and all 18 original six-class category counts were independently reconstructed. The compact [256 paired seed strings](../data/results/chapter2_initial_clock_paired_events_20261013.json) retain an exact nine-character original-category code sequence for every `(founder block, replicate)` rather than treating the 2,304 synthetic paths as independent.

This analysis reuses, without mutation, the [18 original t0 full-parent genotype/return profiles](../data/results/chapter2_initial_clock_t0_raw_20261013.json) produced by read-only GitHub job `38337931445`. No new ecological stochastic histories, original source replacements, changed mutation rate, post hoc event thresholds, field observations or automated restarts were created.

## Predictor families, strictly from the original starting state

- `prevalence`: six-class training prevalence only (not an a priori ecological null).
- `ecology`: fixed supply transform, presence, matched-versus-separated visitor composition and its interaction with supply.
- `genetic_access`: original investment allelic-variance proxy only; **A segregation variance is constant**, so this is not an independent estimate of A accessibility.
- `ecology_genetics`: ecological features plus the investment standing-variance proxy.
- `ecology_genetics_quadratic`: ecological plus investment variance and one additional squared-supply feature. This **equal-complexity non-mechanistic control** checks if source-Price predictive improvement is just ecological nonlinearity.
- `ecology_genetics_price`: ecological plus investment variance and the **signed exact t0 investment Price response** evaluated from female-outcross, paternal-outcross and viable-selfed parental genetic returns. This is not `beta` or the A-versus-I trajectory clock itself.

Regularized multinomial likelihood uses all six original labels (`A-first`, `I-first`, near simultaneous, `A-only`, `I-only`, neither), a five-logit reference formulation, per-cell training frequencies and fixed L2 slope penalties `0.025`, `0.15` (main exploratory display) and `0.6` (sensitivity). No model or lambda was prospectively frozen before exposure to the historical outcomes; these are transparent retrospective choices.

**Main held-out split:** five folds by `replicate % 5`. All nine contexts for one founder-specific seed cluster stay in the **same** fold. For every fold, training contains no event label from a held-out stochastic seed. Scaling and coefficient fitting use training only. Predictive metrics evaluate every held-out case (including single-event/nonresponse histories). Held-out predictions are not allowed to depend on the corresponding later states or class labels.

A separate nine-fold *leave-one-ecological-context-out* exploratory comparison, without paired-stream covariance, appears in [the source identifiability companion](CHAPTER2_INITIAL_CLOCK_IDENTIFIABILITY_20261013.md). **Its numerical scores are not the same test as the current paired-seed held-out experiment.**

## Main paired-seed five-fold results

All figures below are from the **original 2,304-case cohort**, in-sample ecology/genetic model family, with unseen **stochastic seeds** but the same 18 synthetic ecological/genetic profiles. Lower proper score is better.

| Original t0 predictor set | Six-class Log loss | Multiclass Brier | Argmax accuracy |
|---|---:|---:|---:|
| Training prevalence | 1.53134 | 0.75513 | 38.85% |
| Ecological descriptors only | 1.37277 | 0.68441 | 42.80% |
| Founder investment variance only | 1.52421 | 0.75108 | 38.85% |
| Ecology + founder investment variance | 1.36468 | 0.68071 | 44.31% |
| Ecology + founder variance + supply squared | 1.33062 | 0.67249 | 44.57% |
| Ecology + founder variance + **t0 full-parent I response** | **1.31875** | **0.66683** | **45.75%** |

The exact fitted-test summary and all nine context results in the complementary **context-held-out** audit are kept separately; all 256 seed-cluster predictions are reconstructed deterministically from original label strings during paired evaluation. Neither the 45.75% model score nor the earlier 48.48% within-cell post hoc oracle is a prospective natural-population prediction accuracy.

### Primary exploratory contrasts (L2=0.15)

- Adding t0 Price response to ecology+genetics improves **Log loss by 0.04593** and Brier by **0.01388**. Holding all nine contexts together in a cluster and resampling 128 founder-specific streams *within each founder* (10,000 draws), the exploratory **conditional-on-fitted-predictions** Log loss difference has percentile interval **[0.04228, 0.04913]**.
- Crucially, a **matched-complexity ecological curvature control** already improves Log loss from 1.36468 to 1.33062. The extra improvement of the t0 Price model over this squared-supply baseline is therefore just **0.01187**, with conditional paired-stream percentile interval **[0.00850, 0.01524]**. The Brier improvement over this curvature control is **0.00566**.
- Positive incremental Log loss scores occur for all three fixed L2 sensitivities against ecology+variance: **0.04461, 0.04593, 0.03352**. Against the equal-complexity quadratic control, the corresponding *smaller* improvements are **0.00697, 0.01187, 0.00627**.

**Interpretation ceiling:** Under existing Model 3 conditions, the original t0 expected inherited investment response contains additional *predictive information* after certain low-dimensional ecological/genetic summaries. Some of the original apparent uplift is explained by nonlinear ecological exposure, and further correctly chosen ecological functional forms could absorb additional differences. The recorded conditional intervals reflect variability across the preserved stochastic seeds under already-fitted exploratory models. They are **not** model-selection-adjusted, parameter-refitting uncertainty, independent ecological replication, causal mediation, or a preregistered confirmation of Q1→Q2.

## Scientific boundary and next hard gate

This exploratory result does **not** demonstrate that a complete two-stage access-then-selection clock predicts A-versus-I sequence. In the original experiment, A founding expressed variance=0, all A parents are equally heterozygous, and its Mendelian segregation potential is shared across all contexts. There are just two original investment-founder states and nine ecological conditions; no independently replicated variation in the *A genetic-access delay* exists. Signed t0 I expected response predicts later I-event incidence better than a no-exposure category-only description, but whether A or I crosses first also depends on post-t0 segregation, inheritance, mutation, finite sampling, fixation, threshold/censoring and dynamic pollen feedback.

The next *new independent* biological campaign would need **before execution**: (i) multiple prospectively chosen assurance accessibility widths and I standing-variance states, (ii) the same native Model 3 source and all six categories, (iii) a true F1-access mechanism and **outcome-blind** predicted A response time as well as I, (iv) a paired-profile/seed-level pilot-informed power calculation including model refit and response non-crossing, and (v) preregistered independent seeds and one primary proper-score comparison with a full ecological curvature control. The same archived 2,304 outcomes cannot provide independent confirmation. Do not use its narrow exploratory conditional bootstrap interval to assert the required new sample size or a biological critical transition. Q3 mutation-supply robustness and Q4 state-mediated persistence remain separate, unclaimed future questions.

## Code / original source

- [Original SHA-preserving event extractor](../scripts/audit_chapter2_initial_clock_paired_events_20261013.py).
- [t0/context transfer pilot model](../scripts/audit_chapter2_initial_clock_transfer_20261013.py).
- [paired seed-group five-fold and bootstrap auditor](../scripts/audit_chapter2_initial_clock_paired_cv_20261013.py).
- [Paired event readout](../data/results/chapter2_initial_clock_paired_events_20261013.json) and [complete paired CV result](../data/results/chapter2_initial_clock_paired_cv_20261013.json).
- Original frozen biological execution source `328548612e93469fcc8663f24548530a57399b9a`; original compact source Git blob `5608ad2cdcbef167fe9062ab5f26318abf2e1bd9`.

This is an exploratory companion to [PR #494](https://github.com/zuizui0223/izu-core/pull/494), itself stacked on the unmerged four-question submission [PR #491](https://github.com/zuizui0223/izu-core/pull/491). Publication/DOI status does not change.

## Stronger same-condition null: fully known-context lookup (post hoc negative benchmark)

A further **source-matched retrospective check** asks whether the t0 Price model is actually the best forecaster *within these exact 18 already-known founder × visitor profiles*. Using the same 256 paired biological random-stream clusters and the identical held-out `replicate % 5` folds, an **18-cell empirical category-frequency lookup** is estimated from the other four seed folds. To avoid zero probabilities in rare labels, add `alpha=0.5` (Jeffreys pseudocount for each of six labels) to each cell/category frequency. The six possible outcomes and all original starts remain in the loss denominator.

| Model / 5-fold seed-heldout | Six-class Log loss | Brier | Argmax accuracy |
|---|---:|---:|---:|
| Existing ecology+I-genetic variance+t0 I response | 1.31875 | 0.66683 | 45.75% |
| **Known-profile 18-cell empirical lookup**, α=0.5 | **1.13993** | **0.62074** | **47.22%** |

Lookup pseudocount sensitivity `alpha={0.01,0.5,1,2}` gives Log loss `1.14740 / 1.13993 / 1.14676 / 1.16315`. These are **post-exposure checks**; alpha is not an independently frozen biological optimum. The lookup uses many more effective parameters (six-category probabilities independently estimated in each of 18 named original cells). Crucially, it **cannot predict a genuinely new founder/environment condition** because its cell label is absent from training. Consequently this is **not an equal-complexity falsification** of the process model or a competing general ecological mechanism.

It does impose an important ceiling on the claims: within these exact repeatedly sampled contexts, empirical conditional frequencies capture more of the stochastic outcome distribution than the present coarse mechanistic features. The source response feature's small advantage over a flexible ecological covariate is an exploratory **low-dimensional interpolation** result; a model with an A-access delay or reliable unseen-condition prediction has not yet been demonstrated.

Machine-readable same-history check: [`chapter2_initial_clock_saturated_reference_20261013.json`](../data/results/chapter2_initial_clock_saturated_reference_20261013.json); source-bound reader: [`audit_chapter2_initial_clock_saturated_reference_20261013.py`](../scripts/audit_chapter2_initial_clock_saturated_reference_20261013.py). Execute with the original exact PR491 ecological compact JSON and PR494 paired event JSON; their Git blob identities are pinned, and the test rejects lost/changed original histories. This is read-only: **zero new biological cases**.
