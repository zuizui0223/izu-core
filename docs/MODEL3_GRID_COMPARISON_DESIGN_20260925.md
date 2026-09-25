# Prospective matched individual/distribution comparison

This supplements, rather than replaces, the continuous-founder baseline and
assurance campaigns. No outcomes from this new campaign have been inspected.
Q1 remains inspiration only. This is a discrete-time density comparison, not a PDE.

## Numerical design

Run400 reproductive seasons with the SAME founder draws and visitor history
for the individual and deterministic density arms of each pair. Nearest-node
project the founder alleles; initialize the density arm from their exact
empirical genotype frequencies. The density arm retains stochastic community
assembly, but removes demographic sampling and the finite-population individual
diagonal pollen exclusion. Thus discrepancies are finite-population effects,
not a pure estimate of genetic drift alone. Use exact Mendelian inheritance in
both arms. Never use uniformly weighted unordered genotypes.

Primary:3allele nodes per locus x2mainland/full-island environments x2adult
survivals(0,0.75) x2starts(0.3,0.7) x2controls(selected,neutral) x2capacities(48,192)
x64seed blocks =2048paired trajectories. Refinement:4nodes, identical settings,
first16seed blocks =512paired trajectories. Total2560pairs. All seeds follow
104729+7919*i. Selfing0.5, depression0.5; other reproductive settings fixed at
baseline. This does not establish the comparator over other assurance regimes.

Checkpoints10/40/50/100/200/400 follow the prior calendar/replacement-time
interpretation. Annual/perennial contrast includes baseline effort scaling;
do not call it longevity alone. Increasing capacity also scales background loss.
These are standing-variation trajectories, not geological reconstructions.

## Predictions and precision

No universal floral direction or finite-population persistence is predicted.
Annual zero-reproduction causes immediate extinction in both formulations;
positive deterministic density may survive arbitrarily near zero where an
individual population cannot. Do not call positive density empirical persistence.
Compare mass and mean traits at matched checkpoints, conditional on positive
density and living individual populations. Retain unconditional individual
extinction and all paired denominators. Density extinction means exactly zero;
report near-zero values as numbers, not thresholded biological extinction.

The64independent histories provide a worst-case approximate95%binomial margin
of12.25percentage points. They support a bounded numerical comparator, not
precise rare-extinction probabilities. Report Monte Carlo errors explicitly;
16refinement histories diagnose discretization only. Compare3vs4nodes on the
same16seeds; a grid discrepancy invalidates a grid-independent interpretation,
and must not trigger silent retuning. Do not pool correlated arms as replicates.

## Execution and admission

Freeze case lists and all executable source hashes before run. Save both
trajectories, reproductive ledgers, exact initial/final genotypes, and case
metadata. Verify every case against freeze, nonnegative density no greater
than one, initial moment equality, support conservation, finite-population
ledger identities, and one exact replay per artifact. Distinguish numerical
failure, grid sensitivity and ecological outcomes. Preserve completed outputs.

Implementation: `scripts/model3_grid_comparison.py` is a declared forward port
of the frozen robustness lifecycle with only founder projection and parallel
density updates added; reject unsupported parameter settings. The runner is
`scripts/run_model3_grid_comparison.py`. Focused tests cover matched initial
moments, shared community history, zero-pollen extinction, and parameter guards.
Terminal validation and summary must precede scientific claims. Existing
unvaried source-pool geometry and fitness-cost limitations remain in force.
