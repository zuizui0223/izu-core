# Numerical addendum: conservative birth heat PDE

The originally declared node11/21/41 heat-kernel point projection failed the .005 refinement criterion; on node11 its small mutation step is rounded away. All original88cases are retained with source commit877f213. This is numerical failure, not a biological null.

Add a conservative finite-volume no-flux heat semigroup for the same diffusion coefficient u*sigma^2/2. Check conservation, positivity, heat eigenmode and semigroup/time consistency. Run all original density cases at11/21/41 with this scheme. If41-versus21 mean difference exceeds.005, run81nodes for the positive-mutation common-environment histories only; do not alter ecological parameters. Report any unresolved approximation gap. Exact-jump and ABM results are not rerun or reclassified. This addendum is fixed before reading finite-volume biological results.
