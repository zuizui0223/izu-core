# Bounded child-factor reduction before outcross core contraction

For parental joint cores D,R and child factor matrices F1,F2,F3, the expanded
core is a permutation of D outer R, with Frobenius norm B=||D||F||R||F.
Let Li=||Fi||2 and ei be the spectral residual after truncated SVD of Fi.
Using a telescoping product and ||truncated Fi||2<=Li gives
||offspring-error||1 <= sqrt(N)*B*product(Li)*sum(ei/Li),
where N is the full output tensor size. This is an exact-arithmetic bound;
floating-point errors are separately measured, not included in the formula.

Choose each ei/Li <= absolute_L1_budget/(3*sqrt(N)*B*product(Li)).
Return orthogonal child factors and reduced transforms without building the
rank-product core. Retain full directions when the bound cannot permit
truncation; reject nonfinite/oversized inputs. Zero output is handled exactly.
This is not assuming trait independence, clipping negative entries, changing
mutation kernels or proving low ranks at high resolution.

Tests before implementation: actual small-tensor error versus bound; positive
and signed cores/factors; exact zero; invalid budgets and dimensional mismatch.
No changes to any current live-run source set. A later integrated gate is
required before applying this approximation in biological simulations.
