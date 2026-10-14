# Chapter 2 assigned-expression-order cohort: completed production readout

**Result lock: 2026-10-09 JST.** This is a **post-outcome factual report**, NOT an amendment of the preregistered intervention, estimand, exclusion rules, effect threshold, or hypotheses.

## Traceable execution

- Design / operational authorization: merged PR [#416](https://github.com/zuizui0223/izu-core/pull/416), building on merged PR #415.
- Frozen production source: `6d9a2686359a2be131370d48300f9165c72844ce`.
- GitHub Actions full-cohort run: [37856410822](https://github.com/zuizui0223/izu-core/actions/runs/37856410822), `conclusion: success`.
- Audited final JSON: [order-expression-complete-audited-readout, artifact 11583968991](https://github.com/zuizui0223/izu-core/actions/runs/37856410822/artifacts/11583968991), ZIP SHA-256 `62fca337d142b78a17d50ffd2c0599574cd1c7c6d2bdd7055022a9f3b89e278e`.
- Protocol SHA-256: `b6f6336875b04a131434ef35d6ec42b59dc14a1e4c59e7e4d6f2513e24a04fdd`.
- GitHub Actions jobs: preflight 1/1, prehistory 64/64, postshock 64/64, final-readout 1/1 **successful**, none failed.
- Admission: **64 independent visitor histories**, **3,072 source populations**, **86,016 future branches** were validated in the final readout. Two demographic replicates are nested within history, not 86,016 independent units.
- Old-history-only engineering preflight was separately completed before launching full cohort. The ad hoc launcher was removed afterward. The external GitHub Actions artifact has a finite retention interval; do not replace the source artifact with this synopsis.

## Preregistered primary result

The primary outcome is log-budget-weighted terminal occupancy over seven ovule budgets, both future visitor environments and two nested demographic repetitions, under the **eight founders / capacity eight** future stress regime. The primary contrast is the visitor-history-weighted difference in differences:

```
Delta = [survival(A-first, far) - survival(I-first, far)]
      - [survival(A-first, near) - survival(I-first, near)]
```

The four mating settings are equally pooled **within each** of 64 independent histories. Inference uses **9,999 shared-index history-level bootstrap draws**, preregistered seed `3711082026`. The two-sided decision rule was frozen: evidence of a biologically relevant effect needs a 95% bootstrap interval excluding zero **and** an absolute mean of at least **0.05**. An entire 95% interval inside `(-0.05, 0.05)` is declared practically equivalent within that region; otherwise inconclusive.

| Outcome | Value |
|---|---:|
| Primary pooled DID | **−0.013589137072344082** |
| History-bootstrap 95% interval | **[−0.022811888595303833, −0.004302445152193567]** |
| Frozen categorical decision | **`equivalent_within_predeclared_ROPE`** |

**Interpretation:** the uncertainty interval excludes exact zero but lies fully within the preregistered ±0.05 practical-equivalence region. Thus the effect is directionally detectable but **too small to pass the declared biological-effect gate**. It would be incorrect to report either “zero order effect” or “strong survival rescue”; the predefined result is **practical equivalence of the pooled far–near assigned-schedule interaction under this synthetic primary stress**.

This is an **assigned transient expression-schedule effect**, not a causal effect of naturally realized inherited trait order. The time of actual inherited genetic threshold crossing is post-treatment and was **not** used to filter the intention-to-treat estimand.

## Required mating-setting decomposition

### Primary: eight founders / capacity eight

| Mating setting | History-level DID mean | Bootstrap 95% | A-first minus I-first, near | A-first minus I-first, far |
|---|---:|---|---:|---:|
| delayed_control | −0.008121 | [−0.027884, +0.012330] | +0.008279 | +0.000157 |
| prior_selfing | −0.012234 | [−0.030509, +0.005910] | +0.017579 | +0.005346 |
| pollen_discount | **−0.029273** | **[−0.047495, −0.010921]** | **+0.027911** | **−0.001362** |
| assurance_cost | −0.004729 | [−0.018970, +0.009485] | +0.007890 | +0.003161 |

The `pollen_discount` subgroup interval excludes zero. However, this is a **secondary setting-specific decomposition**, not a replacement for the prespecified pooled main gate; multiple-setting interpretation was not promoted to a newly defined confirmatory discovery. Its negative DID is largely associated with the positive **near** contrast, **not a far-environment survival rescue**.

### Mandatory comparator: no founder bottleneck / capacity 48

| Mating setting | History-level DID mean | Bootstrap 95% |
|---|---:|---|
| delayed_control | +0.001874 | [−0.014851, +0.018994] |
| prior_selfing | −0.010411 | [−0.022305, +0.001631] |
| pollen_discount | −0.005623 | [−0.018070, +0.007037] |
| assurance_cost | −0.008635 | [−0.020562, +0.003034] |

Pooled no-bottleneck DID: **−0.005698632796652152**, versus **−0.013589137072344082** in the primary eight-founder bottleneck. No pooled interval for the no-bottleneck contrast was supplied in the frozen readout. This is **descriptive scenario-dependence**, not independently tested mediation by demography.

## Mandatory budget × future-visitor sensitivity (descriptive, not a substitute main gate)

The JSON enumerates seven ovule budgets × two future environments for each stress regime (**14 cells per regime**). On this grid:

- Primary eight-founder/capacity-eight: **6 negative, 3 positive, 5 zero** cell-level pooled DIDs; range **−0.07421875** to **+0.00390625**.
- No-bottleneck/capacity-48: **5 negative, 3 positive, 6 zero**; range **−0.05078125** to **+0.009765625**.
- The largest negative primary individual cell occurs at budget **3.0, future visitor 'near'** (−0.07421875), followed by budget 3.0/far (−0.0546875). Primary budget 4.0 is also negative (near −0.052734375; far −0.046875). These are **descriptive post-readout cells without separately defined confidence intervals or multiplicity-adjusted tests**.
- Therefore do **not** generalize pooled practical equivalence to every budget, future environment or reproductive setting. Nor infer a budget-specific biological threshold from the observed grid without independent confirmation.

## Scientific boundary and following research decision

1. **Supported by this finished experiment:** under the preregistered pooling, the assigned A-first versus I-first *far–near* survival interaction is **practically equivalent within ±0.05**, even though its interval lies below zero.
2. **Secondary observation:** a negative setting-specific contrast is detectable for `pollen_discount` under the eight-founder synthetic stress, and the magnitude varies with demographic scenario and ovule budget. These observations are exploratory as mechanism claims.
3. **Not supported:** a broad “A-first rescues remote populations” law; a general natural-island extinction rate; a causal effect of spontaneously realized genetic order; or genotype-mediated rescue. The earlier **failed independent16 mutational-priority confirmation** retains its failed evidential status.
4. **Next scientific question (separate preregistration):** why does `pollen_discount` show a larger *near*-environment A-first advantage, and whether any setting- or budget-specific mechanism survives an **independent new visitor-history cohort** with a prespecified contrast and an explicit multiplicity plan. Do not mine/relabel the current same histories as independent confirmation.
5. **Retention:** archive the raw signed final receipt and constituent sources externally if long-term reproducibility beyond GitHub Actions artifact retention is required. This document is an indexed readout, not a replacement for the byte-level raw files.

**Source of truth:** the sealed `order_itt_readout.json` and its SHA-verified upstream cohort artifacts in the GitHub Actions run linked above. All numerical statements in this file are extracted or arithmetically derived from that output; no new prospective data, simulations, genetic-order causal analyses, or re-estimation of the primary effect were performed in preparing this report.
