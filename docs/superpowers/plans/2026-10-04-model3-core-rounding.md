# Rank reduction without reconstructing the full joint distribution

Orthogonalize factors by exact reduced QR, transform the joint core, then
perform HOSVD on that small core. Retain each mode's singular values such
that discarded squared sum <= (epsilon*mass/(8*sqrt(3*N)))^2, where N is the
full joint state count. No full genotype tensor is constructed.

The HOSVD projection has L2 truncation bound sqrt(sum of discarded squared
singular values), hence L1 bound sqrt(N) times that. Restore original mass
by rescaling the core; add the rescaling L1 bound using sqrt(N)*||core||_F
of the reconstructed orthogonal representation. Reject if total bound exceeds
epsilon*mass. These are analytical truncation bounds in exact arithmetic;
floating-point QR/SVD/contraction error is separate, checked empirically.

Do not clip negative reconstructed entries invisibly. The method is not
positivity-preserving: if its input was nonnegative, the truncation L1 bound
also bounds any negative output mass, excluding roundoff. Future trajectory
validation must measure negativity directly on a resolvable grid before use.

Tests: actual full-array discrepancy below bound plus roundoff allowance,
mass preservation, rank reduction for nearly rank-one correlated input,
zero state and invalid tolerance rejection. This is a numerical utility, not
automatic approval of high-grid integration. Do not change running sources.
