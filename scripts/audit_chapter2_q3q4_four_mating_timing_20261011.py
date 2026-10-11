"""Exact 80-update Q3→Q4 timing across four historical Model3 mating systems.

Reuses the original father×mother reproduction operator, Mendelian inheritance,
Poisson-capped recruitment, exposed K8/B48/genotype/visitor fixture and budgets.
No stochastic trajectories are sampled. This is EXPLORATORY model accounting;
it neither replicates the prospective #411 histories nor identifies a natural
genetic-evolution-to-extinction mediator.
"""
from __future__ import annotations

from dataclasses import replace
from functools import lru_cache
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.stats import multinomial, poisson

from scripts.audit_chapter2_q3q4_exact_genotype_factorial_20261011 import (
    K, B, BUDGETS, MODES, GENOTYPES, N0,
    states, source,
)
from scripts.audit_chapter2_exact_clonal_demographic_null import static_visitors
from scripts.run_chapter2_assurance_generality import (
    load_design, DEFAULT_DESIGN, config as original_config,
)
from scripts.chapter2_kb_reproduction import reproduce_kb

ROOT = Path(__file__).resolve().parents[1]
SETTING_NAMES = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
HORIZON = 80
STATUS = "EXPLORATORY_EXACT_FOUR_MATING_SYSTEM_Q3Q4_TIMING_NOT_CONFIRMATORY"


def source_ledger(counts: tuple, budget: float, setting: str, mode: str):
    if setting not in SETTING_NAMES or mode not in MODES or budget not in BUDGETS:
        raise ValueError("unregistered exposed mating setting, phenotype or budget")
    original = source(counts)
    cfg = original_config(load_design(DEFAULT_DESIGN), setting, 0., "evolving")
    cfg = replace(cfg, capacity=K, ovule_budget=budget, survival=0.,
                  mutation_rate=0., mutation_sd=0.,
                  seed_arrival=replace(cfg.seed_arrival, supply=0.))
    if mode == "fixed_expression":
        expressed = original.alleles.copy()
        expressed[:,1,:] = .35
        original_expressed = replace(original,alleles=expressed)
    else:
        original_expressed = original
    ledger = reproduce_kb(original_expressed, static_visitors(), cfg,
                          background_denominator_capacity=B)
    matrix = ledger.outcross.copy()
    np.fill_diagonal(matrix, np.diag(matrix)+ledger.self_viable)
    return original, matrix


def source_mu_q(counts: tuple, budget: float, setting: str, mode: str):
    original, matrix = source_ledger(counts,budget,setting,mode)
    mu = float(matrix.sum())
    if mu <= 0:
        raise ArithmeticError("no viable seed source mass")
    w = matrix/mu
    p_high = (original.alleles[:,1,:] == .5).sum(axis=1)/2.
    f=p_high[:,None];m=p_high[None,:]
    q=np.array([np.sum(w*(1-f)*(1-m)),
                np.sum(w*(f*(1-m)+(1-f)*m)),
                np.sum(w*f*m)])
    if abs(float(q.sum())-1)>1e-12:
        raise ArithmeticError("Mendelian transmission mass incomplete")
    q=np.clip(q,0.,1.);q/=q.sum()
    q[-1]=max(0.,1.-float(q[:2].sum()))
    return mu,q


@lru_cache(maxsize=1)
def counts_by_n():
    return {
        n:(np.array([i for i,s in enumerate(states()) if sum(s)==n]),
           np.array([s for s in states() if sum(s)==n]))
        for n in range(K+1)
    }


def matrix(budget: float, setting: str, mode: str):
    T=np.zeros((len(states()),len(states())))
    T[0,0]=1.
    for i,s in enumerate(states()[1:],start=1):
        mu,q=source_mu_q(s,budget,setting,mode)
        pR=np.r_[poisson.pmf(np.arange(K),mu),poisson.sf(K-1,mu)]
        for n in range(K+1):
            ix,compositions=counts_by_n()[n]
            T[i,ix]=pR[n]*multinomial.pmf(compositions,n=n,p=q)
    if not np.isfinite(T).all() or (T<0).any() or not np.allclose(T.sum(axis=1),1.,atol=1e-12):
        raise ArithmeticError("invalid exact source Markov kernel")
    return T


def occupancy_trajectory(T, horizon: int=HORIZON):
    p=np.zeros(len(states()))
    p[states().index((0,N0,0))]=1.
    alive=np.array([sum(s)>0 for s in states()])
    occupancy=[]
    for t in range(horizon+1):
        occupancy.append(float(p[alive].sum()))
        if t<horizon:p=p@T
    if any(occupancy[t] < occupancy[t+1]-1e-10 for t in range(horizon)):
        raise AssertionError("closed population resurrected")
    return occupancy


def audit():
    report=[]
    for setting in SETTING_NAMES:
        for b in BUDGETS:
            a=occupancy_trajectory(matrix(b,setting,"native"))
            c=occupancy_trajectory(matrix(b,setting,"fixed_expression"))
            delta=[x-y for x,y in zip(a,c)]
            if abs(delta[0])>1e-12 or abs(delta[1])>1e-12:
                raise AssertionError("heterozygous founders not expression-matched at t0/t1")
            minimum_t=int(np.argmin(delta[1:]))+1
            first_negative=next((t for t in range(2,HORIZON+1) if delta[t]<-1e-12),None)
            report.append({
                "setting":setting,"resource_budget":b,
                "P80_native":a[-1],"P80_fixed_expression":c[-1],
                "P80_native_minus_fixed":delta[-1],
                "P20_native_minus_fixed":delta[20],
                "P2_native_minus_fixed":delta[2],
                "first_negative_delta_t":first_negative,
                "most_negative_delta_t":minimum_t,
                "minimum_delta":delta[minimum_t],
                "occupied_years_expectation_difference_T1_to_T80":float(sum(delta[1:])),
                "expected_occupied_years_native":float(sum(a[1:])),
                "expected_occupied_years_fixed":float(sum(c[1:])),
                "trajectory_t0_to_t80_delta":delta,
            })
    return {
        "schema":"chapter2_q3q4_four_mating_system_time_decomposition_v1",
        "status":STATUS,
        "n_source_settings":4,"n_budget_scales":3,
        "n_total_source_comparisons":12,"state_count":len(states()),
        "frozen_source_basis":"2026-10-06 four original reproductive rules; previously exposed 2026-10-10 K8/B48 static visitor/genotype fixture",
        "original_reproduction_code":"scripts/chapter2_kb_reproduction.py::reproduce_kb",
        "new_histories":0,"new_genetic_trajectories":0,"independent_confirmation":False,
        "inference_note":(
          "T1-to-T80 occupied years is a restricted-horizon expectation, not "
          "mean time to extinction or measured island persistence. The final "
          "binary occupancy sign may vanish/reverse near the extinction floor "
          "even while the temporal sum remains negative. This is a fixed synthetic "
          "K8 four-setting source audit, not four independent ecological systems."
        ),
        "results":report,
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    d=audit()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(d,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([{k:r[k] for k in (
        "setting","resource_budget","P80_native_minus_fixed","first_negative_delta_t",
        "most_negative_delta_t","minimum_delta","occupied_years_expectation_difference_T1_to_T80")}
        for r in d["results"]],indent=2))


if __name__=="__main__":
    main()
