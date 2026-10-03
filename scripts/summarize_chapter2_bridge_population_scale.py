"""Summarize the frozen bridge population-scale audit."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np

def _stats(x):
    a=np.asarray(x,dtype=float)
    return {
        "n":int(len(a)),
        "mean":float(a.mean()),
        "median":float(np.median(a)),
        "min":float(a.min()),
        "q10":float(np.quantile(a,.10)),
        "q90":float(np.quantile(a,.90)),
        "max":float(a.max()),
    }

def summarize(lock,folder):
    files=sorted(Path(folder).glob("population-scale-shard-*.json"))
    if not files: raise ValueError("no audit shards")
    rows=[]
    seen=set()
    for p in files:
        d=json.loads(p.read_text())
        if d["status"]!="complete_bridge_population_scale_audit_shard":
            raise ValueError(f"incomplete shard {p}")
        for r in d["rows"]:
            key=(r["history_seed"],r["start_investment"],r["demographic_seed"],r["arm"])
            if key in seen: raise ValueError(f"duplicate row {key}")
            seen.add(key); rows.append(r)
    if len(rows)!=int(lock["scope"]["expected_finite_trajectories"]):
        raise ValueError(f"expected {lock['scope']['expected_finite_trajectories']} rows, got {len(rows)}")

    arm_reports={}
    for arm in ("near","far"):
        rr=[r for r in rows if r["arm"]==arm]
        pop=np.array([r["terminal_population"] for r in rr],float)
        mass=np.array([r["terminal_density_mass"] for r in rr],float)
        arm_reports[arm]={
            "finite_population":_stats(pop),
            "finite_occupancy":float(np.mean(pop>0)),
            "finite_at_capacity_fraction":float(np.mean(pop==48)),
            "density_mass":_stats(mass),
            "density_mass_below_1_fraction":float(np.mean(mass<1)),
            "density_mass_below_0_01_fraction":float(np.mean(mass<.01)),
        }

    # Compare finite replicate mean population with the deterministic mass at the
    # same arm/history/start. Density must be identical across demographic reps.
    paired=[]
    for arm in ("near","far"):
        for hs in sorted({r["history_seed"] for r in rows}):
            for start in sorted({r["start_investment"] for r in rows}):
                cell=[r for r in rows if r["arm"]==arm and r["history_seed"]==hs and r["start_investment"]==start]
                masses=np.array([r["terminal_density_mass"] for r in cell],float)
                if not np.allclose(masses,masses[0],rtol=0,atol=1e-12):
                    raise ValueError(f"density depends on demographic seed: {arm}/{hs}/{start}")
                finite_mean=float(np.mean([r["terminal_population"] for r in cell]))
                mass=float(masses[0])
                paired.append({
                    "arm":arm,"history_seed":hs,"start_investment":start,
                    "finite_mean_population":finite_mean,
                    "density_mass":mass,
                    "finite_to_density_ratio":None if mass<=0 else float(finite_mean/mass),
                    "all_finite_occupied":bool(all(r["terminal_population"]>0 for r in cell)),
                })

    # Reproduce the previously reported far-minus-near trait effects.
    starts=sorted({r["start_investment"] for r in rows})
    histories=sorted({r["history_seed"] for r in rows})
    demos=sorted({r["demographic_seed"] for r in rows})
    lookup={(r["arm"],r["start_investment"],r["history_seed"],r["demographic_seed"]):r for r in rows}
    ind=[]; den=[]
    for s in starts:
        for h in histories:
            for d in demos:
                n=lookup["near",s,h,d]; f=lookup["far",s,h,d]
                if n["individual_change"] is not None and f["individual_change"] is not None:
                    ind.append(f["individual_change"]-n["individual_change"])
                if n["density_change"] is not None and f["density_change"] is not None:
                    den.append(f["density_change"]-n["density_change"])
    individual_mean=float(np.mean(ind)); density_mean=float(np.mean(den))
    if abs(individual_mean-(-0.1446))>.002:
        raise ValueError(f"finite headline not reproduced: {individual_mean}")
    if abs(density_mean-(-0.4510))>.002:
        raise ValueError(f"density headline not reproduced: {density_mean}")

    far_pairs=[x for x in paired if x["arm"]=="far"]
    finite_means=np.array([x["finite_mean_population"] for x in far_pairs],float)
    masses=np.array([x["density_mass"] for x in far_pairs],float)
    ratios=np.array([x["finite_to_density_ratio"] for x in far_pairs if x["finite_to_density_ratio"] is not None],float)
    discrepancy={
        "n_history_start_cells":len(far_pairs),
        "all_finite_replicates_occupied_fraction":float(np.mean([x["all_finite_occupied"] for x in far_pairs])),
        "finite_mean_population":_stats(finite_means),
        "density_mass":_stats(masses),
        "finite_to_density_ratio":_stats(ratios),
        "cells_density_below_1_but_all_finite_occupied_fraction":float(np.mean([
            x["density_mass"]<1 and x["all_finite_occupied"] for x in far_pairs
        ])),
    }
    strong=bool(
        arm_reports["far"]["finite_occupancy"]==1.0
        and arm_reports["far"]["density_mass"]["median"]<1
        and discrepancy["finite_mean_population"]["median"]>=1
    )
    return {
        "schema_version":"1.0",
        "status":"complete_bridge_population_scale_audit",
        "rows_checked":len(rows),
        "headline_reproduction":{
            "finite_mean_far_minus_near":individual_mean,
            "density_mean_far_minus_near":density_mean,
        },
        "arm_reports":arm_reports,
        "far_same_cell_comparison":discrepancy,
        "strong_population_scale_disagreement":strong,
        "interpretation":(
            "The deterministic closure is not on the finite-ABM population scale in the far arm; "
            "ABM-versus-density trait differences and movement toward density with larger capacity "
            "must not be interpreted as a pure finite-population attenuation/convergence-to-expectation result."
            if strong else
            "No order-of-magnitude population-scale discrepancy was detected under the frozen rule."
        ),
        "claim_boundary":lock["claim_boundary"],
        "source_shards":[p.name for p in files],
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--lock",required=True)
    p.add_argument("--input-dir",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    lock=json.loads(Path(a.lock).read_text())
    result=summarize(lock,Path(a.input_dir))
    Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))

if __name__=="__main__":
    main()
