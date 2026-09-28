# Independent robustness of the v12 minimal branch generator

## Question

Does the central v12 result—that pre-existing lineage position in functional trait space is the minimal tested generator of within-run response-sign branching—survive an independent stochastic block?

This check was frozen before execution and did not use the 13 external island outcomes, empirical data, or any post-hoc seed/parameter selection.

## Prespecified independent design

- seed: `90260825`
- saturations: `1, 2, 3`
- replicates per saturation: `4`
- lineages per run: `24`
- evolution steps: `120`
- external targets loaded: `false`
- empirical inputs loaded: `false`

The stop rule required accepting the first scientific result from this seed. An initial workflow attempt failed before the simulation started because the wrapper could not import `scripts`; only that import path was corrected. The seed and design were unchanged. Provenance is locked in `data/provenance/abm_v12_branch_generator_independent_robustness_run.json`.

## Result

The independent block **replicated the minimal-generator result**.

| configuration | mixed-sign run fraction | mean within-run branching balance | paired sign changes vs full |
|---|---:|---:|---:|
| full residual | **0.4167** | **0.2917** | — |
| initial trait heterogeneity OFF | **0.0000** | **0.0000** | **44** |
| trait-adjustment heterogeneity OFF | **0.4167** | **0.2847** | 5 |
| assurance-ceiling heterogeneity OFF | **0.4167** | **0.2917** | 0 |

All residual factors OFF again gave zero mixed-sign runs and zero within-run branching balance.

The predeclared decision is therefore:

`replicated_minimal_generator`

## Comparison with the original frozen block

The result is unusually clean because the qualitative boundary is identical in the two independently seeded blocks:

| readout | original v12 block | independent block |
|---|---:|---:|
| full mixed-sign run fraction | **0.4167** | **0.4167** |
| initial-trait-OFF mixed-sign fraction | **0.0000** | **0.0000** |
| full mean branching balance | 0.2569 | 0.2917 |
| initial-trait-OFF mean branching balance | **0.0000** | **0.0000** |

The exact equality of the mixed-sign frequency is not itself the claim and should not be overinterpreted. The important replicated property is the state boundary: branching remains present in the full model and under the other single residual ablations, but collapses when initial trait-position heterogeneity is removed.

## Scientific consequence

The primary simulation claim can now be stated more strongly, while remaining model-internal:

> Across two independently seeded frozen blocks, pre-existing lineage functional-position heterogeneity is the only tested residual factor whose removal eliminates within-run response-sign branching.

This still does not mean that a particular measured floral trait is known to be the real-world causal axis. It establishes the minimal generator **inside the declared ABM**.

Together with the already independent network-context and assurance robustness blocks, the three main mechanistic pieces of the simulation story now each have an independent robustness check:

1. branch generation — independently replicated;
2. network-context sign buffering — independently replicated but bidirectional;
3. assurance magnitude attenuation — independently replicated, with strong sign rescue absent.

No additional seed search is justified for the primary claim. Further simulations should be added only for a new prespecified question, not to improve favorable frequencies.
