"""Freeze/publish gate, then bounded approved I-renewal execution. Never auto-retry."""
import argparse
from dataclasses import asdict
import importlib
import io
import json
import multiprocessing as mp
from pathlib import Path
import sys
import time
import zipfile
import numpy as np
import scipy
from scripts import ecological_I_renewal_20261015 as c
from scripts import ecological_I_renewal_replay_20261015 as consumer

ROOT=Path(__file__).resolve().parents[1]
INPUT_SHA='f0fd126f638e1c6bd130e640ce4491b3bb47aac3da1838359a902776c9a4e037'
ORIGINAL_SHA='819741aa4a9f5bc1aaf2dadddbd56b79d158fc9295d07fc3bffe362693fc056a'
MAX_SECONDS=14400
MAX_BYTES=16*1024**3
MAX_PATH_BYTES=4*1024**2
CTX=None
INIT_ERROR=None


def write(path,obj):
    with Path(path).open('x',encoding='utf8') as f:json.dump(obj,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')


def verify_closure(frozen,root=ROOT):
    if frozen['python']!=sys.version or frozen['numpy']!=np.__version__ or frozen.get('scipy')!=scipy.__version__:raise ValueError('frozen runtime changed')
    for name,digest in frozen['files'].items():
        p=(root/name).resolve()
        if not p.is_relative_to(root.resolve()) or c.digest(p.read_bytes().replace(b'\r\n',b'\n'))!=digest:
            raise ValueError('frozen source changed: '+name)


def verify_original(source):
    root=Path(source['root'])
    for name,h in source['files'].items():
        p=(root/name).resolve()
        if not p.is_relative_to(root.resolve()) or c.digest(p.read_bytes())!=h:raise ValueError('original native source drift: '+name)
    for name,h in source['executable_recipe_files'].items():
        if c.digest((root/'ecological_recipe'/name).read_bytes())!=h:raise ValueError('original recipe drift: '+name)


def native_namespace(root):
    import scripts
    if any(n.startswith('scripts.model3_island') for n in sys.modules):
        raise ValueError('original native source must load in a fresh process')
    scripts.__path__.insert(0,str(Path(root)/'scripts'))


def load_modules(source):
    verify_original(source);native_namespace(source['root'])
    names=['types','population','reproduction','randomness']
    modules=[importlib.import_module('scripts.model3_island.'+n) for n in names]
    for m in modules:
        if not Path(m.__file__).resolve().is_relative_to(Path(source['root']).resolve()):raise ValueError('native import location')
    recipe=Path(source['root'])/'ecological_recipe';sys.path.insert(0,str(recipe))
    imported=importlib.import_module('assurance_causal_inputs')
    if Path(imported.__file__).resolve().parent!=recipe.resolve():raise ValueError('recipe import location')
    return (*modules,imported,source)


def closure():
    paths=['scripts/ecological_I_renewal_20261015.py','scripts/ecological_I_renewal_replay_20261015.py',
           'scripts/run_ecological_I_renewal_20261015.py','scripts/run_ecological_order_boundary_20261013.py',
           'scripts/read_ecological_order_boundary_20261013.py','scripts/audit_genome_response_accounting_20261013.py',
           'tests/test_ecological_I_renewal_20261015.py','docs/ECOLOGICAL_INVESTMENT_RENEWAL_EXECUTION_20261015.md',
           'data/design/ecological_I_renewal_approval_20261015.json','data/design/ecological_I_renewal_technical_restart_20261015.json','scripts/__init__.py']
    return dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,files={p:c.digest((ROOT/p).read_bytes().replace(b'\r\n',b'\n')) for p in paths})


def validate_provider_inventory(names,providers):
    if len(names)!=10 or len(set(names))!=10 or set(names)!=set(providers)|{'PROVIDER_CAPTURE_9.json'}:
        raise ValueError('nine original providers plus authenticated capture sidecar required')


def same_config(native,saved):
    return json.loads(json.dumps(native,allow_nan=False))==saved


def require_restart_approval(a):
    if (a.get('approved') is not True or a.get('prior_reserved_upper_bound')!=1616
            or a.get('combined_update_cap')!=924848 or a.get('new_scientific_paths')!=2304):
        raise ValueError('explicit bounded technical restart approval required')


