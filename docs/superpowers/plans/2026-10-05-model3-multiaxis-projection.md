# Multiaxis projection admission

Strict second-step single-axis projection failed at rank74 constrained by
projected matrix storage, residual7.82824e-13 vs3.35389e-15. Preserve failure.
Build bases without storing projected unfoldings. Project largest modes
first; accept each direct Frobenius residual<=total/3. Orthogonal mode
projections commute and their residual sum bounds joint projection error.
Materialize final core only once its size and binary contraction path fit
16million cap. No tolerance relaxation or independent-locus approximation.
Tests cover correlated signed tensors and forced two-axis resource case.
Test correction:1000-value cap fit one axis; use500 to truly require two.
Actual probe uses captured strict child1399x2145x100, same total Frobenius
3.3538949820031467e-15, initial rank128 seed997; retain failure.
This is component admission only, not complete strict-step convergence.
