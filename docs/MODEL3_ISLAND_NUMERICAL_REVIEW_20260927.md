# Numerical and Monte Carlo precision review

Descriptive comparison of existing paired 95% cluster intervals against frozen tolerance; no multiplicity-adjusted equivalence test and no new simulations.

Trait tolerance: 0.01. Occupancy tolerance: 0.02.

Every mode projects founder alleles onto its grid at time zero (simulate.py project_state). Cross-grid differences therefore include initial-state discretization; continuous means no later projection, not continuous initial founders.

All numerical-control populations survive; observed occupancy differences are zero. Existing marginal uncertainty bounds do not establish a population difference smaller than 0.02.

| A | B | Individual B minus A | Paired 95% CI | Assessment | Density mean B minus A |
|---|---|---:|---|---|---:|
| grid_5_grid | grid_5_continuous | -0.005514 | [-0.014726, 0.004064] | unresolved_at_declared_precision | 0.000000 |
| grid_5_grid | grid_7_grid | -0.034408 | [-0.052107, -0.015789] | interval_outside_tolerance | 0.023055 |
| grid_5_grid | grid_7_continuous | -0.044989 | [-0.062926, -0.026837] | interval_outside_tolerance | 0.023055 |
| grid_5_grid | grid_11_grid | -0.031010 | [-0.048786, -0.012113] | interval_outside_tolerance | 0.022963 |
| grid_5_grid | grid_11_continuous | -0.029109 | [-0.046103, -0.011344] | interval_outside_tolerance | 0.022963 |
| grid_5_continuous | grid_7_grid | -0.028893 | [-0.046364, -0.011313] | interval_outside_tolerance | 0.023055 |
| grid_5_continuous | grid_7_continuous | -0.039475 | [-0.056815, -0.022706] | interval_outside_tolerance | 0.023055 |
| grid_5_continuous | grid_11_grid | -0.025496 | [-0.042244, -0.009621] | unresolved_at_declared_precision | 0.022963 |
| grid_5_continuous | grid_11_continuous | -0.023595 | [-0.039550, -0.007684] | unresolved_at_declared_precision | 0.022963 |
| grid_7_grid | grid_7_continuous | -0.010581 | [-0.021906, 0.000170] | unresolved_at_declared_precision | 0.000000 |
| grid_7_grid | grid_11_grid | 0.003398 | [-0.017192, 0.023524] | unresolved_at_declared_precision | -0.000092 |
| grid_7_grid | grid_11_continuous | 0.005299 | [-0.014977, 0.024078] | unresolved_at_declared_precision | -0.000092 |
| grid_7_continuous | grid_11_grid | 0.013979 | [-0.005058, 0.032810] | unresolved_at_declared_precision | -0.000092 |
| grid_7_continuous | grid_11_continuous | 0.015880 | [-0.003845, 0.034111] | unresolved_at_declared_precision | -0.000092 |
| grid_11_grid | grid_11_continuous | 0.001901 | [-0.007943, 0.010793] | unresolved_at_declared_precision | 0.000000 |
| grid_evolving_coarse | grid_evolving_fine | -0.025478 | [-0.042492, -0.008953] | unresolved_at_declared_precision | 0.003668 |

## Interpretation

No individual-control interval is wholly inside ±0.01. Therefore the full quantitative convergence gate is not established. The 7-to-11 grid-projected comparison has a small point difference (+0.003398), but its interval spans -0.017192 to +0.023524. The evolving-assurance refinement has a larger point difference (-0.025478), but its interval overlaps the tolerance boundary; classify it as unresolved rather than a confidently quantified error above 0.01.

Density mean differences are small for 7-to-11 fixed-assurance refinement (-0.0000921) and evolving-assurance refinement (+0.0036682), but these means alone do not prove per-history convergence or convergence for every other treatment.

Of 70 trajectory/cohort rows, 4 meet the summary conditional half-width target, 64 do not, and 2 lack a defined trait-change interval. All conditions retain the frozen 128 histories; the result is reported as imprecise where applicable, with no outcome-selected extra replication.

Large chronology contrasts may be described at the declared finite discretization with their intervals. Universal continuous-trait magnitudes, converged evolutionary optima and field-calibrated island predictions are not established.
