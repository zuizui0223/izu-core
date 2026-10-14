"""Approved bounded variation intervention; archived biological operators unchanged."""
from pathlib import Path
from dataclasses import replace
import argparse,copy,hashlib,importlib.util,io,json,zipfile
import numpy as np

FIELDS=('ids','alleles','allele_origin','mutation_flags','birth_years')
PROTOCOL=Path(__file__).resolve().parents[1]/'docs/CHAPTER2_INVESTMENT_VARIATION_RESTORATION_PROTOCOL_20261013.md'
def sha(b):return hashlib.sha256(b).hexdigest()

def restore_alleles(a):
    a=np.asarray(a,dtype=float)
    if a.ndim!=3 or a.shape[1:]!=(3,2) or not len(a) or not np.isfinite(a).all():
        raise ValueError('occupied diploid state required')
    v=a[0,1,0]
    if not np.all(a[:,1,:]==v) or v<1/16 or v>15/16:
        raise ValueError('interior investment allele fixation required')
    b=a.copy();b[:,1,0]=v-1/16;b[:,1,1]=v+1/16
    if not np.allclose(b.mean(axis=2),a.mean(axis=2),atol=1e-15,rtol=0):
        raise ValueError('expressed mean changed')
    return b

def primary(rows):
    blocks=('causal_main','causal_confirmation')
    if len(rows)!=64 or any(sum(r['block']==b for r in rows)!=32 for b in blocks):
        raise ValueError('frozen 64-history block inventory')
    if any(r['original_I'] is None or r['restored_I'] is None for r in rows):
        return dict(decision='not_evaluable',reason='undefined_extinct_terminal_trait',pairs=64)
    x=np.array([[r['original_I']-r['restored_I'] for r in rows if r['block']==b] for b in blocks])
    if not np.isfinite(x).all():raise ValueError('nonfinite terminal trait')
    rng=np.random.default_rng(2026101364)
    draws=np.mean(np.take_along_axis(np.broadcast_to(x,(19999,2,32)),rng.integers(0,32,(19999,2,32)),axis=2),axis=(1,2))
    lo,hi=np.quantile(draws,[.025,.975]);bm=x.mean(axis=1)
    decision='supported_restored_reduction' if lo>0 and np.all(bm>0) else 'supported_opposite' if hi<0 and np.all(bm<0) else 'unresolved'
    return dict(decision=decision,estimate=float(x.mean()),ci95=[float(lo),float(hi)],block_estimates=dict(zip(blocks,bm.tolist())),pairs=64)

def write_new(p,obj):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2,allow_nan=False);f.write('\n')

def audit_module():
    p=Path(__file__).with_name('audit_genome_response_accounting_20261013.py')
    s=importlib.util.spec_from_file_location('original_accounting',p)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def states(a,types,t):
    lo,hi=a['offsets'][t:t+2]
    return types.PlantState(**{k:a[k][lo:hi] for k in FIELDS})

def context(a,source,types,randomness):
    m=json.loads(str(a['metadata'].item()));task=m['task']
    ident=m['identity']
    if (ident['source']['source_manifest']!=source['manifest_sha256']
        or ident['source']['local']!=source['local_sha256']
        or ident['producer']!=source['producer_sha256']):raise ValueError('original native source identity drift')
    seed=int.from_bytes(hashlib.sha256(('izu-assurance-causal-v1-28470909\0'+task['pair_key']).encode()).digest()[:16],'big')
    if seed!=m['seed']:raise ValueError('original stream seed drift')
    c=types.Config.from_dict(m['config'])
    if c.survival!=0 or c.seed_arrival.supply!=0 or c.years!=200 or tuple(m['mutation_mask'])!=(False,False,True):
        raise ValueError('frozen annual/mutation law drift')
    optima=source['campaign_design']['compositions'][task['composition']]
    v=types.VisitorState(np.arange(len(optima),dtype=np.int64),np.array(optima),np.full(len(optima),.2),np.ones(len(optima)))
    streams={n:randomness.stream(seed,n,0) for n in randomness.STREAM_IDS}
    return m,c,v,streams

def trigger(a):
    for t in range(201):
        lo,hi=a['offsets'][t:t+2];v=a['alleles'][lo:hi,1,:]
        if len(v) and np.all(v==v.flat[0]):return t
    return None

def replay(a,source,native):
    types,pop,reproduction,randomness=native;m,c,v,streams=context(a,source,types,randomness)
    s=states(a,types,0);empty=pop.subset(s,np.empty(0,dtype=int));tr=trigger(a);saved=None
    maximum=0.;checks=0
    for t in range(201):
        wanted=states(a,types,t)
        for k in FIELDS:
            actual=getattr(s,k);expected=getattr(wanted,k)
            if actual.shape!=expected.shape:raise ValueError('original annual shape drift')
            if k=='alleles':
                e=float(np.max(np.abs(actual-expected))) if actual.size else 0.;maximum=max(maximum,e)
                if e>1e-12:raise ValueError('original annual allele drift')
            elif not np.array_equal(actual,expected):raise ValueError('original annual '+k+' drift')
            checks+=1
        if t==tr:saved=copy.deepcopy(streams)
        if t==200:break
        s,info=pop.advance(s,reproduction.reproduce(s,v,c),empty,c,streams,year=t,mutation_traits=tuple(m['mutation_mask']))
        lo,hi=a['parent_offsets'][t:t+2]
        if not np.array_equal(info['parentage'],a['parentage'][lo:hi]):raise ValueError('original parentage drift')
        checks+=1
    return dict(trigger=tr,streams=saved,maximum=maximum,checks=checks)

