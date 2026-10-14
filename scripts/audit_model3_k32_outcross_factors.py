"""Shapley audit of donor export, visitor routing and maternal seed allocation.

Exactly reconstruct canonical Model3 outcross pair weights using its frozen
reproduce() ledger:
 W_ij = [exported_i] [delivered_ij/exported_i] [female_j/receipt_j], i!=j.
The three bracketed factors are multiplied only when supported; division by
zero means an absent path, never a new positive parent combination.

All 2^3 nested parent-pair laws are evaluated using the exact full 3-locus
Mendelian offspring tensor. Shapley averaging removes arbitrary ordering
of the three factors, but does NOT identify their unique causal effects.
An explicit fourth "neutral-dosage tilt" reference term is needed because
the preceding mean-matched null tilted *offspring genotypes*, not parents.

Old visitor 26110601/near only, K32 mutation0, 8 generations. This is
one-step conditional mathematics, NOT autonomous population forecasting,
natural observation, or selection/pollination counterfactual experiment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_model3_k32_self_outcross_mechanism import (
    exact_ledger_decomposition, conditional_pair_child_law,
)
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import (
    genotype_count_markov_step, genotype_counts_to_canonical_state,
)
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import (
    K, GENERATIONS, MUTATION_RATE, OLD_HISTORY,
)

FACTORS=("donor_export","visitor_routing_and_recipient_affinity",
         "maternal_seed_provisioning")
REFERENCE_KEY="matched_mean_null_offspring_tilt_to_uniform_pair_baseline"


def _shapley(het_by_mask):
    """Three-factor permutation-invariant Shapley sum for a scalar observable."""
    if set(het_by_mask)!=set(range(8)):
        raise ValueError("all eight parent-pair factor combinations required")
    weights={0:1/3,1:1/6,2:1/3}
    phi=[]
    for bit in (1,2,4):
        value=0.
        for mask in range(8):
            if mask & bit:
                continue
            size=mask.bit_count()
            value+=weights[size]*(het_by_mask[mask|bit]-het_by_mask[mask])
        phi.append(float(value))
    if not np.isclose(sum(phi),het_by_mask[7]-het_by_mask[0],
                      atol=1e-12,rtol=0):
        raise ArithmeticError("Shapley attribution does not telescope")
    return dict(zip(FACTORS,phi))


def decompose_outcross_factors(counts,grid,visitors,cfg,year):
    """Per-actual-parent-state exact canonical factorization, no source edits."""
    c=np.asarray(counts)
    if (c.ndim!=1 or c.shape!=(len(grid.genotypes),)
            or c.dtype.kind not in "iu" or np.any(c<0)
            or c.sum()>K):
        raise ValueError("invalid finite source parent counts")
    if c.sum()==0:
        return {"status":"EXTINCT_PARENT"}
    original=exact_ledger_decomposition(c,grid,visitors,cfg,year)
    if original["status"]!="EXACT_LEDGER_STRATIFIED":
        return {"status":"SOURCE_LEDGER_UNMATCHED","reason":original["status"]}
    state=genotype_counts_to_canonical_state(c,grid,year,K)
    ledger=reproduce(state,visitors,cfg)
    outcross=np.asarray(ledger.outcross,float)
    out_mass=float(outcross.sum())
    inv=original["conditional_inverse_positive_recruits"]
    s=original["source_selfing_fraction_of_viable_seed_intensity"]
    ref=original["exact_three_term_next_frequency_variance"][
        "within_outcross_mating_weighting_contrast"]
    if not out_mass>0:
        # Source outcross contribution has coefficient (1-s)=0.
        if not np.isclose(s,1.,atol=1e-12):
            raise ArithmeticError("source zero outcross mass inconsistent")
        if not np.isclose(ref,0.,atol=1e-12):
            raise ArithmeticError("nonzero reference outcross term without source outcross")
        return {
            "status":"ZERO_SOURCE_OUTCROSS",
            "source_self_fraction":float(s),
            "source_outcross_fraction":0.,
            "within_outcross_reference_variance":0.,
            "terms_variance":{REFERENCE_KEY:0.,**{x:0. for x in FACTORS}},
            "max_exact_reconstruction_error":0.,
        }
    n=len(state.ids)
    if n<2:
        raise ArithmeticError("positive source outcross requires 2+ individuals")
    off=np.ones((n,n),float)-np.eye(n)
    e=np.asarray(ledger.exported,float)
    delivered=np.asarray(ledger.delivered,float)
    receipt=delivered.sum(axis=0)
    female=np.asarray(ledger.maternal-ledger.self_viable,float)
    if np.any(female<-1e-12):
        raise ArithmeticError("negative female outcross component")
    female=np.maximum(female,0.)
    # Values correspond exactly to original transfer multiplication. "Routing"
    # includes pollinator channel affinity, visitor efficiency and recipient
    # affinity, not visitor behaviour independently manipulated.
    route=np.divide(delivered,e[:,None],
                    out=np.zeros_like(delivered),where=e[:,None]>0)
    mother=np.divide(female,receipt,out=np.zeros_like(receipt),
                     where=receipt>0)
    factors=(np.broadcast_to(e[:,None],(n,n)),
             route,
             np.broadcast_to(mother[None,:],(n,n)))
    reconstructed=off.copy()
    for x in factors:
        reconstructed*=x
    pair_abs_err=float(np.max(np.abs(reconstructed-outcross)))
    if pair_abs_err>1e-10:
        raise ArithmeticError("source ledger factorization does not reconstruct source outcross")
    b=allele_frequency_basis(grid)[:,2]
    het_by_mask={}
    for mask in range(8):
        w=off.copy()
        for i,factor in enumerate(factors):
            if mask&(1<<i):
                w*=factor
        q=conditional_pair_child_law(state,w,grid)
        if q is None:
            raise ArithmeticError("positive source outcross lost in masked parent-pair law")
        het_by_mask[mask]=float(np.sum(q[b==.5]))
    hsrc=float(original["source_outcross_heterozygote_probability"])
    hnull=float(original["null_outcross_heterozygote_probability"])
    if not np.isclose(het_by_mask[7],hsrc,atol=1e-12):
        raise ArithmeticError("factorized source offspring heterozygosity mismatch")
    phi=_shapley(het_by_mask)
    scale=-0.25*inv*(1.-s)
    variance_components={
        REFERENCE_KEY:float(scale*(het_by_mask[0]-hnull)),
        **{key:float(scale*phi[key]) for key in FACTORS},
    }
    out_delta=float(sum(variance_components.values()))
    if not np.isclose(out_delta,ref,atol=1e-11,rtol=0):
        raise ArithmeticError("four-way outcross variance does not agree with parent ledger")
    return {
        "status":"EXACT_OUTCROSS_FACTORIZATION",
        "n_source_parents":n,
        "source_self_fraction":float(s),
        "source_outcross_fraction":float(1.-s),
        "source_outcross_heterozygote":hsrc,
        "matched_null_outcross_heterozygote":hnull,
        "source_within_outcross_variance":float(ref),
        "unweighted_uniform_pair_heterozygote":het_by_mask[0],
        "four_term_heterozygosity_reference_adjustment":
            float(het_by_mask[0]-hnull),
        "shapley_heterozygosity":phi,
        "terms_variance":variance_components,
        "max_exact_reconstruction_error":float(max(
            pair_abs_err,abs(out_delta-ref),
            abs(het_by_mask[7]-hsrc))),
        "ordering":"three Shapley factor contributions average all six introduction orders; null-to-uniform offspring-tilt term is separate",
    }


def _summarize(records):
    keys=(REFERENCE_KEY,)+FACTORS
    if not records:
        return {"n_evaluable_source_parent_states":0}
    vals=np.array([[r["terms_variance"][k] for k in keys] for r in records])
    total=vals.sum(axis=1)
    return {
        "n_evaluable_source_parent_states":len(records),
        "mean_original_viable_selfing_fraction":float(np.mean([x["source_self_fraction"] for x in records])),
        "mean_source_within_outcross_delta_variance":float(total.mean()),
        "shapley_and_reference_components_mean":dict(zip(keys,vals.mean(axis=0).tolist())),
        "components_demographic_path_mc_se":dict(zip(
            keys,(vals.std(axis=0,ddof=1)/np.sqrt(len(vals))).tolist()
        )) if len(vals)>1 else None,
        "mean_total_demographic_path_mc_se":float(
            total.std(ddof=1)/np.sqrt(len(vals))) if len(vals)>1 else None,
        "max_absolute_state_identity_error":float(
            max(x["max_exact_reconstruction_error"] for x in records)),
        "fraction_positive_source_within_outcross_component":float(np.mean(total>1e-12)),
    }


def run_outcross_factors(*,budget=8.,draws=512,seed=420261016):
    if (budget not in (3.,8.) or type(draws) is not int or
            not 16<=draws<=2048 or type(seed) is not int or seed<0):
        raise ValueError("fixed source K32 historical environment only")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    design=load_design(DEFAULT_DESIGN)
    src=source_config(design,"prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(src,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(src.seed_arrival,supply=0.))
    old=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    if len(old)!=8 or cfg.assurance_timing!="prior":
        raise AssertionError("source history/mating setup drifted")
    digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()+
        v.effectiveness.tobytes() for v in old)).hexdigest()
    parents=np.repeat(initial[None,:],draws,axis=0)
    years=[]
    unmatched=[]
    for year in range(GENERATIONS):
        rows=[]
        statuses={}
        for i in range(draws):
            c=parents[i]
            if not c.sum():
                statuses["EXTINCT_PARENT"]=statuses.get("EXTINCT_PARENT",0)+1
                continue
            result=decompose_outcross_factors(c,grid,old[year],cfg,year)
            if result["status"] in ("EXACT_OUTCROSS_FACTORIZATION","ZERO_SOURCE_OUTCROSS"):
                rows.append(result)
            else:
                statuses[result["status"]]=statuses.get(result["status"],0)+1
            parents[i]=genotype_count_markov_step(
                c,grid,old[year],cfg,
                np.random.default_rng(np.random.SeedSequence([seed,i,year])),
                year=year)
        summary=_summarize(rows)
        summary.update({
            "generation":year+1,
            "statuses_not_evaluable":statuses,
            "n_occupied_next":int(np.count_nonzero(parents.sum(axis=1))),
            "n_zero_source_outcross":sum(
                r["status"]=="ZERO_SOURCE_OUTCROSS" for r in rows),
        })
        years.append(summary)
        if any(k!="EXTINCT_PARENT" for k in statuses):
            unmatched.append({"generation":year+1,"statuses":statuses})
    return {
        "status":("EXACT_MODEL3_OUTCROSS_SHAPLEY_LEDGER_VERIFIED" if not unmatched
                  else "SOURCE_OUTCROSS_FACTORIZATION_NOT_COMPLETE"),
        "evidence_type":"single_old_visitor_source_conditional_genetic_ledger_simulation",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":8,
            "adult_survival":0,"seed_immigration":0,
            "reproductive_setting":"prior_selfing",
            "ovule_budget":budget,
            "old_visitor_history":OLD_HISTORY,"environment":"near",
            "old_visitor_digest":digest,
            "independent_visitor_histories":1,
            "nested_demographic_replicates":draws,
            "source_biological_reproduction_changed":False,
            "artificial_reference_parent_weights_changed":True,
            "same_source_parent_and_source_conditional_mean_N":True,
            "no_autonomous_comparator_trajectory":True,
            "prospective_confirmatory_histories_used":False,
            "donor_export_factor_from_canonical_ledger":True,
            "visitor_routing_factor_from_canonical_delivery":True,
            "maternal_seed_factor_from_canonical_seed_receipt":True,
            "shapley_computed_across_three_factors":True,
        },
        "components":[REFERENCE_KEY,*FACTORS],
        "per_generation":years,
        "unmatched_source_states":unmatched,
        "interpretation_limits":[
            "Only a declared baseline-relative algebraic factorization of the original one-step within-outcross conditional genetic variance contrast.",
            "Donor exported includes donor trait pollen output AND donor visitor affinity; routing includes donor-channel and recipient matching; maternal factor includes ovule production and receipt-dependent saturation. Components are NOT uniquely causal pollinator/export/mother effects.",
            "Shapley averages introduction orders but still depends on chosen factors, baseline and the reference dosage tilt.",
            "Reference neutral tilt is offspring-level and must be separated as an explicit fourth term, not mislabeled as a source biological process.",
            "These are exact genotype probabilities and 512 nested demographic source simulations under ONE old visitor history, not independent ecology.",
            "The contrast does not identify adaptive stabilization of the eight-year endpoint nor a validated SDE/SPDE."
        ],
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    parser.add_argument("--draws",type=int,default=512)
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    result=run_outcross_factors(budget=args.budget,draws=args.draws)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    last=result["per_generation"][-1]
    print(json.dumps({"status":result["status"],"budget":args.budget,
                      "year8":last,"unmatched":result["unmatched_source_states"]}))


if __name__=="__main__":
    main()
