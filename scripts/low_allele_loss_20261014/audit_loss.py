"""Retrospective one-transition allele loss; no advance, RNG or new future."""
import argparse
from collections import Counter
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
import zipfile
import numpy as np

OUTER='819741aa4a9f5bc1aaf2dadddbd56b79d158fc9295d07fc3bffe362693fc056a'
INPUT_CASES='5c8e3fe38d7f2953d2ba8b54e716261c7bdc9d4a92bf928182b5fcf621e5e665'
COMPACT='5608ad2cdcbef167fe9062ab5f26318abf2e1bd9'
FIELDS=('ids','alleles','allele_origin','mutation_flags','birth_years')
CLASSES=('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')


def sha(raw):return hashlib.sha256(raw).hexdigest()


def require(ok,message):
    if not ok:raise ValueError(message)


def response(out,selfed,x):
    out=np.asarray(out,dtype=float);selfed=np.asarray(selfed,dtype=float);x=np.asarray(x,dtype=float)
    require(x.ndim==1 and len(x)>0 and selfed.shape==x.shape and out.shape==(len(x),len(x)),'parent shapes differ')
    require(np.isfinite(out).all() and np.isfinite(selfed).all() and np.isfinite(x).all(),'nonfinite parent data')
    require((out>=0).all() and (selfed>=0).all() and ((x>=0)&(x<=1)).all() and (np.diag(out)==0).all(),'invalid parent returns')
    total=float(out.sum()+selfed.sum());require(math.isfinite(total) and total>0,'no finite viable parent returns')
    p=float(x.mean());female=float(np.dot(out.sum(axis=0),x-p)/(2*total))
    paternal=float(np.dot(out.sum(axis=1),x-p)/(2*total));selfpart=float(np.dot(selfed,x-p)/total)
    expected=float((np.dot(out.sum(axis=0)+out.sum(axis=1),x)+2*np.dot(selfed,x))/(2*total))
    none=1-x;q0=float((none@out@none+np.dot(selfed,none*none))/total)
    require(0<=expected<=1 and 0<=q0<=1,'invalid conditional probabilities; no clipping')
    change=expected-p;residual=-expected
    require(abs(change-female-paternal-selfpart)<=1e-12 and abs(-p-change-residual)<=1e-12,'frequency partition failed')
    return dict(current_frequency=p,expected_frequency=expected,parent_weighting_response=change,
        female_response=female,paternal_response=paternal,self_response=selfpart,
        sampling_transmission_residual=residual,observed_change=-p,q0=q0,total_viable=total)


def loss_probability(q0,n):
    require(type(n) is int and n>0 and math.isfinite(q0) and 0<q0<=1,'impossible-law loss or invalid occupied count')
    return q0**n,n*math.log(q0)


def direction(x):return 'favouring_needed' if x>1e-12 else 'opposing_needed' if x < -1e-12 else 'screened_near_zero'


def frozen_sources(folder,captured=None):
    frozen=json.loads((folder/'FROZEN_SOURCES.json').read_bytes())
    if captured is not None:require(frozen==captured,'source manifest changed during execution')
    require(set(frozen)=={'PROTOCOL.md','audit_loss.py','verify_loss.py','test_loss.py','RECIPE_SOURCE.py',
        'native/__init__.py','native/types.py','native/reproduction.py','native/population.py'},'source inventory differs')
    for name,identity in frozen.items():require(sha((folder/name).read_bytes())==identity,'frozen source differs: '+name)
    return frozen


def load_native(folder):
    spec=importlib.util.spec_from_file_location('loss_saved_native',folder/'native/__init__.py',submodule_search_locations=[str(folder/'native')])
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    from loss_saved_native import types,reproduction
    return types,reproduction


