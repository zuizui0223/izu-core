# Chapter 2 next discriminating experiment: two-axis initial genetic access (design only)

**2026-10-13 — Prospective preparation, not an executed Model 3 biological experiment or a new ecological finding.** This plan is downstream of the retrospective initial-clock PR #494 and the source-identity repair PR #495. Neither of those exposed cohorts proves a two-stage first-passage clock. The current four-setting assurance-compression result remains the paper headline. This proposal cannot alter frozen historical results or promote the exploratory clock to the one active manuscript.

## 1. Current question, and why the prior cohort cannot answer it

The earlier 2,304 trajectories had exactly 18 distinct founding genotype-by-visitor contexts. All founders expressed assurance A=0.5, all A loci were heterozygotes (.4375,.5625), and the initial expected genetic response of A was zero. The F1 **potential** segregational variance was constant at 0.001953125. A t0 Price response for investment I improved a relatively simple six-category predictor, but a more flexible ecological/genetic interaction null achieved lower log loss (1.41659 versus 1.42169 under double history-and-context holdout). Separately, 299 of 335 assurance-first paths had an earlier *on-path* expected I-decline response onset; onset order alone is not the realized threshold-crossing order.

Therefore, the missing scientific question is **whether independently varying inherited A availability and I standing variance produces a predictable change in the joint distribution of six threshold-crossing outcomes**, beyond a flexible nonmechanistic description. This is a conditional model falsification question, not an evolutionary order → persistence study.

## 2. Source-verified two-by-two initial-factor design

The immutably preserved shard-0 ZIP (48 original first-census diploid genotype states per founder) passed source SHA-256 verification. The audit made **eight genotype configurations** without executing Model 3 reproduction, inheritance or population update.

| Initial axis | Low | High | Held fixed |
|---|---:|---:|---|
| A allele half-width `w` | 0.046875 | 0.078125 | All adults have the same expressed A=0.5; each is heterozygous (.5-w,.5+w) |
| I allele-deviation multiplier `c` | 0.5 | 1 | Original founder-wide allele mean I, original M allele values, original population size |

I is transformed **allele-copy by allele-copy**: `I_new = I_founder_mean + c*(I_old - I_founder_mean)`. Its allele-variance proxy and expressed adult variance consequently change by factor `c²` while means are unchanged. Both scales retain an I allele below `(founder I mean − 0.05)` in **both** founders, preventing an accidental I-threshold structural impossibility. Other original genotype fields, source reproduction and mutation kernels must remain unchanged in the eventual implementation.

**Key accessibility distinction:** `w=0.046875` cannot attain a founder-relative +0.05 assurance event without new A mutation, even after arbitrary Mendelian segregation, whereas `w=0.078125` makes such an event structurally possible without new mutation. **Possibility is not guaranteed occurrence.** Expected nonmutated F1 assurance variance is `w²/2` under the original independent diploid gamete sampling: **0.0010986328125 vs 0.0030517578125**.

This manipulation changes the supply of alleles and the support reachable without mutation. I scaling also changes its genetic covariance with M and A, not just a single orthogonal variance coefficient. Therefore conclusions must be about **these exact founder treatments**, not an isolated universal effect of `G_I`.

## 3. Minimal pilot: 1,536 new paths only after source review

- **Two fixed founding templates**, main (27200701) and confirmation (27210701), each from the original source-attested 48-adult diploid genotype population.
- **Three declared visitor contexts**: supply0/empty, supply0.125/matched, supply0.125/separated, using the canonical original visitor functional groups. Original model `activity=.4*supply`; supply is a synthetic establishment-rate coordinate, not field visitor abundance.
- **Four genetic treatments**: full A-width × I-variance-factor factorial; **64 new paired stochastic streams per founder** under salt `chapter2-clock-factorial-pilot-v1-20261013`. The identical founder/seed stream key is reused across all 12 treatment×context cells; the original 2,304 histories and prior 6,144 width-history salts are excluded. There are **128 independent stochastic stream clusters, not 1,536 independent ecological histories**.
- **Horizon 200 updates, K=N0=48, source mating model unchanged**. Only A mutates (rate .01, SD .05). M and I retain original nonmutation rules. Adult survival=0 and seed immigration=0. Full original source/reproduction/parentage, IDs and all A/I/M allele copies must be independently audited, with no missing cases selected away.
- **Six outcomes, unchanged**: A-first, I-first, near-simultaneous, A-only, I-only, neither. A increase/I decrease of 0.05 from *actual transformed founder mean*, sustained 20 censuses, tie window5. Original thresholds0.025/0.10 are secondary sensitivity checks only. Extinction is an absorbing process and trait means after extinction are missing, not zeros.
- **Pilot inference ceiling:** feasibility, observed A/I event accessibility, stage-specific frequencies and cross-treatment paired variation for *future power*. No independent confirmation, causal mediator, ecological continuous root, biological genetic-access universality or Q4 persistence benefit.

