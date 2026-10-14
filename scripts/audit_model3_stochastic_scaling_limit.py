"""Large-population / small-time scaling audit for frozen Model 3.

Does synchronized reproduction admit an Ito SDE on dt=1/K if population
capacity K is made large without weakening canonical ecological selection?

This is a *necessary-condition screen*, not an asymptotic convergence proof.
Cloning the same historical founder genotype pool changes capacity and the
finite-pollen denominator in the canonical model; these alterations are
reported explicitly. The original mating/mutation/visitor operators are
never edited. Only old source visitor history 26110601 is used.
"""
from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.audit_model3_stochastic_bridge import (
    capped_poisson_distribution,
    expected_offspring_moments,
)
from scripts.model3_island.population import subset
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import PlantState, VisitorState
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as canonical_config, founders, load_design,
)
from scripts.run_model3_persistent_isolation import exposure

VISITOR_HISTORY = 26110601
VISITOR_SNAPSHOT_INDEX = 400  # postassembly, before any plant evolution here
CAPACITIES = (8, 16, 32, 64, 128)


def clone_existing_founder_pool(founders8: PlantState, capacity: int) -> PlantState:
    """Clone exact diploid alleles K/8 times, no mutation or invented alleles."""
    if (type(capacity) is not int or capacity<8
            or capacity%8!=0 or len(founders8.ids)!=8):
        raise ValueError("capacity must be a multiple of the eight founders")
    repeats=capacity//8
    alleles=np.tile(founders8.alleles,(repeats,1,1))
    origin=np.tile(founders8.allele_origin,(repeats,1,1))
    flags=np.tile(founders8.mutation_flags,(repeats,1,1))
    return PlantState(
        alleles,origin,flags,np.arange(capacity,dtype=np.int64),
        np.zeros(capacity,dtype=np.int64)
    )


