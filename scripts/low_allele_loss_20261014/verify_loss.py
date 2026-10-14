"""Independent scalar and gamete-enumeration verification; no producer import."""
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
CLASSES=('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')


def sha(raw):return hashlib.sha256(raw).hexdigest()


def check(ok,message):
    if not ok:raise ValueError(message)


def source_gate(folder,captured=None):
    pins=json.loads((folder/'FROZEN_SOURCES.json').read_bytes())
    if captured is not None:check(pins==captured,'source manifest changed during verification')
    check(set(pins)=={'PROTOCOL.md','audit_loss.py','verify_loss.py','test_loss.py','RECIPE_SOURCE.py',
        'native/__init__.py','native/types.py','native/reproduction.py','native/population.py'},'source inventory differs')
    for name,pin in pins.items():check(sha((folder/name).read_bytes())==pin,'source differs')
    return pins


def main():
    p=argparse.ArgumentParser()
    for name in ('outer','compact','cases','output','receipt'):p.add_argument('--'+name,type=Path,required=True)
    args=p.parse_args();check(not args.receipt.exists(),'refuse existing receipt')
    folder=Path(__file__).parent;pins=source_gate(folder)
    raw=args.outer.read_bytes();check(sha(raw)=='819741aa4a9f5bc1aaf2dadddbd56b79d158fc9295d07fc3bffe362693fc056a','outer differs')
    compactraw=args.compact.read_bytes();check(hashlib.sha1(b'blob '+str(len(compactraw)).encode()+b'\0'+compactraw).hexdigest()=='5608ad2cdcbef167fe9062ab5f26318abf2e1bd9','compact differs')
    providers={r['file']:r['sha256'] for r in json.loads(compactraw)['provider_receipts']}
    priorraw=args.cases.read_bytes();check(sha(priorraw)=='5c8e3fe38d7f2953d2ba8b54e716261c7bdc9d4a92bf928182b5fcf621e5e665','prior cases differ')
    priorrows=list(csv.DictReader(io.StringIO(priorraw.decode())))
    old={(r['block'],int(r['context']),int(r['replicate'])):r for r in priorrows};check(len(old)==len(priorrows)==2304,'prior scope differs')
    readout_raw=(args.output/'READOUT.json').read_bytes();readout=json.loads(readout_raw)
    cases_raw=(args.output/'ALL_CASES.csv').read_bytes();check(sha(cases_raw)==readout['cases_sha256'],'cases identity differs')
    rows=list(csv.DictReader(io.StringIO(cases_raw.decode())))
    supplied={(r['block'],int(r['context']),int(r['replicate'])):r for r in rows};check(len(supplied)==len(rows)==2304,'case scope differs')
    spec=importlib.util.spec_from_file_location('loss_verify_native',folder/'native/__init__.py',submodule_search_locations=[str(folder/'native')])
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    from loss_verify_native import types,reproduction
    observed=[];checks=0;gamete_checks=0;max_error=0.;seen=set()
    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        for c in range(9):
            member=outer.read(f'shard_{c}.zip');check(sha(member)==providers[f'shard_{c}.zip'],'provider differs')
            with zipfile.ZipFile(io.BytesIO(member)) as shard:
                records=json.loads(shard.read('_COMPLETION.json'))['records'];check(len(records)==256,'source scope differs')
                for record in records:
                    task=record['task'];key=(task['block'],c,task['replicate']);check(key not in seen and task['context']==c,'source key differs');seen.add(key)
                    before=old[key];actual=supplied[key];r=dict(block=key[0],context=c,replicate=key[2],original_category=record['events']['0.05']['category'])
                    check(actual['original_category']==r['original_category']==before['original_category'],'category differs')
                    h=int(before['first_exclusion']) if before['first_exclusion'] else None
                    r['transition_status']='no_exclusion' if h is None else 'initially_excluded' if h==0 else 'eligible_loss'
                    check(actual['transition_status']==r['transition_status'] and actual['first_exclusion']==before['first_exclusion'],'loss event differs')
                    rawcase=shard.read(f'{key[0]}_c{c}_r{key[2]}.npz');check(sha(rawcase)==record['sha256']==before['raw_sha256']==actual['raw_sha256'],'raw differs')
                    if h is not None and h>0:
                        with np.load(io.BytesIO(rawcase),allow_pickle=False) as z:a={n:z[n].copy() for n in z.files}
                        metadata=json.loads(str(a['metadata'].item()));check(metadata['task']==task and metadata['mutation_mask']==[False,False,True],'source law differs')
                        for name in ('types.py','reproduction.py','population.py'):
                            check(metadata['identity']['source_files']['scripts/model3_island/'+name]==pins['native/'+name],'native identity differs')
                        cfg=types.Config.from_dict(metadata['config']);check(cfg.survival==0 and cfg.seed_arrival.supply==0,'demographic law differs')
                        lo,hi=map(int,a['offsets'][h-1:h+1]);nlo,nhi=map(int,a['offsets'][h:h+2]);n=nhi-nlo
                        initial=float(a['alleles'][:int(a['offsets'][1]),1,:].mean());target=initial-.05
                        check(target==float(before['target']) and hi>lo and n>0,'reference/census differs')
                        alleles=a['alleles'][lo:hi,1,:]
                        g=[[int(float(v)<=target) for v in pair] for pair in alleles]
                        count=sum(sum(pair) for pair in g);check(count>0 and not (a['alleles'][nlo:nhi,1,:]<=target).any(),'needed-copy loss differs')
                        check(not a['mutation_flags'][lo:nhi,1,:].any(),'I mutation differs')
                        state=types.PlantState(**{name:a[name][lo:hi] for name in ('ids','alleles','allele_origin','mutation_flags','birth_years')})
                        optima=[] if task['composition']=='empty' else [.5]*4 if task['composition']=='matched' else [.3,.3,.7,.7]
                        visitor=types.VisitorState(np.arange(len(optima),dtype=np.int64),np.array(optima,dtype=float),np.full(len(optima),.2),np.ones(len(optima)))
                        ledger=reproduction.reproduce(state,visitor,cfg)
                        out=ledger.outcross;selfed=ledger.self_viable;weights=[];zero_terms=[];expected_terms=[];I_terms=[]
                        I_means=[math.fsum(float(v) for v in pair)/2 for pair in alleles]
                        current_I=math.fsum(I_means)/len(I_means)
                        female=[];paternal=[];self_terms=[];pold=count/(2*len(g))
                        for father in range(len(g)):
                            for mother in range(len(g)):
                                w=float(out[father,mother])+(float(selfed[father]) if father==mother else 0.)
                                check(math.isfinite(w) and w>=0,'invalid source parent weight')
                                weights.append(w)
                                I_terms.append(w*((I_means[father]+I_means[mother])/2-current_I))
                                if w:
                                    outcomes=[(g[father][i],g[mother][j]) for i in range(2) for j in range(2)]
                                    zero_terms.append(w*sum(u+v==0 for u,v in outcomes)/4)
                                    expected_terms.append(w*math.fsum((u+v)/2 for u,v in outcomes)/4)
                                    gamete_checks+=4
                                female.append(float(out[father,mother])*(sum(g[mother])/2-pold)/2)
                                paternal.append(float(out[father,mother])*(sum(g[father])/2-pold)/2)
                            self_terms.append(float(selfed[father])*(sum(g[father])/2-pold))
                        total=math.fsum(weights);check(total>0,'no source returns')
                        expected=math.fsum(expected_terms)/total;q0=math.fsum(zero_terms)/total
                        check(0<q0<=1,'impossible-law loss')
                        delta=expected-pold;direction='favouring_needed' if delta>1e-12 else 'opposing_needed' if delta < -1e-12 else 'screened_near_zero'
                        r['loss_direction']=direction;check(direction==actual['loss_direction'],'direction differs')
                        returns=[float(getattr(ledger,name).sum()) for name in ('maternal','paternal','self_raw','self_viable','ovules','exported','delivered','outcross')]
                        return_error=max(abs(v-float(a['returns'][h-1,j])) for j,v in enumerate(returns));check(return_error<=1e-12,'return error exceeds gate')
                        savedI=math.fsum(float(v) for v in a['sexual_selection'][h-1,:,1])
                        check(abs(math.fsum(I_terms)/total-savedI)<=1e-12,'scalar expected I diagnostic differs')
                        fpart=math.fsum(female)/total;ppart=math.fsum(paternal)/total;spart=math.fsum(self_terms)/total
                        quantities=dict(current_frequency=pold,expected_frequency=expected,parent_weighting_response=delta,
                            female_response=fpart,paternal_response=ppart,self_response=spart,sampling_transmission_residual=-expected,
                            observed_change=-pold,q0=q0,total_viable=total,needed_copies_before=count,original_parent_census=hi-lo,
                            retained_resident_count=n,target=target,conditional_loss_probability=q0**n,log_conditional_loss_probability=n*math.log(q0),
                            saved_expected_I_response=savedI,return_error=return_error,partition_error=abs(delta-fpart-ppart-spart))
                        for name,value in quantities.items():
                            error=abs(float(actual[name])-value);max_error=max(max_error,error);check(error<=1e-12,'scalar quantity differs: '+name);checks+=1
                        r.update(quantities)
                    observed.append(r)
    check(seen==set(old)==set(supplied),'full domain differs')
    def summary(selected):
        eligible=[r for r in selected if r['transition_status']=='eligible_loss']
        return dict(cases=len(selected),eligible_loss=len(eligible),statuses=dict(Counter(r['transition_status'] for r in selected)),
            direction_counts={k:sum(r['loss_direction']==k for r in eligible) for k in ('favouring_needed','opposing_needed','screened_near_zero')},
            original_categories={k:sum(r['original_category']==k for r in selected) for k in CLASSES},
            expected_I_negative_with_needed_opposed=sum(r['saved_expected_I_response'] < -1e-12 and r['loss_direction']=='opposing_needed' for r in eligible),
            partition_max_error=max([r['partition_error'] for r in eligible]+[0.]),return_max_error=max([r['return_error'] for r in eligible]+[0.]))
    cells=readout['cells'];check(len(cells)==18 and {(r['block'],r['context']) for r in cells}=={(b,c) for b in ('main','confirmation') for c in range(9)},'cell inventory differs')
    for expected,saved in [(summary(observed),readout)]+[(summary([r for r in observed if (r['block'],r['context'])==(cell['block'],cell['context'])]),cell) for cell in cells]:
        for name,value in expected.items():
            if type(value) is float:check(abs(saved[name]-value)<=1e-12,'summary closure differs')
            else:check(saved[name]==value,'summary differs: '+name)
    check(readout['new_biological_histories']==readout['reproduction_advances']==0 and readout['source_sha256']==pins['audit_loss.py'],'executed scope differs')
    source_gate(folder,pins)
    result=dict(status='ALL2304_LAST_LOSS_RECORDS_INDEPENDENTLY_VERIFIED',cases=2304,eligible_loss=readout['eligible_loss'],
        scalar_checks=checks,gamete_enumerations=gamete_checks,max_scalar_error=max_error,
        readout_sha256=sha(readout_raw),cases_sha256=sha(cases_raw),verifier_sha256=pins['verify_loss.py'],
        producer_imported=False,new_biological_histories=0,reproduction_advances=0)
    with args.receipt.open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
