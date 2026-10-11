"""Source original Model3 2x2 genotype-state x visitor-year cross across 8 histories.

This AFTER-DISCOVERY explanatory mechanistic comparison uses ONLY
the existing eight exploratory visitor seeds 26110602..26110609.
It is NOT an early forecast, preregistered confirmation or
independent natural-island test. The same original genotype-count
Markov kernel generates source parents; off-diagonal evaluations
are one-generation reproductions of FROZEN parent states.

For each history and budget, take source parental genotype populations
at years1 and8 (start-of-reproduction), use the same demographic path
IDs alive at year8 for all four cells, and cross each with original
visitor years1 and8 of that SAME history (no cross-history visitors).
Each cell's expected high-allele offspring direction and self,
outcross father, outcross mother terms use unchanged reproduce().
Decompose the early-to-late direction change into order-averaged
state, visitor contributions and the 2x2 interaction, pathwise.

Only eight new independent simulator RNG visitor histories; each has
128 nested demographic paths. NO new visitor seeds, and NO frozen
prospective confirmatory visitor histories 37110801..37110864.
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
    genotype_count_markov_step,genotype_counts_to_canonical_state,
)
from scripts.audit_model3_k32_parental_marginal_direction import (
    LOCI,exact_parent_marginal_contributions,
)
from scripts.audit_model3_k32_exploratory_visitor_histories import (
    EXPLORATORY_SEEDS, REFERENCE_SEED, CONFIRMATORY_SEEDS,
)
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config,load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import K,GENERATIONS,MUTATION_RATE

CELL_NAMES=("early_parent_early_visitor","early_parent_late_visitor",
            "late_parent_early_visitor","late_parent_late_visitor")
CHANNELS=("expected_allele_direction","viable_self_seed_allele_direction",
          "outcross_paternal_allele_direction",
          "outcross_maternal_allele_direction")


def matched_cross_components(cells):
    """Per-source-path 2x2 two-order allocation, exact 3-locus identity.

    cells has shape (n_paths,2_parent_years,2_visitor_years,4_channels,3_loci)
    """
    a=np.asarray(cells,float)
    if (a.ndim!=5 or a.shape[1:]!=(2,2,4,3)
            or not np.isfinite(a).all()):
        raise ValueError("matched original-source 2x2 4-channel 3-locus matrix")
    np.testing.assert_allclose(
        a[:,:,:,0,:],
        a[:,:,:,1,:]+a[:,:,:,2,:]+a[:,:,:,3,:],
        atol=1e-12,rtol=0)
    A=a[:,0,0,:,:]
    B=a[:,0,1,:,:]
    C=a[:,1,0,:,:]
    D=a[:,1,1,:,:]
    state_early=C-A
    state_late=D-B
    visitor_early=B-A
    visitor_late=D-C
    state=.5*(state_early+state_late)
    visitor=.5*(visitor_early+visitor_late)
    interaction=D-C-B+A
    total=D-A
    np.testing.assert_allclose(state+visitor,total,atol=1e-12,rtol=0)
    np.testing.assert_allclose(
        state_late-state_early,interaction,atol=1e-12,rtol=0)
    np.testing.assert_allclose(
        visitor_late-visitor_early,interaction,atol=1e-12,rtol=0)
    return {
        "state_order_symmetrized":state,
        "visitor_order_symmetrized":visitor,
        "state_visitor_difference_in_differences":interaction,
        "source_late_minus_early_diagonal":total,
        "state_when_early_visitor":state_early,
        "state_when_late_visitor":state_late,
        "visitor_when_early_parent":visitor_early,
        "visitor_when_late_parent":visitor_late,
    }


def _stats(values):
    x=np.asarray(values,float)
    if x.ndim!=2 or x.shape[1]!=3:
        raise ValueError("3 source allele locus columns required")
    return {
        "n_nested_demographic_paths":len(x),
        "mean":x.mean(axis=0).tolist() if len(x) else None,
        "nested_demographic_mc_se":(
            (x.std(axis=0,ddof=1)/np.sqrt(len(x))).tolist()
            if len(x)>1 else None
        ),
    }


def one_history_cross(*,history_seed,budget=8.,draws=128,seed=420261017):
    if (history_seed not in EXPLORATORY_SEEDS
            or history_seed==REFERENCE_SEED
            or history_seed in CONFIRMATORY_SEEDS
            or budget not in (3.,8.)
            or type(draws) is not int or not 16<=draws<=1024
            or type(seed) is not int or seed<0):
        raise ValueError("new exploratory original-source visitor RNG histories only")
    first,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    cfg0=source_config(load_design(DEFAULT_DESIGN),
                       "prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(cfg0,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(cfg0.seed_arrival,supply=0.))
    if (cfg.assurance_timing!="prior" or cfg.assurance_cost!=0
            or cfg.investment_cost!=.5):
        raise AssertionError("frozen original reproductive model changed")
    visits=exposure(history_seed,"near").visitors[:GENERATIONS]
    if len(visits)!=8:
        raise AssertionError("eight original source visitor years required")
    digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+
        v.breadths.tobytes()+v.effectiveness.tobytes()
        for v in visits)).hexdigest()
    current=np.repeat(first[None,:],draws,axis=0)
    early=current.copy()
    for year in range(7):
        for rep in range(draws):
            current[rep]=genotype_count_markov_step(
                current[rep],grid,visits[year],cfg,
                np.random.default_rng(np.random.SeedSequence([
                    seed,history_seed,rep,year])),year=year)
    late=current.copy()
    shared=np.flatnonzero(late.sum(axis=1)>0)
    if len(shared)<16:
        return {"status":"INSUFFICIENT_LATE_SURVIVORS",
                "history_seed":history_seed,
                "n_survivor_source_paths":len(shared)}
    data=np.empty((len(shared),2,2,4,3),float)
    source_parent_matching_high_freq=np.empty((len(shared),2))
    for i,rep in enumerate(shared):
        for t,counts in enumerate((early[rep],late[rep])):
            original_parent_state=genotype_counts_to_canonical_state(
                counts,grid,0 if t==0 else 7,K)
            high=np.mean(original_parent_state.alleles[:,0,:]==.75)
            source_parent_matching_high_freq[i,t]=float(high)
            for v,visit in enumerate((visits[0],visits[7])):
                ledger=reproduce(original_parent_state,visit,cfg)
                e=exact_parent_marginal_contributions(
                    original_parent_state,ledger,ledger.outcross,grid,
                    check_child_genotype_law=False)
                if e["status"]!="MATCHED_MARGINALS":
                    raise ArithmeticError("no original source viable recruitment")
                data[i,t,v]=[e[k] for k in CHANNELS]
    contrast=matched_cross_components(data)
    four={
        CELL_NAMES[0]:data[:,0,0],
        CELL_NAMES[1]:data[:,0,1],
        CELL_NAMES[2]:data[:,1,0],
        CELL_NAMES[3]:data[:,1,1],
    }
    table={
        label:{
            channel:_stats(matrix[:,i,:]) for i,channel in enumerate(CHANNELS)
        } for label,matrix in four.items()
    }
    components={
        name:{
            channel:_stats(values[:,i,:])
            for i,channel in enumerate(CHANNELS)
        } for name,values in contrast.items()
    }
    means={
        key:table[key]["expected_allele_direction"]["mean"][0]
        for key in CELL_NAMES
    }
    original_early=means[CELL_NAMES[0]]
    original_late=means[CELL_NAMES[3]]
    state_only=means[CELL_NAMES[2]]
    visitor_only=means[CELL_NAMES[1]]
    # These are numerical SIGN categories in the retrospective
    # population-conditional source-genetic expected allele direction.
    return {
        "status":"ORIGINAL_SOURCE_EXACT_2x2_VISITOR_CROSS",
        "history_seed":history_seed,
        "visitor_history_sha256":digest,
        "n_source_paths":draws,
        "n_common_surviving_source_parent_paths":len(shared),
        "common_cohort_conditioned_on_parent_year8_survival":True,
        "original_matching_high_allele_parent_frequency_early":float(
            source_parent_matching_high_freq[:,0].mean()),
        "original_matching_high_allele_parent_frequency_late":float(
            source_parent_matching_high_freq[:,1].mean()),
        "four_original_reproduction_cells":table,
        "exact_source_mechanism_contrasts":components,
        "matching_signs":{
            "early_original_negative":bool(original_early<0),
            "late_original_positive":bool(original_late>0),
            "original_negative_to_positive":bool(
                original_early<0 and original_late>0),
            "late_parent_with_early_visitor_positive":bool(state_only>0),
            "early_parent_with_late_visitor_positive":bool(visitor_only>0),
            "joint_conditions_required_to_cross_zero_in_this_2x2":
                bool(original_early<0 and original_late>0
                     and not(state_only>0) and not(visitor_only>0)),
        },
    }


def _correlation(x,y):
    z=np.asarray(x,float)
    w=np.asarray(y,float)
    if (len(z)!=len(w) or len(z)<3 or z.std()<1e-12
            or w.std()<1e-12):
        return None
    return float(np.corrcoef(z,w)[0,1])


def run_across_histories(*,budget=8.,draws=128,seed=420261017):
    histories=[one_history_cross(
        history_seed=history_seed,budget=budget,draws=draws,seed=seed)
        for history_seed in EXPLORATORY_SEEDS]
    if any(r["status"]!="ORIGINAL_SOURCE_EXACT_2x2_VISITOR_CROSS" for r in histories):
        raise ValueError("all 8 new visitor histories must have adequate source survivors")
    if len({r["visitor_history_sha256"] for r in histories})!=8:
        raise AssertionError("independent source visitor history signatures not distinct")
    get_mean=lambda row,where,locus:row["exact_source_mechanism_contrasts"][where][
        "expected_allele_direction"]["mean"][locus]
    state=[get_mean(r,"state_order_symmetrized",0) for r in histories]
    visitor=[get_mean(r,"visitor_order_symmetrized",0) for r in histories]
    interaction=[get_mean(r,"state_visitor_difference_in_differences",0)
                 for r in histories]
    matching_late=[r["four_original_reproduction_cells"][
        CELL_NAMES[3]]["expected_allele_direction"]["mean"][0]
        for r in histories]
    flip=[r["matching_signs"]["original_negative_to_positive"]
          for r in histories]
    early_negative=[r["matching_signs"]["early_original_negative"]
                    for r in histories]
    parent_sufficient=[r["matching_signs"]["late_parent_with_early_visitor_positive"]
                       for r in histories]
    visitor_sufficient=[r["matching_signs"]["early_parent_with_late_visitor_positive"]
                        for r in histories]
    joint_necessary=[r["matching_signs"]["joint_conditions_required_to_cross_zero_in_this_2x2"]
                     for r in histories]
    common_late=[r["original_matching_high_allele_parent_frequency_late"] for r in histories]
    return {
        "status":"ORIGINAL_K32_EIGHT_EXPLORATORY_HISTORY_EXACT_STATE_VISITOR_CROSS_VERIFIED",
        "source_provenance":{
            "K":K,"mutation_rate":0,"generations":8,
            "adult_survival":0,"seed_immigration":0,
            "ovule_budget":budget,
            "original_source_prior_selfing":True,
            "original_assurance_cost":0.,
            "original_investment_cost":.5,
            "archived_old_reference_seed_excluded":REFERENCE_SEED,
            "new_simulated_visitor_seeds":list(EXPLORATORY_SEEDS),
            "n_independent_new_simulated_visitor_rng_histories":8,
            "n_nested_demographic_paths_per_history":draws,
            "year1_and_year8_visitor_snapshots_from_same_history":True,
            "only_original_diagonal_parent_state_histories_evolved":True,
            "original_model3_biological_reproductive_code_edited":False,
            "offdiagonal_one_step_visitor_swaps_not_autonomous_evolution":True,
            "source_parent_ids_same_cohort_early_and_late":True,
            "source_cohort_conditioned_on_year8_parent_survival":True,
            "prospectively_frozen_chapter2_confirmation_seeds_used":False,
            "exploratory_histories_selected_after_prior_outcome_exposure":True,
        },
        "three_locus_order":list(LOCI),
        "channels":list(CHANNELS),
        "per_history_source_cross":histories,
        "eight_history_descriptive_summary":{
            "n_new_histories":8,
            "n_early_negative_matching_direction":sum(early_negative),
            "n_late_positive_matching_direction":sum(
                r["matching_signs"]["late_original_positive"] for r in histories),
            "n_negative_to_positive_matching_direction":sum(flip),
            "n_late_parent_positive_with_early_visitor":sum(parent_sufficient),
            "n_early_parent_positive_with_late_visitor":sum(visitor_sufficient),
            "n_joint_conditions_necessary_among_negative_to_positive":sum(joint_necessary),
            "n_original_flip_with_late_parent_early_visitor_already_positive":
                sum(f and p for f,p in zip(flip,parent_sufficient)),
            "n_original_flip_with_early_parent_late_visitor_already_positive":
                sum(f and v for f,v in zip(flip,visitor_sufficient)),
            "mean_state_contribution_matching":float(np.mean(state)),
            "mean_visitor_contribution_matching":float(np.mean(visitor)),
            "range_state_contribution_matching":[float(min(state)),float(max(state))],
            "range_visitor_contribution_matching":[float(min(visitor)),float(max(visitor))],
            "mean_state_visitor_interaction_matching":float(np.mean(interaction)),
            "n_negative_state_contributions":sum(s<0 for s in state),
            "n_negative_visitor_contributions":sum(v<0 for v in visitor),
            "history_level_correlations_descriptive_only":{
                "late_parent_matching_frequency_vs_state_contribution":
                    _correlation(common_late,state),
                "visitor_contribution_vs_late_expected_direction":
                    _correlation(visitor,matching_late),
                "state_contribution_vs_late_expected_direction":
                    _correlation(state,matching_late),
            },
        },
        "interpretive_boundaries":[
            "Eight new visitor RNG histories are sampled from one synthetic generating mechanism post original discovery; not preregistered independent ecological field systems.",
            "All 2x2 contrasts are one-step original reproduction on the SAME selected original late-year survivor cohort; conditional selection is not a trait-level causal selection coefficient.",
            "State factor includes all three locus genetic backgrounds and census changes; visitor factor captures year1 versus year8 snapshots of the same one visitor RNG trajectory. They can interact.",
            "Sign sufficiency here means only a source-model expected one-generation allele direction at an artificially crossed cell exceeds zero, not that independent transplanted visitor conditions would produce the final population.",
            "Mean two-order state and visitor terms are algebraic contrasts; signed shares are unstable when net changes are small, so no 82% universal mechanism transfer is asserted.",
            "Offspring conditional expected direction does not recover historical allele loss; no ecological confirmation seeds 37110801..37110864, natural island data, or validated full SDE/SPDE."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=128)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=run_across_histories(budget=a.budget,draws=a.draws)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":result["status"],"budget":a.budget,
        "summary":result["eight_history_descriptive_summary"],
        "brief_per_history":[{
            "seed":r["history_seed"],
            "alive":r["n_common_surviving_source_parent_paths"],
            "matching":{
                name:r["four_original_reproduction_cells"][name][
                    "expected_allele_direction"]["mean"][0]
                for name in CELL_NAMES},
            "state_contribution":r["exact_source_mechanism_contrasts"][
                "state_order_symmetrized"]["expected_allele_direction"]["mean"][0],
            "visitor_contribution":r["exact_source_mechanism_contrasts"][
                "visitor_order_symmetrized"]["expected_allele_direction"]["mean"][0],
        } for r in result["per_history_source_cross"]]
    }))


if __name__=="__main__":
    main()
