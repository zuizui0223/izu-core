"""Exposed Model3 t20 source: assurance locus vs other two loci genotype mosaic.

Post-outcome **mechanism engineering**, NO newly independent visitor history.
Original source selected/neutral t20 genomic donors and whole-diploid
resampling are reused exactly; a hybrid replacement copies ALL homologs,
allele origins and mutation flags of a given locus jointly.

Cross-locus mosaics combine counterfactual parental genealogies and need not
occur as a natural lineage. Contrast probabilities are conditional on paired
source-t20 survival, not evolutionary suicide or an ecological field test.
"""
from __future__ import annotations
from dataclasses import replace
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_t20_joint_genome_transplant import (
    DONORS,K_TARGET,SOURCE_HISTORIES,EXPECTED_SOURCE_COUNTS,
    original_contract,replay_original_t20,transplant_diploid_source,
    run_future,visitor_history
)
from scripts.audit_chapter2_gamma_persist_exact_pair_sensitivity import (
    paired_exact_interval, classify,
)
from scripts.model3_island.types import PlantState

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_t20_assurance_locus_hybrid_replay_20261010.json"
ARMS=("neutral_all","selected_assurance_only","selected_nonassurance_only","selected_all")
STATUS="POST_OUTCOME_T20_ASSURANCE_VS_OTHER_LOCI_SOURCE_GENOME_MOSAIC"


def contract():
    blob=DESIGN.read_bytes()
    d=json.loads(blob)
    if (d["status"]!="POST_OUTCOME_COMPONENT_DIAGNOSTIC_LOCKED_AFTER_WHOLE_GENOME_RESULT"
            or d["source_full_artifact_sha256"]!="1c15f1921817f573662615343623e3890c5dce99413484fdd41bb4c07ab52eaf"
            or d["hybrid_genotype_arms"]!=list(ARMS)
            or d["future"]["recipient_K"]!=[8,48]
            or d["future"]["N0"]!=8 or d["future"]["B"]!=48
            or d["future"]["all_eligible_source_futures"]!=400
            or d["whole_genome_source_draw"]["donor_rng_salt"]!=61025971
            or d["future"]["future_demographic_rng_salt"]!=61025972
            or d["replay_source_pre20"]["n_both_eligible"]!=50):
        raise ValueError("unexpected source-locked hybrid locus protocol")
    return d,hashlib.sha256(blob).hexdigest()


def genotypes_by_module(neutral,selected):
    """Copy both diploid homologs and ancestry/flags per locus, never averages."""
    if (not isinstance(neutral,PlantState) or not isinstance(selected,PlantState)
            or len(neutral.ids)!=8 or len(selected.ids)!=8
            or not np.array_equal(neutral.ids,selected.ids)
            or not np.array_equal(neutral.birth_years,selected.birth_years)):
        raise ValueError("source donor transplant fields do not align")
    def hybrid(assurance_from_selected):
        a=neutral.alleles.copy()
        origin=neutral.allele_origin.copy()
        flags=neutral.mutation_flags.copy()
        loci=(2,) if assurance_from_selected else (0,1)
        for j in loci:
            a[:,j,:]=selected.alleles[:,j,:]
            origin[:,j,:]=selected.allele_origin[:,j,:]
            flags[:,j,:]=selected.mutation_flags[:,j,:]
        return replace(neutral,alleles=a,allele_origin=origin,
                       mutation_flags=flags)
    results={
        "neutral_all":neutral,
        "selected_assurance_only":hybrid(True),
        "selected_nonassurance_only":hybrid(False),
        "selected_all":selected,
    }
    for key,genome in results.items():
        for j in range(3):
            selected_expected=(key=="selected_all"
                or key=="selected_assurance_only" and j==2
                or key=="selected_nonassurance_only" and j!=2)
            source=selected if selected_expected else neutral
            for name in ("alleles","allele_origin","mutation_flags"):
                if not np.array_equal(getattr(genome,name)[:,j,:],
                                      getattr(source,name)[:,j,:]):
                    raise AssertionError("hybrid source locus improperly reassigned")
    return results


def _paired_contrast(rows,K,positive,negative):
    a=np.array([r["futures"][f"{positive}|K{K}"]["occupied80"] for r in rows],
               dtype=np.int64)
    b=np.array([r["futures"][f"{negative}|K{K}"]["occupied80"] for r in rows],
               dtype=np.int64)
    n=len(rows)
    pos=int(np.sum((a==1)&(b==0)))
    neg=int(np.sum((a==0)&(b==1)))
    ci=paired_exact_interval(pos,neg,n)
    return {
        "K":K,"positive":positive,"negative":negative,
        "n_conditional_source_histories":n,
        "n_positive_occupied":int(a.sum()),
        "n_negative_occupied":int(b.sum()),
        "paired_positive_only":pos,"paired_negative_only":neg,
        "delta":(pos-neg)/n,"single_comparison_conservative95":ci,
        "single_contrast_ROPE_verdict":classify(ci),
        "post_outcome_secondary":True,
    }