def scaling_screen(*,settings=("prior_selfing","assurance_cost"),
                   environments=("near","far"),
                   sizes=CAPACITIES,
                   snapshot_index=VISITOR_SNAPSHOT_INDEX) -> dict:
    """Quantify conditional one-step drift and 1/N-like finite noise.

    The conditioned trait mean is defined only when offspring N>0.  If the
    breeding-step drift remains O(1) while variance decays O(1/K),
    speeding time to dt=1/K does not yield a standard *finite drift* Ito SDE
    with unchanged reproductive payoffs: K*drift would grow. A deterministic
    discrete map, or a different weak-selection scaling, is required instead.

    This routine does not infer a population-genetic diffusion limit from a
    finite set of K values. It returns measured arrays and labels any
    scaling claim as a bounded diagnosis only.
    """
    sizes=tuple(sizes)
    if (len(sizes)<3 or len(set(sizes))!=len(sizes)
            or any(type(k) is not int or k<8 or k%8 for k in sizes)):
        raise ValueError("need distinct capacities divisible by eight")
    if not settings or not environments:
        raise ValueError("need declared mating and visitor conditions")
    if type(snapshot_index) is not int or snapshot_index not in (0,200,400):
        raise ValueError("snapshot must be a declared source-history checkpoint")
    d=load_design(DEFAULT_DESIGN)
    base8=subset(founders(d),np.arange(8,dtype=np.int64))
    base_hash=hashlib.sha256(base8.alleles.tobytes()).hexdigest()
    # Exogenous visitor communities are sampled at one prospectively fixed
    # postassembly index. At t=0, near/far share their founder visitor pool
    # and are NOT distinct ecological exposures.
    visitor_snapshot={
        env:exposure(VISITOR_HISTORY,env).visitors[snapshot_index]
        for env in environments
    }
    if "near" in visitor_snapshot and "far" in visitor_snapshot:
        near,far=visitor_snapshot["near"],visitor_snapshot["far"]
        if (np.array_equal(near.ids,far.ids)
                and np.array_equal(near.optima,far.optima)
                and np.array_equal(near.breadths,far.breadths)
                and np.array_equal(near.effectiveness,far.effectiveness)):
            if snapshot_index==0:
                raise ValueError(
                    "initial visitor communities are shared; compare near only at t0"
                )
            raise AssertionError(
                "near/far visitor snapshots still identical after assembly"
            )
    rows=[]
    for mating in settings:
        if mating not in d["settings"]:
            raise ValueError("unknown source frozen mating setting")
        source=canonical_config(d,mating,0., "evolving")
        for env in environments:
            if env not in ("near","far"):
                raise ValueError("unfrozen visitor arm")
            visitors=visitor_snapshot[env]
            for K in sizes:
                plants=clone_existing_founder_pool(base8,K)
                cfg=replace(
                    source,capacity=K,survival=0.,
                    mutation_rate=0.,ovule_budget=8.,
                    seed_arrival=replace(source.seed_arrival,supply=0.)
                )
                ledger=reproduce(plants,visitors,cfg)
                weights=ledger.outcross.copy()
                weights[np.diag_indices(K)]+=ledger.self_viable
                intensity=float(weights.sum())
                if not np.isfinite(intensity) or intensity<=0:
                    raise ValueError("invalid positive reproductive return")
                offspring_mean,offspring_cov=expected_offspring_moments(
                    plants,weights/intensity
                )
                recruitment=capped_poisson_distribution(intensity,K)
                occupancy=1-float(recruitment[0])
                reciprocal=float(np.dot(
                    recruitment[1:],1/np.arange(1,K+1))/occupancy)
                mean_current=plants.alleles.mean(axis=(0,2))
                drift=offspring_mean-mean_current
                conditional_cov=offspring_cov*reciprocal
                if (not np.isfinite(drift).all() or
                        not np.isfinite(conditional_cov).all()):
                    raise ArithmeticError("nonfinite stochastic scaling target")
                rows.append({
                    "setting":mating,
                    "environment":env,
                    "visitor_snapshot_index":snapshot_index,
                    "n_visitor_functional_types":len(visitors.ids),
                    "visitor_community_sha256":hashlib.sha256(
                        visitors.ids.tobytes()+visitors.optima.tobytes()
                        +visitors.breadths.tobytes()
                        +visitors.effectiveness.tobytes()
                    ).hexdigest(),
                    "K":K,
                    "dt_fast":1/K,
                    "offspring_occupancy_probability":float(occupancy),
                    "expected_recruitment":float(recruitment @ np.arange(K+1)),
                    "current_trait_mean":mean_current.tolist(),
                    "offspring_trait_mean":offspring_mean.tolist(),
                    "one_generation_drift":drift.tolist(),
                    "one_generation_drift_l2":float(np.linalg.norm(drift)),
                    "fast_time_rescaled_drift_l2":float(K*np.linalg.norm(drift)),
                    "offspring_covariance_diagonal":np.diag(offspring_cov).tolist(),
                    "sample_mean_noise_variance_diagonal":np.diag(conditional_cov).tolist(),
                    "K_times_sample_mean_noise_variance_diagonal":
                        (K*np.diag(conditional_cov)).tolist(),
                    "mean_n_inverse_conditional_occupied":reciprocal,
                })
    grouped={}
    for mating in settings:
        for env in environments:
            selected=[r for r in rows if r["setting"]==mating
                      and r["environment"]==env]
            selected.sort(key=lambda x:x["K"])
            drift_last=selected[-1]["one_generation_drift_l2"]
            drift_initial=selected[0]["one_generation_drift_l2"]
            rescaled=selected[-1]["fast_time_rescaled_drift_l2"]
            # A finite-K screen, NOT a proof of divergence as K goes to inf.
            flag=bool(drift_last>.005 and rescaled>4*drift_initial)
            grouped[mating+"_"+env]={
                "K_values":[r["K"] for r in selected],
                "terminal_drift_l2":drift_last,
                "terminal_K_drift_l2":rescaled,
                "fast_time_finite_drift_screen_fails":flag,
                "result_scope":"finite_K_necessary_condition_not_limit_theorem",
            }
    return {
        "status":"FINITE_K_STOCHASTIC_SCALING_DIAGNOSTIC",
        "source_old_visitor_history":VISITOR_HISTORY,
        "visitor_snapshot_index":snapshot_index,
        "visitor_assembly_is_fixed_not_outcome_selected":True,
        "plants_remain_unchanged_founder_clones_at_snapshot":True,
        "founder_alleles_sha256":base_hash,
        "n_independent_visitor_histories":1,
        "n_new_visitor_histories":0,
        "model3_biology_modified":False,
        "input_biology":"canonical_model3_synchronized_annual_reproduction",
        "source_mutation_rate":0.,
        "source_ovule_budget":8.,
        "capacity_multiplication_changes_finite_pollen_competition":True,
        "fast_time_dt_hypothesis":"1/K",
        "rows":rows,
        "groups":grouped,
        "all_continuous_time_SDE_limits_proved":False,
        "trait_space_SPDE_validated":False,
        "geographic_INLA_used":False,
    }


