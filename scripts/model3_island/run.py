"""Execute immutable cases; a verified atomic receipt is the completion gate."""
import argparse
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
import json
import os
import time
import zipfile
import platform
import scipy

import numpy as np
import psutil
from threadpoolctl import threadpool_limits

from .design import canonical,digest,source_hashes,compile_design,ROOT
from .types import Config,PlantState,VisitorState
from .history import make_history,reflect_unit
from .randomness import stream
from .density import make_grid
from .simulate import simulate
from .assays import investment_assay,reference_service
from .population import subset
from .storage import pack_result


def atomic_json(path,value):
    path=Path(path); tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_bytes(canonical(value)); os.replace(tmp,path)


def runtime_identity():
    return {'python':platform.python_version(),'platform':platform.platform(),
            'numpy':np.__version__,'scipy':scipy.__version__,'blas_threads':1}


def verify_snapshot(output,document,*,current_runtime=False):
    output=Path(output)
    try:
        with zipfile.ZipFile(output/'source_snapshot.zip') as archive:
            if set(archive.namelist())!=set(document['source_hashes']):
                raise ValueError('snapshot source set differs')
            for path,h in document['source_hashes'].items():
                if sha256(archive.read(path)).hexdigest()!=h:
                    raise ValueError('snapshot source hash differs')
        runtime=json.loads((output/'runtime.json').read_text())
        if current_runtime and runtime!=runtime_identity():
            raise ValueError('runtime changed; do not mix numerical environments')
    except (OSError,zipfile.BadZipFile,json.JSONDecodeError,KeyError) as exc:
        raise ValueError('missing or corrupt source/runtime snapshot') from exc


