# Response-regime reappraisal and additional controls — 2026-09-25

Status: completed additional model-conditional controls; not a replacement of frozen results or a new evolutionary model.

## Decision

The mixed-response argument is logically distinct from C/I/S rank transitions. Cached arrays and additional controls support retaining that question in Chapter 2. A reproductive/genetic model remains a separate proposed model class, not a required replacement or a claimed completed result. Neither the old model nor the new controls calibrate natural regional evolution.

## Cached factorial reconstruction

All 30 NPZ files, 270 rows and 360 paired contrasts passed the existing artifact validator (maximum reconstructed statistic error 0). Counts below use the archived numerical sign tolerance 1e-9 in service units. These are alternative initial states under a history pair, not observed plants sharing a population. Values are six-community-seed median [min, max], out of 96 histories.

| Rule | k=1 mixed | k=16 mixed |
|---|---:|---:|
| fixed | 70 [66, 76] | 56 [50, 62] |
| t0_best_d0 | 25.5 [21, 30] | 22 [15, 25] |
| t0_best_d1 | 32.5 [28, 43] | 22.5 [17, 25] |
| t0_centroid_d0 | 14.5 [10, 18] | 1 [0, 2] |
| t0_centroid_d1 | 36.5 [27, 41] | 3.5 [2, 6] |
| t1_best_d0 | 45.5 [43, 59] | 32.5 [26, 36] |
| t1_best_d1 | 46.5 [45, 61] | 31.5 [25, 35] |
| t1_centroid_d0 | 49 [45, 62] | 37.5 [33, 47] |
| t1_centroid_d1 | 50.5 [45, 62] | 39 [37, 49] |

At k=1, all nine rules retain mixed signs in all six community seeds. This is robustness across the tested operators, not all possible biological responses. At k=16, continuous undamped centroid tracking has 0–2 mixed histories; one seed has none. A relative C share near 90% therefore does not itself establish absence of mixed responses.

## Prospective rule-by-control extension

Before new control execution, data/design/chapter2_response_regime_controls_20260925.json fixed all nine rules, seed lists, 96 histories, 21 starts, 120 steps, existing matching algorithm, metrics and source hashes. The prior cached results were already known and this is explicitly a targeted follow-up. Twelve batches produced 108 control/rule/seed rows; complete three-layer endpoints and per-step counts are saved.

Richness matching uses six subsampling seeds on the SAME community ensemble (master seed 20260826); these are not six independent community ensembles. Each uses 11,520 snapshot pairs, hence 69,120 matching checks with zero mismatches. Turnover equality uses six independent community master seeds and keeps other scenario differences. All 108 summary rows were independently reconstructed from NPZ signs and NumPy SS, maximum fraction error 1.11e-16. Original scalar endpoints matched exactly on 63 checked cells.

| Rule | Matched mixed range /96 | Matched I range | Equal-turnover mixed range /96 | Equal-turnover all-negative range /96 |
|---|---:|---:|---:|---:|
| fixed | 73–88 | 0.6430–0.7152 | 69–80 | 0–0 |
| t0_best_d0 | 21–36 | 0.0795–0.1618 | 44–56 | 0–0 |
| t0_best_d1 | 43–51 | 0.2198–0.3725 | 50–57 | 0–0 |
| t0_centroid_d0 | 13–21 | 0.0311–0.0729 | 9–17 | 1–8 |
| t0_centroid_d1 | 39–46 | 0.1781–0.3185 | 24–36 | 0–1 |
| t1_best_d0 | 55–64 | 0.2848–0.4364 | 67–74 | 0–0 |
| t1_best_d1 | 56–70 | 0.3289–0.4824 | 66–73 | 0–0 |
| t1_centroid_d0 | 52–65 | 0.2828–0.4287 | 72–79 | 0–0 |
| t1_centroid_d1 | 56–71 | 0.3258–0.4805 | 72–80 | 0–1 |

