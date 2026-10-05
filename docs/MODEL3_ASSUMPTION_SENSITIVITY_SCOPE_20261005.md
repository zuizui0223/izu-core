# What the current parameter checks establish

The primary Model 3 is process-based but system-uncalibrated. Its numerical settings are researcher-specified assumptions, not estimates from natural islands. Deriving selection from reproduction avoids prescribing a floral direction, but does not make the result independent of the chosen reproduction, cost, inheritance or visitor-assembly functions.

## Verified coverage of the current main line

| Check | Existing evidence | Scope |
|---|---|---|
| Random visitor and demographic histories | 64 histories x eight demographic repeats in each primary setting | Sampling uncertainty conditional on settings, not parameter robustness |
| Mutation | Rates 0 and 0.01 | Two-point comparison, not a mutation-rate response surface |
| Reproductive setting | Delayed selfing with capacity cost 0.5; prior selfing without capacity cost | Joint change of timing and cost; cannot attribute difference to either alone |
| Timing criterion | Changes 0.025, 0.05 and 0.10, held for 20 updates; ties within five | Readout sensitivity, not sensitivity of the underlying biological trajectory |
| Visitor replenishment | 13 rates, 64 histories, 45 resident states, three snapshots in the local-selection diagnostic; completed positive-mutation evolution at all 13 rates, two settings and eight demographic repeats | Both local selection and realized evolutionary order along the declared rate gradient; fixed plant capacity 48 and no geographic calibration |
| Reciprocal selection | Four existing settings, five controlled communities, three matching positions, 49 x 49 investment/capacity grid | Local state and setting coverage; no global parameter/functional-form proof |
| Population size | Completed zero-mutation bridge includes capacities 48 and 192 | Distinct cohort; cannot substitute for mutation-positive, three-trait long-run convergence |

Sources: `data/design/model3_persistent_isolation_20261005.json`, `docs/MODEL3_PERSISTENT_PROCESS_RESULTS_20261005.md`, `data/design/model3_isolation_selection_gradient_20261005.json`, `data/results/model3_reciprocal_selection_20261005.json`, and `data/design/model3_ch2_bridge_20260927.json`.

## Observed dependence, not just hypothetical concerns

At update 1,000, the delayed/costly setting has far-minus-near investment change -0.141 without mutation versus -0.313 at mutation 0.01. The corresponding capacity effects are +0.034 and +0.100. In the prior/no-cost setting the investment effects are -0.030 and -0.020, and capacity effects +0.004 and +0.002. These are rounded estimates from the primary summary, conditional on paired persistence; the complete intervals and survivor denominators remain in MODEL3_PERSISTENT_PROCESS_RESULTS_20261005.md. The size of the effect clearly is not invariant.

For the prior/no-cost setting with mutation, capacity-first histories number 17, 38 and 54 out of 64 when the readout threshold is 0.025, 0.05 and 0.10; the other histories are near-simultaneous. All these histories reach both events. Therefore 'capacity always starts first' is not supported. The delayed/costly counts are 51, 51 and 57, respectively. This is threshold-crossing order, not infinitesimal onset.

The far treatment has visitors absent in approximately 75.9% of the used snapshots (near approximately 0.73%). In the complete-absence limit with positive investment cost, no visitor-mediated attraction benefit remains. This is an important structural boundary and makes intermediate, intermittently visited conditions essential to assessing generality. The completed 13-rate evolution extension now measures realized order there as well as local selection. All 13,312 cases, 9,984 timing records and 156 endpoint rows were independently reconstructed. This exploratory extension varies replenishment within the two declared reproductive settings; it does not establish robustness across other biological parameters. See MODEL3_REPLENISHMENT_EVOLUTION_RESULTS_20261005.md.

## What remains unestablished

Update after the bounded parameter diagnostic: costs, depression, timing and pollen discount have now been crossed independently for local selection, retaining all 500 combinations and 112,500 state/community cases. All four selection-sign regimes occur, and 25 cases reverse the previously negative capacity-to-investment cross effect. See MODEL3_PARAMETER_SELECTION_RESULTS_20261005.md. This narrows local-selection claims but does not resolve the evolutionary-sequence sensitivity below.

The current main-line evolutionary sequence has not been established across a joint sweep of inbreeding depression, both allocation costs, independent selfing timing, visitor supply/loss/functional composition, initial genetic variance, mutation rate/step size and plant capacity. Replacing functional forms is also a different check from varying their coefficients. Do not claim that current 64 x 8 replication or 144,060 local resident states resolves these gaps.

An older robustness campaign has a stored verified receipt for 30,720 cases and includes depression 0, 0.5, 0.9, fixed selfing 0.1/0.5 and alternative life histories. Its design references older `model3_evolution.py` and `model3_reproduction.py` source hashes. It cannot automatically validate the current inherited-capacity temporal result. Current source equivalence and outcome-specific transfer would need verification before using it for that claim. Here only the design and stored receipt were inspected; the old campaign was not reverified or rerun.

The proper next check is a bounded sensitivity design for the ecological claims, preserving the frozen main experiment: first map analytical selection signs and their boundaries over costs and depression; then use predeclared finite-model contrasts on both sides of those boundaries to test temporal order. Report sign, order, persistence and magnitude separately and retain reversals and null regions. No new numerical ranges or confirmatory status are implied by this recommendation. The stopped high-resolution 1,000-update calculation remains stopped.
