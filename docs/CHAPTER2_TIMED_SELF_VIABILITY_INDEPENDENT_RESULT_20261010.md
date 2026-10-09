# Chapter 2 — Independent early-versus-late selfed-seed-viability experiment (2026-10-10 archival review)

**Frozen primary decision: `inconclusive`.** This report preserves the first, predeclared complete-cohort result; it does not replace the successful but different fixed-B48 demographic K experiment in [PR #442](https://github.com/zuizui0223/izu-core/pull/442).

## Scientific rationale and evidence order

The first independent capacity-at-fixed-B48 experiment (new visitor-history cohort 41110901–41110964) **confirmed** that demographic carrying capacity K moderated the randomized phenotypic expression-order occupancy contrast's susceptibility to engineered postzygotic viable selfed seeds: **+0.0077457**, 64-history bootstrap95 **[+0.0024972,+0.0130155]**. Subsequently, [PR #446](https://github.com/zuizui0223/izu-core/pull/446) used that **already outcome-exposed** dataset for exploratory earlier/later extinction and reproductive-channel descriptions. An apparent late appearance of the signal was not evidence of a causal late-life window and could reflect cumulation, extinction-selection, or changing demographic states.

The distinct, prospectively frozen [PR #447](https://github.com/zuizui0223/izu-core/pull/447) therefore randomized **when** model-viable selfed seeds were halved, before running another disjoint independent 64-visitor-history cohort, without treating the PR #446 posthoc late signature as confirmation.

## Frozen intervention

- New independent visitor-history identifiers **42110901–42110964**: 64 independent visitor-history clusters, **2,048** complete diploid t400 source states with original parentage and mutation machinery.
- Identical up-to-eight complete inherited t400 founder genomes across **K=8** and **K=48**, while pollen-recipient dilution normalizer remains **B=48** at every reproduction update, avoiding the old capacity-to-pollen-dilution confounding.
- **Four prospective postzygotic gates**: `baseline` (no attenuation); `early_half` (retain 50% of otherwise viable selfed seeds during updates **0–39 only**); `late_half` (retain 50% during updates **40–79 only**); `full_half` (retain 50% throughout **0–79**). Female outcross viability and expected paternal pollen export are **unchanged at the gate**.
- Four reproductive settings, two prior pollinator environments, A-first/I-first equal-dose **transient phenotype-expression assignments**, two demographic repeats, seven existing logarithmically weighted budgets, two prospective future-visitor environments. Thus **2,048 × 2 K × 4 gates × 7 budgets × 2 future visitors = 229,376 actual future conditions**, but **64** independent inferential clusters.
- Equal *calendar* windows do not imply equal *realized* exposure: some populations become extinct before update 40. No survival-based source exclusions or optional stopping.

Let `D_g(K)` be A-first minus I-first binary occupied-at-80 after gate `g`, averaged over frozen prehistory and future settings, with the original seven-budget log weights. Define `tau_g(K)=D_baseline(K)-D_g(K)`.

The **sole confirmatory primary** is the difference in capacity moderation between *late* and *early* gates:

`[tau_late(K8)-tau_late(K48)] - [tau_early(K8)-tau_early(K48)]`.

Frozen decision rule: **9,999** joint paired 64-visitor-history percentile bootstrap draws, seed **2026100981**, two-sided interval excludes zero **and** absolute point estimate ≥ **0.005** for support; practical equivalence only when the **entire** 95% interval lies strictly within **(−0.005,+0.005)**; otherwise `inconclusive`.

## Original execution and fully authenticated machine result

- Complete, single frozen biological and readout workflow: [Run #37944527799](https://github.com/zuizui0223/izu-core/actions/runs/37944527799), source SHA `e679e0ee190fa02e0a9d60876cd1a3e9987a4c79`: **completed / success**, **131/131 jobs successful**.
- Whole source and future admission completed **before** evaluating the primary: **64/64 independent history shards, 2,048 full-diploid t400 sources and 229,376 future cells**.
- Original [raw machine result artifact #11623707416](https://github.com/zuizui0223/izu-core/actions/runs/37944527799/artifacts/11623707416), containing `chapter2-timed-self-viability-final-20261009.json` and `final-console.txt`. Its JSON is preserved **byte-identically** as [`results/chapter2/timed_self_viability_independent_readout_20261009.json`](../results/chapter2/timed_self_viability_independent_readout_20261009.json), original SHA-256 `42d90c17cef4be1643b987428d3a6367ba09dee6594055ae2d2b693ccb190a01`.

### Scientific readout

| Measure | Mean occupancy-scale difference | Paired 64-history bootstrap95 | Rank |
|---|---:|---:|---|
| **Predeclared primary: late−early moderation** | **−0.0029649032** | **[−0.0072632191,+0.0013173206]** | **INCONCLUSIVE** |
| Early-only K moderation | +0.0060694352 | [+0.0016971548,+0.0105392869] | Descriptive secondary |
| Late-only K moderation | +0.0031045320 | [−0.0022046528,+0.0084543426] | Descriptive secondary |
| Full-period K moderation | +0.0085802590 | [+0.0036196574,+0.0133988032] | Descriptive secondary |
| Full−early−late nonadditivity | −0.0005937082 | [−0.0061382420,+0.0048644629] | Descriptive secondary |

For the **frozen primary**, 31 visitor-history effects were positive, 33 negative. The 95% interval includes zero and is not wholly inside the equivalence region (−0.005,+0.005); hence **neither late dominance nor practical equivalence** is demonstrated. The secondary early-only interval happens to exclude zero, but it is not a second confirmatory primary. Statistical significance of one window and nonsignificance of another is **not** proof that the windows differ.

The model's full-period arm sensitivity is +0.0091950 under K8 and +0.0006147 under K48; those are descriptive within this new timing experiment. They are not an empirical field-island establishment parameter.

## Consequences for the research narrative

**Retained stronger finding:** a separate genuinely independent experiment confirmed K-dependent moderation of selfed seed viability sensitivity **at fixed pollen recipient background B48** (PR #442). The present new experiment does not refute or overwrite that different primary estimand.

**New negative-bounded finding:** a posthoc suggestion that the effect should be stronger when selfed viability is reduced *late rather than early* did **not** pass the separately prospectively registered causal-window test. Avoid the headline that a late-life rescue mechanism has now been identified. Differences in initial breeding returns, selective extinction before the late window, and feedback across generations need distinct interventions to quantify, not causal mediation claims from cumulative recruits.

**Continuing limits:** the A-first/I-first assignment is to transient *expressed* reproductive phenotype schedules, not an intervention on naturally realized genetic mutation order. Selfed viable seed retention is artificially controlled. Occupancy after 80 model updates is neither calibrated Izu Islands persistence nor lifetime individual fitness. All positive findings remain conditional on one explicit plant–pollinator model class and its severe demographic envelope. The separate four-setting floral-investment divergence manuscript retains its earlier confirmatory results unchanged.

## Preservation

The original Actions artifact expires under its retention policy, as do the complete new timing-cohort t400 and future shard ZIPs. [Issue #436](https://github.com/zuizui0223/izu-core/issues/436) already tracks preservation of the preceding three cohorts; the **new fourth timed-gate cohort must be added separately to the raw-artifact preservation inventory**, without claiming it is included in the existing three unpublished draft Releases. External DOI deposit and independent access verification are still pending.
