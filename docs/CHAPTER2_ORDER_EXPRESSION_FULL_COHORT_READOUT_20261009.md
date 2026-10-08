# Chapter 2 — full assigned-expression-order cohort: confirmatory readout (2026-10-09)

## Frozen provenance and admission

- Design/runner: merged PR #415; guarded launch PR #416.
- **Successful complete-production run:** https://github.com/zuizui0223/izu-core/actions/runs/37856410822
- **Exact source commit executed:** `6d9a2686359a2be131370d48300f9165c72844ce` (`main` at dispatch). A temporary workflow-dispatch bridge was removed after launching; no frozen biological source or analysis script was changed.
- Final artifact: [`order-expression-complete-audited-readout`](https://github.com/zuizui0223/izu-core/actions/runs/37856410822/artifacts/11583968991).
- Canonical result snapshot committed alongside this note: [`results/chapter2/order_expression_full_cohort_20261009.json`](../results/chapter2/order_expression_full_cohort_20261009.json); exact SHA-256 of the original readout JSON: `188ecf42f96b53d985bac2bd0a236956cb6b37518b54ec67bff4686cd4583ccb`.
- Frozen protocol SHA-256: `b6f6336875b04a131434ef35d6ec42b59dc14a1e4c59e7e4d6f2513e24a04fdd`.
- Workflow outcome: **success**; preflight 1/1, t400 source shards 64/64, future shards 64/64, final readout 1/1.
- Final reader admitted **3,072 complete t400 diploid sources**, **86,016 verified future trajectories**, **64 independent visitor histories**, and two nested demographic repeats per source/history setting. It independently rechecked the annual inherited-trait order against source summaries, genotype/source hashes, pedigree provenance, and the complete 28-fork grid for each source.

This is the **first admitted prospective outcome** for the #415/#416 expression-order experiment. Do not substitute old-history engineering smoke outcomes for these results.

## Preregistered primary result

The randomized intervention is **assigned transient phenotype-expression schedule** (A-first vs I-first), *not* observed genetic first-crossing order. The primary estimand is the history-paired far–near difference-in-differences of 80-update terminal occupancy:

`DID = (far[A-first − I-first]) − (near[A-first − I-first])`

It pools all four mating settings equally *within each visitor history*, integrates seven ovule budgets on the prespecified log grid, averages the two future visitor environments and two nested demographic repeats, and bootstraps the **64 histories** (9,999 resamples; preregistered seed).

| Primary stress: 8 founders, capacity 8 | Value |
| --- | ---: |
| Mean far–near DID | **−0.0135891371** |
| 95% visitor-history bootstrap percentile interval | **[−0.0228118886, −0.0043024452]** |
| Preregistered practical-effect region | ±0.05 occupancy |
| **Frozen decision** | **`equivalent_within_predeclared_ROPE`** |

**Interpretation:** The interval excludes exact zero, but is wholly inside the *predeclared practical-equivalence interval* (−0.05, +0.05). Therefore the preregistered claim of a meaningfully large pooled expression-order effect is **not supported**; the *frozen* classification is practical equivalence, **not** a rescued positive result. It does **not** establish a mathematically zero effect or rule out smaller context-specific effects. The historic failed independent16 mutational-access priority confirmation in #413 remains FAILED and has not been overturned.

## Absolute effects and compulsory stress comparator

The pooled (four-setting average) **A-first minus I-first absolute occupancy** within each historical environment is:

| Scenario | near A−I | far A−I | far–near DID |
| --- | ---: | ---: | ---: |
| **8 founders / capacity 8 (primary)** | +0.015415 | +0.001826 | **−0.013589** |
| No founder bottleneck / capacity 48 | +0.009842 | +0.004144 | −0.005699 |

A negative DID is not evidence that A-first lowers absolute far-environment survival. On average, A-first has a *small positive absolute* occupancy difference in both far and near primary cells, with the greater benefit near.

### Prespecified mandatory mating-setting breakdown

All values below are the setting-specific **far–near DID**. The intervals use the same visitor-history bootstrap and are not independent ecological replicates.

| Mating rule | Primary capacity-8 DID [95% bootstrap] | Capacity-48 DID [95% bootstrap] |
| --- | --- | --- |
| `delayed_control` | −0.008121 [−0.027884, +0.012330] | +0.001874 [−0.014851, +0.018994] |
| `prior_selfing` | −0.012234 [−0.030509, +0.005910] | −0.010411 [−0.022305, +0.001631] |
| `pollen_discount` | −0.029273 [−0.047495, −0.010921] | −0.005623 [−0.018070, +0.007037] |
| `assurance_cost` | −0.004729 [−0.018970, +0.009485] | −0.008635 [−0.020562, +0.003034] |

The primary `pollen_discount` stratum has a negative interval excluding zero but its magnitude is **below 0.05** and these setting contrasts are secondary. It cannot override the prespecified pooled verdict, and multiplicity across settings must be considered before interpretive promotion.

## Budget-resolved sensitivity: exploratory *localization*, not a new confirmation

The readout prespecified reporting every budget × future visitor environment (7 × 2 = 14 cells per stress regime). The following are *unadjusted descriptive effect magnitudes*, with no post-hoc primary-gate change or new uncertainty tests.

- **Primary eight-founder/capacity-8:** budget 3 near: **−0.074219**; budget 3 far: **−0.054688**; budget 4 near: **−0.052734**; 3/14 cells have |pooled DID| ≥ 0.05. At budgets 0.5 and 1 all corresponding pooled differences were exactly 0.
- **No-bottleneck/capacity-48:** budget 3 far: **−0.050781** is the only one of 14 cells with |pooled DID| ≥ 0.05. Budget 3 near is **−0.042969**.
- These pattern selections were identified after outcome exposure, are not prospectively powered or multiplicity controlled, and cannot be called validated mechanistic thresholds.

A **testable new hypothesis** is that finite-population expression-order effects are confined to intermediate resource budgets, while floor/ceiling regimes mask differences. Before pursuing this, freeze a new independent cohort, a numerically fixed budget-window contrast, sign-free decision criteria, and comparison against a smooth resource response; do not reinterpret the current pooled-equivalence result. The original 64 histories are already exposed and cannot function as independent confirmation.

## Scientific identification limits

1. Randomization identifies **assigned expression-schedule effects** in the coded model. It does **not** identify causal effects of the *naturally realized genetic order*, which is a post-treatment variable; no conditioning on survivors or crossing categories is permitted to redefine ITT.
2. Matching each trait's assigned duration does **not** equate the entire realized selection history or genotype distribution; the synchronous comparator also differs in co-expression duration and is *not* a pure order-matched control.
3. Both stress/capacity regimes are **synthetic**. There is no calibrated natural-Izu extinction risk, proof of an island rescue law, or direct field validation.
4. Secondary budget and reproductive-setting variations cannot replace the preregistered full-grid primary test. The 86,016 future branches are **not** 86,016 independent ecological replicates.
5. The engineering cost audit used **old visitor history 26110601 only**, without peeking at the new cohort. Its single-sample cost estimates were not scientific evidence.

## Reproduction and next permitted decision

```bash
gh run download 37856410822 --repo zuizui0223/izu-core \
  --name order-expression-complete-audited-readout --dir /tmp/chapter2-readout
sha256sum /tmp/chapter2-readout/order_itt_readout.json
```

Expected JSON SHA-256: `188ecf42f96b53d985bac2bd0a236956cb6b37518b54ec67bff4686cd4583ccb`.

**Next scientific decision:** Report the full-cohort practical-equivalence outcome without promotion. Only a separately **prospectively frozen independent** intermediate-budget-window study can test the post-outcome localization hypothesis. No new independent biological histories are launched by this report.
