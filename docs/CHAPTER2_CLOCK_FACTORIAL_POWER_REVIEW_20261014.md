# Chapter 2 Q1→Q2 genetic-access pilot — power and identifiability review

**2026-10-14. Source-based, pre-outcome calculation only. NO original Model 3 biological simulation; no registered 1,536-case pilot started; no predictor trained or scientific execution authorized.** This adds a quantitative science-side readiness check to the original, unchanged [phenotype-matched access×homolog pilot design](../data/design/chapter2_clock_factorial_pilot_protocol_20261013.json) and [five-contrast pre-outcome exploratory contract](../data/design/chapter2_clock_factorial_pilot_analysis_contract_20261013.json).

## What n=128 can—and cannot—establish

The frozen pilot is **2 original founder blocks × 64 independently generated stochastic history masters per founder = 128 paired clusters**, each run in **three fixed visitor contexts × four matched factorial treatments = 12 nested arms**. Hence **1,536 trajectories** and **307,200 proposed original Model3 updates** are NOT 1,536 independently randomized biological ecosystems. The two founders and three environments are deliberate fixed conditions, not randomly replicated natural island systems.

The five prespecified exploratory contrasts are: A-allele halfwidth → A 20-census incidence; hidden I-homolog segregation → I decline incidence; each access axis → six-class all-start order score `D = 1[A-first] - 1[I-first]`; and A-width×I-homolog interaction on `D`. All six classes remain counted; single-event, near-simultaneous, extinct, and neither are not silently discarded. No p-value or multiplicity-corrected nominal confidence interval was preregistered for these five exploratory summaries. **These pilot contrasts have their own cluster-level variance, not the as-yet-undefined score-difference variance of a model-based evolutionary clock versus a flexible null.**

For illustration **only**, if a particular contrast's **cluster-mean SD** happened to be σ, a one-direction positive lower endpoint of a normal 95% CI has 80% power at approximately `2.801585×σ/√n`. These are *assumed scenario SDs*, not measured values from the new genotype intervention or even from the original fixed-access cohort. The normal approximation ignores five-outcome multiplicity and bounded/non-Normal distributions, and it is not a valid author-approved five-test significance plan.

| Assumed paired-history contrast SD | Pilot 128-cluster ~80%-sensitivity effect | Within-one-founder 64-cluster ~80%-sensitivity effect | Pilot 128-cluster SE |
|---:|---:|---:|---:|
| 0.10 | 0.0248 | 0.0350 | 0.00884 |
| 0.15 | 0.0371 | 0.0525 | 0.01326 |
| 0.20 | 0.0495 | 0.0700 | 0.01768 |
| 0.30 | 0.0743 | 0.1051 | 0.02652 |
| 0.50 | 0.1238 | 0.1751 | 0.04419 |
| 1.00 | 0.2476 | 0.3502 | 0.08839 |

**Supports of the bounded outcomes matter:** A- or I-incidence paired main contrasts are in [-1,1]; `D` lies in [-1,1], a two-arm-averaged main contrast on `D` can lie in [-2,2] and the two-factor `D` interaction in [-4,4]. A common numeric SD cannot simply be transferred between incidence, order, interaction or predictive Log loss. At the actual finite n, the intended pilot has real value for feasibility, detecting **comparatively large model-specific effects**, describing six-class spectra, and estimating **five factorial-contrast SDs**. It does not automatically have useful precision for every small effect.

## Why 1,536 registered paths do not provide confirmation of the clock

The original source-only heldout comparison (2,304 old histories) reported a t0 full-parent expected I genetic response signal relative to a simple ecological quadratic. A more flexible ecological×genotype null could perform equally or better; neither its superiority nor the two-stage A segregation-access delay function is independently frozen. Therefore the new factorial pilot's outcome-specific paired contrast SD **cannot be used** as the uncertainty for a not-yet-defined six-class predictor's heldout Log-loss improvement. The same source histories must not be recycled as an independent confirmation after tuning the clock on them.

