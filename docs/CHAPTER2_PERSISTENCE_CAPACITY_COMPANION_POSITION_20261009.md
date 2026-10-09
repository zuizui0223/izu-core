# Chapter 2: Position of the independent capacity–persistence experiments (2026-10-09)

**Editorial decision:** retain the [Ecology Letters four-setting floral-investment manuscript](CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md) as the **primary paper**, and present the new assigned-expression-order, seed-viability and demographic-capacity results as a **separate bounded mechanistic companion** (or transparently labelled supplement if requested at review), *not* as evidence that the principal floral-investment result directly predicts extinction.

This document records an evidence hierarchy; it does not rerun or adjudicate any biological experiment.

## Why the papers answer different ecological questions

| Dimension | Primary four-setting manuscript | New finite-population companion |
|---|---|---|
| Ecological question | Is reproductive-assurance evolution **necessary** for low-pollinator floral-investment decline, and how does it change near/far divergence? | Does the **assigned transient order of reproductive phenotype expression** affect modelled 80-update local occupancy, and which reproductive and demographic interventions moderate it? |
| Experimental contrast | Visitor replenishment near/far × assurance fixed/evolving, across four declared reproduction settings | A-first vs I-first assigned expression schedules × viable selfed-seed retention (100% vs 50%) × demographic capacity K, with background pollen dilution B explicitly controlled |
| Outcome | Inherited investment divergence, local rare-mutant reproductive-return components | Binary occupancy after 80 updates, with supplementary seed output, recruitment and demographic effects |
| Main support | Independent preregistered four-setting interaction: all four positive evolving-minus-fixed attenuation estimates +0.1007 to +0.2200; fixed far−near investment always negative | New independently preregistered K effect at **fixed B=48**: **+0.007745713876893593**, paired 64-history 95% interval **[+0.002497158065469939,+0.013015478808429596]**; supported under its frozen gate |
| Limits | Generality across four configurations of **one model**, not natural-island field validation | Capacity moderation of an **engineered viability sensitivity** of randomized phenotype-expression order; not natural inherited mutation-order causality, lifetime fitness or measured Izu-island extinction |

The main four-setting experiment had terminal occupancy **1.0 in every cell** and was never designed to establish an extinction mechanism. The stress test intentionally admits stochastic extinction and uses a different parameter envelope. Do **not** attach the stress experiment's occupancy effect to the main paper's investment result as an estimated mediation path.

## Frozen evidential chronology (nonexchangeable tests)

