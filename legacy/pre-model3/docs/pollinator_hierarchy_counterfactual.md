# Pollinator-hierarchy counterfactual check

This check advances the PR33 environment layer into a literature-grounded pattern
comparison. It uses already published Inoue-series channels plus the PR33
island-proxy climate values to compare three declared stage-pattern benchmarks:

1. `pollinator_hierarchy`: mainland large *Bombus* -> Oshima *B. ardens* bridge -> non-*Bombus* bee regime;
2. `environment_only`: temperature and precipitation proxy gradient;
3. `isolation_order`: ordered island-chain isolation proxy.

## Locked input channels

The locked table is `data/inoue_literature_island_traits.csv`. It includes:

- *Bombus diversus* and *Bombus ardens* availability/context indicators;
- halictid and megachilid visitor-record indicators;
- bagged capsule/seed-set summaries as a self-compatibility/selfing proxy;
- outcrossing-rate intervals from the mating-system literature;
- flower-length values where the 1995 experimental table provides a locked population mean;
- PR33 island-proxy climate summaries.

The associated visitor-rate audit distinguishes direct positive rates from
non-reports after effort and from units outside 1986 effort coverage. Thus a
zero context indicator must not be read automatically as biological absence or
ineffective pollination.

## Current locked-input result

The original deterministic pattern score ranks:

| rank | model | mean absolute error |
|---:|---|---:|
| 1 | `isolation_order` | 0.1252 |
| 2 | `pollinator_hierarchy` | 0.1719 |
| 3 | `environment_only` | 0.3390 |

Therefore the simple pattern check does not identify the pollinator hierarchy
as the best of these three benchmarks. It is more compatible than the declared
climate-only benchmark but less compatible than ordered island position.

The accompanying `ardens_nonreport_envelope` changes the uncertain *B. ardens*
context codes for five non-mainland islands across all 32 logical configurations.
In the current artifact, `pollinator_hierarchy` remains rank 2 in every case;
`isolation_order` remains rank 1. This is a robustness result for the simple
stage-pattern score, not an island occupancy inference.

## Boundary

This is not a causal proof and not a demographic parameter fit. A model ranking
means only that its declared island-stage prediction has lower pattern error
against the currently locked observed channels. It should be reported alongside,
not substituted for, the source-level multichannel likelihood and profile
analyses, which use different observation models and assumptions.

Nectar-guide loss and inbreeding-depression costs remain blocked until
island-resolved guide/spot measurements and late survival or fitness data are
imported.
