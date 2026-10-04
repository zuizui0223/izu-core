# Before additional full runs: resolution and feasibility

The user requested determining necessary resolution before spending on the next
full campaign. The prepared 17-node campaign is therefore pending, not queued
for automatic execution. The already active 13-node run is retained.

## What can be established cheaply

We tested only one-dimensional birth-mutation kernels, with u=.01 and sigma=.05,
on 9,13,17,25,33,49,65,97,129 allele nodes. This does not instantiate millions
of three-locus genotypes and does not change any biological settings.

Reflecting cosine modes have exact decay factors:

- original jump: `1-u + u exp[-(m pi sigma)^2/2]`;
- heat: `exp[-u(m pi sigma)^2/2]`.

Each numerical operator is compared with its own continuum reference after
1,200,1000 birth events. This separates grid error from the fact that jump and
heat are different operators at fixed mutation settings. The screen was fixed
before evaluating its outputs: max absolute error across modes 1–8 <.01 and
central one-birth variance relative error <1%. These are engineering diagnostics,
not a theorem connecting operator precision to terminal ecological trait error.
Boundary starting nodes are included. Modes 16/32 are separately reported.

| Nodes | Jump variance relative error | Jump mode error | Heat mode error |
|---:|---:|---:|---:|
| 13 | 22.80% | .06973 | .13344 |
| 17 | 13.02% | .04227 | .07188 |
| 25 | 5.79% | .01951 | .03077 |
| 33 | 3.26% | .01112 | .01706 |
| 49 | 1.45% | .00499 | .00750 |
| 65 | 0.81% | .00282 | .00420 |
| 97 | 0.36% | .00125 | .00186 |
| 129 | 0.20% | .00071 | .00105 |

The first passing candidates among those tested are jump65 and heat49. This is
NOT proof that at least65 is necessary, or that65 is sufficient, for the full
nonlinear reproductive model. Some mean responses can converge at coarser
resolution; sharp distributions or nonlinear feedback can require more.
Indeed the separate mode32 heat check still has error .02135 at65 nodes and
first falls below .01 at97 nodes. A grid count must always name the quantities
and tolerance it resolves.

## Why not simply launch65 nodes

The current implementation explicitly retains the full joint diploid genotype
distribution and gamete-pair arrays. A transparent lower bound includes only
the genotype allele array (six float64 values/state), one state vector, one
float64 gamete-pair matrix, and one int32 child lookup. It excludes numerous
temporary arrays, sparse matrices, Python mappings and checkpoints.

| Nodes | Diploid genotype states | Lower-bound memory |
|---:|---:|---:|
| 17 | 3,581,577 | 0.46 GiB |
| 25 | 34,328,125 | 4.52 GiB |
| 33 | 176,558,481 | 23.64 GiB |
| 49 | 1,838,265,625 | 250.56 GiB |
| 65 | 9,869,198,625 | 1,357.59 GiB |

These are not peak-memory predictions. Actual needs are higher; even33 nodes
already exceeds this host's approximately16GB total RAM at the lower bound.
The unchanged engine also uses int32 child indices:65 nodes require about9.87
billion genotype IDs, exceeding the2,147,483,647 maximum. Thus the65-node
number above is only a conservative memory floor, not a runnable specification;
more RAM alone would not suffice without correcting that representation.
Blindly launching17 then25 then33 is not a credible plan for resolving the
full positive-mutation continuum model on this implementation.

## Decision and next numerical gate

Do not launch the prepared17 full stage merely because it is implemented.
Retain13 as the already-declared full-model refinement evidence. Before any
new full-grid campaign, establish a feasible representation of the SAME joint
inheritance/reproduction model, or justified access to sufficient resources.
Any numerical compression, quadrature or alternative representation needs its
own approximation-error control and comparison with the verified small-grid
engine. Assuming independent traits, changing the mutation width, or shortening
the biological horizon would not solve the declared problem.

This screen identifies a numerical obstacle and guides a design decision. It
does not conclude that the PDE is biologically invalid or that the ABM–density
gap represents finite-population biology. The full goal remains unresolved.

