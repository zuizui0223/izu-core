"""Eight-generation controlled one-at-a-time outcross-factor interventions.

The original Model 3 arm ALWAYS executes the unchanged canonical genotype-
count Markov step. For each intervention arm we recompute unchanged canonical
reproduce() on that arm's current individual genotype state, then flatten
ONE parent-pair outcross factor in its already-defined annual ledger:

   exported donor pollen E_i
   visitor routing / recipient affinity R_ij = delivered_ij/E_i
   maternal viable outcross provisioning M_j = female_j/receipt_j

Selfed viable seeds and TOTAL viable outcross seed intensity are held fixed
AT THAT STATE by renormalizing only the modified outcross matrix. Thus the
capped-Poisson recruitment intensity and selfed-seed share are identical
between original versus perturbed law CONDITIONAL ON SAME CURRENT PARENTS,
but genotype states may diverge and hence future demographic rates diverge.

This is an explicit COUNTERFACTUAL BIOLOGICAL CHANGE; not frozen-source
Model3, not three independent causal coefficients, and not field data.
K=32, mutation=0, 8 generations; old near visitor seed 26110601 only.
Never access prospectively frozen confirmatory visitor cohorts.
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

SOURCE="original_canonical"
ARMS=(
    SOURCE,
    "equalize_donor_export",
    "equalize_visitor_routing",
    "equalize_maternal_outcross_provision",
)


def reweighted_outcross(ledger, arm):
    """Modify one original outcross factor, preserve mass, diagonal and zeros.

    This is a deliberate experiment on reproductive weights. The source
    reproducer and all seed/Mendelian inheritance operators are untouched.
    """
    if arm not in ARMS:
        raise ValueError("unapproved reproductive intervention")
    original=np.asarray(ledger.outcross,float)
    if arm==SOURCE:
        return original.copy()
    n=len(original)
    mass=float(original.sum())
    if mass==0:
        return original.copy()
    exported=np.asarray(ledger.exported,float)
    delivered=np.asarray(ledger.delivered,float)
    receipt=delivered.sum(axis=0)
    female=np.asarray(ledger.maternal-ledger.self_viable,float)
    if np.any(female < -1e-11):
        raise ArithmeticError("original source viable outcross seeds negative")
    female=np.maximum(0.,female)
    routing=np.divide(delivered,exported[:,None],out=np.zeros_like(delivered),
                      where=exported[:,None]>0)
    mother=np.divide(female,receipt,out=np.zeros_like(receipt),where=receipt>0)
    e=exported.copy()
    r=routing.copy()
    m=mother.copy()
    if arm=="equalize_donor_export":
        active=e>0
        if active.any():
            e[active]=e[active].mean()
    elif arm=="equalize_visitor_routing":
        # Per-donor received-pollen share remains unchanged, and only
        # the distribution among its ORIGINAL positive recipient edges
        # is made uniform. No new mating edge is introduced.
        for i in range(n):
            mask=r[i]>0
            if mask.any():
                r[i,mask]=float(r[i].sum())/int(mask.sum())
    elif arm=="equalize_maternal_outcross_provision":
        active=receipt>0
        if active.any():
            m[active]=float(np.sum(female[active]))/float(np.sum(receipt[active]))
    altered=e[:,None]*r*m[None,:]
    np.fill_diagonal(altered,0.)
    if (not np.isfinite(altered).all() or
            np.any(altered<-1e-12) or altered.sum()<=0):
        raise ArithmeticError("counterfactual outcross lost positive mass")
    altered=np.maximum(altered,0.)
    # Keep original biological support exactly: no 'rescue' by creating
    # a previously absent recipient or donor relationship.
    if np.any((original==0)&(altered>1e-12)):
        raise ArithmeticError("counterfactual created absent mating link")
    altered*=mass/float(altered.sum())
    if not np.isclose(altered.sum(),mass,rtol=0,atol=1e-10):
        raise ArithmeticError("outcross seed intensity was not preserved")
    if not np.all(np.diag(altered)==0):
        raise ArithmeticError("individual self-pollen exclusion violated")
    return altered


def step_with_intervention(counts,grid,visitors,cfg,rng,year,arm):
    """Exact finite offspring sample with alternative ONE mating component."""
    if arm not in ARMS or not isinstance(rng,np.random.Generator):
        raise ValueError("unknown arm or RNG")
    if (cfg.capacity!=K or cfg.mutation_rate!=0 or cfg.survival!=0
            or cfg.seed_arrival.supply!=0):
        raise ValueError("only declared restricted K32 case allowed")
    c=np.asarray(counts)
    if (c.shape!=(len(grid.genotypes),) or c.dtype.kind not in "iu" or
            np.any(c<0) or c.sum()>K):
        raise ValueError("invalid genotype-count parent state")
    if arm==SOURCE:
        return genotype_count_markov_step(c,grid,visitors,cfg,rng,year=year)
    state=genotype_counts_to_canonical_state(c,grid,year,K)
    if not len(state.ids):
        return np.zeros(len(c),dtype=np.int64)
    ledger=reproduce(state,visitors,cfg)
    pairs=reweighted_outcross(ledger,arm)
    np.fill_diagonal(pairs,0.)
    pairs[np.diag_indices(len(state.ids))]+=ledger.self_viable
    original_total=float(ledger.outcross.sum()+ledger.self_viable.sum())
    changed_total=float(pairs.sum())
    if not np.isclose(original_total,changed_total,atol=1e-10,rtol=0):
        raise ArithmeticError("source-conditional viable offspring census law changed")
    n=min(int(rng.poisson(original_total)),K)
    if n==0 or original_total==0:
        return np.zeros(len(c),dtype=np.int64)
    q=offspring_genotype_distribution(state,pairs/changed_total,grid)
    labels=rng.choice(len(q),size=n,replace=True,p=q/float(q.sum()))
    result=np.bincount(labels,minlength=len(q)).astype(np.int64)
    if (result.sum()!=n or np.any(result<0)):
        raise ArithmeticError("conditional Mendelian offspring lost mass")
    return result


def _snapshot(counts,basis,het):
    n=int(counts.sum())
    if not n:
        return {
            "occupied":0,"census":0,"assurance":None,
            "heterozygote_fraction":None,"genotype_richness":0,
            "allele_types_lost":6,"assurance_fixed":None,
            "trait_mean":None,
        }
    high=np.asarray(counts,dtype=float)@basis/n
    present=0
    for locus in range(3):
        # Allele dosage strictly between 0 and 1 only when both alleles exist.
        p=float(high[locus])
        present+=int(p>0)+int(p<1)
    return {
        "occupied":1,"census":n,"assurance":float(high[2]),
        "heterozygote_fraction":float(counts@het/n),
        "genotype_richness":int(np.count_nonzero(counts)),
        "allele_types_lost":6-present,
        "assurance_fixed":int(np.isclose(high[2],1.,atol=1e-12,rtol=0)),
        "trait_mean":(.25+.5*high).tolist(),
    }


def _mean_se(v):
    a=np.asarray(v,float)
    if len(a)==0:return (None,None)
    return (float(a.mean()),
            float(a.std(ddof=1)/np.sqrt(len(a))) if len(a)>1 else None)


def summarize(rows):
    alive=[r for r in rows if r["occupied"]]
    keys={
        "occupied_fraction":np.asarray([r["occupied"] for r in rows],float),
        "mean_census_all":np.asarray([r["census"] for r in rows],float),
        "mean_genotype_richness_all":np.asarray([r["genotype_richness"] for r in rows],float),
        "mean_lost_allele_types_all":np.asarray([r["allele_types_lost"] for r in rows],float),
        "mean_assurance_high_allele_survivors":np.asarray([r["assurance"] for r in alive],float),
        "mean_assurance_heterozygote_fraction_survivors":np.asarray([r["heterozygote_fraction"] for r in alive],float),
        "high_assurance_fixation_fraction_survivors":np.asarray([r["assurance_fixed"] for r in alive],float),
        "mean_richness_survivors":np.asarray([r["genotype_richness"] for r in alive],float),
    }
    d={"n_total":len(rows),"n_survivors":len(alive),"n_extinct":len(rows)-len(alive)}
    for key,vals in keys.items():
        mean,se=_mean_se(vals)
        d[key]=mean
        d[key+"_demographic_mc_se"]=se
    if alive:
        mat=np.asarray([r["trait_mean"] for r in alive])
        d["mean_3_traits_given_occupied"]=mat.mean(axis=0).tolist()
    else:
        d["mean_3_traits_given_occupied"]=None
    return d


def run_ablation(*,budget=8.,draws=512,seed=420261017):
    if (budget not in (3.,8.) or type(draws) is not int or
            not 16<=draws<=2048 or type(seed) is not int or seed<0):
        raise ValueError("only old-history K32 ablation budgets 8/3 admitted")
    first,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    design=load_design(DEFAULT_DESIGN)
    src=source_config(design,"prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(src,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(src.seed_arrival,supply=0.))
    if cfg.assurance_timing!="prior":
        raise AssertionError("source reassurance configuration changed")
    visitors=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    assert len(visitors)==8
    digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()+
        v.effectiveness.tobytes() for v in visitors)).hexdigest()
    basis=allele_frequency_basis(grid)
    hetero=(basis[:,2]==.5).astype(float)
    trajectories={a:np.repeat(first[None,:],draws,axis=0)
                  for a in ARMS}
    by_generation={}
    for year in range(GENERATIONS):
        snapshots={}
        for arm in ARMS:
            pop=trajectories[arm]
            for rep in range(draws):
                # Paired-in-index common annual RNG stream, reset per
                # generation. Genotype-dependent draws may diverge; this
                # is NOT an identical-counterfactual-outcome coupling.
                rng=np.random.default_rng(np.random.SeedSequence(
                    [seed,rep,year]))
                pop[rep]=step_with_intervention(
                    pop[rep],grid,visitors[year],cfg,rng,year,arm)
                if (np.any(pop[rep]<0) or pop[rep].sum()>K or
                        pop[rep].dtype.kind not in "iu"):
                    raise ArithmeticError("counterfactual invalid finite population")
            snapshots[arm]=[_snapshot(pop[i],basis,hetero) for i in range(draws)]
        by_generation[str(year+1)]={a:summarize(snapshots[a]) for a in ARMS}
    final={a:[_snapshot(x,basis,hetero) for x in trajectories[a]]
           for a in ARMS}
    paired={}
    original=final[SOURCE]
    for arm in ARMS[1:]:
        other=final[arm]
        shared=[i for i in range(draws)
                if original[i]["occupied"] and other[i]["occupied"]]
        diff_ass=[other[i]["assurance"]-original[i]["assurance"] for i in shared]
        diff_het=[other[i]["heterozygote_fraction"]-original[i]["heterozygote_fraction"]
                  for i in shared]
        diff_fix=[other[i]["assurance_fixed"]-original[i]["assurance_fixed"] for i in shared]
        extinction=[(1-other[i]["occupied"])-(1-original[i]["occupied"])
                    for i in range(draws)]
        rich=[other[i]["genotype_richness"]-original[i]["genotype_richness"]
              for i in range(draws)]
        lost=[other[i]["allele_types_lost"]-original[i]["allele_types_lost"]
              for i in range(draws)]
        metrics={
            "assurance_high_frequency_conditional_on_both_surviving":diff_ass,
            "assurance_heterozygosity_conditional_on_both_surviving":diff_het,
            "high_assurance_fixation_conditional_on_both_surviving":diff_fix,
            "extinction_probability_difference":extinction,
            "genotype_richness_unconditional_difference":rich,
            "lost_allele_types_unconditional_difference":lost,
        }
        paired[arm]={
            "n_pairwise_survivors":len(shared),
            "difference_direction":"counterfactual_minus_original",
            "means":{k:_mean_se(v)[0] for k,v in metrics.items()},
            "nested_demographic_mc_se":{k:_mean_se(v)[1] for k,v in metrics.items()},
        }
    return {
        "status":"K32_SOURCE_VS_ONE_FACTOR_OUTCROSS_ABLATIONS_COMPLETED",
        "evidence_type":"exploratory_counterfactual_Model3_different_biology_not_field_data",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":8,
            "adult_survival":0,"seed_immigration":0,
            "ovule_budget":budget,
            "original_setting":"canonical_Chapter2_prior_selfing",
            "old_visitor_history":OLD_HISTORY,"visitor_environment":"near",
            "old_visitor_sequence_sha256":digest,
            "independent_visitor_histories":1,
            "demographic_replicates_per_arm":draws,
            "genotype_support_classes":27,
            "source_biological_code_edited":False,
            "counterfactual_intentionally_modifies_reproduction":True,
            "source_conditional_total_viable_seed_intensity_preserved":True,
            "source_conditional_selfed_seed_mass_and_fraction_preserved":True,
            "original_mating_edge_support_preserved":True,
            "common_random_seed_by_path_and_year":True,
            "confirmatory_visitor_cohorts_used":False,
        },
        "arms":list(ARMS),
        "per_generation":by_generation,
        "year8_paired_contrasts":paired,
        "warnings":[
            "Interventions flatten one selected factor among positive biological mating edges while preserving the original ledger's selfed mass and total viable outcross mass at the intervention state's parent composition.",
            "The source and counterfactual may diverge in future genotype frequencies and therefore future endogenous fertility/census, despite equal conditional total seed intensity when evaluated at the SAME state.",
            "These are autonomous eight-year altered-reproduction models, deliberately different from unchanged canonical biology.",
            "Because total seed intensity is normalized, no DIRECT current-year demography or selfing proportion intervention is identified; changes in extinction can occur indirectly through shifted genotypes over time.",
            "One-at-a-time contrasts are baseline/order/context dependent and do not isolate unique causal pollinator vs maternal processes. The routing factor combines visitor channel and recipient affinity.",
            "Only one archived visitor history and artificial founders; the 512 demographic streams are nested and are not 512 independent ecosystems.",
            "Rare extinction estimates may be imprecise; conditioning of allele traits on occupancy differs between arms.",
            "No natural-island data, preregistered future confirmatory visitor cohorts, full SDE/SPDE or geographical INLA.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=512)
    args=p.parse_args()
    result=run_ablation(budget=args.budget,draws=args.draws)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":result["status"],"budget":args.budget,
        "final":result["per_generation"]["8"],
        "differences":result["year8_paired_contrasts"],
    }))


if __name__=="__main__":
    main()
