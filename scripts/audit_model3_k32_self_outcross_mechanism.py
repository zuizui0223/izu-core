"""Mechanistic ledger decomposition of Model3 one-step assurance heterozygosity.

A SOURCE-MATCHED offspring-mean and census comparator has lower expected
heterozygote frequency than an artificial, neutral all-parent-pairs Mendelian
mixture. Here the exact difference is separated into:
(A) realized source selfing-vs-outcross share, relative to the tilted null;
(B) within-self mating-parent weighting;
(C) within-outcross donor/recipient mating weights.
These terms are exact algebra against a DECLARED counterfactual, NOT a
causal identification of natural pollinators, adaptive selection or selfing
costs. Canonical reproduce() is never changed.

Old near visitor history 26110601 only, K=32, mutation=0, 8 generations.
All controls are applied at IDENTICAL source parent genotype-count states;
no autonomous eight-year comparator population is simulated.
"""
from __future__ import annotations

import argparse
import json
import hashlib
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_stochastic_bridge import (
    capped_poisson_distribution, genotype_count_markov_step,
    genotype_counts_to_canonical_state, offspring_genotype_distribution,
)
from scripts.audit_model3_k32_mean_matched_ceiling import calibrated_laws
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_k32_same_parent_heterozygosity import (
    offspring_assurance_moments, conditional_inverse_positive_census,
    same_parent_exact_contrast,
)
from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import (
    K, GENERATIONS, OLD_HISTORY, MUTATION_RATE,
)


def conditional_pair_child_law(state, pair_weight, grid):
    """Mendelian law for positive nonnegative parent-pair mass."""
    pair=np.asarray(pair_weight,dtype=float)
    if pair.ndim!=2 or pair.shape!=(len(state.ids),len(state.ids)) or not np.isfinite(pair).all() or (pair<0).any():
        raise ValueError("invalid biological pair weights")
    mass=float(pair.sum())
    if not mass>0:
        return None
    return offspring_genotype_distribution(state,pair/mass,grid)


def _het(q, b):
    return float(np.sum(q[b==.5]))


def matched_tilt_pair_mixture(qself0, qout0, neutral_self_fraction, b, target_mu):
    """Tilt neutral offspring by allele dosage, preserving two mating strata.

    Assumes source q has offspring allelic support present in full all-pairs
    null. Handles exact 0/1 frequency fixation by taking the support-limited
    infinite-tilt distribution without inventing an allele.
    """
    s0=float(neutral_self_fraction)
    if not 0<=s0<=1 or qself0 is None:
        raise ValueError("neutral stratification must contain self pair")
    q0=s0*qself0
    if qout0 is not None:
        q0=q0+(1-s0)*qout0
    elif s0!=1:
        raise ValueError("outcross component required for n>1")
    if not np.isclose(q0.sum(),1.,atol=1e-12,rtol=0):
        raise ArithmeticError("neutral mating mixture lost probability mass")
    mu=float(target_mu)
    if not -1e-12<=mu<=1+1e-12:
        raise ValueError("source expected allele dosage outside [0,1]")
    mu=float(np.clip(mu,0,1))
    if mu in (0.,1.):
        weight=(b==mu).astype(float)
        fit_theta=None
    else:
        fit=calibrated_laws(q0[None,:],b,mu)
        if not fit["admissible"]:
            return {"status":"MATCHED_MEAN_UNATTAINABLE"}
        fit_theta=float(fit["calibration_log_weight"])
        weight=np.exp(fit_theta*b)
    us=qself0*weight
    vs=float(us.sum())
    uo=None if qout0 is None else qout0*weight
    vo=0. if uo is None else float(uo.sum())
    unnorm=s0*us
    if uo is not None:
        unnorm+=(1-s0)*uo
    normalizer=float(unnorm.sum())
    if normalizer<=0:
        return {"status":"MATCHED_MEAN_UNATTAINABLE"}
    null=unnorm/normalizer
    self_fraction=float(s0*vs/normalizer)
    hself=float(_het(us/vs,b)) if vs>0 else 0.
    hout=float(_het(uo/vo,b)) if vo>0 else 0.
    if not np.isclose(null@b,mu,atol=1e-7,rtol=0):
        raise AssertionError("neutral tilted assurance mean mismatch")
    if not np.isclose(_het(null,b),self_fraction*hself+(1-self_fraction)*hout,atol=1e-12):
        raise ArithmeticError("tilted neutral branch reconstruction failed")
    return {
        "status":"MATCHED",
        "q":null,
        "self_fraction":self_fraction,
        "self_heterozygote":hself,
        "outcross_heterozygote":hout,
        "log_tilt":fit_theta,
    }


