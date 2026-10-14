"""Approved fixed Q3 futures. GitHub-only execution; no automatic retries."""
import argparse
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import sys
import time
import traceback
import urllib.request
import zipfile

import numpy as np

from q3_futures_contract_20261014 import (FIELDS, MAX_CALLS, MAX_DISK, Budget, admit, arrays,
    checked_bytes, event_start, load_native, require, restore, seed_for, sha, summarize, write_json)
from verify_q3_futures_paths_20261014 import verify_pair, mean_path


def context(case, out):
    out=Path(out)
    a=arrays(checked_bytes(out/'original'/(case['key']+'.npz'),case['original_npz_sha256']))
    meta=json.loads(str(a['metadata']))
    types,pop,repro,randomness=load_native(out/'frozen_source')
    cfg=types.Config.from_dict(meta['config'])
    campaign=json.loads((out/'campaign.json').read_text())
    opt=campaign['compositions'][meta['task']['composition']]
    visitors=types.VisitorState(np.arange(len(opt),dtype=np.int64),np.asarray(opt),np.full(len(opt),.2),np.ones(len(opt)))
    lo,hi=a['offsets'][case['trigger']:case['trigger']+2]
    state=types.PlantState(**{k:a[k][lo:hi].copy() for k in FIELDS})
    return state,cfg,visitors,(types,pop,repro,randomness)


def produce_pair(case, replicate, out, execution_sha, deadline):
    out=Path(out)
    initial,cfg,visitors,native=context(case,out)
    types,pop,repro,randomness=native
    master=seed_for(case['key'],replicate)
    require(str(master)==case['pair_seeds'][replicate],'registered seed')
    saved={}
    for arm in ('native','restored'):
        state=types.PlantState(**{k:getattr(initial,k).copy() for k in FIELDS})
        if arm=='restored':state=replace(state,alleles=restore(state.alleles))
        empty=pop.subset(state,np.empty(0,dtype=int))
        streams={name:randomness.stream(master,name,0) for name in randomness.STREAM_IDS}
        snapshots=[];parents=[]
        for year in range(case['trigger'],201):
            require(time.monotonic()<deadline and not (out/'ABORT').exists(),'execution deadline/abort')
            snapshots.append({k:getattr(state,k).copy() for k in FIELDS})
            if year==200:break
            state,info=pop.advance(state,repro.reproduce(state,visitors,cfg),empty,cfg,streams,
                                   year=year,mutation_traits=(False,False,True))
            parents.append(info['parentage'].copy())
        record=dict(key=case['key'],replicate=replicate,arm=arm,trigger=case['trigger'],seed=str(master),
                    original_sha256=case['original_npz_sha256'],execution_sha256=execution_sha)
        result={k:np.concatenate([s[k] for s in snapshots],axis=0) for k in FIELDS}
        result.update(offsets=np.r_[0,np.cumsum([len(s['ids']) for s in snapshots])],
                      parent_offsets=np.r_[0,np.cumsum([len(p) for p in parents])],
                      parentage=np.concatenate(parents) if parents else np.empty((0,3),dtype=np.int64),
                      metadata=np.array(json.dumps(record,sort_keys=True)))
        name=f"{case['key']}__r{replicate:02d}__{arm}.npz"
        path=out/'raw'/name
        with path.open('xb') as f:np.savez_compressed(f,**result)
        d=200-case['trigger']
        require(path.stat().st_size<=(d+1)*5664+d*1152+131072,'per-path reserved storage exceeded')
        saved[arm]=dict(name=name,sha256=sha(path.read_bytes()),bytes=path.stat().st_size)
    return saved


def run_pair(case, replicate, out, execution_sha, deadline):
    started=time.monotonic()
    saved=produce_pair(case,replicate,out,execution_sha,deadline)
    result=verify_pair(case,replicate,out,execution_sha,deadline,saved)
    result['production_updates']=2*(200-case['trigger'])
    result['worker_seconds']=time.monotonic()-started
    write_json(Path(out)/'pairs'/f"{case['key']}__r{replicate:02d}.json",result)
    return result


