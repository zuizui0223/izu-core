"""Matched-demography neutral Mendelian control for old Model 3 K32.

Canonical source arm: UNMODIFIED reproduce(), capped-Poisson recruitment,
complete joint 3-locus Mendelian inheritance. Counterfactual neutral arm:
neutral unordered distinct-parent mating and the same Mendelian gamete law,
with census sizes IMPOSED from the source arm. Neutral comparison is
deliberately a DIFFERENT reproductive biology, not a Model3 mechanism.

With no genotype-dependent reproductive advantage, E[p_high(t+1) | parent,
N>0] == p_high(t), even near the allele-frequency ceiling 1. This tests
whether bounded sampling by itself generates the large directional mean
change seen in the SOURCE model. It does NOT isolate why the source model's
accumulated direction/sampling components are negatively correlated.

One archived visitor history 26110601, near; no new ecology histories,
no natural observations, no changes to canonical Model3 biological files.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import numpy as np

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_count_markov_step
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.run_model3_three_arm_k32_old_history import K,GENERATIONS,MUTATION_RATE,OLD_HISTORY
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config,load_design)
from scripts.run_model3_persistent_isolation import exposure


def neutral_child_genotype_law(counts,grid):
    """Source Mendelian gamete law, equal parent weights, different individuals.

    Matrix of ordered gamete-pair probabilities excludes the same *individual*
    when n>=2; two genotype-identical individuals may still mate. When
    n==1, use a declared self mating to preserve the neutral invariant.
    """
    c=np.asarray(counts)
    if (c.ndim!=1 or c.shape!=(len(grid.genotypes),) or
        c.dtype.kind not in "iu" or np.any(c<0)):
        raise ValueError("integer joint diploid genotype census required")
    n=int(c.sum())
    if not n:
        return np.zeros(len(c),dtype=float)
    g=np.asarray(grid.gamete_probabilities)
    if n==1:
        i=int(np.flatnonzero(c)[0])
        pairing=np.outer(g[i],g[i])
    else:
        total=c@g
        repeated=(g.T*c)@g
        pairing=(np.outer(total,total)-repeated)/(n*(n-1))
    if pairing.min() < -1e-12:
        raise ArithmeticError("neutral gamete-pair law has negative probability")
    pairing=np.maximum(pairing,0.)
    q=np.bincount(grid.child_lookup.ravel(),weights=pairing.ravel(),
                  minlength=len(grid.genotypes)).astype(float)
    if not np.isclose(q.sum(),1.,atol=1e-11,rtol=0):
        raise ArithmeticError("neutral child genotype law fails mass audit")
    q/=q.sum()
    # Neutrality is exact on each of the 3 allele frequencies.
    basis=allele_frequency_basis(grid)
    parent_freq=(c@basis)/n
    np.testing.assert_allclose(q@basis,parent_freq,atol=1e-12,rtol=0)
    return q


def _summary(x):
    a=np.asarray(x,float)
    if a.ndim!=2 or a.shape[1]!=3:
        raise ValueError("3 locus record required")
    if len(a)==0:
        return {"n":0,"mean":None,"mc_se":None,"variance":None}
    return {
        "n":len(a),
        "mean":a.mean(axis=0).tolist(),
        "mc_se":(a.std(axis=0,ddof=1)/np.sqrt(len(a))).tolist() if len(a)>1 else None,
        "variance":a.var(axis=0,ddof=0).tolist(),
    }


def run_neutral_control(*,budget=8.,draws=512,seed=420261011):
    if (budget not in (3.,8.) or type(draws) is not int or
        not 16<=draws<=4096 or type(seed) is not int or seed<0):
        raise ValueError("old history budget, K32 and sample scope are fixed")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    design=load_design(DEFAULT_DESIGN)
    src=source_config(design,"prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(src,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(src.seed_arrival,supply=0.))
    assert cfg.assurance_timing=="prior" and len(grid.genotypes)==27
    old=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    assert len(old)==GENERATIONS==8
    digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()
        +v.effectiveness.tobytes() for v in old)).hexdigest()

    basis=allele_frequency_basis(grid)
    initial_f=initial@basis/initial.sum()
    source_final=np.full((draws,3),np.nan)
    null_final=np.full((draws,3),np.nan)
    source_fixed_high=np.zeros((draws,3),bool)
    null_fixed_high=np.zeros((draws,3),bool)
    source_lost_high=np.zeros((draws,3),bool)
    null_lost_high=np.zeros((draws,3),bool)
    source_counts=np.repeat(initial[None,:],draws,axis=0)
    neutral_counts=np.repeat(initial[None,:],draws,axis=0)
    active=np.ones(draws,bool)
    census_law_agreement=[]
    per_year=[]
    for t in range(GENERATIONS):
        source_q_allele=[]
        source_parent_allele=[]
        null_parent_allele=[]
        source_child_allele=[]
        null_child_allele=[]
        started=int(active.sum())
        for rep in np.flatnonzero(active):
            s=source_counts[rep].copy()
            n=neutral_counts[rep].copy()
            assert s.sum()==n.sum()
            # Source is the ORIGINAL frozen biological genotype count chain.
            child=genotype_count_markov_step(
                s,grid,old[t],cfg,
                np.random.default_rng(np.random.SeedSequence([seed,rep,t,101])),
                year=t)
            next_n=int(child.sum())
            source_counts[rep]=child
            neutral_q=neutral_child_genotype_law(n,grid)
            if next_n:
                rng=np.random.default_rng(np.random.SeedSequence([seed,rep,t,202]))
                # Re-sample full joint 3-locus Mendelian child genotypes.
                neutral=np.bincount(
                    rng.choice(len(neutral_q),size=next_n,p=neutral_q),
                    minlength=len(neutral_q)).astype(np.int64)
            else:
                neutral=np.zeros(len(n),dtype=np.int64)
                active[rep]=False
            neutral_counts[rep]=neutral
            assert neutral.sum()==next_n and 0<=next_n<=K
            census_law_agreement.append(int(neutral.sum())==int(child.sum()))
            if not next_n:
                continue
            sp=s@basis/s.sum()
            np_=n@basis/n.sum()
            sc=child@basis/next_n
            nc=neutral@basis/next_n
            # qsource from the untouched Model3 reproduction operator.
            from scripts.run_model3_three_arm_k32_old_history import canonical_conditional_kernel
            _,sq=canonical_conditional_kernel(s,grid,old[t],cfg,t)
            source_q_allele.append(sq@basis)
            source_parent_allele.append(sp)
            null_parent_allele.append(np_)
            source_child_allele.append(sc)
            null_child_allele.append(nc)
            source_final[rep]=sc
            null_final[rep]=nc
        if active.any():
            idx=np.flatnonzero(active)
            per_year.append({
                "generation":t+1,"started":started,"survived":int(active.sum()),
                "source_allele_means":source_final[idx].mean(axis=0).tolist(),
                "neutral_allele_means":null_final[idx].mean(axis=0).tolist(),
                "source_expected_direction_conditional_survivors":(
                    np.mean(np.asarray(source_q_allele)-np.asarray(source_parent_allele),axis=0).tolist()
                    if source_q_allele else None),
                "neutral_expected_direction":
                    [0.,0.,0.],
                "source_vs_neutral_mean_difference":(
                    source_final[idx]-null_final[idx]).mean(axis=0).tolist(),
            })
        else:
            per_year.append({
                "generation":t+1,"started":started,"survived":0,
                "source_allele_means":None,"neutral_allele_means":None,
                "source_expected_direction_conditional_survivors":None,
                "neutral_expected_direction":[0.,0.,0.],
                "source_vs_neutral_mean_difference":None,
            })
    idx=np.flatnonzero(active)
    assert all(census_law_agreement)
    if len(idx)==0:
        raise ArithmeticError("no surviving source-controlled cohorts for comparison")
    sp=source_final[idx]
    np_=null_final[idx]
    differences=sp-np_
    src_fix=np.isclose(sp,1.,atol=1e-12,rtol=0)
    null_fix=np.isclose(np_,1.,atol=1e-12,rtol=0)
    src_loss=np.isclose(sp,0.,atol=1e-12,rtol=0)
    null_loss=np.isclose(np_,0.,atol=1e-12,rtol=0)
    return {
        "status":"FROZEN_SOURCE_VS_EXTERNAL_NEUTRAL_MENDELIAN_CONTROL",
        "evidence_type":"one_old_history_engineered_counterfactual_not_natural_island_observations",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":GENERATIONS,
            "ovule_budget":budget,"reproductive_setting":"prior_selfing",
            "old_visitor_history":OLD_HISTORY,"environment":"near",
            "independent_visitor_histories":1,"nested_demographic_replicates":draws,
            "n_source_survivors":len(idx),"n_source_extinct":draws-len(idx),
            "canonical_source_biology_edited":False,
            "neutral_control_intentionally_different_reproductive_operator":True,
            "neutral_census_forced_to_source_same_trajectory":True,
            "confirmatory_cohorts_used":False,
            "full_joint_three_locus_classes":len(grid.genotypes),
            "old_visitor_digest":digest,
        },
        "neutral_definition":"uniform distinct-individual paired gametes (self allowed only if Nparent=1), source Mendelian child tensor; no genotype-dependent reproductive payoffs, demographic census exogenously matched to source",
        "initial_high_allele_frequencies":initial_f.tolist(),
        "source_survivor_endpoint_high_allele_frequency":_summary(sp),
        "neutral_survivor_endpoint_high_allele_frequency":_summary(np_),
        "paired_survivor_source_minus_neutral":_summary(differences),
        "source_high_allele_fixation_probability_given_source_survival":src_fix.mean(axis=0).tolist(),
        "neutral_high_allele_fixation_probability_given_source_survival":null_fix.mean(axis=0).tolist(),
        "source_high_allele_loss_probability_given_source_survival":src_loss.mean(axis=0).tolist(),
        "neutral_high_allele_loss_probability_given_source_survival":null_loss.mean(axis=0).tolist(),
        "same_realized_census_each_year":True,
        "per_generation":per_year,
        "claim_limits":[
            "Neutral null deliberately changes biological mating weights; frozen source biological files stay unchanged.",
            "Matching source N(t) holds realized demography fixed, not the source's endogenous demography under neutral mating.",
            "Neutral expected high allele frequency is exactly constant under unweighted mating conditional on every parent state and N>0.",
            "Conditioning source survival may affect source means; neutral inheritance randomness is independent of source histories.",
            "Difference from neutral supports source-conditional directional reproduction in Model3 but does not identify adaptation in natural populations.",
            "Near-fixation upper bound can still explain small endpoint variance/negative filter-noise covariance; this control does not isolate covariance causality.",
            "One old visitor history, no natural data, no SDE/SPDE validation.",
        ]
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    parser.add_argument("--draws",type=int,default=512)
    a=parser.parse_args()
    r=run_neutral_control(budget=a.budget,draws=a.draws)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps({
        "status":r["status"],"budget":a.budget,
        "n_survivors":r["conditions"]["n_source_survivors"],
        "source":r["source_survivor_endpoint_high_allele_frequency"]["mean"],
        "neutral":r["neutral_survivor_endpoint_high_allele_frequency"]["mean"],
        "paired_difference":r["paired_survivor_source_minus_neutral"]["mean"],
        "paired_se":r["paired_survivor_source_minus_neutral"]["mc_se"],
    }))


if __name__=="__main__":
    main()
