# Q1-to-Q2 mechanism map and reporting priority

User clarification: the main question is whether investment reduction precedes/follows capacity evolution and whether it can occur without capacity evolution. Historical persistence is supplementary, not the primary biological aim. Existing common-environment results remain fully reported; no additional history experiments are proposed.

## Primary causal chain

Isolation changes visitor arrival, ongoing arrival/loss changes pollen-delivery opportunity, reproductive returns and costs change individual contributions, and inheritance/sampling produce realized investment and capacity evolution. The model does not prescribe a syndrome direction.

| Q1 question | Model counterpart | Evidence and limits |
|---|---|---|
| H1 floral patterns along isolation | Sustained-isolation trajectories and trait-specific endpoints | Completed; abstract investment/capacity/matching, not seven measured traits or four regional reconstructions |
| H2 whether selfing explains floral change | Temporal diagnostics plus matched-founder fixed/evolving capacity intervention | Temporal results complete; intervention running. Temporal order is not mediation. Fixed capacity is not fixed selfing fraction |
| H3 isolation and pollen limitation | Visitor-history audit, fixed-plant exposure assay, pollen-saturation comparison | History and evolved-snapshot assays complete; same-plant environment comparison needed to isolate exposure from compensation |
| H4 traits associated with less pollen limitation | Within-environment trait manipulations and saturation assay | Snapshot differences alone do not isolate trait effects. Accessibility/open-flower traits are not directly implemented |

This is a mechanistic connection, not four claims of direct replication. Q1 motivates the questions but does not calibrate parameters or select successful results.

## Existing diagnostics verified in source

`scripts/model3_island/assays.py::investment_assay` perturbs investment for one focal plant at a time, holding other plants and visitors fixed. It returns the finite-difference derivative of half maternal outcross contribution plus half paternal outcross contribution plus viable selfed offspring. Perturbed states are not inherited and do not modify trajectories. At trait boundaries it uses a feasible one-sided difference. This is a fixed-state contribution diagnostic, not an observed evolutionary rate or invasion test in an infinite population.

`scripts/model3_island/selection.py::investment_invasion_terms` is a different estimand: an analytic rare-mutant gradient in a fixed monomorphic resident at capacity. Its benefit/cost decomposition must not be labelled the exact finite-population assay. It offers a complementary local theoretical result, with explicit assumptions.

`reference_service` uses an invariant21-plant panel with capacity disabled to describe visitor opportunity independently of evolved focal plants. It is not the same as the pollen limitation of an evolved population.

## Interpretation rules for pending controls

- A precisely negative investment change under fixed capacity would show that capacity evolution is not necessary for that change under this intervention.
- A non-significant change is not evidence of no change or proof that capacity evolution is necessary. Report effect estimates and intervals rather than selecting conclusions by significance alone.
- Report both changes from founders and extra far-minus-near differences; investment could decline in both arms for reasons not specific to isolation.
- The difference in isolation effects between modes is conditional on common surviving replicates and is not automatically a universal mediation percentage.
- One fixed capacity0.5 and homogeneous assurance founders limit scope; retain this limitation alongside any positive result.

## Figure priority

Primary: `outputs/figures/model3_persistent_trajectories_20261005/persistent_trajectories.pdf`, actual1,001-state trajectories under maintained isolation, all four setting/mutation combinations. Lines are history means; bands are10th–90th history percentiles, not confidence intervals.

Supplement: `outputs/figures/model3_exposure_comparison_20261005/exposure_comparison.pdf`, common-environment contrast. This does not replace the maintained-isolation or mechanism-control results.
