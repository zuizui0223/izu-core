"""Match A/I single-trait access exactly while varying within-parent co-carriage.

Design-only construction: sixteen *synthetic* t0 source profiles made of twelve
four-plant phenotype strata. It is not a biological Model3 trajectory, a
natural source-population sample, a linked-locus model or a causal evolution test.
"""
from __future__ import annotations

import json
import numpy as np

from scripts.model3_island import reproduction, types
from scripts.audit_chapter2_native_founder_source_20261014 import ordered_ids, native_gate
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    CONTEXTS, ledger_parity, original_context, original_fixture,
)
from scripts.audit_chapter2_independent_synthetic_source_pools_20261014 import (
    POOL_COUNT, source_state as fresh_synthetic_source,
)
from scripts.audit_chapter2_founder_F1_conditional_moments_20261014 import (
    conditional_f1_moments,
)

OVERLAPS=(0,3,6,12)
STRATA=12
COPY_PER_STRATUM=4
WIDTH=.0625
GROUP_SALT="izu-core-pr512-balanced-phenotype-fourfold-source-no-biology-v1"


def balanced_source(pool:int)->types.PlantState:
    """Deliberately repeat each sampled synthetic phenotype four times."""
    native_gate()
    if type(pool) is not int or not 0<=pool<POOL_COUNT:
        raise ValueError("Unregistered synthetic phenotype source")
    original=fresh_synthetic_source(pool)
    # Copy only the adult phenotype; retain distinct synthetic individual IDs.
    prototypes=original.alleles[::COPY_PER_STRATUM,:,:]
    if prototypes.shape!=(STRATA,3,2):
        raise ValueError("Artificial phenotype source has wrong dimensions")
    alleles=np.repeat(prototypes,COPY_PER_STRATUM,axis=0)
    state=types.PlantState(
        alleles=alleles, allele_origin=original.allele_origin,
        mutation_flags=original.mutation_flags, ids=original.ids,
        birth_years=original.birth_years,
    )
    if (len(state.ids)!=48 or not np.all(state.alleles[:,:,0]==state.alleles[:,:,1])
            or not np.all(state.alleles[:,2,:]==.5)):
        raise ValueError("Artificial quartet adult phenotype construction failed")
    return state


def balanced_cocarriage(base:types.PlantState,pool:int,m:int)->types.PlantState:
    """Exactly one A and one I segregating parent in *each* phenotype quartet.

    Number of co-carrier individuals m changes, without changing the total
    or the grouping/parental-return-weight distribution of each trait.
    """
    if (type(m) is not int or m not in OVERLAPS or type(pool) is not int
            or not 0<=pool<POOL_COUNT or not np.array_equal(base.ids,np.arange(48))):
        raise ValueError("Unregistered quartet co-carriage treatment")
    original=balanced_source(pool)
    if not np.array_equal(base.alleles,original.alleles):
        raise ValueError("Artificial source phenotype reference drift")
    ranked=ordered_ids(np.arange(STRATA,dtype=np.int64),pool,GROUP_SALT)
    both=set(map(int,ranked[:m]))
    A=np.array([4*g for g in range(STRATA)],dtype=np.int64)
    I=np.array([4*g+(0 if g in both else 1) for g in range(STRATA)],dtype=np.int64)
    if len(set(A)&set(I))!=m:
        raise AssertionError("Artificial co-carrier overlap mismatch")
    a=base.alleles.copy()
    for locus,idx in ((2,A),(1,I)):
        means=base.alleles[:,locus,:].mean(axis=1)
        a[idx,locus,0]=means[idx]-WIDTH
        a[idx,locus,1]=means[idx]+WIDTH
    origins=base.allele_origin.copy()
    for locus in (1,2):
        origins[:,locus,:]+=100_000_000_000
    state=types.PlantState(alleles=a,allele_origin=origins,
                           mutation_flags=base.mutation_flags,
                           ids=base.ids,birth_years=base.birth_years)
    if (not np.array_equal(state.alleles.mean(axis=2),base.alleles.mean(axis=2))
            or not np.array_equal(state.alleles[:,0,:],base.alleles[:,0,:])
            or not np.array_equal(state.ids,base.ids)):
        raise ValueError("Hidden segregation altered initial parental phenotypes")
    return state