def fixtures(case, out):
    """Four declared native calls, synthetic only; no scientific replicate."""
    _,cfg,vis,native=context(case,out)
    types,pop,repro,randomness=native
    a=types.PlantState(np.full((48,3,2),.5),np.zeros((48,3,2),dtype=np.int64),
                       np.zeros((48,3,2),dtype=bool),np.arange(48,dtype=np.int64),np.zeros(48,dtype=np.int64))
    b=types.PlantState(**{k:getattr(a,k).copy() for k in FIELDS})
    empty=pop.subset(a,np.empty(0,dtype=int))
    left={n:randomness.stream(20261014,n,0) for n in randomness.STREAM_IDS}
    right={n:randomness.stream(20261014,n,0) for n in randomness.STREAM_IDS}
    require(all(left[n] is not right[n] and left[n].bit_generator.state==right[n].bit_generator.state for n in left),'separate identical streams')
    before=json.dumps({n:g.bit_generator.state for n,g in left.items()},sort_keys=True)
    edited=replace(a,alleles=restore(a.alleles))
    require(before==json.dumps({n:g.bit_generator.state for n,g in left.items()},sort_keys=True),'edit consumed RNG')
    for field in ('outcross','maternal','paternal','self_viable'):
        np.testing.assert_array_equal(getattr(repro.reproduce(a,vis,cfg),field),getattr(repro.reproduce(edited,vis,cfg),field))
    x,xi=pop.advance(a,repro.reproduce(a,vis,cfg),empty,cfg,left,year=0,mutation_traits=(False,False,True))
    y,yi=pop.advance(b,repro.reproduce(b,vis,cfg),empty,cfg,right,year=0,mutation_traits=(False,False,True))
    for field in FIELDS:np.testing.assert_array_equal(getattr(x,field),getattr(y,field))
    np.testing.assert_array_equal(xi['parentage'],yi['parentage'])
    for streams in (left,right):
        z,zi=pop.advance(empty,repro.reproduce(empty,vis,cfg),empty,cfg,streams,year=1,mutation_traits=(False,False,True))
        require(not len(z.ids) and zi['parentage'].shape==(0,3),'extinct state continuation')
    write_json(Path(out)/'FIXTURES.json',dict(status='PASS',native_calls=4,scientific_replicates=0,
               native_noop_state_parent_equality=True,restoration_no_draws=True,extinct_continuation=True))


def tree_bytes(path):
    return sum(p.stat().st_size for p in Path(path).rglob('*') if p.is_file())


