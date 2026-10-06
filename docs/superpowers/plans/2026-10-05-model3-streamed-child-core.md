# Streamed child-core feasibility

Observed65-node second-step child core844x761x45=28,902,780 values exceeds
declared16million-value cap. Do not loosen numerical tolerance or silently
raise memory budget. Separate prototype required; existing runs frozen.

Investigate contraction in bounded output blocks. Build a mode Gram matrix
from blocks, choose a candidate subspace, and directly recompute projected
residual blocks to certify Frobenius residual (no subtraction of nearly
equal squared norms). Convert to physical L1 using orthonormal child bases
and sqrt(number of genotype states). Increase numerical subspace rank only
under that error bound and fixed allocation cap; retain failure if infeasible.
Do not substitute independent loci. A Gram eigenvalue cutoff alone is NOT
a certificate. Measure contraction path costs as well as output allocation;
all-operands fallback may be prohibitively slow despite fitting memory.
First tests must match a fully materialized small tensor, cover nonzero
truncation, resource rejection and correlated/signed inputs. Then capture
actual failing transforms and test their block access without full allocation.
This is a numerical development path, not ecological evidence or admission.

Actual failed-input probe: use captured844x761x45 core operands, blocks
of4 second-axis values (180 unfolded columns),16million per-array cap.
Measured block timings0.015s for width4, no multi-operand fallback.
Test direct Frobenius residual<=1e-14 before biological integration; do
not relax if it fails. This is a component/resource diagnostic only.

Gram-based actual probe FAILED: residual3.78305e-9 at rank467, target1e-14.
Retain this failure. New isolated direct Gaussian sketch plus QR avoids
squaring condition numbers; fixed numerical seed997, rank schedule and
full block residual acceptance unchanged. No power iteration or tolerance
relaxation. Ill-conditioned known-matrix test included. Test same captured
operands, cap16million and residual1e-14; output separate direct_projection.
Numerical randomization is not a biological stochastic process.
