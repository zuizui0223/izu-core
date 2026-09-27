"""Outcome-blind runtime/state audit for the candidate Ch2 bridge experiment."""
import json,time,argparse,zipfile,io
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
import numpy as np
import psutil
from threadpoolctl import threadpool_limits
from scripts.model3_island.types import Config
from scripts.model3_island_bridge_ops import prepare_arms
from scripts.model3_island.run import founders_from_spec,atomic_json,runtime_identity
from scripts.model3_island.simulate import simulate
from scripts.model3_island.density import make_grid,project_state
from scripts.run_model3_ch2_bridge import sources
from scripts.model3_island.storage import pack_result
from scripts.model3_island.audit import validate_arrays


def main():
    p=argparse.ArgumentParser();p.add_argument('--design',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    path=Path(a.design);d=json.loads(path.read_text());out=Path(a.output)
    if out.exists():raise ValueError('preserve existing pilot; no silent rerun')
    hashes=sources();hashes['scripts/pilot_model3_ch2_bridge.py']=sha256(Path(__file__).read_bytes()).hexdigest()
    with zipfile.ZipFile(out.with_suffix('.sources.zip'),'w',zipfile.ZIP_DEFLATED) as z:
        for f in hashes:z.writestr(f,Path(f).read_bytes())
    arms=prepare_arms(Config.from_dict(d['base_config']),seed=d['pilot_seed'],pool_size=d['pool_size'])
    rows=[];start=time.monotonic();peak=0
    def check():
        nonlocal peak
        peak=max(peak,psutil.Process().memory_info().rss)
        if peak>3072*1024**2 or time.monotonic()-start>1800:raise TimeoutError('pilot resource limit')
    with threadpool_limits(limits=1):
        for initial in d['starts']:
            for name,(cfg,history) in arms.items():
                t=time.monotonic();spec={'count':cfg.capacity,'draw_count':48,'means':[.5,initial,.5],'sd':.15,'birth_year':0}
                founders=founders_from_spec(spec,d['founder_seed'])
                if d.get('initial_projection_axes') is not None:founders,_=project_state(founders,make_grid(d['initial_projection_axes']))
                seed=int(np.random.SeedSequence([d['pilot_seed'],d['demographic_seeds'][0]]).generate_state(1)[0])
                r=simulate(cfg,history,founders,replicate=seed,grid=make_grid(d['grid_axes']),projection_mode='continuous',check_budget=check)
                packed=pack_result(r,{'density_counts':'checkpoints_and_replay_digest','checkpoint_every':50})
                validate_arrays(packed,{'config':asdict(cfg),'cell':{'kind':'trajectory','founders':spec}})
                buffer=io.BytesIO();np.savez_compressed(buffer,**packed)
                rows.append({'arm':name,'start':initial,'elapsed_seconds':time.monotonic()-t,'state_audit':'passed','compressed_bytes':buffer.tell()})
                atomic_json(out,{'status':'running_resource_only','completed':len(rows),'expected':len(d['starts'])*len(arms),'rows':rows})
    atomic_json(out,{'status':'complete_resource_only','candidate_sha256':sha256(path.read_bytes()).hexdigest(),'rows':rows,'completed':len(rows),'source_hashes':hashes,'source_archive_sha256':sha256(out.with_suffix('.sources.zip').read_bytes()).hexdigest(),'projected_output_bytes':sum(r['compressed_bytes'] for r in rows)*len(d['history_seeds'])*len(d['demographic_seeds']),'peak_memory_mb':peak/1024**2,'projected_production_seconds':sum(r['elapsed_seconds'] for r in rows)*len(d['history_seeds'])*len(d['demographic_seeds']),'runtime':runtime_identity(),'scientific_outcomes_inspected':False})
    print(json.dumps({'status':'complete_resource_only','cases':len(rows),'projected_seconds':sum(r['elapsed_seconds'] for r in rows)*len(d['history_seeds'])*len(d['demographic_seeds']),'peak_memory_mb':peak/1024**2}))

if __name__=='__main__':main()
