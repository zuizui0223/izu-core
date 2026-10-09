# Chapter 2 — Independent confirmation of demographic capacity moderation at fixed pollen dilution

**Date:** 2026-10-09  
**Scientific status:** preregistered **SUPPORTED**, strictly within the synthetic Model 3 intervention. The separate, earlier orthogonal 64-history main comparison remains **`inconclusive`**.

## Experiment identity and outcome-independent design

The preceding independent 2×2 K×B study [PR #440](https://github.com/zuizui0223/izu-core/pull/440), raw experiment [Run #37893126472](https://github.com/zuizui0223/izu-core/actions/runs/37893126472), yielded **inconclusive** primary B8 versus B48 at K8: −0.0017526, 95% history-bootstrap [−0.0063336,+0.0028720]. Its **post-outcome secondary** K8 versus K48 at fixed B48 was +0.0134300 [0.0075136,+0.0193620]. That secondary result was a **hypothesis generator**, not a first confirmatory replication.

The independent follow-up was frozen in [PR #441](https://github.com/zuizui0223/izu-core/pull/441) **before exposing any of its newly assigned visitor histories**. Its separate 64-cluster population history IDs are **41110901–41110964**, distinct from the earlier 371*, 381*, 391*, 401* cohorts. Original 4 reproductive settings, historical near/far, A-first/I-first transient equal-dose expression schedules, 2 demographic repeats, 7 log-weighted budgets, 2 future visitor histories, 2 carrying-capacity arms and 2 seed-viability gates were retained.

- **Full independent source archive:** 64 history shards, **2,048 authenticated full diploid t400 source states**, including source-extinct trajectories and parentage.
- **Full future archive:** **114,688 80-update trajectories** (56 futures per full t400 source) with individual SHA-256 and full source-chain admission. Future branches are correlated outcomes; independent bootstrap unit = **64 visitor histories**, *not* 114,688.
- **Manipulation:** the **same at-most-eight inherited complete diploid founder genotypes**, same pollen background normalizer **B=48** in both arms, same visitor exposure and initial stream seeds; vary the **demographic capacity K=8 versus K=48**. The initial reproductive Ledger is identical across K arms for the same source/visitor/budget/gate.
- **Postzygotic gate:** identical baseline (100% viable selfed seed) versus 50% selfed viable seed retained, leaving pollen export and outcross viability unchanged **at the intervention point**. No new plant immigration.
- **Frozen primary estimand:** `tau(K8,B48) - tau(K48,B48)` where `tau(K,B)=D_baseline(K,B)-D_half_selfed(K,B)` and `D=occupancy(A-first)-occupancy(I-first)` after 80 updates.
- **Decision rule:** 9,999 two-sided percentile **paired 64-visitor-history bootstrap** draws with seed `2026100967`; support only if `abs(mean)>=0.005` *and* its entire 95% confidence interval excludes zero; practical equivalence only if entire 95% interval lies strictly inside ±0.005; otherwise inconclusive. Fixed 64-history sample with no optional stopping.

## Executed production, recovery and permanent machine JSON

- Biological source + future computation: [GitHub Actions Run #37896872795](https://github.com/zuizui0223/izu-core/actions/runs/37896872795), original code SHA `2737736f1dca36c8b43e9ac6a9fbd862ca21165b`: **completed/success**. All 64 raw futures shards are independently downloadable.
- Initial readout repair attempts [#37898637860](https://github.com/zuizui0223/izu-core/actions/runs/37898637860), [#37898816728](https://github.com/zuizui0223/izu-core/actions/runs/37898816728), [#37899185428](https://github.com/zuizui0223/izu-core/actions/runs/37899185428) **failed**, for a synthetic numerical-exactness test and then for GitHub Actions artifact retrieval limited to its first 100 of 130 original artifacts. These failed readouts were not tests of the biological hypothesis. The existing raw futures were **not regenerated**.
- Corrected immutable artifact-ID download from both API pages, authenticated full replay and one frozen readout: [Run #37900150213](https://github.com/zuizui0223/izu-core/actions/runs/37900150213), **completed/success**, readout source SHA `592cdad7fa0442a26fd5e79a2fd94812d4515c5d`. All 64 original future ZIPs, all 114,688 futures and source admission were verified before calculating effects.
- [Original readout artifact #11601189449](https://github.com/zuizui0223/izu-core/actions/runs/37900150213/artifacts/11601189449) contains `chapter2-k48-independent-64-history-primary-20261009.json` and its execution console. Byte-identical machine JSON is archived at [`results/chapter2/k_fixedB48_independent_primary_20261009.json`](../results/chapter2/k_fixedB48_independent_primary_20261009.json). Original JSON **SHA-256 `a6f3aad995b561ef4613301857a4e92e24d2d2138d2c66d59a7a28e1bd902023`**.

## Frozen primary outcome

| Quantity | Mean occupancy probability effect | 95% history-cluster bootstrap |
|---|---:|---:|
| `tau(K8,B48)` | +0.0099771962 | [+0.0063404499,+0.0136126143] |
| `tau(K48,B48)` | +0.0022314823 | [−0.0015990853,+0.0061510871] |
| **Registered primary: K8 − K48** | **+0.0077457139** | **[+0.0024971581,+0.0130154788]** |

**Frozen decision: `supported_controlled_demographic_K_moderation_at_fixed_B48`.** The interval excludes zero and the point estimate exceeds 0.005. The history-level paired contrast is positive for **43**, negative for **21**, and exactly zero for **0** visitor histories.

In percentage-point units, at the **fixed modeled pollen-background B48**, the assigned A-first schedule's sensitivity to loss of viable selfed seeds is about **0.775 percentage points larger under K8 than K48**. This is a difference of two randomized intervention sensitivities, not a conventional K effect on unconditional occupancy.

## What the evidence can and cannot claim

**New confirmatory conclusion in this model:** after fixing the pollen-sharing denominator, **population-capacity-dependent demographic regulation still changes the dependence of the expression-order occupancy contrast on postzygotic selfed-seed retention**. The new independent confirmation supports a **capacity moderation mechanism conditional on this model, B48, fixed-eight founders and the specified experimental envelope**.

**Not established:** capacity effects do not imply a universally favorable A-first evolutionary strategy or natural genetic mutation order. The A-first/I-first treatments are **randomly imposed transient expression schedules**, while original allele inheritance and mutation remain active; there is no direct intervention on naturally realized genotype appearance order. The seed viability manipulation is model-engineered, not a uniquely identified natural genetic mediation pathway. `K` affects recruitment vacancies, density-dependent competition, and offspring ID bookkeeping within this simulator. `B=48` is a background recipient normalizer, **not an island area or measured habitat state**. Terminal local occupancy after 80 updates is not individual lifetime fitness and has not been calibrated to observed Izu island extinction.

**Hierarchy and honest history:** (1) the older near/far interaction remained practically equivalent and the independent resource-window hypothesis failed; (2) the earlier orthogonal 64-history K comparison had primary `inconclusive`, which is still frozen; (3) the intervening 2×2 study's **primary B-at-K8** was inconclusive, with its K-at-B48 subgroup **secondary/descriptive**; (4) **only this new independently sampled K-at-fixed-B48 primary passed**, supporting a narrower, more carefully isolated demographic-capacity moderator. The exploratory +0.0134300 and the new +0.0077457 are directionally concordant but **not proven equivalent in magnitude**, nor does repeating a single synthetic model prove broad ecological generality.

## Preservation caveat

Although the original JSON and provenance are committed, original t400 diploid and future-shard GitHub Actions artifacts have finite retention (90 days in the production workflow). [Issue #436](https://github.com/zuizui0223/izu-core/issues/436) tracks full raw archive preservation. The results document does not substitute for a durable independent archive or DOI.
