"""Shardable, receipt-verified full 1024-case Model3 ecological timing campaign.

The design/source is FROZEN before evolutionary outcomes. The runner writes
atomic per-case JSON and SHA256 receipts; an incomplete smoke run must NEVER
be represented as full biological evidence. No independent biological histories
are added: 16 synthetic visitor profiles, four nested demographic replicates.
"""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import argparse
import json
import os

from scripts.run_chapter2_sequence_abrupt_gradual_functional_loss_20261011 import (
    ROOT, DESIGN, contract, simulate
)

# Treat BOTH native biology and experimental orchestration as immutable
# scientific sources. Results from different source revisions cannot be mixed.
SOURCE_FILES=(
    "scripts/model3_island/reproduction.py",
    "scripts/model3_island/population.py",
    "scripts/model3_island/history.py",
    "scripts/model3_island/run.py",
    "scripts/model3_island/randomness.py",
    "scripts/model3_island/types.py",
    "scripts/run_model3_persistent_isolation.py",
    "scripts/run_chapter2_sequence_abrupt_gradual_functional_loss_20261011.py",
    "scripts/run_chapter2_sequence_abrupt_gradual_batch_20261011.py",
    "scripts/summarize_chapter2_sequence_abrupt_gradual_functional_loss_20261011.py",
    "scripts/audit_chapter2_sequence_tempo_focal_sign_clock_20261011.py",
    "data/design/model3_ch2_bridge_20260927.json",
    "data/design/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json",
    ".github/workflows/chapter2-functional-loss-tempo-20261011.yml",
)


def source_identity():
    hashes={p:sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCE_FILES}
    fingerprint=sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
    return {"digest":fingerprint,"files":hashes}


def tasks():
    d,_=contract()
    ex=d["experimental_factorial"]
    out=[]
    for p in range(ex["visitor_profile_history_seeds"]["first"],
                   ex["visitor_profile_history_seeds"]["last"]+1):
        for r in range(ex["demographic_repeat_seeds"]["first"],
                       ex["demographic_repeat_seeds"]["last"]+1):
            for timing in ex["mating_timing"]:
                for cost in ex["direct_assurance_cost"]:
                    for mu in ex["mutation_rate"]:
                        for schedule in d["scheduled_window"]["schedules"]:
                            out.append((p,r,timing,cost,mu,schedule))
    if len(out)!=1024 or len(set(out))!=1024:
        raise AssertionError("frozen biological campaign missing cells")
    return tuple(out)


def key(case):
    p,r,timing,cost,mutation,schedule=case
    return f"p{p}_r{r}_{timing}_cost{int(round(cost*100))}_mu{int(round(mutation*10000))}_{schedule}"


def write_atomic(path,data):
    path=Path(path)
    tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_bytes(data)
    os.replace(tmp,path)


def run_one(out_root,case,*,smoke_years=None):
    d,design_hash=contract()
    original_source=source_identity()
    p,r,timing,cost,mutation,schedule=case
    year=d["common_biology"]["years"] if smoke_years is None else smoke_years
    if smoke_years is not None and not 1<=smoke_years<=40:
        raise ValueError("smoke year count must be 1..40; never use the smoke mode for full biological inference")
    out=Path(out_root)
    out.mkdir(parents=True,exist_ok=True)
    stem=key(case)+("_SMOKE" if smoke_years is not None else "")
    json_path=out/(stem+".json")
    receipt_path=out/(stem+".receipt.json")
    if receipt_path.exists():
        rec=json.loads(receipt_path.read_text())
        if not json_path.exists() or rec["sha256"]!=sha256(json_path.read_bytes()).hexdigest() or rec["case"]!=list(case) or rec["design_sha256"]!=design_hash or rec.get("source_identity_sha256")!=original_source["digest"]:
            raise ValueError("existing case receipt/content/source provenance conflict")
        return stem
    if json_path.exists():
        raise ValueError("unowned result: missing original receipt")
    answer=simulate(p,r,schedule,timing,cost,mutation,years=year)
    answer["case_key"]=key(case)
    answer["full_declared_case"]=(smoke_years is None)
    data=(json.dumps(answer,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
    write_atomic(json_path,data)
    write_atomic(receipt_path,(json.dumps({
        "schema":"chapter2_sequence_abrupt_gradual_case_receipt_v1",
        "case":list(case),
        "design_sha256":design_hash,
        "source_identity_sha256":original_source["digest"],
        "source_file_sha256":original_source["files"],
        "sha256":sha256(data).hexdigest(),
        "full_declared_case":smoke_years is None,
        "years":year,
    },sort_keys=True,indent=2)+"\n").encode())
    return stem


def run_shard(out_root,*,shard_index,shard_count,smoke_years=None,case_limit=None):
    if not 0<=shard_index<shard_count or shard_count!=16:
        raise ValueError("frozen 16-shard policy required")
    todo=[case for i,case in enumerate(tasks()) if i%shard_count==shard_index]
    if len(todo)!=64:raise AssertionError("wrong number of cases in original shard")
    if case_limit is not None:
        if not 1<=case_limit<=len(todo):
            raise ValueError("invalid case cap")
        if smoke_years is None:
            raise ValueError("case-limit requires explicit short SMOKE mode")
        todo=todo[:case_limit]
    completed=[run_one(out_root,c,smoke_years=smoke_years) for c in todo]
    manifest={
        "schema":"chapter2_sequence_abrupt_gradual_shard_manifest_v1",
        "status":"COMPLETE_FROZEN_SHARD" if len(completed)==64 and smoke_years is None
                 else "INCOMPLETE_SMOKE_NO_BIOLOGICAL_READOUT",
        "shard_index":shard_index,"shard_count":shard_count,
        "case_count":len(completed),"expected_full_case_count":64,
        "case_keys":completed,"design_sha256":contract()[1],
        "source_identity_sha256":source_identity()["digest"],
    }
    if manifest["status"]=="COMPLETE_FROZEN_SHARD":
        write_atomic(Path(out_root)/f"shard_{shard_index:02d}_complete.json",
                     (json.dumps(manifest,sort_keys=True,indent=2)+"\n").encode())
    return manifest


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--shard-index",type=int,required=True)
    p.add_argument("--shard-count",type=int,default=16)
    p.add_argument("--smoke-years",type=int,default=None)
    p.add_argument("--case-limit",type=int,default=None)
    args=p.parse_args()
    result=run_shard(args.out,shard_index=args.shard_index,
        shard_count=args.shard_count,smoke_years=args.smoke_years,
        case_limit=args.case_limit)
    print(json.dumps({k:result[k] for k in (
        "status","shard_index","case_count","design_sha256")},sort_keys=True))


if __name__=="__main__":main()
