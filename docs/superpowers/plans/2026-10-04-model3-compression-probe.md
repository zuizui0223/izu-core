# Compression propagation diagnostic, fixed before execution

Purpose: measure error accumulation from joint Tucker compression after each
unchanged dense reproductive update. This is NOT a compressed time integrator
and cannot by itself run a high-resolution model.

Fixed initial admission probe: 9 allele nodes, 40 periods, history76001,
near and far arms, assurance_cost and prior_selfing settings, jump and heat_fv;
eight cases. Mutation .01, width .05; original projected founder support and
all biological settings from run_model3_full_mutation. Per-step relative L1
compression tolerance1e-8, independently checked after clipping and mass repair.
Compare against an uncompressed path under exactly the same history.

Report maximum full-path relative L1 discrepancy, absolute mean-trait difference,
mass difference, ranks/storage, negative mass before clipping and runtime.
Admission thresholds: path L1 <=1e-5, trait gap <=1e-6, mass gap <=1e-5,
no occupancy mismatch. Failure is retained; no tolerance tuning to pass.
Forty periods only admit a subsequent 1000-period check; they do not establish
long-time validity, higher-grid feasibility, or a biological conclusion.
The original thirteen-node run and its frozen sources are not modified.
