# Island reproductive payoff → demographic persistence — 2026-10-08

**Status:** Independent-new-history, targeted model confirmation **passed its one predeclared pooled interaction gate**, following two explicitly outcome-informed exploratory screens. It is **not** a natural-island inference, a general parameter-space theorem, or a temporal-order intervention. No previous four-setting Chapter 2 confirmation or failed 64-history payoff gate was revised.

## Why this test exists

The separate 64-history immediate common-visitor assay (`data/results/chapter2_island_payoff_independent_offline_20261008.json`) showed that prior selfing and pollen discount can increase *viable maternal output* while reducing female outcross after low-pollinator history. Its **global all-five gate FAILED** (assurance-cost viability interval crossed zero). First-generation maternal output did not establish persistence.

At the original 48-individual carrying capacity, an earlier 512-trajectory history-swap pilot had **zero extinctions**. A new demographic perturbation was therefore needed before discussing survival or evolutionary rescue.

## Model intervention

For each reproductive setting (delayed control / prior selfing / pollen discount / direct assurance cost) and assurance mode (fixed / evolving), identical genetic founders spent 400 updates in either a high- or low-replenishment visitor history. A matched eight-individual bottleneck retained each realised genotype. The post-switch condition jointly changed capacity to **8** and imposed ovule-budget treatment for 80 reproductive updates. Each paired historical population received the same new near/far visitor-history process and common RNG streams. There was no plant immigration.

This is a joint, synthetic population-size × fecundity disturbance. Changing capacity also changes density-dependent pollen transfer, so a pure bottleneck mechanism is **not** isolated. The original 400-update evolution also changes matching and investment in both assurance modes; fixed vs evolving is an intervention on *assurance capacity evolution*, not an isolated mediation effect on A.

### First exploratory stress grid: 2,048 post-switch trajectories

Budgets 0.25, 0.5, 1 and 8, eight visitor histories × two demographic repeats. The low three budgets drove **all** trajectories to extinction by 80 updates, while budget 8 almost always produced survival. The grid was uninformative about differential rescue because it mostly saturated at 0/1. Source: `data/design/chapter2_island_demographic_stress_pilot_20261008.json`.

### Post-outcome middle-range exploration: 2,048 more trajectories

After seeing saturation, a **different**, explicitly outcome-informed pilot used the same eight histories and budgets 2, 3, 4 and 5. Several setting-by-treatment occupancy differences emerged, e.g. at budget 3, common post=near: prior selfing evolving-assurance near-history survival 3/16 versus far-history 12/16, and delayed control 5/16 versus 11/16. At budget 5, assurance-cost evolving-assurance near-history survival 7/16 versus far-history 14/16. These examples were *selected from exposed pilot outcomes* and cannot validate themselves. All grid rows retained in the raw archive. Source: `data/design/chapter2_island_demographic_midrange_followup_20261008.json`.

### Independent 32-history frozen test: 4,096 post-switch trajectories

Before the **new** visitor histories were generated, we froze a single primary estimand and gate in `data/design/chapter2_island_demographic_independent32_20261008.json`:

For each new history and each of the four settings, average occupancy over **all** four budgets (2/3/4/5) and both post environments (near/far), *without selecting a favourable budget*. Calculate the far-pre minus near-pre difference. Then contrast the same difference between evolving- and fixed-assurance modes. Pool the resulting four-setting interaction **within history**, and use 9,999 visitor-history bootstraps across the 32 independent histories. The frozen gate requires the pooled mean and the 95% history-bootstrap lower bound both to be positive. No setting may be omitted.

New cohort: 32 visitor histories (30100801–30100832), one demographic realisation each (30101801); paired prehistory/counterfactual conditions share deterministic randomization. That is **32 independent visitor histories, not 4,096 ecological replicates**. The absence of multiple independent demographic repeats per new history limits separation of demographic-sampling uncertainty.

**Result — pooled predeclared gate PASSED:**

- Evolving-minus-fixed interaction in integrated persistence, pooled equally across all four reproductive settings: **+0.108398** (10.84 percentage points).
- Percentile 95% visitor-history bootstrap: **[+0.065430, +0.151367]**.
- All 512 ancestral groups and all **4,096** post-switch trajectories completed; eight archival shards have recorded SHA-256 digests.

| Reproductive setting | Fixed assurance: far-pre minus near-pre | Evolving assurance: far-pre minus near-pre | Evolving − fixed interaction | 95% history bootstrap |
|---|---:|---:|---:|---|
| Delayed control | +0.0391 | +0.1914 | **+0.1523** | [+0.0586,+0.2461] |
| Prior selfing | +0.0117 | +0.0625 | **+0.0508** | [−0.0195,+0.1211] |
| Pollen discount | +0.0547 | +0.1523 | **+0.0977** | [+0.0195,+0.1719] |
| Direct assurance cost | −0.0078 | +0.1250 | **+0.1328** | [+0.0742,+0.1914] |

The prior-selfing setting's interval includes zero; **do not** claim four independently positive setting-level tests. This is one pooled, prospectively frozen test on a **pilot-informed** stress grid, not an unbiased discovery of a universal survival threshold.

## Ecological interpretation

The model provides a concrete pathway:

1. Scarce pollinator replenishment changes the female, male and selfing reproductive payoffs, altering selection on investment and assurance.
2. That historical selective regime leaves different inherited populations after 400 updates, even when later visitors are held identical.
3. Under one investigator-defined small-population/fecundity perturbation, allowing assurance evolution can shift the long-term *relative persistence* advantage of the previously visitor-limited population.
4. This advantage is limited: under very low ovule budgets both histories disappear, and with abundant budgets both generally survive.

This supports **conditional historical effects on persistence in this model**. It does *not* identify whether assurance evolved before investment, show that ordering alone caused rescue, or demonstrate a natural-island survival advantage. A negative or null across-setting outcome in a later external model/field system would not overturn this narrow simulation finding; it would limit transportability.

## Reproducibility and claim firewall

Complete, separately SHA-audited raw history groups, all 3 experimental grids, summaries, runner scripts and archived 2026-10-06 biology source snapshot are bundled in the local review artifact `izu_core_island_demographic_stress_20261008.zip`. Archive SHA-256: `cd9f998e38ec51e747c4495dbe94b1fe1168d48d31ef54a438250bfa0ace5a21`; the independent32 summary SHA-256 is `7b725616470d4118fcfb5a6908d27d3cc8569a616242ba8083b42c9103f33e5f`. This ZIP is **not** a DOI-backed public deposition or a GitHub Actions-confirmed reproduction.

PR #413 remains Draft. The active Ecology Letters manuscript must not automatically inherit the persistence claim; it still relies on the separate prospectively confirmed #411 four-setting non-necessity and attenuation results. A future independent model-class or island-system challenge must separately identify the colonization filter, post-establishment adaptation and survivor sampling.
