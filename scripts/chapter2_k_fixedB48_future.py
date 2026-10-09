"""Opt-in complete 2x2 K/B × 2 postzygotic-gate 80-update futures.

Prospective source IDs 41110901–41110964 must be independently authenticated.
No outcomes on import, manifest preparation, or PR CI. All source/genetic
extinctions retained. Full scientific adjudication is a separate workflow.
"""
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, replace
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.chapter2_k_fixedB48_manifest import compile_manifest, tasks
from scripts.chapter2_k_fixedB48_prehistory import prospective_biological_design
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.chapter2_orthogonal_capacity_pairing import state_fingerprint
from scripts.chapter2_postzygotic_viability_gate import gate_postzygotic_seed_viability
from scripts.chapter2_order_prehistory_runner import case_key, source_hashes, _atomic_bytes
from scripts.chapter2_order_postshock_runner import restore_prehistory
from scripts.model3_island.population import subset, advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_chapter2_assurance_generality import DEFAULT_DESIGN, config as model_config, load_design

ARMS=("K8_B48","K48_B48")
GATES=("baseline","self_half")
STATUS="NEW_FIXEDB48_56_RAW_FUTURES_UNADJUDICATED"


def selected_eight(task, full, d):
    if not 41110901 <= task.visitor_history <= 41110964:
        raise AssertionError("Cannot reuse exposed source cohort")
    if len(full.ids)>48:
        raise ValueError("Unfrozen source genotype population")
    tag=np.random.SeedSequence([task.visitor_history,task.demographic_repeat,
                                d["reproductive_settings"].index(task.setting),
                                4111092026]).generate_state(1)[0]
    pos=np.random.default_rng(int(tag)).choice(
        len(full.ids),size=min(8,len(full.ids)),replace=False)
    return subset(full,pos)


def future_seed(task,d,visitor,budget):
    if not 41110901<=task.visitor_history<=41110964:
        raise AssertionError("Unregistered new history")
    key=[task.visitor_history,task.demographic_repeat,
         d["reproductive_settings"].index(task.setting),
         ("near","far").index(visitor),
         d["postshock"]["budgets"].index(float(budget)),4111092048]
    return int(np.random.SeedSequence(key).generate_state(1)[0])


def one_future(task,founders,d,biology,K,B,gate,visitor,budget):
    if (K,B) not in ((8,48),(48,48)) or gate not in GATES:
        raise ValueError("Invalid frozen K/B/gate cell")
    cfg=replace(model_config(
        biology,task.setting,d["postshock"]["post_mutation_rate"],"evolving"
    ),capacity=K,ovule_budget=float(budget),assurance_mode="evolving")
    if cfg.seed_arrival.supply!=0 or len(founders.ids)>K:
        raise AssertionError("Invalid immigration or founder abundance")
    external=exposure(task.visitor_history+d["postshock"]["future_visitor_seed_offset"],visitor)
    master=future_seed(task,d,visitor,budget)
    streams={name:stream(master,name,0) for name in STREAM_IDS}
    current=founders
    first_extinction=0 if not len(current.ids) else None
    t0=None
    self_recruits=outcross_recruits=0
    for y in range(80):
        if not len(current.ids):
            break
        candidate=external.seed_candidates[y]
        if len(candidate.ids):
            raise AssertionError("No plant seed immigration")
        ledger=reproduce_kb(current,external.visitors[y],cfg,
                            background_denominator_capacity=B)
        if gate=="self_half":
            ledger=gate_postzygotic_seed_viability(
                ledger,selfed_fraction=0.5,outcross_fraction=1.0)
        if y==0:
            t0={
                "selfed_viable":float(ledger.self_viable.sum()),
                "outcrossed_viable":float(ledger.outcross.sum()),
                "exported_pollen":float(ledger.exported.sum()),
            }
        current,details=advance(
            current,ledger,candidate,cfg,streams,year=400+y)
        self_recruits+=int(details["resident_selfed_recruits"])
        outcross_recruits+=int(details["resident_outcross_recruits"])
        if first_extinction is None and not len(current.ids):
            first_extinction=y+1
    return {
        "arm":f"K{K}_B{B}","K":K,"B":B,"gate":gate,
        "budget":float(budget),"visitor":visitor,
        "t0_population":int(len(founders.ids)),"t0":t0,
        "end_population":int(len(current.ids)),
        "occupied":int(bool(len(current.ids))),
        "first_extinction":first_extinction,
        "cumulative_selfed_recruits":self_recruits,
        "cumulative_outcrossed_recruits":outcross_recruits,
    }