def freeze(input_zip,original_zip,base):
    restart=json.loads((ROOT/'data/design/ecological_I_renewal_technical_restart_20261015.json').read_text(encoding='utf8'))
    require_restart_approval(restart)
    base=Path(base);base.mkdir(exist_ok=False)
    if c.digest(Path(input_zip).read_bytes())!=INPUT_SHA or c.digest(Path(original_zip).read_bytes())!=ORIGINAL_SHA:raise ValueError('original external input identity')
    if np.__version__!='2.2.6':raise ValueError('original NumPy runtime')
    native_root=base/'original_native_source';native_namespace(native_root)
    modules=c.old.native(input_zip,native_root);c.old.validate_inputs(modules)
    source=modules[-1]
    source['executable_recipe_files']={p.name:c.digest(p.read_bytes()) for p in (native_root/'ecological_recipe').iterdir() if p.is_file()}
    verify_original(source)
    expected=json.loads((ROOT/'data/results/ecological_order_boundary_20261013.json').read_text(encoding='utf8'))
    if expected['execution_commit']!='328548612e93469fcc8663f24548530a57399b9a' or expected['cases']!=2304:raise ValueError('baseline execution identity')
    old_sha=c.digest(Path(c.old.__file__).read_bytes().replace(b'\r\n',b'\n'))
    if old_sha!=expected['producer_sha256']:raise ValueError('old producer source identity')
    originals=base/'originals';originals.mkdir();rows=[]
    with zipfile.ZipFile(original_zip) as outer:
        validate_provider_inventory(outer.namelist(),[r['file'] for r in expected['provider_receipts']])
        capture_sha=c.digest(outer.read('PROVIDER_CAPTURE_9.json'))
        json.loads(outer.read('PROVIDER_CAPTURE_9.json'))
        for provider in expected['provider_receipts']:
            raw=outer.read(provider['file'])
            if len(raw)!=provider['size'] or c.digest(raw)!=provider['sha256']:raise ValueError('original provider identity')
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                m=json.loads(z.read('_COMPLETION.json'))
                if m['cases']!=256 or m['identity']['producer_sha256']!=old_sha:raise ValueError('original shard identity')
                for r in m['records']:
                    t=r['task'];name=c.key(t)+'.npz';b=z.read(name)
                    if c.digest(b)!=r['sha256']:raise ValueError('original2304 path identity')
                    with np.load(io.BytesIO(b),allow_pickle=False) as f:
                        meta=json.loads(str(f['metadata'].item()));d={n:f[n].copy() for n in f.files if n!='metadata'}
                    if meta['task']!=t or meta['seed']!=c.old.seed(t) or meta['mutation_mask']!=list(c.OLD_MASK):raise ValueError('original task/seed/mask')
                    c.old.validate_shapes(d,200)
                    config,state,visitors=c.old.initial(t,modules)
                    if not same_config(asdict(config),meta['config']):raise ValueError('original full configuration')
                    for name2 in c.old.FIELDS:np.testing.assert_array_equal(d[name2][:48],getattr(state,name2))
                    event=c.old.events(d['means'],d['population'])
                    if event!=r['events']['0.05']:raise ValueError('original event labels')
                    with (originals/name).open('xb') as f:f.write(b)
                    rows.append(dict(task=t,sha256=r['sha256'],events=event))
    c.check_inventory([r['task'] for r in rows])
    approval=json.loads((ROOT/'data/design/ecological_I_renewal_approval_20261015.json').read_text(encoding='utf8'))
    if approval['approved'] is not True:raise ValueError('human execution approval')
    # Import the original decision reader before closing the source manifest.
    c.readout(rows,rows)
    frozen=dict(schema='ecological_I_renewal_freeze_v1',closure=closure(),source=source,original_zip_sha256=ORIGINAL_SHA,
        original_input_sha256=INPUT_SHA,provider_capture_sha256=capture_sha,original_dir=str(originals.resolve()),baselines=rows,approval=approval,technical_restart_approval=restart,
        scientific_paths=2304,references=8,replays=2304,fixture_updates=16,scheduled_updates=c.SCHEDULED_UPDATES,
        update_cap=c.UPDATE_CAP,workers=2,seconds_cap=MAX_SECONDS,bytes_cap=MAX_BYTES,no_automatic_retry=True)
    write(base/'EXECUTION_FREEZE.json',frozen)
    with zipfile.ZipFile(base/'EXECUTION_SOURCE.zip','x',compression=zipfile.ZIP_DEFLATED) as z:
        for name in frozen['closure']['files']:z.writestr(name,(ROOT/name).read_bytes().replace(b'\r\n',b'\n'))
        for name in source['files']:z.writestr('original_native/'+name,(native_root/name).read_bytes())
        for name in source['executable_recipe_files']:z.writestr('original_recipe/'+name,(native_root/'ecological_recipe'/name).read_bytes())
        z.writestr('EXECUTION_FREEZE.json',(base/'EXECUTION_FREEZE.json').read_bytes())
    print(json.dumps(dict(status='FROZEN_NO_NATIVE_UPDATES',baselines=len(rows),source_files=len(frozen['closure']['files']),freeze_sha256=c.digest((base/'EXECUTION_FREEZE.json').read_bytes()),source_zip_sha256=c.digest((base/'EXECUTION_SOURCE.zip').read_bytes()))),flush=True)


