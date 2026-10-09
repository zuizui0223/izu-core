"""Frozen scientific contract and archive authentication for the planned seed viability factorial."""
from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import hashlib
import json

from scripts.chapter2_order_budget_window_followup import load_followup,history_shard,SPEC as FOLLOWUP
from scripts.chapter2_order_prehistory_runner import source_hashes,case_key
from scripts.chapter2_order_postshock_runner import restore_prehistory
from scripts.plan_chapter2_order_expression_identification import SPEC as ORIGINAL,prehistories
from scripts.chapter2_postzygotic_viability_gate import FACTORIAL_GATES

ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/"data/design/chapter2_postzygotic_viability_factorial_20261009.json"
GATE=ROOT/"scripts/chapter2_postzygotic_viability_gate.py"
GATES=("baseline","attenuate_self","attenuate_outcross","attenuate_both")


def sha(path:Path)->str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def frozen():
    s=json.loads(SPEC.read_text(encoding="utf-8"))
    _,d=load_followup()
    expected={name:{"selfed_fraction":pair[0],"outcross_fraction":pair[1]}
              for name,pair in FACTORIAL_GATES.items()}
    if (s["status"]!="PRE_OUTCOME_INTERVENTION_DESIGN_ONLY"
        or s["reusable_source"]["t400_source_run_id"]!=37862121201
        or s["reusable_source"]["t400_source_visitor_history_ids"]!=[38110901,38110964]
        or s["postzygotic_viability_factorial"]["arms"]!=expected
        or s["full_future_grid"]["newly_generated_future_branches"]!=172032
        or s["full_future_grid"]["total_futures_including_verified_baseline"]!=229376
        or s["estimand"]["bootstrap"]!={"unit":"visitor_history","draws":9999,
                 "seed":2026100927,"interval":"percentile95","two_sided":True}
        or s["estimand"]["minimum_meaningful_tau_absolute"]!=0.005):
        raise AssertionError("Viability intervention contract changed")
    tasks=prehistories(d)
    if len(tasks)!=2048 or len({t.visitor_history for t in tasks})!=64:
        raise AssertionError("Source history units changed")
    return d,tasks


def hashes():
    return {"design":sha(SPEC),"gate":sha(GATE),
            "old_protocol":sha(ORIGINAL),"old_followup":sha(FOLLOWUP),
            "biology":source_hashes()}


def folder(root:Path,prefix:str,shard:int)->Path:
    return Path(root)/f"{prefix}{shard}"


def verify_registry(pre_root:Path,post_root:Path,shard:int,tasks,d):
    if not 0<=shard<64:
        raise ValueError("Expected one of 64 history shards")
    group=history_shard(tasks,38110901,shard,64)
    expected=sorted(case_key(t) for t in group)
    for root,prefix,stage in [
        (pre_root,"budget-window-pre-shard-","pre"),
        (post_root,"budget-window-post-shard-","post")]:
        path=folder(root,prefix,shard)/f"window_{stage}_shard_{shard:02}.json"
        row=json.loads(path.read_text(encoding="utf-8"))
        if (row["stage"]!=stage or row["shard"]!=shard
            or row["status"]!="raw_unadjudicated"
            or row["case_keys"]!=expected
            or row["source_hashes"]!=source_hashes()
            or row["new_protocol_sha256"]!=sha(FOLLOWUP)
            or row["underlying_biological_protocol_sha256"]!=sha(ORIGINAL)):
            raise AssertionError("Missing or altered historical "+stage+" receipt")
    return group


def old_state_and_future(pre:Path,post:Path,task,d):
    name=case_key(task)
    raw=post/f"{name}.json"
    if sha(raw)!=(post/f"{name}.sha256").read_text().strip():
        raise AssertionError("Original future checksum mismatch")
    state,digest=restore_prehistory(pre,task,d,source_hashes())
    row=json.loads(raw.read_text(encoding="utf-8"))
    if (row["task"]!=asdict(task)
        or row["status"]!="raw_postshock_unadjudicated"
        or row["source_hashes"]!=source_hashes()
        or row["protocol_sha256"]!=sha(ORIGINAL)
        or row["prehistory_state_sha256"]!=digest
        or len(row["postshock"])!=28):
        raise AssertionError("Unverified original full-diploid source/future")
    ids={(c["regime"],float(c["budget"]),c["future_visitor"]) for c in row["postshock"]}
    expected={(r,float(b),v) for r in d["postshock"]["arms"]
              for b in d["postshock"]["budgets"]
              for v in d["postshock"]["future_environments"]}
    if ids!=expected:
        raise AssertionError("Archived 28-way baseline grid changed")
    return state,digest,row
