"""Fixed-access ecological order assay: original Model3 operators unchanged."""
import argparse
from dataclasses import replace, asdict
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import zipfile
import numpy as np
from scipy.stats import beta

FIELDS=('ids','alleles','allele_origin','mutation_flags','birth_years')
BLOCKS={'main':27200701,'confirmation':27210701}
CONTEXTS=((0.,'empty'),)+tuple((s,c) for s in (.03125,.125,.5,1.) for c in ('matched','separated'))

def tasks():
    for context,(supply,composition) in enumerate(CONTEXTS):
        for block,block_seed in BLOCKS.items():
            for r in range(128):
                yield dict(block=block,block_seed=block_seed,context=context,supply=supply,
                           composition=composition,replicate=r)

def seed(task,technical=False):
    raw=f"ecological-order-v1-20261013\0{task['block']}\0{task['replicate']}\0{int(technical)}".encode()
    return int.from_bytes(hashlib.sha256(raw).digest()[:16],'big')

def events(means,census,threshold=.05):
    means=np.asarray(means);census=np.asarray(census)
    if means.shape!=(201,3) or census.shape!=(201,) or (census<0).any() or (census>48).any():raise ValueError('Annual inventory')
    occupied=census>0
    if not occupied[0] or not np.isfinite(means[occupied]).all() or not np.isnan(means[~occupied]).all():raise ValueError('Trait-state admission')
    first=None
    if (~occupied).any():
        first=int(np.flatnonzero(~occupied)[0])
        if occupied[first:].any():raise ValueError('Extinction not absorbing')
    result={}
    for name,j,direction in [('A',2,1),('I',1,-1)]:
        flags=occupied & (direction*(means[:,j]-means[0,j])>=threshold)
        hits=np.flatnonzero(np.convolve(flags.astype(int),np.ones(20,dtype=int),mode='valid')==20)
        result[name]=int(hits[0]) if len(hits) else None
    a,i=result['A'],result['I']
    result['category']=('neither' if i is None else 'investment_only') if a is None else ('assurance_only' if i is None else ('near_simultaneous' if abs(a-i)<=5 else ('assurance_first' if a<i else 'investment_first')))
    return result

def interval(a,i,n):
    if any(type(x) is not int for x in (a,i,n)) or n<=0 or min(a,i)<0 or a+i>n:raise ValueError('Counts')
    alpha=.05/36
    def cp(k):return (0. if k==0 else float(beta.ppf(alpha/2,k,n-k+1)),1. if k==n else float(beta.ppf(1-alpha/2,k+1,n-k)))
    al,ah=cp(a);il,ih=cp(i)
    return [al-ih,ah-il]

def native(input_zip,destination):
    helper=Path(__file__).with_name('audit_genome_response_accounting_20261013.py')
    spec=importlib.util.spec_from_file_location('original_admission',helper)
    admission=importlib.util.module_from_spec(spec);spec.loader.exec_module(admission)
    source=admission.prepare_source(input_zip,destination)
    types,pop,reproduction,randomness=admission.load_native(source)
    recipe=Path(destination)/'ecological_recipe';recipe.mkdir(exist_ok=True)
    names=('campaign_inputs.py','natural_campaign_design.json','assurance_causal_inputs.py','assurance_causal_design.json')
    with zipfile.ZipFile(input_zip) as z:
        for name in names:
            b=z.read(admission.RECIPE_PREFIX+name)
            (recipe/name).write_bytes(b)
    sys.path.insert(0,str(recipe.resolve()))
    import assurance_causal_inputs
    if Path(assurance_causal_inputs.__file__).resolve().parent!=recipe.resolve():raise ValueError('Recipe import drift')
    return types,pop,reproduction,randomness,assurance_causal_inputs,source

