"""Approved bounded Actions campaign with immutable per-task checkpoints.

A resumed task is read and replay-verified, never regenerated as a new result.
The original proposal is unchanged; execution authorization is a separate receipt.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile
import time

import numpy as np
import scipy

from scripts.readaptation_contract_20261019 import (
    ROOT,canonical,load_contract,allocation_keys,seed_for,preflight)
from scripts.readaptation_transfer_20261019 import (
    STATE_FIELDS,make_cohort,cohort_digest,destination_states)
from scripts.readaptation_futures_20261019 import run_future
from scripts.readaptation_sources_20261019 import iter_donors
from scripts.readaptation_storage_20261019 import save_future
from scripts.readaptation_runtime_20261019 import resource_gate,ResourceStop
from scripts.readaptation_replay_20261019 import replay_cohort,replay_future
from scripts.audit_readaptation_raw_20261019 import (
    require,load_future,audit_cohort,audit_identity,audit_future,audit_archive)
from scripts.model3_island.types import PlantState,Config
from scripts.model3_island.randomness import STREAM_IDS,stream
from scripts.q3_native_runner_20261019 import configuration,provenance as native_provenance

AUTH=ROOT/'docs/protocols/CHAPTER2_READAPTATION_ACTIONS_AUTHORIZED_20261019.json'


def admit_execution(approval,contract):
    expected=dict(schema='readaptation_actions_authorization_v1',execution_authorized=True,
        contract_sha256=hashlib.sha256(canonical(contract)).hexdigest(),
        future_paths=10240,updates=819200,output_bytes=8*2**30,
        minimum_memory_bytes=2**30,minimum_disk_bytes=10*2**30,
        platform='github_actions',decision='user_explicit_20261019')
    require(canonical(contract)==canonical(load_contract()),'execution design changed')
    require(canonical(approval)==canonical(expected),'execution authorization mismatch')
    return approval


def publish_json(path,value):
    """Publish immutable JSON; equality is required when resuming."""
    path=Path(path); raw=canonical(value)+b'\n'
    require(not path.is_symlink(),'JSON symlink')
    if path.exists():
        require(path.read_bytes()==raw,'existing JSON differs: '+path.name)
        return
    temp=None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent,delete=False,prefix='.receipt-') as f:
            temp=Path(f.name);f.write(raw);f.flush();os.fsync(f.fileno())
        os.link(temp,path)
    finally:
        if temp is not None and temp.exists():temp.unlink()


def checkpoint(path,key,produce,validate):
    path=Path(path); sidecar=path.with_suffix('.json')
    require(not path.is_symlink() and not sidecar.is_symlink(),'checkpoint symlink')
    receipt=json.loads(sidecar.read_text()) if sidecar.exists() else None
    if receipt is not None:
        require(path.is_file(),'receipted checkpoint missing')
    if path.exists():
        require(path.is_file() and path.stat().st_size<=16*2**20,'checkpoint size/type')
        observed=dict(key=list(key),file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size)
        require(receipt is None or receipt==observed,'checkpoint receipt mismatch')
        raw=load_future(path,observed['sha256'],key)
        validate(raw)
        publish_json(sidecar,observed)
        return raw,observed
    raw=produce();validate(raw)
    receipt=save_future(path,key,raw)
    loaded=load_future(path,receipt['sha256'],key)
    validate(loaded)
    publish_json(sidecar,receipt)
    return loaded,receipt


def future_config(contract,destination):
    require(type(destination) is int and 0<=destination<5,'destination')
    base=json.loads((ROOT/'data/design/model3_island_v2.json').read_text())['base_config']
    base.update(capacity=48,years=80,assurance_mode='evolving',assurance_cost=.5,
        assurance_timing='delayed',pollen_discount=0,depression=.5,survival=0,
        mutation_rate=0,ovule_budget=8,activity_mode='fixed',
        activity=0 if destination==0 else float(contract['activity'][(destination-1)//2]))
    base['seed_arrival']['supply']=0;base['visitor_arrival']['supply']=0
    return Config.from_dict(base)


def name_for(prefix,key):
    return prefix+'-'+'-'.join(str(x).replace('.', 'p') for x in key)+'.npz'


def process_cohort(output,donor,donor_key,draw,contract,keys,used):
    """Shared production/technical path; caller admits source and allocation."""
    output=Path(output); (output/'cohorts').mkdir(exist_ok=True)
    key=(*donor_key,draw);seed=seed_for(contract,'cohort',key)
    donor_config=configuration(donor_key[2],8.)
    destinations=list(destination_states(contract).values())
    # The source schedule removed every visitor at t35, before the t80 donor.
    empty=destinations[0]
    def make():
        child,receipt=make_cohort(donor,donor_config,empty,
            {n:stream(seed,n,0) for n in STREAM_IDS},key)
        return dict(**{n:getattr(child,n) for n in STATE_FIELDS},receipt=receipt,stream_key=seed)
    def check(raw):
        require(set(raw)==set(STATE_FIELDS)|{'receipt','stream_key'},'cohort inventory')
        audit_cohort({n:getattr(donor,n) for n in STATE_FIELDS},
                     {n:raw[n] for n in STATE_FIELDS},raw['receipt'])
        replay_cohort(raw,donor,donor_config,empty,contract,key)
    path=output/'cohorts'/name_for('cohort',key)
    resource_gate(output,used)
    prior=path.stat().st_size+path.with_suffix('.json').stat().st_size if path.exists() and path.with_suffix('.json').exists() else (path.stat().st_size if path.exists() else 0)
    raw,receipt=checkpoint(path,key,make,check)
    used+=path.stat().st_size+path.with_suffix('.json').stat().st_size-prior
    cohort=PlantState(**{n:raw[n] for n in STATE_FIELDS});sha=cohort_digest(cohort)
    base=json.loads((ROOT/'data/design/model3_island_v2.json').read_text())['base_config']
    futures=[]
    for future_key in keys:
        require(tuple(future_key[:4])==key,'cohort allocation mismatch')
        resource_gate(output,used)
        config=future_config(contract,future_key[4]); visitors=destinations[future_key[4]]
        def make_future():
            return run_future(cohort,config,visitors,seed_for(contract,'future',future_key),80)
        def check_future(saved):
            audit_identity(saved,future_key,contract,base,sha);audit_future(saved)
            replay_future(saved,cohort,config,visitors,contract,future_key)
        path=output/name_for('future',future_key)
        prior=sum(p.stat().st_size for p in (path,path.with_suffix('.json')) if p.exists())
        record,saved=checkpoint(path,future_key,make_future,check_future)
        del record
        used+=sum(p.stat().st_size for p in (path,path.with_suffix('.json')))-prior
        futures.append(saved)
    return dict(key=list(key),cohort_sha256=sha),receipt,futures,used


def run(output,source,expected_head):
    contract=load_contract();approval=json.loads(AUTH.read_text());admit_execution(approval,contract)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    require(head==expected_head and len(head)==40,'execution commit mismatch')
    subprocess.run(['git','diff','--exit-code','HEAD'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    require(os.environ.get('GITHUB_ACTIONS')=='true','production requires GitHub Actions')
    output=Path(output); output.mkdir(parents=True,exist_ok=True)
    require(not output.is_symlink(),'output symlink')
    require(not any(p.is_symlink() for p in output.rglob('*')),'output contains symlink')
    used=sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
    resource_gate(output,used)
    identity=dict(format='readaptation_run_v1',source=head,contract=contract,authorization=approval,
        python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,native=native_provenance())
    publish_json(output/'RUN.json',identity)
    preflight(contract,check_streams=True)
    keys=list(allocation_keys(contract)); cohorts=[]; cohort_files=[]; futures=[]; seen=set()
    expected_donors={k[:3] for k in keys}; started=time.monotonic()
    for state,receipt in iter_donors(source,contract):
        dk=tuple(receipt['key']); require(dk in expected_donors and dk not in seen,'source donor allocation')
        seen.add(dk); donor=PlantState(**state)
        for draw in range(contract['cohort_draws']):
            chosen=[k for k in keys if k[:4]==(*dk,draw)]
            a,b,c,used=process_cohort(output,donor,dk,draw,contract,chosen,used)
            cohorts.append(a);cohort_files.append(b);futures.extend(c)
            print(json.dumps(dict(cohorts=len(cohorts),futures=len(futures),bytes=used,seconds=time.monotonic()-started)),flush=True)
    require(seen==expected_donors and len(futures)==10240,'incomplete allocation')
    sha=hashlib.sha256(canonical(contract)).hexdigest()
    publish_json(output/'cohorts'/'manifest.json',dict(format='readaptation_cohorts_v1',contract_sha256=sha,files=cohort_files))
    publish_json(output/'manifest.json',dict(format='readaptation_manifest_v1',contract_sha256=sha,cohorts=cohorts,futures=futures))
    resource_gate(output,used)
    summary=audit_archive(output,contract,source_directory=source)
    summary['same_implementation_replay']=dict(cohorts=64,futures=10240,independent_biological_implementation=False)
    publish_json(output/'SUMMARY.json',summary)
    actual=sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
    require(actual<=approval['output_bytes'],'final output budget exceeded')
    publish_json(output/'COMPLETE.json',dict(status='PASS_ADMITTED_AND_REPLAYED',futures=10240,
        summary_sha256=hashlib.sha256((output/'SUMMARY.json').read_bytes()).hexdigest()))


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--expected-head',required=True)
    args=p.parse_args()
    try:run(args.output,args.source,args.expected_head)
    except ResourceStop as error:
        print('RESOURCE_STOP: '+str(error),flush=True);raise SystemExit(75)


if __name__=='__main__':main()
