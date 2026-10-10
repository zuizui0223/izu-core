"""Two-factor source Model3 maternal viable-seed partition on original evolved genomes.

Post-discovery source-only one-generation audit, NOT an evolutionary mediation
coefficient or species extinction consequence. Requires four original GitHub
Actions shards with exact authenticated receipts (0,1,2,3).
"""
from __future__ import annotations

import argparse
from pathlib import Path
import json
import hashlib
import numpy as np

from scripts.audit_chapter2_original_evolved_pollen_service import (
    read_design, original_shards, state_from_archive, source_visitors,
    patch_alleles, parity,
)
from scripts.run_chapter2_assurance_generality import (
    config, load_design, DEFAULT_DESIGN,
)
from scripts.model3_island.reproduction import reproduce


def source_viable_seed(ovules, receipt, assurance, cfg):
    """Source algebra for one maternal plant, fixed a and genotype context."""
    O = np.asarray(ovules, dtype=float)
    r = np.asarray(receipt, dtype=float)
    a = np.asarray(assurance, dtype=float)
    if O.shape != r.shape or O.shape != a.shape or np.any(O < 0) or np.any(r < 0):
        raise ValueError("invalid maternal source phenotype vectors")
    if np.any((a < 0) | (a > 1)):
        raise ValueError("invalid assurance capacity")
    q = -np.expm1(-r/(2*cfg.pollen_scale))
    if cfg.assurance_timing == "prior":
        return O*(a*(1-cfg.depression)+(1-a)*q)
    return O*(a*(1-cfg.depression)+(1-a*(1-cfg.depression))*q)


def source_shapley(le, lc, a, cfg):
    """Exact symmetric algebraic decomposition, not causal evolutionary mediation.

    E is original evolved diploid source; C is SAME E diploid source with
    investment locus replaced by original partner fixed-mode population mean.
    Only ovules O and maternal pollen receipt r differ in the one-year ledger.
    """
    Oe, Oc = le.ovules, lc.ovules
    re, rc = le.delivered.sum(axis=0), lc.delivered.sum(axis=0)
    gee = source_viable_seed(Oe,re,a,cfg)
    gcc = source_viable_seed(Oc,rc,a,cfg)
    gec = source_viable_seed(Oe,rc,a,cfg)
    gce = source_viable_seed(Oc,re,a,cfg)
    if not np.allclose(gee,le.maternal,atol=2e-12,rtol=0):
        raise ValueError("E source maternal ledger does not reproduce")
    if not np.allclose(gcc,lc.maternal,atol=2e-12,rtol=0):
        raise ValueError("I-clamp source maternal ledger does not reproduce")
    resource=.5*((gee-gce).sum()+(gec-gcc).sum())
    receipt=.5*((gee-gec).sum()+(gce-gcc).sum())
    net=float(le.maternal.sum()-lc.maternal.sum())
    if not np.isclose(resource+receipt,net,atol=3e-11,rtol=0):
        raise AssertionError("two-factor exact Shapley identity fails")
    return dict(
        ovule_resource_effect=float(resource),
        pollen_receipt_effect=float(receipt),
        group_viable_seed_difference=net,
        delivered_pollen_difference=float(re.sum()-rc.sum()),
    )


def audit(shard_paths):
    d=read_design()
    archives=original_shards(shard_paths,d)
    parity()
    design=load_design(DEFAULT_DESIGN)
    records=[]
    for setting in d["settings"]:
        ce=config(design,setting,.01,"evolving")
        for seed in range(d["history_seed_first"],d["history_seed_last"]+1):
            v=source_visitors(seed,"near")[400]
            e=state_from_archive(archives[1],1,setting,seed,"near","evolving",400)
            f=state_from_archive(archives[0],0,setting,seed,"near","fixed",400)
            target=float(f.alleles[:,1,:].mean())
            clamped=patch_alleles(e,1,target)
            le=reproduce(e,v,ce)
            lc=reproduce(clamped,v,ce)
            a=e.alleles[:,2,:].mean(axis=1)
            x=source_shapley(le,lc,a,ce)
            records.append(dict(setting=setting,history=seed,n_visitor_types=len(v.ids),**x))
    if len(records)!=256:raise ValueError("incomplete original source cells")
    summaries=[]
    for setting in d["settings"]:
        rows=[r for r in records if r["setting"]==setting]
        z=dict(setting=setting,n_original_history_blocks=len(rows),
               n_zero_visitor_histories=sum(x["n_visitor_types"]==0 for x in rows))
        for metric in ("ovule_resource_effect","pollen_receipt_effect",
                       "group_viable_seed_difference","delivered_pollen_difference"):
            a=np.array([x[metric] for x in rows])
            z[metric]=dict(mean=float(a.mean()),
                 positive=int((a>1e-11).sum()),
                 negative=int((a< -1e-11).sum()),
                 zero=int((abs(a)<=1e-11).sum()))
        z["n_receipt_loss_and_resource_gain"]=sum(
           x["pollen_receipt_effect"]< -1e-11 and x["ovule_resource_effect"]>1e-11 for x in rows)
        z["n_resource_more_than_receipt_loss"]=sum(
           x["pollen_receipt_effect"]<0 and
           x["ovule_resource_effect"]> -x["pollen_receipt_effect"] for x in rows)
        summaries.append(z)
    return dict(
        status="POST_OUTCOME_AUTHENTIC_GENOMES_SOURCE_ONLY_EXACT_MATERNAL_SHAPLEY",
        source_reproduction_sha256=d["source_reproduction_sha256"],
        original_artifact_ids=[s["artifact_id"] for s in d["artifact_shards"]],
        original_history_blocks=64,original_nested_repeats_used=1,
        n_new_history_samples=0,n_source_cells=len(records),
        horizon="t400 single reproductive year",
        estimand="original E genome vs same E genome with investment alleles clamped to matched fixed-assurance branch mean; assurance fixed within E",
        decomposition="two-factor symmetric Shapley of ovules O and recipient receipt r in exact maternal viable seed function",
        results=summaries,history_rows=records,
        limits=["Not independent confirmatory experiment","Not a direct/indirect effect of assurance evolution","Not individual paternal genetic fitness","Not occupancy/persistence","Recipient pollen receipt is individual-specific; total delivered volume alone does not identify viable maternal seed","One of original eight demographic repeats per visitor history"],
    )


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--shards",nargs=4,required=True,type=Path)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=audit(a.shards)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps(result["results"],indent=2))


if __name__=="__main__":main()
