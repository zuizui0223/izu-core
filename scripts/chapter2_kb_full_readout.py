"""Full-cohort, source authenticated preregistered K/B readout.

Nothing is adjudicated until all 64 new histories, all 2048 source receipts
and all 229376 full future cells with SHA-256 checksums are accepted.
"""
from __future__ import annotations

from itertools import product
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

from scripts.chapter2_kb_cohort_manifest import compile_manifest,tasks
from scripts.chapter2_kb_future_runner import ARMS,GATES,STATUS
from scripts.chapter2_kb_prehistory_source_runner import prospective_biological_design
from scripts.chapter2_order_prehistory_runner import case_key,source_hashes
from scripts.plan_chapter2_order_expression_identification import log_budget_weights
from scripts.plan_chapter2_kb_decoupled import validate_protocol

EXPECTED_SHAPE=(64,4,2,2,2,7,2,4,2)


def admit(root:Path,source_admission:Path):
    d=prospective_biological_design()
    m=compile_manifest()
    v=json.loads(source_admission.read_text())
    if (v.get("status")!="ALL_2048_INDEPENDENT_KB_T400_SOURCES_AUTHENTICATED"
            or v.get("source_count")!=2048 or v.get("history_count")!=64
            or v.get("protocol_sha256")!=m["protocol_sha256"]):
        raise AssertionError("Original full new diploid source admission missing")
    cube=np.full(EXPECTED_SHAPE,np.nan)
    n=0
    for s,group in enumerate(tasks()):
        folder=root/f"chapter2-kb-future-shard-{s}"
        receipt=json.loads((folder/f"kb_future_shard_{s:02}.json").read_text())
        if (receipt.get("status")!="K_B_COMPLETE_32_SOURCES_3584_FUTURES_UNADJUDICATED"
                or receipt.get("history")!=40110901+s
                or receipt.get("n_sources")!=32
                or receipt.get("n_futures")!=3584
                or receipt.get("protocol_sha256")!=m["protocol_sha256"]
                or receipt.get("case_keys")!=sorted(case_key(t) for t in group)
                or receipt.get("source_hashes")!=source_hashes()):
            raise AssertionError("Incomplete or corrupted K/B history shard")
        for task in group:
            key=case_key(task)
            path=folder/f"kb_{key}.json"
            check=folder/f"kb_{key}.sha256"
            if hashlib.sha256(path.read_bytes()).hexdigest()!=check.read_text().strip():
                raise AssertionError("Bad future source checksum")
            row=json.loads(path.read_text())
            if (row.get("status")!=STATUS or row.get("task")!=vars(task)
                    or row.get("protocol_sha256")!=m["protocol_sha256"]
                    or row.get("source_hashes")!=source_hashes()
                    or len(row.get("futures",[]))!=112):
                raise AssertionError("Unfrozen future provenance")
            seen=set()
            for x in row["futures"]:
                arm=x["arm"];gate=x["gate"];budget=float(x["budget"]);visitor=x["visitor"]
                ident=(arm,gate,budget,visitor)
                if (ident in seen or arm not in ARMS or gate not in GATES
                        or budget not in d["postshock"]["budgets"]
                        or visitor not in ("near","far")
                        or (x["K"],x["B"])!=((8,8),(8,48),(48,8),(48,48))[ARMS.index(arm)]
                        or x["t0_population"]>x["K"] or x["t0_population"]>8
                        or type(x["occupied"]) is not int or x["occupied"] not in (0,1)
                        or int(x["end_population"]>0)!=x["occupied"]):
                    raise AssertionError("Invalid K/B future cell")
                seen.add(ident)
                idx=(task.visitor_history-40110901,
                     d["reproductive_settings"].index(task.setting),
                     d["environmental_settings"].index(task.environment),
                     ("assurance_first","investment_first").index(task.expression_order),
                     d["nested_demographic_repeats"].index(task.demographic_repeat),
                     d["postshock"]["budgets"].index(budget),
                     ("near","far").index(visitor),ARMS.index(arm),GATES.index(gate))
                if np.isfinite(cube[idx]):
                    raise AssertionError("Duplicate whole-cohort cell")
                cube[idx]=x["occupied"]
                n+=1
            if seen!=set(product(ARMS,GATES,d["postshock"]["budgets"],("near","far"))):
                raise AssertionError("Missing full K/B factorial future")
    if n!=229376 or not np.isfinite(cube).all() or cube.shape!=EXPECTED_SHAPE:
        raise AssertionError("Incomplete independent 229376-future campaign")
    return cube,d


