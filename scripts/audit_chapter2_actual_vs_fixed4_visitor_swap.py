"""Model3 same-genotype same-N visitor assemblage replacement at exposed states.

On 96 pre-existing stochastic-visitor pilot native expression paths (16
visitor seeds x K8/48 x budget4.5/6/8), re-evaluate the original mixed
diploid source reproductive ledger ONLY at N6..9. Replace the currently
exposed visitor assemblage by the original four visitor types at that instant
while preserving every adult genotype and actual next-year demographic law.
The visitor-replacement ledger is never sent to population.advance.

No external visitor-history replication and no ecological/trait-evolution
counterfactual is claimed. Richness and assemblage composition change jointly.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts.audit_chapter2_investment_commons_pilot_power import (
    BUDGETS,CAPS,PILOT_SEEDS,contract as original_contract,
    initial_genotypes,visitors,
)
from scripts.audit_chapter2_investment_conflict_path_replay import replay_path

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_actual_vs_fixed4_visitor_same_state_swap_20261010.json"
STATUS="RETROSPECTIVE_SAME_DIPLOID_POPULATION_STOCHASTIC_VISITOR_TO_FIXED4_REPLACEMENT"
SOURCE_96_SHA="94c45f63d6d2f34b50357aaf4bd55ed89a1a2094559b32b45dbae2e585d73db7"


def contract():
    raw=DESIGN.read_bytes()
    d=json.loads(raw)
    if (d["status"]!="POST_OUTCOME_SAME_GENOTYPE_SAME_N_VISITOR_STATE_REPLACEMENT"
            or d["source_exact_sha256"]!=SOURCE_96_SHA
            or d["original_n_stochastic_states"]!=1533):
        raise ValueError("original-source visitor replacement altered")
    return d,hashlib.sha256(raw).hexdigest()


def _type(res):
    return ("conflict" if res["mixed_genotype_majority_conflict"]
            else "not_conflict")


def run_all():
    _,design_hash=contract()
    original,_=original_contract()
    founder,_=initial_genotypes(original)
    ref=visitors(original,9701291,"static_matched4").visitors[0]
    paths=[]
    events=[]
    for seed in PILOT_SEEDS:
        hist=visitors(original,seed,"stochastic_matched4")
        for K in CAPS:
            for budget in BUDGETS:
                r=replay_path(
                    original,founder,hist,seed,"stochastic_matched4",
                    K,budget,"native",diagnose=True,
                    reference_visitor_state=ref,
                )
                paths.append(r)
                for y in r["complete_native_or_centered_80_annual_states"]:
                    old=y["actual_native_mixed_genotype_window"]
                    if old is None:
                        continue
                    counter=old["same_genotype_static_four_visitor_counterfactual"]
                    events.append({
                        "seed":seed,"K":K,"budget":budget,"t":y["t"],
                        "N":y["N"],
                        "observed_visitor_richness":y["visitor_type_count"],
                        "original_visitor_conflict":bool(old["mixed_genotype_majority_conflict"]),
                        "reference_4_visitor_conflict":bool(counter["mixed_genotype_majority_conflict"]),
                        "original_gamma_positive":bool(old["gamma_positive"]),
                        "reference_gamma_positive":bool(counter["gamma_positive"]),
                        "original_focal_negative_count":int(old["focal_beta_negative_count"]),
                        "reference_focal_negative_count":int(counter["focal_beta_negative_count"]),
                        "original_focal_positive_externality_count":int(old["positive_nonneighbor_externality_focal_count"]),
                        "reference_focal_positive_externality_count":int(counter["positive_nonneighbor_externality_focal_count"]),
                    })
    original_results=[p["original_pilot_result"] for p in paths]
    original_hash=hashlib.sha256(json.dumps(
        original_results,sort_keys=True,separators=(",",":"),
        allow_nan=False).encode()).hexdigest()
    if original_hash!=SOURCE_96_SHA:
        raise AssertionError(f"96 original source paths changed: {original_hash}")
    if len(events)!=1533:
        raise AssertionError("not all original N6-9 source visitor states re-evaluated")
    categories={
        "both_conflict":sum(x["original_visitor_conflict"] and x["reference_4_visitor_conflict"] for x in events),
        "original_only_conflict":sum(x["original_visitor_conflict"] and not x["reference_4_visitor_conflict"] for x in events),
        "reference4_only_conflict":sum(not x["original_visitor_conflict"] and x["reference_4_visitor_conflict"] for x in events),
        "neither_conflict":sum(not x["original_visitor_conflict"] and not x["reference_4_visitor_conflict"] for x in events),
    }
    if sum(categories.values())!=1533:
        raise AssertionError("cross-classification missing visitor states")
    by_cell=[]
    for K in CAPS:
        for budget in BUDGETS:
            sub=[x for x in events if x["K"]==K and x["budget"]==budget]
            by_cell.append({
                "K":K,"budget":budget,"n_annual_original_path_states":len(sub),
                "original_observed_conflict_years":sum(x["original_visitor_conflict"] for x in sub),
                "static_four_replacement_conflict_years":sum(x["reference_4_visitor_conflict"] for x in sub),
                "original_gamma_positive_years":sum(x["original_gamma_positive"] for x in sub),
                "static_four_gamma_positive_years":sum(x["reference_gamma_positive"] for x in sub),
                "original_visitor_richness_values":sorted(set(x["observed_visitor_richness"] for x in sub)),
            })
    by_richness=[]
    for n in sorted(set(x["observed_visitor_richness"] for x in events)):
        sub=[x for x in events if x["observed_visitor_richness"]==n]
        by_richness.append({
            "original_visitor_type_count":n,
            "n_path_years_N6_9":len(sub),
            "actual_original_conflict_years":sum(x["original_visitor_conflict"] for x in sub),
            "static_four_replacement_conflict_years":sum(x["reference_4_visitor_conflict"] for x in sub),
            "not_independent_environment_replicates":True,
        })
    return {
        "status":STATUS,
        "design_sha256":design_hash,
        "original_source_96_path_exact_sha256":original_hash,
        "n_exposed_native_stochastic_paths":len(paths),
        "n_original_pre_repro_N6_9_states":len(events),
        "new_visitor_RNG_histories_created":0,
        "source_visitor_state_replacement_cross_classification":categories,
        "by_K_budget":by_cell,
        "by_current_visitor_richness":by_richness,
        "all_1533_same_genotype_same_N_counterfactual_visitor_comparisons":events,
        "scientific_limits":[
            "Only the instant expected Model3 reproduction ledger is re-evaluated with another fixed visitor assemblage; source genetic paths, RNG, and real demographic outcomes are unchanged.",
            "Original four types are a fixed hand-authored counterfactual and do not isolate visitor richness from pollinator type identity/effectiveness.",
            "The 1533 years derive from 96 paths and just 16 original visitor seeds under shared settings, not 1533 independently observed island populations.",
            "Changing visitor mixture may alter beta/gamma in the instant but does not establish future investment allele evolution, population persistence or natural flower size dynamics.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    res=run_all()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(res,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":res["status"],
        "n":res["n_original_pre_repro_N6_9_states"],
        "cross":res["source_visitor_state_replacement_cross_classification"],
        "by_cell":res["by_K_budget"]
    },sort_keys=True))


if __name__=="__main__":
    main()