Every matched rule/seed has all-positive starting-state mean geometry and nonzero mixed-history counts. The original-rule range 55–64 and I range 0.2848–0.4364 reproduce the archived RNG-corrected summary. Matching does not eliminate mixed individual responses under any tested rule. The amplitude and frequency remain rule-dependent.

## Corrections that materially affect interpretation

1. **No demonstrated universal mean flip.** For the exact matched community ensemble, the unmatched original-rule baseline already has all-positive mean geometry (grand mean 0.0837834). Across the six independent baseline community seeds, two are all-positive mean geometry and four mixed; all six grand means are positive. Thus this comparison cannot be described as six independent mean-sign reversals. Distinguish a grand mean, 21 conditional starting-state means, and 96 within-history sign classifications.

2. **Matching is not a uniquely identified species-number mechanism.** Response-blind subsampling removes count differences, but also changes which functional types remain, emptiness on the richer side and the sequence experienced by plants. It supports persistence under this declared count-matching intervention, not a proof that means are exclusively caused by richness and branching exclusively by another separable mechanism.

3. **Turnover equality does not remove all negative responses.** Under the original rule, all-negative histories disappear in all six newly audited community seeds (mixed 67–74/96), but mixed histories still include negative cells. Under continuous undamped centroid tracking, 1–8/96 histories remain all-negative despite equal turnover. Hence the broad claim that negative branches require turnover asymmetry fails across operators. The historic 41→70 and 13→0 figures came from the old single-seed artifact, not the updated six-seed result.

4. **Finite-community necessity is scoped.** The existing all-positive deterministic mean-field result is for the zero-trait-adjustment submodel. It is not a verified mean-field result for every dynamic rule. Finite k=16 still has many mixed histories for several rules; finite pooling is not the exact infinite limit.

5. **42 systems and 0/25 keep their original estimands.** Forty-two interaction systems from six sources occupy observed breadth–synchrony space; they are not 42 independent islands assigned to empirically verified response regimes. The 0/25 count concerns complete outcome-independent determinant–response contracts, not absence of variance reporting.

6. **Operator effects are not identified natural plasticity or selection.** A best-target versus centroid comparison is a legitimate model intervention. It does not show that real plants belong to those categories. Initial-terminal slopes and S are separate diagnostics; fixed traits can retain perfect memory while S remains small.

7. **Model 3 does not have a predetermined S result.** A fitness gradient need not point at a fixed weighted centroid. Multiple optima, genetic constraints, costs and finite time can preserve starting-state dependence. Predeclare reduced S as one directional hypothesis under specified smooth single-optimum conditions, alongside alternatives, rather than freeze disappearance as an expected fact. No model-3 run has been performed.

## Chapter 2 recommendation

Retain Chapter 2 as a bounded response-regime study: a community change can yield uniformly positive conditional means while retaining opposing responses among starting states in individual histories; response rules modify the frequency and variance structure of that contingency. Use the new rule-by-control extension as evidence, preserve the original failed mean-geometry gate, and do not require the original rank sequence. Do not replace or erase the frozen model. A third reproductive/genetic model would test extension to biologically derived reproduction/inheritance, but need not block the current bounded claim.

Q1 contributes observed regional floral combinations, not measurements of the simulated service contrast. Present a testable connection through flower–visitor functional match and reproductive outcomes. Mean-only summaries can miss modeled sign heterogeneity; inconsistent empirical support alone is not proof of this mechanism, and measurement error, sampling power, filtering and evolution remain alternatives.

Novelty should be the specific operational intervention-conditioned response distribution and its controls, not discovery that island responses differ or that trait distributions matter. Closest prior work is documented in [the focused novelty audit](CHAPTER2_RESPONSE_REGIME_NOVELTY_20260925.md), including floral context dependence, multiple island syndromes and richness-controlled trait-space analyses.

## Files

- Design: data/design/chapter2_response_regime_controls_20260925.json
- Runner: scripts/audit_chapter2_response_regime_controls.py
- Endpoints, rows and receipt: data/results/response_regime_controls_20260925/
- No old source locks, model equations or old result files were changed.
