"""Source Model3 finite census N causes a β sign crossover plus cap bottleneck.

Post-pilot diagnostic only. No visitor RNG histories or demographic
trajectory simulation. Entire density/seed intensity grid uses original
Model3 reproduce_kb and original exact capped Poisson recruitment moment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path
import numpy as np

from scripts.audit_chapter2_beta_gamma_seed_map import (
    visitors_for,state_of_clones,changed_state,local_slopes,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.population import subset
from scripts.model3_island.expectation import capped_poisson_mean
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN,config as source_config,load_design,
)

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_investment_density_selection_source_diagnostic_20261010.json"
STATUS="POST_PILOT_CENSUS_SENSITIVE_INVESTMENT_SELECTION_AND_CAP_RECRUITMENT"
BUDGETS=(4.5,6.0,8.0)
CAPS=(8,48)


def contract():
    raw=DESIGN.read_bytes()
    d=json.loads(raw)
    if (d["status"]!="POST_PILOT_MECHANISTIC_DIAGNOSIS_NOT_INDEPENDENT_TEST"
            or d["grid"]["source_N_min"]!=1
            or d["grid"]["source_N_max"]!=48
            or d["grid"]["capacity_K"]!=[8,48]
            or d["grid"]["source_ovule_budget"]!=[4.5,6,8]
            or d["model_states"]["pollen_B"]!=48):
        raise ValueError("source census-selection diagnostic contract changed")
    return d,hashlib.sha256(raw).hexdigest()


def expected_nonfocal_derivative(state,visitor,cfg,h):
    """Net OTHER maternal viable seeds, not another plant's father payoff."""
    def nonfocal(sgn):
        z=changed_state(state,1,sgn*h,whole=False)
        l=reproduce_kb(z,visitor,cfg,background_denominator_capacity=48)
        return float(l.outcross[:,1:].sum()+l.self_viable[1:].sum())
    return (nonfocal(+1)-nonfocal(-1))/(2*h)


def source_row(N,K,budget,visitor,parent48):
    if (not isinstance(N,int) or N<1 or K not in CAPS or N>K or
            budget not in BUDGETS):
        raise ValueError("unregistered source census or K/budget")
    cfg=replace(source_config(load_design(DEFAULT_DESIGN),
                              "delayed_control",0.0,"evolving"),
                capacity=K,ovule_budget=budget,mutation_rate=0.,survival=0.)
    plant=subset(parent48,np.arange(N,dtype=int))
    a=local_slopes(plant,visitor,cfg,1,.005)
    b=local_slopes(plant,visitor,cfg,1,.0025)
    derivative=expected_nonfocal_derivative(plant,visitor,cfg,.005)
    r=reproduce_kb(plant,visitor,cfg,background_denominator_capacity=48)
    seeds=float(r.outcross.sum()+r.self_viable.sum())
    cap_mean=float(capped_poisson_mean(seeds,K))
    if (not np.isclose(a["beta_one_individual"],b["beta_one_individual"],
                       atol=1e-3,rtol=0)
            or not np.isclose(a["gamma_group_seed"],b["gamma_group_seed"],
                              atol=1e-3,rtol=0)):
        raise AssertionError("source density gradient unstable under step halving")
    return {
        "census_N":N,"K":K,"B":48,"budget":budget,
        "beta_log_focal_investment":a["beta_one_individual"],
        "collective_log_group_seed_gamma":a["gamma_group_seed"],
        "beta_component_F":a["beta_components"]["maternal_outcross_F"],
        "beta_component_P":a["beta_components"]["paternal_outcross_P"],
        "beta_component_S":a["beta_components"]["viable_self_S"],
        "nonfocal_viable_seed_derivative_unilateral":derivative,
        "group_viable_seeds_uncapped":seeds,
        "group_viable_seeds_per_parent":seeds/N,
        "exact_capped_Poisson_expected_children":cap_mean,
        "expected_delta_census":cap_mean-N,
        "beta_sign":"+" if a["beta_one_individual"]>1e-8 else (
            "-" if a["beta_one_individual"]<-1e-8 else "0"),
        "gamma_sign":"+" if a["gamma_group_seed"]>1e-8 else (
            "-" if a["gamma_group_seed"]<-1e-8 else "0"),
        "pilot_history_status":"NO_HISTORY_OR_PERSISTENCE_OUTCOMES_USED"
    }