def joint_pre_mutation_segregational_deviations(
    state:types.PlantState, ledger:types.Ledger
)->dict:
    """Probability both offspring loci deviate from their parent-pair midpoints.

    Original native Model3 independently chooses maternal/paternal homolog
    copy at M/I/A. For homozygote carriers=0, one heterozygous parent=1,
    two equal-halfwidth heterozygous parents=0.5 probability of a nonzero
    offspring midpoint deviation at each locus.
    """
    n=len(state.ids)
    if n!=48 or not isinstance(ledger,types.Ledger):
        raise ValueError("Full artificial phenotype source and original ledger required")
    a=state.alleles
    hA=(a[:,2,0]!=a[:,2,1]).astype(np.int64)
    hI=(a[:,1,0]!=a[:,1,1]).astype(np.int64)
    for locus,h in ((1,hI),(2,hA)):
        d=a[:,locus,1]-a[:,locus,0]
        if (int(h.sum())!=12 or
                not np.array_equal(d,np.where(h>0,2*WIDTH,0.))):
            raise ValueError("Only matched symmetric allele segregation admitted")
    parent=ledger.outcross.copy()
    parent[np.diag_indices(n)]+=ledger.self_viable
    total=float(parent.sum())
    if not np.isfinite(total) or total<=0:
        raise ValueError("Empty/nonfinite parental lottery")
    prob=parent/total
    countA=hA[:,None]+hA[None,:]
    countI=hI[:,None]+hI[None,:]
    qA=np.where(countA==2,.5,(countA==1).astype(float))
    qI=np.where(countI==2,.5,(countI==1).astype(float))
    pA=float(np.sum(prob*qA))
    pI=float(np.sum(prob*qI))
    joint=float(np.sum(prob*qA*qI))
    if (min(pA,pI,joint)<-1e-15 or joint>min(pA,pI)+1e-14 or
            abs(float(prob.sum())-1.)>1e-12):
        raise ValueError("Original parental Mendelian co-segregation integral invalid")
    return {
        "p_nonzero_A_segregation_relative_to_parent_midpoint":pA,
        "p_nonzero_I_segregation_relative_to_parent_midpoint":pI,
        "p_joint_nonzero_A_and_I_segregation":joint,
        "excess_joint_probability_over_marginal_product":joint-pA*pI,
    }


def source_only_audit()->dict:
    """16 synthetic sources × 4 co-carrier overlaps × 3 native pollinator arms."""
    orig=original_fixture()
    contexts={context:original_context(orig,"main",context) for context in CONTEXTS}
    rows=[]
    for pool in range(POOL_COUNT):
        base=balanced_source(pool)
        for c,(config,vis) in contexts.items():
            reference=None
            for m in OVERLAPS:
                source=balanced_cocarriage(base,pool,m)
                ledger_parity(base,source,config,vis)
                ledger=reproduction.reproduce(source,vis,config)
                mm=conditional_f1_moments(source,ledger)
                j=joint_pre_mutation_segregational_deviations(source,ledger)
                values={
                    "expected_single_offspring_mean_M_I_A":mm["expected_single_offspring_mean_M_I_A"],
                    "first_offspring_variance_M_I_A":mm["first_offspring_variance_M_I_A"],
                    "segregation_contribution_M_I_A":mm["segregation_contribution_M_I_A"],
                    "parent_pair_contribution_M_I_A":mm["parent_pair_contribution_M_I_A"],
                    "marginal_A_segregation_event_probability":j["p_nonzero_A_segregation_relative_to_parent_midpoint"],
                    "marginal_I_segregation_event_probability":j["p_nonzero_I_segregation_relative_to_parent_midpoint"],
                }
                if reference is None:
                    reference=values
                else:
                    for key in values:
                        if not np.allclose(values[key],reference[key],atol=2e-14,rtol=0):
                            raise ValueError("Marginal F1 moments drifted across matched co-carrier treatment: "+key)
                if c==0:
                    if (abs(j["p_nonzero_A_segregation_relative_to_parent_midpoint"]-.125)>1e-14
                        or abs(j["p_nonzero_I_segregation_relative_to_parent_midpoint"]-.125)>1e-14
                        or abs(j["p_joint_nonzero_A_and_I_segregation"]-
                            (0 if m==0 else 1/16 if m==12 else j["p_joint_nonzero_A_and_I_segregation"]))>1e-14):
                        raise ValueError("Unvisited source-only Mendelian probability formula invalid")
                rows.append({"artificial_source_pool":pool,
                             "visitor_context":c,
                             "co_carriers_m":m,
                             "parent_return_identical":True,
                             "marginal_F1_moments_matched_within_pool_and_context":True,
                             "expected_first_offspring_variance_A":mm["first_offspring_variance_M_I_A"][2],
                             "expected_first_offspring_variance_I":mm["first_offspring_variance_M_I_A"][1],
                             **j})
    if len(rows)!=POOL_COUNT*len(CONTEXTS)*len(OVERLAPS):
        raise AssertionError("Not all source × ecology × co-carrier comparisons covered")
    return {
        "schema":"chapter2_original_model3_cocarriage_with_matched_F1_marginals_v1",
        "status":"TECHNICAL_T0_PREMUTATION_ANALYTICAL_MEIOSIS_ONLY",
        "artificial_full48_source_pools":POOL_COUNT,
        "phenotype_matched_source_strata":STRATA,
        "synthetic_adults_per_stratum":COPY_PER_STRATUM,
        "native_static_return_comparisons":len(rows),
        "native_conditioned_F1_single_offspring_marginal_comparisons":len(rows),
        "independently_observed_natural_source_populations":0,
        "new_biological_genotype_transmission_or_population_histories":0,
        "founder_sample_sizes_intervened":False,
        "original_mutation_process_integrated":False,
        "sustained_order_or_survival_events_observed":False,
        "interpretation":[
            "Quartet-matched M/I adult phenotypes are an expressly artificial balanced t0 source control",
            "Within a given source and visitor context, A and I single-trait expected meiosis moments remain matched across m",
            "Only joint nonzero segregation of A and I within one offspring is allowed to vary across m",
            "This joint segregation probability is not a modelled linkage or independent-locus covariance, and not evolutionary order",
            "Model3 original A mutations and long-run density/stochastic feedback not simulated",
            "No externally valid mainland/island genotype or natural colonisation proof",
        ],
        "rows":rows,
    }


def main()->None:
    print(json.dumps(source_only_audit(),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
