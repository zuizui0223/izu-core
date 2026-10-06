# Fully integrated rounded solver admission, fixed before outputs

Five allele nodes (original founder support), forty periods, history76001,
near/far, two reproductive settings and jump/heat_fv: eight cases. Same
mutation.01/.05 and founders74001 as the full campaign. One worker/BLAS thread.
Apply joint-core rounding at weighted-parent, inherited-birth, sequential
channel-sum and final retained-population stages. Local relative L1 tolerance
1e-8; explicit intermediate/output budget2,000,000 values. No clipping.

Compare every period with the unmodified tensor density_step on the same
grid/history. Admission: full-path relative L1<=1e-5, mean-trait gap<=1e-6,
mass gap<=1e-5, relative negative mass<=1e-10, no occupancy mismatch and all
eight cases finish. Record every local truncation receipt and empirical full
error separately; their simple sum is NOT a propagated nonlinear error bound.
Record runtime and core ranks. Numerical/resource failures retained as failures,
not silently retried at looser tolerance. Save source archive/hash manifest,
full period metrics and endpoint arrays/hashes. No ecological conclusions from
this coarse grid. Passing admits longer/higher-grid solver checks only.