def run_all():
    d,digest=contract()
    parent48=state_of_clones((.2,.35,.35),48)
    v=visitors_for("matched4",{"visitor_regimes":{
        "matched4":{"optima":[.15,.35,.55,.75],
                    "breadths":[.18]*4,"effectiveness":[1.]*4}
    }})
    rows=[]
    for K in CAPS:
        for budget in BUDGETS:
            for N in range(1,K+1):
                rows.append(source_row(N,K,budget,v,parent48))
    if len(rows)!=168:
        raise AssertionError("missing one of 168 model/source census budget states")
    key={(r["K"],r["budget"],r["census_N"]):r for r in rows}
    source8=key[(8,8.,8)]
    source48=key[(48,8.,48)]
    if (not np.isclose(source8["beta_log_focal_investment"],
                       -.0631736695408891,atol=1e-11,rtol=0)
            or not np.isclose(source48["beta_log_focal_investment"],
                              .584002628056346,atol=1e-11,rtol=0)):
        raise AssertionError("original 384-grid finite source beta sign references changed")
    if (source8["gamma_sign"]!="+" or source48["gamma_sign"]!="+"
            or source8["beta_sign"]!="-" or source48["beta_sign"]!="+"):
        raise AssertionError("original strong β x Gamma census mechanism lost")
    summaries=[]
    for K in CAPS:
        for budget in BUDGETS:
            subset_rows=[key[(K,budget,N)] for N in range(1,K+1)]
            change=[r["census_N"] for r in subset_rows
                    if r["beta_sign"]=="+"]
            summaries.append({
                "K":K,"budget":budget,"beta_negative_N":[
                    r["census_N"] for r in subset_rows if r["beta_sign"]=="-"],
                "beta_positive_N":change,
                "first_census_with_beta_positive":min(change) if change else None,
                "last_census_with_beta_negative":max(
                    (r["census_N"] for r in subset_rows if r["beta_sign"]=="-"),
                    default=None),
                "group_gamma_positive_N_count":sum(
                    r["gamma_sign"]=="+" for r in subset_rows),
                "all_visitor_present_nonneighbor_effect_positive_for_N_ge_2":
                    all(r["nonfocal_viable_seed_derivative_unilateral"]>0
                        for r in subset_rows if r["census_N"]>=2),
                "source_at_N8":key[(K,budget,8)],
                "source_at_full_K":key[(K,budget,K)],
            })
    return {
        "status":STATUS,
        "design_sha256":digest,
        "source_cases":len(rows),
        "independent_visitor_histories":0,
        "independent_ecological_island_systems":0,
        "source_monomorphic_beta_reproduces_previous_384_grid":True,
        "per_capacity_budget_selection_thresholds":summaries,
        "full_census_grid":rows,
        "scientific_boundary":[
            "Original Model3 only; source monomorphic no-history census grid AFTER 16-history engineering pilot, not a novel ecological experiment.",
            "Changing N with B=48 fixed changes parentage competition and local focal β; K8 β sign must NOT be transferred to K48 at N48.",
            "At K8 N8, E[min(Poisson(seed_count),K8)] can be below8 even when expected total viable seeds exceed8; capacity and stochastic demographic sinks coexist.",
            "For parent and allele evolution with different genetic means, or time-varying visitors, local monomorphic β(N) alone is not a realized mean allele change, evolutionary suicide or extinction probability.",
            "The density grid cannot select a new budget or visitor regime from post-outcome successes and call it preregistered."
        ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    out=run_all()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":out["status"],
        "cases":out["source_cases"],
        "thresholds":[{
            "K":r["K"],"budget":r["budget"],
            "first_positive_beta_N":r["first_census_with_beta_positive"],
            "last_negative_beta_N":r["last_census_with_beta_negative"],
            "N8_beta":r["source_at_N8"]["beta_log_focal_investment"],
            "N8_next_mean":r["source_at_N8"]["exact_capped_Poisson_expected_children"],
            "N8_unthinned_seeds":r["source_at_N8"]["group_viable_seeds_uncapped"],
        } for r in out["per_capacity_budget_selection_thresholds"]]
    },sort_keys=True))


if __name__=="__main__":
    main()