def summarize(cube,d):
    if cube.shape!=EXPECTED_SHAPE or not np.isfinite(cube).all():
        raise AssertionError("Incomplete whole-cohort admission before inference")
    weight=log_budget_weights(d)
    w=np.array([weight[float(b)] for b in d["postshock"]["budgets"]])
    pooled=cube.mean(axis=(4,6))
    if pooled.shape!=(64,4,2,2,7,4,2):
        raise AssertionError("Aggregation across wrong nested units")
    weighted=np.tensordot(pooled,w,axes=([4],[0]))
    history=(weighted[:,:,:,0,:,:]-weighted[:,:,:,1,:,:]).mean(axis=(1,2))
    if history.shape!=(64,4,2):
        raise AssertionError("History unit changed")
    tau=history[:,:,0]-history[:,:,1]
    contrasts={
        "primary_B_at_K8":tau[:,0]-tau[:,1],
        "secondary_K_at_B8":tau[:,0]-tau[:,2],
        "secondary_K_at_B48":tau[:,1]-tau[:,3],
        "secondary_B_at_K48":tau[:,2]-tau[:,3],
        "secondary_K_by_B":tau[:,0]-tau[:,1]-tau[:,2]+tau[:,3],
    }
    seed=2026100957
    draws=9999
    ids=np.random.default_rng(seed).integers(0,64,size=(draws,64))
    def estimate(v):
        q=np.percentile(v[ids].mean(axis=1),[2.5,97.5])
        return {"mean":float(v.mean()),"bootstrap95":[float(q[0]),float(q[1])],
                "positive_histories":int((v>1e-12).sum()),
                "negative_histories":int((v<-1e-12).sum())}
    estimates={name:estimate(x) for name,x in contrasts.items()}
    arm_sensitivities={ARMS[i]:estimate(tau[:,i]) for i in range(4)}
    main=estimates["primary_B_at_K8"]
    lo,hi=main["bootstrap95"]
    if abs(main["mean"])>=0.005 and (lo>0 or hi<0):
        verdict="supported_controlled_background_B_moderation_at_K8"
    elif lo>-0.005 and hi<0.005:
        verdict="practically_equivalent_within_0p005"
    else:
        verdict="inconclusive"
    return {
        "status":"INDEPENDENT_64_HISTORIES_2048_T400_229376_KB_FUTURES_ADMITTED",
        "n_independent_visitor_histories":64,
        "n_t400_sources":2048,
        "n_future_cells":229376,
        "original_predeclared_primary":"tau(K8,B8)-tau(K8,B48)",
        "primary_verdict":verdict,
        "paired_bootstrap":{"unit":"visitor_history","draws":draws,"seed":seed},
        "by_arm_sensitivity":arm_sensitivities,
        "contrasts":estimates,
        "interpretation_limit":"Synthetic model-specific recipient pollen dilution B vs demographic ceiling K; not natural genetic order mediation, ecological universality or measured Izu extinction."
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--futures",type=Path,required=True)
    ap.add_argument("--t400-admission",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--execute-full-adjudication",action="store_true")
    a=ap.parse_args()
    if not a.execute_full_adjudication:
        raise PermissionError("Full-cohort adjudication only, explicit execution")
    validate_protocol()
    cube,d=admit(a.futures,a.t400_admission)
    result=summarize(cube,d)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps({
        "status":result["status"],
        "primary":result["contrasts"]["primary_B_at_K8"],
        "primary_verdict":result["primary_verdict"],
    }))


if __name__=="__main__":
    main()
