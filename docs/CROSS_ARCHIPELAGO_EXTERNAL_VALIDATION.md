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

The current effect registry contains **17 rows**, including **16 empirical
numeric rows** and **nine numeric rows with effect-level uncertainty**. Three
Wanshan–Yongxing network effects and three Southwest Pacific morphology effects
are eligible only for a future same-family comparison. They belong to different
evidence families, so no compatible family yet has uncertainty in two
independent system clusters and a formal cross-system model remains closed.

## Wanshan–Yongxing: continental island versus oceanic coral island

Wang et al. (2025; article DOI `10.1111/btp.70027`, data DOI
`10.5061/dryad.t76hdr8bj`) provide four quantitative visitation matrices:

- Wanshan whole community;
- Yongxing whole community;
- seven plant species shared between both islands on Wanshan;
- the same shared-plant subnetwork on Yongxing.

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
invasion contexts, and three seasons.

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
effect. Legitimate contact counts are not pollen deposition, effectiveness,
dependency, or reproductive success.

## Canary–Balearic: same-community derivative recovery

The original 2014 Oxford supplementary route remains blocked. An open PLOS/PMC
study (`10.1371/journal.pone.0150824`; `PMC4777429`) using the same four named
communities was recovered through Europe PMC. All four supporting files were
checksum locked.

The source audit resolved:

- S1: selected plant metadata;
- S2: selected visitor metadata;
- S3: 227 flower-visitor × month derived partner-trait rows;
- S4: 230 plant × month derived partner-trait rows;
- 51 visitor and 52 plant codes;
- 457 parsed rows across all four communities.

The S3/S4 article captions are reversed relative to the species-code domains in
the actual file contents, so the mismatch is retained explicitly. A
first-to-last-month screen produced 24 domain × selection-class × partner-trait
profiles. Three exact sign tests were nominally below 0.05, but none survived
Benjamini–Hochberg correction (`minimum q = 0.3054`).

These are deliberately selected extreme linkage/selectiveness classes, not the
complete 2014 plant-by-visitor matrices. They support heterogeneous seasonal
partner-trait trajectories but remain outside the cross-system effect registry.

## Galápagos: published summaries available, raw network transport blocked

Article DOI: `10.1111/oik.06053`; Dryad dataset DOI:
`10.5061/dryad.0c3cn5f`.

The Dryad metadata and file record resolve `data_galapagos_islands.zip`, but
public file delivery returns HTTP 403 in CI. A DOI-locked DataONE fallback was
therefore added. It queries only records explicitly containing the same Dryad
DOI, expands package-linked identifiers, rejects metadata/resource-map objects,
and validates candidate bytes before admission. The executed DataONE route had
zero query errors but zero DOI-matching indexed documents, so the raw source
state remains `dataone_doi_not_indexed_or_unreachable`. This is a transport or
indexing state, not a biological zero.

A separate published-summary layer uses only source-published ten-island Table 1
and Table 2 values and never reconstructs plant-pollinator edges.

| diagnostic | value |
|---|---:|
| observed–AIS Pearson `r` | `0.82837` |
| observed–AIS `r²` | `0.68620` |
| observed–null `r²` | `0.62467` |
| AIS MAE | `0.0268` |
| null MAE | `0.0367` |
| AIS RMSE | `0.03561` |
| null RMSE | `0.05173` |

AIS has lower absolute error on only `4/10` islands; the exact paired sign-flip
test for mean absolute-error improvement gives `p = 0.5723`. AIS and null
published intervals each cover the observed value on `6/10` islands. Thus AIS
tracks the broad ten-island pattern and lowers aggregate error, but its
island-specific advantage is heterogeneous.

Observed nestedness also correlates with log sampling hours (`r = +0.764`) and
weighted connectance (`r = −0.737`). The age correlation is unstable under
leave-one-island deletion. These are descriptive fixed-table relationships, not
causal biogeographic effects. Raw network, shared-plant turnover, and
species-level Galápagos analyses remain closed until the ZIP is recovered.