def exact_ledger_decomposition(counts,grid,visitor,cfg,year):
    """Single original source state; exact three-term heterozygosity contrast."""
    c=np.asarray(counts)
    if c.ndim!=1 or c.shape!=(len(grid.genotypes),) or c.dtype.kind not in "iu" or (c<0).any() or c.sum()>K:
        raise ValueError("invalid source diploid genotype counts")
    n=int(c.sum())
    if not n:
        return {"status":"EXTINCT_PARENT"}
    state=genotype_counts_to_canonical_state(c,grid,year,K)
    ledger=reproduce(state,visitor,cfg)
    self_pair=np.diag(np.asarray(ledger.self_viable,dtype=float))
    out_pair=np.asarray(ledger.outcross,dtype=float)
    selfmass=float(self_pair.sum())
    outmass=float(out_pair.sum())
    total=selfmass+outmass
    if total<=0:
        return {"status":"ZERO_INTENSITY"}
    qself=conditional_pair_child_law(state,self_pair,grid)
    qout=conditional_pair_child_law(state,out_pair,grid)
    qfull=conditional_pair_child_law(state,self_pair+out_pair,grid)
    b=allele_frequency_basis(grid)[:,2]
    src_mu,src_h,src_var=offspring_assurance_moments(qfull,b)
    src_s=selfmass/total

    neutral_all=np.ones((n,n),dtype=float)
    neutral_self=np.eye(n,dtype=float)
    neutral_out=neutral_all-neutral_self
    qself0=conditional_pair_child_law(state,neutral_self,grid)
    qout0=conditional_pair_child_law(state,neutral_out,grid)
    null=matched_tilt_pair_mixture(qself0,qout0,1/n,b,src_mu)
    if null["status"]!="MATCHED":
        return null
    _,null_h,null_var=offspring_assurance_moments(null["q"],b)
    hs_null=null["self_heterozygote"]
    ho_null=null["outcross_heterozygote"]
    hs_source=_het(qself,b) if qself is not None else hs_null
    ho_source=_het(qout,b) if qout is not None else ho_null
    terms={
        "self_vs_outcross_fraction_contrast":
            (src_s-null["self_fraction"])*(hs_null-ho_null),
        "within_self_parent_weighting_contrast":
            src_s*(hs_source-hs_null),
        "within_outcross_mating_weighting_contrast":
            (1-src_s)*(ho_source-ho_null),
    }
    hdiff=sum(terms.values())
    if not np.isclose(hdiff,src_h-null_h,atol=1e-11,rtol=0):
        raise AssertionError("ledger heterozygosity decomposition not additive")
    inv=conditional_inverse_positive_census(total,K)
    if inv is None:
        return {"status":"NO_OCCUPIED_OFFSPRING"}
    # Conditioning on N>0, child dosage mean has Var_q(b)*E(1/N).
    variance_term={k:-0.25*v*inv for k,v in terms.items()}
    expected_variance_delta=(src_var-null_var)*inv
    if not np.isclose(sum(variance_term.values()),expected_variance_delta,atol=1e-11,rtol=0):
        raise AssertionError("3-term variance ledger and direct law disagree")
    parent_q_audit=same_parent_exact_contrast(c,grid,visitor,cfg,year)
    if parent_q_audit["status"]!="MATCHED":
        raise ArithmeticError("same-parent reference did not match")
    if not np.isclose(expected_variance_delta,parent_q_audit["source_minus_comparator_next_frequency_variance"],atol=1e-11,rtol=0):
        raise AssertionError("stratified neutral law changed matched mean/census target")
    return {
        "status":"EXACT_LEDGER_STRATIFIED",
        "source_selfing_fraction_of_viable_seed_intensity":src_s,
        "mean_matched_null_selfing_fraction":null["self_fraction"],
        "source_self_heterozygote_probability":hs_source,
        "source_outcross_heterozygote_probability":ho_source,
        "null_self_heterozygote_probability":hs_null,
        "null_outcross_heterozygote_probability":ho_null,
        "source_total_heterozygote_probability":src_h,
        "null_total_heterozygote_probability":null_h,
        "source_minus_null_heterozygote_probability":src_h-null_h,
        "source_minus_null_next_frequency_variance":expected_variance_delta,
        "exact_three_term_next_frequency_variance":variance_term,
        "exact_three_term_heterozygosity":terms,
        "max_absolute_identity_error":abs(sum(variance_term.values())-expected_variance_delta),
        "conditional_mean_assurance":float(np.clip(src_mu,0,1)),
        "conditional_inverse_positive_recruits":inv,
        "one_step_reproductive_intensity":total,
        "n_source_parents":n,
    }