## Reproduction

`python -m scripts.audit_model3_resolution_screen` with one BLAS thread.
Four tests in `tests/test_model3_resolution_screen.py` pass, checking analytical
end cases, operator distinction, reduced error with refinement, and memory
accounting. Raw metrics and source SHA256 values are in
`data/results/model3_resolution_screen_20261004.json`. All18 operator/grid
combinations are retained, including all three horizons and mode-level errors.

Independent read-only review reproduced heat-FV mode errors with the analytical
discrete eigenvalues within1.72e-10 and verified all archived source hashes.
Passing applies only to the declared modes and sampled horizons, not every
intermediate birth event. No full-grid simulation was launched by this screen.

## Exploratory representation check on completed checkpoints

All six cases completed at this check (first four near/far cases for history76001,
then both near operators for history76002, all delayed/cost.5) were examined.
This is a completion-order subset, not evidence across both reproductive settings.
Case hashes were verified before reading. No original trajectory was modified.

At period1000, retaining probability mass to relative omitted fraction1e-8
required22,189–46,961 of753,571 genotype states. Sparsity is potentially useful,
but omission at a snapshot does not bound errors propagated through selection.
Earlier checkpoints required up to118,049 retained states at the same threshold.

A second probe used a three-mode Tucker/HOSVD representation of the full joint
91x91x91 unordered diploid distribution. This does NOT assume independent traits.
For each mode, SVD truncation used squared discarded singular values at most
`(epsilon * total_mass / 6)^2 / total_state_count`, epsilon=1e-8. The joint tensor
was compressed, reconstructed, negative entries clipped, and mass normalized.
Actual relative L1 error against the original was then checked, not inferred
solely from ranks. The six roundtrips used18,881–37,394 stored floating values
(about20–40 times fewer) and achieved L1 errors1.25e-10–2.32e-10. Tiny negative
mass before clipping was recorded explicitly.

Local exploratory records are in
`outputs/model3_precision_feasibility/checkpoint_compressibility.json` and
`outputs/model3_precision_feasibility/tucker_snapshot_roundtrip.json` with input
hashes. These are snapshot diagnostics, NOT a validated compressed solver. They
currently reconstruct the full tensor to verify error; that alone cannot run
a65-node model. A usable solver must evolve inheritance, mutation, mating and
nonlinear reproduction directly in compressed form, control positivity/mass
and rounding error, and reproduce full trajectories on existing grids before
any high-resolution campaign. Rank growth at higher resolution is unknown.

The next feasible investigation is therefore a small-grid, full-trajectory
equivalence probe of a joint compressed representation, not a blind17-node
campaign or an assertion that high-resolution computation is already solved.

## Forty-period compression propagation admission probe

Completed all eight predeclared nine-node conditions: two reproductive settings,
near/far histories76001, and jump/heat_fv operators. Each step applies the
unchanged dense reproductive operator, then joint Tucker roundtrip with measured
relative L1 error <=1e-8, clipping and mass normalization. An uncompressed path
receives the identical visitors, founders and biological parameters.

All eight pass the preliminary40-period gates. Worst full-path relative L1
discrepancy is3.3495e-7; maximum absolute mean-trait difference2.8312e-8;
maximum mass difference4.974e-14; no occupancy mismatch. The largest discrepancy
occurs in prior-selfing/far/jump. This difference between settings warns against
extrapolating short-run error to1000 periods. Six utility tests pass, including
a correlated joint distribution that an independence approximation cannot retain.

Across times and conditions storage uses3,075–67,347 values versus91,125 original
states. Thus early distributions can require much higher relative ranks than
the previously inspected terminal snapshots. Snapshot compression ratios cannot
be advertised as a trajectory-level speed or memory improvement.

Reproduction: `python -m scripts.audit_model3_compression_probe`, single BLAS
thread. Complete per-period metrics and input/source hashes are archived in
`data/results/model3_compression_probe40_20261004.json`. This admits a subsequent
1000-period diagnostic; it does not establish long-term equivalence or provide
a high-resolution solver. No17-or-higher full-grid simulation was launched.
