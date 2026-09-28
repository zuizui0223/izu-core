# Empirical evidence lock: staged island divergence

## Purpose

Before fitting an integrated scenario model, secure each usable real-data layer
in a provenance-preserving form. The project has a small number of islands, so
it must not substitute repeated simulation for missing empirical channels.

The lock has five separate layers:

```text
A. direct historical observations and experiments
B. public occurrence / image candidate records
C. geography and environmental counter-explanations
D. user-owned genomic and phenotype data
E. simulation and counterfactual comparison
```

Simulation begins only after A--D have declared coverage and missingness.

## A. Direct historical observations now digitized

| Source | Direct observations locked | What it can constrain |
|---|---|---|
| Inoue & Amano 1986 | locality effort, visitor groups/rates, flower--visitor size relationship, breeding-system experiment context | observed visitor channel and its effort |
| Inoue 1988 | bagged capsule set, bagged/open seed summaries, bagged-plant distribution, Toshima/Miyake visitor effort | autonomous seed-production and compatibility channel |
| Inoue 1990 PSB 5:57--64 | outcrossing summaries and main-pollinator labels | mating-system and regime channels |
| Inoue 1990 PSB 5:197--203 | compatibility label, outcrossing, staminate/pistillate duration, sex allocation | reproductive allocation and dichogamy channel |
| Inoue, Maki & Masuda 1995 | common-garden flower length, controlled visit response, nectar-size relationship | floral-size and mechanism-boundary channel |

The values are retained as paper/table-level summaries. They are **not** silently
pooled into a modern common-garden or repeated annual field dataset.

## B. Public candidate observations

### Already retrieved

- GBIF: spatially scoped raw candidate snapshots for the focal plant, mainland
  comparison plant, *Bombus ardens*, *B. diversus*, *Lasioglossum*, *Megachile*,
  and *Ceratina*.

### Added in this branch

- iNaturalist: an independent raw candidate snapshot with coordinates, observed
  taxon, date, quality grade, coordinate accuracy, and photo count.

Both sources have exactly the same evidentiary boundary:

```text
public record -> documented candidate observation
NOT public record -> flower visitation -> pollen transfer -> selection
NOT zero public records -> biological absence
```

Record-level review comes before island assignment. The broad Izu envelope is
not an island polygon and is not a distribution model.

## C. Geography and environment

These layers exist to give `environment_only` and geographic-isolation scenarios
a strong, fair competing explanation. The first model uses only a compact,
predeclared set:

```text
- annual mean temperature
- annual precipitation
- precipitation seasonality
- island area
- maximum elevation / terrain ruggedness
- shortest sea distance to mainland
- shortest sea distance to the next island
```

Each value needs a source version, extraction geometry, method, and date. Do not
compute climate means from loosely georeferenced public occurrences.

## D. User-owned data required for the genomic/trait channel

The currently available `.imiss` file is a QC summary only. It cannot yield
pairwise FST, PCA, admixture, IBD, barrier models, or P_ST--F_ST.

The data lock records these as pending input artifacts:

```text
1. raw VCF or PLINK bed/bim/fam
2. sample manifest: individual -> population -> island -> coordinates -> year
3. library / lane / batch metadata
4. island-resolved flower spot measurements or linkable raw images
5. any existing pollinator field records not already represented in Inoue tables
```

The pipeline will refuse to call a genomic or spot trait channel observed until
those files are present.

## E. Integration after lock

The integrated observation vector for population/island `i` is:

\[
Y_i = (L_i,\; t_i,\; A_i,\; D_i,\; M_i,\; S_i,\; R_i,\; X_i,\; G_i).
\]

Where:

- `L`: flower morphology / size;
- `t`: estimated outcrossing;
- `A`: bagging/autonomous seed production;
- `D`: dichogamy and sex allocation;
- `M`: main visitor evidence and direct effort;
- `S`: spot traits;
- `R`: public-record availability evidence;
- `X`: environment and barrier covariates;
- `G`: genomic structure.

No layer is used as a substitute for another. In particular, `R` cannot estimate
visitor effectiveness, while `G` cannot date a pollinator replacement without a
demographic model and compatible sampling.

## Decision rule

After coverage is locked, scenario comparison uses posterior-predictive or
constraint-based compatibility, leave-one-island-out prediction, and sensitivity
maps. With a small number of islands, it should not present a conventional
high-dimensional island-level regression as decisive evidence.