def authorize(repo):
    require(os.environ.get('GITHUB_ACTIONS')=='true','production runs only on GitHub Actions')
    require(os.environ.get('GITHUB_RUN_ATTEMPT')=='1','automatic biological reruns prohibited')
    require(os.environ.get('GITHUB_REPOSITORY')=='zuizui0223/izu-core','repository gate')
    require(os.environ.get('GITHUB_REF')=='refs/heads/design/chapter2-restoration-conditional-futures-20261014','branch gate')
    raw=(repo/'data/designs/q3_futures_execution_20261014.json').read_bytes()
    execution=json.loads(raw)
    require(execution['approved'] is True and execution['experiment']=='izu-q3-conditional-restoration-v1-20261014','approval gate')
    require(execution['new_trajectories']==7808 and execution['delta']==.01 and execution['max_native_calls']==MAX_CALLS
            and execution['max_worker_seconds']==28800 and execution['max_disk_bytes']==MAX_DISK and execution['workers']==2,'approved limits drift')
    require(platform.python_version()==execution['python']=='3.11.14' and np.__version()==execution['numpy']=='2.2.6','runtime identity')
    for name,digest in execution['code_sha256'].items():checked_bytes(repo/name,digest)
    token=os.environ['GH_TOKEN']
    url='https://api.github.com/repos/zuizui0223/izu-core/actions/workflows/q3-restoration-futures-20261014.yml/runs?per_page=100'
    request=urllib.request.Request(url,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','User-Agent':'izu-q3-admission'})
    with urllib.request.urlopen(request,timeout=60) as response:runs=json.load(response)
    require(runs['total_count']==1 and len(runs['workflow_runs'])==1 and str(runs['workflow_runs'][0]['id'])==os.environ['GITHUB_RUN_ID'],
            'prior execution workflow exists; fresh approval and cumulative budget review required')
    return execution,sha(raw)


def main():
    p=argparse.ArgumentParser()
    for name in ('archive','source-input','out','repo'):p.add_argument('--'+name,type=Path,required=True)
    args=p.parse_args();repo=args.repo.resolve();out=args.out.resolve()
    started=time.monotonic();deadline=started+4*3600-120
    out.mkdir(parents=True,exist_ok=False)
    budget=Budget(out/'BUDGET.json')
    try:
        execution,execution_sha=authorize(repo)
        require(shutil.disk_usage(out).free>=MAX_DISK,'insufficient free disk for approved reservation')
        inventory=admit(args.archive,args.source_input,repo,out)
        cases=inventory['cases']
        (out/'raw').mkdir();(out/'pairs').mkdir()
        write_json(out/'EXECUTION.json',dict(execution_sha256=execution_sha,github_sha=os.environ['GITHUB_SHA'],
                   github_run_id=os.environ['GITHUB_RUN_ID'],execution=execution))
        per_path_bound=sum(2*64*((201-c['trigger'])*5664+(200-c['trigger'])*1152+131072) for c in cases if c['trigger'] is not None)
        # Raw paths, generous 8 KiB pair receipts, metadata and a stored ZIP copy.
        future_bound=per_path_bound+3904*8192+16*1024**2
        require(tree_bytes(out.parent)+2*future_bound<MAX_DISK,'storage reservation exceeds approved ceiling')
        budget.reserve(4,'synthetic_native_noop_and_empty_fixtures')
        fixtures(next(c for c in cases if c['trigger'] is not None),out)
        jobs=iter((c,r) for c in cases if c['trigger'] is not None for r in range(64))
        records=[]
        with ProcessPoolExecutor(max_workers=2) as pool:
            pending={}
            def launch():
                job=next(jobs,None)
                if job is None:return
                c,r=job
                require(time.monotonic()<deadline,'worker time ceiling')
                budget.reserve(4*c['remaining_updates'],f"{c['key']}:{r}:produce_and_one_replay")
                pending[pool.submit(run_pair,c,r,str(out),execution_sha,deadline)]=job
            launch();launch()
            try:
                while pending:
                    done,_=wait(pending,timeout=30,return_when=FIRST_COMPLETED)
                    require(time.monotonic()<deadline,'worker time ceiling')
                    for future in done:
                        pending.pop(future)
                        records.append(future.result())
                        if len(records)%64==0:print(f'verified pairs {len(records)}/3904',flush=True)
                        launch()
            except BaseException:
                (out/'ABORT').write_text('Technical HOLD; no new paths may start.\n')
                for f in pending:f.cancel()
                raise
        require(len(records)==3904,'complete pair coverage')
        require(sum(r['production_updates'] for r in records)==990720 and sum(r['native_updates'] for r in records)==990720,'full replay/update counts')
        # Verify executable bytes again before allowing an inferential readout.
        for name,digest in execution['code_sha256'].items():checked_bytes(repo/name,digest)
        for name,digest in inventory['frozen_source_sha256'].items():checked_bytes(out/'frozen_source'/name.removeprefix('FROZEN_SOURCE/'),digest)
        records.sort(key=lambda r:(r['key'],r['replicate']))
        readout=summarize(records,cases)
        case_summaries=[]
        for case in cases:
            subset=[r for r in records if r['key']==case['key']]
            if subset:
                counts={arm:sum(r[arm+'_event'] is not None for r in subset) for arm in ('native','restored')}
                pre={arm:sum(r[arm+'_event_already_complete'] for r in subset) for arm in ('native','restored')}
                survival={k:sum(r['native_survived']==a and r['restored_survived']==b for r in subset)
                          for k,a,b in [('both_alive',True,True),('native_only',True,False),('restored_only',False,True),('both_extinct',False,False)]}
                case_summaries.append(dict(key=case['key'],block=case['block'],trigger=case['trigger'],pairs=64,event_counts=counts,
                    event_already_complete=pre,survival=survival,conditional_sample_mean_difference=
                    float(np.mean([r['native_I']-r['restored_I'] for r in subset])) if survival['both_alive']==64 else None))
            else:
                original=arrays(checked_bytes(out/'original'/(case['key']+'.npz'),case['original_npz_sha256']))
                means=mean_path(original);event=event_start(means,means[0])
                case_summaries.append(dict(key=case['key'],block=case['block'],trigger=None,pairs=0,policy_zero=True,original_event=event))
        readout['secondary_scope']='Descriptive state-specific event counts; original baseline and full history; no secondary tests.'
        readout['case_summaries']=case_summaries
        readout['execution_sha256']=execution_sha
        write_json(out/'READOUT.json',readout)
        write_json(out/'INDEPENDENT_REPLAY.json',dict(status='ALL_7808_PATHS_REPLAYED_EXACTLY',pairs=len(records),
                   raw_paths=7808,native_updates=990720,state_field_checks=sum(r['state_field_checks'] for r in records),
                   parent_checks=sum(r['parent_checks'] for r in records),execution_sha256=execution_sha,
                   verifier_sha256=execution['code_sha256']['scripts/verify_q3_futures_paths_20261014.py']))
        elapsed=time.monotonic()-started
        require(2*elapsed<28800 and budget.calls<=MAX_CALLS,'aggregate resource ceiling')
        write_json(out/'RESOURCES.json',dict(status='COMPLETE',reserved_calls=budget.calls,actual_calls=1981444,
                   fixture_calls=4,production_calls=990720,replay_calls=990720,workers=2,
                   elapsed_seconds=elapsed,conservative_worker_seconds=2*elapsed,
                   measured_pair_worker_seconds=sum(r['worker_seconds'] for r in records),
                   bytes_before_packaging=tree_bytes(out.parent),max_disk_bytes=MAX_DISK))
        members={str(p.relative_to(out)).replace('\\','/'):sha(p.read_bytes()) for p in sorted(out.rglob('*')) if p.is_file()}
        write_json(out/'MANIFEST.json',members)
        archive=out.parent/'Q3_CONDITIONAL_FUTURES_20261014.zip'
        require(tree_bytes(out.parent)+tree_bytes(out)+16*1024**2<MAX_DISK,'packaging disk ceiling')
        with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_STORED) as z:
            for path in sorted(out.rglob('*')):
                if path.is_file():z.write(path,path.relative_to(out).as_posix())
        with zipfile.ZipFile(archive) as z:
            require(z.testzip() is None,'archive CRC readback')
            require(all(sha(z.read(n))==h for n,h in members.items()),'archive SHA readback')
        require(tree_bytes(out.parent)<MAX_DISK and 2*(time.monotonic()-started)<28800,'final resource ceiling')
        write_json(out.parent/'PUBLICATION_RECEIPT.json',dict(status='COMPLETE_ARCHIVE_READBACK',archive_sha256=sha(archive.read_bytes()),
                   bytes=archive.stat().st_size,members=len(members)+1,incremental_bytes=tree_bytes(out.parent),
                   conservative_worker_seconds=2*(time.monotonic()-started),github_sha=os.environ['GITHUB_SHA'],
                   github_run_id=os.environ['GITHUB_RUN_ID'],readout_sha256=sha((out/'READOUT.json').read_bytes()),
                   execution_sha256=execution_sha))
        print('COMPLETE: all planned paths and independent replays verified; archive readback passed',flush=True)
    except BaseException as exc:
        (out/'ABORT').write_text('Technical HOLD. Do not interpret partial outcomes.\n')
        if not (out/'HOLD.json').exists():
            write_json(out/'HOLD.json',dict(status='TECHNICAL_HOLD',exception=type(exc).__name__,reason=str(exc),
                       reserved_calls=budget.calls,conservative_worker_seconds=2*(time.monotonic()-started)))
        raise


if __name__=='__main__':main()
