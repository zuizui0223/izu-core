"""Reproducible OLD visitor-history engineering benchmark for the SDE precursor.

No biological data from independent confirmation or Chapter 2 prospective
expression-order cohorts are sampled. Output is engineering-only JSON, not
a natural-island inference, new validation cohort, or full SDE/SPDE proof.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

from scripts.audit_model3_stochastic_bridge import (
    exact_one_step_trait_moments, draw_gaussian_trait_surrogate,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as biological_config,
    founders, load_design,
)
from scripts.run_model3_persistent_isolation import exposure
from scripts.model3_island.population import advance, subset
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.randomness import stream, STREAM_IDS

ROOT = Path(__file__).resolve().parents[1]
OLD_VISITOR_HISTORY = 26110601


def audit_old_history(*, setting: str = "prior_selfing",
                      environment: str = "near",
                      budget: float = 0.25,
                      n_draws: int = 512) -> dict:
    """Compare canonical ABM one-step draws and a Gaussian SDE candidate.

    Only repeated demographic random streams differ; founder and visitor
    conditions are held EXACTLY fixed. The independent ecological n remains
    ONE archived visitor history even when demographic draws are numerous.
    """
    if setting not in ("delayed_control","prior_selfing","pollen_discount",
                       "assurance_cost") or environment not in ("near","far"):
        raise ValueError("unsupported original biological control")
    if not 0 < budget <= 8 or type(n_draws) is not int or not 64<=n_draws<=4096:
        raise ValueError("invalid safe one-step benchmark scope")
    d = load_design(DEFAULT_DESIGN)
    state = subset(founders(d),np.arange(8,dtype=int))
    original_sha = hashlib.sha256(state.alleles.tobytes()).hexdigest()
    source = biological_config(d,setting,0., "evolving")
    cfg = replace(source,capacity=8,survival=0.,
                  mutation_rate=0.,ovule_budget=float(budget),
                  seed_arrival=replace(source.seed_arrival,supply=0.))
    history = exposure(OLD_VISITOR_HISTORY,environment)
    ledger = reproduce(state,history.visitors[0],cfg)
    expected = exact_one_step_trait_moments(state,ledger,cfg)
    empty = subset(state,np.empty(0,dtype=int))
    abm = []
    gaussian = []
    abm_dead = gaussian_dead = 0
    for idx in range(n_draws):
        # This is not a prospective new visitor history: only the nested
        # demographic process is resampled for the same fixed parents.
        key = OLD_VISITOR_HISTORY + idx*11939
        streams = {name: stream(key,name,0) for name in STREAM_IDS}
        child,_ = advance(state,ledger,empty,cfg,streams,year=0,
                          mutation_traits=(True,True,True))
        if len(child.ids):
            abm.append(child.alleles.mean(axis=(0,2)))
        else:
            abm_dead += 1
        n,z = draw_gaussian_trait_surrogate(
            expected,np.random.default_rng(key+10313)
        )
        if n:
            gaussian.append(z)
        else:
            gaussian_dead += 1
    def moments(values):
        if len(values)<2:
            raise AssertionError("too few occupied populations to assess moments")
        arr = np.asarray(values)
        return {
            "occupied":len(arr),
            "mean":arr.mean(axis=0).tolist(),
            "covariance":np.cov(arr.T).tolist(),
            "out_of_trait_bounds_fraction":float(np.any(
                (arr<0)|(arr>1),axis=1).mean()),
        }
    abm_m= moments(abm)
    gaussian_m=moments(gaussian)
    target_mu = np.asarray(expected["offspring_mean"])
    target_cov = np.asarray(expected["occupied_trait_mean_covariance"])
    abm_mean_error = float(np.max(np.abs(np.asarray(abm_m["mean"])-target_mu)))
    gaussian_mean_error = float(np.max(np.abs(np.asarray(gaussian_m["mean"])-target_mu)))
    abm_cov_error = float(np.max(np.abs(np.asarray(abm_m["covariance"])-target_cov)))
    gaussian_cov_error = float(np.max(np.abs(np.asarray(gaussian_m["covariance"])-target_cov)))
    occupancy_error = abs(abm_dead/n_draws - expected["probability_extinct"])
    # Conservative engineering gates, not natural-effect confidence bounds.
    gate = (
        occupancy_error < 0.10 and abm_mean_error < 0.075
        and abm_cov_error < 0.045
        and gaussian_mean_error < 0.075
        and gaussian_cov_error < 0.045
    )
    if not gate:
        raise AssertionError(
            f"old-history one-step Monte Carlo precision gate failed: "
            f"occupancy {occupancy_error:.5g}, ABM mean {abm_mean_error:.5g}, "
            f"ABM cov {abm_cov_error:.5g}, Gaussian mean {gaussian_mean_error:.5g}, "
            f"Gaussian cov {gaussian_cov_error:.5g}"
        )
    if hashlib.sha256(state.alleles.tobytes()).hexdigest()!=original_sha:
        raise AssertionError("benchmark modified canonical diploid founders")
    return {
        "status": "OLD_HISTORY_RESTRICTED_ONE_STEP_ENGINEERING_GATE_PASS",
        "visitor_history":OLD_VISITOR_HISTORY,
        "independent_visitor_history_count":1,
        "settings":{"mating":setting,"environment":environment,
                    "capacity":8,"ovule_budget":float(budget),
                    "mutation_rate":0.,"plant_immigration":0.,
                    "adult_survival":0.},
        "demographic_draws":n_draws,
        "founder_genotype_sha256":original_sha,
        "exact_discrete_ABM_target":expected,
        "canonical_ABM":abm_m,
        "gaussian_SDE_candidate":gaussian_m,
        "abm_extinction_frequency":abm_dead/n_draws,
        "gaussian_extinction_frequency":gaussian_dead/n_draws,
        "max_ABM_occupied_trait_mean_error":abm_mean_error,
        "max_ABM_occupied_trait_covariance_error":abm_cov_error,
        "max_gaussian_occupied_trait_mean_error":gaussian_mean_error,
        "max_gaussian_occupied_trait_covariance_error":gaussian_cov_error,
        "extinction_frequency_error":occupancy_error,
        "full_continuous_time_SDE_validated":False,
        "full_trait_space_SPDE_validated":False,
        "natural_island_data_used":False,
        "new_independent_visitor_histories_sampled":0,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--setting",choices=[
        "delayed_control","prior_selfing","pollen_discount","assurance_cost"
    ],default="prior_selfing")
    p.add_argument("--environment",choices=["near","far"],default="near")
    p.add_argument("--budget",type=float,default=0.25)
    p.add_argument("--draws",type=int,default=512)
    args = p.parse_args()
    receipt = audit_old_history(
        setting=args.setting,environment=args.environment,
        budget=args.budget,n_draws=args.draws
    )
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(receipt,indent=2,sort_keys=True,
                                   allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":receipt["status"],
        "P_extinct":receipt["exact_discrete_ABM_target"]["probability_extinct"],
        "ABM_error_mean":receipt["max_ABM_occupied_trait_mean_error"],
        "ABM_error_cov":receipt["max_ABM_occupied_trait_covariance_error"],
        "SDE_candidate_error_mean":receipt["max_gaussian_occupied_trait_mean_error"],
        "SDE_candidate_error_cov":receipt["max_gaussian_occupied_trait_covariance_error"],
    }))


if __name__=="__main__":
    main()
