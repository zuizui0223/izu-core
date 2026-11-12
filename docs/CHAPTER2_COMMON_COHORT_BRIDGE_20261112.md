# Common-cohort bridge from assurance to floral response

Prospective descriptive bridge to R1-R5. Use the same 32 synthetic founding populations, one visitor identity per block, and the same paired random seeds as the [private-return pilot](CHAPTER2_DIRECT_RETURN_ORDER_PILOT_20261112.md). Native Model 3 delayed selfing with no direct assurance cost, mutation or immigration. Cross assurance expression (fixed at 0.5 or evolving), activity (0.4 or 1.6, one visitor, same identity and other configuration), and ovule budget (8 or 4.5). Follow 80 updates. From each endpoint move the complete population to the same destination for 40 updates (one visitor optimum 0.7, activity 1.6, budget 8, evolving expression in both histories). This standardizes the destination, omitting a dispersal bottleneck. An extinct population stays extinct. Retain all 256 histories. This second diagnostic reuses pilot blocks and part of the low-activity native histories.

Record founder and endpoint genetic means of A, I and M, expressed A, terminal size, last-ten-update selfed share of realized local recruits, occupied high-I support (maximum allele at least the founder mean I), and post-transfer changes in I and distance of M to 0.7. Count exact investment polymorphism at entry. For occupied source populations compare the average maternal seed return per unit A at fixed state (mean unfilled ovules times viable-self fraction) in updates 0-9 and 70-79. Report actual changes in genetic A separately. This local slope does not measure the causal benefit of moving a gain earlier. Report number of qualifying intervals and survivors.

Within each budget compare founder-relative I with A fixed, and compression as (high-activity minus low-activity I under fixed expression) minus the same gap under evolving assurance, using all complete blocks and reporting their number. At each service and budget count paired surviving policy histories with close final genetic I (absolute difference <=0.025) but distinct final expressed assurance (>=0.05 difference) or realized selfed share (>=0.10). These are descriptive, threshold-specific model comparisons of allocation, capacity and mating, not observations of floral morphology. Treat occupancy and occupied-with-support as all-start outcomes; missing traits after extinction remain missing. Report transfer changes among survivors and identify shared donors. No significance tests or favourable condition selection.

## Matched source environments

I is a genetic allocation trait. Gap compression uses four occupied endpoints per founder. Near-equal I and distinct A or realized selfing use the predeclared cutoffs and the same two occupied policy endpoints. Late selfing shares require observed recruits.

- B=4.5: complete blocks 32/32. Mean fixed-policy I change at low/high service +0.0189/+0.0981; mean high-minus-low gap fixed +0.0793, evolving +0.1012, compression -0.0219.
  - Activity 0.4: 6/32 pairs had close I; 6 also differed in expressed A, 1 also differed in selfed recruitment share.
  - Activity 1.6: 15/32 pairs had close I; 14 also differed in expressed A, 1 also differed in selfed recruitment share.
- B=8: complete blocks 32/32. Mean fixed-policy I change at low/high service +0.0306/+0.0981; mean high-minus-low gap fixed +0.0676, evolving +0.1043, compression -0.0367.
  - Activity 0.4: 5/32 pairs had close I; 5 also differed in expressed A, 1 also differed in selfed recruitment share.
  - Activity 1.6: 15/32 pairs had close I; 14 also differed in expressed A, 1 also differed in selfed recruitment share.

## Early and late maternal returns; persistence, standing variation and destination responses

Gains are mean expected viable seeds per unit increase in A at fixed state. Early and late averages and genetic A changes below use the same surviving populations with two complete windows. Genetic A is latent in the fixed-expression policy. Source survival, source survival with high-I support, and destination survival use all 32 starts in each row. The final two columns are mean changes among destination survivors; positive matching gain indicates movement towards 0.7.

| B | Activity | Policy | Complete windows | Gain early / late | Genetic A change early / late | Alive at 80 | Alive with support | Polymorphic I among alive | Alive at 120 | Transfer I change | Matching gain |
|---|---|---|---:|---|---|---:|---:|---|---:|---:|---:|
| 4.5 | 0.4 | evolving | 32 | 1.726 / 1.687 | +0.184 / +0.000 | 32 | 19 | 18/32 | 32 | -0.0104 | +0.0054 |
| 4.5 | 0.4 | fixed | 32 | 1.728 / 1.617 | -0.005 / -0.001 | 32 | 22 | 17/32 | 31 | -0.0146 | +0.0097 |
| 4.5 | 1.6 | evolving | 32 | 1.130 / 0.805 | +0.079 / +0.007 | 32 | 31 | 13/32 | 32 | -0.0120 | +0.0191 |
| 4.5 | 1.6 | fixed | 32 | 1.137 / 0.768 | +0.011 / +0.003 | 32 | 31 | 14/32 | 31 | -0.0069 | +0.0102 |
| 8 | 0.4 | evolving | 32 | 3.071 / 3.013 | +0.186 / +0.000 | 32 | 19 | 19/32 | 32 | -0.0150 | +0.0059 |
| 8 | 0.4 | fixed | 32 | 3.076 / 2.836 | -0.002 / -0.015 | 32 | 24 | 16/32 | 31 | -0.0065 | +0.0134 |
| 8 | 1.6 | evolving | 32 | 2.009 / 1.431 | +0.079 / +0.007 | 32 | 31 | 13/32 | 32 | -0.0120 | +0.0191 |
| 8 | 1.6 | fixed | 32 | 2.022 / 1.365 | +0.011 / +0.003 | 32 | 31 | 14/32 | 31 | -0.0069 | +0.0102 |

## Interpretation and relation to the five results

The same cohorts link the stages, with different outcomes at each stage. For R1, fixed-policy I at low activity was lower than at high activity but on average higher than at founding: a spatial contrast and a temporal decline are distinct. For R2 the service gap widened at both budgets. The earlier fresh-founder narrowing cannot be generalized to these persistent-visitor settings. This bridge changes more than one feature of the earlier experiments and does not identify why the sign differs. For R3 the early genetic response to assurance at low activity exceeded the late response even though the maternal marginal return was similar. This distinction separates the size of a seed benefit from the ability to realize further genetic change. The earlier density-ABM threshold comparison and matched prediction scores belong to their original designs.

For R4 every source survived; at low activity fewer evolving histories retained the high-I target than fixed histories. This setting provides no source survival contrast. For R5 the same populations, transferred intact, sometimes improved their visitor match on average while mean investment declined. Support for a founder-relative target, polymorphism and actual destination response remain separate quantities. The earlier registered resource interaction and exploratory seed-cohort transfer keep their own estimates. Numerical similarity of different blocks or budgets never supplies extra independent founders.

Across policies, similar allocation sometimes accompanied different assurance capacities; a ten-point difference in realized selfed recruitment was less frequent among those close-I pairs. These are comparisons at the same service level. They do not demonstrate that compression between environments hides a mating difference: compression was absent here. No floral size, shape or gene flow was measured.

[Full endpoints](../data/results/chapter2_common_cohort_bridge_20261112.csv), [native bridge runner](../scripts/chapter2_common_cohort_bridge.py), [table reproduction](../scripts/report_chapter2_common_cohort_bridge.py). Design frozen at 9cfd38dd before execution.
