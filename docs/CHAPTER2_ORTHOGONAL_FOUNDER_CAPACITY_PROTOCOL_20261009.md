# Chapter 2 — Prospective orthogonal founder/capacity study (2026-10-09)

**Status: protocol only; no new biological histories, source genotypes, viability gates, or future outcomes have been executed.** The immutable machine-readable contract is [`data/design/chapter2_orthogonal_founder_capacity_20261009.json`](../data/design/chapter2_orthogonal_founder_capacity_20261009.json).

## Why this experiment is necessary

The original postzygotic factorial (PR #429) detected a predeclared, model-conditional selfed-seed viability sensitivity of +0.008145 in the eight-founder/capacity-8 stress regime. The paired *post-outcome* comparison (PR #430) found a difference of +0.009428 between that regime and an unbottlenecked, capacity-48 comparator. **Both founding population size and capacity were changed at once.** The historical simulations also generated future random streams with the *regime index* in the seed. The 64 history IDs were paired, but the stochastic future realizations were not identical across regimes.

The result therefore does not demonstrate a pure carrying-capacity effect, a genetic-diversity mediator, or an island extinction threshold. The pre-existing practically equivalent near/far DID and failed independent budget-3/4 confirmation are retained.

## New design: 3 admissible arms and 2 viability gates

| Arm | t400 starting genotypes | Capacity | Purpose |
| --- | --- | ---: | --- |
| **F8/C8** | A deterministic sample of up to eight original diploid individuals | 8 | Severe-bottleneck reference |
| **F8/C48** | **Exactly the same individual IDs, alleles and starting population** as F8/C8 | 48 | **Primary capacity contrast** |
| **F48/C48** | The complete authenticated t400 population (up to 48 surviving individuals) | 48 | Secondary founding-abundance/genotype-sampling contrast |

The **F48/C8** combination is prohibited: the current model requires initial population size not to exceed capacity. Do not silently thin an initial population of 48 to eight and label it as a valid fully crossed 2×2 experiment.

All three arms have an unchanged baseline gate and a second gate that retains only 50% of model-viable *selfed* seed at the postzygotic recruitment stage. Outcrossed seed viability and pollen export are untouched at the intervention point. Fully extinct and sub-eight t400 sources remain in the cohort; no survival-based exclusion is permitted.

## A newly independent cohort is mandatory

Reserve a prospective, previously unused range of **64 visitor histories, IDs 39110901–39110964**, with fresh prehistories and full diploid t400 source genomes. Explicitly verify no source/case-ID collision before production. Reusing the exposed 38110901–38110964 cohort would make this an additional exploratory conditional rerun, **not** a confirmatory replication.

The complete predeclared grid has four reproductive settings, two historical environments, two assigned expression orders, two nested demographic repeats, seven frozen ovule budgets, two future visitor environments, three demographic arms, and two self-viability gates.

- 64 × 4 × 2 × 2 × 2 = **2,048 complete t400 source states**
- 7 × 2 × 3 × 2 = **84 futures per source**
- 2,048 × 84 = **172,032 future records**; only **64 visitor histories** are independent inference clusters.

Use the **same deterministic F8 genotype IDs and allele hashes** in both primary capacity arms. New future stream initialization must omit both regime and viability-gate identifiers while remaining unique across distinct history/settings/repeats/budgets/future-visitor strata. The existing `paired_streams` helper **cannot be reused unchanged**, because it includes the regime index in its seed. Identical starting streams do not guarantee identical individual-level events after population trajectories diverge.

## Frozen estimands

Let `D(R,G)` be the history-paired, equally setting/historical-environment-averaged A-first minus I-first difference in binary terminal occupancy (80 future updates), pooling demographic repeats and future visitors and using the existing logarithmic seven-budget weights. Define:

`tau(R) = D(R, baseline) − D(R, half_selfed_viability)`.

- **Primary confirmatory test:** `tau(F8/C8) − tau(F8/C48)` — identifies model-specific moderation by *capacity conditional on a matched eight-founder starting population*.
- **Secondary predeclared descriptive test:** `tau(F8/C48) − tau(F48/C48)` — conflates starting population abundance and which genotypes are sampled; it **does not isolate genetic diversity**.

The primary decision is two-sided: a **64-history paired percentile bootstrap**, 9,999 draws with seed `2026100943`. Report support only if the 95% interval excludes zero **and** absolute mean difference is at least **0.005 occupancy probability**. Declare practical equivalence only if the whole 95% interval lies strictly within ±0.005. Otherwise report *inconclusive*. This threshold was selected with the earlier exploratory result visible; the newly independent cohort, not this document alone, provides confirmation.

No optional stopping, outcome-selected subgroup analysis, changing bootstrap unit, selective omission of extinct sources, or rerunning random seeds after peeking is allowed.

## Admission and execution gates

The companion JSON fixes the source provenance, 3 valid arms, independent-history range, estimands, bootstrap, and complete-grid record count. Before running production, implementation must add an **explicitly authorized** new runner and raw archive auditor that enforce the protocol. In particular:

1. Validate every original complete t400 genotype/ID hash and certify the F8 genotype hash is **identical** between F8/C8 and F8/C48.
2. Validate the same external visitor histories and initial pseudorandom streams across gates and capacity arms; prevent regime index from entering the new RNG seed.
3. Verify complete baseline/factorial records, never counting 172,032 correlated future conditions as independent replicates.
4. Audit the entire raw cohort and preservation checksums **before** any confirmatory adjudication.
5. Keep tests, plans, and pull-request CI side-effect-free: no model simulation of novel visitor histories until a separately authorized frozen production run.

**Current decision:** the study design is committed, but the new runner, independent t400 cohort, complete future grid, and result adjudication do not yet exist. No biological conclusion follows from this protocol-only PR.
