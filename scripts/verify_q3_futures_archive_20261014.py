"""External raw-only readback of the one approved GitHub artifact; no native calls."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import time
import zipfile

import numpy as np

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'))
from q3_futures_contract_20261014 import require
from verify_q3_futures_paths_20261014 import validate_layout,verify_primary


def verify_execution_binding(repo, raw, expected, archived, receipt, preflight_path):
    require(hashlib.sha256(raw).hexdigest()==expected,'approved execution bytes')
    execution=json.loads(raw)
    require(archived['execution']==execution,'archived execution object')
    require(archived['execution_sha256']==receipt['execution_sha256']==expected,'execution digest binding')
    for name in ('github_sha','github_run_id'):
        require(str(archived[name])==str(receipt[name]),'execution run binding')
    preflight=(repo/preflight_path).read_bytes()
    require(hashlib.sha256(preflight).hexdigest()==execution['preflight_sha256'],'preflight identity')
    for name,wanted in execution['code_sha256'].items():
        require(hashlib.sha256((repo/name).read_bytes()).hexdigest()==wanted,'code identity '+name)
    return json.loads(preflight)


def verify_endpoint_binding(record, arm, raw):
    meta=raw['metadata']
    require((meta['key'],meta['replicate'],meta['arm'])==(record['key'],record['replicate'],arm),'pair/raw identity')
    require(type(record[arm+'_survived']) is bool and record[arm+'_survived']==raw['survived'],'pair/raw survival')
    require(record[arm+'_I']==raw['terminal_I'],'pair/raw terminal mean')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--artifact-dir',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    
    started=time.monotonic()
    def unique(name):
        paths=list(args.artifact_dir.rglob(name));require(len(paths)==1,'ambiguous artifact '+name);return paths[0]
    receipt=json.loads(unique('PUBLICATION_RECEIPT.json').read_text())
    require(receipt['status']=='COMPLETE_ARCHIVE_READBACK','publication incomplete')
    require(receipt['github_sha']=='d92ac4324b6e1c8924dcc8e5f30e0750088a3acf' and str(receipt['github_run_id'])=='38508868485','wrong GitHub run')
    require(receipt['execution_sha256']=='54549eeec37a225526883fad4f08ae11a417a87b12adede05346425114d83c93','execution identity')
    def guard():
        require(receipt['conservative_worker_seconds']+time.monotonic()-started<28800,'remaining verification-time ceiling')
    archive=unique('Q3_CONDITIONAL_FUTURES_20261014.zip')
    digest=hashlib.sha256()
    with archive.open('rb') as f:
        while True:
            guard();part=f.read(1024*1024)
            if not part:break
            digest.update(part)
    require(digest.hexdigest()==receipt['archive_sha256'] and archive.stat().st_size==receipt['bytes'],'published archive SHA/length')
    execution_raw=(root/'data/designs/q3_futures_execution_20261014.json').read_bytes()
    with zipfile.ZipFile(archive) as z:
        preflight=verify_execution_binding(root,execution_raw,
            '54549eeec37a225526883fad4f08ae11a417a87b12adede05346425114d83c93',
            json.loads(z.read('EXECUTION.json')),receipt,'data/designs/restoration_futures_preflight_20261014.json')
    cases={c['key']:c for c in preflight['cases']}
    expected={(c['key'],r,arm) for c in cases.values() if c['trigger'] is not None for r in range(64) for arm in ('native','restored')}
    seen=set();field_rows=0;parents=0;censuses=0;records=[];raw_endpoints={}
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();require(len(names)==len(set(names))==receipt['members'],'archive member inventory')
        require('HOLD.json' not in names and 'ABORT' not in names,'technical HOLD artifact')
        manifest=json.loads(z.read('MANIFEST.json'));require(set(names)==set(manifest)|{'MANIFEST.json'},'complete hash manifest')
        for name,wanted in manifest.items():
            guard();h=hashlib.sha256()
            with z.open(name) as f:
                while True:
                    guard();part=f.read(1024*1024)
                    if not part:break
                    h.update(part)
            require(h.hexdigest()==wanted,'member SHA '+name)
            if name.startswith('pairs/') and name.endswith('.json'):
                records.append(json.loads(z.read(name)))
            if name.startswith('raw/') and name.endswith('.npz'):
                with np.load(io.BytesIO(z.read(name)),allow_pickle=False) as f:
                    a={k:f[k] for k in f.files};m=json.loads(str(a['metadata']))
                    key=(m['key'],m['replicate'],m['arm'])
                    require(key in expected and key not in seen,'foreign/duplicate trajectory')
                    seen.add(key);case=cases[m['key']]
                    require(m['seed']==case['pair_seeds'][m['replicate']] and m['trigger']==case['trigger'],'raw seed/trigger')
                    require(m['execution_sha256']==receipt['execution_sha256'] and m['original_sha256']==case['original_npz_sha256'],'raw provenance')
                    validate_layout(a,case['trigger'])
                    field_rows+=len(a['ids']);parents+=len(a['parentage']);censuses+=len(a['offsets'])-1
                    lo,hi=a['offsets'][-2:]
                    raw_endpoints[name]=dict(metadata=m,survived=bool(hi>lo),
                        terminal_I=float(a['alleles'][lo:hi,1].mean()) if hi>lo else None)
        require(seen==expected and len(records)==3904,'all scientific paths/pairs required')
        for r in records:
            for arm in ('native','restored'):
                item=r['artifacts'][arm]
                require(manifest['raw/'+item['name']]==item['sha256'] and z.getinfo('raw/'+item['name']).file_size==item['bytes'],'pair/raw binding')
                verify_endpoint_binding(r,arm,raw_endpoints['raw/'+item['name']])
        readout=json.loads(z.read('READOUT.json'))
        require(hashlib.sha256(z.read('READOUT.json')).hexdigest()==receipt['readout_sha256'],'readout identity')
        verify_primary(readout,records,preflight['cases'])
        replay=json.loads(z.read('INDEPENDENT_REPLAY.json'))
        require(replay['status']=='ALL_7808_PATHS_REPLAYED_EXACTLY' and replay['raw_paths']==7808 and replay['native_updates']==990720,'full independent replay receipt')
        independent=json.loads(z.read('INDEPENDENT_READOUT.json'))
        require(independent['status']=='INDEPENDENT_AGGREGATE_PRIMARY_AND_SECONDARIES_MATCH' and independent['readout_sha256']==receipt['readout_sha256'],'independent aggregate receipt')
        resources=json.loads(z.read('RESOURCES.json'))
        require(resources['actual_calls']==resources['reserved_calls']==1981444 and resources['fixture_calls']==4,'call accounting')
        require(receipt['incremental_bytes']<=17179869184,'remote storage ceiling')
        require(censuses==998528,'scheduled saved census count')
    guard()
    result=dict(status='EXTERNAL_ALL_MEMBERS_RAW_LAYOUT_AND_PRIMARY_READBACK_PASS',github_run_id=receipt['github_run_id'],
        github_sha=receipt['github_sha'],archive_sha256=receipt['archive_sha256'],members=len(manifest)+1,
        scientific_paths=len(seen),pairs=len(records),saved_censuses=censuses,plant_rows=field_rows,parent_rows=parents,
        native_calls_during_external_verification=0,raw_endpoint_receipt_bindings=7808,
        exact_execution_preflight_and_code_verified=True,secondary_events_rederived_externally=False,
        local_verification_seconds=time.monotonic()-started,
        combined_conservative_worker_seconds=receipt['conservative_worker_seconds']+time.monotonic()-started,
        readout_sha256=receipt['readout_sha256'],verifier_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    with args.out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
