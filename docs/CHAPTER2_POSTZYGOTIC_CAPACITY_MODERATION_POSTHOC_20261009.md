# Chapter 2 — Exploratory paired stress-regime moderation of postzygotic selfing sensitivity (2026-10-09)

**Status: POST-OUTCOME EXPLORATORY; this is not an additional prospective confirmatory gate.**

## Data/analysis provenance

- Prospectively fixed 2×2 postzygotic seed-viability intervention: full GitHub Actions [Run #37869990792](https://github.com/zuizui0223/izu-core/actions/runs/37869990792), success, source SHA `9f69db754ede497b012f4e7dcba5d2aaae9c090a`; original full-result artifact `11590096413`.
- This specific between-regime comparison was selected **after** seeing that the capacity-8 selfed-viability sensitivity passed the primary preregistered gate while the capacity-48 sensitivity did not.
- Fresh read-only source-backed check: [Run #37884342733](https://github.com/zuizui0223/izu-core/actions/runs/37884342733), **success**, including full readmission of **2,048 archived complete diploid t400 sources, 57,344 original futures and 172,032 newly perturbed futures**.
- Machine-readable output: [`results/chapter2/postzygotic_capacity_regime_moderation_posthoc_20261009.json`](../results/chapter2/postzygotic_capacity_regime_moderation_posthoc_20261009.json).
- Reproducible source and synthetic algebra tests: [`scripts/chapter2_postzygotic_capacity_moderation_posthoc.py`](../scripts/chapter2_postzygotic_capacity_moderation_posthoc.py), [`tests/test_chapter2_postzygotic_capacity_moderation_posthoc.py`](../tests/test_chapter2_postzygotic_capacity_moderation_posthoc.py).
- The one-time historical-data readout workflow was removed after successful execution. No new scientific futures or prior cohort outcomes were produced.

## Exactly what is contrasted

For each of the *same* 64 independent visitor-history identities, compute the baseline A-first minus I-first 80-update occupancy difference `D_base` and the difference after halving viable selfed seed output `D_self_half`, each averaged over four reproductive settings, two historical visitor environments, nested repeats, both future visitors and the original seven log-weighted ovule budgets. Define:

`tau_R(h) = D_base,R(h) - D_self_half,R(h)`

and the regime comparison `M(h) = tau_eight_founders_capacity8(h) - tau_unbottlenecked_capacity48(h)`.

Bootstrap **64 paired visitor histories**, 9,999 draws, seed `2026100941`. This is not a difference of two unrelated significance statements, and the future trajectories are not independent units.

| Frozen synthetic stress regime / exploratory comparison | Mean occupancy-scale sensitivity | 95% paired visitor-history bootstrap |
| --- | ---: | --- |
| Eight founders / carrying capacity 8 | **+0.0081451** | [+0.0035365, +0.0128578] |
| No founder bottleneck / carrying capacity 48 | **−0.0012829** | [−0.0047481, +0.0022357] |
| **Between-regime paired moderation: 8−48** | **+0.0094280** | **[+0.0036048, +0.0153466]** |

The interval for the directly paired between-regime contrast excludes zero. This strengthens the *exploratory statistical description* that controlled selfed-seed viability sensitivity differs between the two synthetic founding/stress settings. It does **not** convert this post-outcome comparison into a prospectively registered moderator hypothesis.

The effect of assigning the A-first schedule under the untouched baseline was +0.01209 in capacity 8 versus +0.00924 in capacity 48, both small; after halving viable selfed seeds these were +0.00394 versus +0.01052. These values answer **local terminal occupancy** only.

## Crucial experimental confounding of regime label

The experimental factor labelled `eight_founders_capacity8` sets both the number of sampled founder genotypes **and** the carrying capacity to eight. The comparator `unbottlenecked_capacity48` retains the full 48-genotype t400 source population and carrying capacity 48.

Therefore, this difference **does not identify carrying capacity as the independent causal moderator**. It could arise from the founding bottleneck, genetic sampling, capacity-dependent density regulation, changed starting absolute population size, floor/ceiling effects, or combinations of these. The genotype and demographic random-number identities are paired within each history, but the actual initial genotype subsets are not identical between the two stress regimes.

Likewise, the viability gate is a model-controlled *postzygotic* intervention, while A-first/I-first are randomized **phenotypic expression histories**, not manipulated natural inherited trait-crossing orders. No mediation through genetic rescue in natural island populations has been established.

## Confirmatory hierarchy remains unchanged

1. Original preregistered near/far DID — practically equivalent under the original ±0.05 bound.
2. Independent preregistered budget 3/4 resource window — failed confirmation.
3. Prospectively fixed *new controlled viability sensitivity* in the capacity-8 synthetic regime — **supported**: +0.008145, earlier cohort already exposed and no natural calibration.
4. Capacity-8 vs capacity-48 moderation — **post-outcome exploratory**: +0.009428, CI excluding zero, but founders and capacity co-vary.

## Next causal discriminator, not yet executed

To identify the origin of regime moderation, design a *prospective 2×2 factorial* that crosses independently:

- Founder sample size: **8 versus 48** (entire original diploid genotype sets or explicitly declared subsamples).
- Maximum carrying capacity: **8 versus 48**.

However, the combination **48 founders with maximum capacity 8** is not admissible under the current simulator invariant `n <= capacity`; its initial thinning or transplant timing must be predeclared rather than silently clipping individuals. An alternate fixed-founder design comparing capacity 8 vs 48 **with the same eight starting genotype IDs** is simpler and identifies the effect of capacity conditional on eight founders; the complementary same-capacity different-founder-number contrast can then be tested separately. Frozen random-number pairing and t400 genotype parity checks are required.

No new future interventions are launched by this exploratory readout.
