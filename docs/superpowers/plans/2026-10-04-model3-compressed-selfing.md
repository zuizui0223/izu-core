# Exact local selfing transform on a joint Tucker density

Purpose: implement the linear selfed-offspring inheritance/mutation operator
directly on Tucker factors, without constructing the full three-locus density.
This is only one part of the future solver; nonlinear fecundity, outcrossing,
compression rounding and positivity control are not solved by it.

For one parent's unordered allele pair(a,b), the mutated gamete probabilities
are v=(K[a,:]+K[b,:])/2, where K is the existing birth-mutation matrix.
The offspring unordered pair(i,j) has probability v_i^2 when i=j and
2*v_i*v_j otherwise. This gives a row-stochastic local operator L.
For joint tensor X=core times factors U1,U2,U3, the selfed joint offspring
tensor uses the SAME core and factors L1.T@U1,L2.T@U2,L3.T@U3.
This preserves associations represented in the joint core; it does not assume
independent traits. Input weights are already viable selfed offspring counts;
inbreeding depression must not be applied a second time.

Tests before implementation: unequal allele axes, correlated joint inputs,
zero/positive mutation and jump/heat_fv, direct comparison with frozen
tensor_births using zero outcrossing. Require absolute difference<1e-11 and
mass agreement. Validate transition dimensions, stochasticity and finiteness;
allow signed Tucker factors. No production full-grid campaign is authorized
by these unit tests. All existing frozen model files remain unchanged.