The earlier, unchanged **future** confirmation-planning rule asks if a strictly positive heldout Log-loss reduction of at least **0.02** could be demonstrated with a model-specific paired-history SD, a **0.15 SD floor**, and a minimum 512 / maximum 1,024 independent founder×history clusters rounded to multiples of 128. The conditional normal-approximation sensitivity for a true Log-loss effect = 0.02 is:

| Hypothetical paired Log-loss SD | n=128 pilot *if models were already frozen* | Required future clusters by existing sigma-only rule | Decision conditional on model/reviewer approval |
|---:|---:|---:|---|
| 0.15 | 32.6% | 512 = 6,144 future paths | Further review |
| 0.20 | 20.4% | 896 = 10,752 future paths | Further review |
| 0.225 | 17.0% | 1,024 = 12,288 future paths | Further review |
| 0.25 | 14.6% | 1,280 (over cap) | **NO-GO** under existing ≤1,024 cap |

These numbers **reproduce** the earlier exposed design-only source [power envelope](../data/results/chapter2_clock_power_envelope_20261013.json), including the fixed 512/896/1,024/NO-GO rule. They are conditional assumptions, **not** observed power, not a hypothesis test, and not proof that the future model is already fixed. An independent confirmation protocol must first define both the two-stage genetic response clock and an at-least-equally-flexible ecological/genetic interaction null, calibration, grouped holdouts and the particular model-based cluster score difference. Without those, the pilot cannot yet supply the SD that rule demands.

## Scientific caveats on the genetic intervention itself

* **A width** 0.046875 versus 0.078125 changes diploid allele support as well as potential F1 segregation (`w²/2`): the lower width cannot cross a +0.05 *mutation-free* founder-relative threshold by allele support alone, whereas the upper width can in principle. A-only mutation at 0.01/SD0.05 remains active, so observed threshold accessibility does **not** become a deterministic 0 versus 1 transition. This is not a natural ecological sharp regression discontinuity.
* **I homolog scaling** 0 versus 1 removes within-individual I homolog differences while preserving each individual's expressed I and its between-individual phenotypic variance; it does **not** eliminate standing variation in I across plants. It isolates a particular hidden homolog segregation route, not all genetic accessibility or literal species-level heritability.
* Same original fixed biological model, two founder genotypes and three prespecified visitor contexts: any resulting stochastic six-class changes will be model-conditional, not field-replicated pollinator-driven evolutionary responses or the effect of natural first-event order on Q4 persistence.

## Actual next gate, separate from statistical sensitivity

1. **Technically done:** immutable 1,536 input registry and matching original-genome pedigree/return implementation; short 48×3 original operator writer→reader verification, six-source independent-readback and lossless ZIP packaging technical CI on their draft heads; five-contrast exploratory contract; selected private Drive candidate mirror.
2. **Still needed before pilot dispatch:** an independent scientific source-run reviewer accepts the exact original-code producer, full-census raw output contract, six primary ZIPs and a **separately administered, hash-checked** mirror custody plan, error/partial-run/retry policy and clear exploratory—not confirmatory—claim boundary. Private Drive selected does not alone constitute research deposition, independent custody signoff or DOI.
3. **Only after the independent authorization receipt is actually reviewed and hash-bound** may the currently deliberately disabled `APPROVAL_GIT_BLOB=None` move to an approved execution contract. Do not bypass this guard merely to produce numbers. The original six full ZIPs, separate copies and native readback are currently absent.
4. **After true source admission:** report only the five registered exploratory factorial contrasts and all 24 six-class cells; use the measured cluster variance to characterize uncertainty of *those contrasts*. Decide any future predictor-based confirmation sample size only after the clock and competing null have been mathematically specified and separately preregistered.

**Summary:** The experiment is valuable and appropriately staged as *exploratory*. **The data-science next step is to run it following authorization**, not to infer a new Q2 causal law from a prior t0-only classifier or from the hypothetical σ grid. The confirmatory predictor mechanism, preservation provider and DOI remain distinct tasks.
