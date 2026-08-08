# Hiraiwa–Ushimaru boundary identifiability

## Question

Can the contemporary eight-site network data identify a causal Oshima-to-post-Oshima regime effect after accounting for species and repeated seasons?

No. The dataset is highly informative for contemporary ecological response, temporal variation and falsification of universal-response claims, but the focal second boundary has only one independent geographic unit on its Oshima/bridge side.

## Independent geographic structure

The archived design contains:

- three Honshu mainland sites: Hitachi, Hitachinaka and Tateyama;
- one Oshima bridge-state site;
- four post-Oshima Izu sites: Niijima, Kozu, Miyake and Hachijo;
- five repeated seasonal network snapshots per site, for 40 network snapshots total.

For the focal Oshima-to-post contrast, independent geographic replication is therefore:

```text
Oshima/bridge side: 1 site
post-boundary side: 4 sites
```

Plant species sharing a site are not independent boundary replicates. The five seasons at Oshima are repeated temporal observations of the same geographic unit, not five independent bridge-state islands.

## What a site-aware model can estimate

A hierarchical or mixed model can legitimately use the repeated structure to:

- estimate temporal/seasonal variability;
- model plant-species heterogeneity;
- avoid treating seasonal or species rows as independent island observations;
- estimate a descriptive Oshima-versus-post conditional contrast.

It cannot, from this dataset alone, separate an Oshima-specific site effect from a coefficient assigned to the second-boundary state. The boundary indicator and “being the single Oshima bridge site” are inseparable at the geographic level.

Therefore a statistically precise second-boundary coefficient would still not be a causal regime estimate.

## Consequence for the 8/8 trait-matching subgroup result

The source-defined pollen-success target subset contains eight eligible plant species whose corrected trait-matching means are all lower on the post-Oshima side than on Oshima.

That pattern is biologically interesting and source-defined, but it is not eight independent replications of a boundary experiment. All eight comparisons reuse the same Oshima site and the same four post-Oshima site environments.

The correct reading is:

> a coherent multi-species contemporary functional response associated with the Oshima/post geographic contrast in a source-defined subset.

The incorrect reading is:

> eight independent demonstrations that crossing the pollinator-regime boundary causes lower trait matching.

## What additional design would identify the boundary more strongly

At least one of the following would materially change identifiability:

1. another independent geographic site in the Oshima-like bridge pollinator regime;
2. a temporal transition within one geographic site where pollinator regime changes and pre/post plant responses are measured;
3. an external matched-site design that supplies replication of the bridge state while balancing environment/history;
4. a mechanistically measured continuous pollinator exposure that varies independently of island identity across multiple sites.

Until such replication exists, contemporary network data remain a **functional context and falsification layer**, not a causal boundary experiment.

The machine-readable contract is `data/design/hiraiwa_ushimaru_boundary_identifiability.json`; CI prevents species count or repeated seasons from being silently promoted to geographic boundary replication.
