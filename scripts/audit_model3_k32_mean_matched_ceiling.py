"""Post-outcome mean-matched directional ceiling control for Model 3 K32.

The SOURCE is unchanged canonical Model 3 (complete joint Mendelian
inheritance, source mating, capped-Poisson recruitment). The COMPARATOR
uses a uniform, *externally calibrated per-generation* exponential
reweighting of neutral Mendelian offspring by assurance high-allele dosage,
and follows exactly the same realized source census trajectory.

This comparator is a DIFFERENT biological offspring law, fitted after
source outcomes are known. It is NOT an independent confirmation, pure
neutral drift, a validated deterministic model, or a replacement for the
Model 3 source. It tests whether *the same mean allele-frequency trajectory
and hard [0,1] boundaries* can reproduce the source endpoint variance
and negative cumulative direction/noise covariance.

No new visitor histories; only archived seed 26110601 and fixed engineered
four-founder, 27 joint-genotype support. No mutation, survival, immigration.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_k32_neutral_census_control import neutral_child_genotype_law
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_count_markov_step
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import (
    canonical_conditional_kernel, K, GENERATIONS, MUTATION_RATE, OLD_HISTORY,
)


def tilted_offspring_law(neutral_q, assurance_dosage, log_weight):
    """Uniform external directional weight; no new genotype support."""
    q=np.asarray(neutral_q,float)
    b=np.asarray(assurance_dosage,float)
    if (q.ndim!=1 or q.shape!=b.shape or not len(q) or
            not np.isfinite(q).all() or not np.isfinite(b).all()
            or (q<0).any() or (b<0).any() or (b>1).any() or
            not np.isclose(q.sum(),1.,atol=1e-11,rtol=0)
            or not np.isfinite(log_weight) or abs(log_weight)>45):
        raise ValueError("invalid mean-matched full-joint offspring law")
    weights=q*np.exp(float(log_weight)*b)
    total=float(weights.sum())
    if total<=0 or not np.isfinite(total):
        raise ArithmeticError("tilted Mendelian law normalization failure")
    result=weights/total
    if np.any(result[q==0]!=0) or not np.isclose(result.sum(),1.,atol=1e-12):
        raise ArithmeticError("tilting manufactured genotype support")
    return result


def calibrated_laws(neutral_qs, assurance_dosage, target, *, tol=1e-10):
    """Find ONE external log-weight for the cohort at this generation.

    Match *analytical mean conditional child allele frequency*, not realized
    samples. If an absorbing allele-loss boundary prevents matching the target
    even at allowed extreme tilts, return inadmissible rather than fabricating
    resurrection or silently pretending matching succeeded.
    """
    Q=np.asarray(neutral_qs,float)
    b=np.asarray(assurance_dosage,float)
    if (Q.ndim!=2 or Q.shape[1]!=len(b) or len(Q)==0
            or not 0<=target<=1):
        raise ValueError("invalid frequency cohort or target")
    def evaluate(s):
        w=Q*np.exp(s*b)[None,:]
        p=w/w.sum(axis=1,keepdims=True)
        return float(np.mean(p@b)),p
    lower,_=evaluate(-40.)
    upper,_=evaluate(40.)
    if target < lower-tol or target > upper+tol:
        return {"admissible":False,"target":float(target),
                "lower_attainable":lower,"upper_attainable":upper,
                "reason":"absorbing_allele_support_prevents_mean_matching"}
    lo,hi=-40.,40.
    for _ in range(60):
        mid=(lo+hi)/2
        value,_=evaluate(mid)
        if value<target:
            lo=mid
        else:
            hi=mid
    param=(lo+hi)/2
    achieved,p=evaluate(param)
    if abs(achieved-target)>1e-7:
        raise ArithmeticError("mean match numerical error")
    if np.max(np.abs(p.sum(axis=1)-1.))>1e-12:
        raise ArithmeticError("per-parent genotype law lost mass")
    return {"admissible":True, "target":float(target),
            "calibration_log_weight":float(param),
            "calibrated_conditional_mean":achieved,
            "lower_attainable":lower,"upper_attainable":upper,
            "laws":p}


def variance_parts(direction, noise):
    """Exact finite-ensemble covariance accounting on SURVIVOR paths."""
    d=np.asarray(direction,float)
    e=np.asarray(noise,float)
    if d.shape!=e.shape or d.ndim!=1 or len(d)<2:
        raise ValueError("at least two surviving scalar paths required")
    vd=float(np.var(d,ddof=0))
    ve=float(np.var(e,ddof=0))
    twice=2.*float(np.mean((d-d.mean())*(e-e.mean())))
    total=float(np.var(d+e,ddof=0))
    if not np.isclose(vd+ve+twice,total,atol=1e-11,rtol=0):
        raise AssertionError("variance telescoping failed")
    return {
        "var_cumulative_direction":vd,
        "var_cumulative_sampling":ve,
        "two_times_covariance":twice,
        "total_frequency_change_variance":total,
        "covariance_identity_error":(vd+ve+twice-total),
    }


def run_mean_matched(*,budget=8.,draws=512,seed=420261012):
    if (budget not in (3.,8.) or type(draws) is not int or
            not 16<=draws<=4096 or type(seed) is not int or seed<0):
        raise ValueError("restricted K32 old-history numerical comparison")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=float(budget))
    design=load_design(DEFAULT_DESIGN)
    source=source_config(design,"prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(source,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(source.seed_arrival,supply=0.))
    assert cfg.assurance_timing=="prior" and cfg.mutation_rate==0
    old=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    assert len(old)==8
    digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()
        +v.effectiveness.tobytes() for v in old)).hexdigest()
    basis=allele_frequency_basis(grid)
    b=basis[:,2]
    start=float(initial@b/initial.sum())
    if not np.isclose(start,.5,atol=1e-12):
        raise AssertionError("frozen assurance starting state changed")

    canonical=np.repeat(initial[None,:],draws,axis=0)
    matched=np.repeat(initial[None,:],draws,axis=0)
    active=np.ones(draws,bool)
    canonical_filter=np.zeros(draws,float)
    canonical_sampling=np.zeros(draws,float)
    matched_filter=np.zeros(draws,float)
    matched_sampling=np.zeros(draws,float)
    source_endpoint=np.full(draws,np.nan)
    comparator_endpoint=np.full(draws,np.nan)
    years=[]
    for t in range(GENERATIONS):
        survivors=np.flatnonzero(active)
        source_parent=canonical.copy()
        null_parent=matched.copy()
        q_source={}
        source_census={}
        for i in survivors:
            _,qs=canonical_conditional_kernel(source_parent[i],grid,old[t],cfg,t)
            child=genotype_count_markov_step(
                source_parent[i],grid,old[t],cfg,
                np.random.default_rng(np.random.SeedSequence([seed,100,int(i),t])),
                year=t)
            canonical[i]=child
            next_n=int(child.sum())
            if next_n==0:
                active[i]=False
                matched[i]=np.zeros(len(initial),np.int64)
                continue
            q_source[int(i)]=qs
            source_census[int(i)]=next_n
            p=source_parent[i]@b/source_parent[i].sum()
            p_child=child@b/next_n
            canonical_filter[i]+=float(qs@b-p)
            canonical_sampling[i]+=float(p_child-qs@b)
            source_endpoint[i]=p_child
        survivors=np.flatnonzero(active)
        if not len(survivors):
            return {"status":"NO_SURVIVORS_UNABLE_TO_TEST","budget":budget}
        source_mean=float(np.mean(source_endpoint[survivors]))
        q_null=np.array([neutral_child_genotype_law(null_parent[i],grid)
                          for i in survivors])
        fit=calibrated_laws(q_null,b,source_mean)
        if not fit["admissible"]:
            return {
                "status":"MEAN_MATCH_BOUNDARY_UNATTAINABLE",
                "evidence_type":"exploratory_source_defined_comparator",
                "conditions":{"K":32,"generations":8,"mutation_rate":0,
                              "old_visitor_history":OLD_HISTORY,
                              "budget":budget,"draws":draws},
                "failed_at_generation":t+1,
                "target_and_bounds":fit,
                "no_biological_source_code_changed":True,
                "no_claim_about_feedback_or_ceiling":True,
            }
        for j,i in enumerate(survivors):
            q=fit["laws"][j]
            n=source_census[int(i)]
            rng=np.random.default_rng(np.random.SeedSequence([seed,200,int(i),t]))
            c=np.bincount(rng.choice(len(q),size=n,p=q),
                          minlength=len(q)).astype(np.int64)
            matched[i]=c
            p=null_parent[i]@b/null_parent[i].sum()
            p_child=float(c@b/n)
            matched_filter[i]+=float(q@b-p)
            matched_sampling[i]+=float(p_child-q@b)
            comparator_endpoint[i]=p_child
        # Conditional on the current source survival cohort. Source
        # and null means are compared at equal N in each trajectory.
        d=source_endpoint[survivors]
        z=comparator_endpoint[survivors]
        yrs={
            "generation":t+1,
            "n_source_survivors":int(len(survivors)),
            "source_mean":float(d.mean()),
            "comparator_mean":float(z.mean()),
            "mean_target_minus_realized_comparator":float(d.mean()-z.mean()),
            "calibration_parameter":fit["calibration_log_weight"],
            "calibrated_conditional_mean":fit["calibrated_conditional_mean"],
            "source_allele_frequency_variance":float(d.var(ddof=0)),
            "mean_matched_comparator_frequency_variance":float(z.var(ddof=0)),
            "source_fixation_fraction":float(np.mean(np.isclose(d,1.,atol=1e-12))),
            "comparator_fixation_fraction":float(np.mean(np.isclose(z,1.,atol=1e-12))),
        }
        years.append(yrs)
    survivor=np.flatnonzero(active)
    s=source_endpoint[survivor]
    n=comparator_endpoint[survivor]
    ds=canonical_filter[survivor]
    es=canonical_sampling[survivor]
    dn=matched_filter[survivor]
    en=matched_sampling[survivor]
    np.testing.assert_allclose(start+ds+es,s,atol=1e-11,rtol=0)
    np.testing.assert_allclose(start+dn+en,n,atol=1e-11,rtol=0)
    parts_source=variance_parts(ds,es)
    parts_null=variance_parts(dn,en)
    return {
        "status":"EXPLORATORY_MEAN_MATCHED_CEILING_COMPARATOR_COMPLETE",
        "evidence_type":"source_outcome_calibrated_engineering_simulation_not_observations",
        "conditions":{
            "K":32,"generations":8,"mutation_rate":0,
            "adult_survival":0,"seed_immigration":0,
            "ovule_budget":budget,"reproductive_setting":"prior_selfing",
            "old_visitor_history":OLD_HISTORY,"environment":"near",
            "old_visitor_sha256":digest,
            "independent_visitor_histories":1,
            "nested_demographic_trajectories":draws,
            "n_surviving":int(len(survivor)),
            "n_extinct":int(draws-len(survivor)),
            "source_model3_biology_edited":False,
            "comparator_intentionally_changes_mating_payoffs":True,
            "comparator_reweighted_after_exposure_to_source_outcomes":True,
            "same_realized_census_every_year":True,
            "no_confirmatory_cohorts_used":True,
        },
        "source": {
            "assurance_endpoint_mean":float(s.mean()),
            "assurance_endpoint_variance":float(s.var(ddof=0)),
            "assurance_high_allele_fixation_fraction":float(np.mean(np.isclose(s,1.,atol=1e-12))),
            "cumulative_frequency_variance":parts_source,
        },
        "mean_matched_comparator": {
            "assurance_endpoint_mean":float(n.mean()),
            "assurance_endpoint_variance":float(n.var(ddof=0)),
            "assurance_high_allele_fixation_fraction":float(np.mean(np.isclose(n,1.,atol=1e-12))),
            "cumulative_frequency_variance":parts_null,
        },
        "endpoint": {
            "source_minus_comparator_mean":float((s-n).mean()),
            "source_minus_comparator_mean_mc_se":float(
                (s-n).std(ddof=1)/np.sqrt(len(s))),
            "source_minus_comparator_variance":float(s.var(ddof=0)-n.var(ddof=0)),
            "comparator_variance_over_source_variance":float(n.var(ddof=0)/s.var(ddof=0))
                if s.var(ddof=0)>0 else None,
        },
        "per_generation":years,
        "interpretation_limits":[
            "The comparison is post-outcome mean calibrated and is an exploratory sensitivity comparator, NOT independent confirmatory inference.",
            "Uniform per-year exponential bias is deliberately different biology from source Model3 pollen, mating and fitness.",
            "Genotype frequencies and exact Mendelian support are preserved; extinct alleles cannot be resurrected by weighting.",
            "Matching target mean and census does not match the complete parental genotype distribution or frequency-dependent selection.",
            "Variance/covariance differences cannot uniquely separate frequency ceiling, stochasticity, or biological feedback.",
            "The result is conditional on one old visitor environment, no natural observational data, no SDE/SPDE validation.",
        ],
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    parser.add_argument("--draws",type=int,default=512)
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    out=run_mean_matched(budget=args.budget,draws=args.draws)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps({
        "status":out["status"],"budget":args.budget,
        "source":out.get("source"),
        "comparator":out.get("mean_matched_comparator"),
        "endpoint":out.get("endpoint"),
        "failed_at_generation":out.get("failed_at_generation"),
    }))


if __name__=="__main__":
    main()
