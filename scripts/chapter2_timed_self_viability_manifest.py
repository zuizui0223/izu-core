"""Compile prospective new 64-history K/B cohort task identities, no biology."""
from __future__ import annotations
from dataclasses import asdict
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

from scripts.plan_chapter2_order_expression_identification import Prehistory
from scripts.plan_chapter2_timed_self_viability import SPEC as PROTOCOL, frozen as validate_protocol
from scripts.chapter2_order_prehistory_runner import case_key, source_hashes

N_HIST=64
SOURCES_PER_HISTORY=32
FUTURES_PER_SOURCE=112


def tasks():
    d=validate_protocol()
    h=d["independent_cohort"]
    out=[]
    for ident in range(h["visitor_history_first"],h["visitor_history_last"]+1):
        group=[Prehistory(setting,env,order,ident,rep)
               for setting,env,order,rep in product(
                   h["reproductive_settings"],h["prehistory_visitor_environments"],
                   h["assigned_expression_histories"],
                   h["demographic_repeat_ids"])]
        if len(group)!=32 or len({case_key(t) for t in group})!=32:
            raise AssertionError("Expected complete 32-case history")
        out.append(group)
    if len(out)!=64 or len({case_key(t) for g in out for t in g})!=2048:
        raise AssertionError("Not 2048 genuinely new independent t400 sources")
    return out


def compile_manifest():
    groups=tasks()
    records=[]
    for i,g in enumerate(groups):
        row=[asdict(t) for t in g]
        binary=json.dumps(row,sort_keys=True,separators=(",",":")).encode()
        records.append({
            "shard_index":i,"visitor_history":42110901+i,
            "case_keys":[case_key(t) for t in g],
            "task_sha256":hashlib.sha256(binary).hexdigest(),
            "sources":32,"futures_expected":32*112,
        })
    m={
        "status":"PROSPECTIVE_TIMED_SELF_VIABILITY_TASKS_NO_OUTCOMES",
        "protocol_sha256":hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
        "source_code_sha256":source_hashes(),
        "n_histories":64,"n_sources":2048,
        "futures_per_source":112,"expected_futures":229376,
        "shards":records,
    }
    if sum(x["futures_expected"] for x in records)!=229376:
        raise AssertionError("Omitted K/B futures")
    return m


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    row=compile_manifest()
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(row,sort_keys=True,indent=2)+"\n")
    print(json.dumps({
        "status":row["status"],"n_histories":64,"n_sources":2048,
        "planned_futures":229376,"biology_executed":False}))


if __name__=="__main__":
    main()
