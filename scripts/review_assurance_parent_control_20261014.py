"""Independent original-reference and controlled-birth replay, no new producer import."""
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
import argparse
import hashlib
import io
import json
import zipfile
import numpy as np

from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.types import PlantState, Config, VisitorState
from scripts.model3_island.population import advance, subset
from scripts.model3_island.randomness import stream, STREAM_IDS

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ('alleles','allele_origin','mutation_flags','ids','birth_years')
INPUT_SHA = '51a07a843a087059af3d67ad113f5d849644f5b03739a6df986d506bd636648f'
PRIOR_SHA = 'f3045118f51947e9eaa2dd71f275b5bc1428aa2042dd0c2af95bcaa5ca2b14f5'
POLICY = 'A_mean_equal_A_shadow_parents'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def capture_sources():
    path = ROOT/'data/design/assurance_parent_execution_bindings_20261014.json'
    raw = path.read_bytes()
    binding = json.loads(raw)
    if 'scripts/review_assurance_parent_control_20261014.py' not in binding['normalized_source_sha256']:
        raise ValueError('independent reader must be frozen in source bindings')
    snapshot = (raw,binding)
    assert_sources(snapshot)
    return snapshot


def assert_sources(snapshot):
    raw,binding = snapshot
    path = ROOT/'data/design/assurance_parent_execution_bindings_20261014.json'
    if path.read_bytes() != raw:
        raise ValueError('source bindings changed during admission')
    for relative,digest in binding['normalized_source_sha256'].items():
        if sha((ROOT/relative).read_text(encoding='utf-8').encode()) != digest:
            raise ValueError('frozen source differs: '+relative)


def validate_dtypes(data,*,require_weights):
    integer_fields = ('population','offsets','parentage','ids','birth_years','allele_origin')
    if require_weights:
        integer_fields += ('parent_offsets','matrix_offsets')
    if any(data[name].dtype.kind not in 'iu' for name in integer_fields):
        raise ValueError('integer counts and genetic/parent identities required')
    if data['mutation_flags'].dtype.kind != 'b':
        raise ValueError('boolean mutation records required')
    if data['alleles'].dtype.kind != 'f':
        raise ValueError('floating allele records required')


def arrays(raw):
    with np.load(io.BytesIO(raw), allow_pickle=False) as z:
        return {k:z[k].copy() for k in z.files}


def case_key(task):
    return sha(json.dumps(task,sort_keys=True).encode())[:24]


def future_seed(task):
    identity = dict(study='history',block=task['block'],replicate=task['replicate'])
    return int.from_bytes(hashlib.sha256(('resolution-v1-20261011:challenge' +
        json.dumps(identity,sort_keys=True)).encode()).digest()[:16],'big')


def read_inputs(path):
    raw = Path(path).read_bytes()
    if sha(raw) != INPUT_SHA:
        raise ValueError('original input identity differs')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if sorted(z.namelist()) != ['baselines.npz','manifest.json','states.npz']:
            raise ValueError('original input inventory differs')
        manifest = json.loads(z.read('manifest.json'))
        for name,digest in manifest['member_sha256'].items():
            if sha(z.read(name)) != digest:
                raise ValueError('original input member differs')
        states = arrays(z.read('states.npz'))
    for name,digest in manifest['normalized_biology_sha256'].items():
        if sha((ROOT/name).read_text(encoding='utf-8').encode()) != digest:
            raise ValueError('native biological source differs: '+name)
    lookup = {(r['block'],r['replicate'],r['origin']):i for i,r in enumerate(manifest['states'])}
    domain = {(b,r,o) for b in ('main','confirmation') for r in range(512)
              for o in ('A_access_first','I_access_first')}
    if len(lookup) != 2048 or set(lookup) != domain:
        raise ValueError('all2048 initial states required')
    return manifest,states,lookup


