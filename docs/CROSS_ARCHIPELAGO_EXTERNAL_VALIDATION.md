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

The checked effect registry contains **17 rows**, including **16 empirical
numeric rows** and **nine numeric rows with effect-level uncertainty**. There are
currently **four model-eligible rows**: three Wanshan–Yongxing network effects
and one Southwest Pacific floral-display effect. The two Southwest Pacific
starting-size slopes remain numeric but are formally blocked by the
measurement-error denominator-coupling gate. No compatible effect family has
uncertainty in two independent system clusters, so a formal cross-system model
remains closed.

## Wanshan–Yongxing: continental island versus oceanic coral island

Wang et al. (2025; article DOI `10.1111/btp.70027`, data DOI
`10.5061/dryad.t76hdr8bj`) provide four quantitative visitation matrices:
Wanshan whole community, Yongxing whole community, and the same seven shared
plant species on each island.

| response | median | exact plant-bootstrap 95% interval |
|---|---:|---:|
| `ln(Yongxing visitation / Wanshan visitation)` | **−2.511** | **[−3.323, −2.052]** |
| `ln(Yongxing pollinator richness / Wanshan richness)` | **−0.105** | **[−1.322, 0.288]** |
| pollinator-partner Morisita–Horn turnover | **0.980** | **[0.944, 1.000]** |

The strongest pattern is a large visitation decline accompanied by almost
complete replacement of the pollinator assemblage used by the same seven
plants, not a uniform decline in partner richness. This remains one island pair
sampled in different years. Resampling plants does not create geographic
replication or identify geological origin, FDQ, effectiveness, or effective
dependency.

## Ogasawara: source-native invasion-context networks

The 2026 CC BY dataset (`10.5281/zenodo.19221853`) is checksum locked. Its source
workbook contains 2,745 interaction rows, including 25 `No_pollinator`
sampled-zero markers, across four islands, seven source-defined invasion
contexts, and three seasons.

For the within-Anijima natural-forest contrast (`ANI_P` green-anole presence
versus `ANI_A` absence), eight unique shared-plant effect units give:

| response | median | exact plant-bootstrap 95% interval |
|---|---:|---:|
| `ln(anole-presence interactions / absence interactions)` | **−0.608** | **[−1.342, 0.231]** |
| `ln(anole-presence pollinator richness / absence richness)` | **−0.315** | **[−0.875, 0.405]** |
| pollinator-partner Morisita–Horn turnover | **0.682** | **[0.497, 0.965]** |

The supported interpretation is interaction rewiring under spatially structured
invasion contexts, not a randomized anole effect. Legitimate interaction counts
are not pollen deposition, effectiveness, dependency, or reproductive success.

## Canary–Balearic: same-community derivative recovery

The original 2014 Oxford supplementary route remains blocked. An open PLOS/PMC
study (`10.1371/journal.pone.0150824`; `PMC4777429`) using the same four named
communities was recovered through Europe PMC and all four supporting files were
checksum locked.

The S3/S4 article captions are reversed relative to the species-code domains in
the actual files, so that mismatch is retained explicitly. A first-to-last-month
screen produced 24 domain × selection-class × partner-trait profiles. Three
exact sign tests were nominally below 0.05, but none survived Benjamini–Hochberg
correction (`minimum q = 0.3054`). These selected derivative profiles remain
outside the cross-system effect registry.

## Galápagos: published summaries available, raw network transport blocked

Article DOI: `10.1111/oik.06053`; Dryad dataset DOI:
`10.5061/dryad.0c3cn5f`.

The Dryad metadata resolve `data_galapagos_islands.zip`, but public file delivery
returns HTTP 403 in CI. A DOI-locked DataONE fallback found no DOI-matching
indexed document. This is a transport/indexing state, not a biological zero.

A separate published-summary layer uses only source-published ten-island tables
and never reconstructs plant-pollinator edges. AIS tracks the broad pattern and
lowers aggregate error, but its island-specific advantage is heterogeneous;
sampling effort is also strongly associated with observed nestedness. Raw
network and plant-level turnover analyses remain closed until the ZIP is
recovered.

