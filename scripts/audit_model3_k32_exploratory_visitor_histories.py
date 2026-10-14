"""Exploratory ecological-history replication of Model3 matching-direction reversal.

DO NOT interpret these *newly generated after outcome exposure* histories
as preregistered confirmation, independent natural islands or validation of
any complete SDE/SPDE. Eight fixed discovery-follow-up visitor RNG seeds
(26110602..26110609) are a transparent post hoc stress-test, never the
prospectively frozen Chapter2 seeds 37110801..37110864.
The OLD discovery history 26110601 is separately included as a reference
and excluded from the eight-history exploratory aggregate.

Same canonical K=32, mutation0, prior_selfing and original source
genotype-count Markov reproduction; 128 demographic replicates NESTED under
each visitor history, 8 years, budgets3/8. Among paths alive at START
of year8, evaluate original source q(C_t,V_t)-p(C_t) with the SAME PATH
IDENTITIES for all eight parent years, separating viable selfed-seed,
outcross father, and outcross mother mean directions. No off-diagonal
temporal transplant, no edited parental states, no new biology.
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
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN,config as source_config,load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_model3_three_arm_k32_old_history import (
    K,GENERATIONS,MUTATION_RATE,OLD_HISTORY,
)

# Declared BEFORE viewing any of these exploratory history outcomes.
EXPLORATORY_SEEDS=tuple(range(26110602,26110610))
REFERENCE_SEED=OLD_HISTORY
CONFIRMATORY_SEEDS=frozenset(range(37110801,37110865))
DIRECTION_FIELDS=(
    "expected_allele_direction",
    "viable_self_seed_allele_direction",
    "outcross_paternal_allele_direction",
    "outcross_maternal_allele_direction",
)


def _three_locus_stats(x):
    arr=np.asarray(x,float)
    if arr.ndim!=2 or arr.shape[1]!=3:
        raise ValueError("source expectations require 3 locus vectors")
    return {
        "n_source_demographic_paths":len(arr),
        "mean":arr.mean(axis=0).tolist() if len(arr) else None,
        "nested_demographic_mc_se":(
            (arr.std(axis=0,ddof=1)/np.sqrt(len(arr))).tolist()
        ) if len(arr)>1 else None,
    }


def one_history(*,history_seed,budget=8.,draws=128,seed=420261017):
    if (history_seed not in (REFERENCE_SEED,*EXPLORATORY_SEEDS)
            or history_seed in CONFIRMATORY_SEEDS
            or budget not in (3.,8.)
            or type(draws) is not int or not 16<=draws<=1024
            or type(seed) is not int or seed<0):
        raise ValueError("only declared old reference and 8 new exploratory RNG visitor histories")
    initial,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    cfg0=source_config(load_design(DEFAULT_DESIGN),
                       "prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(cfg0,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(cfg0.seed_arrival,supply=0.))
    if (cfg.assurance_timing!="prior" or cfg.assurance_cost!=0
            or cfg.investment_cost!=.5):
        raise AssertionError("source original prior-selfing formula changed")
    visits=exposure(history_seed,"near").visitors[:GENERATIONS]
    if len(visits)!=8:
        raise AssertionError("eight year source visitor sequence unavailable")
    fingerprint=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+
        v.breadths.tobytes()+v.effectiveness.tobytes()
        for v in visits)).hexdigest()
    parent_states=[]
    parents=np.repeat(initial[None,:],draws,axis=0)
    for t in range(8):
        parent_states.append(parents.copy())
        if t<7:
            for rep in range(draws):
                parents[rep]=genotype_count_markov_step(
                    parents[rep],grid,visits[t],cfg,
                    np.random.default_rng(np.random.SeedSequence([
                        seed,history_seed,rep,t])),
                    year=t)
    original_occupied=[int(np.count_nonzero(c.sum(axis=1)>0))
                       for c in parent_states]
    common=np.flatnonzero(parent_states[-1].sum(axis=1)>0)
    if np.any([np.any(parent_states[t][common].sum(axis=1)==0)
               for t in range(8)]):
        raise AssertionError("source had extinct resurrection in no-immigration case")
    directions=np.zeros((8,len(common),4,3),float)
    parent_high=np.zeros((8,len(common),3),float)
    for t in range(8):
        for j,rep in enumerate(common):
            c=parent_states[t][rep]
            state=genotype_counts_to_canonical_state(c,grid,t,K)
            ledger=reproduce(state,visits[t],cfg)
            r=exact_parent_marginal_contributions(
                state,ledger,ledger.outcross,grid,
                check_child_genotype_law=False)
            if r["status"]!="MATCHED_MARGINALS":
                raise AssertionError("live parent lacks original source reproductive intensity")
            directions[t,j]=[r[k] for k in DIRECTION_FIELDS]
            parent_high[t,j]=r["parent_allele_frequency"]
    np.testing.assert_allclose(
        directions[:,:,0,:],
        directions[:,:,1,:]+directions[:,:,2,:]+directions[:,:,3,:],
        atol=1e-12,rtol=0)
    years={}
    for t in range(8):
        years[str(t+1)]={
            "parent_original_state_occupied_total":original_occupied[t],
            "common_late_survivor_parent_paths":len(common),
            "parent_high_allele_frequency":_three_locus_stats(parent_high[t]),
            "original_reproductive_direction":{
                key:_three_locus_stats(directions[t,:,k,:])
                for k,key in enumerate(DIRECTION_FIELDS)
            },
        }
    early=directions[0,:,0,0]
    late=directions[7,:,0,0]
    if len(common):
        early_mean=float(early.mean())
        late_mean=float(late.mean())
        changes=late-early
    else:
        early_mean=None
        late_mean=None
        changes=np.empty(0,float)
    return {
        "history_seed":history_seed,
        "kind":("old_discovery_reference" if history_seed==REFERENCE_SEED
                else "new_after_discovery_exploratory"),
        "source_visitor_sha256":fingerprint,
        "independent_visitor_seed":history_seed,
        "same_surviving_source_paths_for_all_parent_years":True,
        "n_demographic_paths":draws,
        "n_occupied_at_start_of_year8":len(common),
        "parent_occupation_count_by_year":original_occupied,
        "original_matching_expected_direction_early":early_mean,
        "original_matching_expected_direction_late":late_mean,
        "matching_direction_neg_to_pos":
            (early_mean < 0 and late_mean > 0)
            if early_mean is not None else None,
        "matching_early_late_change_on_same_survivor_paths":{
            "n":len(changes),
            "mean":float(changes.mean()) if len(changes) else None,
            "nested_demographic_mc_se":float(
                changes.std(ddof=1)/np.sqrt(len(changes)))
                if len(changes)>1 else None
        },
        "original_source_parent_years":years,
        "historical_sequence_not_exchanged_with_other_seeds":True,
    }


def run_stress_test(*,budget=8.,draws=128,seed=420261017):
    if budget not in (3.,8.) or type(draws) is not int or not 16<=draws<=1024:
        raise ValueError("source K32 old-budget exploratory stress screen only")
    histories=[one_history(history_seed=h,budget=budget,draws=draws,seed=seed)
               for h in (REFERENCE_SEED,*EXPLORATORY_SEEDS)]
    fingerprint=[r["source_visitor_sha256"] for r in histories]
    if len(set(fingerprint))!=len(fingerprint):
        raise AssertionError("simulated independent visitor histories unexpectedly identical")
    new=histories[1:]
    evaluable=[r for r in new
               if r["original_matching_expected_direction_late"] is not None]
    sign=[r for r in evaluable if r["matching_direction_neg_to_pos"]]
    late_pos=[r for r in evaluable if
              r["original_matching_expected_direction_late"]>0]
    if len(evaluable):
        delta=np.asarray([r["matching_early_late_change_on_same_survivor_paths"]["mean"]
                          for r in evaluable],float)
        end=np.asarray([r["original_matching_expected_direction_late"]
                        for r in evaluable],float)
    else:
        delta=np.empty(0,float)
        end=np.empty(0,float)
    return {
        "status":"MODEL3_K32_EXPLORATORY_NEW_VISITOR_SEED_STRESS_COMPLETE",
        "provenance":{
            "K":K,"mutation_rate":0,"generations":8,
            "adult_survival":0,"seed_immigration":0,
            "budget":budget,
            "original_source_prior_selfing":True,
            "original_assurance_cost":0.,
            "original_investment_cost":.5,
            "archived_discovery_history_seed":REFERENCE_SEED,
            "new_post_outcome_exploratory_history_seeds":list(EXPLORATORY_SEEDS),
            "n_distinct_new_simulated_visitor_histories":len(EXPLORATORY_SEEDS),
            "n_nested_demographic_paths_per_history":draws,
            "environment":"near",
            "history_simulator":"unchanged source exposure(seed,near)",
            "exploratory_histories_newly_generated_not_archived":True,
            "source_biological_code_edited":False,
            "source_state_common_late_survivor_cohort":True,
            "new_history_independent_random_seeds_not_natural_islands":True,
            "prospectively_frozen_chapter2_confirmatory_seeds_used":False,
            "visitor_histories_selected_before_calculating_new_outcomes":True,
            "new_histories_preregistered_before_prior_source_discovery":False,
        },
        "histories":histories,
        "new_histories_summary":{
            "n_predeclared":len(new),
            "n_with_late_source_parent_survivors":len(evaluable),
            "n_negative_to_positive_matching_direction":len(sign),
            "n_positive_late_matching_direction":len(late_pos),
            "positive_late_direction_fraction_of_evaluable":
                len(late_pos)/len(evaluable) if evaluable else None,
            "negative_to_positive_fraction_of_evaluable":
                len(sign)/len(evaluable) if evaluable else None,
            "mean_early_late_matching_direction_change_across_visitor_histories":
                float(delta.mean()) if len(delta) else None,
            "range_early_late_matching_direction_change":
                [float(delta.min()),float(delta.max())] if len(delta) else None,
            "mean_late_matching_direction_across_visitor_histories":
                float(end.mean()) if len(end) else None,
            "range_late_matching_direction":
                [float(end.min()),float(end.max())] if len(end) else None,
        },
        "limits":[
            "Histories 26110602..26110609 were newly generated and selected AFTER seeing the old discovery's sign reversal; this is NOT prospective confirmation, irrespective of running with predetermined codes.",
            "Eight simulated distinct visitor random seeds sample the simulator's generating law; they do not represent independent natural island ecological systems.",
            "128 demographic paths per seed are nested inside each visitor history. Variation among paths is not independent environmental replication; only eight newly generated visitor seeds inform the across-ecology exploratory fraction.",
            "The same survivors at start of parent year8 are used for all within-history parent years, so this analysis conditions on later survival and is not an unconditional average over all founder descendants.",
            "A source matching-direction sign switch is a conditional one-step expected reproductive-allele shift, not recovery from fixed allele loss, a field fitness selection coefficient or validation of full SDE/SPDE.",
            "Frozen prospectively registered Chapter2 visitor seeds 37110801..37110864 are never accessed; original source reproduction and genotype Markov code is untouched."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=128)
    a=p.parse_args()
    r=run_stress_test(budget=a.budget,draws=a.draws)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps({
        "status":r["status"],"budget":a.budget,
        "new_histories_summary":r["new_histories_summary"],
        "per_history_matching_endpoints":[{
            "seed":x["history_seed"],
            "n_alive_start_year8":x["n_occupied_at_start_of_year8"],
            "early":x["original_matching_expected_direction_early"],
            "late":x["original_matching_expected_direction_late"],
            "switch":x["matching_direction_neg_to_pos"]
        } for x in r["histories"]]
    }))


if __name__=="__main__":
    main()