No confirmed one-paper result or old frozen failed/inconclusive gate changes. A separate producer + immutable source/seed/config manifest and independent birth/genome audit are REQUIRED before any production dispatch. This PR does **not** dispatch the pilot.

## 4. Assumption-based power calculation completed BEFORE design freeze

Predeclared candidate effect for a later independent confirmation is a six-class **log-loss reduction of 0.02** over an **equal-or-more-flexible ecology × genetic-variance null**. This is a meaningful target on the original outcome-probability scale, *not* the estimated effect from a new factorial experiment.

The read-only power worksheet evaluates `P(normal two-sided 95% lower confidence bound for paired log-loss reduction >0)` over independent history-cluster counts, hypothetical score difference SDs and effect sizes. Normal approximation requires that independent founder×stream clusters are a valid asymptotic unit; the 12 nested paths within a cluster are not independent. The calculation ignores model-fitting uncertainty and is explicitly **not empirical study power**.

| Hypothetical paired-history SD | 512 independent clusters, power for Δ=0.02 | Planning action |
|---:|---:|---|
| 0.10 | 99.5% | Retain minimum 512 |
| 0.15 | **85.5%** | 512 clusters (256/founder; 6,144 total paths) |
| 0.20 | 61.9% | Increase to 896 clusters (448/founder; 10,752 total paths) |
| 0.25 | 44.0% | No-go under cap 1,024; do not inflate effect to claim power |

For the eventual separate confirmation proposal, use **only the pilot history-cluster score-difference SD** (with a conservative floor0.15), never the pilot point-estimate effect: `n = ceil_to_128(max(512, ((z_0.975+z_0.8)*max(sd_pilot,0.15)/0.02)^2))`; if `n>1024`, stop. Pilot histories are never reused. This rule is *proposed* in advance and must be validated/reviewed with the complete prospective predictor/null training and uncertainty method before that separate confirmation is authorized.

## 5. What remains to specify before biological execution

1. Authenticate the exact original source ZIP and original source/operator snapshot, including full code that constructs the two founder diploid arrays. Implement the 2×2 genetic transformation in a **new, source-verified orchestration wrapper only** and compare its t0 genotype SHA with the independently computed, read-only fixture in `chapter2_clock_factorial_feasibility_20261013.json`. Do not modify the historical Model 3 modules or allow malformed ref mixing.
2. Freeze a *computable* A-access stage: probability/latency of selectable allelic variation and the explicit mutation-sensitive support bound. Separate F1 potential from realized genetic change; any β_A derivative/selection gradient must be calculated with the canonical female, paternal and selfing genetic return, not just maternal seed output. Freeze an I-response stage using actual full-parent return. Avoid substituting retrospective annual responses when forecasting from t0.
3. Fix the full six-outcome probabilistic model and greater-or-equal-flexibility null (feature maps, regularization, training-context splits, calibration, probability floors, missing/censored handling, and bootstrap/refitting/CI rule). Pilot-derived coefficients may inform **a new protocol** but cannot count as independent main evidence.
4. Lock pilot input/export scripts and paired seed inventory. Run only standalone technical short paths for source/identity tests first. Independent review must admit all 12 factor cells, exact original mutation mask, allele origins/parentage, no random source substitution and no output overwrite/race; then authorize a single 1,536-case biological pilot.
5. If technical/power gates cannot be met, record `HOLD`/`NO_GO` with reason, not a positive conclusion. No outcome-driven parameter/horizon/denominator changes.

## 6. Files / evidence classes

- Machine-readable pilot design: [`chapter2_clock_factorial_pilot_protocol_20261013.json`](../data/design/chapter2_clock_factorial_pilot_protocol_20261013.json).
- Source-verified no-biology genotype transformation: [`audit_chapter2_clock_factorial_feasibility_20261013.py`](../scripts/audit_chapter2_clock_factorial_feasibility_20261013.py) → [`feasibility JSON`](../data/results/chapter2_clock_factorial_feasibility_20261013.json).
- Explicit hypothetical power method: [`audit_chapter2_clock_power_envelope_20261013.py`](../scripts/audit_chapter2_clock_power_envelope_20261013.py) → [`power JSON`](../data/results/chapter2_clock_power_envelope_20261013.json).

**Current decision:** `DESIGN_READY_FOR_SOURCE_AND_STATISTICAL_REVIEW; BIOLOGICAL_EXECUTION_NOT_AUTHORIZED`. Scientific goals that depend on actually observing new histories remain unresolved.
