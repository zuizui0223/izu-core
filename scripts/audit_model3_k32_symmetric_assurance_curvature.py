"""Same-heterozygote bidirectional Model 3 assurance response at frozen K32.

The earlier one-copy perturbation experiment sampled a potentially different
source genotype for high->low and low->high. This follow-up selects the SAME
ONE diploid plant genotype heterozygous at assurance and makes two separate
counterfactual censuses: its assurance pair becomes low/low and high/high.
Thus n, non-assurance traits, and all background genotypes are identical.

Measure the original canonical source conditional next-child allele frequency
for original, plus and minus states and compare to a full-Mendelian neutral
mating operator with an externally tilted assurance dosage, fitted ONLY
to the original parent mean and held fixed in both perturbations.

An observed curvature or response slope contrast is a finite source
operator sensitivity, NOT adaptive stabilization, an independently
identified selection coefficient, or an SDE/SPDE.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_count_markov_step
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_k32_local_assurance_response import paired_local_slope
from scripts.run_model3_three_arm_k32_old_history import (
    K, GENERATIONS, OLD_HISTORY,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure

CHECKPOINTS=(2,4,6,7)


def symmetric_heterozygote_variants(counts,grid,rng):
    """Both allele flips on SAME randomly sampled source heterozygote."""
    c=np.asarray(counts)
    if (c.ndim!=1 or c.shape!=(len(grid.genotypes),) or
            c.dtype.kind not in "iu" or (c<0).any() or
            not isinstance(rng,np.random.Generator)):
        raise ValueError("invalid source diploid genotype counts/RNG")
    g_het=np.array([
        np.isclose(grid.genotypes[g,2,0],.25,atol=1e-12,rtol=0)
        and np.isclose(grid.genotypes[g,2,1],.75,atol=1e-12,rtol=0)
        for g in range(len(c))
    ])
    weights=np.where(g_het,c,0)
    if not int(weights.sum()):
        return None
    original=int(rng.choice(len(c),p=weights/weights.sum()))
    out=[]
    for pair in ((.25,.25),(.75,.75)):
        genotype=grid.genotypes[original].copy()
        genotype[2,:]=pair
        new_type=np.flatnonzero(np.isclose(
            grid.genotypes,genotype[None,:,:],atol=1e-12,rtol=0
        ).all(axis=(1,2)))
        if len(new_type)!=1:
            raise ArithmeticError("post perturb genotype not in frozen support")
        variant=c.copy()
        variant[original]-=1
        variant[int(new_type[0])]+=1
        if int(variant.sum())!=int(c.sum()) or (variant<0).any():
            raise AssertionError("one plant perturbation corrupts finite count")
        out.append(variant)
    low,high=out
    n=int(c.sum())
    b=allele_frequency_basis(grid)[:,2]
    assert n>0
    np.testing.assert_allclose(
        [(low-c)@b/n,(high-c)@b/n],
        [-1/(2*n),1/(2*n)],atol=1e-12,rtol=0
    )
    base_traits=c@grid.genotypes.mean(axis=2)
    np.testing.assert_allclose(
        low@grid.genotypes.mean(axis=2)-base_traits,
        [0.,0.,-.25],atol=1e-12,rtol=0
    )
    np.testing.assert_allclose(
        high@grid.genotypes.mean(axis=2)-base_traits,
        [0.,0.,.25],atol=1e-12,rtol=0
    )
    return low,high


def symmetric_response(counts,grid,visitor,config,year,rng):
    variants=symmetric_heterozygote_variants(counts,grid,rng)
    if variants is None:
        return {"status":"NO_HETEROZYGOTE_FOR_TWO_SIDED_RESPONSE"}
    low,high=variants
    a=paired_local_slope(counts,low,grid,visitor,config,year)
    b=paired_local_slope(counts,high,grid,visitor,config,year)
    if (a["status"]!="BASELINE_MEAN_MATCHED_LOCAL_DERIVATIVE" or
            b["status"]!="BASELINE_MEAN_MATCHED_LOCAL_DERIVATIVE"):
        return {"status":"BASELINE_MATCH_UNAVAILABLE",
                "statuses":[a["status"],b["status"]]}
    if not np.isclose(a["baseline_assurance_log_weight"],
                      b["baseline_assurance_log_weight"],atol=1e-11,rtol=0):
        raise AssertionError("same-source baseline got different control tilt")
    if not np.isclose(a["baseline_source_next_allele_frequency"],
                      b["baseline_source_next_allele_frequency"],
                      atol=1e-12,rtol=0):
        raise AssertionError("same source baseline has inconsistent offspring mean")
    return {
        "status":"SYMMETRIC_HETEROZYGOTE_DIRECTIONAL_RESPONSE",
        "parent_n":int(np.asarray(counts).sum()),
        "parent_allele_frequency":a["baseline_assurance_frequency"],
        "source_down_response_slope":a["source_response_slope"],
        "source_up_response_slope":b["source_response_slope"],
        "control_down_response_slope":a["baseline_mean_matched_tilt_slope"],
        "control_up_response_slope":b["baseline_mean_matched_tilt_slope"],
        "down_source_minus_control_slope":a["source_minus_null_response_slope"],
        "up_source_minus_control_slope":b["source_minus_null_response_slope"],
        "source_central_slope":float(
            .5*(a["source_response_slope"]+b["source_response_slope"])),
        "control_central_slope":float(
            .5*(a["baseline_mean_matched_tilt_slope"]+
                b["baseline_mean_matched_tilt_slope"])),
        "source_versus_control_central_slope":float(.5*(
            a["source_minus_null_response_slope"]+
            b["source_minus_null_response_slope"])),
        # qplus + qminus - 2qbase: discrete curvature in next expected
        # allele frequency; not a unit-free physiological effect.
        "source_symmetric_second_difference":float(
            b["perturbed_source_next_allele_frequency"]+
            a["perturbed_source_next_allele_frequency"]-
            2*a["baseline_source_next_allele_frequency"]),
        "control_symmetric_second_difference":float(
            b["perturbed_null_next_allele_frequency"]+
            a["perturbed_null_next_allele_frequency"]-
            2*a["baseline_null_next_allele_frequency"]),
        "matched_baseline_assurance_mean":
            a["baseline_source_next_allele_frequency"],
    }


def _summary(rows):
    if not rows:
        return {"n":0,"mean_source_vs_control_central_slope":None,
                "mean_source_minus_control_second_difference":None}
    keys=[
        "source_down_response_slope","source_up_response_slope",
        "control_down_response_slope","control_up_response_slope",
        "down_source_minus_control_slope","up_source_minus_control_slope",
        "source_central_slope","control_central_slope",
        "source_versus_control_central_slope",
        "source_symmetric_second_difference",
        "control_symmetric_second_difference",
    ]
    a=np.asarray([[r[k] for k in keys] for r in rows])
    if not np.isfinite(a).all():raise ArithmeticError("non-finite local assay")
    mapping=dict(zip(keys,a.mean(axis=0).tolist()))
    curvature_diff=a[:,-2]-a[:,-1]
    return {
        "n":len(rows),
        **{"mean_"+k:v for k,v in mapping.items()},
        "mean_source_minus_control_second_difference":float(curvature_diff.mean()),
        "mc_se_central_slope_source_minus_control":float(
            a[:,8].std(ddof=1)/np.sqrt(len(a))) if len(a)>1 else None,
        "mc_se_curvature_diff":float(
            curvature_diff.std(ddof=1)/np.sqrt(len(a))) if len(a)>1 else None,
        "fraction_source_central_slope_less_than_control":float(
            np.mean(a[:,6]<a[:,7])),
    }


def run_symmetric(*,budget=8.,draws=128,seed=420261015):
    if (budget not in (3.,8.) or type(draws) is not int
            or not 16<=draws<=512 or type(seed) is not int or seed<0):
        raise ValueError("source-locked symmetric perturbation input")
    original,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    d=load_design(DEFAULT_DESIGN)
    biological=source_config(d,"prior_selfing",0.,"evolving")
    cfg=replace(biological,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(biological.seed_arrival,supply=0.))
    if cfg.assurance_timing!="prior" or len(grid.genotypes)!=27:
        raise AssertionError("canonical assurance source structure has changed")
    visitors=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    assert len(visitors)==8
    vh_hash=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()
        +v.effectiveness.tobytes() for v in visitors)).hexdigest()
    counts=np.repeat(original[None,:],draws,axis=0)
    checkpoints={}
    for year in range(GENERATIONS):
        if year in CHECKPOINTS:
            results=[]
            inadmissible={}
            occupied=0
            for rep,state in enumerate(counts):
                if not int(state.sum()):continue
                occupied+=1
                r=symmetric_response(
                    state,grid,visitors[year],cfg,year,
                    np.random.default_rng(np.random.SeedSequence(
                        [seed,rep,year,331])))
                if r["status"]=="SYMMETRIC_HETEROZYGOTE_DIRECTIONAL_RESPONSE":
                    results.append(r)
                else:
                    key=r["status"]
                    inadmissible[key]=inadmissible.get(key,0)+1
            checkpoints[str(year+1)]={
                "n_occupied":occupied,
                "n_comparable_heterozygote_states":len(results),
                "ineligible_states":inadmissible,
                "same_genotype_bidirectional_summary":_summary(results),
            }
        counts=np.asarray([
            genotype_count_markov_step(
                c,grid,visitors[year],cfg,
                np.random.default_rng(np.random.SeedSequence(
                    [seed,rep,year,101])),year=year)
            for rep,c in enumerate(counts)],dtype=np.int64)
    return {
        "status":"SOURCE_SAME_HETEROZYGOTE_SYMMETRIC_RESPONSE_AUDIT",
        "evidence_type":"one_old_history_engineered_exact_conditional_kernels",
        "conditions":{
            "K":32,"mutation_rate":0,"generations":8,
            "adult_survival":0,"seed_immigration":0,
            "ovule_budget":budget,"setting":"prior_selfing",
            "old_visitor_history":OLD_HISTORY,"environment":"near",
            "old_visitor_sha256":vh_hash,
            "independent_visitor_histories":1,
            "nested_demographic_source_paths":draws,
            "parent_genotype_identical_in_two_flip_orientations":True,
            "parent_census_identical_in_all_three_states":True,
            "baseline_comparator_tilt_frozen_under_both_flips":True,
            "comparator_deliberately_alters_reproduction":True,
            "original_model3_biology_modified":False,
            "new_confirmatory_cohorts_reused":False,
        },
        "checkpoints":checkpoints,
        "limitations":[
            "This is a pair of exact conditional-source numerical interventions on an individual heterozygous at assurance, not ecological manipulation.",
            "Same individual background controls a major source of high/low orientation asymmetry from selecting different genotypes, but source frequency response includes all other nonlinear mating ecology.",
            "Fully fixed assurance sources have no heterozygote and cannot identify a local baseline-mean-matched comparator tilt; such states are excluded.",
            "The mean-matched directional control deliberately changes biological mating weights and is post-outcome fitted to each source baseline.",
            "Repeated demographic trajectories are nested under one archived visitor history; not independent island/ecological replication.",
            "A negative central slope or curvature contrast alone does not establish stabilizing selection or a full SDE/SPDE."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=128)
    a=p.parse_args()
    data=run_symmetric(budget=a.budget,draws=a.draws)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":data["status"],"budget":a.budget,
        "symmetric_by_year":{
            y:{
                "n":v["n_comparable_heterozygote_states"],
                "source_control_central":v["same_genotype_bidirectional_summary"][
                    "mean_source_versus_control_central_slope"],
                "curvature_contrast":v["same_genotype_bidirectional_summary"][
                    "mean_source_minus_control_second_difference"],
            } for y,v in data["checkpoints"].items()
        }
    }))


if __name__=="__main__":
    main()
