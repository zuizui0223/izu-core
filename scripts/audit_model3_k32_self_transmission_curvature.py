"""Exact self-allele transmission curvature vs investment pairing in Model3.

The frozen Chapter2 prior_selfing source has assurance_cost=0 and
investment_cost=.5: expected viable self seeds are

 s_i = B*(1-depression) * w_i*a_i,  w_i=exp(-cI*I_i**2).

This is LINEAR in assurance trait a, not a nonlinear intrinsic self
seed intensity function. The expected assurance high-allele numerator
is M=sum_i s_i*(b_i-p) with high-allele dosage b_i in {0,.5,1}
and a_i=.25+.5*b_i. Hence a*b includes a b**2 term.
At fixed b-copy count replacing one LL+HH with two LH changes
sum_i a_i*(b_i-p) EXACTLY -1/4; the reverse changes +1/4.
This is a transmission-weighting/segregation effect even if the
selfed-seed COUNT stays unchanged.

For the SAME two individual edited positions, let bar_w be the
mean of their investment factors and ΔF_i the change in
a_i*(b_i-p). EXACT two-person identity:

 ΔM= B*(1-d)*[bar_w*sum(ΔF_i) +
               sum((w_i-bar_w)*ΔF_i)].

First term: assurance-dosage curvature at mean pair investment.
Second: allocation of assurance edits across different investments.
For original total viable seed intensity T, exact self-channel
expected allele-direction difference is

 (M_edit/T_edit - M_sham/T_sham)
 = ΔM/T_sham - M_edit*ΔT/(T_sham*T_edit),

where ΔT=Δself_viable_seeds+Δoutcross_viable_seeds.
The denominator term is separately split by these two source
expected-seed-intensity changes.

Source original reproduction unmodified. Hypothetically edited
parents from SAME sham + one two-individual HET_UP or HET_DOWN
operation; only old near visitor history 26110601, K32 u=0.
This is mathematical attribution, NOT a uniquely causal fitness
coefficient, independent pollinator manipulation, or natural data.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_count_markov_step, genotype_counts_to_canonical_state
from scripts.audit_model3_k32_fixed_frequency_heterozygosity import (
    assurance_diplotype_multiset, controlled_assurance_pairs,
    OPERATORS,PARENT_YEARS,VISITOR_YEARS,HIGH,
)
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import DEFAULT_DESIGN,config as source_config,load_design
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import K,GENERATIONS,MUTATION_RATE,OLD_HISTORY

KEYS=(
    "intrinsic_dosage_numerator_at_mean_investment",
    "investment_alignment_numerator",
    "self_direction_intrinsic_numerator_over_old_total",
    "self_direction_investment_alignment_over_old_total",
    "self_direction_denominator_due_to_self_seed_mass",
    "self_direction_denominator_due_to_outcross_seed_mass",
    "self_direction_total_exact",
    "self_viable_seed_intensity_delta",
    "outcross_viable_seed_intensity_delta",
    "total_viable_seed_intensity_delta",
    "raw_high_allele_self_numerator_delta",
    "self_intensity_if_both_investments_equal_delta",
    "sum_of_self_dosage_products_delta",
)


def exact_self_transmission_contrast(sham,edited,visitor,cfg):
    if (cfg.assurance_timing!="prior" or cfg.assurance_mode!="evolving"
            or cfg.assurance_cost!=0 or cfg.mutation_rate!=0
            or cfg.investment_cost!=.5):
        raise ValueError("restricted ORIGINAL zero-assurance-cost prior-selfing source only")
    x=np.asarray(sham.alleles,float)
    y=np.asarray(edited.alleles,float)
    if x.shape!=y.shape or x.ndim!=3 or x.shape[1:]!=(3,2) or len(x)<2:
        raise ValueError("same living source parents required")
    if not np.array_equal(x[:,:2,:],y[:,:2,:]):
        raise ValueError("editing another source locus is forbidden")
    if np.any(~np.isin(x,[.25,.75])) or np.any(~np.isin(y,[.25,.75])):
        raise ValueError("source allele values only")
    affected=np.flatnonzero(np.any(x[:,2,:]!=y[:,2,:],axis=1))
    if len(affected)!=2:
        raise ValueError("two edited assurance diplotypes required")
    a0=x[:,2,:].mean(axis=1)
    a1=y[:,2,:].mean(axis=1)
    b0=np.mean(x[:,2,:]==HIGH,axis=1)
    b1=np.mean(y[:,2,:]==HIGH,axis=1)
    if not np.isclose(b0.mean(),b1.mean(),atol=1e-12,rtol=0):
        raise AssertionError("parent assurance high copy count changed")
    p=float(b0.mean())
    investment=x[:,1,:].mean(axis=1)
    w=np.exp(-cfg.investment_cost*investment**2)
    prefactor=cfg.ovule_budget*(1.-cfg.depression)
    old=reproduce(sham,visitor,cfg)
    new=reproduce(edited,visitor,cfg)
    np.testing.assert_allclose(old.self_viable,prefactor*w*a0,atol=1e-12,rtol=0)
    np.testing.assert_allclose(new.self_viable,prefactor*w*a1,atol=1e-12,rtol=0)
    f0=a0*(b0-p)
    f1=a1*(b1-p)
    delta_f=f1[affected]-f0[affected]
    delta_a=a1[affected]-a0[affected]
    if not np.isclose(delta_a.sum(),0,atol=1e-12,rtol=0):
        raise ArithmeticError("fixed allele copies did not conserve linear selfing trait")
    if not np.isclose(abs(delta_f.sum()),.25,atol=1e-12,rtol=0):
        raise ArithmeticError("exact two-genotype assurance transmission curvature changed")
    weights=w[affected]
    avg=float(weights.mean())
    intrinsic=float(prefactor*avg*delta_f.sum())
    alignment=float(prefactor*np.dot(weights-avg,delta_f))
    numerator0=float(old.self_viable@(b0-p))
    numerator1=float(new.self_viable@(b1-p))
    delta_numerator=numerator1-numerator0
    if not np.isclose(intrinsic+alignment,delta_numerator,atol=1e-11,rtol=0):
        raise ArithmeticError("assurance dosage and investment numerator decomposition failed")
    self0=float(old.self_viable.sum())
    self1=float(new.self_viable.sum())
    out0=float(old.outcross.sum())
    out1=float(new.outcross.sum())
    T0=self0+out0
    T1=self1+out1
    if min(T0,T1)<=0:
        raise ArithmeticError("positive original source intensity required")
    delta_self=self1-self0
    delta_out=out1-out0
    delta_t=T1-T0
    equal_investment_self_delta=float(prefactor*avg*delta_a.sum())
    assert np.isclose(equal_investment_self_delta,0,atol=1e-12)
    np.testing.assert_allclose(
        delta_self,prefactor*np.dot(weights-avg,delta_a),atol=1e-11,rtol=0)
    components=np.array([
        intrinsic/T0,
        alignment/T0,
        -numerator1*delta_self/(T0*T1),
        -numerator1*delta_out/(T0*T1),
    ])
    total=float(numerator1/T1-numerator0/T0)
    np.testing.assert_allclose(components.sum(),total,atol=1e-11,rtol=0)
    # source exact original self expected high-dose direction
    if not np.isclose(numerator0/T0,
                      (old.self_viable@b0)/T0-(self0/T0)*p,
                      atol=1e-12,rtol=0):
        raise ArithmeticError("source self direction mismatch")
    if not np.isclose(numerator1/T1,
                      (new.self_viable@b1)/T1-(self1/T1)*p,
                      atol=1e-12,rtol=0):
        raise ArithmeticError("edited source self direction mismatch")
    values=np.array([
        intrinsic,alignment,*components,total,
        delta_self,delta_out,delta_t,delta_numerator,
        equal_investment_self_delta,delta_f.sum()
    ],float)
    if len(values)!=len(KEYS) or not np.isfinite(values).all():
        raise ArithmeticError("invalid source channel array")
    return dict(zip(KEYS,values.tolist()))


def _stats(array):
    z=np.asarray(array,float)
    if z.ndim!=2 or z.shape[1]!=len(KEYS):
        raise ValueError("complete paired source channel component vectors required")
    return {
        "n_original_parent_paths":len(z),
        "means":dict(zip(KEYS,z.mean(axis=0).tolist())) if len(z) else None,
        "nested_demographic_mc_se":dict(zip(KEYS,
            (z.std(axis=0,ddof=1)/np.sqrt(len(z))).tolist()))
            if len(z)>1 else None,
        "max_absolute_reconstruction_error":float(max(
            np.max(np.abs(z[:,2:6].sum(axis=1)-z[:,6])),
            np.max(np.abs(z[:,0]+z[:,1]-z[:,10])),
            np.max(np.abs(z[:,7]+z[:,8]-z[:,9]))
        )) if len(z) else 0.,
    }


def run_self_curvature(*,budget=8.,draws=512,permutations=4,
                       seed=420261017):
    if (budget not in (3.,8.) or type(draws) is not int
            or not 16<=draws<=2048 or type(permutations) is not int
            or not 1<=permutations<=16 or type(seed) is not int or seed<0):
        raise ValueError("one old K32 source history and declared MC range only")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    cfg0=source_config(load_design(DEFAULT_DESIGN),"prior_selfing",
                       MUTATION_RATE,"evolving")
    cfg=replace(cfg0,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(cfg0.seed_arrival,supply=0.))
    assert cfg.assurance_cost==0 and cfg.investment_cost==.5
    assert cfg.assurance_timing=="prior" and cfg.depression==.5
    visits=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    assert len(visits)==8
    visitor_hash=hashlib.sha256(b"".join(
        x.ids.tobytes()+x.optima.tobytes()+x.breadths.tobytes()+
        x.effectiveness.tobytes() for x in visits)).hexdigest()
    states=np.repeat(initial[None,:],draws,axis=0)
    snapshots={}
    for t in range(8):
        if t in PARENT_YEARS:
            snapshots[t]=states.copy()
        if t<7:
            for rep in range(draws):
                states[rep]=genotype_count_markov_step(
                    states[rep],grid,visits[t],cfg,
                    np.random.default_rng(np.random.SeedSequence(
                        [seed,rep,t])),year=t)
    cohort=np.flatnonzero(states.sum(axis=1)>0)
    if len(cohort)<16:
        return {"status":"INSUFFICIENT_SOURCE_YEAR8_PARENT_SURVIVORS"}
    result={}
    for t in PARENT_YEARS:
        parents=snapshots[t]
        eligible={}
        for op in OPERATORS:
            samples={v:[] for v in VISITOR_YEARS}
            n_feasible=0
            for rep in cohort:
                state=genotype_counts_to_canonical_state(
                    parents[rep],grid,t,K)
                _,_,classes=assurance_diplotype_multiset(state)
                allowed=((classes[0]>=1 and classes[2]>=1) if
                         op=="heterozygosity_up" else classes[1]>=2)
                if not allowed:
                    continue
                n_feasible+=1
                per_visitor={v:[] for v in VISITOR_YEARS}
                for m in range(permutations):
                    order=np.random.default_rng(np.random.SeedSequence(
                        [seed,int(rep),t,m,20261009])
                    ).permutation(len(state.ids)).astype(np.int64)
                    sham=controlled_assurance_pairs(state,"sham",order)
                    edit=controlled_assurance_pairs(state,op,order)
                    if edit is None:
                        raise AssertionError("eligible same-source edit became unavailable")
                    for v in VISITOR_YEARS:
                        decomposition=exact_self_transmission_contrast(
                            sham,edit,visits[v],cfg)
                        per_visitor[v].append([
                            decomposition[k] for k in KEYS])
                for v in VISITOR_YEARS:
                    samples[v].append(np.mean(per_visitor[v],axis=0))
            eligible[op]={
                "n_source_parent_paths_eligible":n_feasible,
                "n_source_parent_paths_ineligible":len(cohort)-n_feasible,
                "fraction_eligible":n_feasible/len(cohort),
                "visitors":{
                    str(v+1):_stats(np.asarray(samples[v],float).reshape((-1,len(KEYS))))
                    for v in VISITOR_YEARS
                },
            }
        result[str(t+1)]=eligible
    return {
        "status":"ORIGINAL_K32_EXACT_LINEAR_SELFING_DOSAGE_CURVATURE_AUDIT_VERIFIED",
        "source_provenance":{
            "K":K,"mutation_rate":0,"generations":GENERATIONS,
            "budget":budget,"adult_survival":0,"seed_immigration":0,
            "old_visitor_history":OLD_HISTORY,
            "old_visitor_environment":"near","old_visitor_sha256":visitor_hash,
            "n_independent_visitor_histories":1,
            "nested_source_demographic_paths":draws,
            "n_source_year8_parent_survivors":len(cohort),
            "n_permutations_per_feasible_parent":permutations,
            "assurance_cost":cfg.assurance_cost,
            "investment_cost":cfg.investment_cost,
            "selfing_depression":cfg.depression,
            "source_self_seed_function_linear_in_assurance_a":True,
            "source_model3_reproductive_biology_modified":False,
            "edited_parent_assurance_high_allele_copies_preserved":True,
            "edited_parent_investment_and_matching_genotypes_preserved":True,
            "prospective_confirmatory_histories_accessed":False,
            "visitor_years":[v+1 for v in VISITOR_YEARS],
            "original_source_parent_years":[t+1 for t in PARENT_YEARS],
        },
        "mechanistic_identity":"s_i=B(1-d)*exp(-cI I_i^2)*a_i (cA=0). M=sum self_i*(high_allele_dosage_i-parent_p); HET_UP at fixed allele copies changes unweighted sum a_i*(b_i-p) by exactly -1/4, HET_DOWN by +1/4. ΔM=intrinsic_common_pair_investment + residual_placement_investment. Δ(M/T)=ΔM/T_old - M_edited*(Δself+Δoutcross)/(T_old*T_edit).",
        "component_names":list(KEYS),
        "source_parent_years":result,
        "scientific_boundaries":[
            "There is NO intrinsic nonlinear assurance-cost reproductive seed rule under prior_selfing: assurance_cost is exactly ZERO. High-allele self transmission involves the product a*b, which is quadratic in diploid high-allele dosage b.",
            "At exact fixed parental allele copy number, assurance HET edit alters high-allele self transmission numerator by signed +/-1/4 times mean investment weighting (scaled by B(1-d)), plus an exact residual of two individuals' investment-weight alignment.",
            "Selfed viable seed COUNT has no intrinsic common-investment curvature term because self intensity is linear in assurance; its perturbation arises solely from different investment trait weight alignment.",
            "Changing edited parents can also change outcross seed intensity and thus total normalization of the source self transmission direction; the denominator is decomposed exactly into self and outcross seed-intensity terms.",
            "The comparisons are paired with the same shuffled SHAM genotype alignment and are feasible only with required parental assurance genotype classes; these are hypothetical parent edits not endogenous source evolution.",
            "Only one old visitor history and nested demographic paths, not independent natural island evidence or a causal physiological selection experiment. No frozen confirmatory histories, field data or SDE/SPDE."
        ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=512)
    p.add_argument("--permutations",type=int,default=4)
    a=p.parse_args()
    out=run_self_curvature(budget=a.budget,draws=a.draws,
                           permutations=a.permutations)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":out["status"],"budget":a.budget,
        "year8_late_visitor":{
            op:{
                "n":out["source_parent_years"]["8"][op]["n_source_parent_paths_eligible"],
                "means":out["source_parent_years"]["8"][op]["visitors"]["8"]["means"],
                "identity_error":out["source_parent_years"]["8"][op]["visitors"]["8"]["max_absolute_reconstruction_error"]
            } for op in OPERATORS},
    }))


if __name__=="__main__":
    main()