def analyze(rows):
    eligible=[x for x in rows if x["eligible"]]
    if len(eligible)!=50:
        raise AssertionError("source BOTH-survivor eligibility unexpectedly changed")
    summaries=[]
    contrasts=[]
    for K in K_TARGET:
        counts={name:sum(
            r["futures"][f"{name}|K{K}"]["occupied80"] for r in eligible)
            for name in ARMS}
        summaries.append({"K":K,"n_eligible":50,
                          "occupied_by_genome_module":counts})
        c={}
        for label,p,n in [
            ("assurance_neutral_other","selected_assurance_only","neutral_all"),
            ("assurance_selected_other","selected_all","selected_nonassurance_only"),
            ("other_neutral_assurance","selected_nonassurance_only","neutral_all"),
            ("other_selected_assurance","selected_all","selected_assurance_only"),
            ("full_selected_minus_neutral","selected_all","neutral_all"),
        ]:
            val=_paired_contrast(eligible,K,p,n)
            c[label]=val["delta"]
            contrasts.append({"contrast":label,**val})
        assurance_effect=.5*(c["assurance_neutral_other"]+
                             c["assurance_selected_other"])
        other_effect=.5*(c["other_neutral_assurance"]+
                         c["other_selected_assurance"])
        interaction=(counts["selected_all"]
                     -counts["selected_assurance_only"]
                     -counts["selected_nonassurance_only"]
                     +counts["neutral_all"])/50
        if not np.isclose(assurance_effect+other_effect,
                          c["full_selected_minus_neutral"],atol=1e-12,rtol=0):
            raise AssertionError("Shapley two-order allocation does not sum")
        summaries[-1]["descriptive_two_order_decomposition"]={
            "assurance_locus_shapley_style":assurance_effect,
            "other_two_loci_shapley_style":other_effect,
            "full_source_genomic_effect":c["full_selected_minus_neutral"],
            "four_genotype_cell_interaction":interaction,
            "interaction_already_allocated_in_two_order_averages":True,
            "not_a_unique_causal_mediation_share":True,
        }
    return summaries,contrasts


def run_all():
    d,digest=contract()
    original,_=original_contract()
    raw=[]
    for seed in SOURCE_HISTORIES:
        hist=visitor_history(original,seed)
        source={
            "selected_pre20":replay_original_t20(original,hist,seed,"selected_source"),
            "neutral_pre20":replay_original_t20(
                original,hist,seed,"neutral_within_mating_channel")
        }
        eligible=all(len(s.ids)>0 for s in source.values())
        item={
            "history_seed":seed,"eligible":eligible,
            "original_selected_alive_t20":int(bool(len(source["selected_pre20"].ids))),
            "original_neutral_alive_t20":int(bool(len(source["neutral_pre20"].ids))),
            "excluded_reason":None if eligible else "source_donor_extinct_by_t20",
            "source_donor_mean_genotypes":{
                label:(s.alleles.mean(axis=(0,2)).tolist() if len(s.ids) else None)
                for label,s in source.items()
            },
            "genome_t20_module_mean":{},
            "futures":{},
        }
        if eligible:
            n,_=transplant_diploid_source(
                source["neutral_pre20"],seed=seed,donor_label="neutral_pre20")
            s,_=transplant_diploid_source(
                source["selected_pre20"],seed=seed,donor_label="selected_pre20")
            z=genotypes_by_module(n,s)
            for name,source_genome in z.items():
                item["genome_t20_module_mean"][name]=source_genome.alleles.mean(axis=(0,2)).tolist()
                for K in K_TARGET:
                    item["futures"][f"{name}|K{K}"]=run_future(
                        original,hist,seed,source_genome,K,"selected_source")
        raw.append(item)
    counts={
        "selected_alive":sum(x["original_selected_alive_t20"] for x in raw),
        "neutral_alive":sum(x["original_neutral_alive_t20"] for x in raw),
        "both_alive":sum(x["eligible"] for x in raw),
    }
    if counts!=EXPECTED_SOURCE_COUNTS:
        raise AssertionError("original source t20 survivor history changed")
    if sum(len(x["futures"]) for x in raw)!=400:
        raise AssertionError("complete whole-locus hybrid 50x4x2 missing")
    summaries,contrasts=analyze(raw)
    assert summaries[0]["occupied_by_genome_module"]["neutral_all"]==15
    assert summaries[0]["occupied_by_genome_module"]["selected_all"]==36
    assert summaries[1]["occupied_by_genome_module"]["neutral_all"]==41
    assert summaries[1]["occupied_by_genome_module"]["selected_all"]==49
    return {
        "status":STATUS,
        "design_sha256":digest,
        "source_original_full_genomic_replay_sha256":d["source_full_artifact_sha256"],
        "history_count_exposed":64,
        "both_t20_source_populations_alive":50,
        "not_eligible_count":14,
        "original_counts":counts,
        "post20_hybrid_futures":400,
        "genotype_module_summary":summaries,
        "ten_secondary_paired_contrasts":contrasts,
        "all_64_original_histories_and_conditional_futures":raw,
        "limitations":[
            "Artificial cross-source locus mosaics are not observed natural pedigrees and may alter across-locus associations; no donor locus was mutated.",
            "The conditional hybrid factor intervention is run only among both-alive original t20 sources, 50/64.",
            "This uses already exposed original visitor RNG histories, so it is a post-outcome mechanistic exercise, not a new confirmatory experiment.",
            "The two-order Shapley-style allocation distributes interaction but cannot uniquely assign ecological or genetic mediation fractions.",
            "All original source genome parentage and prospective experiment results remain archived unchanged.",
        ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    d=run_all()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(d,indent=2,sort_keys=True,allow_nan=False)+"\n",
                     encoding="utf-8")
    print(json.dumps({
        "status":d["status"],"source_counts":d["original_counts"],
        "n_futures":d["post20_hybrid_futures"],
        "summary":d["genotype_module_summary"],
        "contrasts":d["ten_secondary_paired_contrasts"],
    },sort_keys=True))


if __name__=="__main__":
    main()
