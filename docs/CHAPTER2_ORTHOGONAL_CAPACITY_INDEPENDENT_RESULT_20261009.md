# Chapter 2 — Independent fixed-founder capacity experiment: complete 64-history result (2026-10-09)

**Scientific readout status: `ALL_64_NEW_HISTORIES_2048_SOURCES_172032_FUTURES_AUTHENTICATED`. Frozen primary decision: `inconclusive`.**

## Original production and machine result

- Complete authenticated independent t400 source run: [#37887039116](https://github.com/zuizui0223/izu-core/actions/runs/37887039116), **65/65 jobs successful**, source SHA `c581d20313326b40233b438ca78fa1c55923b14c`.
- Complete future experiment and source-linked full adjudication: [#37887290489](https://github.com/zuizui0223/izu-core/actions/runs/37887290489), **completed/success**, full 64-history production and final all-case audit.
- Exact original result artifact: [`chapter2-orthogonal-64-history-confirmatory-readout-20261009`](https://github.com/zuizui0223/izu-core/actions/runs/37887290489/artifacts/11597083487). The artifact contains `chapter2-orthogonal-full-scientific-readout.json` and the run console text. The original JSON was also copied **byte-for-byte** to [`results/chapter2/orthogonal_capacity_full_readout_20261009.json`](../results/chapter2/orthogonal_capacity_full_readout_20261009.json): original Git blob SHA-1 `9608751564b76f4d3bfb6c32731d46c475294462` (identical on the GitHub branch), raw JSON SHA-256 `e52d92a4586b92ca0aa3e93b560b2d603d63a9e9ee0b7fa61432a5b7f734d69c`. This document is only the human-readable interpretation.
- All **64 independent visitor histories**, **2,048 complete diploid t400 source states**, and **172,032 postshock futures** were admitted. Of the 64 histories, the full set is retained (including extinct sources). The 172,032 future cells are not independent statistical units.
- The new source cohort is **independent** of the historical visitor IDs 37110801–37110864 and 38110901–38110964. The earlier intervention motivated the new primary test; it is not treated as a second confirmatory result.

**Machine JSON status note:** The nested `inference.status = ALGEBRA_ONLY_NOT_AN_ADMITTED_SCIENTIFIC_RESULT` is the unchanged protective label returned by the reusable pure-algebra routine. It does **not** override the top-level `ALL_64_NEW_HISTORIES_2048_SOURCES_172032_FUTURES_AUTHENTICATED` status or the separately documented whole-cohort admission completed before inference. Both labels are preserved verbatim in the byte-identical archive.

## Frozen estimands and final quantitative results

The common assignment contrast is `D = occupancy(A-first) − occupancy(I-first)` at 80 postshock updates, averaging the four mating settings, historical near/far, both nested demographic repeats, future visitor regimes and all seven originally log-weighted ovule budgets.

Within any founder/capacity condition, `tau = D_baseline − D_half_selfed_viable_seed`. This is an engineered, postzygotic seed-retention intervention, not natural genetically mediated selfing or field-calibrated persistence.

| Prespecified contrast | Paired 64-history estimate (occupancy probability) | 95% percentile paired-history bootstrap | Evidence rank |
|---|---:|---:|---|
| **Primary**: `tau(F8/C8) − tau(F8/C48)` | **+0.0018484189** | **[−0.0034583915, +0.0073367698]** | **INCONCLUSIVE (frozen primary)** |
| Secondary: `tau(F8/C48) − tau(Ffull/C48)` | +0.0028008842 | [−0.0016188597, +0.0073274460] | Descriptive; interval spans zero |

Primary sign consistency at the independent-history level: **31 positive**, **33 negative**, 0 exact zeros. Secondary: **34 positive**, **30 negative**.

Frozen primary rule, fixed *before this new cohort*: paired 9,999-draw two-sided percentile bootstrap, seed `2026100943`, minimum absolute meaningful mean `0.005`; claim support only if the interval excludes zero and `|mean| >= 0.005`, practical equivalence only if the entire interval is strictly inside `(−0.005,+0.005)`. **Neither criterion passed** for the primary. This is not statistical evidence of a zero effect, and re-running under new random seeds after seeing the outcome would not be a valid repair.

### Within-regime sensitivity (descriptive)

| Source regime | `tau = D_base − D_half_selfed` | 95% paired-history bootstrap |
|---|---:|---:|
| 8 founders, capacity 8 | +0.0057704299 | [+0.0019028546, +0.0097514827] |
| Same eight founders, capacity 48 | +0.0039220110 | [+0.0001433364, +0.0077797719] |
| All available founders, capacity 48 | +0.0011211268 | [−0.0029149945, +0.0051216373] |

The first within-regime interval excludes zero, consistent with the earlier synthetic finding that severe-bottleneck absolute schedule effects can be sensitive to viable selfed seed retention. The second within-regime interval also excludes zero, although its point estimate is smaller than 0.005. **These marginal intervals do not establish significant differences between regimes**; the directly paired primary and secondary regime contrasts above decide the moderator question.

## What this result does and does not establish

**Supported by direct production:** the newly generated full cohort reproduces positive selfed-seed viability sensitivity in the synthetic F8/C8 regime, conditional on the unchanged frozen evolutionary-expression model. The experiment directly controls seed viability, not the historical natural genetic route to selfing.

**Not established:** there is no confirmatory evidence for a distinct *carrying capacity* moderator after matching the exact same eight diploid t400 founder genotypes (F8/C8 vs F8/C48); the directly paired 95% interval spans zero and the primary decision is inconclusive. At capacity 48, the comparison of the same eight founders with all available founders also spans zero, and the latter contrast bundles starting abundance with genotype subsampling rather than isolating genetic diversity.

**Earlier conclusions remain untouched:** The earlier full-grid near/far interaction was practically equivalent under its own bound; the independent 3/4-budget window confirmation failed. PR #429's initial capacity-8 viable-selfed-seed gate passed its original criterion on the previous source cohort; PR #430's between-regime moderation `+0.009428`, CI `[+0.003605,+0.015347]`, was explicitly post-outcome exploratory and confounded founder number, capacity, and regime-dependent future RNG. This independent orthogonal experiment does **not** validate that exploratory interaction as a pure capacity effect.

A cautious ecological interpretation is that **reproductive-assurance sensitivity of persistence is possible under severe finite-population stress, while the specific demographic mechanism causing between-regime heterogeneity remains unresolved**. This model does not directly demonstrate an Izu Islands field effect, extinction threshold, long-term fitness gain, or genetic mediation.

## Post-outcome mechanistic interpretation correction (2026-10-09)

An additional **read-only, fully source-authenticated** 172,032-future audit was executed successfully in [Run #37890907635](https://github.com/zuizui0223/izu-core/actions/runs/37890907635). This was performed **after** the frozen inconclusive decision; no original history, biological intervention, estimate or uncertainty bound was changed.

The F8/C8 versus F8/C48 comparison matched the exact eight diploid founders and initial abundance, but the canonical pollen-transfer equation also depends **directly on `config.capacity`** through the recipient denominator `affinity.sum(axis=0, keepdims=True) + config.capacity * config.background_ratio` (`scripts/model3_island/reproduction.py`). Consequently, setting the capacity to 8 versus 48 changes both the *demographic ceiling* and the *background dilution of pollen delivery*. The authenticated t0 channel audit finds no initial pollen-export difference between those F8 arms, but the maximum case-level absolute difference in initial viable outcross seed production is **18.925**, and in viable selfed seeds **8.479**. These are maxima, not mean causal effects.

**The registered primary remains `inconclusive`.** It cannot be described as identifying a pure demographic ceiling effect holding effective pollen-sharing conditions fixed. The new cumulative recruitment and early-extinction decompositions are exploratory, survival-duration-dependent descriptions, **not causal mediation**. See [the source-locked mechanism audit](CHAPTER2_ORTHOGONAL_MECHANISM_CHANNEL_AUDIT_20261009.md).

## Integrity and next decision

The two production stages and whole-cohort statistical audit have **completed successfully**; the result should be archived as `inconclusive`, not rerun selectively. Further mechanism resolution would require a *new* independently justified design (e.g. measuring genotype composition and source population abundance separately); it should not retrospectively re-label the 2026-10-09 confirmatory comparison.