1. **Original expression-order near/far interaction:** the preregistered whole-grid near–far DID was practically equivalent under its own ±0.05 bound, and the independent preregistered ovule-budget 3/4 window failed. Neither becomes positive after the later work.
2. **Original synthetic postzygotic gate:** [PR #429](https://github.com/zuizui0223/izu-core/pull/429) confirmed in the historical eight-founder/capacity-8 setting that reducing viable selfed seeds by 50% attenuated the A-first/I-first *absolute occupancy* contrast: sensitivity **+0.0081451181**, 95% history interval **[+0.0037080830,+0.0127730549]**. Its 64 source visitor histories had already been exposed before this gate; this is a controlled model intervention, not a natural genetic mediator estimate.
3. **Exploratory cross-regime moderator:** [PR #430](https://github.com/zuizui0223/izu-core/pull/430) observed **+0.0094280182**, 95% [0.0036048,0.0153466], after outcomes. It simultaneously varied starting founder number and capacity and used regime-dependent future RNG. It never established a pure capacity mechanism.
4. **New independent fixed-founder capacity comparison:** [PR #435](https://github.com/zuizui0223/izu-core/pull/435) compared K8 vs K48 with matched eight founder genomes and found **+0.0018484189**, 95% **[−0.0034583915,+0.0073367698]**, **`inconclusive`**. The follow-up [PR #437](https://github.com/zuizui0223/izu-core/pull/437) proved why this still was not a pure demographic intervention: canonical `config.capacity` also enters the pollen-recipient denominator `affinity.sum + capacity * background_ratio`, changing initial female outcross output even before population trajectories diverge.
5. **Independent 2×2 K×B:** [PR #440](https://github.com/zuizui0223/izu-core/pull/440) separately manipulated demographic ceiling **K** and pollen-background dilution **B**. Its preregistered B-at-fixed-K8 primary was **`inconclusive`**: **−0.0017526046**, 95% **[−0.0063336262,+0.0028719524]**. Its K8−K48 contrast at B48, **+0.0134300122** [0.0075136311,0.0193619803], was selected as a **secondary descriptive** signal, not a confirmed effect.
6. **Independent fixed-B48 demographic K replication:** [PR #441](https://github.com/zuizui0223/izu-core/pull/441) preregistered `tau(K8,B48)−tau(K48,B48)` *before exposing new histories 41110901–41110964*. The exact 64-history, 2,048 diploid-source, 114,688-future biological production [Run #37896872795](https://github.com/zuizui0223/izu-core/actions/runs/37896872795) and the full immutable-artifact readout [Run #37900150213](https://github.com/zuizui0223/izu-core/actions/runs/37900150213) both succeeded. **Primary +0.0077457139**, 95% **[+0.0024971581,+0.0130154788]**, history sign 43 positive/21 negative. Frozen machine verdict **`supported_controlled_demographic_K_moderation_at_fixed_B48`**. Exact JSON and checks are merged in [PR #442](https://github.com/zuizui0223/izu-core/pull/442).

Thus the current change is from **unidentified combined founder/capacity/pollination moderation** to **positive, prospectively re-tested demographic-capacity moderation conditional on fixed B48, matched eight founders, and this particular model**. It does **not** make the earlier inconclusive primaries positive or justify a natural island demographic-rescue law.

## What the new confirmed result actually measures

Let `D(K,B,g)` be the equally setting- and environment-averaged A-first minus I-first binary terminal occupancy difference under selfed-seed gate `g`. For a K/B condition, `tau(K,B)=D(K,B,baseline)−D(K,B,self_half)`. The preregistered primary is:

`tau(K8,B48) − tau(K48,B48) = +0.007745713876893593`.

The estimate is an absolute occupancy-probability **interaction difference**, or about **+0.775 percentage points**, rather than a comparison of unconditional occupancies or a fraction of mediation. Its 95% percentile bootstrap interval was calculated over **64 visitor-history clusters** (9,999 paired bootstrap draws, frozen seed 2026100967). The minimum meaningful magnitude was ±0.005 and confidence exclusion of zero, both achieved.

Within-condition sensitivities: K8/B48 **+0.0099771962**, K48/B48 **+0.0022314823**. These are not evidence that A-first is always favored in all mating settings, nor that a naturally evolved earlier-selfing genotype causally rescues plants. The A/I manipulation prescribes **transient expressed phenotype order**, not the order in which inherited mutations arise.

## Recommended publication / figure route

**Ecology Letters main paper:** do not revise the four-setting Abstract, primary figures, or central non-necessity/attenuation claim on the basis of the postzygotic stress campaign. Its expected-title spine remains *Reproductive assurance compresses floral-investment divergence under pollinator limitation*. Citation of the companion, if needed, belongs in a restrained limitations paragraph or Supporting Information; an unintroduced capacity analysis cannot be silently inserted as a fourth primary claim.

**Bounded companion manuscript:** lead with the disconnection between *expression-history-dependent viable selfing returns* and *finite-population persistence*; document the negative near/far interaction and failed budget-window first, then the controlled postzygotic sensitivity, confounding diagnostic, 2×2 K/B separation and independent K-at-B48 primary. A useful main figure would depict (1) the intervention graph (assigned expression history -> reproductive ledger -> recruitment -> occupancy, with K and B separate), (2) the predeclared versus exploratory evidence ladder, (3) the B48 capacity contrast's 64-history bootstrap and (4) the four conditions' pre-registered B-focused null/unknown contrast. Do **not** claim total lifetime fitness or a realized genetic mediator from cumulative recruits.

**Empirical transport remains open:** all positive evidence is from the same explicit synthetic model architecture, not replicated across independent model families or observed natural population evolution. A nature-facing paper needs measured pollinator replenishment, seed-source mating route, demographic bottlenecks and inherited phenotype transitions in corresponding real systems.

## Immediate next work, not another outcome-dependent seed search

- Confirm the final scientific result's exact provenance and keep the earlier null/equivalent/inconclusive outcomes frozen as archived.
- Preserve the full raw t400 state and 64 future shard artifacts from Runs #37896872795, #37893126472 and #37887039116 before their 90-day artifact expiration; track [Issue #436](https://github.com/zuizui0223/izu-core/issues/436). A committed JSON summary alone is **not** full raw-data preservation.
- If further causal dissection is necessary, preregister a mechanism intervention that separately manipulates vacancy competition/survival conditions at fixed K/B rather than interpreting survival-duration-dependent cumulative recruits as mediators. No new confirmatory claim is licensed by exploratory recruitment differences.
