# Exact outcross inheritance component

Use the original two factorized outcross weights for one visitor channel:
donor genotype weights and recipient genotype weights. Represent each as a
full joint Tucker tensor, not independent trait marginals. Sum channels only
in a future integrator; this component returns one channel's offspring.

On each locus, apply Mendelian segregation followed by the existing birth
mutation kernel to each factor matrix. Combine donor gamete factor A and
recipient gamete factor B into unordered child pairs: A_i B_i for homozygotes,
A_i B_j + A_j B_i for heterozygotes. The new joint core is the outer product
of the two input cores, with axes paired by locus. This is an algebraic
reordering of the existing operator. Genotype-class diagonal outcrossing is
allowed, as in the deterministic reference; no finite-individual self-exclusion
is silently added.

TDD: compare unequal-grid, correlated donor/recipient distributions with the
frozen tensor_births, mutation0/.01 and jump/heat_fv. Include signed bases,
Mendelian end cases, mass identity and rejection before exceeding a declared
output-size budget. Absolute error tolerance1e-11. Do not modify live sources.

Ranks multiply and the joint core can become huge. Explicitly bound output
size BEFORE allocation. This component is an exact small-rank building block,
not proof of scalable high-resolution integration. Nonlinear ecological
weighting, channel summation, compression error and rank-growth management are
still required. No additional full-grid biological campaign is launched.
