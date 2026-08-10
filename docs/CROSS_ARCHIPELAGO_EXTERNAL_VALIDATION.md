# Cross-archipelago external validation

## Why expand beyond Izu

Izu remains the mechanistic anchor because historical *Campanula* morphology,
outcrossing, autonomous reproduction, contemporary pollinator networks, and the
prospective SVD/reproductive-dependency panel can be linked unusually closely.
External archipelagos test recurrence, response heterogeneity, and boundary
conditions; they do not replace that depth with a single global distance
regression.

The general question is:

> When pollinator functional environments simplify or turn over across
> mainland, continental-island, and oceanic-island systems, which plant response
> modes recur, and which depend on lineage, effective dependency, geology,
> establishment history, invasion context, or biological response channel?

## Analysis architecture

The analysis is explicitly two-stage.

1. Estimate source-native effects inside each system.
2. Compare only genuinely compatible effects across independent system clusters.

Community networks, population comparisons, sister-taxon contrasts,
reproductive experiments, and historical observations are not exchangeable raw
rows. Absolute kilometres from a continent are not treated as a universal
exposure: source pool, stepping-stone structure, island origin, age, invasion
context, sampling year, and response channel remain separate.

The current effect registry contains 15 rows, including 13 empirical numerical
rows and six numerical rows with effect-level uncertainty. Three Wanshan–Yongxing
rows are eligible for a future same-family cross-system analysis. Three
Ogasawara rows use a different exposure and remain context-specific. No effect
family yet has compatible uncertainty in two independent system clusters, so a
formal cross-system model remains closed.

## Wanshan–Yongxing: continental island versus oceanic coral island

Wang et al. (2025; article DOI `10.1111/btp.70027`, data DOI
`10.5061/dryad.t76hdr8bj`) provide four quantitative visitation matrices:

- Wanshan whole community;
- Yongxing whole community;
- seven plant species shared between both islands on Wanshan;
- the same shared-plant subnetwork on Yongxing.

The matched subnetwork partially separates pollinator turnover from wholesale
replacement of the plant flora. The implementation reports transparent metrics
that do not claim exact equivalence to package-specific H2′ or weighted NODF:

- plant and pollinator richness;
- positive links, binary connectance, and total visitation rate;
- Shannon interaction diversity;
- Morisita–Horn overlap;
- plant-specific visitation and partner-richness log response ratios;
- binary Jaccard and Morisita–Horn partner turnover;
- exact sign tests;
- deterministic exact nonparametric bootstrap intervals for plant-level medians.

### Matched-plant results

| response | median | exact plant-bootstrap 95% interval |
|---|---:|---:|
| `ln(Yongxing visitation / Wanshan visitation)` | **−2.511** | **[−3.323, −2.052]** |
| `ln(Yongxing pollinator richness / Wanshan richness)` | **−0.105** | **[−1.322, 0.288]** |
| pollinator-partner Morisita–Horn turnover | **0.980** | **[0.944, 1.000]** |

The strongest result is not a uniform decline in partner richness. It is a
large visitation decline accompanied by almost complete replacement of the
pollinator assemblage used by the same seven plants.

This remains one continental-island/oceanic-island pair sampled in different
years. Resampling seven plants quantifies heterogeneity among those plants; it
does not create geographic replication or identify geological origin as a
cause. A visitation matrix does not measure FDQ, trait matching, pollen
deposition, reproductive success, or effective dependency.

## Ogasawara: source-native invasion-context networks

The 2026 CC BY dataset (`10.5281/zenodo.19221853`) was acquired and checksum
locked. Its source workbook contains 2,745 interaction rows, including 25
`No_pollinator` sampled-zero markers, across four islands, seven source-defined
invasion contexts, and three seasons. The fields retained are:

- `Island`;
- `Invasional Context`;
- `Season`;
- `Forest_Status`;
- `Anole`;
- `Plant_sp`;
- `Poll_sp`;
- `N.Int` legitimate-contact count.

Zero markers remain in the sampling ledger but are not turned into positive
network partners. Twenty-one context × season networks are summarized before
any contrast.

### Within-Anijima natural-forest contrast

The source defines `ANI_A` as green-anole absence and `ANI_P` as presence. The
comparison contains 12 shared plant × season cells and eight unique plant effect
units after taking a within-plant median across shared seasons.

