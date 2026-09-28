"""Frozen, case-resumable follow-up; no edits to the archived biological operator."""
import argparse,json,time,zipfile,os
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
import numpy as np
import psutil
from threadpoolctl import threadpool_limits
from scripts.model3_island.design import canonical,digest,source_hashes
from scripts.model3_island.run import atomic_json,runtime_identity,founders_from_spec
from scripts.model3_island.types import Config
from scripts.model3_island.density import make_grid,project_state
from scripts.model3_island.simulate import simulate
from scripts.model3_island.storage import pack_result
from scripts.model3_island.audit import validate_arrays
from scripts.model3_island_bridge_ops import prepare_arms


def sources():
    result=source_hashes()
    for name in ('scripts/model3_island_bridge_ops.py','scripts/run_model3_ch2_bridge.py'):
        result[name]=sha256(Path(name).read_bytes()).hexdigest()
    return result


def _run_campaign(d,output,*,budget_used=0.,on_progress=None):
    if d['status']!='frozen' or d['source_hashes']!=sources():raise ValueError('frozen source-bound design required')
    if len(set(d['history_seeds']))!=len(d['history_seeds']) or len(set(d['demographic_seeds']))!=len(d['demographic_seeds']):raise ValueError('duplicate seeds')
    expected=len(d['history_seeds'])*len(d['demographic_seeds'])*len(d['starts'])*len(d['arms'])
    if expected!=d['cases'] or d['years']!=d['base_config']['years']:raise ValueError('case count or horizon differs')
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    mh=digest(d);runtime=runtime_identity();manifest=output/'manifest.json'
    if manifest.exists():
        if json.loads(manifest.read_text())!=d or json.loads((output/'runtime.json').read_text())!=runtime:raise ValueError('output identity/runtime changed')
        with zipfile.ZipFile(output/'sources.zip') as z:
            if set(z.namelist())!=set(d['source_hashes']):raise ValueError('source archive differs')
            for p,h in d['source_hashes'].items():
                if sha256(z.read(p)).hexdigest()!=h:raise ValueError('source archive corrupt')
    else:
        if any(output.iterdir()):raise ValueError('unowned output directory')
        atomic_json(manifest,d);atomic_json(output/'runtime.json',runtime)
        with zipfile.ZipFile(output/'sources.zip','w',zipfile.ZIP_DEFLATED) as z:
            for p in d['source_hashes']:z.writestr(p,Path(p).read_bytes())
    started=time.monotonic();used=budget_used
    size=sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
    limits=d['resource_limits'];completed=executed=0;stop=None
    def check():
        if on_progress is not None:on_progress()
        if used+time.monotonic()-started>=limits['runtime_seconds']:raise TimeoutError('runtime_budget')
        if psutil.Process().memory_info().rss>limits['memory_mb']*1024**2:raise TimeoutError('memory_budget')
        if size>limits['output_mb']*1024**2:raise TimeoutError('output_budget')
        if psutil.disk_usage(str(output)).free<limits['min_free_mb']*1024**2:raise TimeoutError('disk_budget')
    grid=make_grid(d['grid_axes'])
    with threadpool_limits(limits=1):
        for hs in d['history_seeds']:
            arms=prepare_arms(Config.from_dict(d['base_config']),seed=hs,pool_size=d['pool_size'])
            for initial in d['starts']:
                for name in d['arms']:
                    cfg,history=arms[name]
                    spec={'count':cfg.capacity,'draw_count':48,'means':[.5,initial,.5],'sd':.15,'birth_year':0}
                    founders=founders_from_spec(spec,d['founder_seed'])
                    if d.get('initial_projection_axes') is not None:founders,_=project_state(founders,make_grid(d['initial_projection_axes']))
                    for ds in d['demographic_seeds']:
                        case_id=f'{name}-s{int(round(initial*10))}-h{hs}-d{ds}'
                        case={'id':case_id,'config':asdict(cfg),'history_seed':hs,'demographic_seed':ds,'cell':{'kind':'trajectory','founders':spec},'manifest_hash':mh}
                        folder=output/case_id;receipt=folder/'receipt.json';arrays=folder/'arrays.npz';ch=digest(case)
                        if receipt.exists():
                            r=json.loads(receipt.read_text())
                            if r.get('status')!='complete' or r['case_hash']!=ch or r['manifest_hash']!=mh or canonical(json.loads((folder/'input.json').read_text()))!=canonical(case) or sha256(arrays.read_bytes()).hexdigest()!=r['arrays_sha256']:raise ValueError('corrupt or different completed case')
                            completed+=1;continue
                        folder.mkdir(exist_ok=True);old_size=sum(p.stat().st_size for p in folder.iterdir());atomic_json(folder/'input.json',case);t=time.monotonic()
                        try:
                            check();seed=int(np.random.SeedSequence([hs,ds]).generate_state(1)[0])
                            result=simulate(cfg,history,founders,replicate=seed,grid=grid,projection_mode=d['projection_mode'],check_budget=check)
                            packed=pack_result(result,{'density_counts':'checkpoints_and_replay_digest','checkpoint_every':50})
                            validate_arrays(packed,case);check()
                            with (folder/'arrays.tmp').open('wb') as f:np.savez_compressed(f,**packed)
                            size+=sum(p.stat().st_size for p in folder.iterdir())-old_size
                            old_size=sum(p.stat().st_size for p in folder.iterdir())
                            check()
                            os.replace(folder/'arrays.tmp',arrays)
                            atomic_json(receipt,{'status':'complete','manifest_hash':mh,'case_hash':ch,'arrays_sha256':sha256(arrays.read_bytes()).hexdigest(),'elapsed_seconds':time.monotonic()-t})
                        except TimeoutError as exc:
                            stop=str(exc); prior=json.loads((folder/'interruption.json').read_text()) if (folder/'interruption.json').exists() else {'elapsed_seconds':0.,'attempts':[]}
                            elapsed=time.monotonic()-t
                            atomic_json(folder/'interruption.json',{'elapsed_seconds':prior['elapsed_seconds']+elapsed,'reason':stop,'attempts':prior.get('attempts',[])+[{'elapsed_seconds':elapsed,'reason':stop}]})
                            status={'complete':False,'completed':completed,'expected':expected,'executed':executed,'manifest_hash':mh,'stop_reason':stop};atomic_json(output/'campaign_status.json',status);return status
                        completed+=1;executed+=1;size+=sum(p.stat().st_size for p in folder.iterdir())-old_size
            atomic_json(output/'progress.json',{'completed':completed,'expected':expected,'last_history':hs,'manifest_hash':mh})
    try:check()
    except TimeoutError as exc:stop=str(exc)
    status={'complete':completed==expected and stop is None,'completed':completed,'expected':expected,'executed':executed,'manifest_hash':mh,'stop_reason':stop}
    atomic_json(output/'campaign_status.json',status);return status



