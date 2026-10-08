# Why mutational priority did not consistently change island persistence (2026-10-08)

**Status:** retrospective mechanistic audit, not a confirmatory result. The source of truth for the frozen independent16 test is `data/results/chapter2_island_mutational_priority_independent16_20261008.json`: its predeclared prior-selfing minus pollen-discount gate **FAILED** (mean −0.08594, 95% history bootstrap [−0.27344, +0.09375]). The distinct balanced mutation-duration experiment is exploratory and its four-setting pooled mean is **zero**. Neither failure is reclassified here.

## New question: did the mutation-access intervention actually change realized order?

The archived source code records for each finite plant population the **first reproductive generation at which population-mean assurance A or floral investment I differs from founder value 0.5 by at least 0.05**. This is a finite threshold for observed change, not the onset of selection.

The complete raw groups were independently re-read from the previously archived offline ZIPs and classified as `A_before_I`, `I_before_A`, `A_only`, `I_only`, `tie` or `neither`. A group with just the intended trait crossing is reported separately and included in the descriptive intended-first tally.

| Experimental cohort | Early access | Intended trait first or only | Historical groups |
|---|---|---:|---:|
| Independent 16-history | assurance first | 118 | 128 |
| Independent 16-history | investment first | 97 | 128 |
| Balanced-duration 4-history | assurance first | 52 | 64 |
| Balanced-duration 4-history | investment first | 51 | 64 |

The archived raw observations support **manipulation compliance**: the intervention usually changed the realized threshold order, even though it does not force it in every finite stochastic population. Historical groups within a visitor seed are *not independent history replicates*: independent visitor n was 16 and 4, respectively.

## Why compliance is not enough for demographic rescue

The within-visitor-history matched difference **(assurance-first − investment-first) of the far-history minus near-history contrast**, averaged over the entire predefined post-stress grid, was:

| Reproductive mechanism | I/A final phenotype difference (A / I) | Immediate viable maternal difference | 80-update occupancy difference |
|---|---:|---:|---:|
| Delayed control | +0.0276 / +0.0559 | +0.0218 | −0.0234 |
| Prior selfing | +0.0364 / +0.0486 | +0.0459 | −0.0469 |
| Pollen discount | +0.0553 / +0.0543 | +0.1246 | +0.0391 |
| Assurance cost | +0.0273 / +0.0068 | −0.0108 | 0.0000 |

The values above are **post-outcome explanatory** means from the independent16 cohort, not evidence that the frozen cross-setting sign test passed. In particular, the prior-selfing case shows a positive immediate viable maternal-output interaction but a negative 80-update occupancy interaction. This is a direct warning against treating per-capita female fitness proxies as persistence, or reading a viable-output effect as a genetic mediation fraction. Pollen export, recruitment variance, the sequence of random parental contributions and finite demographic risk can all separate instantaneous expected payoff from survival.

In the balanced-duration four-history cohort, mean order-by-history occupancy interactions were delayed +0.0156, prior +0.0313, pollen discount +0.0469 and costly −0.0938: **pooled zero**, not a universal direction. Despite exactly 250 mutation-supply updates for A and I in every schedule, the timing of variants entering selection still differs. This is still not a clean intervention on observed trait-change order.

## What the island question actually gains

The strong prospectively confirmed four-setting Chapter 2 result from merged PR #411 remains a different statement: evolving assurance narrows floral-investment divergence even though assurance evolution is unnecessary for low-replenishment decline, with the attenuation mostly caused by stronger high-replenishment investment decrease.

PR #413 adds a conditional pathway from past pollination regimes through inherited states to payoff differences and, in a pilot-informed synthetic demographic stress range, later relative persistence. But changing *mutational priority* within a bounded model does not produce a reproducible universal persistence direction. Therefore:

> Ecological payoff determines selection; mutation, inheritance and finite demographic histories determine which evolutionary responses become realized. Realized order is not, by itself, a stable scalar predictor of subsequent persistence across reproductive mechanisms.

The last sentence is a **bounded inference**, not a claim about all selfing syndromes or natural islands.

## Next causal study to justify

Prioritize intervention on **realized inherited states at the t400 switch** (equalize A while preserving I and matching, and vice versa), on a set of historically paired populations. Then quantify expected viable maternal output, realized pollen transfer and population persistence under the exact same post environment. The intervention must preserve the physical distinction between allele clamping, trait expression and population means; if clamping genetic values destroys variance, report the induced genetic-variation change rather than interpreting everything as mediation. Hold the full stress grid and inferential unit fixed before generating new histories.

A further hypothesis about colonization filters vs in-situ evolution needs a separate arrival/establishment experiment. The current model is still synthetic visitor *replenishment*, not calibrated island kilometres, area, wind pollination, field genetics or natural extinction times.

## Provenance

- Audited raw ZIPs: `izu_core_mutational_priority_independent16_20261008.zip` (SHA256 `28b03fc0ea5a20e8f5bd9b2b9e54ae8e3873f3fca9c8af5bae40d40099d57a28`); `izu_core_mutational_priority_balanced_20261008.zip` (SHA256 `758830ecdcd168a49d733037f4d985d98a2dda4b1bf38625e257774d98988a7e`).
- Exact tabulation: `data/results/chapter2_island_mutational_order_realization_audit_20261008.json`.
- Runnable raw case validator: `scripts/audit_chapter2_island_mutational_order_realization.py`.
- No merged manuscript claim or field validation is amended.
