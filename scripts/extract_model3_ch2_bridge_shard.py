"""Extract compact, auditable sufficient statistics from one frozen bridge shard."""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

import numpy as np

from scripts.model3_island.design import canonical, digest

INTERVENTIONS = {
    "natural": ("near", "far"),
    "richness_matched": ("matched_near", "matched_far"),
    "visitor_pooled": ("pool_near", "pool_far"),
    "large_plant_capacity": ("large_near", "large_far"),
}
MODES = {
    "individual": ("trait_mean", "population"),
    "density": ("density_traits", "density_mass"),
}


def _jsonable(a):
    x=np.asarray(a,float)
    out=[]
    for row in x:
        rr=[]
        for col in row:
            rr.append([None if not np.isfinite(v) else float(v) for v in col])
        out.append(rr)
    return out


def _expected_shard(parent, shard):
    if shard.get("execution_shard") is None:
        raise ValueError("missing execution_shard")
    expected=deepcopy(parent)
    expected["history_seeds"]=list(shard["history_seeds"])
    expected["cases"]=len(expected["history_seeds"])*len(expected["demographic_seeds"])*len(expected["starts"])*len(expected["arms"])
    expected["execution_shard"]=shard["execution_shard"]
    return expected


def extract(parent, shard, campaign):
    campaign=Path(campaign)
    if shard != _expected_shard(parent,shard):
        raise ValueError("shard is not a pure execution partition of parent design")
    if shard["source_hashes"] != parent["source_hashes"]:
        raise ValueError("source hashes differ from parent design")
    status=json.loads((campaign/"campaign_status.json").read_text())
    if not status.get("complete") or status["completed"]!=shard["cases"] or status["expected"]!=shard["cases"]:
        raise ValueError(f"incomplete shard: {status}")
    if json.loads((campaign/"manifest.json").read_text()) != shard:
        raise ValueError("campaign manifest differs from shard design")
    mh=digest(shard)
    if status["manifest_hash"]!=mh:
        raise ValueError("shard manifest hash mismatch")

    starts=list(parent["starts"]); histories=list(shard["history_seeds"]); demos=list(parent["demographic_seeds"])
    shape=(len(starts),len(histories),len(demos))
    changes={(arm,mode):np.full(shape,np.nan) for arm in parent["arms"] for mode in MODES}
    occupancy={(arm,mode):np.zeros(shape,float) for arm in parent["arms"] for mode in MODES}
    visitor={}
    root=sha256()

    for si,start in enumerate(starts):
        sid=int(round(start*10))
        for hi,hs in enumerate(histories):
            for di,ds in enumerate(demos):
                for arm in parent["arms"]:
                    case_id=f"{arm}-s{sid}-h{hs}-d{ds}"
                    folder=campaign/case_id
                    inp=json.loads((folder/"input.json").read_text())
                    receipt=json.loads((folder/"receipt.json").read_text())
                    raw=(folder/"arrays.npz").read_bytes()
                    if inp.get("id")!=case_id or inp.get("manifest_hash")!=mh:
                        raise ValueError(f"input identity mismatch {case_id}")
                    if receipt.get("status")!="complete" or receipt.get("manifest_hash")!=mh:
                        raise ValueError(f"receipt mismatch {case_id}")
                    if digest(inp)!=receipt.get("case_hash"):
                        raise ValueError(f"case hash mismatch {case_id}")
                    if sha256(raw).hexdigest()!=receipt.get("arrays_sha256"):
                        raise ValueError(f"array hash mismatch {case_id}")
                    root.update(case_id.encode());root.update(receipt["arrays_sha256"].encode())
                    with np.load(folder/"arrays.npz",allow_pickle=False) as a:
                        vc=np.asarray(a["visitor_count"])
                        vk=(arm,hi)
                        if vk in visitor:
                            if not np.array_equal(visitor[vk],vc):
                                raise ValueError(f"visitor history differs across starts/repeats {arm} {hs}")
                        else:
                            visitor[vk]=vc.copy()
                        for mode,(trait_key,pop_key) in MODES.items():
                            tr=np.asarray(a[trait_key]); pop=np.asarray(a[pop_key])
                            occupancy[arm,mode][si,hi,di]=float(pop[-1]>0)
                            valid=bool(pop[0]>0 and pop[-1]>0 and np.isfinite(tr[[0,-1],1]).all())
                            if valid:
                                changes[arm,mode][si,hi,di]=float(tr[-1,1]-tr[0,1])

    contrasts={}
    for name,(near,far) in INTERVENTIONS.items():
        contrasts[name]={}
        for mode in MODES:
            contrasts[name][mode]={
                "values":_jsonable(changes[far,mode]-changes[near,mode]),
                "near_occupancy":_jsonable(occupancy[near,mode]),
                "far_occupancy":_jsonable(occupancy[far,mode]),
            }

    visitor_out={}
    for arm in parent["arms"]:
        visitor_out[arm]=[visitor[(arm,hi)].astype(int).tolist() for hi in range(len(histories))]

    return {
        "schema_version":"1.0",
        "status":"complete_bridge_shard_extract",
        "parent_design_hash":digest(parent),
        "shard_design_hash":mh,
        "execution_shard":shard["execution_shard"],
        "history_seeds":histories,
        "starts":starts,
        "demographic_seeds":demos,
        "cases_verified":int(shard["cases"]),
        "receipt_arrays_hash_root":root.hexdigest(),
        "contrasts":contrasts,
        "visitor_count":visitor_out,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--parent-design",required=True)
    p.add_argument("--shard-design",required=True)
    p.add_argument("--campaign",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    parent=json.loads(Path(a.parent_design).read_text())
    shard=json.loads(Path(a.shard_design).read_text())
    result=extract(parent,shard,Path(a.campaign))
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(canonical(result))
    print(json.dumps({k:result[k] for k in ("status","execution_shard","cases_verified","receipt_arrays_hash_root")},indent=2))


if __name__=="__main__":
    main()