def run_campaign(d,output):
    if d['status']!='frozen' or d['source_hashes']!=sources():raise ValueError('frozen source-bound design required')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    path=output.with_name(output.name+'.attempts.json')
    mh=digest(d)
    if not path.exists() and output.exists() and any(output.iterdir()):raise ValueError('missing attempt ledger for existing campaign')
    book=json.loads(path.read_text()) if path.exists() else {'manifest_hash':mh,'attempts':[]}
    if book['manifest_hash']!=mh or any(not a.get('closed') for a in book['attempts']):
        raise ValueError('different manifest or unclosed attempt; refuse an unaccounted budget reset')
    used=sum(a['elapsed_seconds'] for a in book['attempts']);started=time.monotonic();last=started
    item={'closed':False,'elapsed_seconds':0.,'pid':os.getpid(),'start_unix':time.time()}
    book['attempts'].append(item);atomic_json(path,book)
    def progress():
        nonlocal last
        now=time.monotonic()
        if now-last>=30:
            item['elapsed_seconds']=now-started;atomic_json(path,book);last=now
    try:
        return _run_campaign(d,output,budget_used=used,on_progress=progress)
    finally:
        item.update(closed=True,elapsed_seconds=time.monotonic()-started)
        atomic_json(path,book)


def main():
    p=argparse.ArgumentParser();p.add_argument('--design',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    r=run_campaign(json.loads(Path(a.design).read_text()),a.output);print(json.dumps(r))
    if not r['complete']:raise SystemExit(2)

if __name__=='__main__':main()
