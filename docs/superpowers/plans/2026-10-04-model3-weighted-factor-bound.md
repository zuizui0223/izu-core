# Pre-contraction ecological weighting

Preserve full joint genotype dependence. Expand separable XY weight in SVD
terms, but never form the duplicated parent core. Compress two raw weighted
factors before contracting. Use a spectral norm telescoping bound with
implicit expanded-core Frobenius norm sqrt(p)*norm(core), converting to L1
by sqrt(number of physical states). Include assurance-factor spectral norm.
Return an absolute error bound, not a positivity guarantee; roundoff excluded.
Tests: direct correlated signed-basis density comparison, preallocation
resource rejection, low-support large physical axes. No live solver edits.
This component is not admitted into full trajectories without separate tests.

Admit XY weight rank reduction first: bound error by omitted singular value
times an absolute-factor upper bound on weighted-state L1. Half absolute
budget for weight reduction, remainder for factor truncation.
Probe all8 archived period200 states embedded onto65nodes: self, donor0,
recipient0 weights. Compare against exact same-input supported density;
bound all off-support output mass. Cap2million values; local relative1e-8.
Record every failure. No full high-grid trajectory admission from this test.