def initial_state(states,lookup,task):
    state = PlantState(**{f:states[f][lookup[task['block'],task['replicate'],task['origin']]].copy() for f in FIELDS})
    genes = state.alleles.copy()
    genes[:,2,:] += .5-float(genes[:,2,:].mean())
    if np.any((genes<0)|(genes>1)):
        raise ValueError('mean mapping requires clipping; forbidden')
    return replace(state,alleles=genes)


def independent_sampling(state,visitors,config,policy):
    if policy not in ('native',POLICY):
        raise ValueError('unregistered independent reader policy')
    biological = reproduce_kb(state,visitors,config,background_denominator_capacity=48)
    n = len(state.ids)
    if policy == 'native' or n < 2 or np.all(state.alleles[:,2].mean(1)==state.alleles[0,2].mean()):
        sampled = biological
    else:
        genes = state.alleles.copy()
        values = genes[:,2,:].sum(1)/2
        genes[:,2,:] = values.sum()/n
        shadow = reproduce_kb(replace(state,alleles=genes),visitors,config,background_denominator_capacity=48)
        controlled = []
        for actual,reference in ((biological.outcross,shadow.outcross),
                                 (biological.self_viable,shadow.self_viable)):
            if not np.isfinite(reference).all() or np.any(reference<0):
                raise ValueError('invalid independent shadow class')
            total = float(actual.sum())
            if total == 0:
                weights = np.zeros_like(reference)
            elif reference.sum() <= 0:
                raise ValueError('native-positive class lacks shadow support')
            else:
                weights = reference * (total/float(reference.sum()))
            np.testing.assert_allclose(weights.sum(),total,atol=1e-12,rtol=0)
            controlled.append(weights)
        sampled = SimpleNamespace(outcross=controlled[0],self_viable=controlled[1],ovules=biological.ovules.copy())
    weights = sampled.outcross.copy()
    np.fill_diagonal(weights,sampled.self_viable)
    return biological,sampled,weights


def census(data,t):
    a,b = data['offsets'][t:t+2]
    return PlantState(**{f:data[f][a:b].copy() for f in FIELDS})


