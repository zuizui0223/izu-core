"""Old-history mutation-enabled three-generation conditional-moment preflight.

Each update is the original canonical Model 3 ABM, using unchanged visitor
history 26110601 and no immigration. At EACH realized genotype state, a
separate independent demographic ensemble checks the exact *one-step*
mutation-aware mean/covariance prediction. This is NOT a multigeneration
SDE/SPDE and not a new independent ecological-history campaign.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.audit_model3_stochastic_mutation_scaling import (
    exact_mutation_one_step_trait_moments,
    population_size_noise_scaling,
)
from scripts.model3_island.population import advance, subset
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as config_for_setting, founders, load_design,
)
from scripts.run_model3_persistent_isolation import exposure


OLD_VISITOR_HISTORY = 26110601


def run_mutation_multistep_preflight(
    *, n_draws: int = 512, updates: int = 3,
    mutation_rate: float = .01, mutation_sd: float = .05,
) -> dict:
    if (type(n_draws) is not int or n_draws < 256 or n_draws > 4096
            or type(updates) is not int or updates < 1 or updates > 3
            or mutation_rate not in (0.01, 0.5)
            or mutation_sd not in (0.05, 0.2)):
        raise ValueError("restricted preflight scope requires declared settings")
    design=load_design(DEFAULT_DESIGN)
    state=subset(founders(design),np.arange(8,dtype=int))
    genotype_start_hash=hashlib.sha256(state.alleles.tobytes()).hexdigest()
    base=config_for_setting(design,"prior_selfing",mutation_rate,"evolving")
    c=replace(
        base,capacity=8,survival=0.,ovule_budget=8.,
        mutation_sd=mutation_sd,
        seed_arrival=replace(base.seed_arrival,supply=0.),
    )
    history=exposure(OLD_VISITOR_HISTORY,"near")
    canonical_streams={
        name:stream(98765421,name,0) for name in STREAM_IDS
    }
    rows=[]
    for t in range(updates):
        if not len(state.ids):
            raise RuntimeError("stopped: canonical trajectory became extinct")
        ledger=reproduce(state,history.visitors[t],c)
        target=exact_mutation_one_step_trait_moments(state,ledger,c)
        empty=subset(state,np.empty(0,dtype=int))
        observed=[]
        extinct=0
        for draw in range(n_draws):
            master=987810000+t*10000+draw
            sim_rng={name:stream(master,name,0) for name in STREAM_IDS}
            offspring,_=advance(
                state,ledger,empty,c,sim_rng,year=t,
                mutation_traits=(True,True,True),
            )
            if len(offspring):
                observed.append(offspring.alleles.mean(axis=(0,2)))
            else:
                extinct+=1
        if len(observed)<128:
            raise AssertionError("fewer than 128 occupied offspring samples")
        arr=np.asarray(observed)
        mean_error=float(np.max(np.abs(
            arr.mean(axis=0)-np.asarray(target["offspring_mean"])
        )))
        cov_error=float(np.max(np.abs(
            np.cov(arr.T)-
            np.asarray(target["occupied_population_trait_mean_covariance"])
        )))
        extinction_error=abs(extinct/n_draws-target["probability_extinct"])
        if mean_error >= .04 or cov_error >= .020 or extinction_error >= .08:
            raise AssertionError(
                f"state-conditioned mutation moment gate failed in update {t}: "
                f"mean={mean_error},cov={cov_error},extinction={extinction_error}"
            )
        state_hash=hashlib.sha256(state.alleles.tobytes()).hexdigest()
        next_state,_=advance(
            state,ledger,empty,c,canonical_streams,year=t,
            mutation_traits=(True,True,True)
        )
        rows.append({
            "update":t,
            "genotype_sha256":state_hash,
            "n_current_individuals":len(state.ids),
            "n_next_original_ABM":len(next_state.ids),
            "conditional_P_extinct":target["probability_extinct"],
            "observed_P_extinct":extinct/n_draws,
            "offspring_mean":target["offspring_mean"],
            "mean_max_error":mean_error,
            "covariance_max_error":cov_error,
            "extinction_absolute_error":extinction_error,
            "mutation_rate":mutation_rate,
            "mutation_sd":mutation_sd,
            "occupied_comparison_count":len(observed),
        })
        state=next_state
    # These are controlled genotype-frequency sampling calculations,
    # not a carrying-capacity intervention on the nonlinear Model 3 payoff.
    scaling=population_size_noise_scaling(
        np.asarray([.02,.18,.30,.50]),
        sizes=(8,16,32,64,128)
    )
    return {
        "status":"OLD_HISTORY_MUTATION_THREE_UPDATE_CONDITIONAL_GATES_PASS",
        "source_visitor_history":OLD_VISITOR_HISTORY,
        "independent_visitor_histories":1,
        "new_visitor_histories_drawn":0,
        "n_nested_demographic_draws_per_step":n_draws,
        "n_conditional_steps":updates,
        "founder_genotype_sha256":genotype_start_hash,
        "results":rows,
        "conditional_population_size_scaling":scaling,
        "canonical_Model3_modified":False,
        "full_multigeneration_SDE_validated":False,
        "full_trait_space_SPDE_validated":False,
        "geographic_INLA_performed":False,
    }


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--draws",type=int,default=512)
    parser.add_argument("--updates",type=int,default=3)
    parser.add_argument("--mutation-rate",type=float,default=.01)
    parser.add_argument("--mutation-sd",type=float,default=.05)
    args=parser.parse_args()
    receipt=run_mutation_multistep_preflight(
        n_draws=args.draws,updates=args.updates,
        mutation_rate=args.mutation_rate,mutation_sd=args.mutation_sd
    )
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(receipt,sort_keys=True,
        indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":receipt["status"],
        "updates":receipt["n_conditional_steps"],
        "max_mean_error":max(x["mean_max_error"] for x in receipt["results"]),
        "max_covariance_error":max(x["covariance_max_error"] for x in receipt["results"]),
        "max_extinction_error":max(
            x["extinction_absolute_error"] for x in receipt["results"]
        ),
    }))


if __name__=="__main__":
    main()
