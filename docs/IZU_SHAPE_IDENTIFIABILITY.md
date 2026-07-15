# Izu cline-threshold identifiability stage

## Purpose

This stage connects the first public-data acquisition to the biological question
raised by the source-locked *Campanula microdonta* calibration:

- floral size changes as continuous erosion;
- multilocus outcrossing changes as continuous erosion; and
- autonomous reproductive capacity changes as a sharp second-transition step.

Nectar-guide and visible-signal data remain excluded. They contribute no direction,
effect size, breakpoint, or simulation truth.

The next question is not merely whether an island differs from the mainland. It is
whether an independent response is better represented by:

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

The scaffold makes Toshima special by design. It is the immediate post-Oshima unit,
so it is the most direct public-data target for deciding whether a response changes
smoothly along the chain or discontinuously at the second boundary.

The regime labels are working hypotheses. They must not be converted into measured
pollinator effectiveness without source-direct interaction evidence.

## Supplemental public-data acquisition

The previous audit acquired six exact GSHHG polygons:

- Izu Oshima;
- Niijima;
- Kozushima;
- Miyakejima;
- Mikurajima; and
- Hachijojima.

`scripts/acquire_supplemental_izu_gbif.py` adds:

- Toshima;
- Shikinejima; and
- Aogashima.

The script downloads the version-locked GSHHG 2.3.7 high-resolution shoreline,
selects the land polygon containing each declared interior seed point, and queries
GBIF Plantae occurrences within the resulting polygon. It archives the raw records,
query log, source and query vertex counts, selected polygons, species aggregation,
and observation-effort summary.

This is deliberately separate from the global `island` repository. `izu-core` owns
the nine-island universe, extraction outputs, interpretation limits, and subsequent
response-shape analyses.

## Design-power simulation

`channel_id/regime_shape_identifiability.py` generates virtual continuous, binary,
and occupancy responses under each candidate shape. It then selects among the same
candidate models using BIC.

The simulation compares five observation designs:

1. the current six islands plus mainland;
2. the current six islands only;
3. the current design plus Toshima;
4. all nine islands plus mainland; and
5. all nine islands only.

For occupancy, the mainland row is automatically excluded and non-detection is
simulated from the committed island-level occurrence effort. Missing islands use a
declared target effort rather than being treated as perfectly observed.

The output answers design questions such as:

- Can the present geometry distinguish a cline from a second step?
- How much does the immediate post-Oshima Toshima observation help?
- Which hypotheses are structurally unidentifiable without a mainland reference?
- How often can uneven public-record effort manufacture a false threshold?

It does **not** answer which response shape is true in nature.

## Interpretation boundary

The following claims remain prohibited:

- a successful virtual recovery proves staged pollinator loss;
- latitude is a complete environmental/history model;
- occurrence is native establishment;
- non-detection is biological absence;
- the same species label on several islands is an independent evolutionary replicate;
- a regime label is pollinator effectiveness; or
- the unfinished nectar-guide analysis supports a second threshold.

The environmental/history competitor must later use measured climate, island area,
isolation, geology, disturbance history, habitat, and observation process. The
simulation's latitude axis is only an order-correlated adversary used to expose
confounding in the proposed sampling geometry.

## Decision rule for the next empirical stage

After the nine-island artifact is generated:

1. normalize taxonomy and preserve synonym decisions;
2. classify native, introduced, cultivated, transient, and unresolved records;
3. create effort-aware plant occupancy candidates;
4. obtain Apidae/Bombus availability under the same island polygons;
5. assign specialist-like/generalist-like dependency classes before inspecting
   island response shapes; and
6. admit source-direct SI/SC, autonomous reproduction, outcrossing, flower-size,
   accessibility, and effective-interaction channels through their native
   observation models.

The first empirical comparison should report model ambiguity, not force every
lineage into a single island-syndrome trajectory.
