"""Replay one prespecified frozen pair and verify lossless trajectory capture."""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import numpy as np
from scripts.run_model3_joint_syndrome_finite_followup import BRIDGE,JOINT,DESIGN,save_trajectory
from scripts.model3_island.types import Config
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.density import make_grid
from scripts.model3_island.simulate import simulate
from scripts.model3_island_bridge_ops import prepare_arms

def run(reference, output):
    reference=json.loads(Path(reference).read_text())
    design=json.loads(DESIGN.read_text())
    bridge=json.loads(BRIDGE.read_text())
    joint=json.loads(JOINT.read_text())
    setting=reference["setting"]
    start=next(x for x in design["initial_states"] if x["id"]=="central")
    seed=bridge["history_seeds"][0];ds=design["demographic_seeds"][0]
    ref=next(r for r in reference["records"] if r["initial_state"]["id"]=="central")
    pair=next(h for h in ref["histories"] if h["history_seed"]==seed)["per_repeat"]
    pair=next(p for p in pair if p["demographic_seed"]==ds)
    founders=founders_from_spec(dict(design["founders"],means=[start[k] for k in ("access","investment","assurance")]),bridge["founder_seed"])
    base=Config.from_dict(bridge["base_config"])
    arms=prepare_arms(base,seed=seed,pool_size=bridge["pool_size"])
    grid=make_grid(design["grid_axes"]);rows=[]
    patch=joint["settings"][setting]
    for arm in ("near","far"):
        cfg,hist=arms[arm]
        cfg=replace(cfg,assurance_mode="evolving",assurance_timing=patch["assurance_timing"],pollen_discount=patch["pollen_discount"],assurance_cost=patch["assurance_cost"],mutation_rate=design["mutation_rate"],years=design["years"],seed_arrival=replace(cfg.seed_arrival,supply=design["seed_arrival_supply"]))
        replicate=int(np.random.SeedSequence([seed,ds]).generate_state(1)[0])
        result=simulate(cfg,hist,founders,replicate=replicate,grid=grid,projection_mode=design["projection_mode"])
        target=Path(output)/f"{setting}_{seed}_{arm}_{ds}.npz"
        receipt=save_trajectory(result,target)
        with np.load(target) as stored:
            for key in stored.files:
                np.testing.assert_array_equal(stored[key],result[key])
        observed=result["trait_mean"][-1,1:]
        expected=np.array([pair[arm+"_investment"],pair[arm+"_assurance"]])
        np.testing.assert_allclose(observed,expected,atol=1e-12,rtol=0)
        rows.append(dict(arm=arm,endpoint=observed.tolist(),stored=receipt))
    return dict(status="passed",history=seed,demographic_seed=ds,setting=setting,cases=2,rows=rows,scope="capture and exact frozen endpoint replay, not a time-scale adequacy test")

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("reference");p.add_argument("output");a=p.parse_args()
    r=run(a.reference,a.output);Path(a.output,"receipt.json").write_text(json.dumps(r,indent=2));print(json.dumps(r))
