# Izu cline-threshold identifiability stage

## Purpose

This stage connects public-data acquisition to the biological question raised by
the source-locked *Campanula microdonta* calibration:

- floral size changes as continuous erosion;
- multilocus outcrossing changes as continuous erosion; and
- autonomous reproductive capacity changes as a sharp second-transition step.

Nectar-guide and visible-signal data remain excluded. They contribute no direction,
effect size, breakpoint, or simulation truth.

The competing response shapes are:

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
boundary. Regime labels remain working hypotheses and are not measured pollinator
effectiveness.

## Completed nine-island public-data acquisition

The pinned audit covered Izu Oshima, Niijima, Kozushima, Miyakejima, Mikurajima,
and Hachijojima. The supplemental workflow used GSHHG 2.3.7 exact land polygons
and GBIF occurrence search to add:

| island | GBIF records | raw species labels | datasets |
|---|---:|---:|---:|
| Toshima | 263 | 88 | 4 |
| Shikinejima | 348 | 100 | 8 |
| Aogashima | 615 | 304 | 5 |

The combined nine-island candidate product contains:

- **11,104 occurrence records**;
- **2,321 island × raw-species-label rows**; and
- **1,243 distinct raw species labels**.

The effort-corrected full artifact is `8340962440` from workflow run
`29410478908`, digest
`sha256:0b229a6b94847fd1caa7a331819963d32a080cde69e9a82be274e75af090fc5b`.
Small committed products are:

- `data/public/izu_occurrence_audit/izu_supplemental_summary.json`;
- `data/public/izu_occurrence_audit/izu_9island_effort.csv`; and
- `data/design/izu_supplemental_polygons.geojson`.

These are occurrence candidates, not a native-flora matrix. The two acquisition
paths still require one shared taxonomic normalization. Aogashima's high raw-label
count must be audited rather than interpreted as native richness.

## Design-power simulation

`channel_id/regime_shape_identifiability.py` generates virtual continuous, binary,
and occupancy responses under each candidate shape and selects among the same
models using BIC. Each cell used 300 replicates and 20 virtual lineages. Occupancy
non-detection uses the acquired nine-island record effort rather than a uniform
placeholder.

### Recovery of a true second-transition step

| response domain | current six | add Toshima | full nine |
|---|---:|---:|---:|
| continuous, with mainland reference | 0.953 | **0.993** | 0.983 |
| binary, with mainland reference | 0.570 | 0.650 | **0.687** |
| occupancy, islands only | 0.743 | 0.787 | **0.850** |

Conditional on the declared effect size and observation model:

1. Continuous source-native traits can distinguish a strong second step with the
   current geometry, and Toshima removes most residual cline confusion.
2. Binary states such as SI/SC or autonomous reproduction require several
   independent lineages; nine islands improve recovery, but ambiguity remains.
3. Occupancy benefits from both the immediate post-Oshima island and completion of
   the full effort surface. The gain after replacing placeholder effort confirms
   that detection design is part of the biological test, not a nuisance added later.

### Structural limitations

The first transition cannot be identified from island-only responses because every
island lies after the mainland-to-island boundary. A mainland or equivalent
large-Bombus reference is mandatory for `first_step` and `two_step` claims.

The full two-step truth is recovered poorly even with a mainland reference. The
first- and second-step parameters are too correlated for the declared units and
noise. A two-step biological claim therefore needs stronger source-direct traits,
more mainland/large-Bombus reference populations, or a hierarchical multichannel
mechanism rather than pretending each trait independently estimates both breaks.

The compact result is `data/design/izu_shape_identifiability_summary.json`; the
full 90-cell confusion output is retained in the workflow artifact.

## Interpretation boundary

Do not infer that:

- successful virtual recovery proves staged pollinator loss;
- latitude is a complete environment/history model;
- occurrence is native establishment;
- non-detection is biological absence;
- repeated island records are independent evolutionary replicates;
- a regime label is pollinator effectiveness; or
- unfinished nectar-guide work supports a second threshold.

The environment/history competitor must use measured climate, island area,
isolation, geology, disturbance history, habitat, and observation process. The
latitude axis is only an order-correlated adversary.

## Next empirical stage

1. Normalize taxonomy across the pinned and live-GBIF acquisitions and preserve
   synonym decisions.
2. Classify native, introduced, cultivated, transient, and unresolved records.
3. Create effort-aware plant occupancy candidates.
4. Obtain Apidae/Bombus availability under the same exact island polygons.
5. Assign specialist-like/generalist-like dependency classes before inspecting
   island response shapes.
6. Admit source-direct SI/SC, autonomous reproduction, outcrossing, flower-size,
   accessibility, and effective-interaction channels through their native models.
7. Replace the latitude surrogate with an explicit climate, area, isolation, and
   geological-history likelihood.

The first empirical comparison must report model ambiguity rather than force every
lineage into one island-syndrome trajectory.
