# Izu cline-threshold identifiability stage

## Purpose

This stage connects public-data acquisition to the biological question raised by
the source-locked *Campanula microdonta* calibration:

- floral size changes as continuous erosion;
- multilocus outcrossing changes as continuous erosion; and
- autonomous reproductive capacity changes as a sharp second-transition step.

Nectar-guide and visible-signal data remain excluded. They contribute no direction,
effect size, breakpoint, or simulation truth.

The comparative question is whether an independent response is better represented
by:

```text
none
smooth cline
first step: mainland large Bombus -> Izu Oshima B. ardens
second step: Izu Oshima B. ardens -> no effective Bombus islands
two steps
environment/history alternative
```

## Frozen geographic scaffold

`data/design/izu_regime_scaffold.csv` contains nine islands plus a mainland
reference. The mainland row is a trait-calibration reference and is not part of the
island occupancy universe.

Toshima is the immediate post-Oshima unit, making it the most direct observation
for distinguishing a smooth chain-wide cline from a discontinuity at the second
boundary. Regime labels remain working hypotheses and must not be converted into
measured pollinator effectiveness without source-direct interaction evidence.

## Completed nine-island public-data acquisition

The previous pinned audit covered Izu Oshima, Niijima, Kozushima, Miyakejima,
Mikurajima, and Hachijojima. The supplemental workflow used GSHHG 2.3.7 exact land
polygons and the GBIF occurrence-search API to add:

| island | GBIF records | raw species labels | datasets |
|---|---:|---:|---:|
| Toshima | 263 | 88 | 4 |
| Shikinejima | 348 | 100 | 8 |
| Aogashima | 615 | 304 | 5 |

The combined nine-island candidate product contains:

- **11,104 occurrence records**;
- **2,321 island × raw-species-label rows**; and
- **1,243 distinct raw species labels**.

The full raw acquisition is retained in workflow artifact `8340718650` from run
`29409801950`, with digest
`sha256:4edd2519f3110c928e4d1e24ac1d5240055ce465a2bf0b68d98519219772ddfa`.
Small audit products are committed as:

- `data/public/izu_occurrence_audit/izu_supplemental_summary.json`;
- `data/public/izu_occurrence_audit/izu_9island_effort.csv`; and
- `data/design/izu_supplemental_polygons.geojson`.

These are candidate occurrence data, not a native-flora matrix. The two acquisition
paths have not yet undergone one shared taxonomic normalization, and Aogashima's
high label count must be reviewed rather than interpreted as true native richness.

## Design-power simulation

`channel_id/regime_shape_identifiability.py` generates virtual continuous, binary,
and occupancy responses under each candidate shape and selects among the same
models using BIC. Each reported cell used 300 replicates and 20 independent virtual
lineages.

### Recovery of a true second-transition step

| response domain | current six | add Toshima | full nine |
|---|---:|---:|---:|
| continuous, with mainland reference | 0.953 | **0.993** | 0.983 |
| binary, with mainland reference | 0.570 | 0.650 | **0.687** |
| occupancy, islands only | 0.743 | 0.747 | **0.813** |

The simulation implies three design lessons, conditional on its declared effect
size and observation model:

1. Continuous source-native traits can distinguish a strong second step with the
   present geometry, and Toshima removes most residual cline confusion.
2. Binary states such as SI/SC or autonomous reproduction require multiple
   independent lineages; nine islands improve recovery, but ambiguity remains.
3. Occupancy gains more from completing the nine-island effort surface than from
   adding Toshima alone, because non-detection and island-level effort dominate.

### Structural limitations

The first transition cannot be identified from island-only responses because every
island lies after the mainland-to-island boundary. A mainland or equivalent
large-Bombus reference is therefore mandatory for `first_step` and `two_step`
claims.

Under the present simulation, the full two-step truth is recovered poorly even
when a mainland reference is included. The first- and second-step parameters are
too correlated for the declared number of units and noise. A two-step biological
claim should therefore require either stronger source-direct trait information,
more mainland/large-Bombus reference populations, or a hierarchical mechanism
that links channels without pretending each trait independently estimates both
breakpoints.

The committed compact result is
`data/design/izu_shape_identifiability_summary.json`; the full 90-cell confusion
output is in the workflow artifact.

## Interpretation boundary

The following claims remain prohibited:

- a successful virtual recovery proves staged pollinator loss;
- latitude is a complete environmental/history model;
- occurrence is native establishment;
- non-detection is biological absence;
- the same species label on several islands is an independent evolutionary replicate;
- a regime label is pollinator effectiveness; or
- the unfinished nectar-guide analysis supports a second threshold.

The environmental/history competitor must use measured climate, island area,
isolation, geology, disturbance history, habitat, and observation process. The
simulation's latitude axis is only an order-correlated adversary used to expose
confounding in the sampling geometry.

## Next empirical stage

1. Normalize taxonomy across the pinned and live-GBIF acquisitions and preserve
   synonym decisions.
2. Classify native, introduced, cultivated, transient, and unresolved records.
3. Create effort-aware plant occupancy candidates.
4. Obtain Apidae/Bombus availability under the same exact island polygons.
5. Assign specialist-like/generalist-like dependency classes before inspecting
   island response shapes.
6. Admit source-direct SI/SC, autonomous reproduction, outcrossing, flower-size,
   accessibility, and effective-interaction channels through their native
   observation models.
7. Replace the latitude surrogate with an explicit climate, area, isolation, and
   geological-history likelihood.

The first empirical comparison must report model ambiguity rather than force every
lineage into one island-syndrome trajectory.