def initial(task,modules):
    _,_,_,_,recipe,_=modules
    old=dict(block=task['block'],block_seed=task['block_seed'],supply=task['supply'],composition=task['composition'],
        capacity=48,mode='standing_mutation',assurance=.5,arm='evolving',mutation_mask='standing_MI_new_A')
    c,s,v,mask=recipe.inputs(old)
    a=s.alleles.copy();a[:,2,:]=[.4375,.5625];s=replace(s,alleles=a)
    if mask!=(False,False,True) or len(s.ids)!=48 or c.capacity!=48 or c.years!=200 or c.survival!=0 or c.seed_arrival.supply!=0:raise ValueError('Native config admission')
    if (c.investment_cost,c.assurance_cost,c.depression,c.mutation_rate,c.mutation_sd)!=(.5,.5,.5,.01,.05):raise ValueError('Frozen parameter mismatch')
    return c,s,v

def validate_inputs(modules):
    for block in BLOCKS:
        reference=None
        for task in (t for t in tasks() if t['block']==block and t['replicate']==0):
            c,s,v=initial(task,modules);config=asdict(c);config.pop('activity')
            if c.activity!=.4*task['supply']:raise ValueError('Activity scaling')
            if reference is None:reference=(config,s)
            else:
                if config!=reference[0]:raise ValueError('Non-ecological config changed')
                for k in FIELDS:np.testing.assert_array_equal(getattr(s,k),getattr(reference[1],k))
            np.testing.assert_array_equal(s.alleles[:,2,:],np.tile([.4375,.5625],(48,1)))
            optima=[] if task['composition']=='empty' else ([.5]*4 if task['composition']=='matched' else [.3,.3,.7,.7])
            np.testing.assert_array_equal(v.optima,optima)
    return True

def simulate(task,modules,technical=False):
    _,pop,reproduction,randomness,_,_=modules
    c,s,v=initial(task,modules);empty=pop.subset(s,np.array([],dtype=int))
    streams={n:randomness.stream(seed(task,technical),n,0) for n in randomness.STREAM_IDS}
    horizon=3 if technical else 200
    arrays={k:[] for k in FIELDS};offsets=[0];means=[];census=[];parentage=[];parent_offsets=[0];returns=[];selection=[]
    for t in range(horizon+1):
        n=len(s.ids);census.append(n);means.append(s.alleles.mean(axis=(0,2)) if n else np.full(3,np.nan))
        for k in FIELDS:arrays[k].append(getattr(s,k).copy())
        offsets.append(offsets[-1]+n)
        if t==horizon:break
        ledger=reproduction.reproduce(s,v,c)
        returns.append([float(getattr(ledger,k).sum()) for k in ('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')])
        w=np.stack([ledger.outcross.sum(axis=0)/2,ledger.outcross.sum(axis=1)/2,ledger.self_viable]);total=w.sum()
        traits=s.alleles.mean(axis=2)
        selection.append(w@(traits-traits.mean(axis=0))/total if total else np.full((3,3),np.nan))
        s,info=pop.advance(s,ledger,empty,c,streams,year=t,mutation_traits=(False,False,True))
        parentage.append(info['parentage']);parent_offsets.append(parent_offsets[-1]+len(info['parentage']))
    result={k:np.concatenate(v) for k,v in arrays.items()}
    result.update(offsets=np.array(offsets),means=np.array(means),population=np.array(census),
        parentage=np.concatenate(parentage),parent_offsets=np.array(parent_offsets),returns=np.array(returns),sexual_selection=np.array(selection))
    return result,asdict(c)

def validate_shapes(arrays,horizon):
    n=len(arrays['ids'])
    required={'ids':(n,),'alleles':(n,3,2),'allele_origin':(n,3,2),'mutation_flags':(n,3,2),
        'birth_years':(n,),'population':(horizon+1,),'means':(horizon+1,3),'offsets':(horizon+2,),
        'parent_offsets':(horizon+1,),'returns':(horizon,8),'sexual_selection':(horizon,3,3)}
    if set(arrays)!=set(required)|{'parentage'}:raise ValueError('Unexpected raw field inventory')
    if any(arrays[k].shape!=shape for k,shape in required.items()):raise ValueError('Raw field shape')
    if any(arrays[k].dtype.kind not in 'iu' for k in ('ids','allele_origin','birth_years','population','offsets','parent_offsets','parentage')) or arrays['mutation_flags'].dtype.kind!='b':raise ValueError('Genealogy dtype')
    if arrays['offsets'][0]!=0 or arrays['offsets'][-1]!=n or arrays['parent_offsets'][0]!=0 or arrays['parentage'].shape!=(int(arrays['parent_offsets'][-1]),3):raise ValueError('Genotype/parent end offsets')
    if (arrays['population']<0).any() or (arrays['population']>48).any() or (arrays['ids']<0).any() or (arrays['allele_origin']<0).any():raise ValueError('Raw integer bounds')
    for t in range(horizon+1):
        lo,hi=arrays['offsets'][t:t+2]
        if lo>hi or len(set(arrays['ids'][lo:hi]))!=hi-lo or (arrays['birth_years'][lo:hi]!=t).any():raise ValueError('Census identity/birth year')
    return True

