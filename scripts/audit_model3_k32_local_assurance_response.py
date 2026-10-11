"""Frozen-source local allele perturbation assay, K32, old visitor history.

Question: at SAME parental 3-locus genotype census and matched baseline
conditional next-generation assurance allele frequency, does canonical
source reproductive feedback react differently to a single assurance
allele replacement than a constant, directionally tilted neutral-mating
Mendelian model?

One genotype COPY is swapped to the nearest valid same-other-locus genotype
whose assurance diploid pair differs by ONE .25/.75 allele. N and 3-locus
non-assurance genotypes remain unchanged. The comparator's exponential
assurance-dosage tilt is fitted ONLY at the unperturbed source state, then
held fixed for the perturbed state. This compares analytic source kernels;
it is NOT an experiment measuring biological fitness or adaptation.

A SOURCE genotype census already fixed for either assurance allele makes
baseline-tilt calibration unidentified: mark as INELIGIBLE, never assign
an arbitrary tilt and advertise a stabilizing signal. One historic visitor
history 26110601, near; no confirmatory cohorts, no natural data, no
changes to canonical Model3 mating/reproduction code, no SDE/SPDE.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_k32_mean_matched_ceiling import (
    calibrated_laws, tilted_offspring_law,
)
from scripts.audit_model3_k32_neutral_census_control import neutral_child_genotype_law
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_count_markov_step
from scripts.run_model3_three_arm_k32_old_history import (
    canonical_conditional_kernel, K, GENERATIONS, OLD_HISTORY,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure

CHECKPOINTS=(2,4,6,7)
DIRS=("high_to_low","low_to_high")


def flip_one_assurance_copy(counts,grid,direction,rng):
    """One-copy perturbation of a real source plant, same n and other loci."""
    if direction not in DIRS or not isinstance(rng,np.random.Generator):
        raise ValueError("invalid one-copy direction/RNG")
    c=np.asarray(counts)
    if (c.ndim!=1 or c.shape!=(len(grid.genotypes),)
            or c.dtype.kind not in "iu" or (c<0).any()):
        raise ValueError("integer joint genotype counts required")
    from_value,to_value=((.75,.25) if direction=="high_to_low"
                         else (.25,.75))
    weights=np.array([
        int(c[g])*int(np.count_nonzero(np.isclose(
            grid.genotypes[g,2,:],from_value,atol=1e-12,rtol=0
        ))) for g in range(len(c))
    ],dtype=np.int64)
    if int(weights.sum())==0:
        return None
    g=int(rng.choice(len(c),p=weights/weights.sum()))
    altered=grid.genotypes[g].copy()
    location=np.flatnonzero(np.isclose(altered[2,:],from_value,
                                      atol=1e-12,rtol=0))
    if not len(location):
        raise AssertionError("chosen genotype has no eligible allele")
    altered[2,int(location[0])]=to_value
    altered[2]=np.sort(altered[2])
    equals=np.isclose(grid.genotypes,altered[None,:,:],
                      atol=1e-12,rtol=0).all(axis=(1,2))
    lookup=np.flatnonzero(equals)
    if len(lookup)!=1:
        raise ArithmeticError("one-allele intervention outside exact support")
    result=c.copy()
    result[g]-=1
    result[int(lookup[0])]+=1
    if int(result.sum())!=int(c.sum()) or (result<0).any():
        raise AssertionError("one-allele perturbation corrupts finite census")
    np.testing.assert_allclose(
        result@grid.genotypes.mean(axis=2)-c@grid.genotypes.mean(axis=2),
        [0.,0.,-.25 if direction=="high_to_low" else .25],
        atol=1e-12,rtol=0)
    return result


def paired_local_slope(base,changed,grid,visitor,cfg,year):
    """Exact local response: source versus BASELINE mean-matched tilt null."""
    basis=allele_frequency_basis(grid)[:,2]
    n=int(np.asarray(base).sum())
    if n<=1 or int(np.asarray(changed).sum())!=n:
        raise ValueError("source and perturbed integer parents required")
    p=float(base@basis/n)
    dp=float((changed-base)@basis/n)
    if not np.isclose(abs(dp),1/(2*n),atol=1e-12,rtol=0):
        raise ValueError("perturbation must change exactly one assurance copy")
    # At p=0 or p=1, the baseline tilt is mathematically unidentifiable.
    if not 0<p<1:
        return {"status":"BASELINE_FIXED_TILT_UNIDENTIFIABLE",
                "p":p,"n":n,"delta_p":dp}
    intensity,q0=canonical_conditional_kernel(base,grid,visitor,cfg,year)
    intensity_changed,q1=canonical_conditional_kernel(
        changed,grid,visitor,cfg,year)
    if intensity<=0 or intensity_changed<=0:
        return {"status":"NO_REPRODUCTION",
                "p":p,"n":n,"delta_p":dp}
    neutral0=neutral_child_genotype_law(base,grid)
    fit=calibrated_laws(neutral0[None,:],basis,float(q0@basis))
    if not fit["admissible"]:
        return {"status":"BASELINE_TILT_UNATTAINABLE",
                "p":p,"n":n,"delta_p":dp}
    theta=float(fit["calibration_log_weight"])
    neutral1=neutral_child_genotype_law(changed,grid)
    tilted_base=tilted_offspring_law(neutral0,basis,theta)
    tilted_changed=tilted_offspring_law(neutral1,basis,theta)
    src_base=float(q0@basis)
    src_change=float(q1@basis)
    null_base=float(tilted_base@basis)
    null_change=float(tilted_changed@basis)
    if not np.isclose(src_base,null_base,atol=1e-8,rtol=0):
        raise AssertionError("baseline source/neutral mean mismatch")
    slope_source=(src_change-src_base)/dp
    slope_null=(null_change-null_base)/dp
    return {
        "status":"BASELINE_MEAN_MATCHED_LOCAL_DERIVATIVE",
        "n":n,"baseline_assurance_frequency":p,
        "delta_parent_assurance_frequency":dp,
        "baseline_source_next_allele_frequency":src_base,
        "baseline_null_next_allele_frequency":null_base,
        "perturbed_source_next_allele_frequency":src_change,
        "perturbed_null_next_allele_frequency":null_change,
        "source_response_slope":float(slope_source),
        "baseline_mean_matched_tilt_slope":float(slope_null),
        "source_minus_null_response_slope":float(slope_source-slope_null),
        "source_directional_drift_derivative":float(slope_source-1.),
        "control_directional_drift_derivative":float(slope_null-1.),
        "baseline_assurance_log_weight":theta,
        "source_reproductive_intensity_original":float(intensity),
        "source_reproductive_intensity_changed":float(intensity_changed),
        "absolute_source_intensity_change":float(abs(intensity_changed-intensity)),
    }


def _summarize(rows):
    if not rows:
        return {"n":0,"mean_source_slope":None,
                "mean_control_slope":None,"mean_source_minus_control":None,
                "mc_se_source_minus_control":None}
    array=np.array([[x["source_response_slope"],
                     x["baseline_mean_matched_tilt_slope"],
                     x["source_minus_null_response_slope"]] for x in rows])
    return {"n":len(rows),"mean_source_slope":float(array[:,0].mean()),
            "mean_control_slope":float(array[:,1].mean()),
            "mean_source_minus_control":float(array[:,2].mean()),
            "mc_se_source_minus_control":float(
                array[:,2].std(ddof=1)/np.sqrt(len(rows))
            ) if len(rows)>1 else None,
            "sample_response_slope_min_max":{
                "source":[float(array[:,0].min()),float(array[:,0].max())],
                "control":[float(array[:,1].min()),float(array[:,1].max())]},
            "fraction_source_slope_below_control":float(np.mean(array[:,0]<array[:,1])),
            "fraction_both_slope_below_1":float(np.mean(
                (array[:,0]<1)&(array[:,1]<1))),
            }


def run_local(*,budget=8.,draws=128,seed=420261014):
    if (budget not in (3.,8.) or type(draws) is not int
        or not 16<=draws<=512 or type(seed) is not int or seed<0):
        raise ValueError("source-locked K32 one-copy perturbation scope")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    d=load_design(DEFAULT_DESIGN)
    source=source_config(d,"prior_selfing",0.,"evolving")
    cfg=replace(source,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(source.seed_arrival,supply=0.))
    if cfg.assurance_timing!="prior":
        raise AssertionError("source config does not use prior assurance")
    visitors=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    if len(visitors)!=GENERATIONS:
        raise ValueError("archived visitor history too short")
    digest=hashlib.sha256(b"".join(
        x.ids.tobytes()+x.optima.tobytes()+x.breadths.tobytes()
        +x.effectiveness.tobytes() for x in visitors)).hexdigest()
    states=np.repeat(initial[None,:],draws,axis=0)
    by_checkpoint={}
    for year in range(GENERATIONS):
        if year in CHECKPOINTS:
            records={direction:[] for direction in DIRS}
            boundary=0
            absent={direction:0 for direction in DIRS}
            for rep,c in enumerate(states):
                if not int(c.sum()):
                    continue
                basis=allele_frequency_basis(grid)[:,2]
                p=float(c@basis/c.sum())
                if p<=0 or p>=1:
                    boundary+=1
                    continue
                for di,direction in enumerate(DIRS):
                    altered=flip_one_assurance_copy(
                        c,grid,direction,
                        np.random.default_rng(np.random.SeedSequence(
                            [seed,rep,year,di,321])))
                    if altered is None:
                        absent[direction]+=1
                        continue
                    r=paired_local_slope(c,altered,grid,visitors[year],cfg,year)
                    if r["status"]=="BASELINE_MEAN_MATCHED_LOCAL_DERIVATIVE":
                        records[direction].append(r)
                    else:
                        absent[direction]+=1
            by_checkpoint[str(year+1)]={
                "generation":year+1,
                "n_occupied_parent_states":int(sum(c.sum()>0 for c in states)),
                "n_assurance_frequency_boundary_states_excluded":boundary,
                "not_admissible_per_direction":absent,
                "assurance_high_to_low":_summarize(records["high_to_low"]),
                "assurance_low_to_high":_summarize(records["low_to_high"]),
            }
        new=[]
        for rep,c in enumerate(states):
            new.append(genotype_count_markov_step(
                c,grid,visitors[year],cfg,
                np.random.default_rng(np.random.SeedSequence(
                    [seed,rep,year,101])),year=year
            ))
        states=np.array(new,dtype=np.int64)
    return {
        "status":"OLD_HISTORY_EXACT_SOURCE_LOCAL_ASSURANCE_PERTURBATION",
        "evidence_type":"simulated_source_local_derivative_vs_posthoc_matched_simple_tilt",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":GENERATIONS,
            "ovule_budget":float(budget),
            "adult_survival":0,"seed_immigration":0,
            "reproductive_setting":"canonical_Chapter2_prior_selfing",
            "old_visitor_history":OLD_HISTORY,"environment":"near",
            "old_visitor_sha256":digest,
            "independent_visitor_histories":1,
            "nested_demographic_source_paths":draws,
            "analytic_one_step_intervention":True,
            "one_assurance_allele_changed_per_state":True,
            "parent_census_and_other_loci_fixed":True,
            "frozen_baseline_matched_tilt_applied_to_perturbation":True,
            "boundary_states_excluded_from_matched_tilt":True,
            "counterfactual_alters_reproductive_operator":True,
            "canonical_model3_biology_modified":False,
            "confirmatory_history_reused":False,
        },
        "checkpoints":by_checkpoint,
        "limitations":[
            "A single assurance allele flip perturbs a complete diploid individual; the measured slope is a discrete directional state perturbation, not an infinitesimal derivative.",
            "Source directional reproduction and genotype associations remain jointly involved; no causal isolated stabilizing-selection coefficient.",
            "The comparator tilt is fit at each unperturbed source state, not out-of-sample and not a frozen source Model3 rule.",
            "Fixed-allele-frequency source states are excluded because a baseline directional tilt is mathematically unidentified.",
            "Source demographic trajectories are independent conditional on ONE old archived visitor history; no additional ecological replication.",
            "The results are a mechanistic in-silico counterfactual, not natural plant observations, a geographical analysis, or SDE/SPDE validation."
        ],
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    ap.add_argument("--draws",type=int,default=128)
    args=ap.parse_args()
    r=run_local(budget=args.budget,draws=args.draws)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":r["status"],
        "budget":args.budget,
        "checkpoint_slope_summary":{
            year:{
                k:{m:v[m] for m in ("n","mean_source_slope","mean_control_slope",
                                    "mean_source_minus_control")}
                for k,v in data.items()
                if k in ("assurance_high_to_low","assurance_low_to_high")
            } for year,data in r["checkpoints"].items()
        }
    }))


if __name__=="__main__":
    main()