def initialize(frozen,out,deadline):
    global CTX,INIT_ERROR
    CTX=None;INIT_ERROR=None
    try:
        verify_closure(frozen['closure']);modules=load_modules(frozen['source'])
        CTX=(frozen,Path(out),deadline,modules)
    except Exception as e:INIT_ERROR=repr(e)


def admit_reference(actual,expected):
    required=set(c.old.FIELDS)|{'offsets','means','population','parentage','parent_offsets','returns','sexual_selection'}
    if set(actual)!=required or set(expected)!=required:raise ValueError('complete reference array inventory')
    diagnostic={'returns':1e-10,'sexual_selection':1e-12}
    exact=[];errors={}
    for name in sorted(required):
        if name in diagnostic:
            np.testing.assert_allclose(actual[name],expected[name],atol=diagnostic[name],rtol=0,equal_nan=name=='sexual_selection')
            difference=np.abs(actual[name]-expected[name]);finite=np.isfinite(difference)
            errors[name]=float(np.max(difference[finite])) if finite.any() else 0.
        else:
            np.testing.assert_array_equal(actual[name],expected[name]);exact.append(name)
    return dict(biological_arrays_exact=True,exact_arrays=exact,diagnostic_max_abs=errors,
                original_source_diagnostic_atol=diagnostic,rtol=0)


def work(job):
    if INIT_ERROR:raise ValueError('source admission failed: '+INIT_ERROR)
    frozen,out,deadline,modules=CTX;verify_closure(frozen['closure']);verify_original(frozen['source'])
    if time.time()>=deadline:raise TimeoutError('four-hour cap')
    stage,t=job;name=c.key(t)+'.npz';target=out/('references' if stage=='reference' else 'paths')/name
    original=next(r for r in frozen['baselines'] if r['task']==t)
    raw=(Path(frozen['original_dir'])/name).read_bytes()
    if c.digest(raw)!=original['sha256']:raise ValueError('original case drift')
    if stage=='replay':
        with np.load(io.BytesIO(raw),allow_pickle=False) as z:
            typed=modules[0].PlantState(**{n:z[n][:48].copy() for n in c.old.FIELDS})
        config,_,visitors=c.old.initial(t,modules)
        actual=consumer.replay(t,(config,typed,visitors),modules)
        with np.load(target,allow_pickle=False) as z:
            if json.loads(str(z['metadata'].item()))['task']!=t:raise ValueError('replay task')
            for n,b in actual.items():np.testing.assert_array_equal(b,z[n])
        result=dict(task=t,status='ALL_ARRAYS_REPLAY_EXACT',sha256=c.digest(target.read_bytes()))
    else:
        actual=c.produce(t,modules,renew=stage=='production')
        c.old.validate_shapes(actual,200)
        admission=None
        if stage=='reference':
            with np.load(io.BytesIO(raw),allow_pickle=False) as z:
                admission=admit_reference(actual,{n:z[n].copy() for n in z.files if n!='metadata'})
        config,_,_=c.old.initial(t,modules)
        meta=dict(task=t,stage=stage,seed=c.old.seed(t),config=asdict(config),mutation_mask=list(c.NEW_MASK if stage=='production' else c.OLD_MASK),original_sha256=original['sha256'])
        buf=io.BytesIO();np.savez_compressed(buf,**actual,metadata=np.array(json.dumps(meta,sort_keys=True)));body=buf.getvalue()
        if len(body)>MAX_PATH_BYTES:raise ValueError('predeclared4MiB per-path bound')
        with target.open('xb') as f:f.write(body)
        result=dict(task=t,events=c.old.events(actual['means'],actual['population']),sha256=c.digest(body),reference_admission=admission)
    verify_closure(frozen['closure']);verify_original(frozen['source'])
    if time.time()>=deadline:raise TimeoutError('four-hour cap')
    return result


def contained_output(freeze_path,out):
    base=Path(freeze_path).resolve().parent
    target=Path(out).resolve()
    if target==base or not target.is_relative_to(base):raise ValueError('output storage must be inside frozen study directory')
    return target


