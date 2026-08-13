# Campanula microdonta morphology-only scenario example

The companion repository `zuizui0223/shimahotarubukuro` provides a reproducible individual-corolla table from five Izu Islands: Oshima, Toshima, Niijima, Shikinejima and Kozushima (218 corollas). The adapter in this repository converts its `results_shimask_all/corolla_master.csv` into one mean, SE and sample size per island and morphological trait.

```bash
python scripts/prepare_shimahotarubukuro_example.py path/to/corolla_master.csv \
  --output results/shimahotarubukuro_summary.csv
python scripts/run_scenario_workflow.py results/shimahotarubukuro_summary.csv \
  --output results/shimahotarubukuro_scenarios.json
```

The default traits are corolla length, throat width, mouth width and style length. They remain separate in the output even though the scenario score is joint.

## Evidence boundary

This example is **not** the authoritative three-channel Campanula calibration. The adopted evidence state in `izu-core` remains:

- floral size: continuous erosion;
- multilocus outcrossing: continuous erosion;
- autonomous reproductive capacity: second-transition step.

Nectar-guide and visible-signal traits are excluded from the current adopted evidence state. They contribute no default trait, direction, breakpoint or effect estimate in this example.

The source-locked three-channel calibration is built from `data/inoue_literature_island_traits.csv` and should be interpreted through the repository current-evidence-state workflow.

## Predeclared scenarios

- `cline`: each morphological trait changes smoothly with island order.
- `bombus_loss_step`: Oshima differs from all four islands assigned to the declared post-Oshima regime.
- `cline_plus_step`: a smooth geographic component and an additional Oshima-to-non-Oshima step both contribute.

The workflow reports BIC differences and a simulation recovery matrix under the observed means and SEs. This is useful for asking whether measured morphology is better approximated by a smooth, step-like, or combined response shape.

## Interpretation boundary

The specimen pipeline establishes measured floral-morphology differences, not pollinator causation. The scenario workflow asks which predeclared mathematical response shape jointly approximates those morphology traits and whether the design can recover that shape. Climate, population history, collection date, site structure and other causes remain viable unless independently measured.

The declared regime labels are an analysis scaffold, not evidence that historical loss of a particular pollinator caused a fitted morphology pattern.

## Source provenance

- repository: `zuizui0223/shimahotarubukuro`
- input: `results_shimask_all/corolla_master.csv`
- source table includes island, individual, sexual phase, ruler-calibrated corolla dimensions, entrance-width proxies and style length.
- this adapter intentionally does not promote nectar-guide measurements into the current adopted evidence state.
