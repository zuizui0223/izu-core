# Island ecology via ecological payoff → selection → evolutionary history

**Status (2026-10-08):** prospective *exploratory* cross-over pilot only. The four-setting result merged in PR #411 stays unchanged; this work cannot be advertised as confirmed persistence, path-dependence, or island-specific field evidence.

## Island-biogeography question

Why do islands with different pollinator replenishment regimes sometimes show similar floral phenotypes, while apparently comparable islands diverge? An observed island phenotype is a mixture of (i) **arrival and establishment sorting**, (ii) **selection on established plant populations**, and (iii) **survivor filtering / demographic loss**. These are distinct causal stages. This pilot isolates stage (ii); it neither models nor quantifies stage (i).

A post-establishment feedback already supported by the independent four-setting campaign: assurance-capacity evolution was not necessary for reduced floral investment in low replenishment, but it consistently narrowed the high–low investment contrast. The post-confirmation arm decomposition attributes 78–90% of this compression to additional declines in the **high-replenishment** populations. A corrected fixed-resident rare-mutant calculation implicates lost marginal maternal outcross and paternal export benefit, not a calibrated effect in a named island species.

## Closest island-biogeography comparators (preoutcome)

- Zell et al. (2025, *New Phytologist*, DOI 10.1111/nph.20234; published online 2024-11-08): 3,222 species across 169 families; island occurrence reflects self-compatibility and especially arrival opportunity. This concerns **which taxa establish**, not the inherited response of a deliberately identical post-establishment population.
- Ciarle et al. (2025, *Annals of Botany*, DOI 10.1093/aob/mcaf005): 129 inferred colonization events across ten Southwest Pacific archipelagos. Animal-pollinated flower size followed an island-rule-like relationship, whereas wind-pollinated flowers showed enlargement. The authors identify the ecological causes as unresolved. This is a direct motivation for separating starting state, pollination function and post-establishment response, **not** an empirical prediction already reproduced by our abstract floral-investment trait. Our ABM only models animal-visitor pollen transfer, not wind pollination or ancestral size allometry.
- Island-rule-like convergence and the modelled attenuation of high–low investment difference are **different statistical patterns**. Neither is evidence of the other without matching ancestral reference states and observational traits.

This literature makes a simple selfing-first explanation or a general rescue claim insufficient for Ecology Letters; the prospective value is in demonstrating how the same current ecology yields distinct *future* evolutionary capacity due to historical payoff-driven genetic change.

## New falsifiable prediction: island evolutionary memory

After the same plant founders have experienced contrasting pollinator histories for 400 reproductive updates, transplant their populations into the **same newly generated pollinator community**. If historical evolution and finite genetic realization matter, they should respond differently despite the same current visitors. We expect three possibilities, all admissible:

1. **History erases:** near- and far-history populations rapidly converge after a common replacement. The earlier divergence was largely reversible under the model.
2. **History persists:** near- and far-history populations retain different investment/assurance/matching, reproduction or recovery for 400 further updates. Historic payoffs and realized genetic composition affect later trajectories.
3. **Mutation dependence:** any lag after transfer differs when *new* mutation is suppressed (0) or allowed (.01), which helps distinguish response possible from retained standing variation from response using de novo input. It does **not** alone prove a loss of evolvability.

Both pre-histories (near/far) are crossed with both new post-histories (near/far) under all four existing reproductive settings, fixed/evolving assurance, and post-switch mutation 0/.01. The exact **finite plant state and random-stream state at the switch are forked**; within each pair the second-stage visitor history is identical. New randomization: four independent visitor histories × two nested demographic repeats. The resulting 512 trajectories are an exploratory screen, **not 512 independent ecological replicates**.

## Biologically necessary separations

- Selection gradients: *local* fixed-resident invasion gradients use **maternal outcross, paternal export, selfing displacement and ovule-allocation cost**. This is not a whole-population reproductive derivative.
- Evolution: ABM genotype inheritance, segregation and demographic sampling yield the realized populations. The PDE is a conditional genotype-density reference, not the ABM mean or currently proven positive-mutation equivalence.
- Reproduction: per-capita viable maternal output at transfer is not occupancy, and realized selfing is not assurance **capacity**.
- Persistence: baseline 48-individual carrying capacity and no seed immigration may make all populations survive. Under that outcome no evolutionary-rescue inference is justified. A separate demographic-risk design, *frozen before examining outcomes*, is required to identify a persistence contrast.
- History versus temporal order: this experiment manipulates **past ecological forcing**, not directly the temporal order of trait changes. It tests a necessary ecological-history mechanism for later work on order-dependent rescue.

## Connection to actual islands

The current prior `near`/`far` contrast represents **visitor functional-type replenishment**, not island area, distance in kilometres, colonization opportunity, extinction rate or pollinator richness itself. The later empirical bridge must independently measure visitation effectiveness, maternal and paternal function, breeding system, and separate colonist identity from in-situ lineage change. Matching island plant floral measurements to synthetic model units without those observations is not validation.

### Interpretation rule

A positive future result would support: *similar contemporary pollination conditions need not imply identical evolutionary potential because historic pollinator limitation altered the inherited population state*. It would **not** demonstrate that historical selfing evolved before attraction in nature, that islands generally converge, or that genetic variation necessarily predicts future fitness.

## Current actions

- Machine-readable pilot protocol: `data/design/chapter2_island_history_transplant_20261008.json`.
- Isolated pilot runner, tests and uploaded exploratory outputs are separate from all previously frozen Chapter 2 confirmation files.
- After descriptive readout, discriminate historical selection from **arrival filtering** in a separately defined founding/establishment experiment; never fit both stages to one endpoint phenotype without identification.
