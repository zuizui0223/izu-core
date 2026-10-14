"""Entire outcome-unselected post-outcome engineering grid for Model3 capacity floor.

Uses fixed synthetic visitors, source genetic founder seed and independent
K/B reproduction only. Every specified budget x horizon is reported. This
is NOT prospective ecological confirmation; no natural populations or 451
A-first/I-first expression histories are involved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts.audit_chapter2_joint_multigen_engineering import run_pilot

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_joint_multigen_occupancy_surface_20261010.json"
STATUS="POST_OUTCOME_ENGINEERING_GRID_EXECUTED_ALL_CELLS"


def run_grid(*,design_path=DESIGN):
    b=Path(design_path).read_bytes()
    d=json.loads(b)
    if (d.get("status")!="POST_OUTCOME_ENGINEERING_GRID_FROZEN_BEFORE_ITS_OWN_EXECUTION_NOT_PREREGISTERED_CONFIRMATION"
            or d["ovule_budgets"]!=[3.,4.5,6.,8.]
            or d["horizons"]!=[40,80]
            or d["replicates_per_synthetic_environment"]!=24
            or d["visitor_conditions"]!=["two_hand_authored","no_visitors"]
            or d["K"]!=[8,48] or d["B"]!=48
            or d["viability_gates"]!=["baseline","half_self","half_outcross"]
            or d["no_new_visitor_histories"] is not True
            or d["no_preregistered_primary_hypothesis_test"] is not True):
        raise ValueError("unrecognized or outcome-modified engineering grid")
    cells=[]
    for ovules in d["ovule_budgets"]:
        for horizon in d["horizons"]:
            run=run_pilot(draws=24,years=horizon,ovule_budget=ovules)
            if run["design"]["independent_ecological_visitor_histories"]!=0:
                raise AssertionError("unexpected ecological visitor histories")
            reports=[]
            for regime in d["visitor_conditions"]:
                r=run["results"][regime]
                for k in (8,48):
                    entry={
                        "regime":regime,
                        "K":k,
                        "occupied_of_24":{gate:r[f"K{k}_{gate}"]["occupied_count"]
                                         for gate in ("baseline","half_self","half_outcross")},
                        "outcross_null_exact": (
                            r["comparisons"][f"K{k}_half_outcross"][
                                "baseline_minus_gate_occupancy"]==0
                            if regime=="no_visitors" else None
                        ),
                    }
                    if regime=="no_visitors" and not entry["outcross_null_exact"]:
                        raise AssertionError("no-visitor outcross negative control failed")
                    reports.append(entry)
            cells.append({
                "ovule_budget":ovules,
                "horizon":horizon,
                "conditions":reports,
            })
    return {
        "status":STATUS,
        "design_sha256":hashlib.sha256(b).hexdigest(),
        "source":"canonical Model3 + fixed B and synthetic engineering fixture",
        "grid_cell_count":len(cells),
        "regime_K_entries":len(cells)*4,
        "independent_ecological_histories":0,
        "demographic_reps_per_condition":24,
        "all_cell_results_including_floor_and_ceiling":cells,
        "scientific_boundary":(
            "Post-outcome complete parameter-grid engineering screen designed"
            " after the budget3 extinction-floor finding. No A-first/I-first,"
            " no true independent ecological histories and no prospective"
            " inferential success. Only diagnoses identifiability windows;"
            " it cannot select an inferential budget after outcomes."
        ),
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    out=run_grid()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
    for cell in out["all_cell_results_including_floor_and_ceiling"]:
        print(json.dumps({
            "ovule_budget":cell["ovule_budget"],
            "horizon":cell["horizon"],
            "counts":cell["conditions"],
        },sort_keys=True))
    print(json.dumps({"status":out["status"],"cells":out["grid_cell_count"],
                      "design_sha256":out["design_sha256"]}))


if __name__=="__main__":
    main()