def verify_trace(data,initial,visitors,config,seed,policy,*,require_weights):
    validate_dtypes(data,require_weights=require_weights)
    h = 200
    if data['population'].shape != (201,) or data['offsets'].shape != (202,) or data['diagnostics'].shape != (200,11):
        raise ValueError('complete200-update trace required')
    if any(data[f].dtype.kind not in 'iu' for f in ('population','offsets','parentage')):
        raise ValueError('integer census/offset/parentage identities required')
    np.testing.assert_array_equal(np.diff(data['offsets']),data['population'])
    if data['offsets'][0] != 0 or data['offsets'][-1] != len(data['alleles']):
        raise ValueError('complete source census offsets required')
    total = len(data['alleles'])
    for f in FIELDS:
        shape = (total,3,2) if f in FIELDS[:3] else (total,)
        if data[f].shape != shape:
            raise ValueError('complete full-state shape required: '+f)
    if config.survival != 0 or config.seed_arrival.supply != 0:
        raise ValueError('original complete-replacement closed future law required')
    for f in FIELDS:
        np.testing.assert_array_equal(getattr(census(data,0),f),getattr(initial,f))
    parent_offsets = np.r_[0,np.cumsum(data['population'][1:])]
    matrix_offsets = np.r_[0,np.cumsum(data['population'][:-1]**2)]
    if data['parentage'].shape != (int(parent_offsets[-1]),3):
        raise ValueError('complete parentage inventory required')
    if require_weights:
        np.testing.assert_array_equal(data['parent_offsets'],parent_offsets)
        np.testing.assert_array_equal(data['matrix_offsets'],matrix_offsets)
        if (len(data['sampling_weights'])!=matrix_offsets[-1]
                or len(data['native_outcross'])!=matrix_offsets[-1]
                or len(data['native_self_viable'])!=data['offsets'][-2]):
            raise ValueError('complete recorded weighting inventory required')
    streams = {name:stream(seed,name,0) for name in STREAM_IDS}
    empty = subset(initial,np.empty(0,dtype=int))
    max_float_error = 0.
    for t in range(h):
        state = census(data,t)
        biological,sampled,weights = independent_sampling(state,visitors,config,policy)
        if require_weights:
            lo,hi = matrix_offsets[t:t+2]
            np.testing.assert_allclose(data['sampling_weights'][lo:hi],weights.ravel(),atol=1e-12,rtol=0)
            np.testing.assert_allclose(data['native_outcross'][lo:hi],biological.outcross.ravel(),atol=1e-12,rtol=0)
            a,b = data['offsets'][t:t+2]
            np.testing.assert_allclose(data['native_self_viable'][a:b],biological.self_viable,atol=1e-12,rtol=0)
        following,info = advance(state,sampled,empty,config,streams,year=200+t,mutation_traits=(False,True,True))
        observed = census(data,t+1)
        for f in FIELDS:
            if f == 'alleles':
                np.testing.assert_allclose(getattr(following,f),getattr(observed,f),atol=1e-12,rtol=0)
                if len(observed.ids):
                    max_float_error = max(max_float_error,float(np.max(abs(following.alleles-observed.alleles))))
            else:
                np.testing.assert_array_equal(getattr(following,f),getattr(observed,f))
        a,b = parent_offsets[t:t+2]
        np.testing.assert_array_equal(data['parentage'][a:b],info['parentage'])
        diag = np.asarray([biological.maternal.sum(),biological.outcross.sum(),biological.self_raw.sum(),
            biological.self_viable.sum(),biological.ovules.sum(),biological.exported.sum(),biological.delivered.sum(),
            info['resident_potential'],info['resident_recruits'],info['resident_selfed_recruits'],info['resident_outcross_recruits']])
        np.testing.assert_allclose(data['diagnostics'][t,:7],diag[:7],atol=1e-12,rtol=0)
        np.testing.assert_array_equal(data['diagnostics'][t,7:],diag[7:])
    for t in range(201):
        state = census(data,t)
        mean = state.alleles.mean(2).mean(0) if len(state.ids) else np.full(3,np.nan)
        np.testing.assert_allclose(data['means'][t],mean,atol=1e-12,rtol=0,equal_nan=True)
    return h,max_float_error


