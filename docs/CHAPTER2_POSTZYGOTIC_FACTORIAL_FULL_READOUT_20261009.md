# Chapter 2 — Controlled postzygotic viability factorial: complete production result (2026-10-09)

## Identity, whole-case admission, and frozen verdict

- **Experiment:** separately prospectively frozen synthetic intervention on viable *selfed* and/or *outcrossed* seed contributions, not a manipulation of naturally realized genetic evolutionary order.
- **Frozen protocol:** [`data/design/chapter2_postzygotic_viability_factorial_20261009.json`](../data/design/chapter2_postzygotic_viability_factorial_20261009.json), merged under PR #426.
- **Full workflow:** [GitHub Actions #37869990792](https://github.com/zuizui0223/izu-core/actions/runs/37869990792): **completed / success**. Exact workflow input/source SHA `9f69db754ede497b012f4e7dcba5d2aaae9c090a`; the one-time dispatch workflow was removed afterward.
- **Complete raw cohort:** all 64/64 new-future shards, full-fork checksum and original genotype checks, plus the final admission job **success**. Includes all **2,048 diploid t400 source groups**, **57,344 original baseline futures** and **172,032 newly perturbed futures**, altogether **229,376 future cells**. The inferential unit is **64 pre-existing independent visitor-history clusters**, not the future-cell count.
- **Original downloadable scientific artifact:** [`postzygotic-factorial-full-adjudication`](https://github.com/zuizui0223/izu-core/actions/runs/37869990792/artifacts/11590096413).
- **Machine result committed byte-for-byte:** [`results/chapter2/postzygotic_factorial_full_readout_20261009.json`](../results/chapter2/postzygotic_factorial_full_readout_20261009.json), expected SHA-256 `41b6513a762f8e1d1be7df8ec3533812abc1fc23dd0a37ea78f7c02c1f2826ca`.
- **Original unmodified control:** `baseline` delegates to the verified preexisting `one_future` and the readout draws from archived baseline; no reconstructed control populations or survival-only conditioning.

### Preregistered primary — **SUPPORTED** in the 8-founder/capacity-8 regime

The randomized transient A-first versus I-first expression-schedule absolute terminal occupancy difference, averaged equally across original 4 mating settings, historical near/far environments, both nested demographic repeats and future visitor regimes, and the original 7 log-budget weights, is:

| Synthetic viability treatment | A-first − I-first 80-step occupancy difference | Cluster-bootstrap 95% interval |
| --- | ---: | --- |
| Unattenuated baseline (self 1, outcross 1) | **+0.0120897** | [+0.0067535, +0.0174808] |
| Half viable selfed seeds (self 0.5, outcross 1) | **+0.0039446** | [+0.0012117, +0.0066629] |
| Half viable outcrossed seeds (self 1, outcross 0.5) | **+0.0112629** | [+0.0062123, +0.0161258] |
| Half viable selfed and outcrossed seeds (both 0.5) | **+0.0050458** | [+0.0026592, +0.0074213] |

**Predeclared primary self-viability sensitivity:**

`tau_self = Delta_baseline − Delta_self_half = +0.0081451181`, **95% history bootstrap [+0.0037080830, +0.0127730549]**.

The predeclared minimum magnitude was **0.005 occupancy probability** with a two-sided 95% interval excluding zero. Both conditions were satisfied; frozen machine decision: **`nonzero_controlled_self_viability_sensitivity`**. Expressed in percentage points, the order-schedule advantage fell from about **1.21 pp** to **0.39 pp**, a decrease of **0.81 pp**.

This is a controlled perturbation of the model's *postzygotic seed-viability channel*: it says that the A-first *assigned expression-history effect* on local persistence is sensitive to selfed viable seed retention in the bottlenecked scenario. It does **not** estimate a natural genetic-order-mediated indirect effect, establish that seed selfing is the unique mechanism, or prove a natural-island rescue law.

### Other factorial contrasts in the same primary regime

- Outcross-viability sensitivity `Delta_baseline − Delta_outcross_half`: **+0.0008268**, history bootstrap95 **[−0.0026803, +0.0041248]**. No resolved nonzero effect.
- Two-gate factorial nonadditivity `Delta_baseline − Delta_self_half − Delta_outcross_half + Delta_both_half`: **+0.0019280**, 95% **[−0.0016586, +0.0055155]**. No resolved interaction.
- Under the self-halving gate, the initial A-first minus I-first expected selfed viable population output was **+0.19817**, versus **+0.39634** at baseline. By construction, the initial female outcross output and expected pollen export contrasts did not change from the baseline; both stayed near **−0.23696** and **−0.79853**, respectively. Thus the gate operated on its intended channel at future entry.

The history-paired near/far absolute occupancy schedule contrasts remain **distinct** from a historical-environment DID. In capacity 8, baseline near/far are +0.01656/+0.00762; under self-halving they are +0.00641/+0.00148. This analysis should not be reinterpreted as a confirmed *far-specific* effect.

## Crucial heterogeneity: no-bottleneck/capacity-48 model

In the unbottlenecked/capacity-48 regime:

| Synthetic viability treatment | A-first − I-first 80-step occupancy difference |
| --- | ---: |
| Baseline | +0.0092374 |
| Half selfed viable seeds | +0.0105203 |
| Half outcross viable seeds | +0.0116134 |
| Half both | +0.0130472 |

The same primary sensitivity formula gives **−0.0012829**, 95% history bootstrap **[−0.0047781, +0.0022461]**. This interval contains zero, and the effect is not supported under the predeclared nonzero criterion (the interval does lie within ±0.005, an ancillary *within-regime* practical-equivalence observation). The negative sign is not proof of a reversal. Differences between these synthetic stress regimes should not be generalized into a field-calibrated carrying-capacity threshold.

## Three scientific conclusions to keep separate

1. **Previous frozen question remains negative:** the original full-grid near–far difference-in-differences had a small practically equivalent effect under the separately declared ±0.05 threshold. The independent preregistered budget-3/4 window confirmation failed. Neither verdict was overwritten.
2. **A new positive, model-conditional test:** when selfed viable seeds were experimentally halved, the previously exploratory A-first *absolute* local-persistence advantage diminished under eight-founder/capacity-8 bottlenecks. This planned synthetic intervention supplies stronger evidence of causal *sensitivity* than post-outcome correlations between selfing and survival.
3. **Important limits:** only the viability channel was directly intervened upon. Altered offspring survival propagates through genotype inheritance, competition, demographic stochasticity, recruitment opportunities and local extinction. That total response is not a pure natural indirect effect or proof of higher total plant fitness; pollen export is an expected output, not lifetime realized paternal success. The 64 historical visitor environments had already been observed, and the new intervention shares model assumptions and source genotypes with the earlier experiment.

The strongest defensible ecological statement is that **the evolutionary-expression schedule's small local persistence contrast is dependent on postzygotic selfed-seed viability under a severe finite-population bottleneck, but this dependence does not generalize automatically to the higher-capacity control**.

## Reproduce / preservation

```bash
gh run download 37869990792 --repo zuizui0223/izu-core \
  --name postzygotic-factorial-full-adjudication --dir /tmp/ch2-factorial
sha256sum /tmp/ch2-factorial/final.json
# 41b6513a762f8e1d1be7df8ec3533812abc1fc23dd0a37ea78f7c02c1f2826ca
```

Archive PR introduces only this interpretation document plus an exact byte-for-byte readout JSON. No new history cohorts, protocol revisions or biological outcomes are launched by the archive operation.
