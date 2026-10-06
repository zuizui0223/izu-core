# Pollen saturation assay: compensation and remaining reproductive deficit

## Design and verification

The diagnostic was declared before readout in `data/design/model3_pollen_assay_20261005.json`. It assays all 12,288 saved population snapshots: two settings, two mutation probabilities, 64 histories, eight demographic repeats, two isolation treatments and periods 0/200/400. Period 1000 is excluded because no matching visitor snapshot exists in the frozen history. This is an instantaneous maternal-function counterfactual, not a new evolutionary simulation.

Original case tasks, hashes and frozen biological sources were verified. Reconstructed allele means agree with saved traces. Natural viable output and viable selfed contributions agree with the original reproduction ledger. Independent verification checks all unique design keys, recorded hashes, arithmetic and all 24 summary cells. One zero-mutation delayed/near population is extinct at period400; its deficit is undefined, not zero. Paired contrasts exclude the corresponding pair and disclose this exclusion.

## What is measured

Both deficits are one minus natural output divided by output under saturating outcross pollen at the same plant state. Raw output counts offspring before the model's inbreeding-depression penalty; viable output includes that penalty. They are not interchangeable with field fruit set or a particular meta-analysis effect size.

For delayed selfing, saturation fills all ovules by outcrossing and removes residual selfing. For prior selfing, pre-empted ovules remain selfed; only remaining ovules can receive extra outcross pollen. No resource reallocation, altered male success, recruitment or later generations are included. Therefore the prior and delayed saturation denominators represent different timing interventions.

## Positive-mutation results at period400

| Reproductive setting | Outcome deficit | Less isolated | More isolated | Paired far-minus-near [descriptive 95% interval] |
|---|---|---:|---:|---:|
| Delayed selfing, capacity cost0.5 | Raw offspring | 0.1822 | 0.1571 | -0.0251 [-0.0362, -0.0136] |
| Delayed selfing, capacity cost0.5 | Viable offspring | 0.4635 | 0.5745 | +0.1110 [+0.0940, +0.1283] |
| Prior selfing, capacity cost0 | Raw offspring | 0.0425 | 0.0339 | -0.0086 [-0.0128, -0.0043] |
| Prior selfing, capacity cost0 | Viable offspring | 0.0771 | 0.0633 | -0.0137 [-0.0203, -0.0066] |

All four displayed contrasts have 512 paired estimable populations. Intervals resample 64 history means, 5,000 times; demographic repeats are not treated as independent histories. These are exploratory descriptive intervals without multiplicity correction. All settings, rates and snapshots are retained in the result files.

In the delayed setting, the sign changes with reproductive outcome: stronger isolation has a smaller raw deficit but a larger viable deficit. This is consistent with selfing compensating seed production while the fixed inbreeding penalty leaves a loss in viable offspring relative to sufficient outcross pollen. It does not establish mediation of investment decline by selfing, which still needs intervention controls.

This reversal is not universal: both deficits are smaller in the prior setting, where supplemental pollen cannot replace prior selfing. Timing and capacity cost are jointly different between settings, so neither alone explains their contrast. The depression parameter is fixed at0.5; this assay does not demonstrate purging or evolved inbreeding depression.

## Evidence and claim boundary

- `data/results/model3_pollen_assay_20261005.json`: all summary cells, source and raw-record digests.
- `data/results/model3_pollen_assay_verified_20261005.json`: independent verification and paired history-bootstrap contrasts, including exclusions.
- `outputs/model3_persistent_isolation_20261005/pollen_assay_records.json`: all individual assay records.
- Five assay boundary tests plus six existing temporal/exposure tests pass.

Q1 connection: pollen limitation after compensation need not directly measure visitor scarcity. This model-conditional example supplies a possible process explanation, not a fitted reproduction of Q1 H3/H4, measured field effect size or evidence for flower colour evolution. Numerical deterministic/PDE closure remains outstanding.
