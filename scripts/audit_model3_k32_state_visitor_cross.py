"""Original Model3 state × archived-visitor-year 8×8 crossing.

Separate temporal changes in original parental genotype/census states
from changes in the archived visitor condition, without changing ANY
source biological reproduction, gamete transmission, or genetic state
transition rules. For every one of eight source parent-state years t
and eight years of the SAME OLD visitor seed 26110601 v, evaluate
the conditional expected one-generation high-allele direction
D(t,v)=E[p_child|C_t,V_v,N>0]-p(C_t) from the original reproduce ledger.

Only original source trajectories evolve along the archived *diagonal*
visitor sequence; off-diagonal cells are counterfactual swap assays,
NOT autonomous populations or independently sampled environments.

The primary 2×2 early-vs-late attribution uses the SAME demographic
replicate identities alive at parent-state year7. That fixes the cohort
across state years and avoids silently changing survival denominators,
but it CONDITIONs on subsequent occupancy. Both the parent state
(including census/genotype history) and visitor state can interact.
Order-symmetrized state & visitor contrasts are a descriptive
two-factor accounting, not uniquely causal selection or field ecology.
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

STAT_KEYS=(
    "expected_allele_direction",
    "viable_self_seed_allele_direction",
    "outcross_paternal_allele_direction",
    "outcross_maternal_allele_direction",
)


def exact_original_crossed_direction(counts,grid,visitor,cfg,year):
    """Exact source pair ledger mean; no arbitrary altered mating weights."""
    state=genotype_counts_to_canonical_state(counts,grid,year,K)
    if not len(state.ids):
        return {"status":"EXTINCT_PARENT"}
    ledger=reproduce(state,visitor,cfg)
    result=exact_parent_marginal_contributions(
        state,ledger,ledger.outcross,grid,check_child_genotype_law=False)
    if result["status"]!="MATCHED_MARGINALS":
        return result
    result["source_canonical_biology_edited"]=False
    return result


def symmetrized_endpoint_attribution(matrix):
    """Exact diagonal early/late contrast split into state, visitor, cross.

    Matrix (8,8,3) of *same cohort* mean expected per-year allele
    directions. Shapley over the TWO pathways of moving state
    year 0→7 and visitor condition 0→7:
        state = 1/2[(D_70-D_00)+(D_77-D_07)]
        visit = 1/2[(D_07-D_00)+(D_77-D_70)]
    plus explicit early visitor and late visitor state changes,
    early vs late visitor effects, and difference-in-differences.
    """
    arr=np.asarray(matrix,float)
    if arr.shape!=(8,8,3) or not np.isfinite(arr).all():
        raise ValueError("complete 8×8×3 shared-survivor source means required")
    a=arr[0,0]
    b=arr[0,7]
    c=arr[7,0]
    d=arr[7,7]
    state_early_vis=c-a
    state_late_vis=d-b
    visitor_early_state=b-a
    visitor_late_state=d-c
    interaction=d-c-b+a
    state=.5*(state_early_vis+state_late_vis)
    visitor=.5*(visitor_early_state+visitor_late_state)
    total=d-a
    np.testing.assert_allclose(state+visitor,total,atol=1e-12,rtol=0)
    np.testing.assert_allclose(state_late_vis-state_early_vis,
                               interaction,atol=1e-12,rtol=0)
    np.testing.assert_allclose(visitor_late_state-visitor_early_state,
                               interaction,atol=1e-12,rtol=0)
    return {
        "early_original":[float(x) for x in a],
        "late_original":[float(x) for x in d],
        "early_state_late_visitor":[float(x) for x in b],
        "late_state_early_visitor":[float(x) for x in c],
        "actual_diagonal_late_minus_early":total.tolist(),
        "state_effect_at_early_visitor":state_early_vis.tolist(),
        "state_effect_at_late_visitor":state_late_vis.tolist(),
        "visitor_effect_at_early_state":visitor_early_state.tolist(),
        "visitor_effect_at_late_state":visitor_late_state.tolist(),
        "state_visitor_difference_in_differences":interaction.tolist(),
        "symmetrized_state_contribution":state.tolist(),
        "symmetrized_visitor_contribution":visitor.tolist(),
        "numerical_identity_max_abs_error":float(np.max(np.abs(state+visitor-total))),
    }


def _mc(a):
    z=np.asarray(a,float)
    if z.ndim!=2 or z.shape[1]!=3:
        raise ValueError("expected one record per path and source locus")
    return {
        "n":len(z),
        "mean":z.mean(axis=0).tolist() if len(z) else None,
        "nested_demographic_mc_se":(
            z.std(axis=0,ddof=1)/np.sqrt(len(z))).tolist()
            if len(z)>1 else None,
    }


def run_state_visitor_cross(*,budget=8.,draws=512,seed=420261017):
    if (budget not in (3.,8.) or type(draws) is not int or
        not 16<=draws<=2048 or type(seed) is not int or seed<0):
        raise ValueError("only old K32 source crossover design admitted")
    first,grid,_,_=fixed_support_problem(capacity=K,ovule_budget=budget)
    source=source_config(load_design(DEFAULT_DESIGN),
                         "prior_selfing",MUTATION_RATE,"evolving")
    cfg=replace(source,capacity=K,survival=0.,mutation_rate=0.,
                ovule_budget=float(budget),
                seed_arrival=replace(source.seed_arrival,supply=0.))
    if cfg.assurance_timing!="prior":
        raise AssertionError("frozen prior selfing changed")
    visits=exposure(OLD_HISTORY,"near").visitors[:GENERATIONS]
    if len(visits)!=GENERATIONS==8:
        raise AssertionError("one old archived visitor history required")
    digest=hashlib.sha256(b"".join(
        v.ids.tobytes()+v.optima.tobytes()+v.breadths.tobytes()+
        v.effectiveness.tobytes() for v in visits)).hexdigest()

    # Generate ONLY original-canonical 8-year parent states ONCE.
    original=np.repeat(first[None,:],draws,axis=0)
    parent_states=[]
    for t in range(8):
        parent_states.append(original.copy())
        for rep in range(draws):
            original[rep]=genotype_count_markov_step(
                original[rep],grid,visits[t],cfg,
                np.random.default_rng(np.random.SeedSequence([seed,rep,t])),
                year=t)

    living_last=(parent_states[7].sum(axis=1)>0)
    shared=np.flatnonzero(living_last)
    if len(shared)<16:
        return {
            "status":"INSUFFICIENT_SHARED_SURVIVORS",
            "n_alive_parent_year7":int(len(shared)),
            "n_parent_paths":draws,
        }
    # No dropout in the retained parent-state cohort prior to t7.
    for t in range(8):
        if np.any(parent_states[t][shared].sum(axis=1)<=0):
            raise AssertionError("source population resurrected after extinction")

    # 4 components (direction, self, outcross father, outcross mother)
    # for each t, visitor year v, shared replicated original state.
    observations=np.empty((8,8,len(shared),4,3),dtype=float)
    all_parent_year_survivors=[]
    for t in range(8):
        all_parent_year_survivors.append(int(np.count_nonzero(
            parent_states[t].sum(axis=1))))
        for v in range(8):
            for j,rep in enumerate(shared):
                result=exact_original_crossed_direction(
                    parent_states[t][rep],grid,visits[v],cfg,t)
                if result["status"]!="MATCHED_MARGINALS":
                    raise ArithmeticError("crossed source state lacks reproduction")
                observations[t,v,j]=np.array(
                    [result[k] for k in STAT_KEYS],dtype=float)
    np.testing.assert_allclose(
        observations[:,:,:,0,:],
        observations[:,:,:,1,:]+observations[:,:,:,2,:]+
        observations[:,:,:,3,:],
        atol=1e-12,rtol=0)
    # Diagonal uses exact visitor year matching its actual source state year.
    means=observations.mean(axis=2)
    selected=means[:,: ,0,:]
    endpoint=symmetrized_endpoint_attribution(selected)
    per_path_d=observations[:,:,:,0,:]
    a=per_path_d[0,0]
    b=per_path_d[0,7]
    c=per_path_d[7,0]
    d=per_path_d[7,7]
    state_contrib=.5*((c-a)+(d-b))
    visitor_contrib=.5*((b-a)+(d-c))
    interaction=(d-c)-(b-a)
    np.testing.assert_allclose(state_contrib+visitor_contrib,d-a,
                               atol=1e-12,rtol=0)
    np.testing.assert_allclose(
        endpoint["symmetrized_state_contribution"],
        state_contrib.mean(axis=0),atol=1e-12,rtol=0)
    np.testing.assert_allclose(
        endpoint["symmetrized_visitor_contribution"],
        visitor_contrib.mean(axis=0),atol=1e-12,rtol=0)
    np.testing.assert_allclose(
        endpoint["state_visitor_difference_in_differences"],
        interaction.mean(axis=0),atol=1e-12,rtol=0)

    # Balanced two-way descriptive decomposition over the SAME cohort.
    grand=selected.mean(axis=(0,1))
    state_marginal=selected.mean(axis=1)-grand
    visitor_marginal=selected.mean(axis=0)-grand
    state_visitor_interaction=(
        selected-state_marginal[:,None,:]-
        visitor_marginal[None,:,:]-grand)
    np.testing.assert_allclose(
        state_visitor_interaction.mean(axis=0),
        np.zeros((8,3)),atol=1e-12,rtol=0)
    np.testing.assert_allclose(
        state_visitor_interaction.mean(axis=1),
        np.zeros((8,3)),atol=1e-12,rtol=0)
    matrix_summary={}
    for t in range(8):
        matrix_summary[str(t+1)]={
            str(v+1):{
                key:_mc(observations[t,v,:,k,:])
                for k,key in enumerate(STAT_KEYS)
            } for v in range(8)
        }
    return {
        "status":"K32_ORIGINAL_MODEL3_OLD_HISTORY_STATE_VISITOR_CROSS_VERIFIED",
        "evidence_type":"post_outcome_original_source_state_by_visitor_counterfactual_replay",
        "conditions":{
            "K":K,"mutation_rate":0,"generations":8,
            "adult_survival":0,"seed_immigration":0,
            "budget":budget,"source_reproduction":"Chapter2_prior_selfing",
            "old_visitor_history":OLD_HISTORY,"environment":"near",
            "old_history_sha256":digest,
            "n_independent_visitor_histories":1,
            "n_nested_demographic_draws":draws,
            "n_alive_parent_year7":int(len(shared)),
            "source_parent_survival_cohort_common_across_years":True,
            "conditioned_on_occupation_at_start_of_year8":True,
            "source_parent_occupied_counts_by_year":all_parent_year_survivors,
            "visitor_levels_are_eight_years_of_one_archived_history":True,
            "source_biological_reproduction_changed":False,
            "visitor_swap_is_non_autonomous_one_step_counterfactual":True,
            "prospective_confirmatory_history_used":False,
            "natural_island_data_used":False,
            "genotype_support_classes":27,
            "locus_order":list(LOCI),
        },
        "full_8x8_same_cohort":matrix_summary,
        "observed_diagonal_expected_direction_by_original_parent_year":[
            means[t,t,0,:].tolist() for t in range(8)],
        "observed_diagonal_self_direction_by_original_parent_year":[
            means[t,t,1,:].tolist() for t in range(8)],
        "observed_diagonal_father_direction_by_original_parent_year":[
            means[t,t,2,:].tolist() for t in range(8)],
        "observed_diagonal_mother_direction_by_original_parent_year":[
            means[t,t,3,:].tolist() for t in range(8)],
        "early_late_same_cohort_order_symmetrized":endpoint,
        "early_late_same_cohort_demographic_mc_se":{
            "state":_mc(state_contrib),
            "visitor":_mc(visitor_contrib),
            "state_by_visitor_interaction":_mc(interaction),
            "diagonal_late_minus_early":_mc(d-a),
        },
        "balanced_8x8_effects":{
            "grand_mean":grand.tolist(),
            "genotype_state_year_mean_centered":state_marginal.tolist(),
            "visitor_year_mean_centered":visitor_marginal.tolist(),
            "state_visitor_interaction_matrix":state_visitor_interaction.tolist(),
            "max_double_centering_error":float(max(
                np.max(np.abs(state_visitor_interaction.mean(axis=0))),
                np.max(np.abs(state_visitor_interaction.mean(axis=1))))),
        },
        "scope_limits":[
            "Parent years are not experimental treatments: they include accumulated genotype frequency selection, finite drift, population census, prior visitor exposure and genotype-specific survival/occupancy conditioning.",
            "Source-parent sample is restricted to paths occupied at parent state year7 for exact paired cohort comparisons; this is prospective-state-conditioned and not the entire unconditional source ensemble.",
            "Visitor conditions are year-specific realizations of ONE archived visitor history, NOT eight ecologically independent habitats or randomized trials.",
            "Crossing environmental snapshots breaks their original sequence and is a one-step counterfactual only; no independently evolved source populations for off-diagonal cells.",
            "State and visitor contributions use explicit two-order Shapley allocation of a 2x2 difference; their interaction is not uniquely causal pollinator change or adaptive genotype feedback.",
            "All underlying source reproduction, pollen routing, selfing and exact genetics remain unchanged; no natural-island field evidence or validated continuous SDE/SPDE."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--budget",type=float,choices=[3.,8.],default=8.)
    p.add_argument("--draws",type=int,default=512)
    a=p.parse_args()
    r=run_state_visitor_cross(budget=a.budget,draws=a.draws)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":r["status"],"budget":a.budget,
        "original_diagonal_matching":[float(a[0]) for a in
                                       r.get("observed_diagonal_expected_direction_by_original_parent_year",[])],
        "matching_early_late_decomposition":{
            k:v[0] for k,v in
            r.get("early_late_same_cohort_order_symmetrized",{}).items()
            if isinstance(v,list) and len(v)==3},
        "shared_survivors":r.get("conditions",{}).get("n_alive_parent_year7"),
    }))


if __name__=="__main__":
    main()