## Southwest Pacific: 129 source-defined colonisation events

Article DOI: `10.1093/aob/mcaf005`; PMCID: `PMC12445859`.

The source workbook is checksum locked and contains exactly 129 source-defined
mainland–island colonisation-event rows. The analysis workbook SHA-256 is
`452c6f83143eb17e8249faae9659386be7b162f93742c4e137921952a9b88677`.
The released workbook contains 89 source-coded animal rows, 39 wind rows and one
unresolved row; valid flower-size data are available for 88 animal and 38 wind
rows. The source/article count discrepancy is retained rather than repaired with
undocumented exclusions.

### Starting-size dependence

| source-coded pollination mode | n | OLS slope `LR ~ log10(FM)` | island-cluster 95% interval | family-cluster 95% interval |
|---|---:|---:|---:|---:|
| animal | 88 | **−0.15099** | **[−0.30406, −0.07252]** | **[−0.24834, −0.02076]** |
| wind | 38 | `−0.07611` | `[−0.14876, 0.11631]` | `[−0.32191, 0.11961]` |

The animal starting-size slope remains negative under event, island, and family
resampling and under every leave-one-island analysis. Wind uncertainty crosses
zero. A direct animal-minus-wind analysis does **not** robustly separate the two
slopes, so source-coded pollination mode is not promoted to a causal moderator.

The animal mean flower-size response itself is near zero (`mean LR = −0.00770`,
95% event-bootstrap interval `[−0.05486, 0.03928]`). The important pattern is
conditional response shape rather than universal island dwarfism.

### Measurement-error admission gate

The primary response is `log10(FI/FM)` and its predictor is `log10(FM)`, so the
mainland measurement appears in both the predictor and response denominator. A
classical measurement-error partial-identification audit therefore precedes
formal effect admission.

For the source-coded animal subset:

- the observed negative point slope requires mainland log-size reliability
  above **0.8490** under the declared error model;
- keeping the island-cluster interval wholly negative requires reliability above
  **0.9259**;
- the source does not empirically identify that reliability.

The animal and wind starting-size rows consequently remain numerical and
reportable but have `cross_system_model_eligible = false`. The animal
floral-display mean log ratio remains eligible because this specific shared-
denominator gate does not apply to that response.

### Archipelago heterogeneity

All ten source-defined island groups contain at least one valid animal-pollinated
pair. Six meet the predeclared minimum of five pairs for a descriptive
within-group slope, and all six point slopes are negative. They range from
`−0.52091` to `−0.01172` (median `−0.12404`). Mean LR, however, is negative in
four groups and positive in six, spanning `−0.18811` to `+0.13554`.

Thus a broadly negative starting-size dependence can coexist with no common
mean direction of island flower-size change. Archipelago rows are descriptive
sensitivities, not independent experimental effects.

## Hendriks 2019: independent flower-area sister-pair reconstruction

Hendriks' 2019 Victoria University of Wellington MSc thesis (*The island rule
and its application to multiple plant traits*; author-upload identifier
`10.13140/RG.2.2.25945.08805`; VUW Open Access identifier
`10.26686/wgtn.17136800`) supplies an independent plant dataset around New
Zealand and the southwest Pacific.

The author-uploaded full text exposes Appendix B Table B9 with **35
island–mainland flower-area pairs**. Those 35 numerical pairs were reconstructed
transparently, and Appendix A Tables A1–A12 were used to assign each island taxon
to its source-defined island group. The mapped frequency vector exactly matches
Table A14:

- Antipodes 1; Auckland 1; Campbell 1;
- Chatham 10; Kermadec 4; Lord Howe 11;
- Norfolk 3; Stewart 1; Three Kings 3.

The rounded Table B9 values reproduce the thesis' direct OLS anchor:

| analysis | slope | 95% interval |
|---|---:|---:|
| author-reported `ln(island) ~ ln(mainland)` OLS | `0.58` | `[0.36, 0.82]` |
| reconstructed OLS point | **0.58334** | — |
| pair bootstrap | — | `[0.30601, 0.84913]` |
| island-cluster bootstrap | — | **`[0.21279, 0.77849]`** |
| reconstructed SMA point | `0.90002` | — |
| island-cluster SMA bootstrap | — | **`[0.72967, 1.07310]`** |