def aggregate(rows):
    eligible=[r for r in rows if r['transition_status']=='eligible_loss']
    counts=Counter(r['loss_direction'] for r in eligible)
    return dict(cases=len(rows),eligible_loss=len(eligible),statuses=dict(Counter(r['transition_status'] for r in rows)),
        direction_counts={k:counts[k] for k in ('favouring_needed','opposing_needed','screened_near_zero')},
        original_categories={k:sum(r['original_category']==k for r in rows) for k in CLASSES},
        expected_I_negative_with_needed_opposed=sum(r['saved_expected_I_response'] < -1e-12 and r['loss_direction']=='opposing_needed' for r in eligible),
        partition_max_error=max([r['partition_error'] for r in eligible]+[0.]),
        return_max_error=max([r['return_error'] for r in eligible]+[0.]))


def main():
    ap=argparse.ArgumentParser()
    for name in ('outer','compact','cases','out'):ap.add_argument('--'+name,type=Path,required=True)
    args=ap.parse_args();folder=Path(__file__).parent;frozen=frozen_sources(folder)
    require(not args.out.exists(),'refuse existing output')
    raw=args.outer.read_bytes();require(sha(raw)==OUTER,'original outer differs')
    compactraw=args.compact.read_bytes();require(hashlib.sha1(b'blob '+str(len(compactraw)).encode()+b'\0'+compactraw).hexdigest()==COMPACT,'compact differs')
    providers={r['file']:r['sha256'] for r in json.loads(compactraw)['provider_receipts']}
    casesraw=args.cases.read_bytes();require(sha(casesraw)==INPUT_CASES,'fixed first-loss cases differ')
    prior=list(csv.DictReader(io.StringIO(casesraw.decode())));prior={(r['block'],int(r['context']),int(r['replicate'])):r for r in prior}
    require(len(prior)==2304,'fixed case inventory differs')
    types,reproduction=load_native(folder);rows=[];seen=set()
    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        for context in range(9):
            member=outer.read(f'shard_{context}.zip');require(sha(member)==providers[f'shard_{context}.zip'],'provider differs')
            with zipfile.ZipFile(io.BytesIO(member)) as shard:
                records=json.loads(shard.read('_COMPLETION.json'))['records'];require(len(records)==256,'provider case count differs')
                for record in records:
                    task=record['task'];key=(task['block'],context,task['replicate']);require(key not in seen and task['context']==context,'case identity differs');seen.add(key)
                    before=prior[key];rawcase=shard.read(f'{key[0]}_c{context}_r{key[2]}.npz');require(sha(rawcase)==record['sha256']==before['raw_sha256'],'case bytes differ')
                    with np.load(io.BytesIO(rawcase),allow_pickle=False) as z:a={n:z[n].copy() for n in z.files}
                    meta=json.loads(str(a['metadata'].item()));require(meta['task']==task and meta['mutation_mask']==[False,False,True],'case source law differs')
                    for name in ('types.py','reproduction.py','population.py'):
                        require(meta['identity']['source_files']['scripts/model3_island/'+name]==frozen['native/'+name],'archived biological source differs')
                    cfg=types.Config.from_dict(meta['config'])
                    require(cfg.survival==0 and cfg.seed_arrival.supply==0 and cfg.capacity==48 and cfg.years==200,'demographic law differs')
                    require(record['events']['0.05']['category']==before['original_category'] and before['original_category'] in CLASSES,'original event category changed')
                    row=dict(block=key[0],context=context,replicate=key[2],raw_sha256=sha(rawcase),original_category=before['original_category'],
                        first_exclusion=int(before['first_exclusion']) if before['first_exclusion'] else None,
                        exclusion_before_fixation=before['exclusion_before_fixation']=='True')
                    h=row['first_exclusion'];row['transition_status']='no_exclusion' if h is None else 'initially_excluded' if h==0 else 'eligible_loss'
                    if h is not None and h>0:
                        lo,hi=a['offsets'][h-1:h+1];nlo,nhi=a['offsets'][h:h+2];alleles=a['alleles'][lo:hi];target=float(before['target'])
                        require(hi>lo and nhi>nlo and hi-lo==int(a['population'][h-1]) and nhi-nlo==int(a['population'][h]),'occupied loss census differs')
                        needed=alleles[:,1,:]<=target;child_needed=a['alleles'][nlo:nhi,1,:]<=target
                        require(needed.sum()>0 and child_needed.sum()==0 and not a['mutation_flags'][lo:nhi,1,:].any(),'needed allele loss differs')
                        state=types.PlantState(**{field:a[field][lo:hi] for field in FIELDS})
                        optima=[] if task['composition']=='empty' else [.5]*4 if task['composition']=='matched' else [.3,.3,.7,.7]
                        visitors=types.VisitorState(np.arange(len(optima),dtype=np.int64),np.asarray(optima,dtype=float),np.full(len(optima),.2),np.ones(len(optima)))
                        ledger=reproduction.reproduce(state,visitors,cfg)
                        returns=np.array([float(getattr(ledger,name).sum()) for name in ('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')])
                        error=float(np.max(np.abs(returns-a['returns'][h-1])));require(error<=1e-12,'saved native returns differ')
                        weights=(ledger.outcross.sum(axis=0)+ledger.outcross.sum(axis=1))/2+ledger.self_viable
                        phenotype=alleles[:,1,:].mean(axis=1);expectedI=float(np.dot(weights,phenotype-phenotype.mean())/weights.sum())
                        savedI=float(a['sexual_selection'][h-1,:,1].sum());require(abs(expectedI-savedI)<=1e-12,'saved expected I response differs')
                        result=response(ledger.outcross,ledger.self_viable,needed.mean(axis=1));n=int(nhi-nlo)
                        prob,logprob=loss_probability(result['q0'],n)
                        pl,ph=a['parent_offsets'][h-1:h+1];parentage=a['parentage'][pl:ph]
                        require(len(parentage)==n and np.array_equal(parentage[:,0],a['ids'][nlo:nhi]) and np.isin(parentage[:,1:],a['ids'][lo:hi]).all(),'resident child parentage differs')
                        row.update(result,loss_direction=direction(result['parent_weighting_response']),needed_copies_before=int(needed.sum()),
                            original_parent_census=int(hi-lo),retained_resident_count=n,target=target,conditional_loss_probability=prob,
                            log_conditional_loss_probability=logprob,saved_expected_I_response=savedI,return_error=error,
                            partition_error=abs(result['parent_weighting_response']-result['female_response']-result['paternal_response']-result['self_response']))
                    rows.append(row)
    require(seen==set(prior),'all-start scope differs');frozen_sources(folder,frozen)
    rows.sort(key=lambda r:(r['block'],r['context'],r['replicate']))
    result=dict(status='LAST_LOSS_CONDITIONAL_PARENT_AND_TRANSMISSION_ACCOUNTING_NOT_HISTORICAL_CAUSAL_SHARES',**aggregate(rows),
        cells=[dict(block=b,context=c,**aggregate([r for r in rows if (r['block'],r['context'])==(b,c)])) for b in ('main','confirmation') for c in range(9)],
        original_outer_sha256=OUTER,input_cases_sha256=INPUT_CASES,source_sha256=frozen['audit_loss.py'],protocol_sha256=frozen['PROTOCOL.md'],
        new_biological_histories=0,reproduction_advances=0,limits=['Loss-selected one-transition probabilities, not prospective hazards/p-values.',
            'Residual combines parent choice and segregation, not pure drift or unique historical mediation.',
            'No assurance causation, continuous ecological root or natural-order future benefit identified.'])
    args.out.mkdir(parents=True,exist_ok=False)
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (args.out/'ALL_CASES.csv').open('x',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    result['cases_sha256']=sha((args.out/'ALL_CASES.csv').read_bytes())
    with (args.out/'READOUT.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cells'},indent=2))


if __name__=='__main__':main()
