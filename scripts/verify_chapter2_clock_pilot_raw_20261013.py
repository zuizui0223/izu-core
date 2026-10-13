"""Producer-independent full raw archive / heredity verifier for clock factorial.

Never imports the producer. Checks the canonical original Model3 biological model,
all raw adults and parent pairs, independent recruitment replay, every checksum,
six-category right-censoring and the exact source input registration.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import re
from dataclasses import replace
from pathlib import Path
import numpy as np

ORIGINAL_BLOBS={
    'types.py':'0bc427b3261e7baf1651648ee879b368f9bf935b',
    'reproduction.py':'95314698a3296b6f13b8c053c36f2df0b7b744ca',
    'population.py':'20e90f249f63e9f37e8801d19d9b75cade2fe193',
    'randomness.py':'46f1ee55899e729cdd09d9dbb9332694ef1e2071',
    'history.py':'0c58aee6f73ae133d96d8da4dd6678886ff3061c',
}
REGISTRY_BLOB='f18eae09e3f569ae7edefe970ea17d93c64b1bd5'
T0_BLOB='4b529cce12bc44e06d43a22b10c325a52bbd967b'
DESIGN_BLOB='75d49de2781a240c14bdc3f9106212b0dbbda6aa'
FIELDS=('ids','alleles','allele_origin','mutation_flags','birth_years')
RETURN_COLUMNS=('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')
LEDGER_COLUMNS=('outcross','self_raw','self_viable','ovules','exported','delivered','lost','maternal','paternal')
CATEGORIES=('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')
OP_RE=re.compile(r'^(main|confirmation)_c(0|3|4)_A([LH])_I([01])_r(\d{3})$')
WIDTH={'L':.046875,'H':.078125};HOM={'0':0.,'1':1.}
ENV={0:(),3:(.5,.5,.5,.5),4:(.3,.3,.7,.7)}
TECH_SALT='chapter2-clock-factorial-producer-validation-v1-20261013'


def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def git_blob(data:bytes)->str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def locked(path:Path,want:str)->dict:
    data=path.read_bytes()
    if git_blob(data)!=want:raise ValueError('independent input Git blob failure: '+str(path))
    return json.loads(data)


def native():
    from scripts.model3_island import types,population,reproduction,randomness,history
    named={'types.py':types,'population.py':population,'reproduction.py':reproduction,'randomness.py':randomness,'history.py':history}
    for k,m in named.items():
        if git_blob(Path(m.__file__).read_bytes())!=ORIGINAL_BLOBS[k]:
            raise ValueError('historical Model3 original source mismatch '+k)
    return types,population,reproduction,randomness


def array(p):
    b=base64.b64decode(p['data_b64'],validate=True)
    if sha(b)!=p['sha256']:raise ValueError('initial source genotype field corruption')
    dtype=np.dtype(p['dtype']);shape=tuple(p['shape'])
    if dtype.hasobject or dtype.itemsize*int(np.prod(shape))!=len(b):
        raise ValueError('initial source genetic dtype mismatch')
    return np.frombuffer(b,dtype=dtype).reshape(shape).copy()


def genotype(block,letter,h,original,modules):
    typ,_,_,_=modules
    src=original['original_founders'][block]
    adult=typ.PlantState(**{k:array(src['source_state_arrays'][k]) for k in FIELDS})
    old=adult.alleles;new=old.copy();mid=old[:,1,:].mean(axis=1)
    half=(old[:,1,1]-old[:,1,0])/2
    new[:,1,0]=mid-HOM[h]*half;new[:,1,1]=mid+HOM[h]*half
    new[:,2,:]=[.5-WIDTH[letter],.5+WIDTH[letter]]
    if not np.array_equal(new.mean(axis=2),old.mean(axis=2)):
        raise ValueError('unmatched original time0 individual phenotypes')
    return replace(adult,alleles=new)


def case_args(case_key):
    m=OP_RE.fullmatch(case_key)
    if not m:raise ValueError('invalid original case key')
    block,c,a,i,rep=m.groups()
    if int(rep)>=64:raise ValueError('case outside 64-registered per founder')
    return block,int(c),a,i,int(rep)


def ledger_digest(l):
    z=hashlib.sha256()
    for key in LEDGER_COLUMNS:
        a=np.asarray(getattr(l,key),dtype=np.float64)
        z.update(key.encode()+b'\0');z.update(np.asarray(a.shape,dtype=np.int64).tobytes());z.update(a.tobytes(order='C'))
    return z.hexdigest()


def six_class(means,pop):
    means=np.asarray(means,dtype=float);pop=np.asarray(pop,dtype=int)
    if (pop[0]!=48 or means.shape!=(201,3) or len(pop)!=201 or (pop<0).any() or (pop>48).any()):
        raise ValueError('six-class source census dimensions')
    flags=pop>0
    if not np.isfinite(means[flags]).all() or not np.isnan(means[~flags]).all():
        raise ValueError('missing/extinct phenotype not handled')
    if (~flags).any() and flags[np.flatnonzero(~flags)[0]:].any():
        raise ValueError('extinction should be absorbing')
    first=[]
    for col,direction in ((2,1),(1,-1)):
        hit=flags & (direction*(means[:,col]-means[0,col])>=.05)
        found=np.flatnonzero(np.convolve(hit.astype(np.int64),np.ones(20,dtype=np.int64),'valid')==20)
        first.append(int(found[0]) if len(found) else None)
    a,i=first
    if a is None:category='neither' if i is None else 'investment_only'
    elif i is None:category='assurance_only'
    elif abs(a-i)<=5:category='near_simultaneous'
    else:category='assurance_first' if a<i else 'investment_first'
    return {'A':a,'I':i,'category':category}


def require_array_shape(raw:dict,n:int,years:int):
    nsource=int(raw['offsets'][-1]);nparents=int(raw['parent_offsets'][-1]);nreturns=int(raw['source_offsets'][-1]);
    shapes={
        'ids':(nsource,), 'alleles':(nsource,3,2),
        'allele_origin':(nsource,3,2),'mutation_flags':(nsource,3,2),'birth_years':(nsource,),
        'offsets':(years+2,),'population':(years+1,),'means':(years+1,3),
        'parentage':(nparents,3),'parent_offsets':(years+1,),
        'source_parent_returns':(nreturns,3),'source_offsets':(years+1,),
        'returns':(years,8),'sexual_selection':(years,3,3),
        'reproductive_ledger_sha256':(years,),'recruitment':(years,8),
    }
    if set(raw)!=(set(shapes)|{'metadata'}):raise ValueError('unknown/missing archive data arrays')
    for key,shape in shapes.items():
        if raw[key].shape!=shape:raise ValueError('incorrect archive field shape: '+key)
    for key in ('ids','allele_origin','birth_years','offsets','population','parentage','parent_offsets','source_offsets','recruitment'):
        if raw[key].dtype.kind not in 'iu':raise ValueError('bad integer array type '+key)
    if raw['mutation_flags'].dtype.kind!='b' or raw['reproductive_ledger_sha256'].dtype.kind!='S':
        raise ValueError('bad flag/digest dtype')
    for offset,measure in [('offsets','population'),('parent_offsets',None),('source_offsets',None)]:
        v=raw[offset]
        if v[0]!=0 or np.any(np.diff(v)<0):raise ValueError('nonmonotone archive offsets '+offset)
        if measure is not None and not np.array_equal(np.diff(v),raw[measure]):
            raise ValueError('original census offset mismatch')
    if not np.array_equal(np.diff(raw['parent_offsets']),raw['population'][1:]):
        raise ValueError('recruits versus saved parentage mismatch')
    if not np.array_equal(np.diff(raw['source_offsets']),raw['population'][:-1]):
        raise ValueError('source parent return offsets mismatch')
    if np.any(raw['population']>48) or raw['population'][0]!=n or np.any(raw['population']<0):
        raise ValueError('population history invalid')


def verify_one(path:Path,expected_case:dict,reg,fixture,mods,technical:bool):
    typ,pop,repro,randomness=mods
    blob=path.read_bytes()
    if sha(blob)!=expected_case['sha256']:
        raise ValueError('case NPZ SHA changed: '+path.name)
    with np.load(path,allow_pickle=False) as npz:
        saved={k:npz[k] for k in npz.files}
    meta=json.loads(str(saved['metadata'].item()))
    case=expected_case['case_key'];b,c,a,i,r=case_args(case)
    if (meta['case_key']!=case or path.name!=case+'.npz' or meta['block']!=b
        or meta['original_context']!=c or meta['A_halfwidth']!=WIDTH[a]
        or meta['I_hidden_homolog']!=HOM[i] or meta['replicate']!=r):
        raise ValueError('shuffled pilot NPZ metadata versus complete inventory')
    if (meta['registry_git_blob']!=REGISTRY_BLOB or meta['fixture_git_blob']!=T0_BLOB
        or meta['model_git_blobs']!=ORIGINAL_BLOBS or meta['mutation_traits']!=[False,False,True]):
        raise ValueError('original source/sex/mutation/ancestry receipts drift')
    years=3 if technical else 200
    if (meta['years']!=years or meta['technical']!=technical
        or meta['numpy_version']!=np.__version__):
        raise ValueError('changed exploratory/technical horizon')
    if not technical and np.__version__!='2.2.6':
        raise ValueError('registered 200-year original runtime must be NumPy2.2.6')
    master=(int.from_bytes(hashlib.sha256(f'{TECH_SALT}\0{b}\0{r}'.encode()).digest()[:16],'big') if technical else
            int(reg['stochastic_history_cluster_master_seeds_decimal'][f'{b}:r{r:03d}']))
    if meta['master_seed_decimal']!=str(master):
        raise ValueError('independent source stream seed does not match registration')
    initial=genotype(b,a,i,fixture,mods)
    key=f'{b}:A{a}:I{i}'
    if sha(initial.alleles.tobytes(order='C'))!=reg['genetic_treatment_genome_sha256'][key]['allele_sha256']:
        raise ValueError('original pilot genotype fingerprint mismatch')
    cfg_dict=fixture['original_founders'][b]['contexts'][str(c)]['config']
    config=typ.Config.from_dict(cfg_dict)
    cfghash=sha(json.dumps(cfg_dict,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
    if meta['source_config_sha256']!=cfghash or cfghash!=reg['source_config_contexts'][f'{b}:context{c}']['original_configuration_sha256']:
        raise ValueError('original environment fingerprint mismatch')
    optima=np.array({0:(),3:(.5,)*4,4:(.3,.3,.7,.7)}[c],dtype=float)
    vis=typ.VisitorState(ids=np.arange(len(optima),dtype=np.int64),optima=optima,
        breadths=np.full(len(optima),config.visitor_breadth),
        effectiveness=np.full(len(optima),config.visitor_effectiveness))
    require_array_shape(saved,48,years)
    steams={name:randomness.stream(master,name,0) for name in randomness.STREAM_IDS}
    empty=pop.subset(initial,np.empty(0,dtype=int))
    state=initial
    checked=0;parentpairs=0;source_genomes=0;birth_changes=0
    for year in range(years+1):
        lo=int(saved['offsets'][year]);hi=int(saved['offsets'][year+1]);n=hi-lo
        stored=typ.PlantState(**{k:saved[k][lo:hi] for k in FIELDS})
        if n!=len(state.ids):raise ValueError('original indexed occupancy drift')
        for k in FIELDS:
            if not np.array_equal(getattr(stored,k),getattr(state,k)):
                raise ValueError('native independent source-to-child replay mismatch: '+k)
        expected_mean=state.alleles.mean(axis=(0,2)) if n else np.full(3,np.nan)
        np.testing.assert_allclose(saved['means'][year],expected_mean,rtol=0,atol=0,equal_nan=True)
        if year==years:break
        ledger=repro.reproduce(stored,vis,config)
        true_hash=ledger_digest(ledger)
        if saved['reproductive_ledger_sha256'][year].decode()!=true_hash:
            raise ValueError('independent original source ledger SHA mismatch')
        expected_returns=np.array([np.asarray(getattr(ledger,k)).sum() for k in RETURN_COLUMNS],dtype=float)
        np.testing.assert_allclose(saved['returns'][year],expected_returns,rtol=0,atol=0)
        w=np.stack([ledger.outcross.sum(axis=0)/2,ledger.outcross.sum(axis=1)/2,ledger.self_viable],axis=1)
        rlo=int(saved['source_offsets'][year]);rhi=int(saved['source_offsets'][year+1]);
        if not np.array_equal(saved['source_parent_returns'][rlo:rhi],w):
            raise ValueError('actual mother/father/self full parent expected return mismatch')
        mu=float(w.sum())
        traits=stored.alleles.mean(axis=2) if n else np.empty((0,3))
        components=(np.stack([w[:,j]@(traits-traits.mean(axis=0))/mu for j in range(3)])
                    if mu>0 else np.zeros((3,3),dtype=float))
        np.testing.assert_allclose(saved['sexual_selection'][year],components,rtol=0,atol=0)
        if not np.isclose(float(ledger.maternal.sum()),mu,rtol=0,atol=1e-12):
            raise ValueError('mother+father+self reproductive genetic return conservation')
        future,info=pop.advance(stored,ledger,empty,config,steams,year=year,mutation_traits=(False,False,True))
        plo=int(saved['parent_offsets'][year]);phi=int(saved['parent_offsets'][year+1]);parents=saved['parentage'][plo:phi]
        if parents.shape!=(len(future.ids),3) or not np.array_equal(parents,info['parentage']):
            raise ValueError('native independent parentpair RNG replay mismatch')
        count=saved['recruitment'][year]
        exp=np.array([n,len(future.ids),info['resident_potential'],info['resident_recruits'],
            info['resident_selfed_recruits'],info['resident_outcross_recruits'],
            info['immigrant_recruits'],info['survivors']],dtype=np.int64)
        if not np.array_equal(count,exp):raise ValueError('actual demographic native receipt mismatch')
        if info['immigrant_recruits'] or info['survivors']:
            raise ValueError('unsupported immigrant or perennial recruitment')
        for k in FIELDS:
            if not np.array_equal(getattr(future,k),saved[k][int(saved['offsets'][year+1]):int(saved['offsets'][year+2])]):
                raise ValueError('original complete allele/genotype/origin/age birth replay mismatch: '+k)
        parentpairs+=len(parents);source_genomes+=n;checked+=1
        state=future
    if not technical:
        evt=six_class(saved['means'],saved['population'])
        if evt!=expected_case['event_0p05']:
            raise ValueError('six outcome categories changed or mis-censored')
    else:
        if expected_case['event_0p05'] is not None:
            raise ValueError('technical 3-update fixture must not report biological order')
    return {'case_key':case,'updates':checked,'genotype_record_source_years':source_genomes,
            'parent_pairs':parentpairs,'case_sha256':sha(blob),
            'event_0p05':None if technical else evt}


def verify(directory:Path,registry_path:Path,fixture_path:Path,design_path:Path,technical:bool):
    reg=locked(registry_path,REGISTRY_BLOB);fixture=locked(fixture_path,T0_BLOB)
    design=locked(design_path,DESIGN_BLOB)
    if reg['status']!='PRE_BIOLOGICAL_EXPLICIT_PILOT_INPUTS_RECORDED_NO_EXECUTION' or design['pilot']['total_trajectories']!=1536:
        raise ValueError('original design and registry admission')
    modules=native()
    completed=json.loads((directory/'_COMPLETION.json').read_bytes())
    n=48 if technical else 256
    if (completed['cases']!=n or completed['source_code_sha256']==''
        or completed['pilot_registry_git_blob']!=REGISTRY_BLOB
        or completed['protocol_git_blob']!=DESIGN_BLOB
        or completed['fixture_git_blob']!=T0_BLOB
        or completed['model_biological_git_blobs']!=ORIGINAL_BLOBS
        or completed['source_runtime_numpy']!=np.__version__
        or completed['updates_per_case']!=(3 if technical else 200)
        or completed['status']!=('TECHNICAL_ONLY_48_NATIVE_PATHS' if technical else 'COMPLETE_REGISTERED_256_NATIVE_PATHS')):
        raise ValueError('producer completion manifest is not complete or source locked')
    if completed['execution_mode']!=('technical' if technical else 'pilot'):
        raise ValueError('technical/pilot namespace violation')
    if len(completed['case_records'])!=n:
        raise ValueError('producer omitted/shuffled case count')
    candidates=reg['case_identifiers']
    if technical:
        expected={s for s in candidates if int(case_args(s)[-1])<2}
    else:
        shard=completed['shard']; block=('main','confirmation')[shard//3];ctx=(0,3,4)[shard%3]
        expected={s for s in candidates if case_args(s)[:2]==(block,ctx)}
    keys=[x['case_key'] for x in completed['case_records']]
    if set(keys)!=expected or len(set(keys))!=n:
        raise ValueError('original registry case table does not match archived receipt')
    if {p.name for p in directory.iterdir()}!={x+'.npz' for x in expected}|{'_COMPLETION.json'}:
        raise ValueError('archive member inventory missing/extra')
    rows=[]
    for one in completed['case_records']:
        rows.append(verify_one(directory/(one['case_key']+'.npz'),one,reg,fixture,modules,technical))
    checks=sum(x['updates'] for x in rows)
    if checks!=n*(3 if technical else 200):raise ValueError('wrong complete original biological annual updates')
    return {'schema':'chapter2_clock_factorial_producer_independent_raw_reader_v1',
        'status':'ALL_48_NATIVE_TECHNICAL_PATHS_REPRODUCED' if technical else 'ALL_256_PILOT_SHARD_RAW_GENOMES_REPLAYED',
        'pilot_registry_git_blob':REGISTRY_BLOB,'original_source_git_blobs':ORIGINAL_BLOBS,
        'cases':n,'updates':checks,'parent_pairs':sum(r['parent_pairs'] for r in rows),
        'source_year_genetic_records':sum(r['genotype_record_source_years'] for r in rows),
        'producer_loaded_as_python_module':False,
        'original_model3_biological_source_replayed':True,'original_t0_historical_source_admitted':True,
        'six_event_categories':CATEGORIES if not technical else None,
        'new_pilot_biological_histories':0 if technical else n,
        'original_case_receipts':rows}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',type=Path,required=True);p.add_argument('--registry',type=Path,required=True)
    p.add_argument('--fixture',type=Path,required=True);p.add_argument('--design',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--technical',action='store_true')
    args=p.parse_args()
    if args.out.exists():raise ValueError('independent source readout output exists')
    receipt=verify(args.data,args.registry,args.fixture,args.design,args.technical)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf8',newline='\n') as file:
        json.dump(receipt,file,indent=2,ensure_ascii=False,allow_nan=False);file.write('\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='original_case_receipts'},indent=2))

if __name__=='__main__':main()
