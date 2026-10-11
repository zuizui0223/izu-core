"""Source-native no-visitor falsifier for Q3 genetic expression → Q4 occupancy.

Uses the unchanged Model 3 K/B pollen-and-selfing ledger and finite K8
Mendelian/Poisson demographic kernel. Original mating settings and only the
already exposed resource budgets 6 and 8. ALL results are post-discovery
restricted synthetic source counterfactuals, not observed island extinction.
"""
from __future__ import annotations

from dataclasses import replace
from functools import lru_cache
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.stats import multinomial,poisson

from scripts.audit_chapter2_q3q4_exact_genotype_factorial_20261011 import (
    K,B,N0,MODES,states,source,
)
from scripts.audit_chapter2_exact_clonal_demographic_null import static_visitors
from scripts.model3_island.types import VisitorState
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN,load_design,config as original_config,
)
from scripts.chapter2_kb_reproduction import reproduce_kb

SETTINGS=("delayed_control","prior_selfing","pollen_discount","assurance_cost")
SCENARIOS=("visitors4","visitors0")
BUDGETS=(6.0,8.0)
HORIZON=80
STATUS="EXPLORATORY_EXACT_POLLINATOR_ABSENCE_Q3Q4_SOURCE_FALSIFIER_NOT_CAUSAL_FIELD_RESULT"


def visitors(which):
    if which=="visitors4":return static_visitors()
    if which!="visitors0":raise ValueError("unknown visitor scenario")
    return VisitorState(
        ids=np.empty(0,dtype=np.int64),
        optima=np.empty(0,dtype=float),
        breadths=np.empty(0,dtype=float),
        effectiveness=np.empty(0,dtype=float),
    )


@lru_cache(maxsize=1)
def by_n():
    s=states()
    return {
        n:(
            np.array([i for i,x in enumerate(s) if sum(x)==n],dtype=int),
            np.array([x for x in s if sum(x)==n],dtype=int),
        )
        for n in range(K+1)
    }


@lru_cache(maxsize=None)
def cfg(setting,budget):
    if setting not in SETTINGS or budget not in BUDGETS:
        raise ValueError("unregistered mating system or resource")
    original=original_config(load_design(DEFAULT_DESIGN),setting,0.,"evolving")
    return replace(original,capacity=K,ovule_budget=budget,survival=0.,
                   mutation_rate=0.,mutation_sd=0.,
                   seed_arrival=replace(original.seed_arrival,supply=0.))


def mu_and_q(counts,setting,budget,scenario,mode):
    if scenario not in SCENARIOS or mode not in MODES:
        raise ValueError("unregistered scenario/expression policy")
    genome=source(counts)
    expressed=genome
    if mode=="fixed_expression":
        aa=genome.alleles.copy()
        aa[:,1,:]=.35
        expressed=replace(genome,alleles=aa)
    ledger=reproduce_kb(expressed,visitors(scenario),cfg(setting,budget),
                        background_denominator_capacity=B)
    matrix=ledger.outcross.copy()
    np.fill_diagonal(matrix,np.diag(matrix)+ledger.self_viable)
    mu=float(matrix.sum())
    if not np.isfinite(mu) or mu<=0:
        raise ArithmeticError("nonpositive original source viable seed")
    weights=matrix/mu
    # Crucial regression protection from PR #466: infer gamete classes from
    # genotype CLASS, not floating numeric allele equality.
    hi=np.repeat(np.array([0.,.5,1.]),np.asarray(counts,dtype=int))
    father=hi[:,None];mother=hi[None,:]
    q=np.array([
        np.sum(weights*(1-father)*(1-mother)),
        np.sum(weights*(father*(1-mother)+(1-father)*mother)),
        np.sum(weights*father*mother),
    ])
    if abs(float(q.sum())-1)>1e-12:raise ArithmeticError("lost parental mass")
    q=np.clip(q,0.,1.);q/=q.sum()
    q[-1]=max(0.,1.-float(q[:2].sum()))
    return mu,q,float(ledger.delivered.sum()),float(ledger.outcross.sum())


def transition(setting,budget,scenario,mode):
    all_states=states()
    T=np.zeros((len(all_states),len(all_states)),dtype=float)
    T[0,0]=1.
    for i,s in enumerate(all_states[1:],start=1):
        mu,q,_,_=mu_and_q(s,setting,budget,scenario,mode)
        recruitment=np.r_[poisson.pmf(np.arange(K),mu),poisson.sf(K-1,mu)]
        for n in range(K+1):
            ix,compositions=by_n()[n]
            T[i,ix]=recruitment[n]*multinomial.pmf(compositions,n=n,p=q)
    if (T<0).any() or not np.allclose(T.sum(axis=1),1.,rtol=0,atol=1e-12):
        raise ArithmeticError("nonstochastic genomic/demographic transition")
    return T


def occupancy(T):
    all_states=states()
    p=np.zeros(len(all_states))
    p[all_states.index((0,N0,0))]=1.
    alive=np.asarray([sum(s)>0 for s in all_states])
    out=[]
    for t in range(HORIZON+1):
        out.append(float(p[alive].sum()))
        if t<HORIZON:p=p@T
    return out


def audit():
    result=[]
    for setting in SETTINGS:
        for budget in BUDGETS:
            for scenario in SCENARIOS:
                raw={mode:occupancy(transition(setting,budget,scenario,mode))
                     for mode in MODES}
                d=[x-y for x,y in zip(raw["native"],raw["fixed_expression"])]
                if abs(d[0])>1e-12 or abs(d[1])>1e-12:
                    raise AssertionError("matched founder and first-generation laws broken")
                mu,q,delivered,outcross=mu_and_q((0,8,0),setting,budget,scenario,"native")
                if scenario=="visitors0" and (delivered!=0 or outcross!=0):
                    raise AssertionError("zero-visitor control still transferred pollen")
                result.append({
                    "setting":setting,"resource_budget":budget,"visitor_scenario":scenario,
                    "source_N8_viable_seed_intensity":mu,
                    "source_N8_total_delivered_pollen":delivered,
                    "source_N8_outcross_seeds":outcross,
                    "P80_native":raw["native"][-1],
                    "P80_fixed_expression":raw["fixed_expression"][-1],
                    "P80_native_minus_fixed":d[-1],
                    "P20_native_minus_fixed":d[20],
                    "expected_occupied_years_delta_t1_80":float(sum(d[1:])),
                    "first_negative_difference":next((t for t in range(2,81) if d[t]<-1e-12),None),
                    "trajectory":d,
                })
    return {
        "schema":"chapter2_q3q4_no_visitor_exact_native_model_v1",
        "status":STATUS,
        "source":"unchanged Model3 reproduce_kb, K8/B48 clonal visitors4 vs visitors0",
        "n_cases":len(result),"K":K,"B":B,"N0":N0,"states":len(states()),
        "new_history_draws":0,"natural_ecological_systems":0,
        "independent_confirmation":False,
        "interpretation":"Within artificial K8/B48 Model3, the sign of the 80-step genotype-expression contrast can switch when all visitors are removed. This does not identify evolved pollinator extinction, conspecific public-good mediation, genetic order or a natural island evolutionary-suicide mechanism.",
        "results":result,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    a=parser.parse_args()
    r=audit();a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps([{k:x[k] for k in (
        "setting","resource_budget","visitor_scenario","P80_native_minus_fixed"
    )} for x in r["results"]],sort_keys=True))


if __name__=="__main__":main()
