# Full joint distance for compressed trajectory comparison

Represent both states in common orthonormal factor bases using QR of
concatenated factors. Contract each core into these bases, subtract cores
directly, then use Frobenius norm times sqrt(number of physical genotype
states) as exact-arithmetic L1 upper bound. Do not subtract squared norms
or replace joint states by products of marginals. Roundoff excluded.
Tests: dense correlated signed-state agreement, near-equal states1e-10,
allocation rejection, equal locus marginals with different joint structure.
Use later for tolerance and grid comparisons; tests alone establish no
high-resolution trajectory convergence.
