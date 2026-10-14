"""Fresh t0 donor histories + independent post-t20 ecologies: assurance module test.

All source visitor histories 61028001..61028192 and independent future visitor
transition histories 61029001..61029192 are fresh. Source genotypes share a
single frozen eight-plant standing-variation fixture intentionally. Both
original source parentage modes must survive t20 for donor eligibility.
Two whole-diploid genome draws per source history are NESTED, not new donors.

This is a prospectively frozen *within-one-Model3* replication following
previously observed genomic effects; locus mosaics and survivor conditioning
do NOT identify natural genetic mediation or evolutionary suicide.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path
import numpy as np

from scripts.audit_chapter2_t20_joint_genome_transplant import (
    original_contract,replay_original_t20,run_future,visitor_history
)
from scripts.audit_chapter2_selected_vs_neutral_parentage_new64 import biological_config
from scripts.audit_chapter2_t20_assurance_locus_hybrid import ARMS,genotypes_by_module
from scripts.model3_island.history import make_history
from scripts.model3_island.types import History,PlantState

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_assurance_independent_source_future_192_20261010.json"
STATUS="FRESH_SOURCE_AND_FUTURE_MODEL192_ASSURANCE_LOCI_PREOUTCOME_REPLICATION"
SOURCE_SEEDS=range(61028001,61028193)
FUTURE_SEEDS=range(61029001,61029193)
K_VALUES=(8,48)
DRAWS=2
TEST_ONLY_SOURCE_SEED=990901
TEST_ONLY_FUTURE_SEED=990902


def contract():
    blob=DESIGN.read_bytes()
    d=json.loads(blob)
    p=d["history_design"]
    q=d["inference"]
    if (d["status"]!="NEW_INDEPENDENT_MODEL_HISTORY_COHORT_SOURCE_LOCKED_BEFORE_ANY_OUTCOMES"
            or (p["source_history_seed_first"],p["source_history_seed_last"])!=(61028001,61028192)
            or (p["future_ecology_seed_first"],p["future_ecology_seed_last"])!=(61029001,61029192)
            or p["number_of_independent_source_environment_rng_histories"]!=192
            or p["source_K"]!=48 or p["source_B"]!=48
            or p["source_ovule_budget"]!=8 or p["source_selfed_viable_fraction"]!=.5
            or p["source_pre20_updates"]!=20
            or p["future_N0"]!=8 or p["future_B"]!=48
            or p["future_K"]!=[8,48]
            or p["future_ovule_budget"]!=8
            or p["whole_diploid_resamples_per_eligible_source"]!=DRAWS
            or p["genomic_compositions"]!=list(ARMS)
            or p["genome_resample_salt"]!=61029971
            or q["bootstrap_seed"]!=61029999
            or q["meaningful_absolute_survival_delta"]!=.05
            or q["stop"].find("exactly 192")<0):
        raise ValueError("new independent model-source protocol altered")
    return d,hashlib.sha256(blob).hexdigest()


def new_future_seed_from_source(old):
    if type(old) is not int or old not in SOURCE_SEEDS:
        raise ValueError("future ecological source must be newly frozen")
    return 61029001+(old-61028001)


def new_ecology_after_t20(original,old_hist,future_seed):
    if future_seed not in FUTURE_SEEDS and future_seed!=TEST_ONLY_FUTURE_SEED:
        raise ValueError("not a registered future ecology seed")
    at20=old_hist.visitors[20]
    config=replace(biological_config(original,48,8.),
                   years=60,initial_visitors=len(at20.ids))
    novel=make_history(config,seed=future_seed,inherited_visitors=at20)
    if (len(novel.visitors)!=60
            or not np.array_equal(novel.visitors[0].ids,at20.ids)
            or not np.array_equal(novel.visitors[0].optima,at20.optima)
            or any(len(x.ids)>0 for x in novel.seed_candidates)):
        raise AssertionError("fresh t20 visitor transition initialization mismatch")
    merged=History(old_hist.visitors[:20]+novel.visitors,
                   old_hist.seed_candidates[:20]+novel.seed_candidates,
                   old_hist.event_order,initialization="controlled")
    if len(merged.visitors)!=80 or len(merged.seed_candidates)!=80:
        raise AssertionError("source and fresh future ecology not 80 updates")
    return merged


def draw_genomes(donor,source_seed,donor_label,draw):
    if (len(donor.ids)==0
            or donor_label not in ("selected_pre20","neutral_pre20")
            or type(draw) is not int or draw not in range(DRAWS)
            or (source_seed not in SOURCE_SEEDS and source_seed!=TEST_ONLY_SOURCE_SEED)):
        raise ValueError("invalid fresh source-genotype draw")
    rng=np.random.default_rng(np.random.SeedSequence(
        [source_seed,61029971,
         0 if donor_label=="selected_pre20" else 1,draw]))
    index=rng.integers(0,len(donor.ids),size=8)
    g=PlantState(
        alleles=donor.alleles[index],allele_origin=donor.allele_origin[index],
        mutation_flags=donor.mutation_flags[index],
        ids=np.arange(8,dtype=np.int64),
        birth_years=np.full(8,20,dtype=np.int64),
    )
    if (not np.array_equal(g.alleles,donor.alleles[index])
            or not np.array_equal(g.allele_origin,donor.allele_origin[index])
            or not np.array_equal(g.mutation_flags,donor.mutation_flags[index])):
        raise AssertionError("whole individual homolog transfer failed")
    return g,index.tolist()


def history_cluster_intervals(values,*,bootstrap_seed):
    d=np.asarray(values,dtype=float)
    if d.ndim!=1 or len(d)<2 or (not np.isfinite(d).all()) or (abs(d)>1).any():
        return {
            "estimate":float(d.mean()) if len(d)>0 else None,
            "n_eligible_source_histories":len(d),
            "classification":"not_estimable_insufficient_eligible_sources",
            "cluster_bootstrap_95":None,
            "hoeffding_95":None,
        }
    rng=np.random.default_rng(bootstrap_seed)
    idx=rng.integers(0,len(d),size=(2999,len(d)))
    lo,hi=np.quantile(d[idx].mean(axis=1),[.025,.975])
    est=float(d.mean())
    radius=float(np.sqrt(2*np.log(2/.05)/len(d)))
    worst=[max(-1.,est-radius),min(1.,est+radius)]
    ci=[float(lo),float(hi)]
    if ci[0]>.05 and worst[0]>.05:
        verdict="resolved_positive"
    elif ci[1]<-.05 and worst[1]<-.05:
        verdict="resolved_negative"
    elif ci[0]>=-.05 and ci[1]<=.05 and worst[0]>=-.05 and worst[1]<=.05:
        verdict="practically_equivalent"
    else:
        verdict="inconclusive"
    return {
        "estimate":est,"n_eligible_source_histories":len(d),
        "n_nested_genome_draws_per_source":DRAWS,
        "cluster_bootstrap_95":ci,"hoeffding_95":worst,
        "hoeffding_radius":radius,
        "classification":verdict,
    }


def summarise(rows):
    accepted=[x for x in rows if x["eligible"]]
    primary={}
    summaries=[]
    for k in K_VALUES:
        distributions={}
        for arm in ARMS:
            v=[z["future_occupancy"][f"{arm}|K{k}"]
               for r in accepted for z in r["genome_draws"]]
            if len(v)!=len(accepted)*DRAWS:
                raise AssertionError("incomplete repeated source-genotype assignments")
            distributions[arm]={"occupied":int(sum(v)),"total":len(v),
                                "proportion":float(np.mean(v)) if v else None}
        def pair(a,b):
            x=[]
            for r in accepted:
                vals=[
                    z["future_occupancy"][f"{a}|K{k}"]
                    -z["future_occupancy"][f"{b}|K{k}"]
                    for z in r["genome_draws"]
                ]
                if len(vals)!=DRAWS:
                    raise AssertionError("missing whole-genome draws")
                x.append(float(np.mean(vals)))
            return history_cluster_intervals(x,bootstrap_seed=61029999)
        contrasts={
            "assurance_only_vs_neutral_all":pair("selected_assurance_only","neutral_all"),
            "other_loci_only_vs_neutral_all":pair("selected_nonassurance_only","neutral_all"),
            "full_selected_vs_neutral_all":pair("selected_all","neutral_all"),
            "assurance_given_selected_other":pair("selected_all","selected_nonassurance_only"),
        }
        if k==8:
            primary=contrasts["assurance_only_vs_neutral_all"]
        if accepted:
            def mean(arm):return distributions[arm]["proportion"]
            a=.5*(mean("selected_assurance_only")-mean("neutral_all")
                 +mean("selected_all")-mean("selected_nonassurance_only"))
            b=.5*(mean("selected_nonassurance_only")-mean("neutral_all")
                 +mean("selected_all")-mean("selected_assurance_only"))
            if not np.isclose(a+b,mean("selected_all")-mean("neutral_all"),
                              rtol=0,atol=1e-12):
                raise AssertionError("source two-order locus decomposition altered")
            descriptive={"assurance":a,"other_two_loci":b,
                         "whole_source_genome":a+b}
        else:descriptive=None
        summaries.append({"future_K":k,"source_history_donors_eligible":len(accepted),
                          "genome_draws_nested":DRAWS,
                          "genotype_occupancy":distributions,
                          "contrasts":contrasts,
                          "two_order_descriptive_allocation":descriptive})
    return summaries,primary


def run_all():
    frozen,hash_design=contract()
    source,_=original_contract()
    rows=[]
    for oldseed in SOURCE_SEEDS:
        original_ecology=visitor_history(source,oldseed)
        sources={
            "selected_pre20":replay_original_t20(
                source,original_ecology,oldseed,"selected_source"),
            "neutral_pre20":replay_original_t20(
                source,original_ecology,oldseed,"neutral_within_mating_channel")
        }
        eligible=all(len(s.ids)>0 for s in sources.values())
        freshseed=new_future_seed_from_source(oldseed)
        newecology=new_ecology_after_t20(source,original_ecology,freshseed)
        record={
            "source_visitor_seed":oldseed,"future_visitor_seed":freshseed,
            "selected_source_alive_t20":int(bool(len(sources["selected_pre20"].ids))),
            "neutral_source_alive_t20":int(bool(len(sources["neutral_pre20"].ids))),
            "eligible":eligible,"genome_draws":[],
            "source_assurance_means":{
                name:(float(st.alleles[:,2,:].mean()) if len(st.ids) else None)
                for name,st in sources.items()
            },
        }
        if eligible:
            for draw in range(DRAWS):
                neutral,nindex=draw_genomes(sources["neutral_pre20"],oldseed,
                                            "neutral_pre20",draw)
                selected,sindex=draw_genomes(sources["selected_pre20"],oldseed,
                                             "selected_pre20",draw)
                genomes=genotypes_by_module(neutral,selected)
                item={
                    "draw":draw,"source_selected_indices":sindex,
                    "source_neutral_indices":nindex,
                    "genome_means":{
                        name:st.alleles.mean(axis=(0,2)).tolist()
                        for name,st in genomes.items()},
                    "future_occupancy":{},
                }
                for k in K_VALUES:
                    for name,genome in genomes.items():
                        result=run_future(
                            source,newecology,freshseed,genome,k,"selected_source")
                        item["future_occupancy"][f"{name}|K{k}"]=result["occupied80"]
                record["genome_draws"].append(item)
        rows.append(record)
    if len(rows)!=192:
        raise AssertionError("missing registered source donor histories")
    accepted=sum(r["eligible"] for r in rows)
    futures=sum(len(r["genome_draws"])*len(ARMS)*len(K_VALUES) for r in rows)
    if futures!=accepted*DRAWS*len(ARMS)*len(K_VALUES):
        raise AssertionError("incomplete full eligible donor factorial")
    summary,primary=summarise(rows)
    return {
        "status":STATUS,"design_sha256":hash_design,
        "independent_new_source_visitor_RNG_histories":192,
        "independent_future_visitor_RNG_transition_histories":192,
        "independent_natural_island_systems":0,
        "same_initial_genetic_founders_across_source_histories":True,
        "eligible_both_donors_alive_t20":accepted,
        "ineligible_count":192-accepted,
        "all_future_trajectories":futures,
        "primary_K8_assurance_only_vs_neutral_all":primary,
        "complete_genome_module_results":summary,
        "all_source_histories_including_ineligible_and_nested_genotype_draws":rows,
        "claim_limits":[
            "Fresh independent visitor and demographic source history seeds and post20 independent visitor transition seeds, but same original Model3 biology and founding genotypes.",
            "Donor source eligibility still requires both selected and neutral t20 source survivors; effects conditional on this pre-transplant post-treatment event.",
            "Genome draws are nested within histories; 2 per eligible history do not double independent source sample size.",
            "Source-selected versus source-neutral inheritance affects joint 3-locus genomic distributions and costs; assurance-only mosaic is artificial.",
            "Cluster-bootstrap and distribution-free Hoeffding both must support >5pp in predeclared K8 primary to call model-internal direction resolved; failure is inconclusive.",
            "No evolutionary-suicide, mutation load, purging or natural Izu Islands interpretation is identified.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=run_all()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":result["status"],
        "n_source_histories":result["independent_new_source_visitor_RNG_histories"],
        "n_eligible":result["eligible_both_donors_alive_t20"],
        "n_futures":result["all_future_trajectories"],
        "primary":result["primary_K8_assurance_only_vs_neutral_all"],
        "summaries":result["complete_genome_module_results"]
    },sort_keys=True))


if __name__=="__main__":
    main()