def founders_from_spec(spec,seed):
    n=spec['count']; draw_count=spec.get('draw_count',n); rng=stream(seed,'founders',0)
    if n and (draw_count<1 or n%draw_count):
        raise ValueError('founder census must be an integer multiple of the underlying draw')
    alleles=reflect_unit(np.array(spec['means'])[None,:,None]+rng.normal(0,spec['sd'],(draw_count,3,2)))
    if n: alleles=np.tile(alleles,(n//draw_count,1,1))
    # Unique founder gene copies allow descendant ancestry accounting.
    return PlantState(alleles,np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        np.zeros((n,3,2),bool),np.arange(n,dtype=np.int64),np.full(n,spec['birth_year'],dtype=np.int64))


def history_from_spec(config,recipe,seed):
    inherited=None
    if config.island_history=='separation':
        rng=stream(seed,'visitor_arrivals',0); n=config.initial_visitors
        inherited=VisitorState(np.arange(n,dtype=np.int64),rng.uniform(size=n),
            np.full(n,config.visitor_breadth),np.full(n,config.visitor_effectiveness))
    h=make_history(config,seed=seed,inherited_visitors=inherited)
    if 'seed_window' in recipe:
        start,end=recipe['seed_window']
        h=replace(h,seed_candidates=tuple(p if start<=i<end else subset(p,np.empty(0,dtype=int))
                                         for i,p in enumerate(h.seed_candidates)))
    if recipe['kind']=='assembly':
        return h
    pools={}; path=[]
    for segment in recipe['segments']:
        key=segment['pool']; signature=(segment['count'],segment['optimum'],segment['sd'])
        if key in pools and pools[key][0]!=signature:
            raise ValueError('one pool ID cannot describe different visitor states')
        if key not in pools:
            rng=stream(seed,'visitor_arrivals',key); n=segment['count']
            optima=reflect_unit(segment['optimum']+rng.normal(0,segment['sd'],n))
            v=VisitorState(np.arange(n,dtype=np.int64)+key*1000000,optima,
                np.full(n,config.visitor_breadth),np.full(n,config.visitor_effectiveness))
            pools[key]=(signature,v)
        path.extend([pools[key][1]]*segment['years'])
    return replace(h,visitors=tuple(path),initialization='controlled')


def execute_case(case,document,check_budget=None):
    config=Config.from_dict(case['config']); cell=case['cell']
    founders=founders_from_spec(cell['founders'],document['founder_seed'])
    history=history_from_spec(config,cell['history'],case['history_seed'])
    if cell['kind']=='assay':
        return investment_assay(founders,history.visitors[0],config,step=.001)
    demographic_seed=int(np.random.SeedSequence([case['history_seed'],case['demographic_seed']]).generate_state(1)[0])
    result=simulate(config,history,founders,replicate=demographic_seed,grid=make_grid(cell['grid_axes']),check_budget=check_budget,
                    projection_mode=cell['projection_mode'],immigration_mode=cell['immigration_mode'])
    result['reference_service']=reference_service(history.visitors,config)
    # Expected opportunity weights for one initially adult plant, not lineage age.
    result['lifetime_exposure_weights']=config.survival**np.arange(config.years)
    return result


def run_campaign(document,output,*,mode,case_limit=None):
    cases=compile_design(document)
    if mode not in ('pilot','production'):
        raise ValueError('unknown execution mode')
    if mode=='production' and not document['frozen']:
        raise ValueError('production requires a frozen scientific manifest')
    if source_hashes()!=document['source_hashes']:
        raise ValueError('source code differs from the declared immutable hash set')
    cases=[c for c in cases if (c['cohort']=='pilot')==(mode=='pilot')]
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    identity={'manifest_hash':digest(document),'mode':mode}
    manifest_path=output/'manifest.json'
    if manifest_path.exists():
        if canonical(json.loads(manifest_path.read_text()))!=canonical({'identity':identity,'design':document}):
            raise ValueError('output collision: different manifest or execution mode')
    else:
        if any(output.iterdir()):
            raise ValueError('output directory contains unowned files')
        atomic_json(manifest_path,{'identity':identity,'design':document})
        with zipfile.ZipFile(output/'source_snapshot.zip','w',zipfile.ZIP_DEFLATED) as archive:
            for source,h in document['source_hashes'].items():
                data=(ROOT/source).read_bytes()
                if sha256(data).hexdigest()!=h: raise ValueError('source changed during snapshot')
                archive.writestr(source,data)
        atomic_json(output/'runtime.json',runtime_identity())
    verify_snapshot(output,document,current_runtime=True)
    start=time.monotonic(); completed=0; executed=0; stop_reason=None
    limits=document['resource_limits']
    # Completed work counts toward the campaign budget across resumptions.
    used=sum(json.loads(p.read_text()).get('elapsed_seconds',0.) for pattern in ('*/receipt.json','*/interruption.json')
             for p in output.glob(pattern))
    output_bytes=sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
    def check_budget():
        if used+time.monotonic()-start>=limits['runtime_seconds']:
            raise TimeoutError('runtime_budget')
        if psutil.Process().memory_info().rss>limits['memory_mb']*1024**2:
            raise TimeoutError('memory_budget')
        if output_bytes>limits['output_mb']*1024**2:
            raise TimeoutError('output_budget')
        if psutil.disk_usage(str(output)).free<limits['min_free_mb']*1024**2:
            raise TimeoutError('free_disk_budget')
    with threadpool_limits(limits=1):
        for case in cases:
            folder=output/case['case_id']; receipt=folder/'receipt.json'; arrays=folder/'arrays.npz'
            case_hash=digest(case)
            expected={'case_hash':case_hash,**identity}
            if receipt.exists():
                r=json.loads(receipt.read_text())
                if any(r.get(k)!=v for k,v in expected.items()) or not arrays.exists() or r.get('arrays_sha256')!=sha256(arrays.read_bytes()).hexdigest():
                    raise ValueError(f'invalid completion receipt: {case["case_id"]}')
                completed+=1; continue
            if case_limit is not None and executed>=case_limit:
                stop_reason='case_limit'
                break
            try:
                check_budget()
            except TimeoutError as exc:
                stop_reason=str(exc)
                break
            folder.mkdir(exist_ok=True)
            input_path=folder/'input.json'
            if input_path.exists() and canonical(json.loads(input_path.read_text()))!=canonical(case):
                raise ValueError('case input collision')
            atomic_json(input_path,case)
            t=time.monotonic()
            old_bytes=sum(p.stat().st_size for p in folder.iterdir() if p.is_file())
            try:
                result=execute_case(case,document,check_budget)
                check_budget()
            except TimeoutError as exc:
                stop_reason=str(exc)
                interruption=folder/'interruption.json'
                previous=json.loads(interruption.read_text()).get('elapsed_seconds',0.) if interruption.exists() else 0.
                atomic_json(folder/'interruption.json',{'case_hash':case_hash,'reason':stop_reason,
                    'elapsed_seconds':previous+time.monotonic()-t})
                break
            # No object arrays, pickle or non-atomic completion inference.
            with (folder/'arrays.npz.tmp').open('wb') as handle:
                np.savez_compressed(handle,**pack_result(result,document['storage']))
            os.replace(folder/'arrays.npz.tmp',arrays)
            atomic_json(receipt,{**expected,'arrays_sha256':sha256(arrays.read_bytes()).hexdigest(),
                'elapsed_seconds':time.monotonic()-t,'status':'complete'})
            output_bytes+=sum(p.stat().st_size for p in folder.iterdir() if p.is_file())-old_bytes
            completed+=1; executed+=1
    status=dict(expected=len(cases),completed=completed,executed=executed,
                complete=completed==len(cases),manifest_hash=identity['manifest_hash'],stop_reason=stop_reason)
    atomic_json(output/'campaign_status.json',status)
    return status


def main():
    p=argparse.ArgumentParser(); p.add_argument('--design',required=True); p.add_argument('--output',required=True)
    p.add_argument('--mode',choices=['pilot','production'],required=True)
    args=p.parse_args()
    status=run_campaign(json.loads(Path(args.design).read_text(encoding='utf-8')),args.output,mode=args.mode)
    print(json.dumps(status,indent=2))
    if not status['complete']:
        raise SystemExit(2)


if __name__=='__main__':
    main()