def one_source(out,pre,task,d,biology,manifest):
    key=case_key(task)
    target=out/f"k48_{key}.json"
    check=out/f"k48_{key}.sha256"
    full,source_digest=restore_prehistory(pre,task,d,source_hashes())
    eight=selected_eight(task,full,d)
    founder_hash=state_fingerprint(eight)
    if target.exists() or check.exists():
        if not target.is_file() or not check.is_file():
            raise AssertionError("Partial K/B future source")
        if hashlib.sha256(target.read_bytes()).hexdigest()!=check.read_text().strip():
            raise AssertionError("Corrupted resumed future")
        old=json.loads(target.read_text())
        if (old["task"]!=asdict(task) or old["source_sha256"]!=source_digest
                or old["protocol_sha256"]!=manifest["protocol_sha256"]
                or old["status"]!=STATUS or len(old["futures"])!=56):
            raise AssertionError("Changed or incomplete resumed source")
        return key
    futures=[one_future(task,eight,d,biology,K,B,gate,visitor,budget)
             for K,B in ((8,48),(48,48))
             for budget in d["postshock"]["budgets"]
             for visitor in ("near","far")
             for gate in GATES]
    got={(q["arm"],q["gate"],q["visitor"],q["budget"]) for q in futures}
    if len(got)!=56 or len(futures)!=56:
        raise AssertionError("Missing or duplicate K×B future")
    # Capacity alone is manipulated; identical starting genomes, visitor and B=48
    # require exactly identical initial expected reproductive payoffs.
    for budget in d["postshock"]["budgets"]:
        for visitor in ("near","far"):
            for gate in GATES:
                rows={q["K"]:q for q in futures
                      if q["budget"]==budget and q["visitor"]==visitor
                      and q["gate"]==gate}
                if set(rows)!={8,48} or rows[8]["t0_population"]!=rows[48]["t0_population"]:
                    raise AssertionError("K arm changed initial F8 founder abundance")
                if rows[8]["t0"]!=rows[48]["t0"]:
                    raise AssertionError("K changed initial reproduction at fixed B48")
    raw={
        "status":STATUS,"task":asdict(task),"source_sha256":source_digest,
        "sampled_founder_full_genotype_sha256":founder_hash,
        "protocol_sha256":manifest["protocol_sha256"],
        "source_hashes":source_hashes(),"futures":futures,
    }
    buf=(json.dumps(raw,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
    _atomic_bytes(target,buf)
    _atomic_bytes(check,(hashlib.sha256(buf).hexdigest()+"\n").encode())
    return key


def run_shard(pre,out,shard,workers):
    if not 0<=shard<64 or not 1<=workers<=4:
        raise ValueError("Unfrozen shard/workers")
    m=compile_manifest()
    group=tasks()[shard]
    receipt=json.loads((pre/f"k48_pre_shard_{shard:02}.json").read_text())
    if (receipt["protocol_sha256"]!=m["protocol_sha256"]
            or receipt["task_sha256"]!=m["shards"][shard]["task_sha256"]
            or receipt["case_keys"]!=sorted(case_key(t) for t in group)
            or receipt["n_t400_sources"]!=32):
        raise AssertionError("No authentic complete new cohort source")
    d=prospective_biological_design()
    biology=load_design(DEFAULT_DESIGN)
    out.mkdir(parents=True,exist_ok=True)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        records=sorted(f.result() for f in as_completed([
            pool.submit(one_source,out,pre,t,d,biology,m) for t in group
        ]))
    if records!=sorted(case_key(t) for t in group):
        raise AssertionError("Incomplete full future shard")
    receipt={
        "status":"K_FIXEDB48_COMPLETE_32_SOURCES_1792_FUTURES_UNADJUDICATED",
        "history":41110901+shard,"shard":shard,
        "n_sources":32,"n_futures":1792,
        "protocol_sha256":m["protocol_sha256"],
        "source_hashes":source_hashes(),
        "case_keys":records,
    }
    _atomic_bytes(out/f"k48_future_shard_{shard:02}.json",
                  (json.dumps(receipt,indent=2,sort_keys=True)+"\n").encode())
    return receipt


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--prehistory",type=Path)
    ap.add_argument("--out",type=Path)
    ap.add_argument("--shard-index",type=int,required=True)
    ap.add_argument("--workers",type=int,default=2)
    ap.add_argument("--dry-run",action="store_true")
    ap.add_argument("--execute-frozen-cohort",action="store_true")
    ap.add_argument("--acknowledge-resource-cost",action="store_true")
    a=ap.parse_args()
    if a.dry_run:
        print(json.dumps({"futures_per_shard":1792,"biology_executed":False}))
        return
    if not (a.execute_frozen_cohort and a.acknowledge_resource_cost):
        raise PermissionError("Only dual-opt-in K/B production is authorized")
    if a.prehistory is None or a.out is None:
        raise ValueError("Source and output archives required")
    print(json.dumps(run_shard(a.prehistory,a.out,a.shard_index,a.workers)))


if __name__=="__main__":
    main()
