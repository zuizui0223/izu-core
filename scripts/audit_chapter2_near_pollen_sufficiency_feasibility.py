"""Source-only near pollen sufficiency feasibility, not evolution or preregistration."""
from __future__ import annotations
from dataclasses import replace
import argparse
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.reproduction import reproduce
from scripts.model3_pollen_assay import assay_totals
from scripts.run_model3_assurance_intervention import founders, config
from scripts.run_model3_persistent_isolation import exposure

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_near_pollen_sufficiency_feasibility_20261010.json"


def load_contract():
    d = json.loads(DESIGN.read_text(encoding="utf-8"))
    if (d["status"] != "POST_DISCOVERY_DIAGNOSTIC_NO_EVOLUTIONARY_CONCLUSIONS"
        or d["pollen_budget_multipliers"] != [1, 2, 4, 8, 16]
        or d["source_history_first"] != 76001 or d["source_history_last"] != 76064
        or d["visitor_snapshot"] != 400 or d["arms"] != ["near", "far"]
        or d["setting"] != "assurance_cost"
        or d["prior_fixed_near_raw_deficit"] != 0.39014861544866286):
        raise ValueError("sufficiency feasibility freeze changed")
    return d


def run_all():
    d=load_contract()
    state=founders()
    assert len(state.ids) == 48 and np.all(state.alleles[:,2,:] == .5)
    cfg=config("assurance_cost", .01, "fixed")
    out=[]
    for seed in range(76001,76065):
        for arm in d["arms"]:
            visitors=exposure(seed,arm).visitors[400]
            for multiplier in d["pollen_budget_multipliers"]:
                adjusted=replace(cfg,pollen_budget=cfg.pollen_budget * multiplier)
                led=reproduce(state,visitors,adjusted)
                raw=assay_totals(
                    ovules=led.ovules, outcross=led.outcross.sum(axis=0),
                    capacity=np.full(48,.5),
                    depression=adjusted.depression,timing=adjusted.assurance_timing,
                )
                fraction=float(led.outcross.sum()/led.ovules.sum())
                # In delayed selfing a=.5, raw deficit is after selfing.
                if abs(fraction-(1-2*raw["raw_deficit"])) > 1e-11:
                    raise AssertionError("raw deficit and actual outcross fraction diverged")
                out.append({
                    "visitor_history":seed,"arm":arm,"pollen_budget_multiplier":multiplier,
                    "n_visitors":len(visitors.ids),"outcross_ovule_fraction":fraction,
                    "raw_deficit_after_selfing":raw["raw_deficit"],
                    "viable_deficit_after_selfing":raw["viable_deficit"],
                    "delivered_total":float(led.delivered.sum()),
                })
    assert len(out)==64*2*5
    s=[]
    for arm in d["arms"]:
        for m in d["pollen_budget_multipliers"]:
            rows=[r for r in out if r["arm"]==arm and r["pollen_budget_multiplier"]==m]
            s.append({
                "arm":arm,"multiplier":m,
                "n_histories":len(rows),
                "n_zero_visitor_histories":sum(x["n_visitors"]==0 for x in rows),
                "n_outcross_ge_0p90":sum(x["outcross_ovule_fraction"]>=.90 for x in rows),
                "mean_outcross_fraction":float(np.mean([x["outcross_ovule_fraction"] for x in rows])),
                "mean_raw_deficit":float(np.mean([x["raw_deficit_after_selfing"] for x in rows])),
                "mean_viable_deficit":float(np.mean([x["viable_deficit_after_selfing"] for x in rows])),
                "mean_delivered_pollen":float(np.mean([x["delivered_total"] for x in rows])),
            })
    for arm,expect in (("near",d["prior_fixed_near_raw_deficit"]),("far",d["prior_fixed_far_raw_deficit"])):
        row=next(x for x in s if x["arm"]==arm and x["multiplier"]==1)
        if not np.isclose(row["mean_raw_deficit"],expect,atol=1e-10,rtol=0):
            raise AssertionError(f"{arm} does not reproduce original raw fixed-plant deficit")
    qualified=[x for x in s if x["arm"]=="near"
               and x["mean_outcross_fraction"]>=.90
               and x["n_outcross_ge_0p90"]>=60]
    qualified.sort(key=lambda x:x["multiplier"])
    winner=qualified[0]["multiplier"] if qualified else None
    return {
        "status":"SUFFICIENCY_FEASIBLE_FOR_EVOLUTIONARY_DESIGN" if qualified
                 else "SUFFICIENCY_NOT_REACHED_IN_FROZEN_FEASIBILITY_GRID",
        "source_scope":d["status"],"design":d,
        "source_state":"original fixed N48 a=.5; exposed historical 64 visitor histories",
        "n_independent_new_histories":0,
        "n_source_history_blocks":64,
        "n_rows":len(out),
        "candidate_multiplier":winner,
        "summary_rows":s,"rows":out,
        "scientific_boundaries":[
            "Not evolutionary compression; 0 new independent visitor histories.",
            "Pollen_budget multiplier is supply engineering, not changed visitor replenishment.",
            "Outcross fraction differs from raw deficit; in delayed a=0.5, F/O=1−2d_raw.",
            "Candidate multiplier is a post-outcome calibration; any full evolutionary generality claim must use a separately frozen independent experiment."
        ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    res=run_all()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(res,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":res["status"],"candidate_multiplier":res["candidate_multiplier"],
      "summary_rows":res["summary_rows"]
    },sort_keys=True))


if __name__=="__main__":
    main()
