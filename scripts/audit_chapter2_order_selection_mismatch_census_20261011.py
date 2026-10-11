"""Q1 mechanism of evolutionary order: fixed-genome local fitness-sign timing.

Exact original Model3 reproductive source W_i = .5(F_i+P_i)+S_i, not only
maternal fitness. Declining floral-visitor functional matching is crossed with
source census N and independently with assurance timing and cost.

The visitor assembly has four types at EVERY mismatch stage. Every plant
genotype is held constant. This diagnostic does NOT identify a historical
mutation, allele-frequency change, actual threshold-crossing time, or a
natural ecological temporal causation mechanism. All exposed settings are
post-discovery synthetic source calculations, not independent island systems.
"""
from __future__ import annotations
from dataclasses import replace
from pathlib import Path
import argparse
import json

import numpy as np

from scripts.model3_island.types import PlantState, VisitorState
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, load_design, config as original_config
)

N_VALUES=(8,24,48)
TIMINGS=("delayed","prior")
ASSURANCE_COSTS=(0.,.5)
FRACTIONS=(0.,.25,.5,.75,1.)
STEPS=(.005,.0025)
MATCHED=np.array([.15,.35,.55,.75])
SHIFTED=np.array([.65,.75,.85,.95])
B=48
OVULE_BUDGET=6.
STATUS="POSTDISCOVERY_ORIGINAL_SOURCE_FOCAL_FITNESS_N_BY_FUNCTIONAL_MATCH_NOT_ACTUAL_ORDER"


def plants(n:int):
    if type(n) is not int or n not in N_VALUES:
        raise ValueError("source census outside diagnostic")
    a=np.broadcast_to(np.array([.20,.35,.35])[None,:,None],(n,3,2)).copy()
    return PlantState(
        alleles=a,
        allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        mutation_flags=np.zeros((n,3,2),dtype=bool),
        ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64)
    )


def visitor_state(fraction):
    if fraction not in FRACTIONS: raise ValueError("unknown matching fraction")
    return VisitorState(
        ids=np.arange(4,dtype=np.int64),
        optima=MATCHED+fraction*(SHIFTED-MATCHED),
        breadths=np.full(4,.18),
        effectiveness=np.ones(4),
    )


def source_config(timing,cost):
    if timing not in TIMINGS or cost not in ASSURANCE_COSTS:
        raise ValueError("unknown mating-timing or direct assurance-cost arm")
    cfg=original_config(load_design(DEFAULT_DESIGN),"delayed_control",0.,"evolving")
    return replace(cfg,capacity=48,ovule_budget=OVULE_BUDGET,
                   assurance_timing=timing,assurance_cost=cost,
                   mutation_rate=0.,mutation_sd=0.,
                   seed_arrival=replace(cfg.seed_arrival,supply=0.))


def genetic_return(source,visitors,cfg,where=0):
    led=reproduce_kb(source,visitors,cfg,background_denominator_capacity=B)
    F=led.outcross.sum(axis=0)
    P=led.outcross.sum(axis=1)
    S=led.self_viable
    W=.5*(F+P)+S
    total=float(led.outcross.sum()+S.sum())
    if not np.isclose(W.sum(),total,rtol=0,atol=1e-11):
        raise ArithmeticError("maternal/paternal/self contributions lost")
    if np.any(W<=0): raise ArithmeticError("nonpositive focal genetic return")
    return {
        "W":float(W[where]),
        "group_seed":total,
        "pollen_delivery":float(led.delivered.sum()),
        "group_outcross":float(led.outcross.sum()),
        "F":float(F[where]),
        "P":float(P[where]),
        "S":float(S[where]),
    }


def perturb(source,trait,delta,whole=False):
    if trait not in ("investment","assurance"):
        raise ValueError("unknown floral phenotype")
    ix={"investment":1,"assurance":2}[trait]
    a=source.alleles.copy()
    if whole:a[:,ix,:]+=delta
    else:a[0,ix,:]+=delta
    if ((a<0)|(a>1)).any(): raise ValueError("mutation step left biological bounds")
    return replace(source,alleles=a)


