# Campanula microdonta multichannel scenario example

The companion repository `zuizui0223/shimahotarubukuro` provides a reproducible individual-corolla table from five Izu Islands: Oshima, Toshima, Niijima, Shikinejima and Kozushima (218 corollas). The adapter in this repository converts its `results_shimask_all/corolla_master.csv` into one mean, SE and sample size per island and trait.

```bash
python scripts/prepare_shimahotarubukuro_example.py path/to/corolla_master.csv \
  --output results/shimahotarubukuro_summary.csv
python scripts/run_scenario_workflow.py results/shimahotarubukuro_summary.csv \
  --output results/shimahotarubukuro_scenarios.json
```

The default traits are corolla length, throat width, mouth width, style length, nectar-guide coverage and guide-spot count. They must remain separate in the output even though the scenario score is joint.

## Predeclared scenarios

- `cline`: each trait changes smoothly with island order.
- `bombus_loss_step`: Oshima differs from all four islands lacking the declared Bombus state.
- `cline_plus_step`: a smooth geographic component and an additional Oshima-to-non-Oshima step both contribute.

The workflow reports BIC differences and a simulation recovery matrix under the observed means and SEs. A combined scenario can therefore explain a pattern in which size-related traits vary gradually while guide-related traits shift mainly at the declared boundary.

## Interpretation boundary

The specimen pipeline establishes measured floral-pattern differences, not pollinator causation. The scenario workflow asks which predeclared mathematical response shape jointly approximates the traits and whether the design can recover that shape. Climate, population history, collection date, site structure and other causes remain viable unless independently measured.

## Source provenance

- repository: `zuizui0223/shimahotarubukuro`
- input: `results_shimask_all/corolla_master.csv`
- source table includes island, individual, sexual phase, ruler-calibrated corolla dimensions, entrance-width proxies, style length and guide traits.
- the companion summary reports markedly higher mean guide coverage and spot count for the declared Bombus-present group, while guide contrast and saturation do not show the same binary difference. These channels should not be collapsed into one guide index.