| response | median | exact plant-bootstrap 95% interval |
|---|---:|---:|
| `ln(anole-presence interactions / absence interactions)` | **−0.608** | **[−1.342, 0.231]** |
| `ln(anole-presence pollinator richness / absence richness)` | **−0.315** | **[−0.875, 0.405]** |
| pollinator-partner Morisita–Horn turnover | **0.682** | **[0.497, 0.965]** |

Interaction abundance and richness vary in direction, whereas partner turnover
is consistently substantial. The supported interpretation is interaction
rewiring under spatially structured invasion contexts, not a randomized anole
effect. Source rows do not contain replicated site identifiers, and legitimate
contact counts are not pollen deposition, effectiveness, dependency, or
reproductive success.

Ogasawara is therefore an independent oceanic endpoint for response-mode and
rewiring evidence, not a direct replicate of the Wanshan–Yongxing geological
contrast or the Izu mainland-distance series.

## Galápagos: analysis-ready parser, source delivery blocked

The ten-island Dryad dataset (`10.5061/dryad.0c3cn5f`) is represented by a
version-aware and bytes-safe source resolver. The implementation can admit:

- source-defined long interaction tables;
- explicitly oriented plant × pollinator matrices;
- island covariates and sampling-effort tables;
- shared-plant island-pair turnover;
- descriptive area, age, isolation, and elevation links.

The public ZIP currently returns delivery or authorization errors in CI.
Consequently Galápagos remains a nonnumeric blocked source state. A failed
remote download is not interpreted as missing interactions, zero richness, or
absence of an island effect.

The next gate is recovery of `data_galapagos_islands.zip` through a lawful public,
institutional, repository, author-supplied, or user-supplied route, followed by
sampling-effort audit.

## Southwest Pacific floral evolution: admission-ready, supplement blocked

The 129-colonisation-event study (`10.1093/aob/mcaf005`) provides the morphology
layer needed to test whether island floral change depends on mainland starting
value and pollination mode. Crossref/OUP discovery, payload validation, and
CSV/XLSX/DOCX table auditing are implemented.

A quantitative pair is admitted only when the source resolves:

- comparison identity;
- island/mainland orientation;
- trait identity;
- trait unit;
- sampling hierarchy;
- numerical values and uncertainty;
- pollination mode, breeding system, island type, and other moderators where
  reported.

Both explicit trait identity and unit are required. The publisher supplement is
currently blocked, so the 129 comparisons are not reconstructed from the
abstract or figures.

## Independent-archipelago replication simulation

A source-locked synthetic simulation holds total sampling at 24 island units
while changing the number of independent archipelagos:

| independent archipelagos | islands per archipelago |
|---:|---:|
| 2 | 12 |
| 4 | 6 |
| 8 | 3 |
| 12 | 2 |
| 24 | 1 |

With strong between-archipelago heterogeneity (`SD = 0.5`) and a null population
mean, naive island-level interval coverage is only `0.435` for the `2 × 12`
design. Archipelago-level coverage is `0.712`, then improves to `0.855`, `0.910`,
`0.926`, and `0.937` for 4, 8, 12, and 24 independent archipelagos.

These are synthetic operating characteristics, not empirical power or a field
sample-size prescription. They support the architecture:

> **deep Izu mechanistic sampling + several shallower independent archipelagos**

Many islands within one or two archipelagos improve within-system resolution but
do not create independent evolutionary repetitions.

## Current synthesis

The external results strengthen three points.

1. **Partner turnover can be much stronger and more consistent than partner-
   richness decline.** Wanshan–Yongxing and Anijima both show substantial
   rewiring, while richness effects include zero.
2. **Response mode matters.** Visitation, richness, partner identity, morphology,
   reproduction, establishment, and effective dependency are distinct channels.
3. **Independent systems, not raw island counts, determine external validity.**
   Within-archipelago depth and cross-archipelago replication serve different
   purposes.

The current external layer does not identify a universal mainland-distance
effect or a common oceanic-island coefficient. Wanshan–Yongxing and Ogasawara
have different exposures and remain separate in the effect registry.

## Claim boundary

External systems can show that network simplification, partner turnover,
rewiring, morphology change, and persistence filtering recur or diverge. They do
not retroactively identify historical *Bombus* causation in Izu. Direct
`effective dependency × functional exposure` moderation remains prospective
until dependency is measured in matched populations, and formal cross-system
synthesis remains closed until a second independent system contributes a truly
compatible effect family with uncertainty.
