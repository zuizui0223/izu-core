"""Exact original-source far t0→t200 diploid Price and parentage replay.

This re-executes *the already run* original frozen histories and RNG streams,
requires bit-for-bit match to original archived t200 genotypes, and decomposes
each realized I change into a survival term, a conditional expected Mendelian
parental Price term and a residual (birth lottery, Mendelian sampling/mutation).
NO new biological history, priority claim or selection/drift mediation fraction.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import numpy as np

from scripts.audit_chapter2_original_evolved_pollen_service import (
    original_shards, read_design, parity, state_from_archive,
)
from scripts.chapter2_far_t200_history_swap_20261015 import conditional_price
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream, STREAM_IDS
from scripts.model3_island.reproduction import reproduce
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config, founders, load_design,
)
from scripts.run_model3_persistent_isolation import exposure

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT/"docs/protocols/chapter2_far_original_0_200_accounting_20261015.json"
START, END = 0, 200
MODES = ("fixed","evolving")
FIELDS = ("alleles","allele_origin","mutation_flags","ids","birth_years")


def digest(b:bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def source_protocol():
    p=json.loads(PROTOCOL.read_text(encoding="utf-8"))
    src=read_design()
    d=load_design(DEFAULT_DESIGN)
    if not (p["status"]=="POST_OUTCOME_SOURCE_RECONSTRUCTION_NOT_NEW_ECOLOGICAL_CONFIRMATION"
            and p["source_horizon_begin"]==START
            and p["source_horizon_end"]==END
            and p["expected_source_case_replays"]==512
            and p["expected_original_source_updates"]==102400
            and p["settings"]==src["settings"]
            and p["original_source_shards"]==
               [r["artifact_id"] for r in src["artifact_shards"]]
            and p["original_workflow_run"]==src["original_workflow_run_id"]
            and p["original_demographic_seed"]==src["demographic_repeat_seed"]
            and set(p["modes"])==set(MODES)
            and p["arm"]=="far"):
        raise AssertionError("source reconstruction protocol mismatch")
    return p,src,d


def original_streams(visit_seed, demographic_repeat=26111601):
    master=int(np.random.SeedSequence(
        [visit_seed,demographic_repeat]
    ).generate_state(1)[0])
    return {name:stream(master,name,0) for name in STREAM_IDS}


def annual_source_replay(design, setting, history_seed, mode, reference=None):
    cfg=config(design, setting, .01, mode)
    history=exposure(history_seed,"far")
    state=founders(design)
    streams=original_streams(history_seed)
    cap=cfg.capacity
    size=END+1
    a=np.full((size,cap,3,2),np.nan,dtype=float)
    origin=np.full((size,cap,3,2),-1,dtype=np.int64)
    mflags=np.zeros((size,cap,3,2),dtype=bool)
    ids=np.full((size,cap),-1,dtype=np.int64)
    born=np.full((size,cap),-1,dtype=np.int64)
    parents=np.full((END,cap,3),-1,dtype=np.int64)
    meanI=np.full(size,np.nan)
    meanA=np.full(size,np.nan)
    varI=np.full(size,np.nan)
    minI=np.full(size,np.nan)
    uniqueI=np.zeros(size,dtype=np.int64)
    N=np.zeros(size,dtype=np.int64)
    visitor_count=np.zeros(END,dtype=np.int64)
    expected_price=np.full(END,np.nan)
    realized_delta=np.full(END,np.nan)
    weighted_price=np.zeros(END)
    survivor_sampling=np.zeros(END)
    recruit_transmission_residual=np.zeros(END)
    survivors=np.zeros(END,dtype=np.int64)
    recruited=np.zeros(END,dtype=np.int64)
    self_recruited=np.zeros(END,dtype=np.int64)
    outcross_recruited=np.zeros(END,dtype=np.int64)
    F=np.zeros(END);P=np.zeros(END);S=np.zeros(END)

    for t in range(END+1):
        n=len(state.ids)
        if n<=0 or n>cap or len(np.unique(state.ids))!=n:
            raise AssertionError("original occupied source has wrong population")
        a[t,:n]=state.alleles
        origin[t,:n]=state.allele_origin
        mflags[t,:n]=state.mutation_flags
        ids[t,:n]=state.ids
        born[t,:n]=state.birth_years
        I=state.alleles[:,1,:].mean(axis=1)
        meanI[t]=I.mean()
        meanA[t]=state.alleles[:,2,:].mean() if mode=="evolving" else cfg.fixed_assurance
        varI[t]=I.var()
        minI[t]=state.alleles[:,1,:].min()
        uniqueI[t]=len(np.unique(state.alleles[:,1,:]))
        N[t]=n
        if mode=="fixed" and np.any(state.alleles[:,2,:]!=cfg.fixed_assurance):
            raise AssertionError("original fixed-A latent locus has mutated")
        if t==END:
            break
        v=history.visitors[t]
        visitor_count[t]=len(v.ids)
        led=reproduce(state,v,cfg)
        expected_price[t]=conditional_price(state,led)
        F[t]=led.outcross.sum(axis=0).sum()
        P[t]=led.outcross.sum(axis=1).sum()
        S[t]=led.self_viable.sum()
        if abs(F[t]-P[t])>1e-10:
            raise AssertionError("sex-specific original pollen weights not conserved")
        later,info=advance(
            state,led,history.seed_candidates[t],cfg,streams,year=t,
            mutation_traits=(True,True,mode=="evolving"),
        )
        if (info["immigrant_recruits"] or info["immigrant_settled"]
                or info["resident_recruits"]+info["survivors"]!=len(later.ids)):
            raise AssertionError("source historical no-immigration accounting failed")
        survivors[t]=info["survivors"]
        recruited[t]=info["resident_recruits"]
        self_recruited[t]=info["resident_selfed_recruits"]
        outcross_recruited[t]=info["resident_outcross_recruits"]
        edge=info["parentage"]
        if len(edge)!=recruited[t] or len(edge)>cap:
            raise AssertionError("parentage malformed")
        parents[t,:len(edge)]=edge
        retained_mask=np.isin(later.ids,state.ids)
        child_mask=np.isin(later.ids,edge[:,0])
        if (int(retained_mask.sum())!=survivors[t]
                or int(child_mask.sum())!=recruited[t]
                or not np.all(retained_mask^child_mask)):
            raise AssertionError("offspring/survivor assignment inconsistent")
        I_next=float(later.alleles[:,1,:].mean())
        I_s=float(later.alleles[retained_mask,1,:].mean()) if survivors[t] else 0.
        I_c=float(later.alleles[child_mask,1,:].mean()) if recruited[t] else 0.
        w_s=survivors[t]/len(later.ids);w_c=recruited[t]/len(later.ids)
        survivor_sampling[t]=w_s*(I_s-meanI[t]) if survivors[t] else 0.
        weighted_price[t]=w_c*expected_price[t] if recruited[t] else 0.
        recruit_transmission_residual[t]=(
            w_c*(I_c-meanI[t]-expected_price[t]) if recruited[t] else 0.
        )
        realized_delta[t]=I_next-meanI[t]
        if abs(realized_delta[t]-(
            survivor_sampling[t]+weighted_price[t]+
            recruit_transmission_residual[t]
        ))>1e-12:
            raise AssertionError("exact source annual genetic bookkeeping failed")
        state=later
    if reference is not None and not np.array_equal(state.alleles,reference.alleles):
        raise AssertionError("EXACT frozen original t200 diploid allele parity failed")
    if abs(np.sum(realized_delta)-(meanI[-1]-meanI[0]))>1e-12:
        raise AssertionError("annual accounting does not telescope")
    if mode=="fixed" and not np.all(meanA==cfg.fixed_assurance):
        raise AssertionError("A-fixed genetics changed")
    return {
        "alleles":a, "allele_origin":origin, "mutation_flags":mflags,
        "ids":ids,"birth_years":born,"parentage":parents,
        "mean_I":meanI,"mean_A_expressed":meanA,"var_I":varI,
        "min_I_allele":minI,"n_unique_I_alleles":uniqueI,
        "N":N, "n_visitors":visitor_count,
        "expected_Price_shift_I":expected_price,
        "realized_delta_I":realized_delta,
        "weighted_parental_Price_I":weighted_price,
        "survivor_sampling_I":survivor_sampling,
        "recruit_transmission_residual_I":recruit_transmission_residual,
        "n_survivors":survivors,"n_resident_recruits":recruited,
        "n_selfed_recruits":self_recruited,
        "n_outcross_recruits":outcross_recruited,
        "F_outcross":F,"P_outcross":P,"S_viable_selfing":S,
    }


def write_case(source_archives,src,design,p,setting,seed,mode,out):
    key=f"original0_200_{setting}_h{seed}_{mode}"
    destination=out/(key+".npz");receipt_path=out/(key+".json")
    if destination.exists() or receipt_path.exists():
        raise FileExistsError("source original source replay output already exists")
    index=2 if mode=="fixed" else 3
    ref=state_from_archive(
        source_archives[index],index,setting,seed,"far",mode,END
    )
    result=annual_source_replay(design,setting,seed,mode,reference=ref)
    temp=destination.with_suffix(".npz.tmp")
    with temp.open("wb") as fh:
        np.savez_compressed(fh,**result)
    os.replace(temp,destination)
    record={
        "key":key,"setting":setting,"history_seed":seed,
        "mode":mode,"original_repeat":p["original_demographic_seed"],
        "source_original_t200_exact_allele_parity":True,
        "source_contract_sha256":digest(PROTOCOL.read_bytes()),
        "npz_sha256":digest(destination.read_bytes()),
        "original_t200_alleles_sha256":digest(ref.alleles.tobytes()),
        "original_replayed_updates":END,
        "n_at200":int(result["N"][-1]),
        "t0_I":float(result["mean_I"][0]),
        "t200_I":float(result["mean_I"][-1]),
        "total_realized_I_delta":float(result["realized_delta_I"].sum()),
        "weighted_Price_I_sum":float(result["weighted_parental_Price_I"].sum()),
        "survivor_I_sum":float(result["survivor_sampling_I"].sum()),
        "recruit_transmission_residual_I_sum":float(
            result["recruit_transmission_residual_I"].sum()),
        "no_new_independent_ecological_histories":True,
    }
    if abs(record["total_realized_I_delta"]-
          (record["weighted_Price_I_sum"]+record["survivor_I_sum"]+
           record["recruit_transmission_residual_I_sum"]))>1e-12:
        raise AssertionError("sum decomposition changed source trait")
    temp=receipt_path.with_suffix(".json.tmp")
    temp.write_text(json.dumps(record,indent=2,allow_nan=False)+"\n",
                    encoding="utf-8")
    os.replace(temp,receipt_path)
    return record


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--shards",type=Path,nargs=4)
    ap.add_argument("--out",type=Path)
    ap.add_argument("--shard-index",type=int,default=0)
    ap.add_argument("--shard-count",type=int,default=4)
    ap.add_argument("--dry-run",action="store_true")
    args=ap.parse_args()
    p,src,design=source_protocol()
    if (args.shard_count!=4 or not 0<=args.shard_index<4):
        ap.error("freeze exactly four non-overlapping source-history shards")
    seeds=[s for s in range(p["history_seed_first"],
                             p["history_seed_last"]+1)
           if (s-p["history_seed_first"])%4==args.shard_index]
    if args.dry_run:
        print(json.dumps({"source_cases":len(seeds)*len(p["settings"])*2,
                          "original_updates":len(seeds)*len(p["settings"])*2*200,
                          "history_seeds":seeds,"new_ecological_histories":0},
                         indent=2))
        return
    if args.shards is None or args.out is None:
        ap.error("--shards original0.zip original1.zip original2.zip original3.zip --out DIR required")
    if args.out.exists() and list(args.out.iterdir()):
        raise FileExistsError("source replay output must be empty and immutable")
    args.out.mkdir(parents=True,exist_ok=True)
    original=original_shards(args.shards,src)
    parity()
    cases=[]
    for setting in p["settings"]:
        for seed in seeds:
            for mode in MODES:
                cases.append(write_case(original,src,design,p,
                                        setting,seed,mode,args.out))
        print("original exact t200 parity complete for",setting,flush=True)
    if len(cases)!=128 or not all(x["source_original_t200_exact_allele_parity"] for x in cases):
        raise AssertionError("original 128 source replays incomplete")
    d={
        "status":"EXACT_ORIGINAL_T0_T200_SOURCE_REPLAY_SHARD",
        "shard_index":args.shard_index,"shard_count":4,
        "history_seeds":seeds,"n_cases":len(cases),
        "total_original_replayed_updates":len(cases)*200,
        "original_source_shards_sha_validated":True,
        "original_source_t200_complete_genotype_parity":True,
        "new_independent_histories":0,"cases":cases,
        "interpretation":"post-outcome source historical accounting, not drift/selection mediation",
    }
    out=args.out/"readout.json"
    if out.exists():raise FileExistsError("source readout exists")
    out.write_text(json.dumps(d,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({"cases":len(cases),"source_updates":len(cases)*200,
                      "all_original_t200_genomes_exact":True},indent=2))


if __name__=="__main__":
    main()
