# Initial response clock: ecological-context × seed-history double holdout

**2026-10-13. Exploratory retrospective test of the already admitted ecological-order cohort, not prospective confirmation, a historical mutation-order reconstruction, or a natural island study.** This analysis is supplemental to [the original seed-paired test](CHAPTER2_INITIAL_CLOCK_PAIRED_SEED_RESULTS_20261013.md) on draft PR #494, stacked on the unfinished four-question PR #491. No original Model 3 biological rule, frozen event definition, original genotype, manuscript headline, or stochastic case was changed.

## Question and proper separation

**Question:** Does original t0 *full parentage* expected inherited investment response (maternal outcross + paternal export + viable selfing) add predictive information to six distinct evolutionary outcomes, even when **both** stochastic visitor-history cluster and the evaluated ecological context are excluded from training?

This is a stricter retrospective check than either:

- the *seed-blocked only* analysis, where the tested ecological context remains in training through other histories, or
- the *context-held-out only* analysis, where tested stochastic streams have analogues in the remaining contexts.

Its extra ecological criterion still tests interpolation/extrapolation *within the same model family and nine exposed functional-environment designs*, not transfer to an independent ecosystem or new founder genotype.

## Source/inference unit

The original [ecological readout](../data/results/ecological_order_boundary_20261013.json) and original-source t0 F/P/S [feature audit](../data/results/chapter2_initial_clock_t0_raw_20261013.json) were checked against the preserved 9 original provider ZIPs. Their [all-start category strings](../data/results/chapter2_initial_clock_paired_events_20261013.json) preserve **2 founders × 128 random-stream clusters × 9 ecological contexts = 2,304 original cases**. Every one of six categories (A-first, I-first, tie, A-only, I-only, neither) remains an outcome; no restriction to the 770 both-event strict-order histories.

For each of 9 ecological contexts *c* and each of five fixed seed folds *f* (`replicate % 5 == f`):

1. Train on the **eight other ecological contexts** and only the **four other random-stream folds**. Training contains **no outcome from held-out context c and no label from a held-out seed cluster at any ecological context**. Both founder states remain in training but no individual genotype within a founder is new.
2. Fit the exact same multinomial regularization method used in the original audit, with fixed L2 slope penalties **0.025, 0.15 and 0.6**. Centre/scale predictors using training contexts only. Equalize the training weight of 16 founder×context rows. Models use no outcomes, realised genotypes after t0, per-seed labels or replicate IDs as features.
3. Predict all held-out `(founder,replicate,c)` cases, retaining every case exactly once over **45 nested fits per model**. Evaluate log loss and multiclass Brier as proper scores, argmax accuracy as secondary, and model differences by paired 256-history clusters.
4. Bootstrap (10,000 resamples) within founder, retaining all nine contexts per stochastic seed, **conditional on the already-fitted exploratory predictions**. This does *not* refit predictive models within resamples, does not create independent ecological replicates and is not a confirmatory confidence interval or significance test.

## Competing source-t0 feature sets

All models include only initial ecological/genic descriptors. The original models are prior prevalence, ecology (`log1p(16*supply)`, nonempty indicator, separated visitor composition and its interaction), investment founding allele variance alone, their combination, plus one squared supply term, or plus the **t0 expected full-parent I response** instead of that squared term. The exact price response is not a `beta` invasion gradient or an A-to-I passage-time ratio.

**Additional deliberately adverse post-outcome nulls**, not an already frozen causal comparison, add (a) separately curved supply for matched/separated groups, (b) investment genetic variance × log supply, (c) variance × separated composition, and (d) combined supply-curvature + genotype × supply. These models can have **more degrees of freedom** than the one-extra-Price-response model. They test whether the apparent mechanism signal is reproducible by flexible ecological/genetic interactions rather than uniquely attributable to full-parent selection.

## Verified numerical result (same original cohort; main displayed L2=0.15)