def admit_references(prior,input_path,reference_root,out):
    raw = Path(prior).read_bytes()
    if sha(raw) != PRIOR_SHA:
        raise ValueError('original reference outer identity differs')
    source_snapshot = capture_sources()
    out = Path(out)
    if out.exists():
        raise FileExistsError('Never overwrite a reference admission')
    manifest,states,lookup = read_inputs(input_path)
    root = Path(reference_root)
    configs = {t:Config.from_dict(manifest['configs'][str(t)]) for t in (1.05,1.5)}
    visitors = VisitorState(np.arange(4),np.full(4,.5),np.full(4,.2),np.ones(4))
    expected = {(b,r,o,t) for b in ('main','confirmation') for r in range(512)
                for o in ('A_access_first','I_access_first') for t in (1.05,1.5)}
    seen = set(); records = []; updates = 0; max_error = 0.
    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        inventory = {f'initial-mean-shard-{j}.zip' for j in range(16)} | {
            'initial-mean-admission.zip','initial-mean-full-readout.zip','INDEPENDENT_RECEIPT.json'}
        if set(outer.namelist()) != inventory or len(outer.namelist()) != 19:
            raise ValueError('complete original provider ZIP inventory required')
        with zipfile.ZipFile(io.BytesIO(outer.read('initial-mean-full-readout.zip'))) as z:
            source_outcomes = arrays(z.read('all_start_outcomes.npz'))
        current_outcomes = arrays((root/'verified/all_start_outcomes.npz').read_bytes())
        if set(source_outcomes) != set(current_outcomes):
            raise ValueError('reference outcome inventory differs')
        for name in source_outcomes:
            np.testing.assert_array_equal(source_outcomes[name],current_outcomes[name])
        for shard in range(16):
            with zipfile.ZipFile(io.BytesIO(outer.read(f'initial-mean-shard-{shard}.zip'))) as z:
                shard_raw = z.read('SHARD.json')
                r = json.loads(shard_raw)
                if (r['status']!='COMPLETE_NATIVE_MEAN_SHARD' or r['cases']!=256 or r['shard']!=shard
                        or r['execution_commit']!='615cd38156b0d0004a9415797ef498791b74257c'
                        or r['input_sha256']!=INPUT_SHA or r['numpy']!='2.2.6'):
                    raise ValueError('original shard source/domain differs')
                folder = root/'shards'/f'initial-mean-shard-{shard}'
                if (folder/'SHARD.json').read_bytes() != shard_raw:
                    raise ValueError('extracted reference manifest differs from immutable outer source')
                for record in r['records']:
                    task = record['task']; key = case_key(task)
                    identity = (task['block'],task['replicate'],task['origin'],task['target'])
                    if identity not in expected or identity in seen or task['policy']!='A_mean_equal_native':
                        raise ValueError('original paired case identity differs')
                    seen.add(identity)
                    body = z.read(key+'.npz')
                    if record['archive'] != key+'.npz' or sha(body)!=record['sha256']:
                        raise ValueError('original case member differs')
                    if (folder/(key+'.npz')).read_bytes() != body:
                        raise ValueError('extracted reference case differs from immutable outer source')
                    data = arrays(body); meta = json.loads(str(data['metadata'].item()))
                    if meta['task']!=task or meta['input_sha256']!=INPUT_SHA or meta['config']!=manifest['configs'][str(task['target'])]:
                        raise ValueError('original case configuration differs')
                    h,error = verify_trace(data,initial_state(states,lookup,task),visitors,configs[task['target']],future_seed(task),'native',require_weights=False)
                    updates += h; max_error = max(max_error,error)
                    index = (('main','confirmation').index(task['block']),task['replicate'],
                             (1.05,1.5).index(task['target']),1,
                             ('A_access_first','I_access_first').index(task['origin']))
                    np.testing.assert_array_equal(source_outcomes['curves'][index],data['population']>0)
                    if bool(source_outcomes['occupied'][index]) != bool(data['population'][-1]):
                        raise ValueError('original outcome arithmetic differs')
                    records.append(dict(task=task,archive=key+'.npz',sha256=sha(body)))
            print('ORIGINAL_REFERENCE_SHARD_ADMITTED',shard,flush=True)
    if seen != expected:
        raise ValueError('all4096 original mean-native cases required')
    value = dict(status='ALL4096_IMMUTABLE_REFERENCE_CASES_AND_NATIVE_BIRTHS_INDEPENDENTLY_ADMITTED',
        cases=len(records),updates=updates,original_outer_sha256=PRIOR_SHA,input_sha256=INPUT_SHA,
        reference_admission_sha256=sha((root/'ADMISSION.json').read_bytes()),
        outcome_npz_sha256=sha((root/'verified/all_start_outcomes.npz').read_bytes()),
        independent_reader_normalized_sha256=sha(Path(__file__).read_text(encoding='utf-8').encode()),
        source_bindings_sha256=sha(source_snapshot[0]),
        max_allele_replay_error=max_error,new_control_producer_imported=False,new_sampler_imported=False,
        new_biological_histories=0,records=records)
    out.parent.mkdir(parents=True,exist_ok=True)
    assert_sources(source_snapshot)
    with out.open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2); f.write('\n')
    return value


