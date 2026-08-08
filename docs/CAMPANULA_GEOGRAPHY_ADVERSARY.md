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