Every leave-one-island OLS slope and every leave-one-island SMA point estimate
is below one. Thus the OLS response-shape signal is not explained by treating 35
pairs as geographically independent. However, the symmetric-axis SMA interval
still includes the line of isometry, and mainland flower-area measurement
reliability is not empirically identified.

The VUW institutional record and its `ndownloader` route are now identified, but
the exact PDF/data bytes were not delivered in the current execution environment
and are not checksum locked. Hendriks therefore remains **directional
replication evidence, not a formal registry effect** until the exact source
artifact is locked and the errors-in-variables boundary is better constrained.

## Cross-system morphology response-shape audit

To compare response direction without pooling incompatible raw effects, the
Southwest Pacific animal result is expressed in its equivalent direct form:
`slope(log island trait ~ log mainland trait)`. The two independent systems then
read:

| system | trait | n pairs | island groups | direct OLS slope | island-cluster interval |
|---|---|---:|---:|---:|---:|
| Southwest Pacific animal | source-defined flower size | 88 | 10 | **0.84901** | **[0.69164, 0.92580]** |
| Hendriks 2019 | flower area | 35 | 9 | **0.58334** | **[0.21279, 0.77849]** |

Both source-native OLS summaries and both island-cluster intervals fall below
the isometry slope of one. This is now a genuine **2/2 independent-system
directional replication of a compression-like island floral response shape**.
It is deliberately not a pooled coefficient or formal same-family
meta-analysis.

The boundary remains important: mainland-trait reliability is not empirically
identified in either system, Hendriks' island-cluster SMA interval includes one,
Hendriks source provenance is not checksum locked, and flower size versus flower
area are not treated as identical raw effect scales. The checked
`cross_archipelago_morphology_response_shape_summary.json` therefore remains
`effect_registry_eligible = false` and `formal_cross_system_fit_ready = false`.

## Independent-archipelago replication simulation

A source-locked synthetic simulation holds total sampling at 24 island units
while changing the number of independent archipelagos. With strong
between-archipelago heterogeneity (`SD = 0.5`) and a null population mean, naive
island-level interval coverage is only `0.435` for the `2 × 12` design.
Archipelago-level coverage improves as independent archipelago count increases.

These are synthetic operating characteristics, not empirical power or a field
sample-size prescription. They support the architecture:

> **deep Izu mechanistic sampling + several shallower independent archipelagos**

## Current synthesis

The external results now support five separable conclusions.

1. **Partner turnover can be much stronger than richness decline.**
   Wanshan–Yongxing and Anijima both show substantial rewiring while richness
   intervals include zero.
2. **A compression-like floral response shape now has independent directional
   replication.** Southwest Pacific animal flower size and Hendriks flower area
   both have direct OLS slopes and island-cluster intervals below isometry.
3. **That directional replication is not yet an errors-in-variables result.**
   Unknown mainland-trait reliability and Hendriks' SMA interval prevent a
   universal coefficient or formal same-family fit.
4. **Sampling and model context matter.** Galápagos nestedness covaries strongly
   with sampling effort and AIS improvement is not consistently positive on all
   islands.
5. **Independent systems, not raw island counts, determine external validity.**
   Within-archipelago depth and cross-archipelago replication serve different
   purposes.

The external layer still does not identify a universal mainland-distance effect,
a common oceanic-island coefficient, a pollination-mode causal effect, or direct
effective dependency.

## Claim boundary

External systems can show that network simplification, partner turnover,
rewiring, conditional morphology change, and directional response-shape
recurrence occur across systems. They do not retroactively identify historical
*Bombus* causation in Izu. Direct `effective dependency × functional exposure`
moderation remains prospective until dependency is measured in matched
populations. Formal cross-system synthesis remains closed until a genuinely
compatible response family has source-locked provenance, defensible
errors-in-variables constraints, independent-system uncertainty, and matching
biological interpretation.
