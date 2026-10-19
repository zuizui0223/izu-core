"""Authorized source-bound160 adapter; original technical cap remains unchanged."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import numpy as np
from scripts import q3_native_runner_20261019 as n
from scripts import q3_release160_20261019 as release

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT/'docs/protocols/CHAPTER2_CONFIRM160_EXECUTION_20261019.json'
EPS = (0., .005, .01, .02, .05)


def plan(technical=False):
    if technical:
        return n.technical_plan()
    p = release.candidate()
    return dict(schema='q3_production160_v1', mode='confirmation',
        namespace=p['seed_registry']['namespace'],
        founders=p['seed_registry']['founders'], visitors=p['seed_registry']['visitors'],
        policies=p['design']['policies'], budgets=p['design']['budgets'],
        fork=35, end=80, capacity=48, margin=.10, confirmation_authorized=True)


def provenance():
    release.snapshot_sources()
    release.load_oc()
    return dict(native=n.provenance(), adapter=n.digest(Path(__file__).read_bytes()),
                protocol=n.digest(PROTOCOL.read_bytes()))


def initialize(root, technical=False, shard=0):
    root = Path(root)
    p = plan(technical)
    count = 1 if technical else 32
    if type(shard) is not int or not 0 <= shard < count:
        raise ValueError('invalid shard')
    authorization = json.loads(PROTOCOL.read_text(encoding='utf8'))
    if not authorization['execution_authorized']:
        raise ValueError('execution not authorized')
    if not technical and shutil.disk_usage(root.parent).free < authorization['minimum_worker_free_bytes']:
        raise ValueError('worker storage admission failed')
    info = dict(plan=p, technical=technical, shard=shard, shards=count, provenance=provenance())
    info['contract_sha256'] = n.digest(n.canonical(info))
    root.mkdir(parents=True, exist_ok=False)
    (root/'states').mkdir()
    (root/'RUN.json').write_bytes(n.canonical(info)+b'\n')
    return info


def contract(root):
    info = json.loads((Path(root)/'RUN.json').read_bytes())
    return validate_contract(info)


def validate_contract(info):
    raw = {k:v for k,v in info.items() if k != 'contract_sha256'}
    if (info['contract_sha256'] != n.digest(n.canonical(raw))
        or type(info['technical']) is not bool
        or type(info['shard']) is not int or type(info['shards']) is not int
        or info['plan'] != plan(info['technical']) or info['provenance'] != provenance()
        or info['shards'] != (1 if info['technical'] else 32)
        or not 0 <= info['shard'] < info['shards']):
        raise ValueError('contract/source/runtime mismatch')
    return info


def cells(c):
    p = c['plan']
    return [(f,v) for i,f in enumerate(p['founders']) for j,v in enumerate(p['visitors'])
            if (i*len(p['visitors'])+j) % c['shards'] == c['shard']]


def run(root, max_updates=None):
    """Same native transition and snapshot helpers; shard-local atomic restart."""
    root = Path(root); c = contract(root); p = c['plan']; used = 0
    if max_updates is not None and (type(max_updates) is not int or max_updates < 1):
        raise ValueError('positive update limit required')
    lock = root/'RUN.lock'
    fd = os.open(lock, os.O_CREAT|os.O_EXCL|os.O_WRONLY, 0o600); os.close(fd)
    try:
        for spec in n.tasks(p, cells(c)):
            path = n.task_path(root, spec)
            seed = n.master(p, spec['founder'], spec['visitor'],
                            'prefix' if spec['stage']=='prefix' else 'fork')
            rng = n.rngs(seed)
            if path.exists():
                meta, arrays = n.read_snapshot(path, c['contract_sha256'])
                if meta['task'] != spec or meta['master'] != seed:
                    raise ValueError('checkpoint assignment mismatch')
                if meta['current'] == spec['end']:
                    continue
                if not spec['start'] <= meta['current'] < spec['end']:
                    raise ValueError('invalid checkpoint year')
                states = [n.state_at(arrays,t) for t in range(len(arrays['counts']))]
                for key in rng:
                    rng[key].bit_generator.state = meta['rng'][key]
            else:
                parent = None
                if spec['stage'] == 'prefix':
                    state = n.founder(spec['founder'])
                else:
                    prefix = dict(spec, stage='prefix', budget=8., start=0, end=35)
                    pm, pa = n.read_snapshot(n.task_path(root,prefix), c['contract_sha256'])
                    if pm['current'] != 35:
                        raise ValueError('incomplete prefix')
                    state = n.state_at(pa,-1); parent = pm['payload_sha256']
                states = [state]
                meta = dict(task=spec, current=spec['start'], master=seed,
                    contract_sha256=c['contract_sha256'], parent_payload_sha256=parent,
                    target_I=float(n.founder(spec['founder']).alleles[:,1,:].mean()))
            cfg = n.configuration(spec['policy'],spec['budget'])
            full, sparse, none = n.visitors(spec['visitor'])
            for t in range(meta['current'],spec['end']):
                state = states[-1]; visitors = full if t<5 else sparse if t<35 else none
                child,_ = n.advance(state,n.reproduce(state,visitors,cfg),n.empty(state),
                                    cfg,rng,year=t,mutation_traits=(False,False,False))
                states.append(child); meta['current']=t+1; used+=1
                stop = max_updates is not None and used>=max_updates
                if stop or (t+1)%10==0 or t+1==spec['end']:
                    meta['rng']={k:g.bit_generator.state for k,g in rng.items()}
                    n.save_snapshot(path,meta,states)
                if stop:
                    return dict(new_updates=used,complete=False)
        return dict(new_updates=used,complete=True)
    finally:
        lock.unlink()


def seal(root):
    """Validate all raw states one crossing at a time; do not load full study."""
    root=Path(root); c=contract(root); p=c['plan']; chosen=cells(c)
    specs=n.tasks(p,chosen)
    if {x.name for x in (root/'states').iterdir()} != {n.task_path(root,s).name for s in specs}:
        raise ValueError('incomplete/unexpected shard inventory')
    records=[]; inventory={}; slots=0
    for f,v in chosen:
        initial=n.founder(f); origin=initial.alleles.ravel(); target=float(initial.alleles[:,1,:].mean())
        loaded={}; arm=[]
        for spec in n.tasks(p,[(f,v)]):
            path=n.task_path(root,spec); m,a=n.read_snapshot(path,c['contract_sha256'])
            if (m['task']!=spec or m['current']!=spec['end'] or m['target_I']!=target
                or m['master']!=n.master(p,f,v,'prefix' if spec['stage']=='prefix' else 'fork')):
                raise ValueError('incomplete/misassigned task')
            states=[n.state_at(a,t) for t in range(len(a['counts']))]
            for i,state in enumerate(states):
                year=spec['start']+i; origins=state.allele_origin
                if (np.any(origins<0) or np.any(origins>=288) or np.any(state.mutation_flags)
                    or np.any(state.birth_years!=year)
                    or not np.array_equal(state.ids,np.arange(year*48,year*48+len(state.ids)))
                    or not np.array_equal(state.alleles,origin[origins])):
                    raise ValueError('invalid native genotype/identity')
                if i:
                    for loc in range(3):
                        if not set(state.allele_origin[:,loc,:].ravel()) <= set(states[i-1].allele_origin[:,loc,:].ravel()):
                            raise ValueError('new inherited origin')
            if spec['stage']=='prefix':
                ancestor=initial
                if m['parent_payload_sha256'] is not None: raise ValueError('prefix has parent')
            else:
                pm,pre=loaded[spec['policy'],'prefix']; ancestor=pre[-1]
                if m['parent_payload_sha256']!=pm['payload_sha256']: raise ValueError('fork ancestry')
            for key in n.FIELDS:
                if not np.array_equal(getattr(states[0],key),getattr(ancestor,key)):
                    raise ValueError('founder/fork mismatch')
            loaded[spec['policy'],spec['stage']]=(m,states)
            inventory[path.name]=dict(sha256=n.digest(path.read_bytes()),payload=m['payload_sha256'])
            slots+=len(states)
        for policy in p['policies']:
            for stage in ('B8','B4p5'):
                _,pre=loaded[policy,'prefix']; _,future=loaded[policy,stage]
                seq=pre+future[1:]
                upper=[float(s.alleles[:,1,:].max()) if len(s.ids) else None for s in seq]
                lower=[float(s.alleles[:,2,:].min()) if len(s.ids) else None for s in seq]
                ev=[n.events(upper,target-eps) for eps in EPS]
                alive=upper[-1] is not None
                arm.append(dict(policy=policy,stage=stage,alive=alive,
                    genetic_first=[x['G_first'] for x in ev],
                    extinction_first=[x['E_first'] for x in ev],
                    first_loss=[x['first_G'] for x in ev],
                    final_access=[bool(alive and upper[-1]>=target-eps-1e-12) for eps in EPS],
                    max_I=upper,min_A=lower))
        records.append(dict(founder=f,visitor=v,target_I=target,arms=arm))
    result=dict(contract=c,records=records,inventory=inventory,saved_states=slots,
                unique_updates=250*len(chosen),complete=True)
    result['seal_sha256']=n.digest(n.canonical(result))
    return result


def aggregate(seals, technical=False):
    p=plan(technical); count=1 if technical else 32
    seen=set(); shard_seen=set(); refs=[]; records=[]
    for s in seals:
        raw={k:v for k,v in s.items() if k!='seal_sha256'}
        if s.get('seal_sha256')!=n.digest(n.canonical(raw)):
            raise ValueError('seal checksum mismatch')
        c=validate_contract(s['contract'])
        if c['plan']!=p or c['technical']!=technical or c['provenance']!=provenance():
            raise ValueError('mixed source/runtime/plan')
        if c['shard'] in shard_seen: raise ValueError('duplicate shard')
        shard_seen.add(c['shard']); expected=set(cells(c))
        keys={(r['founder'],r['visitor']) for r in s['records']}
        if (keys!=expected or len(keys)!=len(s['records']) or len(s['inventory'])!=6*len(keys)
            or s['saved_states']!=256*len(keys) or s['unique_updates']!=250*len(keys)
            or not s['complete'] or seen & keys):
            raise ValueError('incomplete/duplicate crossing inventory')
        seen |= keys; records.extend(s['records']); refs.append(s['seal_sha256'])
    if shard_seen!=set(range(count)) or len(seen)!=len(p['founders'])*len(p['visitors']):
        raise ValueError('missing shards/crossings')
    shape=(len(p['founders']),len(p['visitors']))
    g=np.zeros(shape+(2,),int); occ=np.zeros(shape+(2,2),int)
    sens=np.zeros((len(EPS),)+shape+(2,),int)
    counts={}
    for r in records:
        fi=p['founders'].index(r['founder']); vi=p['visitors'].index(r['visitor'])
        expected_arms={(policy,stage) for policy in p['policies'] for stage in ('B8','B4p5')}
        if (len(r['arms'])!=4 or {(a['policy'],a['stage']) for a in r['arms']}!=expected_arms):
            raise ValueError('missing or duplicate arm')
        for arm in r['arms']:
            if (type(arm['alive']) is not bool or any(
                len(arm[key])!=len(EPS) or any(type(x) is not bool for x in arm[key])
                for key in ('genetic_first','extinction_first','final_access'))):
                raise ValueError('invalid arm endpoint vectors')
            if len(arm['max_I'])!=81 or len(arm['min_A'])!=81:
                raise ValueError('missing arm census')
            for ei,eps in enumerate(EPS):
                ev=n.events(arm['max_I'],r['target_I']-eps)
                alive=arm['max_I'][-1] is not None
                access=bool(alive and arm['max_I'][-1]>=r['target_I']-eps-1e-12)
                if (ev['G_first']!=arm['genetic_first'][ei] or ev['E_first']!=arm['extinction_first'][ei]
                    or ev['first_G']!=arm['first_loss'][ei] or alive!=arm['alive']
                    or access!=arm['final_access'][ei]):
                    raise ValueError('arm endpoint/extrema mismatch')
            pi=p['policies'].index(arm['policy']); bi=('B8','B4p5').index(arm['stage'])
            occ[fi,vi,pi,bi]=arm['alive']
            if bi==0:
                g[fi,vi,pi]=arm['genetic_first'][0]
                for ei in range(len(EPS)):sens[ei,fi,vi,pi]=arm['genetic_first'][ei]
            key=arm['policy']+'_'+arm['stage']
            out=counts.setdefault(key,dict(alive=0,alive_accessible=0,genetic_first=0,extinction_first=0))
            out['alive']+=int(arm['alive']);out['alive_accessible']+=int(arm['final_access'][0])
            out['genetic_first']+=int(arm['genetic_first'][0]);out['extinction_first']+=int(arm['extinction_first'][0])
    return dict(status='TECHNICAL' if technical else 'COMPLETE_MODEL_CONDITIONAL_CONFIRMATION',
        independent_axes=list(shape),crossings=len(seen),unique_updates=250*len(seen),
        files=6*len(seen),saved_states=256*len(seen),shard_seals=refs,arms=counts,
        genetic_loss_inputs=g.tolist(),occupancy_inputs=occ.tolist(),
        primary=n.summarize(n.contrasts(g,occ),margin=.10),
        epsilon_descriptive=[dict(epsilon=eps,fixed=int(sens[i,:,:,0].sum()),
                                 evolving=int(sens[i,:,:,1].sum())) for i,eps in enumerate(EPS)],
        actual_restoration_tested=False,biological_SESOI_endorsed=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('init','run','seal','aggregate'))
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--technical',action='store_true')
    parser.add_argument('--shard',type=int,default=0)
    parser.add_argument('--max-updates',type=int)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    if args.action=='init':result=initialize(args.root,args.technical,args.shard)
    elif args.action=='run':result=run(args.root,args.max_updates)
    elif args.action=='seal':result=seal(args.root)
    else:result=aggregate([json.loads(p.read_bytes()) for p in sorted(args.root.glob('seal-*.json'))],args.technical)
    if args.out:
        with args.out.open('xb') as handle:handle.write(n.canonical(result)+b'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('inventory','records','contract','genetic_loss_inputs','occupancy_inputs')},sort_keys=True))
