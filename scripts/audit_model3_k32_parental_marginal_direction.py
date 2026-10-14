"""Exact maternal/paternal allele-frequency directions in Model3 K32.

Within one ORIGINAL finite Model3 parental population, unchanged canonical
reproduce() gives an ordered father(row) x mother(column) viable mating
matrix W = outcross + diag(self_viable). The exact Mendelian offspring
high-allele expectation at all three biallelic diploid loci is

 q_l = (W.sum(axis=1) @ b_l + W.sum(axis=0) @ b_l)/(2 W.sum())

where b_l is each parent's high-allele dosage {0,.5,1}. Thus q-p is
the sum of expected contributions from viable SELF seed production,
female receipt of OUTCROSS seeds, and male donation to OUTCROSS seeds.

At precisely the SAME source parental state C, apply the seven
predeclared altered outcross-mating-weight matrices from the previous
2x2x2 Model3 factorial. Reproduction INTENSITY, source viable selfing
and existing mating edge support are held fixed at this state. This
identifies parent-MARGINAL one-step EXPECTED allele direction contrasts,
not eight-year autonomous counterfactual differences.

CRITICAL: pairwise mating association at FIXED father/mother marginals
does not change any locus's immediate Mendelian mean q; it CAN change
the joint offspring genotype law and later genotype-driven evolution.
The paternal/maternal/self terms are an EXACT Price-style accounting
of this specified biological model, not independently causal
pollinator-selection coefficients or natural fitness estimates.

Only old archived near visitor seed 26110601, 8 years, K32 u=0,
512 nested demographic source paths and no confirmatory histories.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_stochastic_bridge import (
    genotype_counts_to_canonical_state,genotype_count_markov_step,
    offspring_genotype_distribution,
)
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config,load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import (
    K,GENERATIONS,MUTATION_RATE,OLD_HISTORY,
    canonical_conditional_kernel,
)
from scripts.run_model3_k32_outcross_factorial import (
    combine_outcross_factors,MASK_LABELS,
)

LOCI=("pollinator_matching","floral_investment","reproductive_assurance")


def exact_parent_marginal_contributions(state,ledger,outcross,grid, *,
                                        check_child_genotype_law=False):
    """Three-locus exact Mendelian allele shift for specific mating weights.

    Conditional on source parent C: self, outcross father, and outcross
    mother are separate source-vs-control algebraic terms, weighted
    by the ORIGINAL mass of viable self and outcross offspring.
    """
    n=len(state.ids)
    mat=np.asarray(outcross,float)
    canonical=np.asarray(ledger.outcross,float)
    selfmass=np.asarray(ledger.self_viable,float)
    if (n<1 or mat.shape!=(n,n) or np.any(~np.isfinite(mat))
            or np.any(mat<0) or not np.all(np.diag(mat)==0)
            or np.any((canonical==0)&(mat>1e-12))
            or not np.isclose(mat.sum(),canonical.sum(),atol=1e-10,rtol=0)):
        raise ValueError("same-state outcross edge support and mass must remain fixed")
    total=float(mat.sum()+selfmass.sum())
    if total<=0:
        return {"status":"ZERO_REPRODUCTION"}
    b=np.asarray(state.alleles,float).mean(axis=2)
    # frozen individual diploid genotype values .25 and .75
    dosage=(b-.25)/.5
    if dosage.shape!=(n,3) or not np.all(np.isin(dosage,[0.,.5,1.])):
        raise ValueError("unexpected source diploid high-allele dosage")
    p=dosage.mean(axis=0)
    outfrac=float(mat.sum()/total)
    selffrac=float(selfmass.sum()/total)
    mat_father=np.asarray(mat.sum(axis=1),float)
    mat_mother=np.asarray(mat.sum(axis=0),float)
    self_shift=(selfmass@dosage)/total-selffrac*p
    father_shift=.5*((mat_father@dosage)/total-outfrac*p)
    mother_shift=.5*((mat_mother@dosage)/total-outfrac*p)
    expected_direction=self_shift+father_shift+mother_shift
    exact_next=p+expected_direction
    paternal_all=(mat_father+selfmass)@dosage/total
    maternal_all=(mat_mother+selfmass)@dosage/total
    np.testing.assert_allclose(exact_next,.5*(paternal_all+maternal_all),
                               atol=1e-12,rtol=0)
    if check_child_genotype_law:
        W=mat.copy()
        W[np.diag_indices(n)]+=selfmass
        q=offspring_genotype_distribution(state,W/total,grid)
        b_genotype=allele_frequency_basis(grid)
        np.testing.assert_allclose(q@b_genotype,exact_next,atol=1e-12,rtol=0)
    return {
        "status":"MATCHED_MARGINALS",
        "parent_allele_frequency":p.tolist(),
        "expected_next_allele_frequency":exact_next.tolist(),
        "expected_allele_direction":expected_direction.tolist(),
        "viable_self_seed_allele_direction":self_shift.tolist(),
        "outcross_paternal_allele_direction":father_shift.tolist(),
        "outcross_maternal_allele_direction":mother_shift.tolist(),
        "expected_paternal_allele_frequency":paternal_all.tolist(),
        "expected_maternal_allele_frequency":maternal_all.tolist(),
        "source_selfed_intensity_fraction":selffrac,
        "source_outcross_intensity_fraction":outfrac,
        "total_viable_expected_seed_intensity":total,
        "max_identity_error":float(np.max(np.abs(
            exact_next-p-expected_direction))),
    }


def same_parent_factorial_marginals(counts,grid,visitors,cfg,year):
    state=genotype_counts_to_canonical_state(counts,grid,year,K)
    if len(state.ids)==0:
        return {"status":"EXTINCT_PARENT"}
    ledger=reproduce(state,visitors,cfg)
    if not (ledger.outcross.sum()+ledger.self_viable.sum())>0:
        return {"status":"ZERO_REPRODUCTION"}
    results={}
    for mask in range(8):
        alt=combine_outcross_factors(ledger,mask)
        r=exact_parent_marginal_contributions(
            state,ledger,alt,grid,check_child_genotype_law=(mask in (0,1,2,4,7)))
        if r["status"]!="MATCHED_MARGINALS":
            return {"status":"UNMATCHED_FACTORIAL_STATE","mask":mask}
        results[mask]=r
    ref=results[0]
    p=np.asarray(ref["parent_allele_frequency"])
    # Assert original from independent canonical conditional genotype kernel.
    _,q=canonical_conditional_kernel(counts,grid,visitors,cfg,year)
    b=allele_frequency_basis(grid)
    np.testing.assert_allclose(q@b,ref["expected_next_allele_frequency"],
                               atol=1e-11,rtol=0)
    contrasts={}
    for mask in range(1,8):
        intervention=results[mask]
        diff=np.asarray(intervention["expected_allele_direction"])-ref["expected_allele_direction"]
        dp=np.asarray(intervention["outcross_paternal_allele_direction"])-ref["outcross_paternal_allele_direction"]
        dm=np.asarray(intervention["outcross_maternal_allele_direction"])-ref["outcross_maternal_allele_direction"]
        ds=np.asarray(intervention["viable_self_seed_allele_direction"])-ref["viable_self_seed_allele_direction"]
        np.testing.assert_allclose(diff,dp+dm+ds,atol=1e-12,rtol=0)
        np.testing.assert_allclose(ds,0.,atol=1e-12,rtol=0)
        contrasts[mask]={
            "source_parent_allele_direction_difference":diff.tolist(),
            "outcross_father_marginal_contrast":dp.tolist(),
            "outcross_mother_marginal_contrast":dm.tolist(),
            "self_component_contrast":ds.tolist(),
            "max_identity_error":float(np.max(np.abs(diff-dp-dm-ds))),
        }
    return {
        "status":"EXACT_PARENTAL_MARGINALS",
        "parent_frequencies":p.tolist(),
        "source":ref,
        "same_parent_intervention_contrasts":contrasts,
    }


def summarize(a):
    arr=np.asarray(a,float)
    if arr.ndim!=2 or arr.shape[1]!=3:
        raise ValueError("expected three diploid locus traits")
    return {
        "n_source_parent_states":int(len(arr)),
        "mean":arr.mean(axis=0).tolist() if len(arr) else None,
        "nested_demographic_mc_se":(
            arr.std(axis=0,ddof=1)/np.sqrt(len(arr))).tolist()
            if len(arr)>1 else None,
    }


def run_parental_marginals(*,budget=8.,draws=512,seed=420261017):
    if (budget not in (3.,8.) or type(draws) is not int or
            not 16<=draws<=2048 or type(seed) is not int or seed<0):
        raise ValueError("old-history K32 parental marginal diagnostic only")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    design=load_design(DEFAULT_DESIGN)
    source=source_config(design,"prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(source,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(source.seed_arrival,supply=0.))
    if cfg.assurance_timing!="prior":
        raise AssertionError("canonical source prior selfing changed")
    old=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    assert len(old)==8
    visitor_digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()+
        v.effectiveness.tobytes() for v in old)).hexdigest()
    parents=np.repeat(initial[None,:],draws,axis=0)
    years={}
    unexpected=[]
    for year in range(GENERATIONS):
        source_records=[]
        reference_contrasts={mask:[] for mask in range(1,8)}
        father_contrasts={mask:[] for mask in range(1,8)}
        mother_contrasts={mask:[] for mask in range(1,8)}
        statuses={}
        for rep in range(draws):
            c=parents[rep]
            if not int(c.sum()):
                statuses["EXTINCT_PARENT"]=statuses.get("EXTINCT_PARENT",0)+1
                continue
            result=same_parent_factorial_marginals(c,grid,old[year],cfg,year)
            if result["status"]=="EXACT_PARENTAL_MARGINALS":
                source_records.append(result["source"])
                for mask in range(1,8):
                    d=result["same_parent_intervention_contrasts"][mask]
                    reference_contrasts[mask].append(d["source_parent_allele_direction_difference"])
                    father_contrasts[mask].append(d["outcross_father_marginal_contrast"])
                    mother_contrasts[mask].append(d["outcross_mother_marginal_contrast"])
            else:
                statuses[result["status"]]=statuses.get(result["status"],0)+1
            parents[rep]=genotype_count_markov_step(
                c,grid,old[year],cfg,
                np.random.default_rng(np.random.SeedSequence([seed,rep,year])),
                year=year)
        source_stats={
            "parent_allele_frequency":summarize([x["parent_allele_frequency"] for x in source_records]),
            "next_allele_frequency":summarize([x["expected_next_allele_frequency"] for x in source_records]),
            "expected_allele_direction":summarize([x["expected_allele_direction"] for x in source_records]),
            "self_seed_contribution":summarize([x["viable_self_seed_allele_direction"] for x in source_records]),
            "outcross_father_contribution":summarize([x["outcross_paternal_allele_direction"] for x in source_records]),
            "outcross_mother_contribution":summarize([x["outcross_maternal_allele_direction"] for x in source_records]),
        }
        contrasts={}
        for mask in range(1,8):
            a=summarize(reference_contrasts[mask])
            f=summarize(father_contrasts[mask])
            m=summarize(mother_contrasts[mask])
            if a["mean"] is not None:
                np.testing.assert_allclose(
                    a["mean"],np.asarray(f["mean"])+m["mean"],
                    atol=1e-12,rtol=0)
            contrasts[str(mask)]={
                "mask_name":MASK_LABELS[mask],
                "counterfactual_minus_source_expected_allele_direction":a,
                "outcross_father_marginal_contribution":f,
                "outcross_mother_marginal_contribution":m,
                "self_contribution_zero_exactly":True,
            }
        years[str(year+1)]={
            "n_surviving_original_parent_states":len(source_records),
            "noncomparable_parent_statuses":statuses,
            "source_marginals":source_stats,
            "factorial_contrasts_on_identical_parent_state":contrasts,
        }
        if any(k!="EXTINCT_PARENT" for k in statuses):
            unexpected.append({"generation":year+1,"statuses":statuses})
    return {
        "status":"K32_EXACT_SAME_PARENT_MATERNAL_PATERNAL_PRICE_IDENTITY"
                 if not unexpected else "K32_MARGINAL_CONDITIONS_INCOMPLETE",
        "evidence_type":"source_conditional_exact_parental_allele_marginal_accounting_simulation",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":GENERATIONS,
            "adult_survival":0,"seed_immigration":0,
            "ovule_budget":budget,"old_visitor_history":OLD_HISTORY,
            "environment":"near","visitor_history_sha256":visitor_digest,
            "independent_visitor_histories":1,
            "nested_demographic_replicates":draws,
            "source_genotype_support_classes":27,
            "locus_order":list(LOCI),
            "canonical_original_Model3_biology_modified":False,
            "counterfactual_outcross_mating_weights_intentionally_modified":True,
            "original_viable_self_seeds_and_total_outcross_intensity_preserved_in_comparisons":True,
            "same_original_parental_genotype_state_across_all_masks":True,
            "no_autonomous_alternative_population_forecast":True,
            "prospective_confirmatory_histories_used":False,
        },
        "formula":"q_l-p_l = s*(b_self_l-p_l) + 0.5*(weighted_father_outcross_l - outcross_fraction*p_l) + 0.5*(weighted_mother_outcross_l - outcross_fraction*p_l); same-parent self term cancels from every altered-outcross contrast",
        "biological_caution":[
            "Father and mother are algebraic marginals of source viable offspring pair probabilities; neither is uniquely causal sexual selection or pollinator preference.",
            "The mating-pair joint covariance is not needed to determine expected single-locus Mendelian direction if parental marginals are held fixed; it can influence multilocus offspring genotypes and later trajectories.",
            "All intervention masks are deliberately different reproductive mating operators, not frozen biological source Model3 or natural experiments.",
            "Only one archived visitor history with 512 nested demographic paths, not independent ecology or plant observations.",
            "No confirmatory visitor history, independent islands, causal adaptive fitness or full SDE/SPDE validation."
        ],
        "years":years,
        "unmatched":unexpected,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",required=True,type=Path)
    parser.add_argument("--budget",choices=[3.,8.],type=float,default=8.)
    parser.add_argument("--draws",type=int,default=512)
    a=parser.parse_args()
    result=run_parental_marginals(budget=a.budget,draws=a.draws)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    final=result["years"]["8"]
    print(json.dumps({
        "status":result["status"],"budget":a.budget,
        "n_eligible":final["n_surviving_original_parent_states"],
        "source":final["source_marginals"]["expected_allele_direction"]["mean"],
        "all_three_minus_source":final["factorial_contrasts_on_identical_parent_state"]["7"],
    }))


if __name__=="__main__":
    main()
