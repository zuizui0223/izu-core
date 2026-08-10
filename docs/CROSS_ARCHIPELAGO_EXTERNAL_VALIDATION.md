# Cross-archipelago external validation

## Why expand beyond Izu

Izu remains the mechanistic anchor because historical *Campanula* morphology,
outcrossing, autonomous reproduction, contemporary pollinator networks, and the
prospective SVD/reproductive-dependency panel can be linked unusually closely.
External archipelagos are used to test recurrence, response heterogeneity, and
boundary conditions—not to replace that depth with a single global distance
regression.

The general question is:

> When pollinator functional environments simplify or turn over from mainland
> source pools toward continental and oceanic islands, which plant response
> modes recur, and which depend on lineage, effective dependency, geology,
> establishment history, or invasion context?

## Analysis architecture

The analysis is explicitly two-stage.

1. Estimate source-native effects inside each system.
2. Compare those effects across systems while retaining archipelago, lineage,
   evidence type, and response channel.

Community networks, population comparisons, sister-taxon contrasts,
reproductive experiments, and historical observations are not exchangeable raw
rows. Absolute kilometres from a continent are also not treated as a universal
exposure: source pool, stepping-stone structure, island origin, age, sampling
year, and invasion context are stored separately.

## First active external system: Wanshan–Yongxing

Wang et al. (2025; article DOI `10.1111/btp.70027`, data DOI
`10.5061/dryad.t76hdr8bj`) provide four quantitative visitation matrices:

- Wanshan whole community;
- Yongxing whole community;
- seven plant species shared between both islands on Wanshan;
- the same shared-plant subnetwork on Yongxing.

This is especially useful because the matched subnetwork partially separates
pollinator turnover from wholesale replacement of the plant flora.

The implemented reanalysis reports transparent metrics that can be reproduced
without claiming exact equivalence to package-specific H2′ or weighted NODF:

- plant and pollinator richness;
- positive links, binary connectance, total visitation rate;
- Shannon interaction diversity;
- mean Morisita–Horn niche overlap;
- plant-specific visitation and partner-richness log response ratios;
- binary Jaccard and Morisita–Horn pollinator-assemblage turnover;
- exact sign tests and leave-one-plant median sensitivity.

The source design is still one continental island versus one oceanic island,
and the islands were sampled in different years. Therefore the result is an
external contrast, not replicated causation by island geological origin or
mainland distance.

Most importantly, a visitation matrix does **not** measure FDQ, flower–pollinator
trait matching, single-visit pollen deposition, reproductive success, or
effective pollinator dependency.

## Next systems

### Ogasawara

The 2026 CC BY dataset (`10.5281/zenodo.19221853`) contains legitimate
interactions across Chichijima, Hahajima, Anijima, and Ototojima, with site,
forest status, anole context, and season. It will be analysed as an oceanic
invasion/rewiring system rather than a direct mainland-distance replicate.

### Galápagos

The ten-island Dryad dataset (`10.5061/dryad.0c3cn5f`) provides network data plus
area, isolation, age, and sampling effort. Sampling effort must be audited before
interpreting nestedness or richness, and adaptive interaction switching remains
separate from direct pollinator-effectiveness evidence.

### Southwest Pacific floral evolution

The 129 colonisation-event study (`10.1093/aob/mcaf005`) supplies a morphology
layer. Its main use is testing whether animal-pollinated flower-size change
depends on the mainland starting value and differs from wind-pollinated change.
It is not a contemporary network or reproductive-function dataset.

## Claim boundary

External systems can show that network simplification, partner turnover,
rewiring, morphology change, and persistence filtering recur or diverge. They do
not retroactively identify historical *Bombus* causation in Izu. Direct
`effective dependency × functional exposure` moderation remains prospective
until dependency is measured in matched populations.