def verify(arrays,task,modules,horizon):
    validate_shapes(arrays,horizon)
    c,s,v=initial(task,modules)
    if arrays['means'].shape!=(horizon+1,3) or arrays['offsets'].shape!=(horizon+2,) or arrays['parent_offsets'].shape!=(horizon+1,):raise ValueError('Recorded shape')
    np.testing.assert_array_equal(np.diff(arrays['offsets']),arrays['population'])
    np.testing.assert_array_equal(np.diff(arrays['parent_offsets']),arrays['population'][1:])
    if len(arrays['parentage'])!=arrays['parent_offsets'][-1]:raise ValueError('Parentage count')
    for k in FIELDS:np.testing.assert_array_equal(arrays[k][:48],getattr(s,k))
    for t in range(horizon+1):
        lo,hi=arrays['offsets'][t:t+2];a=arrays['alleles'][lo:hi]
        if len(a):np.testing.assert_allclose(a.mean(axis=(0,2)),arrays['means'][t],atol=1e-14,rtol=0)
        elif arrays['population'][t:].any() or not np.isnan(arrays['means'][t:]).all():raise ValueError('Extinct state')
        if not np.isfinite(a).all() or (a<0).any() or (a>1).any():raise ValueError('Allele validity')
        if t:
            pl,ph=arrays['parent_offsets'][t-1:t+1];parents=arrays['parentage'][pl:ph]
            np.testing.assert_array_equal(parents[:,0],arrays['ids'][lo:hi])
            blo,bhi=arrays['offsets'][t-1:t+1];previous_ids=arrays['ids'][blo:bhi]
            if parents.size and not np.isin(parents[:,1:],previous_ids).all():raise ValueError('Parent namespace')
            lookup={int(x):j for j,x in enumerate(previous_ids)}
            previous=arrays['alleles'][blo:bhi]
            for copy in (0,1):
                indices=np.array([lookup[int(x)] for x in parents[:,copy+1]],dtype=int)
                if len(indices) and not (a[:,:2,copy,None]==previous[indices,:2,:]).any(axis=2).all():raise ValueError('Nonmutating inheritance')
    if arrays['returns'].shape!=(horizon,8) or not np.isfinite(arrays['returns']).all():raise ValueError('Return inventory')
    if np.max(np.abs(arrays['returns'][:,0]-arrays['returns'][:,7]-arrays['returns'][:,3]))>1e-10:raise ValueError('Maternal conservation')
    if task['supply']==0 and np.any(arrays['returns'][:,5:8]):raise ValueError('Absent visitor pollen')
    types,pop,reproduction,randomness,_,_=modules
    streams={name:randomness.stream(seed(task,horizon==3),name,0) for name in randomness.STREAM_IDS}
    empty=pop.subset(s,np.array([],dtype=int))
    for t in range(horizon):
        lo,hi=arrays['offsets'][t:t+2]
        state=types.PlantState(**{k:arrays[k][lo:hi] for k in FIELDS})
        ledger=reproduction.reproduce(state,v,c)
        returns=np.array([float(getattr(ledger,k).sum()) for k in ('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')])
        np.testing.assert_allclose(returns,arrays['returns'][t],atol=1e-10,rtol=0)
        w=np.stack([ledger.outcross.sum(axis=0)/2,ledger.outcross.sum(axis=1)/2,ledger.self_viable]);total=w.sum()
        traits=state.alleles.mean(axis=2)
        response=w@(traits-traits.mean(axis=0))/total if total else np.full((3,3),np.nan)
        np.testing.assert_allclose(response,arrays['sexual_selection'][t],atol=1e-12,rtol=0,equal_nan=True)
        child,info=pop.advance(state,ledger,empty,c,streams,year=t,mutation_traits=(False,False,True))
        nlo,nhi=arrays['offsets'][t+1:t+3]
        for k in FIELDS:np.testing.assert_array_equal(getattr(child,k),arrays[k][nlo:nhi])
        pl,ph=arrays['parent_offsets'][t:t+2]
        np.testing.assert_array_equal(info['parentage'],arrays['parentage'][pl:ph])
    return True

