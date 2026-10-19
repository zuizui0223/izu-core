"""Technical SOURCE-ONLY initial-genotype contract for a NEW Q3 confirmation.

Make the two historical policies start from exactly the same genotypes AND
exactly the same expressed A=0.5 in every original diploid adult, while
retaining segregating assurance alleles. No biological evolutionary paths.
No change to the already executed/started 6x6 exploratory pilot (#596).
"""
from __future__ import annotations

from dataclasses import replace

import numpy as np


def balance_founder_assurance_expression(state, *, seed: int,
                                        fixed_expression: float=0.5):
    """Create pre-assignment allelic variation without t0 phenotype mismatch.

    Requires the specific prospective high-I study's 0.25/0.50/0.75
    symmetric allelic carrier construction. The original founder identity,
    I/matching loci, allele-origin IDs and mutation marks are unaltered.
    Caller gives the SAME returned PlantState to both policies.
    """
    if (type(seed) is not int or seed<0 or seed>=2**32
            or fixed_expression!=0.5):
        raise ValueError("unapproved founder assurance seed or expression")
    a=np.asarray(state.alleles)
    n=len(state.ids)
    if (a.ndim!=3 or a.shape!=(n,3,2) or n<3 or n%3
            or not np.isfinite(a).all()):
        raise ValueError("balanced genetic founders need n>=3 divisible by 3")
    alleles=a.copy()
    first=np.tile(np.array([0.25,0.50,0.75],dtype=float),n//3)
    rng=np.random.default_rng(seed)
    rng.shuffle(first)
    alleles[:,2,0]=first
    alleles[:,2,1]=1-first
    if not (np.array_equal(alleles[:,:2,:],a[:,:2,:])
            and np.all(alleles[:,2,:].mean(axis=1)==0.5)
            and np.unique(alleles[:,2,:]).tolist()==[0.25,0.5,0.75]
            and np.var(alleles[:,2,:])>0
            and np.var(alleles[:,2,:].mean(axis=1))==0):
        raise AssertionError("allelic carrier / phenotype matching invariant failed")
    return replace(state,alleles=alleles)


def verify_pairing(fixed_state,evolving_state,*,fixed_A=0.5):
    """Fail unless policies have EXACT matched t0 genes and A phenotypes."""
    if fixed_A!=.5:
        raise ValueError("unapproved fixed assurance")
    if not np.array_equal(fixed_state.alleles,evolving_state.alleles):
        raise ValueError("historical policy starting genotypes differ")
    if not np.array_equal(fixed_state.ids,evolving_state.ids):
        raise ValueError("starting plant IDs differ")
    for name in ("allele_origin","mutation_flags","birth_years"):
        if not np.array_equal(getattr(fixed_state,name),
                              getattr(evolving_state,name)):
            raise ValueError("source founder provenance differs: "+name)
    if not np.all(evolving_state.alleles[:,2,:].mean(axis=1)==fixed_A):
        raise ValueError("initial expressed A not matched")
    if not np.var(evolving_state.alleles[:,2,:])>0:
        raise ValueError("no heritable A-locus standing variation")
    return dict(source_genotypes_identical=True,
                every_adult_initially_expressed_A=fixed_A,
                standing_A_allele_variance=float(np.var(
                    evolving_state.alleles[:,2,:])),
                initially_expressed_A_between_adult_variance=0.0,
                genotype_carrier_rule="0.25/0.75, 0.5/0.5, 0.75/0.25",
                assertion_scope="GENOTYPE/PHENOTYPE PRE-ASSIGNMENT ONLY; NO biological outcome")
