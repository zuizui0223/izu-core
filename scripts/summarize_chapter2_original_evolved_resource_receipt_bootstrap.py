"""Exploratory history-cluster descriptive intervals for source Shapley audit.

These are NOT new independent histories, prospective inference or multiplicity
adjusted p-values. Reuses old 64 visitor histories, first demographic repeat.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

SOURCE_SHA="6fdd8ed45af9f7b9c65b513cb20fa1f3ba224519695ec37940421a7a6d60ae5e"
SETTINGS=("delayed_control","prior_selfing","pollen_discount","assurance_cost")
METRICS=("shapley_ovule_resource","shapley_pollen_receipt",
         "net_evolved_minus_clamp_viable_seed","delivered_pollen_e_minus_clamp")


def summarize(raw_path:Path):
    raw=raw_path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA:
        raise ValueError("raw 256-row result must match original authenticated audit")
    data=json.loads(raw)
    if (data["status"]!="POST_DISCOVERY_ORIGINAL_E_GENOME_STATIC_SHAPLEY_NOT_EVOLUTION_OR_SURVIVAL"
            or len(data["source_rows"])!=256):
        raise ValueError("source audit incomplete")
    seeds=sorted({r["history"] for r in data["source_rows"]})
    if len(seeds)!=64:raise ValueError("wrong number of visitor history clusters")
    rng=np.random.default_rng(20261010)
    sample=rng.integers(0,64,size=(9999,64))
    results=[]
    for setting in SETTINGS:
        rows={r["history"]:r for r in data["source_rows"] if r["setting"]==setting}
        if len(rows)!=64 or set(rows)!=set(seeds):
            raise ValueError("one setting has missing visitor histories")
        d=dict(setting=setting,original_history_clusters=64,intervals={})
        for key in METRICS:
            x=np.array([rows[s][key] for s in seeds],dtype=float)
            interval=np.quantile(x[sample].mean(axis=1),[.025,.975])
            d["intervals"][key]={
               "mean":float(x.mean()),
               "history_bootstrap_percentile95":[float(v) for v in interval]}
        results.append(d)
    return dict(
        status="POST_OUTCOME_DESCRIPTIVE_UNADJUSTED_HISTORY_BOOTSTRAP",
        source_raw_sha256=SOURCE_SHA,source_history_count=64,
        nested_demographic_repeats_used=1,draws=9999,seed=20261010,
        unit="visitor-history cluster, common bootstrap indices across four settings",
        scope="descriptive exploratory confidence intervals; no preregistration/multiplicity correction, no new biological simulations",
        results=results,
    )


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-json",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    d=summarize(a.source_json)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(d,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(d["results"],indent=2))


if __name__=="__main__":main()