def continue_case(a,source,native,admitted):
    types,pop,reproduction,randomness=native;m,c,v,_=context(a,source,types,randomness)
    tr=admitted['trigger'];start=tr if tr is not None else 200
    s=states(a,types,start)
    if tr is not None:s=replace(s,alleles=restore_alleles(s.alleles))
    streams=admitted['streams'];empty=pop.subset(s,np.empty(0,dtype=int))
    snapshots=[];parentage=[];rows=[]
    for t in range(start,201):
        snapshots.append({k:getattr(s,k).copy() for k in FIELDS})
        n=len(s.ids);traits=s.alleles.mean(axis=2);ledger=reproduction.reproduce(s,v,c)
        weights=np.stack([ledger.outcross.sum(axis=0)/2,ledger.outcross.sum(axis=1)/2,ledger.self_viable])
        total=weights.sum()
        response=(weights@(traits-traits.mean(axis=0))/total).sum(axis=0) if n and total else None
        rows.append(dict(year=t,census=n,mean=traits.mean(axis=0).tolist() if n else None,
            allele_variance=s.alleles.var(axis=(0,2)).tolist() if n else None,
            expressed_variance=traits.var(axis=0).tolist() if n else None,
            expected_response=response.tolist() if response is not None else None,
            maternal=float(ledger.maternal.sum()),paternal=float(ledger.paternal.sum()),
            outcross=float(ledger.outcross.sum()),self_viable=float(ledger.self_viable.sum())))
        if t==200:break
        s,info=pop.advance(s,ledger,empty,c,streams,year=t,mutation_traits=tuple(m['mutation_mask']))
        parentage.append(info['parentage'])
    original=states(a,types,200)
    return snapshots,parentage,dict(task=m['task'],trigger=tr,half_width=1/16 if tr is not None else None,
        original_I=float(original.alleles[:,1,:].mean()) if len(original.ids) else None,
        restored_I=float(s.alleles[:,1,:].mean()) if len(s.ids) else None,
        original_census=len(original.ids),restored_census=len(s.ids),rows=rows,
        original_case_sha256=None,scope='diagnostic allele restoration, not naturally occurring mutation')

def main():
    p=argparse.ArgumentParser();p.add_argument('--cohort',type=Path,required=True);p.add_argument('--source-input',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);args=p.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=False)
    auditor=audit_module();source=auditor.prepare_source(args.source_input,out/'source');native=auditor.load_native(source)
    if sha(args.cohort.read_bytes())!=auditor.COHORT_SHA:raise ValueError('original cohort identity')
    ph=sha(PROTOCOL.read_bytes());code=sha(Path(__file__).read_bytes());cases=[]
    with zipfile.ZipFile(args.cohort) as z:
        for name in sorted(n for n in z.namelist() if '/assurance_causal_campaign_' in n and n.endswith('.npz')):
            receipt=json.loads(z.read(name[:-4]+'.json'));task=receipt['task']
            if task['supply']!=.125 or task['composition']!='matched':continue
            raw=z.read(name)
            if sha(raw)!=receipt['sha256'] or receipt['technical']:raise ValueError('case receipt')
            with np.load(io.BytesIO(raw),allow_pickle=False) as f:a={k:f[k].copy() for k in f.files}
            if json.loads(str(a['metadata'].item()))['identity']!=receipt['identity']:raise ValueError('case source identity')
            cases.append((a,receipt,replay(a,source,native)))
            print('native admitted',len(cases),flush=True)
    keys=[r['task']['key'] for _,r,_ in cases]
    if len(set(keys))!=64 or any(sum(r['task']['block']==b for _,r,_ in cases)!=32 for b in ('causal_main','causal_confirmation')):raise ValueError('64 inventory')
    write_new(out/'NATIVE_ADMISSION.json',dict(status='64_native_complete',protocol_sha256=ph,code_sha256=code,
        checks=sum(x['checks'] for _,_,x in cases),max_allele_error=max(x['maximum'] for _,_,x in cases),keys=keys))
    results=[]
    for a,receipt,admitted in cases:
        snapshots,parents,r=continue_case(a,source,native,admitted);r['original_case_sha256']=receipt['sha256']
        key=r['task']['key'];rawpath=out/(key+'.npz')
        offsets=np.concatenate([[0],np.cumsum([len(x['ids']) for x in snapshots])]);po=np.concatenate([[0],np.cumsum([len(x) for x in parents])])
        arrays={k:np.concatenate([x[k] for x in snapshots],axis=0) for k in FIELDS}
        arrays.update(offsets=offsets,parent_offsets=po,parentage=np.concatenate(parents) if parents else np.empty((0,3),dtype=np.int64),metadata=np.array(json.dumps(r,allow_nan=False)))
        with rawpath.open('xb') as f:np.savez_compressed(f,**arrays)
        r['raw_sha256']=sha(rawpath.read_bytes());write_new(out/(key+'.json'),r)
        results.append(dict(block=r['task']['block'],original_I=r['original_I'],restored_I=r['restored_I'],key=key,raw_sha256=r['raw_sha256']))
        print('restored slot',len(results),flush=True)
    if sha(PROTOCOL.read_bytes())!=ph or sha(Path(__file__).read_bytes())!=code:raise ValueError('frozen source changed')
    write_new(out/'READOUT.json',dict(status='COMPLETE_PRODUCER_NOT_INDEPENDENTLY_VERIFIED',protocol_sha256=ph,code_sha256=code,
        original_cohort_sha256=auditor.COHORT_SHA,original_input_sha256=auditor.INPUT_SHA,primary=primary(results),cases=results))

if __name__=='__main__':main()
