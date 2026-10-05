# Visitor environment changes investment returns without capacity evolution

All768 declared assays completed and passed step-halving checks for every focal plant. Source archive/current hashes, full design keys,48-individual arrays, summary gradients, and initial near/far equality were verified before readout. Existing assay/pollen tests:12 passed.

Each assay uses the same48 plants with the original matching/investment variation and fixed selfing capacity0.5. These plants do not evolve. Only visitor exposures from the frozen near/far histories at indices0/200/400 change. The label400 refers to the visitor-history snapshot, not400 generations of plant evolution in this diagnostic.

For each focal plant, investment is perturbed while other plants remain fixed. The measured derivative is half maternal outcross contribution plus half paternal outcross contribution plus viable selfed offspring, per unit investment. It is a local contribution derivative, not a realized evolutionary change or a physiological cost measured independently.

## Visitor snapshot400: identical plants, different environments

| Setting | Quantity | Less isolated | More isolated |
|---|---|---:|---:|
| Delayed selfing; capacity cost0.5 | Mean total contribution derivative | +0.5793 | -0.7004 |
| Delayed selfing; capacity cost0.5 | Fraction of focal derivatives negative | 0.2051 | 0.9775 |
| Delayed selfing; capacity cost0.5 | Raw pollen-saturation deficit | 0.3901 | 0.4948 |
| Delayed selfing; capacity cost0.5 | Viable pollen-saturation deficit | 0.5852 | 0.7423 |
| Prior selfing; capacity cost0 | Mean total contribution derivative | +0.0650 | -0.8228 |
| Prior selfing; capacity cost0 | Fraction of focal derivatives negative | 0.4782 | 0.9948 |
| Prior selfing; capacity cost0 | Raw pollen-saturation deficit | 0.3901 | 0.4948 |
| Prior selfing; capacity cost0 | Viable pollen-saturation deficit | 0.5202 | 0.6598 |

Mean received outcross pollen is25.3793 versus1.0534 in both settings. The paired far-minus-near total derivative difference is-1.2797 [descriptive95% interval -1.4353,-1.1231] in the delayed setting and-0.8878 [-0.9928,-0.7815] in the prior setting. Intervals resample64 paired visitor histories, not individual plants. All snapshots and metrics remain reported in the summary JSON; no multiplicity correction is applied.

The local direction can therefore shift toward lower investment without changing selfing capacity or the plant state. This supports an environmental-return pathway in the declared model, independently of capacity evolution. It does not prove that visitor richness alone causes the shift: richness and composition change together. Nor does it establish how much investment actually evolves; the matched-founder evolutionary intervention remains running.

The cost coefficient is unchanged. Do not describe this as isolation increasing physiological cost. Instead, the net return to maintaining investment falls under these visitor conditions. Outcross contribution derivatives also fall (delayed1.6523 to0.0854; prior0.9361 to0.0484), but these derivatives themselves include the model's allocation costs; they are not a pure cost-free benefit decomposition.

## Relation to Q1

This fixed-plant result connects environmental pollen limitation (H3) with a possible investment pathway beyond evolving selfing capacity (H2). Evolved-snapshot assays answer a different question because plants have already compensated. H1 endpoints and the pending intervention establish realized trajectories. No direct replication of flower colour, accessibility, H4 field coefficients or regional responses is claimed.

Evidence: `data/results/model3_fixedplant_returns_20261005.json`, `data/results/model3_fixedplant_returns_summary_20261005.json`; raw768 records and individual derivative arrays under `outputs/model3_fixedplant_returns_20261005`. Every case uses the frozen source archive; no main-model biological rule changed.
