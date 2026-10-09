# Chapter 2 — Independent 2×2 demographic K vs pollen-background B experiment (2026-10-09)

**Result rank: preregistered primary `inconclusive`.** Full raw experiment **completed / success** and all 64 new independent visitor histories, 2,048 full diploid t400 source states and 229,376 80-update futures passed whole-case admission. The 229,376 future trajectories are **NOT** independent visitor histories.

## Exactly what was changed and why

Previous [PR #435](https://github.com/zuizui0223/izu-core/pull/435) tested capacity 8 vs 48 using matched eight founder genotypes but got **inconclusive** capacity sensitivity +0.0018484, paired-history bootstrap95 [−0.0034584,+0.0073370]. A later, explicitly post-outcome audit ([PR #437](https://github.com/zuizui0223/izu-core/pull/437)) showed that the canonical `config.capacity` affected both the demographic recruitment ceiling **K** and pollen-recipient background dilution **B** through `affinity.sum(axis=0) + capacity*background_ratio`. Capacity was a composite model intervention, even at matched initial founder genotypes.

The new [PR #439](https://github.com/zuizui0223/izu-core/pull/439) froze a genuinely independent two-factor K×B study **before the new cohort was generated**, with:
- New visitor histories **40110901–40110964** and two new demographic repeats, no overlap with the older exposed cohorts.
- Four model conditions **K8/B8, K8/B48, K48/B8 and K48/B48**. Each starts from the exact same deterministic sample of up to eight authenticated complete diploid t400 founder IDs/alleles. Extinct t400 sources are included.
- Two otherwise identical seed-retention gates: baseline and 50% viable selfed-seed contribution at recruitment. Matched initial RNG streams, 4 reproductive settings, 2 old visitor environment assignments, 2 expression orders, 7 log-budget-weighted ovule budgets, and 2 future visitor regimes.
- **K** controls the true maximum plant population size and recruitment vacancies; **B** controls only the pollen-background denominator. When B=K, the complete reproduction Ledger is identical to the original canonical biological model; this was checked through a real old-history 80-update engineering [Run #37892586479](https://github.com/zuizui0223/izu-core/actions/runs/37892586479).
- Assigned A-first/I-first orders are transient expressed phenotype schedules, **not manipulated naturally inherited mutation sequence**.

## Complete, frozen source-backed production

- **Original independent full cohort:** [Run #37893126472](https://github.com/zuizui0223/izu-core/actions/runs/37893126472), **completed / success**, exact source/dispatch SHA `6d04dca9354b3a2b600d26134f86117d225f4708`.
- Preflight, 64 authenticated source shards and complete 2,048-t400 source admission; 64 complete future shards (112 futures per source) and final whole-229,376-future authentication plus registered primary adjudication all **success**.
- Original scientific readout: [artifact `chapter2-kb-64-history-229376-full-readout`](https://github.com/zuizui0223/izu-core/actions/runs/37893126472/artifacts/11600220519). The entire original JSON is preserved **byte-for-byte** at [`results/chapter2/kb_independent_full_readout_20261009.json`](../results/chapter2/kb_independent_full_readout_20261009.json) with SHA-256 `74df9619590023ee7416035ea31068b541e08dd731b603e879a27c26ccd35ed9`.
- **Registered inferential unit:** 64 paired visitor-history clusters, **not** 2,048 source cases or 229,376 individual futures. Bootstrap: 9,999 paired history samples, seed `2026100957`, two-sided percentile95.
- All remaining 80-update stochastic trajectories retain model assumptions and lack a calibrated natural-island field analogue.

## Primary result: isolating recipient pollen-background B at fixed demographic K8

Let `D(K,B,gate) = P(occupied at 80 | assigned A-first) − P(occupied at 80 | assigned I-first)` with equal four-setting/historical-environment averaging, paired visitor histories and demographic repeats, and original seven-budget log weights. Define `tau(K,B) = D(K,B,baseline) − D(K,B,self_half)`.

The **only confirmatory primary** was:

`tau(K8,B8) − tau(K8,B48) = −0.0017526046`, **95% paired-history bootstrap [−0.0063336262,+0.0028719524]** (30 positive, 34 negative histories).

The prospectively fixed decision required **|mean| ≥ 0.005** and the two-sided 95% interval excluding zero for support; practical equivalence required the entire interval strictly within ±0.005. **Neither rule was satisfied. The frozen primary decision is `inconclusive`.** This is not evidence that the B effect is zero, nor confirmation of a recipient dilution mechanism.

## Secondary prespecified, DESCRIPTIVE contrasts

| Secondary contrast | Estimate (occupancy probability) | 95% unadjusted, paired-history percentile interval |
| --- | ---: | --- |
| Demographic K effect, **B8 fixed**, `tau(K8,B8) − tau(K48,B8)` | **+0.00655956** | [+0.00117163,+0.01200915] |
| Demographic K effect, **B48 fixed**, `tau(K8,B48) − tau(K48,B48)` | **+0.01343001** | [+0.00751363,+0.01936198] |
| Pollen-background B effect at **K48 fixed**, `tau(K48,B8) − tau(K48,B48)` | **+0.00511785** | [+0.00137444,+0.00882815] |
| K×B interaction, `tau(K8,B8) − tau(K8,B48) − tau(K48,B8) + tau(K48,B48)` | **−0.00687045** | [−0.01308482,−0.00066672] |

**These comparisons were named before outcomes but deliberately designated secondary/descriptive without a confirmatory multiplicity policy.** They suggest that the true demographic ceiling K could influence the relative susceptibility to viable selfed-seed retention, particularly under B48. However, the positive intervals for these secondary estimands **must not be promoted to a second confirmatory gate**. A distinct new cohort with one predeclared K estimand would be needed to confirm that candidate mechanism.

Within-arm exploratory sensitivities (same `tau` definition) were:
- K8/B8: **+0.00982161**, CI [+0.00489299,+0.01469526].
- K8/B48: **+0.01157421**, CI [+0.00718794,+0.01595131].
- K48/B8: **+0.00326205**, CI [+0.00009087,+0.00630885].
- K48/B48: **−0.00185580**, CI [−0.00608175,+0.00224764].

These are model-conditional occupancy sensitivity measures, not verified natural selection coefficients, lifetime reproductive fitness, or longitudinal mediation through naturally evolving genetic order.

## How the scientific conclusion changed, without overwriting old verdicts

1. **Main Chapter 2 established claim remains:** across four preregistered reproductive settings, visitor-replenishment limitation reduced floral investment even when assurance evolution was blocked, while permitting assurance evolution compressed the near–far investment gap. The ecological central narrative stands independent of the later order/persistence experiments.
2. **Old negative decisions stand:** original near/far assigned-order DID practically equivalent under its own threshold; independent 3/4 resource window failed confirmation; the orthogonal fixed-eight simple capacity-varying primary was `inconclusive`.
3. **Viable-selfed-seed susceptibility can occur:** the earlier planned intervention under bottlenecked capacity8 gave sensitivity +0.008145, and the new study's K8 within-arm sensitivities remain positive. That is controlled postzygotic model susceptibility, **not natural genetic order-mediated rescue**.
4. **New strongest mechanistic insight:** `config.capacity` controlled two distinct biological operations; K and B can be separated mathematically and in a full biological factorial. The newly preregistered **primary B at K8 remained inconclusive**, whereas secondary K effects and K×B interaction suggest model-state dependence. Additional inference must preserve that evidence rank.

## Archival and next step

The primary decision and original result bytes are frozen. Do not rerun only favorable histories or modify the originally declared primary after outcome exposure. Reusable raw-genome and trajectory shards are GitHub Actions artifacts with finite retention; permanent external deposition is still needed ([Issue #436](https://github.com/zuizui0223/izu-core/issues/436)). Any further K-specific confirmatory test requires a **new disjoint history cohort and preregistration** rather than a post hoc re-ranking of the secondary contrasts.
