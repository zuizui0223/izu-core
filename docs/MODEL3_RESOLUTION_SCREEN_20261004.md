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

## Exact selfing component without full joint reconstruction

`scripts/model3_compressed_selfing.py` now applies selfed inheritance and
birth mutation to the three Tucker factors, retaining the same joint core.
It accepts already viable selfed-birth weights; neither fecundity nor
inbreeding depression is added/removed or applied twice. A one-locus transition
maps each unordered parental allele pair to unordered offspring pairs using
the original mutation kernel and independent Mendelian transmissions.

Seven new tests compare its reconstructed small-grid output with the frozen
full-joint `tensor_births` operator (unequal allele grids, correlated components,
signed bases, mutation0/.01 and jump/heat_fv). They agree within1e-11 and
preserve mass. Together with compression/inheritance regressions26 tests pass.
The selfing transform does not grow the Tucker ranks. Its per-locus transition
matrices can still be large; no high-resolution performance claim is made.

This is only a verified linear component. A complete compressed solver still
needs outcrossing, nonlinear ecological weighting, rank/error control and
trajectory validation. It does not change the running production model or
settle the required grid count.

## Exact one-channel outcross component

`scripts/model3_compressed_outcross.py` maps correlated donor and recipient
Tucker distributions into offspring using the frozen Mendelian and mutation
kernels. Six new tests reproduce `tensor_births` on unequal grids, signed
bases, zero/positive mutation and jump/heat_fv. Combined suite32 passes.

Output ranks are products of parental ranks. Parental ranks40 in each mode
would create a1600^3 core, exceeding32GB before factors and temporaries.
An output-value budget rejects such allocation first; it is not a peak-memory
bound. Rank rounding/structured contraction remains necessary. This is only
one visitor channel's already weighted donor/recipient operator, not ecological
weighting, channel summation or a complete scalable population integrator.

## Exact QR contraction improvement

An optional reduced-QR path now factors the three offspring matrices before
contracting the parental cores. No singular directions are discarded; this is
an exact basis change up to floating-point arithmetic. It avoids explicitly
forming the rank-product core. A fixed einsum path is inspected and rejected
if any explicit intermediate exceeds its value budget; raw factor and final
output sizes are also checked. This is not a bound on full peak memory.

Tests compare both paths with the frozen birth operator and include a case
where the expanded4096-value core fails the output budget but the27-value
QR core reproduces it. Combined relevant suite38 passes. High-resolution rank
sizes and nonlinear ecological weighting remain unverified; no full solver
or new ecological result is claimed from this algebraic improvement.

The separate1000-period dense compression diagnostic currently has three
hash-verified completed cases, all passing (delayed-cost near jump/heat_fv,
far jump). Largest path L1 among these is2.00274e-7 and largest trait gap
1.70633e-8. Five cases remain; this partial subset cannot establish the gate.

## Exact ecological weight calculation from joint marginals

The new compressed-ecology component computes phenotype-level pollen affinity,
receipt and saturating seed set from joint assurance-weighted marginals.
Identical allele-pair means are grouped exactly, not binned approximately.
Donor, recipient and viable-selfing weights factor into an access/investment
matrix and an assurance vector. The population distribution itself is still
fully joint, preserving cross-trait associations. Ovule/pollen costs, selfing
timing and inbreeding depression follow the frozen density_step algebra.

Eight tests reconstruct the weighted full genotype counts and compare them
with the original ledger for both settings, visitors present/absent and
fixed/evolving assurance with count-scaled activity, within1e-10. Combined
component/inheritance suite46 passes. Applying these weight functions to
compressed densities, summing birth channels, rank/error control and full
trajectory validation remain unimplemented; there is still no production
compressed solver or demonstrated high-resolution runtime.

## Integrated exact small-grid reproductive step

The components are now joined in `scripts/model3_compressed_step.py`: exact
phenotype weight multiplication (full SVD without truncation), viable selfed
inheritance, every visitor's outcross channel, capacity retention and surviving
adults. Channel sums use QR bases without an expanded block-diagonal core.
All operations retain the joint distribution. The scope is evolving assurance,
all three mutation-active loci and no plant immigration, matching the current
full-mutation campaign; fixed assurance is explicitly rejected in this adapter.

Eight complete-step comparisons match the frozen reference to1e-9 for both
reproductive settings, both mutation operators and visitors present/absent.
Four12-step comparisons additionally verify actual far visitor histories and
adult survival. Fifteen new integration tests and all component regressions
pass (61 total). No frozen running source was modified; both running source
manifests were reverified.

This establishes exact algebra on a small grid, not a scalable solver: no
rank truncation/rounding is performed, ranks can saturate the full grid, and
the explicit-array budget will reject large contractions. Long trajectory
accuracy with controlled rank reduction and high-resolution cost still need
validation before the required grid count can be established.

## Rank rounding with recorded truncation bound

`scripts/model3_core_rounding.py` orthogonalizes the joint factors and performs
HOSVD on the small core, without reconstructing the full genotype array. It
selects retained singular directions using a fixed per-mode error allowance,
then restores mass by core rescaling. The receipt includes an L1 upper bound
from discarded singular-value energy plus rescaling. This analytical bound
excludes floating-point QR/SVD error, which is checked against explicit arrays
in tests with a separate roundoff allowance.

Seven tests pass, including actual rank reduction, measured discrepancy versus
the recorded bound, mass conservation, correlated signed bases, zero state and
invalid tolerances. No negative-entry clipping is performed; this truncation
is not positivity-preserving. For nonnegative input, its L1 bound bounds the
negative output mass in exact arithmetic. A future small-grid trajectory
diagnostic must measure negativity, all accumulated errors and rank growth;
this utility alone does not authorize high-resolution production runs.

