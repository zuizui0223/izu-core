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