def review_shard(path,input_path,execution_commit,archive_sha256,out,*,technical=False):
    raw = Path(path).read_bytes()
    if sha(raw) != archive_sha256:
        raise ValueError('re-downloaded controlled archive identity differs')
    out = Path(out)
    if out.exists():
        raise FileExistsError('Never overwrite an independent shard review')
    source_snapshot = capture_sources()
    binding = source_snapshot[1]
    manifest,states,lookup = read_inputs(input_path)
    configs = {t:Config.from_dict(manifest['configs'][str(t)]) for t in (1.05,1.5)}
    visitors = VisitorState(np.arange(4),np.full(4,.5),np.full(4,.2),np.ones(4))
    records = []; updates = 0; max_error = 0.
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        source = json.loads(z.read('SHARD.json'))
        shard = source['shard']
        if type(shard) is not int or shard not in range(16):
            raise ValueError('registered shard index required')
        expected = {case_key(dict(block=b,replicate=r,origin=o,target=t,policy=POLICY)):
                    dict(block=b,replicate=r,origin=o,target=t,policy=POLICY)
                    for b in ('main','confirmation') for r in range(512)
                    for o in ('A_access_first','I_access_first') for t in (1.05,1.5)
                    if (r==0 if technical else r%16==shard)}
        n = 8 if technical else 256
        status = 'TECHNICAL8_FULL_NATIVE_REPLAY_ADMITTED' if technical else 'COMPLETE_ASSURANCE_SHADOW_PARENT_SHARD'
        if (source['status']!=status or source['cases']!=n or len(source['records'])!=n
                or source['updates']!=n*200 or source['execution_commit']!=execution_commit
                or source['input_sha256']!=INPUT_SHA
                or source['runner_sha256']!=binding['normalized_source_sha256']['scripts/run_assurance_parent_control_20261014.py']
                or source['design_sha256']!=binding['normalized_source_sha256']['scripts/assurance_parent_control_20261014.py']):
            raise ValueError('controlled shard source/domain differs')
        keys = [case_key(r['task']) for r in source['records']]
        if len(set(keys))!=n or set(keys)!=set(expected):
            raise ValueError('complete unique paired shard domain required')
        if set(z.namelist())!={k+'.npz' for k in expected}|{'SHARD.json'} or len(z.namelist())!=n+1:
            raise ValueError('controlled archive inventory differs')
        actual_policy = 'native' if technical else POLICY
        for record in source['records']:
            task = record['task']; key = case_key(task)
            body = z.read(key+'.npz')
            if task!=expected[key] or record['archive']!=key+'.npz' or sha(body)!=record['sha256']:
                raise ValueError('controlled case identity differs')
            data = arrays(body); metadata = json.loads(str(data['metadata'].item()))
            if (metadata['task']!=task or metadata['actual_policy']!=actual_policy or metadata['input_sha256']!=INPUT_SHA
                    or metadata['config']!=manifest['configs'][str(task['target'])]):
                raise ValueError('controlled case configuration differs')
            h,error = verify_trace(data,initial_state(states,lookup,task),visitors,
                                   configs[task['target']],future_seed(task),actual_policy,require_weights=True)
            updates += h; max_error = max(max_error,error)
            if bool(data['population'][-1]) != record['terminal_occupied']:
                raise ValueError('controlled terminal summary differs')
            records.append(dict(task=task,sha256=sha(body),
                terminal_occupied=bool(data['population'][-1]),
                occupancy_curve=(data['population']>0).astype(int).tolist()))
    result = dict(status='NATIVE8_INDEPENDENT_WEIGHT_AND_BIRTH_REPLAY' if technical else 'CONTROLLED256_INDEPENDENT_WEIGHT_AND_BIRTH_REPLAY',
        cases=n,updates=updates,shard=shard,execution_commit=execution_commit,source_archive_sha256=archive_sha256,
        independent_reader_normalized_sha256=sha(Path(__file__).read_text(encoding='utf-8').encode()),
        source_bindings_sha256=sha(source_snapshot[0]),
        max_allele_replay_error=max_error,new_control_producer_imported=False,new_sampler_imported=False,records=records)
    assert_sources(source_snapshot)
    with out.open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2);f.write('\n')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prior',type=Path,required=True)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--references',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a = p.parse_args()
    r = admit_references(a.prior,a.input,a.references,a.out)
    print(json.dumps({k:v for k,v in r.items() if k!='records'},indent=2))
