"""Authenticate immutable independent receipts before starting approved futures."""
import hashlib
import json
from pathlib import Path

PRIOR='f3045118f51947e9eaa2dd71f275b5bc1428aa2042dd0c2af95bcaa5ca2b14f5'
INPUT='51a07a843a087059af3d67ad113f5d849644f5b03739a6df986d506bd636648f'
READER='scripts/review_assurance_parent_control_20261014.py'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def receipt(binding,name,repo_root,label):
    pin=binding.get(name)
    if not pin:
        raise ValueError(label+' required')
    raw=(Path(repo_root)/pin['receipt_relative']).read_bytes()
    if digest(raw)!=pin['receipt_sha256']:
        raise ValueError('independent receipt identity differs')
    return pin,json.loads(raw)


def reference_proof(root,binding,repo_root):
    pin,r=receipt(binding,'reference_admission',repo_root,'independent reference receipt')
    if (r.get('status')!='ALL4096_IMMUTABLE_REFERENCE_CASES_AND_NATIVE_BIRTHS_INDEPENDENTLY_ADMITTED'
        or r.get('cases')!=4096 or r.get('updates')!=819200
        or r.get('new_biological_histories')!=0 or r.get('new_control_producer_imported') is not False
        or r.get('new_sampler_imported') is not False or r.get('original_outer_sha256')!=PRIOR
        or r.get('input_sha256')!=INPUT):
        raise ValueError('complete original reference birth replay required')
    if (r['independent_reader_normalized_sha256']!=binding['normalized_source_sha256'][READER]
        or r['source_bindings_sha256']!=pin['historical_source_bindings_sha256']):
        raise ValueError('independent reference source identity differs')
    root=Path(root)
    if (digest((root/'ADMISSION.json').read_bytes())!=r['reference_admission_sha256']
        or digest((root/'verified/all_start_outcomes.npz').read_bytes())!=r['outcome_npz_sha256']):
        raise ValueError('independently authenticated reference files changed')
    expected={(b,i,o,t) for b in ('main','confirmation') for i in range(512)
              for o in ('A_access_first','I_access_first') for t in (1.05,1.5)}
    seen=set();by_key={}
    for row in r['records']:
        task=row['task'];identity=(task['block'],task['replicate'],task['origin'],task['target'])
        key=digest(json.dumps(task,sort_keys=True).encode())[:24]
        if (identity not in expected or identity in seen or task['policy']!='A_mean_equal_native'
            or row['archive']!=key+'.npz' or len(row['sha256'])!=64):
            raise ValueError('independent reference domain differs')
        seen.add(identity);by_key[key]=row['sha256']
    if seen!=expected or len(by_key)!=4096:
        raise ValueError('complete independent reference domain required')
    return r,by_key


def technical_proof(root,binding,repo_root):
    pin,r=receipt(binding,'technical_admission',repo_root,'independent native control receipt')
    if (r.get('status')!='NATIVE8_INDEPENDENT_WEIGHT_AND_BIRTH_REPLAY'
        or r.get('cases')!=8 or r.get('updates')!=1600
        or r.get('new_control_producer_imported') is not False or r.get('new_sampler_imported') is not False):
        raise ValueError('complete independent native control replay required')
    if (r['source_archive_sha256']!=pin['native_archive_sha256']
        or r['independent_reader_normalized_sha256']!=binding['normalized_source_sha256'][READER]
        or r['source_bindings_sha256']!=pin['historical_source_bindings_sha256']):
        raise ValueError('independent native control source identity differs')
    if root is None:
        raise ValueError('independent native control root required')
    root=Path(root);manifest_raw=(root/'SHARD.json').read_bytes()
    if digest(manifest_raw)!=pin['native_manifest_sha256']:
        raise ValueError('independent native control manifest changed')
    native=json.loads(manifest_raw)
    if native['execution_commit']!=r['execution_commit']:
        raise ValueError('independent native control execution differs')
    expected={digest(json.dumps(t,sort_keys=True).encode())[:24]:t for t in (
        dict(block=b,replicate=0,origin=o,target=t,policy='A_mean_equal_A_shadow_parents')
        for b in ('main','confirmation') for o in ('A_access_first','I_access_first') for t in (1.05,1.5))}
    seen=set()
    for row in r['records']:
        task=row['task'];key=digest(json.dumps(task,sort_keys=True).encode())[:24]
        if key not in expected or key in seen or task!=expected[key]:
            raise ValueError('independent native control domain differs')
        if digest((root/(key+'.npz')).read_bytes())!=row['sha256']:
            raise ValueError('independent native control raw changed')
        seen.add(key)
    if seen!=set(expected):
        raise ValueError('complete independent native control domain required')
    return r
