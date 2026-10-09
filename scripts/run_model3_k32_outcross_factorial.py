"""Autonomous 2^3 outcross-factor interaction screen on frozen K32 Model3.

Original arm is EXACT canonical genotype-count Markov process. Other arms
intentionally change ONE OR MULTIPLE source-ledger donor-export (E),
visitor/recipient routing (R), and maternal seed-provisioning (M) factors.
Every arm preserves at its own parental state the canonical viable self-seed
masses and total viable outcross-seed mass; extinct alleles never resurrect.
All intermediate edge support remains the ORIGINAL ledger support.

We calculate full factorial / Möbius contrasts for unconditional genotype
richness, allele types lost, occupancy, and occupancy-WEIGHTED assurance
dosage and heterozygosity (zero after extinction is an occupancy-weighted
product, not a fabricated trait mean for extinct populations). Survivor-
only trait means are reported separately and must not be used for factorial
comparisons across differently conditioned survival sets.

The factorial contrasts are effects of precisely specified artificial
reproductive operators; NOT independent causal field pollinator effects,
true ecological replication, or the prior one-step Shapley estimands.
Only archived visitor seed 26110601 (near), K32, u=0, eight generations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import (
    genotype_count_markov_step, genotype_counts_to_canonical_state,
    offspring_genotype_distribution,
)
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import (
    K, GENERATIONS, MUTATION_RATE, OLD_HISTORY,
)
from scripts.run_model3_k32_outcross_ablation import (
    reweighted_outcross, ARMS, _snapshot,
)

FACTOR_NAMES=("donor_export","visitor_routing","maternal_provisioning")
MASK_LABELS={0:"original_canonical",1:"equal_donor",2:"equal_routing",
             3:"equal_donor_and_routing",4:"equal_maternal",
             5:"equal_donor_and_maternal",6:"equal_routing_and_maternal",
             7:"equal_all_three"}
SINGLE_ARM={1:ARMS[1],2:ARMS[2],4:ARMS[3]}
FACT_METRICS=(
    "occupied",
    "genotype_richness",
    "allele_types_lost",
    "assurance_occupancy_weighted",
    "assurance_heterozygosity_occupancy_weighted",
    "fixation_occupancy_weighted",
)


def combine_outcross_factors(ledger,mask):
    """Renormalized source-ledger outcross under a declared three-bit mask."""
    if type(mask) is not int or not 0<=mask<=7:
        raise ValueError("factor intervention mask must be in [0,7]")
    original=np.asarray(ledger.outcross,dtype=float)
    if mask==0 or original.sum()==0:
        return original.copy()
    if mask in SINGLE_ARM:
        # Exact compatibility of the one-factor experiment is essential.
        return reweighted_outcross(ledger,SINGLE_ARM[mask])
    n=len(original)
    exported=np.asarray(ledger.exported,float)
    delivered=np.asarray(ledger.delivered,float)
    receipt=delivered.sum(axis=0)
    female=np.asarray(ledger.maternal-ledger.self_viable,float)
    if (female < -1e-11).any():
        raise ArithmeticError("invalid source female outcross intensity")
    female=np.maximum(female,0.)
    r=np.divide(delivered,exported[:,None],
                out=np.zeros_like(delivered),where=exported[:,None]>0)
    m=np.divide(female,receipt,out=np.zeros_like(receipt),where=receipt>0)
    e=exported.copy()
    if mask&1:
        active=e>0
        if active.any():
            e[active]=float(e[active].mean())
    if mask&2:
        for i in range(n):
            active=r[i]>0
            if active.any():
                r[i,active]=float(r[i].sum())/int(active.sum())
    if mask&4:
        active=receipt>0
        if active.any():
            m[active]=float(female[active].sum())/float(receipt[active].sum())
    altered=e[:,None]*r*m[None,:]
    np.fill_diagonal(altered,0.)
    if not np.isfinite(altered).all() or altered.min()<-1e-12:
        raise ArithmeticError("invalid alternative source pair weights")
    altered=np.maximum(0.,altered)
    if np.any((original==0)&(altered>1e-12)):
        raise ArithmeticError("experiment created an unobserved source pair edge")
    if not altered.sum()>0:
        raise ArithmeticError("positive source outcross disappeared")
    altered*=float(original.sum())/float(altered.sum())
    if (not np.isclose(altered.sum(),original.sum(),atol=1e-10,rtol=0)
            or np.any(np.diag(altered)!=0)):
        raise ArithmeticError("source total outcross or self-exclusion violated")
    return altered


def step_with_mask(counts,grid,visitors,cfg,rng,year,mask):
    if type(mask) is not int or not 0<=mask<=7:
        raise ValueError("unknown factor combination")
    if (cfg.capacity!=K or cfg.mutation_rate!=0 or cfg.survival!=0
            or cfg.seed_arrival.supply!=0):
        raise ValueError("restricted canonical eight-year case only")
    c=np.asarray(counts)
    if (c.shape!=(len(grid.genotypes),) or c.dtype.kind not in "iu"
            or np.any(c<0) or c.sum()>K):
        raise ValueError("invalid source parent genotype counts")
    if mask==0:
        return genotype_count_markov_step(c,grid,visitors,cfg,rng,year=year)
    source=genotype_counts_to_canonical_state(c,grid,year,K)
    if not len(source.ids):
        return np.zeros(len(c),dtype=np.int64)
    ledger=reproduce(source,visitors,cfg)
    altered=combine_outcross_factors(ledger,mask)
    parents=altered.copy()
    parents[np.diag_indices(len(source.ids))]+=ledger.self_viable
    expected=float(ledger.outcross.sum()+ledger.self_viable.sum())
    if not np.isclose(parents.sum(),expected,atol=1e-10,rtol=0):
        raise ArithmeticError("conditional birth intensity changed")
    n=min(int(rng.poisson(expected)),K)
    if n==0 or expected==0:
        return np.zeros(len(c),dtype=np.int64)
    q=offspring_genotype_distribution(source,parents/float(parents.sum()),grid)
    labels=rng.choice(len(q),size=n,replace=True,p=q/float(q.sum()))
    child=np.bincount(labels,minlength=len(q)).astype(np.int64)
    if int(child.sum())!=n or np.any(child<0):
        raise ArithmeticError("finite Mendelian offspring mass mismatch")
    return child


def _row_values(c,basis,het):
    s=_snapshot(c,basis,het)
    alive=s["occupied"]
    return np.array([
        alive,s["genotype_richness"],s["allele_types_lost"],
        s["assurance"] if alive else 0.,
        s["heterozygote_fraction"] if alive else 0.,
        s["assurance_fixed"] if alive else 0.,
    ],dtype=float)


def factorial_terms(raw_by_mask):
    """Per-path Möbius transform with exact inclusion-exclusion identity."""
    if set(raw_by_mask)!=set(range(8)):
        raise ValueError("all eight interventions required")
    arrays={m:np.asarray(v,float) for m,v in raw_by_mask.items()}
    shape=arrays[0].shape
    if any(x.shape!=shape or not np.isfinite(x).all() for x in arrays.values()):
        raise ValueError("factorial responses must have identical finite shape")
    contrasts={}
    for m in range(8):
        ans=np.zeros(shape,float)
        for s in range(8):
            if (s&m)==s:
                ans+=(-1)**((m^s).bit_count())*arrays[s]
        contrasts[m]=ans
    np.testing.assert_allclose(
        sum((contrasts[m] for m in range(8)),np.zeros(shape,float)),
        arrays[7],atol=1e-12,rtol=0)
    return contrasts


def _statistics(values):
    a=np.asarray(values,float)
    return {"mean":float(a.mean()),"demographic_mc_se":float(
        a.std(ddof=1)/np.sqrt(len(a))) if len(a)>1 else None}


def run_factorial(*,budget=8.,draws=512,seed=420261017):
    if (budget not in (3.,8.) or type(draws) is not int or
            not 16<=draws<=2048 or type(seed) is not int or seed<0):
        raise ValueError("frozen K32 old-history budgets and draws only")
    first,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    d=load_design(DEFAULT_DESIGN)
    source=source_config(d,"prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(source,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(source.seed_arrival,supply=0.))
    if cfg.assurance_timing!="prior":
        raise AssertionError("source prior-selfing changed")
    visits=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    if len(visits)!=8:
        raise AssertionError("old visitor horizon unavailable")
    checksum=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()+
        v.effectiveness.tobytes() for v in visits)).hexdigest()
    basis=allele_frequency_basis(grid)
    het=(basis[:,2]==.5).astype(float)
    trajectory={m:np.repeat(first[None,:],draws,axis=0)
                for m in range(8)}
    all_years={}
    for t in range(GENERATIONS):
        records={}
        for mask in range(8):
            state=trajectory[mask]
            for i in range(draws):
                rng=np.random.default_rng(
                    np.random.SeedSequence([seed,i,t]))
                state[i]=step_with_mask(
                    state[i],grid,visits[t],cfg,rng,t,mask)
            records[mask]=np.asarray(
                [_row_values(c,basis,het) for c in state],float)
        expansions=factorial_terms(records)
        metric_results={}
        for k,name in enumerate(FACT_METRICS):
            vals={str(m):_statistics(records[m][:,k])
                  for m in range(8)}
            main_and_interaction={str(m):_statistics(expansions[m][:,k])
                                  for m in range(1,8)}
            net=records[7][:,k]-records[0][:,k]
            np.testing.assert_allclose(
                sum(expansions[m][:,k] for m in range(1,8)),
                net,atol=1e-12,rtol=0)
            single_total=sum(expansions[m][:,k] for m in (1,2,4))
            interaction_total=sum(expansions[m][:,k] for m in (3,5,6,7))
            np.testing.assert_allclose(single_total+interaction_total,
                                       net,atol=1e-12,rtol=0)
            metric_results[name]={
                "each_arm":vals,
                "factorial_components":main_and_interaction,
                "sum_of_three_single_factor_effects":_statistics(single_total),
                "aggregate_pairwise_and_three_way_interaction":_statistics(interaction_total),
                "all_three_minus_original":_statistics(net),
                "max_additivity_identity_error":float(np.max(np.abs(
                    sum(expansions[m][:,k] for m in range(1,8))-net))),
            }
        per_arm={}
        for m in range(8):
            rs=records[m]
            survivors=rs[:,0]>0
            per_arm[str(m)]={
                "name":MASK_LABELS[m],
                "n_survivors":int(survivors.sum()),
                "n_extinct":int(draws-survivors.sum()),
                "mean_richness_all":float(rs[:,1].mean()),
                "mean_lost_alleles_all":float(rs[:,2].mean()),
                "mean_high_assurance_given_survival":float(
                    rs[survivors,3].mean()) if survivors.any() else None,
                "mean_heterozygosity_given_survival":float(
                    rs[survivors,4].mean()) if survivors.any() else None,
                "fixation_given_survival":float(
                    rs[survivors,5].mean()) if survivors.any() else None,
            }
        all_years[str(t+1)]={"arms":per_arm,"metrics":metric_results}
    return {
        "status":"SOURCE_EXACT_K32_OLD_HISTORY_FULL_2x2x2_FACTORIAL",
        "evidence_type":"one_old_visitor_history_engineered_counterfactual_demographic_MC",
        "conditions":{
            "K":32,"mutation_rate":0,"generations":8,
            "adult_survival":0,"seed_immigration":0,
            "ovule_budget":budget,
            "old_visitor_history":OLD_HISTORY,
            "environment":"near","visitor_digest":checksum,
            "independent_visitor_histories":1,
            "nested_demographic_paths_per_arm":draws,
            "frozen_four_founder_27_joint_genotype_support":True,
            "canonical_source_biology_modified":False,
            "alternative_reproductive_operators_intentionally_modified":True,
            "self_seed_intensity_and_total_outcross_seed_intensity_preserved_at_each_current_parent":True,
            "outcross_parent_pair_support_preserved":True,
            "prospective_confirmatory_cohorts_used":False,
            "same_seed_by_path_and_year_not_exact_offspring_coupling":True,
        },
        "factors":FACTOR_NAMES,
        "masks":{str(m):MASK_LABELS[m] for m in range(8)},
        "factorial_order":"Möbius inclusion-exclusion on full 2^3 table; each component and interaction includes higher-order state feedback; do NOT interpret as one-step Shapley",
        "metric_scopes":{
            "occupied":"binary occupation of source or counterfactual",
            "genotype_richness":"unconditional count, 0 if extinct",
            "allele_types_lost":"unconditional count of 6 initial allele types, 6 if extinct",
            "assurance_occupancy_weighted":"occupancy TIMES assurance allele frequency; zero when extinct is product, not a fake trait mean",
            "assurance_heterozygosity_occupancy_weighted":"occupancy TIMES frequency of heterozygote plants",
            "fixation_occupancy_weighted":"occupancy TIMES indicator of assurance high-allele fixation",
        },
        "years":all_years,
        "interpretation_limits":[
            "Main and interaction terms are exact algebra of declared eight-year simulated autonomous counterfactual response means; they are not independent causal biological effects.",
            "All controls renormalize same-parent expected seed intensity and preserve original mating edge support and viable selfed-seed masses.",
            "Genotype feedback over eight years makes combination effects non-additive even if original factorization is multiplicative.",
            "This is a completely new factorial screen motivated by the one-factor results and is exploratory/post-outcome within one old visitor environment.",
            "No held-out ecological visitor histories, natural observation, independent environments, source Model3 edits, geographical INLA or SDE/SPDE validation.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=512)
    a=p.parse_args()
    result=run_factorial(budget=a.budget,draws=a.draws)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    final=result["years"]["8"]["metrics"]
    print(json.dumps({
        "status":result["status"],"budget":a.budget,
        "assurance_all_three_minus_source":final["assurance_occupancy_weighted"]["all_three_minus_original"],
        "richness_all_three_minus_source":final["genotype_richness"]["all_three_minus_original"],
        "richness_factorial_components":final["genotype_richness"]["factorial_components"],
    }))


if __name__=="__main__":
    main()
