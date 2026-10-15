"""Independent 64-history aggregation of exact old-source far t0→t200 replay.

Requires all 512 original single-repeat historical paths with complete
SHA-verified native genome/parentage arrays. Nothing here estimates a natural
causal mediator or runs a new independent ecological history.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

import numpy as np

from scripts.replay_chapter2_far_original_0_200_20261015 import (
    PROTOCOL, source_protocol,
)
from scripts.summarize_chapter2_far_t200_history_swap_20261015 import bootstrap_history

TIMEPOINTS = (0, 10, 20, 50, 100, 150, 200)
TERMS = ("weighted_parental_Price_I", "survivor_sampling_I",
         "recruit_transmission_residual_I")


def validate_case(folder, record):
    key = record["key"]
    file = folder/(key+".npz")
    receipt = folder/(key+".json")
    if not file.is_file() or not receipt.is_file():
        raise AssertionError("source replay output missing "+key)
    if (hashlib.sha256(file.read_bytes()).hexdigest()!=record["npz_sha256"]
        or json.loads(receipt.read_text(encoding="utf-8"))!=record
        or record["source_contract_sha256"]!=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
        or record["original_replayed_updates"]!=200
        or record["source_original_t200_exact_allele_parity"] is not True):
        raise AssertionError("original replay source/receipt SHA gate "+key)
    with np.load(file,allow_pickle=False) as a:
        n=a["N"];aI=a["mean_I"];d=a["realized_delta_I"]
        price=a["weighted_parental_Price_I"]
        surv=a["survivor_sampling_I"]
        resid=a["recruit_transmission_residual_I"]
        geno=a["alleles"]
        ids=a["ids"];parents=a["parentage"]
        if (len(n)!=201 or len(aI)!=201 or len(d)!=200
            or geno.shape[0]!=201 or geno.shape[2:]!=(3,2)
            or ids.shape!=geno.shape[:2]
            or parents.shape!=(200,geno.shape[1],3)
            or not np.array_equal((ids>=0).sum(axis=1),n)
            or np.any(n<=0)
            or not np.allclose(np.nanmean(geno[:,:,1,:],axis=(1,2)),aI,atol=1e-12,rtol=0)
            or not np.allclose(d,np.diff(aI),atol=1e-12,rtol=0)
            or not np.allclose(d,price+surv+resid,atol=1e-12,rtol=0)
            or abs(record["t200_I"]-float(aI[-1]))>1e-12
            or abs(record["total_realized_I_delta"]-float(d.sum()))>1e-12):
            raise AssertionError("annual exact source replay accounting "+key)
        sums={term:float(a[term].sum()) for term in TERMS}
        if abs(sum(sums.values())-float(d.sum()))>1e-12:
            raise AssertionError("non-telescoping I decomposition "+key)
        return {"timepoints":{t:float(aI[t]) for t in TIMEPOINTS},
                "components":sums, "final_N":int(n[-1]),
                "visitor_free_years":int(np.count_nonzero(a["n_visitors"]==0)),
                "annual_exact":True}


def aggregate(root):
    p,_,_=source_protocol()
    manifests=sorted(root.glob("*/readout.json"))
    if len(manifests)!=4:raise AssertionError("exact four provenance shards required")
    case_map={}
    data={}
    for manifest in manifests:
        d=json.loads(manifest.read_text(encoding="utf-8"))
        shard=d["shard_index"]
        expected=[s for s in range(26110601,26110665)
                  if (s-26110601)%4==shard]
        if (d["status"]!="EXACT_ORIGINAL_T0_T200_SOURCE_REPLAY_SHARD"
            or d["shard_count"]!=4 or d["history_seeds"]!=expected
            or d["n_cases"]!=128
            or d["total_original_replayed_updates"]!=25600
            or d["new_independent_histories"]!=0
            or d["original_source_t200_complete_genotype_parity"] is not True):
            raise AssertionError("source replay shard inclusion/provenance")
        for rec in d["cases"]:
            k=(rec["setting"],rec["history_seed"],rec["mode"])
            if k in case_map:raise AssertionError("duplicate source case")
            case_map[k]=rec
            data[k]=validate_case(manifest.parent,rec)
    expected={(setting,s,mode) for setting in p["settings"]
              for s in range(26110601,26110665)
              for mode in ("fixed","evolving")}
    if set(case_map)!=expected or len(case_map)!=512:
        raise AssertionError("missing source experimental unit")
    sections={}
    for setting_idx,setting in enumerate(p["settings"]):
        histories=[]
        for h in range(26110601,26110665):
            f=data[setting,h,"fixed"];e=data[setting,h,"evolving"]
            orig_f=case_map[setting,h,"fixed"]
            orig_e=case_map[setting,h,"evolving"]
            if (abs(f["timepoints"][0]-e["timepoints"][0])>1e-12
                or orig_f["original_repeat"]!=orig_e["original_repeat"]
                or orig_f["original_repeat"]!=26111601
                or f["final_N"]<=0 or e["final_N"]<=0
                or f["visitor_free_years"]!=e["visitor_free_years"]):
                raise AssertionError("source E/F original path pairing incorrect")
            diffs={t:e["timepoints"][t]-f["timepoints"][t] for t in TIMEPOINTS}
            parts={term:e["components"][term]-f["components"][term] for term in TERMS}
            if abs(sum(parts.values())-diffs[200])>1e-12:
                raise AssertionError("original source Price/residual totals incorrect")
            histories.append({"history":h,"I_level_EminusF":diffs,
                              "I_delta_EminusF_terms":parts,
                              "visitor_free_years":f["visitor_free_years"]})
        time={
            str(t):bootstrap_history([r["I_level_EminusF"][t] for r in histories],
                                      20261015+setting_idx*100+t)
            for t in TIMEPOINTS}
        components={
            term:bootstrap_history([r["I_delta_EminusF_terms"][term] for r in histories],
                                   20261015+setting_idx*100+500+k)
            for k,term in enumerate(TERMS)}
        if abs(sum(components[t]["mean"] for t in TERMS)-time["200"]["mean"])>1e-12:
            raise AssertionError("mean original E-F I difference does not decompose")
        sections[setting]={"timepoints":time,"component_sums":components,
                           "positive_t200_histories":time["200"]["positive"],
                           "negative_t200_histories":time["200"]["negative"],
                           "zero_visitor_years_min":min(x["visitor_free_years"] for x in histories),
                           "zero_visitor_years_max":max(x["visitor_free_years"] for x in histories)}
    return {
        "status":"EXACT_ORIGINAL_FIRST_200_SOURCE_REPLAY_ACCOUNTED",
        "source_original_run_id":p["original_workflow_run"],
        "original_single_demographic_repeat":26111601,
        "original_visitor_history_clusters":64,
        "original_replayed_case_paths":512,
        "original_replayed_updates":102400,
        "source_t200_bit_exact_admission":True,
        "annual_genome_parentage_sha_rechecked":True,
        "new_independent_visitor_histories":0,
        "model_interpretation":"Price/survivor/residual is exact pathwise bookkeeping, not cause-specific selection-vs-drift mediation",
        "settings":sections,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    if args.out.exists():raise FileExistsError("no overwrites of source-original audit")
    result=aggregate(args.input)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    tmp=args.out.with_suffix(".tmp")
    tmp.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    os.replace(tmp,args.out)
    print(json.dumps({"status":result["status"],"cases":512,"original_updates":102400,
                      "genomic_parity_all":True},indent=2))


if __name__=="__main__":
    main()
