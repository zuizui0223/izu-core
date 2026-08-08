# Campanula area/connectivity geography adversary

## Question

Can the three adopted island-side *Campanula* channels be approximated by measured static geography rather than by the staged response profile?

This extends the straight-line mainland-distance audit with island area and local inter-island connectivity while keeping the same evidence boundary.

## Source-locked geography

`data/design/izu_geography_covariates.csv` contains GSHHG 2.3.7 high-resolution level-1 polygon areas for all nine focal islands.

- Izu Oshima, Niijima, Kozushima, Miyakejima, Mikurajima and Hachijojima come from the reviewed `zuizui0223/island` curation registry at commit `79e6be52efb1c434897a52b3b022a19400c2fc2e`.
- Toshima, Shikinejima and Aogashima come from the exact supplemental GSHHG acquisition merged in Izu-core PR #88.

Coordinates are the frozen centroid seeds in `data/design/izu_regime_scaffold.csv`.

## Derived geography axes

The module constructs the axes before joining the Campanula response table:

1. great-circle distance from the frozen mainland geographic anchor;
2. log island area;
3. nearest-island centroid distance among all nine islands;
4. an equal-weight geography-pressure index:

```text
mean(z(mainland distance), -z(log area), z(nearest-island distance))
```

The equal-weight index is declared for adversary testing only. It is not a demographic or colonisation model.

## Candidate response shapes

For each retained channel the audit compares:

- `null`;
- `island_order_cline`;
- `mainland_distance_cline`;
- `log_area_cline`;
- `nearest_island_distance_cline`;
- `geography_pressure_cline`;
- `oshima_to_toshima_step`.

Composite diagnostics compare single-axis models and two-stage hybrids in which flower size and outcrossing follow one continuous geography axis while autonomous reproductive capacity takes the predeclared Oshima-to-Toshima step.

## Current frozen result

Workflow run `31233831728` completed successfully and uploaded artifact `campanula-geography-adversary` (artifact id `9014721609`).

### Channel-level comparison

| channel | order cline AICc | mainland distance | log area | nearest-island distance | geography pressure | Oshima→Toshima step |
|---|---:|---:|---:|---:|---:|---:|
| flower length | 31.78 | 37.44 | 41.81 | 40.26 | 39.34 | 39.01 |
| multilocus outcrossing midpoint | **-10.20** | 0.56 | 4.64 | 3.42 | 2.92 | 1.42 |
| autonomous capsule set | 8.67 | 10.86 | 9.39 | 11.40 | 9.68 | **-16.46** |

Flower length still has only four island observations; its null AICc is 29.94. The morphology channel therefore remains underpowered for a strong shape declaration from AICc alone even though leave-one-island-out error is lowest for island order among these simple continuous axes.

The outcrossing channel is not reproduced well by mainland distance, area, nearest-island distance, or the declared equal-weight geography index. The autonomous-reproduction channel remains qualitatively different: the predeclared second step beats every static geography cline by more than 25 AICc units relative to the best of those geography competitors.

### Composite diagnostic

| composite model | AICc |
|---|---:|
| **two-stage order hybrid** | **5.12** |
| two-stage mainland-distance hybrid | 21.53 |
| two-stage geography-pressure hybrid | 25.80 |
| two-stage nearest-island hybrid | 27.22 |
| two-stage area hybrid | 29.98 |
| single island-order cline | 30.25 |
| null | 36.28 |
| single mainland-distance cline | 48.86 |
| single geography-pressure cline | 51.94 |
| single nearest-island-distance cline | 55.08 |
| single log-area cline | 55.83 |

Thus the current three-channel pattern does not collapse to any of the tested static geography axes. Even when the autonomous step is retained and only the two continuous channels are replaced by the equal-weight geography index, the composite worsens by about 20.7 AICc units relative to the order-based two-stage profile.

## Interpretation boundary

Static area and centroid connectivity are stronger adversaries than island order alone, but they still do not represent demographic history. A poor fit does not reject:

- stepping-stone gene flow or effective migration;
- founder number and source-population identity;
- island age or colonisation time;
- volcanic disturbance and vegetation reset;
- habitat availability;
- climate not represented in the existing three-variable PC1;
- pollinator causation.

The next history layer should therefore use source-locked disturbance/colonisation variables rather than turning the present geography index into a catch-all environmental explanation.

Run:

```bash
python paper/run_campanula_geography_adversary.py
```

The workflow uploads `geography_axes.csv`, channel fits, composite fits and the machine-readable summary.