| t0 predictor | Double-heldout six-class Log loss ↓ | Multiclass Brier ↓ | Accuracy |
|---|---:|---:|---:|
| Training prevalence only | 1.63933 | 0.79027 | 38.85% |
| Ecology | 1.48617 | 0.71989 | 41.58% |
| Ecology + initial I genetic variance | 1.47931 | 0.71664 | 42.36% |
| Ecology + I variance + one ecological quadratic term | 1.44390 | 0.71117 | 44.36% |
| Ecology + I variance + **t0 full-parent expected I response** | **1.42169** | **0.70107** | **44.62%** |
| Ecology + I variance + **two ecological curvatures and variance×supply** (flexible adverse null) | **1.41659** | 0.70307 | 44.44% |

- Price response versus ecology+I variance improves Log loss by **+0.05762**; versus the **same-complexity one-quadratic term** the improvement is **+0.02221**. The latter is positive in 7/9 contexts, negative in contexts 3 and 8. The *fixed fitted-model* 256-cluster percentile interval for the matched-complexity reduction is recorded in the machine result; it is **not** a source of general ecological precision.
- Price response **does not beat the flexible post-hoc ecological/genetic null in Log loss** at central L2=0.15: the reduction is **−0.00510**, with descriptive paired-seed conditional interval **[−0.00956, −0.00058]**. Its Brier remains slightly lower, so the conclusion depends on which proper score is targeted.
- Across L2 settings `(0.025,0.15,0.6)`, Price-vs-same-complexity-quadratic Log-loss reductions are **(+0.02485,+0.02221,+0.00742)**; Price-vs-flexible-null reductions are **(+0.00047,−0.00510,−0.01885)**. Thus the exact t0 Price feature improves parsimonious six-class predictors but **does not establish unique or robust superiority over richer nonmechanistic descriptions**.
- Unlike the previous known-profile saturated frequency lookup (seed-only heldout Log loss **1.13993**), this two-axis comparison actually excludes the entire tested ecological context, so **the saturated 18-cell lookup cannot be evaluated as a valid unseen-context model**. Do not compare its 1.13993 as if it were a two-axis score.

## Scientific decision: hypothesis still open

**Supported as a bounded exploratory numerical finding:** the early full-parent investment return carries useful predictive information about later investment/reproductive-response categories in this one synthetic model. The result withstands excluding the tested seed AND ecological context, but flexible ecology/genetic interactions can equal or outperform the exact Price feature.

**Not established:** an autonomous genetic-access delay clock for assurance, an A versus I first-passage equation, identification of a natural two-threshold ecological boundary, independent biological-generalization, causal order selection, or any Q4 order-mediated persistence benefit. Original A expressed genetic variance and expected t0 selection response are **exactly zero across all 18 conditions**, and potential segregation variance is the same in all contexts. With no manipulation of assurance accessibility across independent founders, a two-stage A-clock is **not identifiable** from this cohort. Choosing a favorable subset of contexts, changing the event threshold or calling fitted-model bootstrap intervals independent confirmation would violate frozen boundaries.

## Next discriminating experiment, **design only**

Before a *new* stochastic source campaign, define and independently review multiple A-width genetic-access states and noncollinear I founding-variance states, a true t0→F1 genotype-potential rule, and an outcome-blind six-class distributional prediction. Predeclare an equal-or-greater-flexibility ecological interaction null, **one** proper-score primary, minimal worthwhile improvement, all-start failure criteria, response censoring, genotype fixation and pre-execution power from a separately labelled pilot. Distinct new visitor-history seeds and source identities are mandatory. No new biological histories are executed by this audit.

## Reproduce and scope

- Audit code: [`audit_chapter2_initial_clock_two_axis_cv_20261013.py`](../scripts/audit_chapter2_initial_clock_two_axis_cv_20261013.py).
- Machine-readable full 9-context/3-penalty result: [`chapter2_initial_clock_two_axis_cv_20261013.json`](../data/results/chapter2_initial_clock_two_axis_cv_20261013.json).
- Original nine provider SHA identities, paired original categories and existing source-aware read-only workflow are unchanged; current PR adds a numerical reproduction gate and no stochastic producer invocation.