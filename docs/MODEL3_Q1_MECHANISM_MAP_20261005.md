# Q1-to-Q2 mechanism map and reporting priority

User clarification: the main question is whether investment reduction precedes/follows capacity evolution and whether it can occur without capacity evolution. Historical persistence is supplementary, not the primary biological aim. Existing common-environment results remain fully reported; no additional history experiments are proposed.

## Primary causal chain

## Resumed completion objective

Finish the independent Model 3 mechanism test connecting isolation, visitor replenishment, pollen delivery, investment returns, autonomous selfing and viable reproduction to all four Q1 questions. Q1 supplies questions, not calibration targets. Historical persistence remains supplementary.

Completion gates, in order:

1. Finish all 8,192 predeclared fixed/evolving-capacity cases; verify source hashes, exact task coverage, fixed capacity and all 2,048 zero-mutation paired negative controls before biological readout.
2. Report investment changes from founders and additional far-minus-near effects separately, with paired-history uncertainty, extinction and all declared settings. Test whether investment reduction occurs without capacity evolution; do not infer necessity from non-significance.
3. Separate H3 exposure at identical plant states from pollen limitation after evolutionary compensation. For H4, declare a same-environment trait intervention before reading its results; keep raw and viable offspring deficits separate and retain selfing timing and costs. Matching is not measured floral accessibility.
4. Complete the numerical admission gates before interpreting ABM-versus-deterministic or diffusion differences biologically. Preserve failed gates and distinguish computational incompletion from scientific non-support.
5. Update the H1-H4 evidence map, figures and poster from verified results, retaining uncertainty and explicit non-correspondence to literal flower colour, seven empirical traits and four regional responses.

Operational resumption on 2026-10-05: both the capacity intervention and checked 65-node gate were confirmed running; neither was restarted. After the user edited the goal, the app record was verified active with the revised H1-H4 mechanism objective. An integrity-only audit checked 6,315 available cases and all 2,048 zero-mutation negative-control pairs, which were exactly identical. Biological readout still requires the complete 8,192-case campaign.

Isolation changes visitor arrival, ongoing arrival/loss changes pollen-delivery opportunity, reproductive returns and costs change individual contributions, and inheritance/sampling produce realized investment and capacity evolution. The model does not prescribe a syndrome direction.

| Q1 question | Model counterpart | Evidence and limits |
|---|---|---|
| H1 floral patterns along isolation | Sustained-isolation trajectories and trait-specific endpoints | Completed; abstract investment/capacity/matching, not seven measured traits or four regional reconstructions |
| H2 whether selfing explains floral change | Temporal diagnostics plus matched-founder fixed/evolving capacity intervention | All8,192 cases and84 estimates independently verified. Investment declines at fixed capacity0.5; evolving capacity is not necessary under this intervention. Temporal order is not mediation. Fixed capacity is not fixed selfing fraction |
| H3 isolation and pollen limitation | Visitor-history audit, fixed-plant exposure assay, pollen-saturation comparison | Same-plant exposure comparison now complete (768 assays): stronger isolation increases saturation deficits at fixed plant state. Evolved-state compensation is a different contrast |
| H4 traits associated with less pollen limitation | Within-environment trait manipulations and saturation assay | Completed exploratory 6,912-case capacity-by-investment intervention, 84 verified contrasts. Higher capacity can compensate deficits; lower deficit alone does not imply more viable offspring. Accessibility/open-flower traits are not directly implemented |

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
