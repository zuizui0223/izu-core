"""Targeted audit of population-scale comparability in the frozen 200-season bridge."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np

from scripts.model3_island.density import make_grid
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.simulate import simulate
from scripts.model3_island.types import Config
from scripts.model3_island_bridge_ops import prepare_arms

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_DESIGN=ROOT/"data/design/chapter2_bridge_population_scale_audit_20261003.json"
DEFAULT_PARENT=ROOT/"data/design/model3_ch2_bridge_execution_20260927.json"

def _change(result, key, popkey):
    x=result[key]
    if not (result[popkey][-1] > 0 and np.isfinite(x[[0,-1],1]).all()):
        return None
    return float(x[-1,1]-x[0,1])

def run_shard(lock,parent,shard_index,shard_count):
    if lock["status"]!="diagnostic_locked_before_population_scale_rerun":
        raise ValueError("locked audit required")
    if parent["status"]!="frozen":
        raise ValueError("frozen bridge required")
    if parent["years"]!=200 or parent["base_config"]["years"]!=200:
        raise ValueError("audit is fixed to the frozen 200-season bridge")
    histories=[int(h) for i,h in enumerate(parent["history_seeds"]) if i % shard_count == shard_index]
    if not histories:
        raise ValueError("empty shard")
    starts=[float(x) for x in parent["starts"]]
    demos=[int(x) for x in parent["demographic_seeds"]]
    grid=make_grid(parent["grid_axes"])
    base=Config.from_dict(parent["base_config"])
    rows=[]
    for hs in histories:
        arms=prepare_arms(base,seed=hs,pool_size=int(parent["pool_size"]))
        for start in starts:
            spec={"count":base.capacity,"draw_count":48,"means":[0.5,start,0.5],"sd":0.15,"birth_year":0}
            founders=founders_from_spec(spec,int(parent["founder_seed"]))
            for arm in ("near","far"):
                cfg,history=arms[arm]
                for ds in demos:
                    replicate=int(np.random.SeedSequence([hs,ds]).generate_state(1)[0])
                    result=simulate(
                        cfg,history,founders,replicate=replicate,grid=grid,
                        projection_mode=parent["projection_mode"]
                    )
                    rows.append({
                        "history_seed":hs,
                        "start_investment":start,
                        "demographic_seed":ds,
                        "arm":arm,
                        "terminal_population":int(result["population"][-1]),
                        "terminal_density_mass":float(result["density_mass"][-1]),
                        "individual_change":_change(result,"trait_mean","population"),
                        "density_change":_change(result,"density_traits","density_mass"),
                    })
    return {
        "status":"complete_bridge_population_scale_audit_shard",
        "shard_index":shard_index,
        "shard_count":shard_count,
        "histories":histories,
        "rows":rows,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--lock",default=str(DEFAULT_DESIGN))
    p.add_argument("--parent",default=str(DEFAULT_PARENT))
    p.add_argument("--shard-index",type=int,required=True)
    p.add_argument("--shard-count",type=int,required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    lock=json.loads(Path(a.lock).read_text())
    parent=json.loads(Path(a.parent).read_text())
    r=run_shard(lock,parent,a.shard_index,a.shard_count)
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({"status":r["status"],"shard":a.shard_index,"rows":len(r["rows"])}))

if __name__=="__main__":
    main()
