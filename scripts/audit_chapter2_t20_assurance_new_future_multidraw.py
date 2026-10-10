"""Conditional t20 assurance-genome transfer into NEW future visitor innovations.

Previously exposed source donor populations are replayed for t0..t19 only.
The future ecological transitions use 64 NEW RNG visitor seeds, mapped
one-to-one to original source history IDs and inheriting the original t20
visitor state. Three whole-diploid genotype resamples are nested per eligible
original source history, never regarded as 150 independent ecological units.

No new independent source donor histories, no natural ecological replication,
no unique assurance mediation fraction, no evolutionary suicide conclusion.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_t20_joint_genome_transplant import (
    SOURCE_HISTORIES,EXPECTED_SOURCE_COUNTS,original_contract,
    replay_original_t20,run_future,visitor_history,
)
from scripts.audit_chapter2_t20_assurance_locus_hybrid import (
    ARMS,genotypes_by_module
)
from scripts.audit_chapter2_selected_vs_neutral_parentage_new64 import (
    biological_config
)
from scripts.model3_island.history import make_history
from scripts.model3_island.types import PlantState,History

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_t20_assurance_new_future_multidraw_20261010.json"
STATUS="NEW_POST20_ECOLOGY_OLD_SOURCE_T20_CONDITIONAL_MULTIDRAW_GENOTYPE_TRANSFER"
FUTURE_SEEDS=range(61026001,61026065)
TEST_FUTURE_SEED=990893  # source-only smoke never consumes registered new visitor IDs
DRAWS=3
CAPS=(8,48)


def contract():
    blob=DESIGN.read_bytes()
    d=json.loads(blob)
    q=d["new_future"]
    e=d["experiment"]
    p=d["primary"]
    if (d["status"]!="FROZEN_BEFORE_NEW_FUTURE_ECOLOGY_OUTCOMES_MODEL_INTERNAL_TRANSFER"
            or q["seed_first"]!=61026001
            or q["seed_last"]!=61026064
            or q["inherit_t20_visitor_state"] is not True
            or e["original_source_K"]!=48
            or e["original_source_budget"]!=8
            or e["original_source_gate"]!="half_self"
            or e["source_first_updates"]!=20
            or e["recipient_N0"]!=8 or e["recipient_B"]!=48
            or e["genome_draws_per_source_history"]!=3
            or e["independent_genotype_draw_salt"]!=61026971
            or e["genomic_locus_compositions"]!=list(ARMS)
            or e["recipient_future_K"]!=[8,48]
            or e["future_trajectories_expected"]!=1200
            or p["bootstrap_seed"]!=61026999
            or p["rope_absolute_survival_probability"]!=.05):
        raise ValueError("frozen conditional ecological-transfer design changed")
    return d,hashlib.sha256(blob).hexdigest()


def mapped_new_future_seed(original_source_seed):
    if type(original_source_seed) is not int or original_source_seed not in SOURCE_HISTORIES:
        raise ValueError("not a registered original model source history")
    return 61026001+(original_source_seed-61024001)


def new_future_history(original,original_history,new_seed):
    if type(new_seed) is not int or (new_seed not in FUTURE_SEEDS and new_seed!=TEST_FUTURE_SEED):
        raise ValueError("only frozen, unused new future ecological histories")
    inherited=original_history.visitors[20]
    cfg=replace(biological_config(original,48,8.),
                years=60,initial_visitors=len(inherited.ids))
    future=make_history(cfg,seed=new_seed,inherited_visitors=inherited)
    if (len(future.visitors)!=60 or len(future.seed_candidates)!=60
            or not np.array_equal(future.visitors[0].optima,inherited.optima)
            or not np.array_equal(future.visitors[0].ids,inherited.ids)
            or any(len(s.ids) for s in future.seed_candidates)):
        raise AssertionError("new future visitor innovations not source-matched")
    hybrid=History(
        visitors=original_history.visitors[:20]+future.visitors,
        seed_candidates=original_history.seed_candidates[:20]+future.seed_candidates,
        event_order=original_history.event_order,
        initialization="controlled",
    )
    if (len(hybrid.visitors)!=80 or len(hybrid.seed_candidates)!=80
            or any(hybrid.visitors[i] is not original_history.visitors[i]
                   for i in range(20))
            or hybrid.visitors[20] is not future.visitors[0]):
        raise AssertionError("original donor ecology and new post20 ecology incorrectly spliced")
    return hybrid


def sample_eight_individuals(donor,*,source_history_seed,donor_label,draw):
    if (donor_label not in ("selected_pre20","neutral_pre20")
            or type(draw) is not int or not 0<=draw<DRAWS
            or source_history_seed not in SOURCE_HISTORIES
            or len(donor.ids)==0):
        raise ValueError("invalid donor genotype draw/seed")
    donor_index=0 if donor_label=="selected_pre20" else 1
    rng=np.random.default_rng(np.random.SeedSequence([
        source_history_seed,61026971,donor_index,draw]))
    indices=rng.integers(0,len(donor.ids),size=8)
    st=PlantState(
        alleles=donor.alleles[indices],
        allele_origin=donor.allele_origin[indices],
        mutation_flags=donor.mutation_flags[indices],
        ids=np.arange(8,dtype=np.int64),
        birth_years=np.full(8,20,dtype=np.int64),
    )
    if (not np.array_equal(st.alleles,donor.alleles[indices])
            or not np.array_equal(st.allele_origin,donor.allele_origin[indices])
            or not np.array_equal(st.mutation_flags,donor.mutation_flags[indices])):
        raise AssertionError("whole-genome source cannot be split by allele")
    return st,indices.tolist()


def paired_interval(values,seed=61026999):
    """Values are ONE average of three paired donor draws per source history.

    Cluster bootstrap is interpretive, not the only CI. The Hoeffding interval
    handles zero-discordance/ceiling cells without asserting equivalence.
    """
    x=np.asarray(values,dtype=float)
    if x.ndim!=1 or len(x)<2 or np.any(~np.isfinite(x)) or np.any(x<-1) or np.any(x>1):
        raise ValueError("paired source-history average outside [-1,1]")
    rng=np.random.default_rng(seed)
    draws=rng.integers(0,len(x),size=(1999,len(x)))
    means=x[draws].mean(axis=1)
    lo,hi=np.quantile(means,[.025,.975])
    delta=float(x.mean())
    hoeffding=float(np.sqrt(2*np.log(2/.05)/len(x)))
    h_ci=[max(-1.,delta-hoeffding),min(1.,delta+hoeffding)]
    bootstrap_ci=[float(lo),float(hi)]
    rope=.05
    if bootstrap_ci[0]>rope and h_ci[0]>rope:
        verdict="resolved_positive"
    elif bootstrap_ci[1]<-rope and h_ci[1]<-rope:
        verdict="resolved_negative"
    elif (bootstrap_ci[0]>=-rope and bootstrap_ci[1]<=rope
          and h_ci[0]>=-rope and h_ci[1]<=rope):
        verdict="practically_equivalent"
    else:
        verdict="inconclusive"
    return {
        "effect":delta,
        "cluster_bootstrap_95":bootstrap_ci,
        "hoeffding_95_for_cluster_means":h_ci,
        "hoeffding_radius":hoeffding,
        "classification":verdict,
        "n_independent_old_donor_history_units":len(x),
        "independent_genotype_draws_per_source_history":DRAWS,
    }


def summarise(all_rows):
    eligible=[r for r in all_rows if r["eligible"]]
    if len(eligible)!=50:
        raise AssertionError("source t20 both-survival cohort changed")
    out=[]
    for k in CAPS:
        def contrast(a,b):
            per_history=[]
            for row in eligible:
                vals=[]
                for d in row["draws"]:
                    vals.append(
                        d["future_occupancy"][f"{a}|K{k}"]
                        -d["future_occupancy"][f"{b}|K{k}"]
                    )
                if len(vals)!=DRAWS:
                    raise AssertionError("missing donor draws")
                per_history.append(float(np.mean(vals)))
            return paired_interval(per_history)
        effects={
            "assurance_only_over_neutral_all":contrast(
                "selected_assurance_only","neutral_all"),
            "other_two_over_neutral_all":contrast(
                "selected_nonassurance_only","neutral_all"),
            "whole_selected_over_neutral_all":contrast(
                "selected_all","neutral_all"),
            "assurance_over_selected_other":contrast(
                "selected_all","selected_nonassurance_only"),
        }
        means={arm:float(np.mean([
            d["future_occupancy"][f"{arm}|K{k}"]
            for row in eligible for d in row["draws"]
        ])) for arm in ARMS}
        assurance=.5*(means["selected_assurance_only"]-means["neutral_all"]
                       +means["selected_all"]-means["selected_nonassurance_only"])
        other=.5*(means["selected_nonassurance_only"]-means["neutral_all"]
                   +means["selected_all"]-means["selected_assurance_only"])
        if not np.isclose(
            assurance+other,means["selected_all"]-means["neutral_all"],
            atol=1e-12,rtol=0,
        ):
            raise AssertionError("two-order locus effects do not reconstruct total")
        out.append({
            "K":k,
            "eligible_old_donor_history_units":len(eligible),
            "new_post20_visitor_innovations_on_eligible_donors":len(eligible),
            "genome_draws_nested_per_source":DRAWS,
            "n_future_trajectories_in_K":len(eligible)*DRAWS*len(ARMS),
            "occupied_proportions_all_150_nested_genomes":means,
            "effect_comparisons":effects,
            "two_order_locus_allocation_descriptive_only":{
                "assurance":assurance,"other_loci":other,
                "full_three_locus":means["selected_all"]-means["neutral_all"],
                "not_a_physical_mediation_share":True,
            },
        })
    return out


def run_all():
    design,digest=contract()
    source,_=original_contract()
    all_rows=[]
    for seed in SOURCE_HISTORIES:
        original_ecology=visitor_history(source,seed)
        donors={
            "selected_pre20":replay_original_t20(
                source,original_ecology,seed,"selected_source"),
            "neutral_pre20":replay_original_t20(
                source,original_ecology,seed,"neutral_within_mating_channel"),
        }
        eligible=all(len(st.ids)>0 for st in donors.values())
        future_seed=mapped_new_future_seed(seed)
        fresh=new_future_history(source,original_ecology,future_seed)
        item={
            "old_source_seed":seed,"new_future_seed":future_seed,
            "original_selected_t20_alive":int(bool(len(donors["selected_pre20"].ids))),
            "original_neutral_t20_alive":int(bool(len(donors["neutral_pre20"].ids))),
            "eligible":eligible,
            "reason_not_eligible":None if eligible else "one_or_both_original_source_donors_extinct_by_t20",
            "post20_initial_visitor_count":len(original_ecology.visitors[20].ids),
            "new_post20_visitors_first_20_counts":[len(v.ids) for v in fresh.visitors[20:40]],
            "draws":[],
        }
        if eligible:
            for draw in range(DRAWS):
                n,ni=sample_eight_individuals(
                    donors["neutral_pre20"],source_history_seed=seed,
                    donor_label="neutral_pre20",draw=draw)
                s,si=sample_eight_individuals(
                    donors["selected_pre20"],source_history_seed=seed,
                    donor_label="selected_pre20",draw=draw)
                genomes=genotypes_by_module(n,s)
                record={
                    "draw_index":draw,
                    "selected_source_indices":si,
                    "neutral_source_indices":ni,
                    "genotype_means_at_t20":{
                        name:z.alleles.mean(axis=(0,2)).tolist()
                        for name,z in genomes.items()
                    },
                    "future_occupancy":{},
                }
                for K in CAPS:
                    for name,z in genomes.items():
                        result=run_future(
                            source,fresh,future_seed,z,K,"selected_source")
                        record["future_occupancy"][f"{name}|K{K}"]=result["occupied80"]
                item["draws"].append(record)
        all_rows.append(item)
    counts={
        "selected_alive":sum(r["original_selected_t20_alive"] for r in all_rows),
        "neutral_alive":sum(r["original_neutral_t20_alive"] for r in all_rows),
        "both_alive":sum(r["eligible"] for r in all_rows),
    }
    if counts!=EXPECTED_SOURCE_COUNTS:
        raise AssertionError("archived original selected/neutral source t20 counts changed")
    nfutures=sum(len(r["draws"])*len(ARMS)*len(CAPS) for r in all_rows)
    if nfutures!=1200 or len(all_rows)!=64:
        raise AssertionError("new future-transfer factorial incomplete")
    return {
        "status":STATUS,
        "contract_sha256":digest,
        "old_source_histories_total":64,
        "original_t20_source_counts":counts,
        "conditional_eligible_old_donor_histories":50,
        "new_post20_visitor_seed_count":64,
        "new_future_visitor_histories_used_with_both_donors":50,
        "n_whole_genome_draws_per_donor":DRAWS,
        "total_future_trajectories":nfutures,
        "model_independent_natural_island_systems":0,
        "source_conditioned_new_future":True,
        "results":summarise(all_rows),
        "all_histories_and_nested_future_occupancy":all_rows,
        "scientific_limits":[
            "This is a fresh post-t20 visitor transition cohort conditional on previously exposed source donor histories and their visitor state at t20, NOT a fresh original donor history or independent island ecological system.",
            "Three repeated whole-genotype draws per source history are NESTED, not 150 independent ecological history replicates.",
            "The group genetic-state mosaics mix two source genealogies and cannot be interpreted as one naturally evolved diploid multilocus genotype.",
            "Mean and variance effects within a locus are not separated; fixed depression/no mutation excludes deleterious-load meltdown and purging.",
            "All comparisons are conditioned on both original t20 source arms surviving 50/64; no unconditional from-t0 population survival inference.",
            "Neither selected source inheritance nor the mean expression clamp is a full genetic evolution freeze; no evolutionary suicide inference.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    res=run_all()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(res,indent=2,sort_keys=True,allow_nan=False)+"\n",
                     encoding="utf-8")
    print(json.dumps({
        "status":res["status"],"original_t20_counts":res["original_t20_source_counts"],
        "full_futures":res["total_future_trajectories"],
        "summary":res["results"],
    },sort_keys=True))


if __name__=="__main__":
    main()
