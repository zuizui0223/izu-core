# Does the private return to assurance increase assurance-first outcomes?

Prospective minimal Model 3 diagnostic. Compare native cost-free delayed selfing with a counterfactual that pools the filling probability across all unfilled ovules. At each given state, use the unfilled-ovule-weighted mean A for every plant in the pooled arm. Both assignments retain exactly the same expected totals of selfed seeds and the same outcross matrix evaluated at that state. Descendants in both arms self with their own genotype. Later states, seed totals and extinction may diverge. This removes the within-state advantage of expressing higher A for otherwise identical unfilled ovules; it does not eliminate associations with other inherited traits or isolate drift.

Use 32 independent blocks (one paired future each; founder, visitor and demographic stream seeds 655100+i, 655200+i and 655300+i for i=0..31). Each block starts from the same 48 balanced diploids in both arms, expressed A=0.5, segregating A and I. Use native B8 configuration with direct A cost zero, no pollen discount, no mutation or immigration, one persistent visitor from the block's low-supply visitor set, and 200 updates. Compare assurance increase and investment decrease from each founder mean. Count sustained departures of 0.05 for 20 consecutive censuses, with a five-update tie window. Missing censuses after extinction never qualify. Include all 32 pairs; report all six categories and terminal occupancy.

Primary contrast: paired difference in the proportion classified assurance-first (both traits cross, assurance earlier). Report discordant counts and two-sided exact paired binomial test at 0.05. Secondary descriptive outcome: any sustained assurance increase. A secondary difference alone does not establish an effect on order. No tuning, replacement, expansion or extrapolation to the fraction of historical or wild cases explained.
## Result

All 32 paired blocks completed. The native arm produced assurance-first in 17/32 blocks and the pooled arm in 1/32. The paired difference was +50 percentage points (17 native-only versus 1 pooled-only pair; two-sided exact paired binomial p = 0.00014496). Both traits had to cross for this endpoint. In the other 15 native blocks only assurance crossed. Any sustained A increase occurred in 32/32 native versus 12/32 pooled blocks; all populations remained occupied at update 200.

| Outcome | Native | Pooled |
|---|---:|---:|
| Assurance first | 17 | 1 |
| Investment first | 0 | 0 |
| Near simultaneous | 0 | 1 |
| Assurance only | 15 | 10 |
| Investment only | 0 | 5 |
| Neither | 0 | 15 |

This comparison holds expected population seed output and the outcross matrix constant when both policies are evaluated on the same parental state. The native rule gives each plant its own filling probability; pooling makes that probability common to all plants while retaining differences in unfilled ovules. Keeping the individual return increased the frequency of the complete assurance-first sequence in this setting. Investment crossed in 17 versus 7 blocks, so the order difference includes changes in whether a later investment response occurred. Descendants follow different histories, and the contrast does not decompose the timing difference into a pure acceleration of A. This pilot used one cost-free delayed-selfing regime and restricted standing variation. It does not attribute any fraction of earlier studies or natural island cases to the private return.

[All paired onsets and final sizes](../data/results/chapter2_direct_return_order_pilot_20261112.csv) and [runner](../scripts/chapter2_direct_return_order_pilot.py). Reproduce from the repository root with `python -m scripts.chapter2_direct_return_order_pilot`. The protocol was pushed at c39e98ff before the first biological run.
