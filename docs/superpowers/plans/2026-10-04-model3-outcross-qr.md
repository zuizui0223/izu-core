# Exact QR contraction before rank-product core allocation

Do not allocate the expanded donor-core outer recipient-core. First take a
reduced QR of each child factor F=Q R (no singular-value truncation). Contract
R1/R2/R3 directly with both parental cores. The reconstructed joint tensor
must match the prior exact implementation and frozen tensor_births to1e-11.
Signed cores/factors remain valid. QR does not add a biological assumption.

Fix an explicit contraction path before executing it. Calculate the size of
each intermediate from its retained index set and reject over-budget paths.
This bounds explicit einsum intermediates, not BLAS/SVD workspace or full peak
memory. Also budget the raw child factor size and final output; do not pretend
QR guarantees small rank at high resolution. Test both exact paths, a case
whose expanded core exceeds the output cap but QR does not, and rejection of
an oversized intermediate. Keep live-run sources unchanged.