## Integrated stagewise-rounding admission in progress

The solver now optionally rounds weighted-parent tensors, inherited births,
sequential channel sums and the retained population. Local rounding receipts
are retained by the caller. A full-step regression matches the frozen model
and checks negative mass; the combined relevant suite has69 passing tests.

A separate predeclared eight-case n5/40-period run now compares this integrated
method with the unchanged reference at every period. It records full-state
L1 error, trait means, mass, negative mass, rank, runtime and all local error
receipts. Numerical/resource failures are recorded rather than retuned away.
This differs from the n9/1000-period diagnostic, which rounds only after a
full dense update. Neither diagnostic alone demonstrates high-resolution
feasibility. No17+ full biological campaign has been started.

## Completed 1000-period dense-roundtrip diagnostic

All eight predeclared n9/history76001 cases completed and pass the original
thresholds across all1000 periods. Maximum trajectory relative L1 discrepancy
is1.0443221e-6 (threshold1e-5), maximum trait-mean gap8.1150344e-8 (threshold1e-6),
and maximum mass gap5.6843419e-14 (threshold1e-5). No occupancy mismatches.
The near/far environmental switch and both reproductive/mutation settings are
included. This is one history, not a population-wide or high-grid error bound.

Verified all case identities,1000 consecutive period records, source hashes,
NPZ hashes and recomputed L1 gaps from saved distributions at200/400/1000.
The complete raw/source bundle is34,058,669 bytes at
`outputs/model3_precision_feasibility/propagation1000_verified.zip`.
Its hash, case-level extrema and source hashes are archived in
`data/results/model3_compression_long_20261004.json`.

Interpretation: truncation after the dense reproductive step at this grid and
tolerance did not materially perturb the measured trajectories. This does NOT
validate the integrated stagewise rounded solver, which inserts approximation
inside nonlinear weighting and mating. That separate n5/40-period experiment
remains running, as does the13-node full-model precision campaign. Required
high-resolution grid size, integrated solver speed/precision and ecological
ABM-density/PDE comparisons therefore remain unresolved.

## Measured integrated-solver performance bottleneck

The n5 admission process remains live. A separate identical first-period
profile (four visitors) took13.97s versus0.00445s for the dense reference;
full-state relative L1 difference3.5354e-15. More than99% of profiled time was
inside the outcross einsum contraction, not ecological weights or rounding.

Three candidate explanations were distinguished: contraction scheduling,
intrinsic rank growth, and matrix-library overhead. A fixed-shape experiment
(seed124, parental ranks12, output ranks15) directly tests scheduling with
identical operands. Default greedy planning selected a single five-operand
contraction. Giving the planner the already allowed2,000,000-value intermediate
budget selected binary contractions, largest intermediate32,400 values.
Measured82.701s versus0.001288s with maximum result difference1.7764e-14;
theoretical FLOPs50.39billion versus11.55million. These single-call timings are
not a claimed full-model speedup or proof of high-grid feasibility.

The tested candidate changes scheduling only. Current live sources are still
untouched. A corrected solver must be tested/run in an isolated source snapshot
while the original frozen admission continues; its results must be distinguished
from the old run. Evidence is in
`data/results/model3_contraction_profile_20261004.json` and the local profile
artifacts. No biological parameters or numerical error tolerances were changed.

## Isolated scheduling fix: integrated admission passed

Copied the hash-verified original admission source archive to an isolated
candidate directory, preserving the live source files. Exactly two solver
lines changed: einsum planning now receives its existing intermediate budget.
The regression first reproduced all-at-once scheduling, then passed. Candidate
tests were run with candidate-local imports/root (an initial parent-repository
import was identified and excluded);70 tests pass in2.08s.

The same n5/40-period/eight-case integrated admission then completed: all8 pass,
total case runtime23.518s. Max full-state L1 error1.3217425e-8, mean-trait gap
1.7097166e-9, mass gap4.1211479e-13, and relative negative mass2.6360477e-11.
All endpoint arrays/hashes were checked, final L1 recomputed, source hashes
verified. Maximum core rank15 still reaches the full diploid-mode dimension;
these results establish small-grid correctness and remove a scheduling
bottleneck, not high-grid efficiency or required allele-node resolution.

Candidate patch/provenance and audited case metrics are retained under
`data/results/model3_fastpath_candidate_20261004.*` and
`data/results/model3_fastpath_admission_20261004.json`. The verified source,
tests and raw outputs are bundled at
`outputs/model3_precision_feasibility/fastpath_candidate_verified.zip` with
hash/size in the result record. Original slow admission and13-node run remain
separate, unchanged computations. Next gates are long-horizon integrated
accuracy and higher-grid numerical/resource checks before production use.

## Integrated long run and symbolic contraction preflight

The corrected isolated solver now runs the same8 cases for1000 periods under
the separately frozen fastpath-long plan. All thresholds and biological inputs
remain fixed. Candidate-local71 tests pass; source hashes and source archive
were created before launch. Session67923; no completed-case claim yet.

A separate allocation-free contraction-shape screen considered allele nodes
9/13/17/33/65, parental rank min(40,diploid-mode-size), and explicit intermediate
budgets2/16/64 million values. These are assumed ranks, NOT measured guarantees.
At that scenario, n9/n13 acquire binary paths at16million; n17 at64million.
n33/n65 do not. The unrounded n65 child core would still contain4.096billion
values. Thus the planner correction does not eliminate high-grid rank growth.
The current2million-value output cap rightly refuses such an allocation.

Raw symbolic paths are in model3_contraction_shape_screen_20261004.json. This
does not authorize raising memory caps blindly or launching17+ biology. A
pre-contraction reduction of child-factor ranks, with a defensible error bound,
is needed for those scenarios before claiming high-resolution feasibility.
