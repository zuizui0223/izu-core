"""Independent vectorized check of retrospective high-I access from saved Q3 NPZ.

Does not import the primary Chapter 3 auditor, model operators, birth simulators
or past results of its new conclusion. Validates source SHA and recomputes
the same mathematical exclusion using broadcast masks.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/"data/results/directional_access_20261013"


def check(root: Path=ROOT) -> dict:
    folder=root/"data/results/directional_access_20261013"
    prior=json.loads((folder/"READOUT.json").read_text(encoding="utf-8"))
    raw_arrays=(folder/"ALL_CENSUS_SUPPORT.npz").read_bytes()
    raw_cases=(folder/"ALL_CASES.csv").read_bytes()
    if (hashlib.sha256(raw_arrays).hexdigest()!=prior["arrays_sha256"]
        or hashlib.sha256(raw_cases).hexdigest()!=prior["cases_sha256"]):
        raise ValueError("Q3 original source digest differs")
    with np.load(folder/"ALL_CENSUS_SUPPORT.npz",allow_pickle=False) as z:
        keys=z["keys"].astype(str).tolist()
        maximum=z["maximum"].copy()
        minimum=z["minimum"].copy()
        support=z["support_size"].copy()
        pvar=z["phenotype_variance"].copy()
    if (len(keys)!=2304 or len(set(keys))!=2304
        or any(x.shape!=(2304,201) for x in (maximum,minimum,support,pvar))):
        raise ValueError("Q3 original key/shape contract differs")
    old=list(csv.DictReader(raw_cases.decode("utf-8").splitlines()))
    table={}
    for row in old:
        k=f"{row['block']}_c{int(row['context'])}_r{int(row['replicate'])}"
        if k in table:
            raise ValueError("duplicate source case")
        table[k]=row
    if len(table)!=2304 or set(keys)!=set(table):
        raise ValueError("Q3 case key mismatch")
    target=np.asarray([float(table[k]["initial_I"]) for k in keys])[:,None]
    alive=np.isfinite(maximum)
    if not np.all(alive[:,0]):
        raise ValueError("founder states missing")
    if not np.all(np.diff(alive.astype(np.int8),axis=1)<=0):
        raise ValueError("source occupancy resurrection")
    if not np.all(np.diff(maximum,axis=1)[alive[:,1:]]<=1e-12):
        raise ValueError("maximum support increased")
    if not np.all(np.diff(minimum,axis=1)[alive[:,1:]]>=-1e-12):
        raise ValueError("minimum support decreased")
    excluded=alive & (maximum<target-1e-12)
    if not np.all(np.diff(excluded.astype(np.int8),axis=1)>=0):
        raise ValueError("high-I support exclusion reversed while occupied")
    eligible=excluded.any(axis=1)
    t_high=np.where(eligible,np.argmax(excluded,axis=1),-1)
    fixed=alive & (support==1)
    fixed_any=fixed.any(axis=1)
    t_fixed=np.where(fixed_any,np.argmax(fixed,axis=1),-1)
    pre=eligible & ((t_fixed<0)|(t_high<t_fixed))
    at=eligible & (t_high==t_fixed)
    old_low=(alive & (minimum>target-0.05+1e-12)).any(axis=1)
    valid_r=np.nonzero(eligible)[0]
    t_hist=t_high[valid_r]
    pv=np.zeros(2304)
    pv[valid_r]=pvar[valid_r,t_high[valid_r]]
    if int(old_low.sum())!=prior["ever_excluded"]:
        raise ValueError("original low-I count differs")
    if not np.all(t_high[eligible]>=0):
        raise ValueError("first high-loss time missing")
    summary={
        "status":"INDEPENDENT_VECTOR_RECONCILED_FROM_SAVED_ORIGINAL_ARRAYS",
        "original_cases":2304,
        "high_I_support_excluded":int(eligible.sum()),
        "high_I_before_fixation":int(pre.sum()),
        "high_I_at_fixation":int(at.sum()),
        "high_I_after_fixation":int((eligible&(~pre)&(~at)).sum()),
        "high_I_pre_fix_with_positive_expressed_variance":int(np.sum(pre&(pv>1e-12))),
        "high_I_first_time_median":float(np.median(t_hist)),
        "high_I_first_time_q25":float(np.percentile(t_hist,25)),
        "high_I_first_time_q75":float(np.percentile(t_hist,75)),
        "original_low_I_access_exclusions":int(old_low.sum()),
        "high_low_I_overlap":int(np.sum(eligible & old_low)),
        "by_founder":{b:int(np.sum(eligible & np.array([k.startswith(b+"_") for k in keys])))
                      for b in ("main","confirmation")},
        "all_terminal_occupied":bool(np.all(alive[:,-1])),
        "new_biological_histories":0,
        "pollinator_restoration_executed":False,
    }
    if (summary["high_I_support_excluded"]!=1455
        or summary["high_I_before_fixation"]!=758
        or summary["high_I_at_fixation"]!=697
        or summary["high_low_I_overlap"]!=404
        or not summary["all_terminal_occupied"]):
        raise ValueError("independent vector source counts disagree with retrospective readout")
    return summary


def main():
    print("CH3_HIGH_I_INDEPENDENT_VECTOR_JSON="+json.dumps(check(),sort_keys=True))


if __name__=="__main__":
    main()
