# Exact phenotype-level ecological weights from a joint density

In frozen density_step, affinity depends on access and investment but not
assurance. Pollen discount, ovule assurance cost and prior/delayed selfing
enter through separable assurance functions. Compute the required weighted
access/investment marginals directly from a joint Tucker core and factors.
Group identical allele-pair means exactly; no binning/rounding of phenotypes.

Return donor, recipient and viable-selfing weight functions as an
access/investment matrix times an assurance vector. Preserve the original
affinity normalization, background resource denominator, pollen receipt,
saturating seed set, timing and inbreeding depression. This is not assuming
the joint density factors into independent traits: assurance-weighted
marginals retain its associations.

Before implementation compare reconstructed weighted counts with the frozen
density_step ledger on correlated densities, both reproductive settings,
visitors present/absent, fixed/evolving assurance and count-scaled activity.
Require absolute agreement1e-10. This component does not yet multiply these
weights into compressed tensors or integrate the full dynamics. No live source
files or ecological assumptions change.