def corruption_gate(arrays,task,modules):
    for mode in ('flag','origin','birth','duplicate_id','ledger','response','parent','shape'):
        bad={k:v.copy() for k,v in arrays.items()}
        child=int(bad['offsets'][1])
        if mode=='flag':bad['mutation_flags'][child,2,0]^=True
        elif mode=='origin':bad['allele_origin'][child,2,0]+=1
        elif mode=='birth':bad['birth_years'][child]+=1
        elif mode=='duplicate_id':bad['ids'][child]=bad['ids'][child+1]
        elif mode=='ledger':bad['returns'][0,0]+=.001;bad['returns'][0,3]+=.001
        elif mode=='response':bad['sexual_selection'][0,0,0]+=.001
        elif mode=='parent':bad['parentage'][0,1]=bad['ids'][0] if bad['parentage'][0,1]!=bad['ids'][0] else bad['ids'][1]
        elif mode=='shape':bad['allele_origin']=bad['allele_origin'][:-1]
        try:verify(bad,task,modules,3)
        except (ValueError,AssertionError):continue
        raise ValueError('Technical corruption accepted: '+mode)
    return 8

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--source-dir',required=True);p.add_argument('--out',required=True);p.add_argument('--shard',type=int);p.add_argument('--technical',action='store_true')
    a=p.parse_args();out=Path(a.out)
    if out.exists():raise ValueError('Refuse output replacement')
    if not a.technical and a.shard not in range(9):raise ValueError('Frozen shard')
    if np.__version__!='2.2.6':raise ValueError('Original numerical runtime')
    modules=native(a.input,a.source_dir);validate_inputs(modules);source=modules[-1]
    out.mkdir(parents=True)
    selected=[t for t in tasks() if (t['context'] in (0,1) and t['replicate']==0)] if a.technical else [t for t in tasks() if t['context']==a.shard]
    identity=dict(source_manifest_sha256=source['manifest_sha256'],source_files=source['files'],recipe_sha256={**source['local_sha256'],**source['producer_sha256']},numpy=np.__version__,producer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),technical=a.technical)
    (out/'REGISTRATION.json').write_text(json.dumps(dict(identity=identity,tasks=selected,expected=len(selected),no_new_decision_rules=True),indent=2)+'\n')
    records=[];corruption_checks=0
    for index,t in enumerate(selected):
        result,c=simulate(t,modules,a.technical)
        key=f"{t['block']}_c{t['context']}_r{t['replicate']}";path=out/(key+'.npz')
        metadata=dict(task=t,config=c,identity=identity,seed=seed(t,a.technical),mutation_mask=[False,False,True])
        np.savez_compressed(path,**result,metadata=np.array(json.dumps(metadata,sort_keys=True)))
        with np.load(path,allow_pickle=False) as z:verify({k:z[k] for k in result},t,modules,3 if a.technical else 200)
        if a.technical:corruption_checks+=corruption_gate(result,t,modules)
        records.append(dict(task=t,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),events={str(th):events(result['means'],result['population'],th) for th in (.025,.05,.1)} if not a.technical else None))
        if (index+1)%32==0:print('saved',index+1,'/',len(selected),flush=True)
    (out/'_COMPLETION.json').write_text(json.dumps(dict(status='TECHNICAL_ONLY' if a.technical else 'COMPLETE_FROZEN_ECOLOGICAL_SHARD',identity=identity,cases=len(records),corruption_rejections=corruption_checks,records=records),indent=2)+'\n')

if __name__=='__main__':main()
