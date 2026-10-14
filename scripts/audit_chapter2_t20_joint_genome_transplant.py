"""Post-outcome source replay: t20 genome-distribution transplant factorial.

Source *previously exposed* 64 model visitor histories and their selected/
channel-neutral age20 genotypes are replayed exactly. Eligible histories must
have BOTH original source populations occupied at t20. A common 8-plant
recipient census is resampled as WHOLE diploid 3-locus individuals and then
crossed with recipient K8/K48 and future selected/neutral parentage.

The intervention identifies post-survival CONDITIONAL impacts of a joint
genotype distribution, not the total causal effect of selection from t0,
pure historical drift, an independently confirmed island effect or evolution
suicide. Reuse of earlier history IDs is deliberate and fully disclosed.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_selected_vs_neutral_parentage_new64 import (
    ARMS, contract as original_contract, biological_config, demographic_streams,
    initial_genotypes, neutralize_transmitted_genomes, visitor_history,
)
from scripts.audit_chapter2_gamma_persist_exact_pair_sensitivity import (
    paired_exact_interval, classify,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.chapter2_postzygotic_viability_gate import gate_postzygotic_seed_viability
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS,stream
from scripts.model3_island.types import PlantState

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_t20_joint_genome_transplant_original_history_v1_20261010.json"
STATUS="POST_OUTCOME_AGE20_SOURCE_GENOME_TRANSPLANT_REPLAY_NOT_NEW_ECOLOGY"
SOURCE_HISTORIES=range(61024001,61024065)
DONORS=("selected_pre20","neutral_pre20")
K_TARGET=(8,48)
POST_OPERATORS=("selected_source","neutral_within_mating_channel")
EXPECTED_SOURCE_COUNTS={"selected_alive":58,"neutral_alive":52,"both_alive":50}


def contract():
    raw=DESIGN.read_bytes()
    d=json.loads(raw)
    source= d["source_pre20"]
    target=d["transplant"]
    if (d["status"]!="POST_OUTCOME_SOURCE_REPLAY_EXPLORATORY_LOCK_BEFORE_TRANSPLANT_FUTURE_OUTCOMES"
            or d["source_original_sha"]!="48eb9da3f709f40523c8bc13ce3068dc2dd97cf4"
            or source["K"]!=48 or source["ovule_budget"]!=8
            or source["gate"]!="half_self" or source["years"]!=20
            or source["selected_and_neutral_pre20_occupied_expected"]!={
                "selected":58,"neutral":52,"both":50}
            or target["at_year"]!=20 or target["run_to_year"]!=80
            or target["recipient_census_N0"]!=8
            or target["donor_genotype_distribution"]!=list(DONORS)
            or target["target_capacity_K"]!=list(K_TARGET)
            or target["future_transmission_operator"]!=list(POST_OPERATORS)
            or target["factorial_cells_per_eligible_history"]!=8
            or target["recipient_pollen_background_B"]!=48
            or target["source_biology"].find("reproduce_kb")<0
            or target["future_rng_salt"]!=61025972
            or target["neutral_parentage_rng_salt"]!=61025973
            or d["analysis"]["effect_ROPE_absolute_probability"]!=.05):
        raise ValueError("unregistered/relabelled source-transplant design")
    return d,hashlib.sha256(raw).hexdigest()


def replay_original_t20(design,history,seed,mode):
    """Byte-compatible with already exposed source runner for first 20 years."""
    if mode not in ARMS:
        raise ValueError("unknown original source parentage")
    cfg=biological_config(design,48,8.)
    current=initial_genotypes(design)
    streams=demographic_streams(design,seed)
    for t in range(20):
        if not len(current.ids):
            break
        ledger=reproduce_kb(current,history.visitors[t],cfg,
                            background_denominator_capacity=48)
        ledger=gate_postzygotic_seed_viability(
            ledger,selfed_fraction=.5,outcross_fraction=1.)
        ancestor=current
        current,info=advance(current,ledger,history.seed_candidates[t],
                             cfg,streams,year=t)
        if mode=="neutral_within_mating_channel":
            current=neutralize_transmitted_genomes(
                ancestor,current,info,cfg,seed=seed,year=t,
                salt=design["frozen_conditions"]["neutral_parentage_rng_salt"]
            )
    return current


def transplant_diploid_source(source,*,seed,donor_label):
    """Common N0=8 whole diploid genotype bootstrap, no locus-level reshuffle."""
    if donor_label not in DONORS or len(source.ids)==0:
        raise ValueError("not an eligible donor source population")
    donor_idx=DONORS.index(donor_label)
    rng=np.random.default_rng(np.random.SeedSequence([
        int(seed),61025971,donor_idx]))
    chosen=rng.integers(0,len(source.ids),size=8)
    replacement=PlantState(
        alleles=source.alleles[chosen],
        allele_origin=source.allele_origin[chosen],
        mutation_flags=source.mutation_flags[chosen],
        ids=np.arange(8,dtype=np.int64),
        birth_years=np.full(8,20,dtype=np.int64),
    )
    if (len(replacement.ids)!=8
            or not np.array_equal(replacement.alleles,source.alleles[chosen])
            or not np.array_equal(replacement.allele_origin,
                                  source.allele_origin[chosen])
            or not np.array_equal(replacement.mutation_flags,
                                  source.mutation_flags[chosen])):
        raise AssertionError("whole diploid parental genotypes not retained")
    return replacement,chosen.tolist()


def future_streams(seed):
    master=int(np.random.SeedSequence([
        int(seed),61025972]).generate_state(1)[0])
    return {name:stream(master,name,0) for name in STREAM_IDS}


def run_future(original_design,history,seed,recipient,K,future_mode):
    if (K not in K_TARGET or future_mode not in POST_OPERATORS
            or len(recipient.ids)!=8 or len(history.visitors)!=80):
        raise ValueError("invalid source-matched post20 factorial cell")
    cfg=biological_config(original_design,K,8.)
    current=recipient
    streamers=future_streams(seed)
    first_extinction=None
    for year in range(20,80):
        if not len(current.ids):
            break
        ledger=reproduce_kb(current,history.visitors[year],cfg,
                            background_denominator_capacity=48)
        ledger=gate_postzygotic_seed_viability(
            ledger,selfed_fraction=.5,outcross_fraction=1.)
        old=current
        current,info=advance(current,ledger,history.seed_candidates[year],
                             cfg,streamers,year=year)
        if future_mode=="neutral_within_mating_channel":
            current=neutralize_transmitted_genomes(
                old,current,info,cfg,seed=seed,year=year,salt=61025973)
        if not len(current.ids):
            first_extinction=year+1
    return {
        "occupied80":int(bool(len(current.ids))),
        "end_census":int(len(current.ids)),
        "first_post20_extinction":first_extinction,
        "final_allele_mean_given_occupied":(
            current.alleles.mean(axis=(0,2)).tolist()
            if len(current.ids) else None
        ),
    }


def paired_effect(values,ref,alt):
    pos=sum(int(x[ref]["occupied80"] and not x[alt]["occupied80"])
            for x in values)
    neg=sum(int(x[alt]["occupied80"] and not x[ref]["occupied80"])
            for x in values)
    n=len(values)
    if n==0:return None
    ci=paired_exact_interval(pos,neg,n)
    return {
        "n_eligible":n,
        "reference_occupied":sum(x[ref]["occupied80"] for x in values),
        "alternative_occupied":sum(x[alt]["occupied80"] for x in values),
        "reference_only":pos,"alternative_only":neg,
        "paired_difference":(pos-neg)/n,
        "conservative_95":ci,
        "classification":classify(ci),
    }


def summaries(rows):
    eligible=[r for r in rows if r["eligible"]]
    if len(eligible)!=50:
        raise AssertionError("original pre20 source BOTH-alive gate changed")
    cells=[]
    contrasts=[]
    for k in K_TARGET:
        for f in POST_OPERATORS:
            a=f"selected_pre20|K{k}|{f}"
            b=f"neutral_pre20|K{k}|{f}"
            paired=paired_effect([r["futures"] for r in eligible],a,b)
            contrasts.append({
                "effect":"selected_minus_neutral_source_genome",
                "K_recipient":k,"future_operator":f,**paired})
    for g in DONORS:
        for k in K_TARGET:
            a=f"{g}|K{k}|selected_source"
            b=f"{g}|K{k}|neutral_within_mating_channel"
            contrasts.append({
                "effect":"future_selected_minus_future_neutral_parentage",
                "G_source":g,"K_recipient":k,
                **paired_effect([r["futures"] for r in eligible],a,b),
            })
        for f in POST_OPERATORS:
            a=f"{g}|K48|{f}"
            b=f"{g}|K8|{f}"
            contrasts.append({
                "effect":"future_K48_minus_K8_given_N0_8",
                "G_source":g,"future_operator":f,
                **paired_effect([r["futures"] for r in eligible],a,b),
            })
    for g in DONORS:
        for k in K_TARGET:
            for f in POST_OPERATORS:
                tag=f"{g}|K{k}|{f}"
                cells.append({
                    "G_source":g,"K_recipient":k,"future_operator":f,
                    "n_eligible":len(eligible),
                    "n_occupied":sum(r["futures"][tag]["occupied80"]
                                     for r in eligible),
                })
    # Balanced factorial means define contrasts, not direct independently
    # identified genetic mediation or a unique Shapley attribution.
    effects={}
    for name in ("genome_source","future_operator","future_K"):
        def balanced_mean(g=None,k=None,f=None):
            tags=[f"{gg}|K{kk}|{ff}"
                  for gg in DONORS for kk in K_TARGET for ff in POST_OPERATORS
                  if (g is None or g==gg)
                  and (k is None or k==kk)
                  and (f is None or f==ff)]
            return float(np.mean([
                r["futures"][tag]["occupied80"] for r in eligible for tag in tags
            ]))
        if name=="genome_source":
            effects[name]=balanced_mean(g=DONORS[0])-balanced_mean(g=DONORS[1])
        elif name=="future_operator":
            effects[name]=balanced_mean(f=POST_OPERATORS[0])-balanced_mean(f=POST_OPERATORS[1])
        else:
            effects[name]=balanced_mean(k=48)-balanced_mean(k=8)
    return cells,contrasts,effects


def run_all():
    original,_=original_contract()
    experimental,digest=contract()
    if original["frozen_conditions"]["visitor_history_first"]!=61024001:
        raise AssertionError("wrong original immutable model history")
    rows=[]
    for seed in SOURCE_HISTORIES:
        history=visitor_history(original,seed)
        source_selected=replay_original_t20(
            original,history,seed,"selected_source")
        source_neutral=replay_original_t20(
            original,history,seed,"neutral_within_mating_channel")
        src={
            "selected_pre20":source_selected,
            "neutral_pre20":source_neutral,
        }
        eligible=all(len(x.ids)>0 for x in src.values())
        row={
            "history_seed":seed,"selected_t20_n":len(source_selected.ids),
            "neutral_t20_n":len(source_neutral.ids),"eligible":eligible,
            "ineligibility_reason":None if eligible else
                "at_least_one_original_pre20_source_extinct",
            "donor_full_genome_means":{
                label:(state.alleles.mean(axis=(0,2)).tolist()
                       if len(state.ids) else None)
                for label,state in src.items()
            },
            "donor_full_genome_dosage_variances":{
                label:(state.alleles.mean(axis=2).var(axis=0).tolist()
                       if len(state.ids) else None)
                for label,state in src.items()
            },
            "source_transplant_index":{},
            "transplanted_t20_mean":{},
            "futures":{},
        }
        if eligible:
            for label in DONORS:
                start,selected_idx=transplant_diploid_source(
                    src[label],seed=seed,donor_label=label)
                row["source_transplant_index"][label]=selected_idx
                row["transplanted_t20_mean"][label]=start.alleles.mean(axis=(0,2)).tolist()
                for k in K_TARGET:
                    for f in POST_OPERATORS:
                        tag=f"{label}|K{k}|{f}"
                        row["futures"][tag]=run_future(
                            original,history,seed,start,k,f)
        rows.append(row)
    counts={
        "selected_alive":sum(r["selected_t20_n"]>0 for r in rows),
        "neutral_alive":sum(r["neutral_t20_n"]>0 for r in rows),
        "both_alive":sum(r["eligible"] for r in rows),
    }
    if counts!=EXPECTED_SOURCE_COUNTS:
        raise AssertionError(f"original archived t20 source counts altered: {counts}")
    if sum(len(r["futures"]) for r in rows)!=50*8:
        raise AssertionError("incomplete original eligible transplant factorial")
    cells,contrasts,effects=summaries(rows)
    return {
        "status":STATUS,
        "design_sha256":digest,
        "source_original_sha":"48eb9da3f709f40523c8bc13ce3068dc2dd97cf4",
        "original_exposed_visitor_histories":64,
        "eligible_t20_joint_survivor_histories":50,
        "excluded_history_count":14,
        "transplant_futures":50*8,
        "initial_recipient_census_all_arms":8,
        "source_counts":counts,
        "cells":cells,
        "paired_effects":contrasts,
        "balanced_factorial_descriptive_effects":effects,
        "original_all_64_history_receipts":rows,
        "scientific_exclusion":[
            "Reuses identical previously exposed visitor histories; post-outcome source replay, no ecological replication.",
            "Conditioning on both year20 source arms surviving changes the target population; 50/64 is eligibility, not a valid 64-history transplant denominator.",
            "Donor genomic state is a source-genotype distribution bootstrap of 8 entire diploid plants; not exact 1-to-1 transplant and induces sampling variance.",
            "Post20 future native versus within-mating-channel neutral genome operator still does not freeze genetic drift.",
            "Balanced factor contrasts and 2-way/3-way interactions are neither a uniquely identified mediation fraction nor a field effect.",
            "Fixed-depression zero-mutation model has no deleterious genetic load/purging and does not establish evolutionary suicide.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    r=run_all()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "status":r["status"],
        "source_counts":r["source_counts"],
        "futures":r["transplant_futures"],
        "factorial_cells":r["cells"],
        "paired_effects":r["paired_effects"],
        "balanced_effects":r["balanced_factorial_descriptive_effects"],
    },sort_keys=True))


if __name__=="__main__":
    main()
