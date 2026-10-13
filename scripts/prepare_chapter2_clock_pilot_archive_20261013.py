"""Model3 original-biological-operator pilot producer. NO implicit execution.

Use --technical for independent, 3-update fixtures; actual --shard (0..5)
is deliberately blocked unless the separately reviewed approval receipt is supplied.
This file does not change the original biological Model3 source.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import io
from dataclasses import replace
import numpy as np

FIELDS = ('ids','alleles','allele_origin','mutation_flags','birth_years')
LEDGER_FIELDS = ('outcross','self_raw','self_viable','ovules','exported',
                 'delivered','lost','maternal','paternal')
RETURNS = ('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')
ORIGINAL_MODEL_BLOBS = {
    'types.py':'0bc427b3261e7baf1651648ee879b368f9bf935b',
    'reproduction.py':'95314698a3296b6f13b8c053c36f2df0b7b744ca',
    'population.py':'20e90f249f63e9f37e8801d19d9b75cade2fe193',
    'randomness.py':'46f1ee55899e729cdd09d9dbb9332694ef1e2071',
    'history.py':'0c58aee6f73ae133d96d8da4dd6678886ff3061c',
}
REGISTRY_SHA = 'f18eae09e3f569ae7edefe970ea17d93c64b1bd5'
ORIGINAL_T0_SHA = '4b529cce12bc44e06d43a22b10c325a52bbd967b'
DESIGN_SHA = '75d49de2781a240c14bdc3f9106212b0dbbda6aa'
ORIGINAL_LEDGER_SHA = 'e1d4e58a8dde547a94b687d6f89d2843c8bfff0c'
TECH_SALT = 'chapter2-clock-factorial-producer-validation-v1-20261013'
APPROVAL_GIT_BLOB = None  # No independent scientific authorization receipt has yet been frozen
PILOT_SALT = 'chapter2-clock-factorial-pilot-v1-20261013'
CASE_RE = re.compile(r'^(main|confirmation)_c(0|3|4)_A([LH])_I([01])_r(\d{3})$')
WIDTHS={'L':.046875,'H':.078125}
HIDDEN={'0':0.,'1':1.}
CONTEXTS={0:(),3:(.5,.5,.5,.5),4:(.3,.3,.7,.7)}
EXPECTED_COLS = ('original_census','offspring_census','resident_potential','resident_recruits',
                 'resident_selfed','resident_outcross','immigrant_recruits','survivors')


def digest(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data:bytes)->str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def json_text(obj)->str:
    return json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n'


def source_json(path:Path,expected:str):
    raw=path.read_bytes()
    if git_blob(raw)!=expected:
        raise ValueError('frozen input Git blob mismatch: '+str(path))
    return json.loads(raw)


def native():
    from scripts.model3_island import types, population, reproduction, randomness, history
    mods={'types.py':types,'population.py':population,'reproduction.py':reproduction,
          'randomness.py':randomness,'history.py':history}
    for name,mod in mods.items():
        if git_blob(Path(mod.__file__).read_bytes())!=ORIGINAL_MODEL_BLOBS[name]:
            raise ValueError('original native Model3 source drift: '+name)
    return types,population,reproduction,randomness


def decode(original:dict)->np.ndarray:
    import base64
    data=base64.b64decode(original['data_b64'],validate=True)
    if digest(data)!=original['sha256']:
        raise ValueError('source historical t0 allele copy changed')
    dtype=np.dtype(original['dtype']);shape=tuple(original['shape'])
    if dtype.hasobject or len(shape)>3 or np.prod(shape)*dtype.itemsize!=len(data):
        raise ValueError('source historical typed original shape/bytes invalid')
    return np.frombuffer(data,dtype=dtype).reshape(shape).copy()


def sources(registry_path:Path,fixture_path:Path,design_path:Path,ledger_path:Path):
    registry=source_json(registry_path,REGISTRY_SHA)
    fixture=source_json(fixture_path,ORIGINAL_T0_SHA)
    design=source_json(design_path,DESIGN_SHA)
    ledger=source_json(ledger_path,ORIGINAL_LEDGER_SHA)
    if (registry['status']!='PRE_BIOLOGICAL_EXPLICIT_PILOT_INPUTS_RECORDED_NO_EXECUTION'
        or registry['pilot_salt']!=PILOT_SALT or registry['total_input_trajectories']!=1536
        or len(set(registry['case_identifiers']))!=1536
        or len(registry['stochastic_history_cluster_master_seeds_decimal'])!=128
        or registry['updates_per_trajectory']!=200
        or registry['original_model_source_blobs']!=ORIGINAL_MODEL_BLOBS):
        raise ValueError('pilot input registration no longer matches frozen source')
    if design['pilot']['total_trajectories']!=1536 or design['factorial']['horizon_updates']!=200:
        raise ValueError('pilot design changed')
    if fixture['new_biological_histories']!=0 or len(fixture['original_founders'])!=2:
        raise ValueError('source biological time-zero fixture changed')
    if ledger['status']!='SIX_ORIGINAL_SOURCE_STATES_TWENTY_FOUR_GENOTYPE_CONTRAST_LEDGERS_EXACT':
        raise ValueError('original reproductive ledger not admitted')
    expected={str(x['block'])+':'+str(x['original_context']):x['source_original_ledger_sha256']
              for x in ledger['records']}
    if len(expected)!=6:
        raise ValueError('source ledger expected six founder/ecology inputs')
    return registry,fixture,design,expected


def case_parts(case_key:str):
    mat=CASE_RE.fullmatch(case_key)
    if mat is None:raise ValueError('unregistered pilot case key')
    block,context,letter,h,rep=mat.groups()
    if int(rep)>=64:raise ValueError('outside frozen 64 source seeds')
    return block,int(context),letter,h,int(rep)


def technical_seed(block:str,rep:int)->int:
    return int.from_bytes(hashlib.sha256(f'{TECH_SALT}\0{block}\0{rep}'.encode()).digest()[:16],'big')


def founder_case(registry,fixture,block,context,letter,h,modules):
    typ,pop,repro,rng=modules
    src=fixture['original_founders'][block]
    base=typ.PlantState(**{key:decode(src['source_state_arrays'][key]) for key in FIELDS})
    config=typ.Config.from_dict(src['contexts'][str(context)]['config'])
    n=len(base.ids)
    if n!=48 or config.capacity!=48 or config.years!=200 or config.seed_arrival.supply!=0 or config.survival!=0:
        raise ValueError('original biological baseline genotype, demographic or horizon drift')
    if (config.assurance_mode,config.mutation_rate,config.mutation_sd)!=( 'evolving',.01,.05):
        raise ValueError('assurance/mutation config drift')
    if context not in CONTEXTS:raise ValueError('unregistered ecology')
    optima=np.array(CONTEXTS[context],dtype=np.float64)
    visitor=typ.VisitorState(ids=np.arange(len(optima),dtype=np.int64),optima=optima,
          breadths=np.full(len(optima),config.visitor_breadth),
          effectiveness=np.full(len(optima),config.visitor_effectiveness))
    alleles=base.alleles.copy()
    old=alleles[:,1,:].copy();means=old.mean(axis=1)
    d=(old[:,1]-old[:,0])/2
    alleles[:,1,0]=means-HIDDEN[h]*d
    alleles[:,1,1]=means+HIDDEN[h]*d
    alleles[:,2,:]=[.5-WIDTHS[letter],.5+WIDTHS[letter]]
    if not np.array_equal(base.alleles.mean(axis=2),alleles.mean(axis=2)):
        raise ValueError('source individual initial phenotype changed')
    initial=replace(base,alleles=alleles)
    key=f'{block}:A{letter}:I{h}'
    record=registry['genetic_treatment_genome_sha256'][key]
    if digest(alleles.tobytes(order='C'))!=record['allele_sha256']:
        raise ValueError('registered 8-genotype source SHA mismatch: '+key)
    if digest(alleles.mean(axis=2).tobytes(order='C'))!=record['founder_trait_sha256']:
        raise ValueError('registered source phenotype SHA mismatch: '+key)
    expectedcfg=registry['source_config_contexts'][f'{block}:context{context}']
    original_cfg=src['contexts'][str(context)]['config']
    csha=digest(json.dumps(original_cfg,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf8'))
    if expectedcfg['original_configuration_sha256']!=csha:
        raise ValueError('original ecological configuration fingerprint drift')
    return initial,config,visitor,csha,record['allele_sha256'],base


def ledger_hash(ledger):
    h=hashlib.sha256()
    for key in LEDGER_FIELDS:
        arr=np.asarray(getattr(ledger,key),dtype=np.float64)
        h.update(key.encode()+b'\0')
        h.update(np.asarray(arr.shape,dtype=np.int64).tobytes())
        h.update(arr.tobytes(order='C'))
    return h.hexdigest()



def verify_original_t0_source_returns(original_ledger, archived_source_totals):
    """Anchor t0 biology to recorded original NPZ returns, not a cross-platform SHA.

    Historical t0 full-array ledger SHA came from a separate source-admission
    computation with no recorded numerical runtime. Even matching NumPy
    versions do not guarantee identical BLAS/ufunc last bits across machines.
    Within a runtime, original-vs-hidden-genotype ledger SHA MUST match
    exactly; eight archived source totals must match independently at the
    already registered 1e-12 source tolerance.
    """
    actual=np.array([float(np.asarray(getattr(original_ledger,k)).sum())
                     for k in RETURNS],dtype=np.float64)
    recorded=np.asarray(archived_source_totals,dtype=np.float64)
    if (recorded.shape!=(len(RETURNS),) or not np.isfinite(recorded).all()
            or not np.allclose(actual,recorded,atol=1e-12,rtol=0)):
        raise ValueError('historical original t0 reproductive totals differ')
    return actual


def original_events(means,census,threshold=.05):
    means=np.asarray(means,dtype=np.float64);census=np.asarray(census,dtype=int)
    length=len(census)
    if means.shape!=(length,3) or census[0]!=48 or (census<0).any() or (census>48).any():
        raise ValueError('source annual census event admission')
    occupied=census>0
    if not np.isfinite(means[occupied]).all() or not np.isnan(means[~occupied]).all():
        raise ValueError('extinct traits are missing, not zero')
    if (~occupied).any():
        first=np.flatnonzero(~occupied)[0]
        if occupied[first:].any():raise ValueError('recolonization under no-seed-arrival rule')
    ret={}
    for name,k,d in [('A',2,1),('I',1,-1)]:
        flags=occupied & (d*(means[:,k]-means[0,k])>=threshold)
        hit=np.flatnonzero(np.convolve(flags.astype(int),np.ones(20,dtype=int),mode='valid')==20)
        ret[name]=int(hit[0]) if len(hit) else None
    a,i=ret['A'],ret['I']
    if a is None:ret['category']='investment_only' if i is not None else 'neither'
    elif i is None:ret['category']='assurance_only'
    elif abs(a-i)<=5:ret['category']='near_simultaneous'
    else:ret['category']='assurance_first' if a<i else 'investment_first'
    return ret


def model_history(case_key,reg,fixture,expected,modules,technical=False):
    _,pop,repro,randomness=modules
    block,context,letter,h,rep=case_parts(case_key)
    state,config,vis,conf_sha,gen_sha,unaltered=founder_case(reg,fixture,block,context,letter,h,modules)
    original_ledger=repro.reproduce(unaltered,vis,config)
    adjusted_ledger=repro.reproduce(state,vis,config)
    digest0=ledger_hash(original_ledger)
    if ledger_hash(adjusted_ledger)!=digest0:
        raise ValueError('t0 genotype variation changed reproductive state within runtime')
    if f'{block}:{context}' not in expected:
        raise ValueError('source-authenticated historical ledger receipt absent')
    historical_t0=fixture['original_founders'][block]['contexts'][str(context)]['original_returns_t0']
    verify_original_t0_source_returns(original_ledger,historical_t0)
    if technical:
        if rep>=2:raise ValueError('max two technical reps per founder')
        master=technical_seed(block,rep);years=3
    else:
        if np.__version__!='2.2.6':
            raise ValueError('Full 200-update cohort restricted to frozen NumPy 2.2.6 original runtime')
        master=int(reg['stochastic_history_cluster_master_seeds_decimal'][f'{block}:r{rep:03d}'])
        years=200
    streams={key:randomness.stream(master,key,0) for key in randomness.STREAM_IDS}
    empty=pop.subset(state,np.empty(0,dtype=int))
    vals={key:[] for key in FIELDS}
    offsets=[0];parents=[];parent_offsets=[0];source_returns=[];source_offsets=[0]
    counts=[];means=[];totals=[];return_components=[];full_ledger_hashes=[];recruitment=[]
    for t in range(years+1):
        n=len(state.ids)
        counts.append(n)
        means.append(state.alleles.mean(axis=(0,2)) if n else np.full(3,np.nan))
        for key in FIELDS:vals[key].append(getattr(state,key).copy())
        offsets.append(offsets[-1]+n)
        if t==years:break
        ledger=repro.reproduce(state,vis,config)
        full_ledger_hashes.append(ledger_hash(ledger).encode('ascii'))
        sums=[float(np.asarray(getattr(ledger,k)).sum()) for k in RETURNS]
        totals.append(sums)
        traits=state.alleles.mean(axis=2) if n else np.empty((0,3),dtype=float)
        w=np.stack([ledger.outcross.sum(axis=0)/2,ledger.outcross.sum(axis=1)/2,ledger.self_viable],axis=1)
        source_returns.append(w)
        source_offsets.append(source_offsets[-1]+n)
        mu=float(w.sum())
        if mu>0:
            selection=np.stack([w[:,j]@(traits-traits.mean(axis=0))/mu for j in range(3)])
        else:
            selection=np.zeros((3,3),dtype=np.float64)
        return_components.append(selection)
        nxt,info=pop.advance(state,ledger,empty,config,streams,year=t,mutation_traits=(False,False,True))
        parentage=info['parentage']
        if parentage.shape!=(len(nxt.ids),3) or not np.array_equal(parentage[:,0],nxt.ids):
            raise ValueError('original source parentage/child mismatch')
        parents.append(parentage)
        parent_offsets.append(parent_offsets[-1]+len(parentage))
        recruitment.append([n,len(nxt.ids),info['resident_potential'],info['resident_recruits'],
            info['resident_selfed_recruits'],info['resident_outcross_recruits'],
            info['immigrant_recruits'],info['survivors']])
        if (len(nxt.ids)>48 or info['immigrant_recruits'] or info['survivors']
            or info['resident_selfed_recruits']+info['resident_outcross_recruits']!=len(nxt.ids)):
            raise ValueError('original canonical density-parentage contract changed')
        state=nxt
    data={k:np.concatenate(v) for k,v in vals.items()}
    data.update(
        offsets=np.asarray(offsets,dtype=np.int64),
        population=np.asarray(counts,dtype=np.int64),
        means=np.asarray(means,dtype=np.float64),
        parentage=np.concatenate(parents).reshape(-1,3).astype(np.int64),
        parent_offsets=np.asarray(parent_offsets,dtype=np.int64),
        source_parent_returns=np.concatenate(source_returns).reshape(-1,3).astype(np.float64),
        source_offsets=np.asarray(source_offsets,dtype=np.int64),
        returns=np.asarray(totals,dtype=np.float64),
        sexual_selection=np.asarray(return_components,dtype=np.float64),
        reproductive_ledger_sha256=np.asarray(full_ledger_hashes,dtype='S64'),
        recruitment=np.asarray(recruitment,dtype=np.int64),
    )
    metadata={
        'case_key':case_key,'block':block,'original_context':context,
        'A_halfwidth':WIDTHS[letter],'I_hidden_homolog':HIDDEN[h],
        'replicate':rep,'master_seed_decimal':str(master),'technical':bool(technical),
        'original_source_execution_commit':'328548612e93469fcc8663f24548530a57399b9a',
        'registry_git_blob':REGISTRY_SHA,'fixture_git_blob':ORIGINAL_T0_SHA,
        'source_config_sha256':conf_sha,'starting_alleles_sha256':gen_sha,
        'model_git_blobs':ORIGINAL_MODEL_BLOBS,
        'numpy_version':np.__version__,'years':years,
        'mutation_traits':[False,False,True],
        'all_six_original_categories_retained':True
    }
    data['metadata']=np.array(json.dumps(metadata,sort_keys=True,separators=(',',':')))
    event=original_events(data['means'],data['population']) if years==200 else None
    return data,meta(metadata),event


def meta(m):
    return dict(m)


def technical_case_keys(reg):
    return [k for k in reg['case_identifiers'] if case_parts(k)[-1]<2]


def shard_case_keys(reg,shard:int):
    if shard not in range(6):raise ValueError('six prespecified founder/ecology shards, 0-5')
    block=('main','confirmation')[shard//3]
    context=(0,3,4)[shard%3]
    return [k for k in reg['case_identifiers'] if case_parts(k)[:2]==(block,context)]


def archive(out_dir:Path,registry_path:Path,fixture_path:Path,design_path:Path,ledger_path:Path,
            technical:bool=False,shard:int|None=None,approval_path:Path|None=None):
    reg,fixture,design,expected=sources(registry_path,fixture_path,design_path,ledger_path)
    modules=native()
    if technical:
        if shard is not None or approval_path is not None:
            raise ValueError('technical test must have no pilot shard/approval')
        keys=technical_case_keys(reg)
    else:
        if shard is None or approval_path is None:
            raise ValueError('real pilot is blocked without explicit shard and approved pre-execution receipt')
        if APPROVAL_GIT_BLOB is None:
            raise ValueError('no frozen independent scientific approval: 200-year pilot execution prohibited')
        approval=source_json(approval_path, APPROVAL_GIT_BLOB)
        if approval.get('status')!='APPROVED_TO_RUN_PILOT':
            raise ValueError('pilot approval was not granted')
        if approval.get('registry_git_blob')!=REGISTRY_SHA:
            raise ValueError('pilot approval must refer to original registry identity')
        keys=shard_case_keys(reg,shard)
    out_dir.mkdir(parents=True,exist_ok=False)
    rec=[]
    for i,key in enumerate(keys):
        arrays,metadata,event=model_history(key,reg,fixture,expected,modules,technical=technical)
        destination=out_dir/(key+'.npz')
        # Exclusive writes: incomplete output directory is never a complete receipt.
        # Exclusive creation is required: exists()+write has a race that can
        # overwrite a prior valid biological NPZ produced by another worker.
        with destination.open('xb') as sink:
            np.savez_compressed(sink,**arrays)
        sourcebytes=destination.read_bytes()
        rec.append({'case_key':key,'sha256':digest(sourcebytes),'size':len(sourcebytes),
            'status':'TECHNICAL_NATIVE_3_UPDATE_ONLY' if technical else 'COMPLETE_ORIGINAL_200_UPDATE',
            'event_0p05':event})
    index={
        'schema':'chapter2_clock_factorial_model3_native_raw_shard_v1',
        'status':'TECHNICAL_ONLY_48_NATIVE_PATHS' if technical else 'COMPLETE_REGISTERED_256_NATIVE_PATHS',
        'pilot_registry_git_blob':REGISTRY_SHA,'protocol_git_blob':DESIGN_SHA,
        'fixture_git_blob':ORIGINAL_T0_SHA,'model_biological_git_blobs':ORIGINAL_MODEL_BLOBS,
        'execution_mode':'technical' if technical else 'pilot',
        'shard':None if technical else shard,'cases':len(keys),
        'source_runtime_numpy':np.__version__,
        'updates_per_case':3 if technical else 200,
        'source_code_sha256':digest(Path(__file__).read_bytes()),
        'new_scientific_pilot_histories':0 if technical else len(keys),
        'case_records':rec,
    }
    (out_dir/'_COMPLETION.json').open('x',encoding='utf8',newline='\n').write(json_text(index))
    return index


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--registry',type=Path,required=True)
    p.add_argument('--fixture',type=Path,required=True)
    p.add_argument('--design',type=Path,required=True)
    p.add_argument('--original-ledger',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--technical',action='store_true')
    p.add_argument('--shard',type=int)
    p.add_argument('--approval',type=Path)
    args=p.parse_args()
    r=archive(args.out,args.registry,args.fixture,args.design,args.original_ledger,
         technical=args.technical,shard=args.shard,approval_path=args.approval)
    print(json_text({k:v for k,v in r.items() if k!='case_records'}))

if __name__=='__main__':main()
