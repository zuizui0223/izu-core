"""Read-only replay audit: keep numerical agreement separate from original bytes.

Does not change either frozen values or their strict byte-identity admission gate.
No biological simulation, historical-runtime authentication or genome reconstruction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path

import numpy as np


def audit(directory: Path, design: dict, frozen: dict) -> dict:
    paths=list(Path(directory).rglob("demographic_independent32_shard_*.json"))
    names={f"demographic_independent32_shard_{i:02d}.json" for i in range(8)}
    if len(paths)!=8 or {p.name for p in paths}!=names:
        raise ValueError("Require exactly eight unique original shard files")
    settings=list(design["settings"])
    histories=list(range(design["independent_visitor_histories"]["first"],
                         design["independent_visitor_histories"]["last"]+1))
    rep,=design["demographic_repeat_seeds"]
    if len(settings)!=4 or len(histories)!=32 or design["total_groups"]!=512:
        raise ValueError("Independent32 source design scope differs")
    keys=set(product(settings,("fixed","evolving"),histories,(rep,),("near","far")))
    grid=set(product(design["post_environments"],design["stress_ovule_budgets"]))
    if len(grid)!=8:
        raise ValueError("Eight-case stress grid required")
    capacity=design["post_capacity"]
    if isinstance(capacity,bool) or not isinstance(capacity,int) or capacity<=0:
        raise ValueError("Invalid declared census capacity")
    records={}; hashes={}; mismatches=[]
    for path in sorted(paths):
        raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
        hashes[path.name]=digest
        expected=frozen["archive"]["offline_shard_sha256"][path.name]
        if digest!=expected:
            mismatches.append({"member":path.name,"observed_sha256":digest,"declared_sha256":expected})
        for row in json.loads(raw):
            key=tuple(row["group"])
            if key in records:
                raise ValueError("duplicate history group")
            if key not in keys:
                raise ValueError("Unexpected history group")
            if (isinstance(row["pre_survivors"],bool) or not isinstance(row["pre_survivors"],int)
                or row["pre_survivors"]<0):
                raise ValueError("Invalid preparation census")
            cases=row["post_cases"]
            if row["pre_survivors"]==0 and cases is None:
                # The original source's no-immigration extinction marker denotes
                # eight structural zeros. Keep the history in the all-start mean.
                cases=[{"post":p,"ovule_budget":b,"occupied":0,"terminal_N":0}
                       for p,b in sorted(grid)]
                row={**row,"post_cases":cases}
            if (not isinstance(cases,list) or len(cases)!=8
                or {(p["post"],p["ovule_budget"]) for p in cases}!=grid):
                raise ValueError("Incomplete or duplicated stress grid")
            for case in cases:
                flag=case["occupied"];n=case["terminal_N"]
                if isinstance(flag,bool) or not isinstance(flag,int) or flag not in (0,1):
                    raise ValueError("Invalid occupancy indicator")
                if isinstance(n,bool) or not isinstance(n,int) or n<0 or n>capacity or int(n>0)!=flag:
                    raise ValueError("Invalid census or census/occupancy contradiction")
                if row["pre_survivors"]==0 and n!=0:
                    raise ValueError("Extinct preparation contradicts no-immigration future census")
            records[key]=row
    if set(records)!=keys:
        raise ValueError("Incomplete all-start history inventory")
    values=np.empty((32,4),float);fixed=np.empty_like(values);evolved=np.empty_like(values)
    for hi,h in enumerate(histories):
        for si,setting in enumerate(settings):
            def occupancy(mode,pre):
                return sum(p["occupied"] for p in records[setting,mode,h,rep,pre]["post_cases"])/8
            fixed[hi,si]=occupancy("fixed","far")-occupancy("fixed","near")
            evolved[hi,si]=occupancy("evolving","far")-occupancy("evolving","near")
            values[hi,si]=evolved[hi,si]-fixed[hi,si]
    draw=design["bootstrap"]["draws"];seed=design["bootstrap"]["seed"]
    if draw!=9999 or seed!=frozen.get("bootstrap_seed",seed):
        raise ValueError("Frozen bootstrap configuration differs")
    index=np.random.default_rng(seed).choice(32,size=(draw,32),replace=True)
    sampled=values[index].mean(axis=1)
    pooled={"mean":float(values.mean()),
            "bootstrap95":np.percentile(sampled.mean(axis=1),[2.5,97.5]).tolist()}
    per_setting=[{"setting":s,"fixed_delta":float(fixed[:,i].mean()),
                  "evolving_delta":float(evolved[:,i].mean()),"interaction":float(values[:,i].mean()),
                  "bootstrap95":np.percentile(sampled[:,i],[2.5,97.5]).tolist()}
                 for i,s in enumerate(settings)]
    failures=[]
    def compare(label,observed,expected):
        a=np.asarray(observed,dtype=float);b=np.asarray(expected,dtype=float)
        if a.shape!=b.shape or not np.isfinite(a).all() or not np.isfinite(b).all() or not np.allclose(a,b,atol=1e-12,rtol=0):
            failures.append({"field":label,"observed":observed,"frozen":expected})
    for k in ("mean","bootstrap95"):
        compare("pooled_primary."+k,pooled[k],frozen["predeclared_pooled_primary"][k])
    declared={r["setting"]:r for r in frozen["per_setting"]}
    if set(declared)!=set(settings) or len(frozen["per_setting"])!=4:
        raise ValueError("Frozen setting inventory differs")
    for row in per_setting:
        for k in ("fixed_delta","evolving_delta","interaction","bootstrap95"):
            if k in declared[row["setting"]]:
                compare(row["setting"]+"."+k,row[k],declared[row["setting"]][k])
    numerical=not failures
    status=("NUMERICAL_DISAGREEMENT_NOT_ADMITTED" if not numerical else
            "NUMERICS_MATCH_DECLARED_BYTES_DIVERGE_NOT_ORIGINAL_ADMISSION" if mismatches else
            "NUMERICS_AND_DECLARED_SHARD_BYTES_MATCH")
    return {"schema":"independent32_replay_admission_v1","status":status,
            "groups":512,"post_trajectories":4096,"independent_histories":32,
            "numerical_agreement":numerical,"declared_byte_agreement":not mismatches,
            "shard_sha256":hashes,"byte_mismatches":mismatches,"numerical_mismatches":failures,
            "pooled_primary":pooled,"per_setting":per_setting,
            "bootstrap":{"draws":draw,"seed":seed,"absolute_tolerance":1e-12,"relative_tolerance":0},
            "original_genome_or_runtime_identity_authenticated":False,
            "scope":"All-start numerical summaries and declared shard byte comparison only. A numerical match does not replace frozen original-identity admission; no retuning, new biological run or natural-order mediation."}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--design",type=Path,required=True)
    p.add_argument("--frozen",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args();r=audit(a.input,json.loads(a.design.read_bytes()),json.loads(a.frozen.read_bytes()))
    r["input_design_sha256"]=hashlib.sha256(a.design.read_bytes()).hexdigest()
    r["frozen_readout_sha256"]=hashlib.sha256(a.frozen.read_bytes()).hexdigest()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_bytes((json.dumps(r,indent=2,allow_nan=False)+"\n").encode("utf-8"))
    print(json.dumps({k:r[k] for k in ("status","groups","post_trajectories","numerical_agreement","declared_byte_agreement")}))


if __name__=="__main__":main()
