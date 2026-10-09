# Chapter 2 — Identify causal sensitivity to selfed versus outcross seed viability

**2026-10-09 — prospectively declared, no new postzygote intervention outcomes.**

## Confirmed scientific state

The original assigned-order full-grid near–far interaction was practically equivalent under its own prespecified occupancy ±0.05 criterion. The separately frozen independent budget-3/4 "threshold" study did **not** confirm a localized effect. Post-outcome raw-case reanalysis shows a small, directionally positive **absolute** A-first occupancy contrast and stronger selfed expected seed output and recruited descendants, with reduced outcross contribution and expected pollen export. Replaying the original and next disjoint 64-history cohorts yielded the same seven signed contrasts under the same fixed model. These results motivate a *new* model-specific intervention but neither confirm natural gene-order mediation nor establish total fitness gain.

## New estimand is not mediation by observed genetic order

The question is: **if viable selfed seed survival is experimentally reduced after fertilization while keeping each already evolved t400 diploid source state unchanged, does A-first's subsequent local persistence advantage diminish?**

For each of the 64 previously used (already exposed) environmental histories, define a paired A-first vs I-first 80-update occupancy difference `Delta_g(h)` under gate `g`. Within each history average the same four reproductive settings, both near/far historical contexts, two demographic repeats, two future visitor environments and **seven original log-weighted ovule budgets** in primary capacity-8 stress.

Predeclared primary sensitivity:

```text
tau_self(h) = Delta_baseline(h) - Delta_attenuate_self(h)
```

Secondary: `tau_outcross(h) = Delta_baseline(h) − Delta_attenuate_outcross(h)`; a 2×2 nonadditivity contrast; absolute near/far survival under all gates; and capacity-48 stress. Bootstrap only the 64 independent visitor histories, two-sided percentile95, 9,999 draws and seed 2026100927. A nonzero sensitivity requires an interval excluding zero **and** an absolute mean ≥0.005 occupancy; an interval wholly inside (−0.005,+0.005) is practical equivalence, otherwise inconclusive. This **0.005 is a newly specified sensitivity scale, not a rewrite** of either earlier experiment's 0.05 criterion.

The 64 historical states are already outcome-exposed, so this does not qualify as a new unexposed historical cohort. The **future viability intervention itself** is declared before running its new counterfactuals. Conditional model intervention sensitivity is not the natural indirect genetic-order effect.

## Manipulation: downstream of pollen transfer, upstream of recruitment

The frozen original `scripts/model3_island/reproduction.py` produces an immutable `Ledger`: donor-row × recipient-column expected outcross viable seed contributions, an array of viable selfed contributions, ovule budget, pollen export and delivery, and maternal/paternal bookkeeping.

In the experiment the canonical ledger is generated first. Then the **viable seed offspring contribution** is scaled after fertilization, not the expressed floral trait, genotype, visitor encounter, ovule allocation or pollen transfer.

| Gate | Selfed viable seed retention | Outcross viable seed retention |
| --- | ---: | ---: |
| baseline | 1 | 1 |
| attenuate_self | 0.5 | 1 |
| attenuate_outcross | 1 | 0.5 |
| attenuate_both | 0.5 | 0.5 |

From the scaled viable offspring matrix, recompute maternal total per recipient and paternal offspring contribution per donor. Keep pollen export, pollen delivery, raw selfed seed formation, ovules, mutation rules, source alleles, founder identities and all visitor/demographic stream seeds unchanged.

This is a **synthetic postzygotic viability manipulation**, not a realistic field estimate of seed mortality. It does not pretend that exported pollen is sired offspring. Loss of offspring viability is not reallocated automatically into another reproduction channel.

For the exact `(1,1)` gate, return the original ledger **by identity** and delegate future simulation to the frozen original `one_future`. Reject new/unregistered factors, negative fractions, increased viable seed counts, maternal outputs above the original ovule budget, and inconsistent male/female expected viable offspring accounting. Source state arrays remain read-only.

## Future design and stopping gate

Reuse the full **2,048 t400 states** from successfully archived independent Run [37862121201](https://github.com/zuizui0223/izu-core/actions/runs/37862121201), each hash-authenticated against its original biological source. Its 57,344 baseline futures are already complete. The three new gates across the original 28 futures per state would create **172,032 new counterfactual future trajectories**, to compare against the 57,344 baseline futures (229,376 across the full factorial). No new t400 histories are generated; no biology is calibrated to natural Izu conditions.

No new future outcomes may be run in PR CI or the historical engineering preflight. Before authorizing production, require:

1. **OLD visitor history 26110601**, used only for engineering tests, shows bit-for-bit identical baseline future output versus frozen `one_future`.
2. Each gated synthetic/old-history ledger passes all population conservation and parentage validity tests, with no genotype alteration before future start.
3. A future results reader authenticates **all 2,048 source state hashes and all 57,344 baseline outcomes**, and admits only a complete 3×28×2,048 viability-fork grid.
4. All observations, positive/negative/zero paired history effects, and compulsory capacity-48/future-visitor/budget sensitivities are retained; no survivor-only, first-genetic-crossing, posthoc-best-budget or future-branch pseudoreplication.
5. Expected case costs and artifact retention are audited before a manual full launch requiring reviewed `main` SHA and explicit approval.

This branch presently supplies only the **frozen experimental contract, a pure mass-conserving ledger gate, a conditional future replay function and old-history/synthetic tests**. It does not itself run or authorize the 172,032 new futures.

## Limits and interpretation

If the schedule contrast shrinks after reducing selfed viability, the model's A-first **schedule effect is sensitive to a controlled selfed seed viability manipulation**, not necessarily "the natural indirect effect of genetically evolving selfing first." The gate perturbs extinction risk, mean genotype trajectories and density feedback jointly. The response can reflect floor/ceiling effects and ecological conditions, so even a positive result remains conditional on this synthetic payoff model.

If there is no change, it does not falsify reproductive assurance in nature: a halving of postzygotic seed viability may be buffered by long-lived adults, other pathways, or the floor/ceiling regime. No genetic mediation, total evolutionary fitness, or natural-island rescue claim is made without further separately identified evidence.