def gradient(n,timing,cost,fraction,trait,step):
    if step not in STEPS:raise ValueError("unregistered finite-gradient step")
    source=plants(n);v=visitor_state(fraction);cfg=source_config(timing,cost)
    positive=genetic_return(perturb(source,trait,+step),v,cfg)
    negative=genetic_return(perturb(source,trait,-step),v,cfg)
    focal_beta=(np.log(positive["W"])-np.log(negative["W"]))/(2*step)
    return float(focal_beta)


def gradient_sign(x,deadband=.02):
    if not np.isfinite(x):return "unresolved"
    if x>deadband:return "positive"
    if x<-deadband:return "negative"
    return "near_zero"


def audit():
    rows=[]
    for n in N_VALUES:
        for timing in TIMINGS:
            for cost in ASSURANCE_COSTS:
                for fraction in FRACTIONS:
                    bas=genetic_return(plants(n),visitor_state(fraction),
                                       source_config(timing,cost))
                    gradients={}
                    for trait in ("assurance","investment"):
                        a,b=[gradient(n,timing,cost,fraction,trait,h) for h in STEPS]
                        if abs(a-b)> .02 + .05*max(abs(a),abs(b)):
                            tag="unstable"
                        else:tag=gradient_sign(a)
                        gradients[trait]={"focal_log_genetic_gradient":a,
                                          "refinement":b,"status":tag}
                    rows.append({
                        "n_adults":n,"assurance_timing":timing,"assurance_cost":cost,
                        "functional_mismatch_fraction":fraction,
                        "visitor_functional_types":4,
                        "focal_selection":gradients,
                        "reference_focal_W":bas["W"],
                        "reference_total_seed_mu":bas["group_seed"],
                        "reference_delivered_pollen":bas["pollen_delivery"],
                        "reference_outcross_seeds":bas["group_outcross"],
                    })
    condensed=[]
    for n in N_VALUES:
        for timing in TIMINGS:
            for cost in ASSURANCE_COSTS:
                r=[x for x in rows if x["n_adults"]==n and x["assurance_timing"]==timing
                   and x["assurance_cost"]==cost]
                r=sorted(r,key=lambda z:z["functional_mismatch_fraction"])
                signs=[x["focal_selection"]["investment"]["status"] for x in r]
                first_negative=next((x["functional_mismatch_fraction"]
                     for x in r if x["focal_selection"]["investment"]["status"]=="negative"),None)
                condensed.append({
                    "n_adults":n,"assurance_timing":timing,"assurance_cost":cost,
                    "investment_sign_path":signs,
                    "assurance_sign_path":[x["focal_selection"]["assurance"]["status"] for x in r],
                    "first_analysed_mismatch_step_with_negative_investment_gradient":first_negative,
                    "positive_to_negative_between_tested_steps":(
                        signs[0]=="positive" and "negative" in signs[1:]),
                })
    return {
        "schema":"chapter2_order_local_fitness_sign_functional_match_and_density_v1",
        "status":STATUS,
        "source":"native original Model 3 reproduce_kb / full W .5 F + .5 P + S",
        "n_cells":len(rows),"n_original_mating_factorial_combinations":4,
        "n_plant_census_states":3,"n_functional_mismatch_steps":5,
        "n_independent_natural_islands":0,"n_new_evolutionary_histories":0,
        "assurance_mode":"evolving; both source traits cloned and held fixed",
        "notes":[
            "Source local beta signs are directional FITNESS derivatives, not dates of mutation, genomic response or observed chronology.",
            "Assurance and investment gradients may both be nonzero at baseline; a first observed 0.05 change can instead reflect genetic variance and drift.",
            "Historical prior-selfing and delayed-selfing settings had different direct assurance costs: this 2x2 factorial separates those source factors at identical genomes and visitors.",
            "Only K48 is the actual common source capacity; N8/N24/N48 vary current census, not K, and share pollen background B48.",
            "Mismatch stages are historical synthetic four-visitor trait replacements and their interpolation; these are NOT separate islands or empirical functional traits.",
        ],
        "rows":rows,"by_source_factorial":condensed
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    r=audit();args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(r,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps(r["by_source_factorial"],sort_keys=True))


if __name__=="__main__":main()
