# Supporting Table S9. Exact realized-richness matching sensitivity

| Quantity | Result | Interpretation |
| --- | ---: | --- |
| Original matched community realizations | 96 | unchanged BASE trajectories |
| Steps per realization | 120 | unchanged BASE horizon |
| Prespecified matching seeds | 6 | 20260907–20260912 |
| Snapshot pairs per matching seed | 11,520 | 96 × 120 |
| Unequal richness pairs after matching | 0 | hard control passed |
| Mean matched target richness | 2.3885 | `min(mainland, island)` at each step |
| Matched target richness range | 0–11 | design output |
| Zero-target snapshot fraction | 10.15% | both matched snapshots empty when either original side is empty |
| Original mean mainland-like richness | 14.4140 | before hard matching |
| Original mean island-like richness | 2.3892 | before hard matching |
| Original mean absolute richness gap | 12.0261 | large baseline realized-richness asymmetry |
| Original non-zero gap fraction | 99.965% | before hard matching |
| Mean-geometry classification | all-positive in 6/6 matching seeds | prespecified mixed-mean gate failed |
| Mixed-sign individual realizations | 51–65/96 | branching persists after exact richness matching |
| Starting-position SS fraction | 0.94–2.21% | additive starting state remains small |
| Community-realization SS fraction | 50.04–55.92% | community realization remains major |
| State × community non-additivity | 42.72–48.51% | relational contingency remains large |
| Additive-sign mismatch | 31.80–36.76% | additive representation misses many cell signs |

**Primary matching seed (20260907):** mean geometry was all-positive; realization classes were 58 mixed, 21 all-positive, 4 all-negative and 13 other. Sum-of-squares fractions were 0.94% starting position, 51.59% community realization and 47.47% state × community non-additivity.

**Decision:** the prespecified full-clear gate failed because mean mixed geometry did not survive exact realized-richness matching. The supported reframe is that realized richness helps position the coarse mean regime, whereas substantial response branching remains conditional on starting state × realized community composition.

This is a synthetic hard control, not an empirical richness manipulation or evidence that richness alone determines natural island responses.