## Southwest Pacific: 129 source-defined colonisation events

Article DOI: `10.1093/aob/mcaf005`; PMCID: `PMC12445859`.

The source workbook is already checksum locked and contains exactly 129
source-defined mainland–island colonisation-event rows in the `Flower dataframe`
sheet. The analysis workbook SHA-256 is
`452c6f83143eb17e8249faae9659386be7b162f93742c4e137921952a9b88677`.
The current reproducibility lane attempts Oxford transport first and Europe PMC
as a fallback; the fallback must reproduce all three previously locked file
hashes before any source-native analysis is admitted.

The released workbook contains 89 source-coded animal rows, 39 wind rows and one
unresolved row; valid flower-size data are available for 88 animal and 38 wind
rows. The source/article count discrepancy is retained rather than repaired with
undocumented exclusions.

### Starting-size dependence

| source-coded pollination mode | n | OLS slope `LR ~ log10(FM)` | island-cluster 95% interval | family-cluster 95% interval |
|---|---:|---:|---:|---:|
| animal | 88 | **−0.15099** | **[−0.29979, −0.07390]** | **[−0.24846, −0.01980]** |
| wind | 38 | `−0.07611` | `[−0.14840, 0.10946]` | `[−0.32649, 0.11832]` |

The animal-pollinated starting-size slope is negative under event, island and
family resampling and remains negative in every leave-one-island analysis. The
wind point slope is also negative, but its uncertainty intervals cross zero.
This does **not** by itself establish that animal and wind slopes differ; a new
direct animal-minus-wind bootstrap contrast is therefore analysed separately.
Source-coded pollination mode is not an effective-dependency or
specialist/generalist measurement.

The animal mean flower-size response itself is near zero (`mean LR = −0.00770`,
95% event-bootstrap interval `[−0.05591, 0.03737]`). Thus the important pattern
is starting-size dependence rather than universal island dwarfism: larger
mainland flowers tend to become proportionally smaller and smaller flowers can
become larger.

### Archipelago heterogeneity

All ten source-defined island groups contain at least one valid animal-pollinated
pair. Six groups meet the predeclared minimum of five pairs for a descriptive
within-group slope. All six point slopes are negative, but they vary from
`−0.52091` to `−0.01172` (median `−0.12404`). Only some individual-group
bootstrap intervals exclude zero. Meanwhile mean LR is negative in four groups
and positive in six, spanning `−0.18811` to `+0.13554`.

This distinction matters: a broadly negative starting-size dependence can occur
without a common direction in mean island flower-size change. The 129-pair
system therefore supports a conditional island-rule response, not a universal
shrinkage syndrome. Island-group rows remain descriptive sensitivities and are
not treated as ten independent experiments in the cross-system registry.

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

## Current synthesis

The external results now support four separable conclusions.

1. **Partner turnover can be much stronger than richness decline.**
   Wanshan–Yongxing and Anijima both show substantial rewiring while richness
   intervals include zero.
2. **Morphological island response is conditional rather than universally
   directional.** The Southwest Pacific animal subset shows robust negative
   starting-size dependence, but mean responses differ among island groups.
3. **Sampling and model context matter.** Galápagos nestedness covaries strongly
   with sampling effort and AIS improvement is not consistently positive on all
   islands.
4. **Independent systems, not raw island counts, determine external validity.**
   Within-archipelago depth and cross-archipelago replication serve different
   purposes.

The current external layer does not identify a universal mainland-distance
effect, a common oceanic-island coefficient, or a universal flower-size
direction. It also does not turn source-coded pollination mode into effective
dependency.

## Claim boundary

External systems can show that network simplification, partner turnover,
rewiring, conditional morphology change, and persistence filtering recur or
diverge. They do not retroactively identify historical *Bombus* causation in
Izu. Direct `effective dependency × functional exposure` moderation remains
prospective until dependency is measured in matched populations. Formal
cross-system synthesis remains closed until a second independent system
contributes a genuinely compatible exposure, response, independent unit, and
uncertainty family.
