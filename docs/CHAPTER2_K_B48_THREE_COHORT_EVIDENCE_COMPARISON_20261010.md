# Chapter 2 — Three independent K-at-fixed-B48 cohorts: evidence-rank-preserving comparison (2026-10-10)

**Status: read-only, post-outcome cross-cohort descriptive comparison. NOT a new preregistered confirmation, pooled meta-analysis, model-independent replication, or test of ecological transport.**

## Scientific question

The new independent fixed-B48 experiment (merged PR #442) confirmed that, conditional on the chosen synthetic model, identical up-to-eight t400 diploid founders and (B=48), lowering modeled demographic carrying capacity from K48 to K8 strengthens the sensitivity of the randomized A-first-vs-I-first expression-order occupancy contrast to an engineered halving of viable selfed seeds. This is a small *difference of differences*, not a statement that A-first universally rescues populations.

A later prospective early-versus-late intervention (merged PR #448) returned an **inconclusive** primary for the timing-of-selfed-viability difference. Separately, all three independent visitor-history cohorts contain a **full-period baseline-vs-half-selfed-viability K-at-B48** contrast. This audit compares their original values *without recomputing the science*.

## Exact original comparisons

For each condition, define `D(K,B,g) = P(occupied at 80 | A-first,K,B,g) − P(occupied at 80 | I-first,K,B,g)`. Then `tau(K,B) = D(K,B,baseline) − D(K,B,half viable selfed seeds for the entire 80-update window)`.

All three rows use **`tau(K8,B48) − tau(K48,B48)`**, matched up-to-eight diploid founders, 4 reproductive settings, old near/far histories, 2 nested demographic repeats, 7 frozen log-weighted budgets and near/far future visitors. Each row represents its own **64 independent visitor-history clusters**, not hundreds of thousands of independent branches.

| Independent new-history cohort | Contrast mean (occupancy probability) | Original paired 64-history bootstrap95 | Evidence rank |
| --- | ---: | --- | --- |
| **40110901–40110964**, four-cell K×B experiment, [PR #440](https://github.com/zuizui0223/izu-core/pull/440) | **+0.0134300** | [+0.0075136,+0.0193620] | **Secondary/descriptive**, selected after outcomes for the next primary |
| **41110901–41110964**, fixed-B48 independent K experiment, [PR #442](https://github.com/zuizui0223/izu-core/pull/442) | **+0.0077457** | [+0.0024972,+0.0130155] | **ONE preregistered supported primary** |
| **42110901–42110964**, early/late/full timed-viability experiment, [PR #448](https://github.com/zuizui0223/izu-core/pull/448) | **+0.0085803** | [+0.0036197,+0.0133988] | **Secondary/descriptive** full-period gate; actual registered timing primary is **inconclusive** |

The three independently sampled cohort estimates have the **same positive direction**. Their descriptive point estimates span **+0.0077457 to +0.0134300**, with a range of **0.0056843**; their simple, *non-inferential* arithmetic mean is **+0.0099187** (about 0.992 occupancy percentage points). None of these is a pooled estimate with an uncertainty interval, a formal between-cohort equivalence result, or a test of selection-free replication. Counting all three zero-excluding intervals as three confirmatory positives would be incorrect.

The first cohort's *preregistered* primary was instead **B-at-K8: inconclusive**; the third cohort's *preregistered* primary was instead **late-minus-early K moderation: inconclusive**. The middle study explicitly followed an outcome-selected earlier secondary observation, so its independent positive primary is meaningful but belongs to an **adaptive sequential hypothesis-development history**. No seed-based repetition after this outcome is warranted merely to obtain a smaller P-value.

## What became more credible, and what did not

**Strengthened within one model:** Repeated fresh visitor-history cohorts show a directionally concordant **model-conditional K-dependent difference** in the A/I expression-schedule occupancy response to manipulated viable selfed seed survival while pollen background B is held fixed. The prospectively registered middle cohort is the direct confirmatory evidence.

**Unchanged limitations:** This is **one model family**, not three independent ecological model architectures or natural island populations. The original pre-registered near/far DID practical equivalence, independent resource-window failure and separate fixed-founder and B-at-K8 **inconclusive** primaries remain. The timed primary does not establish that the causal effect occurs preferentially late or early. A-first/I-first are imposed transient reproductive expression schedules, **not the natural evolutionary order of spontaneous inherited allele changes**. Occupancy at 80 updates is not lifetime plant fitness or field-calibrated Izu extinction probability. Neither cumulative offspring counts nor early-extinction associations identify biological mediation.

**Editorial decision:** Retain the independently supported four-setting floral-investment non-necessity / divergence-compression claim as the main **Ecology Letters** manuscript. Keep these bounded, demographic viability-sensitivity findings in a **separate mechanistic companion**. There is no additional claim of ecosystem-scale geographic generality.

## Reproducibility, sources, and durability

The cross-cohort audit script `scripts/audit_chapter2_k_at_b48_crosscohort.py` reads only three **SHA-256 pinned, previously full-raw-admitted** machine JSON files:

- `results/chapter2/kb_independent_full_readout_20261009.json`: `74df9619590023ee7416035ea31068b541e08dd731b603e879a27c26ccd35ed9`.
- `results/chapter2/k_fixedB48_independent_primary_20261009.json`: `a6f3aad995b561ef4613301857a4e92e24d2d2138d2c66d59a7a28e1bd902023`.
- `results/chapter2/timed_self_viability_independent_readout_20261009.json`: `42d90c17cef4be1643b987428d3a6367ba09dee6594055ae2d2b693ccb190a01`.

The audit checks the three distinct new visitor-history ranges, exactly 64 inference clusters per cohort, complete original t400/future counts, fixed bootstrap seed and each original evidence verdict. It does **not** re-download full future raw ZIPs or recalculate any bootstrap, and does **not** claim an additional raw biological verification. Original raw biological archive ZIPs for **all four separate cohorts** have been preserved and re-downloaded/verified in unpublished GitHub draft Releases (merged PR #449). Full external DOI-backed public deposit still remains open under [Issue #436](https://github.com/zuizui0223/izu-core/issues/436).

**No additional biological histories or treatment outcomes were generated by this read-only comparison.**
