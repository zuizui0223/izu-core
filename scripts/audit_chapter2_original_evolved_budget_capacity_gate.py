"""Fixed-grid one-step demographic feasibility on ORIGINAL evolved t400 maternal seed means.

Requires the exact 256-row SHA-verified retrospective source JSON. No new
genotype sampling, pollinator histories or stochastic trajectories are run.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import poisson

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_original_evolved_budget_capacity_gate_20261010.json"


def expected_census_occupancy(mu, k=48):
    a=np.asarray(mu,dtype=float)
    if k!=48 or not np.isfinite(a).all() or (a<0).any():
        raise ValueError("unsupported K or invalid expected viable seed")
    nxt=a*poisson.cdf(k-2,a)+k*poisson.sf(k-1,a)
    occ=-np.expm1(-a)
    p_under_k=poisson.cdf(k-1,a)
    return nxt,occ,p_under_k


def audit(original_source:Path):
    contract=json.loads(DESIGN.read_text(encoding="utf-8"))
    scales=contract["budget_scale_grid"]
    if (contract["status"]!="POST_DISCOVERY_DESCRIPTIVE_FIXED_GRID_BEFORE_READOUT"
        or scales != [.025,.05,.125,.25,.5,1.]
        or contract["original_census_K"]!=48
        or contract["original_pollen_background_B"]!=48):
        raise ValueError("outcome-independent budget grid contract changed")
    raw=original_source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=contract["source_raw_sha256"]:
        raise ValueError("source JSON SHA256 not authenticated")
    source=json.loads(raw)
    if len(source["source_rows"])!=256:
        raise ValueError("incomplete original t400 source")
    settings=("delayed_control","prior_selfing","pollen_discount","assurance_cost")
    draws=np.random.default_rng(20261010).integers(0,64,size=(9999,64))
    rows=[]; summaries=[]
    for setting in settings:
        population=sorted((r for r in source["source_rows"]
                           if r["setting"]==setting),key=lambda r:r["history"])
        if len(population)!=64 or len({r["history"] for r in population})!=64:
            raise ValueError("not 64 independent original visitor histories")
        muE=np.array([r["current_seed_mu"] for r in population])
        muC=np.array([r["clamp_seed_mu"] for r in population])
        for b in scales:
            ne,oe,fe=expected_census_occupancy(b*muE)
            nc,oc,fc=expected_census_occupancy(b*muC)
            dN=ne-nc;dO=oe-oc;dMU=b*(muE-muC)
            for i,base in enumerate(population):
                rows.append(dict(setting=setting,history=base["history"],
                   budget_multiplier=b,expected_viable_E=float(b*muE[i]),
                   expected_viable_clamp=float(b*muC[i]),
                   delta_viable=float(dMU[i]),delta_next_N=float(dN[i]),
                   delta_occupancy=float(dO[i]),E_occupancy=float(oe[i]),
                   C_occupancy=float(oc[i]),E_prob_under_K=float(fe[i]),
                   C_prob_under_K=float(fc[i])))
            record=dict(setting=setting,budget_multiplier=b,
                        ovule_budget=b*8,history_blocks=64)
            for name,x in (("delta_viable",dMU),("delta_next_N",dN),
                           ("delta_occupancy",dO)):
                intervals=np.quantile(x[draws].mean(axis=1),[.025,.975])
                record[name]=dict(mean=float(x.mean()),
                    history_bootstrap95_descriptive=[float(v) for v in intervals],
                    positive=int((x>1e-11).sum()),
                    negative=int((x< -1e-11).sum()),
                    near_zero=int((np.abs(x)<=1e-11).sum()))
            record["mean_E_one_step_occupancy"]=float(oe.mean())
            record["mean_C_one_step_occupancy"]=float(oc.mean())
            record["n_E_history_occupancy_in_0p1_0p9"]=int(
                    ((oe>=.1)&(oe<=.9)).sum())
            record["n_both_expected_N_in_0p1K_0p9K"]=int(
                    ((ne>4.8)&(ne<43.2)&(nc>4.8)&(nc<43.2)).sum())
            summaries.append(record)
    if len(rows)!=64*4*6 or len(summaries)!=24:
        raise ValueError("source completeness mismatch")
    return dict(
        status="POST_OUTCOME_EXACT_ONE_STEP_GRID_NOT_SURVIVAL",
        source_sha256=contract["source_raw_sha256"],
        n_original_visitor_histories=64,n_original_nested_repeats_used=1,
        n_new_independent_histories=0,n_raw_cells=len(rows),
        uncertainty="9999 unadjusted descriptive visitor-history bootstrap draws; 4 settings x 6 resource levels, no multipicity correction",
        raw=rows,summary=summaries,
        conclusion="Original K48 seed supply at b=1 is capacity saturated. Resource reduction reveals one-step census differences, but occupancy remains near 1 over grid. Not genetic mediation nor 80-year persistence."
    )


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    result=audit(args.source)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(result["summary"],indent=2))


if __name__=="__main__": main()
