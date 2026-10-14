"""Native source replay with a separately recorded counterfactual parent sampler."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np
from scripts import assurance_parent_control_20261014 as design
from scripts import initial_assurance_mean_20261013 as mean
from scripts import persistence_expression_mechanism_20261012 as old
from scripts.run_initial_assurance_mean_20261013 import inputs,original_state,arrays,json_write
from scripts.model3_island.types import Config,VisitorState
from scripts.model3_island.population import advance,subset
from scripts.model3_island.randomness import stream,STREAM_IDS


ROOT=Path(__file__).resolve().parents[1]
SOURCE_BINDINGS=ROOT/'data/design/assurance_parent_execution_bindings_20261014.json'


def source_gate():
    binding=json.loads(SOURCE_BINDINGS.read_bytes())
    if (binding['approved_future_cases']!=4096 or binding['approved_native_controls']!=8
            or binding['human_approval']!='この自殖能力に限定した親選択対照を進める'):
        raise ValueError('assurance parent approval/design differs')
    for relative,digest in binding['normalized_source_sha256'].items():
        if old.digest((ROOT/relative).read_text(encoding='utf-8').encode())!=digest:
            raise ValueError('assurance parent execution source differs: '+relative)
    return binding


def ledger_and_weights(state,visitors,cfg,policy):
    if policy=='native':
        native=old.expression_ledger(state,visitors,cfg,'native');sampled=native
    elif policy==design.POLICY:
        native,sampled,_=design.ledgers(state,visitors,cfg)
    else:
        raise ValueError('unregistered sampler policy')
    p=sampled.outcross.copy();np.fill_diagonal(p,sampled.self_viable)
    return native,sampled,p


def diagnostics(ledger,info):
    return [ledger.maternal.sum(),ledger.outcross.sum(),ledger.self_raw.sum(),ledger.self_viable.sum(),
            ledger.ovules.sum(),ledger.exported.sum(),ledger.delivered.sum(),info['resident_potential'],
            info['resident_recruits'],info['resident_selfed_recruits'],info['resident_outcross_recruits']]


def trajectory(initial,visitors,cfg,seed,policy,*,horizon=200):
    if type(horizon) is not int or horizon<1:raise ValueError('invalid horizon')
    streams={name:stream(seed,name,0) for name in STREAM_IDS};state=initial
    empty=subset(initial,np.empty(0,dtype=int));fields={f:[] for f in old.FIELDS}
    pop=[];means=[];diag=[];parents=[];weights=[];native_o=[];native_s=[]
    offsets=[0];matrix_offsets=[0];parent_offsets=[0]
    for t in range(horizon+1):
        n=len(state.ids);pop.append(n);offsets.append(offsets[-1]+n)
        means.append(state.alleles.mean(axis=(0,2)) if n else np.full(3,np.nan))
        for f in fields:fields[f].append(getattr(state,f).copy())
        if t==horizon:break
        ledger,sampling,p=ledger_and_weights(state,visitors,cfg,policy)
        weights.append(p.ravel());native_o.append(ledger.outcross.ravel());native_s.append(ledger.self_viable)
        matrix_offsets.append(matrix_offsets[-1]+n*n)
        state,info=advance(state,sampling,empty,cfg,streams,year=200+t,mutation_traits=(False,True,True))
        parents.append(info['parentage']);parent_offsets.append(parent_offsets[-1]+len(info['parentage']))
        diag.append(diagnostics(ledger,info))
    result={f:np.concatenate(v) for f,v in fields.items()}
    result.update(population=np.array(pop),offsets=np.array(offsets),means=np.array(means),diagnostics=np.array(diag),
                  parentage=np.concatenate(parents),parent_offsets=np.array(parent_offsets),
                  sampling_weights=np.concatenate(weights),native_outcross=np.concatenate(native_o),
                  native_self_viable=np.concatenate(native_s),matrix_offsets=np.array(matrix_offsets))
    return result


def verify(z,initial,visitors,cfg,seed,policy,*,float_atol=0.):
    if float_atol not in (0.,1e-12):raise ValueError('only frozen zero/local or1e-12/cross-worker float tolerance')
    for f in ('population','offsets','matrix_offsets','parent_offsets','parentage','ids','birth_years','allele_origin'):
        if z[f].dtype.kind not in 'iu':raise ValueError('integer count/identity/offset arrays required')
    for f in ('offsets','matrix_offsets','parent_offsets'):
        if z[f].ndim!=1 or not len(z[f]) or z[f][0]!=0:raise ValueError('zero offset origins required')
    h=len(z['population'])-1
    if h<1 or z['diagnostics'].shape!=(h,11):raise ValueError('invalid complete trace shape')
    if z['population'].shape!=(h+1,) or z['offsets'].shape!=(h+2,) or z['matrix_offsets'].shape!=(h+1,) or z['parent_offsets'].shape!=(h+1,):
        raise ValueError('complete offsets/census inventory required')
    n=int(z['offsets'][-1])
    shapes={'alleles':(n,3,2),'allele_origin':(n,3,2),'mutation_flags':(n,3,2),'ids':(n,),'birth_years':(n,)}
    if any(z[f].shape!=shape for f,shape in shapes.items()):raise ValueError('complete full-state inventory required')
    if (z['parentage'].shape!=(int(z['parent_offsets'][-1]),3)
            or len(z['sampling_weights'])!=z['matrix_offsets'][-1]
            or len(z['native_outcross'])!=z['matrix_offsets'][-1]
            or len(z['native_self_viable'])!=z['offsets'][-2]
            or z['means'].shape!=(h+1,3)):
        raise ValueError('complete ledger/parentage inventory required')
    np.testing.assert_array_equal(np.diff(z['offsets']),z['population'])
    np.testing.assert_array_equal(np.diff(z['matrix_offsets']),z['population'][:-1]**2)
    np.testing.assert_array_equal(np.diff(z['parent_offsets']),z['population'][1:])
    streams={name:stream(seed,name,0) for name in STREAM_IDS};empty=subset(initial,np.empty(0,dtype=int))
    for f in old.FIELDS:np.testing.assert_array_equal(getattr(old.census(z,0),f),getattr(initial,f))
    for t in range(h):
        state=old.census(z,t);native,sampling,p=ledger_and_weights(state,visitors,cfg,policy)
        lo,hi=z['matrix_offsets'][t:t+2]
        np.testing.assert_allclose(z['sampling_weights'][lo:hi],p.ravel(),atol=float_atol,rtol=0)
        np.testing.assert_allclose(z['native_outcross'][lo:hi],native.outcross.ravel(),atol=float_atol,rtol=0)
        a,b=z['offsets'][t:t+2]
        np.testing.assert_allclose(z['native_self_viable'][a:b],native.self_viable,atol=float_atol,rtol=0)
        np.testing.assert_allclose(p.sum(),native.outcross.sum()+native.self_viable.sum(),atol=1e-12,rtol=1e-12)
        following,info=advance(state,sampling,empty,cfg,streams,year=200+t,mutation_traits=(False,True,True))
        saved=old.census(z,t+1)
        for f in old.FIELDS:
            if f=='alleles':np.testing.assert_allclose(getattr(following,f),getattr(saved,f),atol=float_atol,rtol=0)
            else:np.testing.assert_array_equal(getattr(following,f),getattr(saved,f))
        a,b=z['parent_offsets'][t:t+2];np.testing.assert_array_equal(z['parentage'][a:b],info['parentage'])
        expected_diag=np.asarray(diagnostics(native,info))
        np.testing.assert_allclose(z['diagnostics'][t,:7],expected_diag[:7],atol=float_atol,rtol=0)
        np.testing.assert_array_equal(z['diagnostics'][t,7:],expected_diag[7:])
    for t in range(h+1):
        state=old.census(z,t);expected=state.alleles.mean(axis=(0,2)) if len(state.ids) else np.full(3,np.nan)
        np.testing.assert_allclose(z['means'][t],expected,atol=float_atol,rtol=0,equal_nan=True)
    return h


def admit_reference_root(root):
    root=Path(root);r=json.loads((root/'ADMISSION.json').read_bytes())
    if r['status']!='ALL4096_ORIGINAL_MEAN_NATIVE_REFERENCES_ADMITTED' or r['cases']!=4096:
        raise ValueError('full reference admission required')
    if r['prior_sha256']!='f3045118f51947e9eaa2dd71f275b5bc1428aa2042dd0c2af95bcaa5ca2b14f5':
        raise ValueError('original prior identity differs')
    if old.digest((root/'verified/all_start_outcomes.npz').read_bytes())!=r['outcome_npz_sha256']:
        raise ValueError('reference outcomes changed')
    return r


def reference_case(root,task):
    t=dict(task,policy=mean.POLICY);key=old.case_key(t)
    folder=Path(root)/'shards'/f'initial-mean-shard-{old.shard_for(t)}'
    sr=json.loads((folder/'SHARD.json').read_bytes())
    if sr['execution_commit']!='615cd38156b0d0004a9415797ef498791b74257c':raise ValueError('original execution identity')
    rows=[row for row in sr['records'] if row['task']==t]
    if len(rows)!=1 or rows[0]['archive']!=key+'.npz':raise ValueError('original task domain')
    raw=(folder/(key+'.npz')).read_bytes()
    if old.digest(raw)!=rows[0]['sha256']:raise ValueError('original reference case changed')
    return arrays(raw)


def technical_gate(root,m,s,lookup,configs,visitors):
    root=Path(root);tr=json.loads((root/'SHARD.json').read_bytes())
    expected={old.case_key(t):t for t in design.tasks() if t['replicate']==0}
    records=tr.get('records',[]);keys=[old.case_key(r['task']) for r in records]
    if (tr.get('status')!='TECHNICAL8_FULL_NATIVE_REPLAY_ADMITTED' or tr.get('cases')!=8
            or len(keys)!=8 or len(set(keys))!=8 or set(keys)!=set(expected)):
        raise ValueError('complete unique technical8 domain required')
    if tr.get('updates')!=1600:raise ValueError('technical 200-update horizons required')
    source_gate()
    if tr['runner_sha256']!=old.digest(Path(__file__).read_text(encoding='utf-8').encode()):
        raise ValueError('technical assurance-parent runner differs')
    if (tr['design_sha256']!=old.digest(Path(design.__file__).read_text(encoding='utf-8').encode())
            or tr['input_sha256']!=mean.INPUT_SHA):raise ValueError('technical source/input drift')
    for row in records:
        t=row['task'];key=old.case_key(t)
        if t!=expected[key] or row['archive']!=key+'.npz':raise ValueError('technical key mismatch')
        raw=(root/row['archive']).read_bytes()
        if old.digest(raw)!=row['sha256']:raise ValueError('technical raw changed')
        z=arrays(raw)
        if z['population'].shape!=(201,):raise ValueError('technical 200-update horizons required')
        meta=json.loads(str(z['metadata'].item()))
        if meta['task']!=t or meta['actual_policy']!='native' or meta['input_sha256']!=mean.INPUT_SHA or meta['config']!=m['configs'][str(t['target'])]:
            raise ValueError('technical metadata drift')
        assigned,mapping=mean.equalize_mean(original_state(s,lookup[t['block'],t['replicate'],t['origin']]))
        mean.verify_mapping(meta['mapping'],mapping)
        verify(z,assigned,visitors,configs[t['target']],old.future_seed(t),'native',float_atol=1e-12)
    return tr


def run(input_path,reference_root,shard,out,*,technical=False,technical_root=None):
    if type(shard) is not int or shard not in range(16):raise ValueError('invalid shard')
    bindings=source_gate()
    if not technical and not bindings['production_gate_open']:
        raise ValueError('independent controlled reader/review gate must open before production')
    mean.source_gate();admit_reference_root(reference_root)
    m,s,baseline,lookup=inputs(input_path);configs={t:Config.from_dict(m['configs'][str(t)]) for t in old.TARGETS}
    visitors=VisitorState(np.arange(4),np.full(4,.5),np.full(4,.2),np.ones(4))
    if technical:
        if shard!=0:raise ValueError('technical shard0 only')
        selected=[t for t in design.tasks() if t['replicate']==0]
    else:
        if not technical_root:raise ValueError('complete technical gate required')
        technical_gate(technical_root,m,s,lookup,configs,visitors)
        selected=[t for t in design.tasks() if old.shard_for(t)==shard]
    out=Path(out)
    if out.exists():raise ValueError('refuse output overwrite')
    out.mkdir(parents=True);records=[];updates=0
    for task in selected:
        i=lookup[task['block'],task['replicate'],task['origin']]
        assigned,mapping=mean.equalize_mean(original_state(s,i));cfg=configs[task['target']]
        policy='native' if technical else design.POLICY
        trace=trajectory(assigned,visitors,cfg,old.future_seed(task),policy)
        updates+=verify(trace,assigned,visitors,cfg,old.future_seed(task),policy)
        if technical:
            prior=reference_case(reference_root,task)
            for f in old.FIELDS+('population','offsets','means','diagnostics','parentage'):
                if prior[f].dtype.kind=='f':np.testing.assert_allclose(trace[f],prior[f],atol=1e-12,rtol=0,equal_nan=True)
                else:np.testing.assert_array_equal(trace[f],prior[f])
        key=old.case_key(task)
        meta=dict(task=task,input_sha256=mean.INPUT_SHA,config=m['configs'][str(task['target'])],mapping=mapping,actual_policy=policy)
        trace['metadata']=np.array(json.dumps(meta,sort_keys=True))
        np.savez_compressed(out/(key+'.npz'),**trace)
        records.append(dict(task=task,archive=key+'.npz',sha256=old.digest((out/(key+'.npz')).read_bytes()),terminal_occupied=bool(trace['population'][-1])))
    expected_count=8 if technical else 256
    if len(records)!=expected_count:raise ValueError('complete shard domain required')
    result=dict(status='TECHNICAL8_FULL_NATIVE_REPLAY_ADMITTED' if technical else 'COMPLETE_ASSURANCE_SHADOW_PARENT_SHARD',
                cases=len(records),shard=shard,input_sha256=mean.INPUT_SHA,updates=updates,
                runner_sha256=old.digest(Path(__file__).read_text(encoding='utf-8').encode()),
                design_sha256=old.digest(Path(design.__file__).read_text(encoding='utf-8').encode()),
                execution_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),records=records)
    source_gate()
    json_write(out/'SHARD.json',result);return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True);p.add_argument('--references',required=True)
    p.add_argument('--shard',type=int,required=True);p.add_argument('--out',required=True);p.add_argument('--technical',action='store_true');p.add_argument('--technical-root')
    a=p.parse_args();r=run(a.input,a.references,a.shard,a.out,technical=a.technical,technical_root=a.technical_root)
    print(json.dumps({k:v for k,v in r.items() if k!='records'},indent=2))


if __name__=='__main__':main()
