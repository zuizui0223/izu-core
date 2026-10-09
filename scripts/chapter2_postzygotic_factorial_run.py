"""Run only the three *new* viability-gated futures from each verified t400 source."""
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor,as_completed
from dataclasses import asdict
from pathlib import Path
import argparse
import hashlib
import json

from scripts.chapter2_postzygotic_factorial_common import (
    frozen,hashes,folder,verify_registry,old_state_and_future,sha,
)
from scripts.chapter2_order_prehistory_runner import case_key,_atomic_bytes
from scripts.chapter2_order_postshock_runner import sampled_eight
from scripts.chapter2_postzygotic_viability_gate import simulate_gated_future
from scripts.run_chapter2_assurance_generality import DEFAULT_DESIGN,load_design


def one_source(out:Path,pre:Path,post:Path,task,d,biology):
    key=case_key(task)
    dest=out/f"viability_{key}.json"
    check=out/f"viability_{key}.sha256"
    provenance=hashes()
    if dest.exists() or check.exists():
        if not dest.is_file() or not check.is_file() or sha(dest)!=check.read_text().strip():
            raise AssertionError("Partial/corrupt resumed viability source")
        x=json.loads(dest.read_text())
        if x["task"]!=asdict(task) or x["hashes"]!=provenance or len(x["futures"])!=84:
            raise AssertionError("Wrong resumed experiment")
        return key
    state,source_sha,reference=old_state_and_future(pre,post,task,d)
    selected=sampled_eight(task,state,d)
    reference_by_key={(x["regime"],float(x["budget"]),x["future_visitor"]):x
                      for x in reference["postshock"]}
    futures=[]
    for gate in ("attenuate_self","attenuate_outcross","attenuate_both"):
        for regime in d["postshock"]["arms"]:
            for budget in d["postshock"]["budgets"]:
                for visitor in d["postshock"]["future_environments"]:
                    actual=simulate_gated_future(
                        task,state,selected,d,biology,regime,visitor,float(budget),
                        intervention=gate)
                    old=reference_by_key[(regime,float(budget),visitor)]
                    if (actual["t0_population"]!=old["t0_population"]
                        or actual["future_expression_offsets"]!=[0,0]):
                        raise AssertionError("Altered t400 source or future expression")
                    futures.append({"gate":gate,**actual})
    ids={(r["gate"],r["regime"],r["budget"],r["future_visitor"]) for r in futures}
    if len(futures)!=84 or len(ids)!=84:
        raise AssertionError("Incomplete future factorial grid")
    row={"status":"raw_futures_no_adjudication",
         "task":asdict(task),"hashes":provenance,
         "state_sha256":source_sha,
         "old_future_sha256":sha(post/f"{key}.json"),
         "futures":futures}
    buf=(json.dumps(row,sort_keys=True,allow_nan=False,indent=2)+"\n").encode()
    _atomic_bytes(dest,buf)
    _atomic_bytes(check,(hashlib.sha256(buf).hexdigest()+"\n").encode())
    return key


def run_shard(pre_root:Path,post_root:Path,out:Path,shard:int,workers:int):
    d,tasks=frozen()
    if workers not in (1,2,3,4):
        raise ValueError("Only 1 to 4 workers are admitted")
    group=verify_registry(pre_root,post_root,shard,tasks,d)
    pre=folder(pre_root,"budget-window-pre-shard-",shard)
    post=folder(post_root,"budget-window-post-shard-",shard)
    out.mkdir(parents=True,exist_ok=True)
    bio=load_design(DEFAULT_DESIGN)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        keys=sorted(f.result() for f in as_completed(
            [pool.submit(one_source,out,pre,post,t,d,bio) for t in group]))
    expected=sorted(case_key(t) for t in group)
    if keys!=expected or len(keys)!=32:
        raise AssertionError("Incomplete history shard")
    receipt={"status":"complete_raw_32_source_2688_futures",
             "shard":shard,"visitor_history":38110901+shard,
             "keys":keys,"count":2688,"hashes":hashes()}
    _atomic_bytes(out/f"factorial_shard_{shard:02}.json",
                  (json.dumps(receipt,sort_keys=True,indent=2)+"\n").encode())
    return receipt


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode",choices=("plan","shard"),required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--prehistory",type=Path)
    p.add_argument("--baseline",type=Path)
    p.add_argument("--shard",type=int)
    p.add_argument("--workers",type=int,default=2)
    p.add_argument("--execute-frozen-cohort",action="store_true")
    a=p.parse_args()
    d,tasks=frozen()
    if a.mode=="plan":
        row={"status":"DESIGN_ONLY_NO_FRESH_FUTURES",
             "source_states_reused":len(tasks),"independent_histories":64,
             "baseline_futures_to_verify":57344,
             "new_futures_planned":172032,
             "full_factorial":229376,"production_launched":False,
             "hashes":hashes()}
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(json.dumps(row,indent=2)+"\n")
        print(json.dumps(row))
        return
    if not a.execute_frozen_cohort:
        raise PermissionError("New biological future outcomes require explicit launch")
    if a.prehistory is None or a.baseline is None or a.shard is None:
        raise ValueError("Need baseline and prehistory archives and explicit shard")
    receipt=run_shard(a.prehistory,a.baseline,a.out,a.shard,a.workers)
    print(json.dumps({"status":receipt["status"],"shard":a.shard}))


if __name__=="__main__":
    main()