def run(freeze_path,expected_sha,out):
    raw=Path(freeze_path).read_bytes()
    if c.digest(raw)!=expected_sha:raise ValueError('published execution freeze identity')
    frozen=json.loads(raw);verify_closure(frozen['closure']);verify_original(frozen['source'])
    require_restart_approval(frozen.get('technical_restart_approval',{}))
    if frozen['approval']['approved'] is not True:raise ValueError('execution approval')
    out=contained_output(freeze_path,out);out.mkdir(exist_ok=False);(out/'paths').mkdir();(out/'references').mkdir()
    (out/'EXECUTION_FREEZE.json').write_bytes(raw)
    start=time.time();deadline=start+MAX_SECONDS;used=0;completed=0
    def reserve(stage,n):
        nonlocal used
        used=c.reserve(used,n);write(out/f'RESERVATION_{stage}.json',dict(reserved=n,total=used))
    def phase(stage,jobs):
        nonlocal completed
        reserve(stage,200*len(jobs));records=[]
        pool=mp.get_context('spawn').Pool(2,initializer=initialize,initargs=(frozen,str(out),deadline))
        try:
            results=pool.imap_unordered(work,[(stage,t) for t in jobs],chunksize=1)
            for _ in jobs:
                r=results.next(timeout=max(.01,deadline-time.time()));records.append(r);completed+=200
                write(out/(stage+'_'+c.key(r['task'])+'.json'),r)
                if len(records)%64==0:print(stage,len(records),'/',len(jobs),flush=True)
                if sum(p.stat().st_size for p in Path(freeze_path).parent.rglob('*') if p.is_file())>MAX_BYTES:raise ValueError('16GiB extra-study cap')
            pool.close();pool.join()
        except BaseException:pool.terminate();pool.join();raise
        verify_closure(frozen['closure']);verify_original(frozen['source'])
        write(out/(stage.upper()+'_COMPLETE.json'),dict(paths=len(records),records=records));return records
    try:
        reserve('fixture',16)
        # Fresh isolated process initializes the original namespace; the main process has no native module imports.
        initialize(frozen,out,deadline)
        if INIT_ERROR:raise ValueError(INIT_ERROR)
        modules=CTX[-1]
        for t in (t for t in c.tasks() if t['block']=='main' and t['replicate']==0 and t['context'] in (0,1)):
            initial=c.old.initial(t,modules);a=c.produce(t,modules,horizon=4);b=consumer.replay(t,initial,modules,horizon=4)
            for n in a:np.testing.assert_array_equal(a[n],b[n])
            completed+=8
        verify_closure(frozen['closure']);verify_original(frozen['source']);write(out/'FIXTURE_COMPLETE.json',dict(updates=16,status='EXACT_TWO_CONTEXTS'))
        ts=list(c.tasks());phase('reference',c.references(ts))
        produced=phase('production',ts);replayed=phase('replay',ts)
        r=c.readout(produced,frozen['baselines'])
        r.update(status='ALL2304_PRODUCTION_AND_INDEPENDENT_REPLAY_VERIFIED',source_freeze_sha256=expected_sha,
                 scientific_paths=2304,references=8,independent_replays=len(replayed),completed_updates=completed,
                 cumulative_reserved_updates=used,elapsed_seconds=time.time()-start)
        if completed!=c.SCHEDULED_UPDATES:raise ValueError('native update accounting')
        verify_closure(frozen['closure']);verify_original(frozen['source'])
        write(out/'READOUT.json',r);write(out/'ALL_START_OUTCOMES.json',produced)
        print('COMPLETE_VERIFIED',completed,'native updates',flush=True)
    except BaseException as e:
        write(out/'TECHNICAL_HOLD.json',dict(error=repr(e),reserved_upper_bound=used,completed_lower_bound=completed,no_automatic_retry=True));raise


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['freeze','run'])
    p.add_argument('--input',type=Path);p.add_argument('--original',type=Path);p.add_argument('--base',type=Path)
    p.add_argument('--freeze',type=Path);p.add_argument('--freeze-sha');p.add_argument('--out',type=Path)
    a=p.parse_args()
    if a.action=='freeze':
        if not all((a.input,a.original,a.base)):p.error('freeze requires input/original/base')
        freeze(a.input,a.original,a.base)
    else:
        if not all((a.freeze,a.freeze_sha,a.out)):p.error('run requires published freeze/freeze-sha/out')
        run(a.freeze,a.freeze_sha,a.out)

if __name__=='__main__':main()