def _statistics(rows):
    keys=[
        "self_vs_outcross_fraction_contrast",
        "within_self_parent_weighting_contrast",
        "within_outcross_mating_weighting_contrast",
    ]
    vec=np.asarray([[r["exact_three_term_next_frequency_variance"][k] for k in keys]
                    for r in rows],float)
    if len(vec)<1:
        return {"n_source_parent_states":0,"terms":None}
    combined=vec.sum(axis=1)
    return {
        "n_source_parent_states":len(vec),
        "mean_source_minus_null_frequency_variance":float(combined.mean()),
        "mean_source_selfing_fraction":float(np.mean([
            r["source_selfing_fraction_of_viable_seed_intensity"] for r in rows])),
        "mean_null_selfing_fraction":float(np.mean([
            r["mean_matched_null_selfing_fraction"] for r in rows])),
        "terms":{k:float(vec[:,i].mean()) for i,k in enumerate(keys)},
        "term_demographic_mc_se":{k:float(vec[:,i].std(ddof=1)/np.sqrt(len(vec)))
                                 for i,k in enumerate(keys)} if len(vec)>1 else None,
        "total_demographic_mc_se":float(combined.std(ddof=1)/np.sqrt(len(vec)))
                                  if len(vec)>1 else None,
        "max_absolute_analytic_identity_error":float(max(
            r["max_absolute_identity_error"] for r in rows)),
        "fraction_of_parent_states_with_positive_source_minus_null_variance":
            float(np.mean(combined>1e-12)),
    }


def run_ledger(*,budget=8.,draws=512,seed=420261015):
    if budget not in (3.,8.) or type(draws) is not int or not 16<=draws<=2048 or type(seed) is not int or seed<0:
        raise ValueError("old-history restricted K32 comparison only")
    first,grid,_,_=fixed_support_problem(capacity=32,ovule_budget=budget)
    design=load_design(DEFAULT_DESIGN)
    src=source_config(design,"prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(src,capacity=32,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(src.seed_arrival,supply=0.))
    old=exposure(OLD_HISTORY,"near").visitors[:8]
    if len(old)!=8 or cfg.assurance_timing!="prior":
        raise AssertionError("source timing/history changed")
    digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()+
        v.effectiveness.tobytes() for v in old)).hexdigest()
    states=np.repeat(first[None,:],draws,axis=0)
    years=[]
    unexpected=[]
    for year in range(8):
        records=[]
        status={}
        for i in range(draws):
            parent=states[i]
            if int(parent.sum())==0:
                status["EXTINCT_PARENT"]=status.get("EXTINCT_PARENT",0)+1
                continue
            item=exact_ledger_decomposition(parent,grid,old[year],cfg,year)
            if item["status"]=="EXACT_LEDGER_STRATIFIED":
                records.append(item)
            else:
                status[item["status"]]=status.get(item["status"],0)+1
            states[i]=genotype_count_markov_step(
                parent,grid,old[year],cfg,
                np.random.default_rng(np.random.SeedSequence([seed,i,year])),
                year=year)
        row=_statistics(records)
        row.update({"generation":year+1,"status_counts_not_comparable":status,
                    "n_source_occupied_after_generation":int(np.sum(states.sum(axis=1)>0))})
        years.append(row)
        if any(k!="EXTINCT_PARENT" for k in status):
            unexpected.append({"generation":year+1,"statuses":status})
    return {
        "status":("EXACT_SELF_OUTCROSS_DECOMPOSITION_VERIFIED" if not unexpected
                  else "SOURCE_STRATIFICATION_HAD_UNMATCHED_STATES"),
        "evidence_type":"old_history_synthetic_model3_exact_conditional_ledger_not_natural_observations",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":8,
            "adult_survival":0,"seed_immigration":0,
            "ovule_budget":budget,"old_visitor_history":OLD_HISTORY,
            "environment":"near","visitor_sha256":digest,
            "independent_visitor_histories":1,
            "nested_demographic_replicates":draws,
            "canonical_model3_biology_modified":False,
            "confirmatory_history_used":False,
            "reference_is_autonomous_population_simulation":False,
            "source_parent_and_matched_offspring_mean_and_recruitment_law_identical":True,
            "comparator_parent_pairing_permits_self":True,
        },
        "per_generation":years,
        "unmatched_states":unexpected,
        "mechanistic_identity":"Hsource-Hmatched=(s_source-s_null)*(Hself_null-Hout_null)+s_source*(Hself_source-Hself_null)+(1-s_source)*(Hout_source-Hout_null); VarNextDelta=-Hdiff*E[1/N|N>0]/4.",
        "scientific_limits":[
            "The three terms are exactly additive relative to a declared equal-parent, self-including dosage-tilted null, but depend on the baseline and decomposition order.",
            "Self-vs-outcross fraction is a composition contrast, not isolation of the causal advantage of self-fertilization.",
            "Within-self term includes source genotype-specific maternal fecundity and assurance allocation.",
            "Within-outcross term includes donor export, visitor-mediated pollen affinity, mating bias, and maternal fecundity; these are not individually identified.",
            "No stand-alone eight-year comparator, independent ecology histories, real plant fitness, or established SDE/SPDE."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=512)
    a=p.parse_args()
    report=run_ledger(budget=a.budget,draws=a.draws)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    last=report["per_generation"][-1]
    print(json.dumps({"status":report["status"],"budget":a.budget,
          "last":{k:last[k] for k in (
            "n_source_parent_states",
            "mean_source_minus_null_frequency_variance",
            "mean_source_selfing_fraction","mean_null_selfing_fraction",
            "terms","max_absolute_analytic_identity_error")}}))


if __name__=="__main__":
    main()