def no_visitor_fast_time_counterexample(sizes=CAPACITIES) -> dict:
    """Exact biological counterexample to a universal dt=1/K drift limit.

    In a visitor-free source state with prior selfing, all reproductive
    opportunities are selfing. Replicating an existing genotype K/8 times
    multiplies every parental reproduction weight by K/8, so their normalized
    offspring weights, trait-selection drift, and nonzero mean change are
    *identical at every population size*. The unrelated stochastic sample
    noise decays as population size grows.

    This is an exact algebraic property of this frozen source regime,
    conditional on identical founder genotype proportions and no visitors.
    It does NOT claim to rule out all SDEs, alternative weak-selection
    scalings, or spatial stochastic descriptions.
    """
    sizes=tuple(sizes)
    if len(sizes)<2 or len(set(sizes))!=len(sizes):
        raise ValueError("need at least two distinct population sizes")
    d=load_design(DEFAULT_DESIGN)
    eight=subset(founders(d),np.arange(8,dtype=np.int64))
    visitors=VisitorState(
        np.empty(0,dtype=np.int64),
        np.empty(0,dtype=float),
        np.empty(0,dtype=float),
        np.empty(0,dtype=float),
    )
    source=canonical_config(d,"prior_selfing",0.,"evolving")
    rows=[]
    for K in sizes:
        state=clone_existing_founder_pool(eight,K)
        cfg=replace(
            source,capacity=K,survival=0.,
            mutation_rate=0.,ovule_budget=8.,
            seed_arrival=replace(source.seed_arrival,supply=0.)
        )
        ledger=reproduce(state,visitors,cfg)
        pairs=ledger.outcross.copy()
        pairs[np.diag_indices(K)]+=ledger.self_viable
        if not np.allclose(ledger.outcross,0,atol=0,rtol=0):
            raise AssertionError("zero visitors cannot generate outcrosses")
        prob=pairs/pairs.sum()
        offspring_mean,offspring_cov=expected_offspring_moments(state,prob)
        drift=offspring_mean-state.alleles.mean(axis=(0,2))
        rows.append({
            "K":K,
            "one_generation_drift":drift.tolist(),
            "drift_l2":float(np.linalg.norm(drift)),
            "K_times_drift_l2":float(K*np.linalg.norm(drift)),
            "child_covariance_trace":float(np.trace(offspring_cov)),
        })
    baseline=np.asarray(rows[0]["one_generation_drift"])
    for r in rows[1:]:
        np.testing.assert_allclose(
            np.asarray(r["one_generation_drift"]),baseline,
            rtol=0,atol=1e-12
        )
    if np.linalg.norm(baseline)<=1e-6:
        raise AssertionError("constructed no-visitor state lacks nonzero selection")
    return {
        "status":"EXACT_NO_VISITOR_ORDER_ONE_DRIFT_COUNTEREXAMPLE",
        "n_visitor_types":0,
        "source_mating_setting":"prior_selfing",
        "mutation_rate":0,
        "original_model3_reproductive_operator_unchanged":True,
        "distinct_joint_genotypes_replicated_without_new_alleles":True,
        "one_generation_drift_nonzero_and_capacity_invariant":True,
        "fast_time_dt_hypothesis":"1/K",
        "continuous_time_finite_drift_SDE_limit_for_this_family_admissible":False,
        "not_a_theorem_against_other_weak_selection_or_spde_models":True,
        "rows":rows,
    }


def main()->None:
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--snapshot-index",type=int,default=VISITOR_SNAPSHOT_INDEX)
    parser.add_argument("--near-only",action="store_true")
    parser.add_argument("--zero-visitors-counterexample",action="store_true")
    args=parser.parse_args()
    data=(no_visitor_fast_time_counterexample()
          if args.zero_visitors_counterexample else scaling_screen(
              snapshot_index=args.snapshot_index,
              environments=("near",) if args.near_only else ("near","far")
          ))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(
        data,indent=2,sort_keys=True,allow_nan=False
    )+"\n",encoding="utf-8")
    if args.zero_visitors_counterexample:
        print(json.dumps({
            "status":data["status"],
            "K":[r["K"] for r in data["rows"]],
            "drift_l2":[r["drift_l2"] for r in data["rows"]],
            "K_times_drift_l2":[r["K_times_drift_l2"] for r in data["rows"]],
            "fast_time_dt_1_over_K_finite_drift_admissible":
                data["continuous_time_finite_drift_SDE_limit_for_this_family_admissible"],
        }))
        return
    print(json.dumps({
        "status":data["status"],
        "snapshot_index":data["visitor_snapshot_index"],
        "finite_K_groups":{
            key:{
                "K":x["K_values"],
                "drift": [
                    round(r["one_generation_drift_l2"],9)
                    for r in data["rows"]
                    if r["setting"]+"_"+r["environment"]==key
                ],
                "K_times_drift":[
                    round(r["fast_time_rescaled_drift_l2"],9)
                    for r in data["rows"]
                    if r["setting"]+"_"+r["environment"]==key
                ],
                "terminal_drift":x["terminal_drift_l2"],
                "terminal_K_drift":x["terminal_K_drift_l2"],
                "fast_time_screen_fails":x["fast_time_finite_drift_screen_fails"],
            }
            for key,x in data["groups"].items()
        }
    }))

if __name__=="__main__":
    main()
