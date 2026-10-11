"""Held-out *demographic* replication for source-calibrated mean-matched control.

Split 512 demographic trajectories into fixed train 0..255 and holdout
256..511. On EACH training generation, calibrate a single external
assurance tilt using ONLY training-source survivors and TRAINING-comparator
parental states. Apply that frozen per-year coefficient to independent
holdout source/comparator genetic draws, NEVER reading holdout outcomes
to adjust coefficients. Source biological operators are unchanged.

This remains one archived ecological visitor history (26110601), not an
independent visitor-historical or natural-island confirmation. The null
deliberately changes mating/fitness and imposes source census each year.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_k32_mean_matched_ceiling import (
    calibrated_laws, paired_bootstrap_spread, tilted_offspring_law,
    variance_parts,
)
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


def split_indices(total):
    if type(total) is not int or total<32 or total%2:
        raise ValueError("even demographic cohort with >=32 paths required")
    return np.arange(total//2),np.arange(total//2,total)


def _summarize_pair(which, alive, source_last, control_last,
                    src_dir,src_noise,ctrl_dir,ctrl_noise, *,
                    boot_seed):
    ids=which[alive[which]]
    if len(ids)<16:
        return {"status":"INSUFFICIENT_SURVIVORS","n_survived":int(len(ids))}
    s,c=source_last[ids],control_last[ids]
    sd,sn=src_dir[ids],src_noise[ids]
    cd,cn=ctrl_dir[ids],ctrl_noise[ids]
    a,b=variance_parts(sd,sn),variance_parts(cd,cn)
    mc=paired_bootstrap_spread(s,c,sd,sn,cd,cn,seed=boot_seed,
                               bootstrap_draws=512)
    return {
        "status":"COMPARABLE",
        "n_survived":int(len(ids)),
        "n_source_extinct":int(len(which)-len(ids)),
        "source_mean":float(s.mean()),
        "control_mean":float(c.mean()),
        "source_minus_control_mean":float((s-c).mean()),
        "source_minus_control_mean_mc_se":float((s-c).std(ddof=1)/np.sqrt(len(s))),
        "source_variance":float(s.var(ddof=0)),
        "control_variance":float(c.var(ddof=0)),
        "source_minus_control_variance":float(s.var(ddof=0)-c.var(ddof=0)),
        "source_fixation_fraction":float(np.isclose(s,1.,atol=1e-12).mean()),
        "control_fixation_fraction":float(np.isclose(c,1.,atol=1e-12).mean()),
        "source_variance_parts":a,
        "control_variance_parts":b,
        "source_minus_control_twice_covariance":float(
            a["two_times_covariance"]-b["two_times_covariance"]),
        "paired_demographic_mc":mc,
    }


def run_holdout(*,budget=8.,draws=512,seed=420261013,train_half="first"):
    if (budget not in (3.,8.) or type(draws) is not int or
            not 32<=draws<=2048 or draws%2 or type(seed) is not int or seed<0
            or train_half not in ("first","second")):
        raise ValueError("K32 old-history 50/50 demographic split only")
    first_half,second_half=split_indices(draws)
    train,holdout=(first_half,second_half) if train_half=="first" else (second_half,first_half)
    first,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    source_design=load_design(DEFAULT_DESIGN)
    source=source_config(source_design,"prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(source,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(source.seed_arrival,supply=0.))
    if cfg.assurance_timing!="prior":
        raise AssertionError("source assurance timing changed")
    old=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    if len(old)!=8:raise AssertionError("old history too short")
    old_hash=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()+
        v.effectiveness.tobytes() for v in old)).hexdigest()
    b=allele_frequency_basis(grid)[:,2]
    start=float(first@b/first.sum())

    src=np.repeat(first[None,:],draws,axis=0)
    ctrl=np.repeat(first[None,:],draws,axis=0)
    live=np.ones(draws,bool)
    src_dir=np.zeros(draws);src_noise=np.zeros(draws)
    ctrl_dir=np.zeros(draws);ctrl_noise=np.zeros(draws)
    src_last=np.full(draws,np.nan);ctrl_last=np.full(draws,np.nan)
    years=[]
    for t in range(8):
        src_parent=src.copy()
        ctrl_parent=ctrl.copy()
        # SOURCE is generated independently of control and never changed.
        next_census=np.zeros(draws,int)
        source_q={}
        for i in np.flatnonzero(live):
            intensity,q=canonical_conditional_kernel(
                src_parent[i],grid,old[t],cfg,t)
            child=genotype_count_markov_step(
                src_parent[i],grid,old[t],cfg,
                np.random.default_rng(np.random.SeedSequence([seed,100,int(i),t])),
                year=t)
            src[i]=child
            n=int(child.sum())
            next_census[i]=n
            if not n:
                live[i]=False
                ctrl[i]=np.zeros(len(first),dtype=np.int64)
                continue
            p=float(src_parent[i]@b/src_parent[i].sum())
            f=float(child@b/n)
            src_dir[i]+=float(q@b-p)
            src_noise[i]+=float(f-q@b)
            src_last[i]=f
            source_q[int(i)]=q
        good_train=train[live[train]]
        good_holdout=holdout[live[holdout]]
        if not len(good_train) or not len(good_holdout):
            return {
                "status":"HOLDOUT_NOT_EVALUABLE_ZERO_SURVIVORS",
                "failed_generation":t+1,"budget":budget
            }
        source_train_target=float(np.mean(src_last[good_train]))
        # Strict firewall: NO holdout q, allele, fitness or endpoint can
        # enter the coefficient calibration.
        train_neutral_q=np.array([
            neutral_child_genotype_law(ctrl_parent[i],grid) for i in good_train])
        fitted=calibrated_laws(train_neutral_q,b,source_train_target)
        if not fitted["admissible"]:
            return {
                "status":"TRAINING_MEAN_UNATTAINABLE",
                "failed_generation":t+1,
                "budget":budget,
                "target_and_bounds":{
                    key:value for key,value in fitted.items() if key!="laws"},
            }
        theta=float(fitted["calibration_log_weight"])
        for i in np.flatnonzero(live):
            neutral=neutral_child_genotype_law(ctrl_parent[i],grid)
            q0=tilted_offspring_law(neutral,b,theta)
            n=int(next_census[i])
            sampled=np.bincount(
                np.random.default_rng(np.random.SeedSequence([seed,200,int(i),t]))
                .choice(len(q0),size=n,p=q0),
                minlength=len(q0)).astype(np.int64)
            if int(sampled.sum())!=n or n>K:
                raise ArithmeticError("source-imposed census not conserved")
            ctrl[i]=sampled
            p=float(ctrl_parent[i]@b/ctrl_parent[i].sum())
            f=float(sampled@b/n)
            ctrl_dir[i]+=float(q0@b-p)
            ctrl_noise[i]+=float(f-q0@b)
            ctrl_last[i]=f
        years.append({
            "generation":t+1,"theta_train_only":theta,
            "n_train_survivors":int(len(good_train)),
            "n_holdout_survivors":int(len(good_holdout)),
            "train_source_target":source_train_target,
            "train_control_conditional_mean":fitted["calibrated_conditional_mean"],
            "train_control_realized_mean":float(ctrl_last[good_train].mean()),
            "holdout_source_mean":float(src_last[good_holdout].mean()),
            "holdout_control_mean":float(ctrl_last[good_holdout].mean()),
            "holdout_mean_error":float(
                ctrl_last[good_holdout].mean()-src_last[good_holdout].mean()),
            "coefficient_did_not_access_holdout":True,
        })
    tr=_summarize_pair(train,live,src_last,ctrl_last,src_dir,src_noise,
                       ctrl_dir,ctrl_noise,
                       boot_seed=np.random.SeedSequence([seed,300,1]))
    ho=_summarize_pair(holdout,live,src_last,ctrl_last,src_dir,src_noise,
                       ctrl_dir,ctrl_noise,
                       boot_seed=np.random.SeedSequence([seed,300,2]))
    if tr["status"]!="COMPARABLE" or ho["status"]!="COMPARABLE":
        return {"status":"HOLDOUT_NOT_EVALUABLE_FEW_SURVIVORS",
                "budget":budget,"training":tr,"holdout":ho}
    for group,ids in (("train",train[live[train]]),
                      ("holdout",holdout[live[holdout]])):
        np.testing.assert_allclose(
            start+src_dir[ids]+src_noise[ids],
            src_last[ids],atol=1e-11,rtol=0)
        np.testing.assert_allclose(
            start+ctrl_dir[ids]+ctrl_noise[ids],
            ctrl_last[ids],atol=1e-11,rtol=0)
    return {
        "status":"K32_HELDOUT_DEMOGRAPHIC_MEAN_MATCH_EVALUATED",
        "evidence_type":"exploratory_old_history_demographic_holdout_not_new_ecology",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":8,
            "adult_survival":0,"seed_immigration":0,
            "ovule_budget":budget,
            "reproduction":"canonical_Chapter2_prior_selfing",
            "old_history":OLD_HISTORY,"environment":"near",
            "old_visitor_digest":old_hash,
            "n_independent_visitor_histories":1,
            "train_demographic_draws":int(len(train)),
            "holdout_demographic_draws":int(len(holdout)),
            "split":"first_half_train_second_half_holdout_fixed_before_fit" if train_half=="first" else "second_half_train_first_half_holdout_fixed_before_fit",
            "training_half":train_half,
            "source_biology_unchanged":True,
            "control_intentionally_differs_in_reproduction":True,
            "holdout_outcomes_used_in_calibration":False,
            "coefficient_calibration_is_post_outcome_exploratory":True,
            "confirmatory_visitor_cohorts_used":False,
        },
        "training":tr,
        "demographic_holdout":ho,
        "per_generation":years,
        "limitations":[
            "Demographic holdout does not create independent visitor/environment histories.",
            "Training estimates 8 per-year coefficients from source training outcomes; the alternative biological reproductive operator differs.",
            "The same old visitor history is shared between fit and evaluation.",
            "Near fixation and accumulated covariance remain mathematically constrained; not a unique adaptive stabilization mechanism.",
            "Held-out point estimates and bootstrap are conditional on source survival.",
            "Neither geographical INLA nor natural island/plant observations are involved.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=512)
    p.add_argument("--train-half",choices=["first","second"],default="first")
    args=p.parse_args()
    r=run_holdout(budget=args.budget,draws=args.draws,
                  train_half=args.train_half)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":r["status"],"budget":args.budget,
        "training":{k:r.get("training",{}).get(k) for k in
                    ("source_mean","control_mean","source_minus_control_variance")},
        "holdout":{k:r.get("demographic_holdout",{}).get(k) for k in
                   ("source_mean","control_mean","source_minus_control_variance",
                    "source_minus_control_twice_covariance")}
    }))


if __name__=="__main__":
    main()
