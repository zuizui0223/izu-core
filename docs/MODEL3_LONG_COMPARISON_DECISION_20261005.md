# User stop and alternatives to the high-grid long comparison

The user requested stopping the 1,000-update computation, examining alternatives,
and closing this comparison as unresolved if no adequate substitute is feasible.
This supersedes the execution requirement to continue all eight high-grid cases;
it does not turn missing numerical evidence into a successful comparison.
The Ch2 ecological mechanism and poster work remain active.

PID23688 was stopped after checking its command line. Period7 is complete and
its checkpoint was independently matched to the producer arrays; period8 was
unfinished. All files are retained. No automatic restart is planned.

## Evidence and feasible alternatives

| Route | Existing evidence | What it can answer | What it cannot replace |
|---|---|---|---|
| Reuse coarser full-model grids | Only1/32 of the9-to13-node terminal comparisons passed the declared tolerance | Documents unresolved discretization | Positive-mutation ABM versus continuum departure or isolated PDE error |
| Short high-grid comparison | Verified65-node local updates through7 in one case | Local operator and checkpoint consistency | Long-run evolution, accumulated joint error, all-case precision |
| Zero-mutation full model | Common-founder-support checks pass in the completed benchmark | Finite versus deterministic realization on that fixed support | Mutation-enabled continuous-genotype evolution |
| One-locus mutation diagnostic | Completed ABM, exact-jump density and heat-FV comparisons;21-to41 refinement within.005 for terminal means | A bounded example of variation loss and replenishment | Joint evolution of matching, investment and capacity; sustained-isolation main experiment |
| Mutation-kernel spectral analysis | Exact mode factors and refinement diagnostics already completed | Where diffusion approximates allelic mutation | Nonlinear whole-population ecological trajectory error |
| New adaptive or alternative tensor solver / external compute | Not validated as a replacement | Potential future engineering route | A currently available, verified fast completion |

The one-locus heat-versus-jump comparison itself failed the.005 equivalence gate
in the absent-past condition (.007607 at41 nodes). Retain this negative result.
The prior history experiment has200 different-environment periods followed by
800 common periods; it must not be relabelled sustained isolation.

## Decision

There is no currently verified cheap replacement for the original full,
positive-mutation, high-resolution three-locus long comparison. Do not weaken
tolerances, broaden mutation, assume independent loci, or rename a shorter run
as completion. Close this numerical extension as computationally unresolved
under the present implementation and resources, preserving the failed gates.

Retain the completed local selection thresholds, maintained-isolation ABM
trajectories, capacity intervention and pollen/fitness assays as the primary
ecological evidence. Retain the completed fixed-support ABM/density comparison
and restricted mutation diagnostics with explicit scope. The third explanatory
stage concerns genetic accessibility; it is supported by restricted diagnostics,
not a completed full-model long PDE validation. Its title should be a question
or a scoped finding, not a universal explanation of evolutionary arrest.

Sources: MODEL3_FULL_MUTATION_RESULTS_20261004.md;
MODEL3_MUTATION_MEMORY_20261004.md; MODEL3_RESOLUTION_SCREEN_20261004.md;
data/results/model3_grid13_verified_20261005.json;
data/results/model3_slab_seventh65_verified_20261005.json;
data/results/model3_long_run_user_stop_20261005.json.
