"""Independent scalar/set ancestry and support audit; no producer imports."""
import argparse
from collections import Counter
import csv
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path
import zipfile
import numpy as np


def sha(raw):return hashlib.sha256(raw).hexdigest()


def require(ok,message):
    if not ok:raise ValueError(message)


def schema(a):
    needed={'ids','alleles','allele_origin','mutation_flags','birth_years','population','means','offsets','parent_offsets','parentage'}
    require(needed<=set(a),'missing source fields')
    for name in ('ids','allele_origin','birth_years','population','offsets','parent_offsets','parentage'):
        require(a[name].dtype.kind in 'iu','integer source field required: '+name)
    require(a['ids'].ndim==1,'ID shape differs');n=len(a['ids'])
    require(a['alleles'].shape==(n,3,2) and a['allele_origin'].shape==(n,3,2),'diploid shape differs')
    require(a['mutation_flags'].shape==(n,3,2) and a['mutation_flags'].dtype.kind=='b','boolean mutation flags required')
    require(a['birth_years'].shape==(n,) and a['population'].shape==(201,) and a['means'].shape==(201,3),'annual field shapes differ')
    require(a['offsets'].shape==(202,) and a['parent_offsets'].shape==(201,), 'offset shapes differ')
    require(a['parentage'].ndim==2 and a['parentage'].shape[1]==3,'parentage shape differs')
    require(np.isfinite(a['alleles']).all() and np.all((a['alleles']>=0)&(a['alleles']<=1)),'invalid diploid values')


def cell_inventory(cells):
    require(len(cells)==18 and all(type(c['context']) is int for c in cells),'cell inventory size/type differs')
    actual=[(c['block'],c['context']) for c in cells]
    expected={(b,c) for b in ('main','confirmation') for c in range(9)}
    require(len(set(actual))==18 and set(actual)==expected,'cell inventory duplicate/missing')


def event(means,pop):
    result={}
    for name,column,sign in [('A',2,1),('I',1,-1)]:
        found=None;run=0
        for t,n in enumerate(pop):
            run=run+1 if n>0 and sign*(float(means[t,column])-float(means[0,column]))>=.05 else 0
            if run==20:found=t-19;break
        result[name]=found
    a,i=result['A'],result['I']
    if a is None and i is None:kind='neither'
    elif a is None:kind='investment_only'
    elif i is None:kind='assurance_only'
    elif abs(a-i)<=5:kind='near_simultaneous'
    else:kind='assurance_first' if a<i else 'investment_first'
    result['category']=kind
    return result


def aggregate(rows):
    return dict(cases=len(rows),original_categories={k:sum(r['original_category']==k for r in rows) for k in ('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')},
        ever_excluded=sum(r['first_exclusion'] is not None for r in rows),
        excluded_before_fixation=sum(r['exclusion_before_fixation'] for r in rows),
        excluded_at_fixation=sum(r['first_exclusion'] is not None and r['first_exclusion']==r['first_single_allele_fixation'] for r in rows),
        excluded_with_expressed_variance=sum(r['exclusion_before_fixation'] and r['exclusion_phenotype_variance']>0 for r in rows),
        missing_I_terminal_excluded_alive=sum(r['missing_I'] and r['terminal_alive'] and r['terminal_excluded'] for r in rows),
        missing_I_excluded_before_fixation=sum(r['missing_I'] and r['exclusion_before_fixation'] for r in rows),
        missing_I_not_excluded_alive=sum(r['missing_I'] and r['terminal_alive'] and not r['terminal_excluded'] for r in rows),
        terminal_extinct=sum(not r['terminal_alive'] for r in rows),
        A_only_excluded_before_A_completion=sum(r['original_category']=='assurance_only' and r['first_exclusion'] is not None and r['first_exclusion']<r['original_A']+19 for r in rows),
        A_only_excluded_at_A_completion=sum(r['original_category']=='assurance_only' and r['first_exclusion'] is not None and r['first_exclusion']==r['original_A']+19 for r in rows),
        A_only_excluded_after_A_completion=sum(r['original_category']=='assurance_only' and r['first_exclusion'] is not None and r['first_exclusion']>r['original_A']+19 for r in rows))


def main():
    p=argparse.ArgumentParser();p.add_argument('--outer',type=Path,required=True);p.add_argument('--compact',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--frozen',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);args=p.parse_args()
    require(not args.receipt.exists(),'refuse existing receipt')
    frozen=json.loads(args.frozen.read_bytes());folder=Path(__file__).parent
    def sources():
        require(set(frozen)=={'PROTOCOL.md','audit_access.py','verify_access.py','test_access.py','POPULATION_SOURCE.py'},'source inventory differs')
        for name,identity in frozen.items():require(sha((folder/name).read_bytes())==identity,'source identity differs')
        require(frozen['POPULATION_SOURCE.py']=='c03fc6fccdf4efb660ece8fa5ee016d4de14f84f3b234dfb6322666b89ec34c1','native law differs')
    sources()
    raw=args.outer.read_bytes();require(sha(raw)=='819741aa4a9f5bc1aaf2dadddbd56b79d158fc9295d07fc3bffe362693fc056a','outer differs')
    compact_raw=args.compact.read_bytes();require(hashlib.sha1(f'blob {len(compact_raw)}\0'.encode()+compact_raw).hexdigest()=='5608ad2cdcbef167fe9062ab5f26318abf2e1bd9','compact differs')
    compact=json.loads(compact_raw);providers={x['file']:x['sha256'] for x in compact['provider_receipts']}
    readout_raw=(args.output/'READOUT.json').read_bytes();readout=json.loads(readout_raw)
    cell_inventory(readout['cells'])
    cases_raw=(args.output/'ALL_CASES.csv').read_bytes();arrays_raw=(args.output/'ALL_CENSUS_SUPPORT.npz').read_bytes()
    require(sha(cases_raw)==readout['cases_sha256'] and sha(arrays_raw)==readout['arrays_sha256'],'output identity differs')
    table=list(csv.DictReader(io.StringIO(cases_raw.decode('utf-8'))));bykey={(r['block'],int(r['context']),int(r['replicate'])):r for r in table}
    require(len(table)==len(bykey)==2304,'all-case inventory differs')
    with np.load(io.BytesIO(arrays_raw),allow_pickle=False) as z:saved={name:z[name].copy() for name in z.files}
    require(len(saved['keys'])==len(set(saved['keys']))==2304,'array keys differ')
    positions={str(key):j for j,key in enumerate(saved['keys'])}
    for name in ('minimum','maximum','support_size','allele_variance','phenotype_variance'):
        require(saved[name].shape==(2304,201),'array shapes differ')
    rows=[];seen=set();ancestry=0;scalar_checks=0;max_error=0.
    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        for c in range(9):
            shard_raw=outer.read(f'shard_{c}.zip');require(sha(shard_raw)==providers[f'shard_{c}.zip'],'provider differs')
            with zipfile.ZipFile(io.BytesIO(shard_raw)) as shard:
                records=json.loads(shard.read('_COMPLETION.json'))['records'];require(len(records)==256,'case count differs')
                for record in records:
                    task=record['task'];key=(task['block'],c,task['replicate']);require(key not in seen and task['context']==c,'task identity differs');seen.add(key)
                    case_raw=shard.read(f'{key[0]}_c{c}_r{key[2]}.npz');require(sha(case_raw)==record['sha256'],'case differs')
                    with np.load(io.BytesIO(case_raw),allow_pickle=False) as z:a={name:z[name].copy() for name in z.files}
                    schema(a)
                    meta=json.loads(str(a['metadata'].item()));cfg=meta['config']
                    require(meta['task']==task and meta['mutation_mask']==[False,False,True] and cfg['survival']==0 and cfg['seed_arrival']['supply']==0,'source conditions differ')
                    require(meta['identity']['source_files']['scripts/model3_island/population.py']==frozen['POPULATION_SOURCE.py'] and meta['identity']['producer_sha256']=='cd9779c89c643c9daf4a9c9001ce14dcf5d3cf95300d98f50c4ba3a4d1998fae','archived source differs')
                    offs=a['offsets'];pop=a['population'];means=a['means'];actual=event(means,pop)
                    require(actual==record['events']['0.05'],'original events differ')
                    require(np.array_equal(np.diff(offs),pop) and np.array_equal(np.diff(a['parent_offsets']),pop[1:]),'census/parent offsets differ')
                    first=a['alleles'][offs[0]:offs[1],1,:];initial=float(first.mean());cut=Fraction(sum(int(round(v*8)) for v in first.ravel()),16*len(first))-Fraction(1,20)
                    h=None;f=None;prev=None;first_var=first_pvar=None;first_size=None;terminal_excluded=False;case_ancestry=0
                    position=positions[f'{key[0]}_c{c}_r{key[2]}']
                    for t,n in enumerate(pop):
                        lo,hi=offs[t:t+2]
                        if n==0:
                            require(not np.any(pop[t:]),'resurrection')
                            for name in ('minimum','maximum','allele_variance','phenotype_variance'):require(math.isnan(float(saved[name][position,t])),'undefined descriptor replaced')
                            require(saved['support_size'][position,t]==0,'extinct support nonzero');continue
                        values=a['alleles'][lo:hi,1,:];origins=a['allele_origin'][lo:hi,1,:]
                        require(not a['mutation_flags'][lo:hi,1,:].any(),'I mutation flag')
                        alleles=[float(v) for v in values.ravel()];support=set(alleles)
                        require(support<=set([.375,.5,.625]),'standing support changed')
                        if prev is not None:require(support<=prev,'support expanded')
                        prev=support
                        mean=math.fsum(alleles)/len(alleles);phen=[(float(x)+float(y))/2 for x,y in values]
                        avar=math.fsum((v-mean)**2 for v in alleles)/len(alleles)
                        pvar=math.fsum((v-mean)**2 for v in phen)/len(phen)
                        lower=min(support);excluded=Fraction(int(round(lower*8)),8)>cut
                        if excluded:
                            require(lower-(initial-.05)>1e-12,'numerical boundary ambiguity')
                            if h is None:h=t;first_var=avar;first_pvar=pvar;first_size=len(support)
                        if len(support)==1 and f is None:f=t
                        if t==200:terminal_excluded=excluded
                        descriptors={'minimum':lower,'maximum':max(support),'support_size':len(support),'allele_variance':avar,'phenotype_variance':pvar}
                        for name,value in descriptors.items():
                            observed=float(saved[name][position,t]);require(math.isfinite(observed),'nonfinite living descriptor');max_error=max(max_error,abs(observed-value));scalar_checks+=1
                        require(abs(mean-float(means[t,1]))<=1e-12,'archived mean differs')
                        if t<200:
                            nl,nh=offs[t+1:t+3];ps,pe=a['parent_offsets'][t:t+2];parents=a['parentage'][ps:pe]
                            require(parents.shape==(pop[t+1],3) and np.array_equal(parents[:,0],a['ids'][nl:nh]),'parentage count/child differs')
                            ids={int(pid):j for j,pid in enumerate(a['ids'][lo:hi])}
                            for child,record_parent in enumerate(parents):
                                for role in (0,1):
                                    parent=ids[int(record_parent[role+1])]
                                    pair=(float(a['alleles'][nl+child,1,role]),int(a['allele_origin'][nl+child,1,role]))
                                    choices={(float(values[parent,j]),int(origins[parent,j])) for j in (0,1)}
                                    require(pair in choices,'parent homolog mismatch');case_ancestry+=1
                    if h is not None and actual['I'] is not None:require(actual['I']+19<h,'completed I window contradicts support')
                    row=dict(first_exclusion=h,first_single_allele_fixation=f,initial_I=initial,target=initial-.05,
                        terminal_alive=bool(pop[-1]>0),terminal_support=int(saved['support_size'][position,-1]),terminal_excluded=terminal_excluded,
                        exclusion_support=first_size,exclusion_allele_variance=first_var,exclusion_phenotype_variance=first_pvar,
                        exclusion_before_fixation=h is not None and (f is None or h<f),missing_I=actual['I'] is None,
                        original_A=actual['A'],original_I=actual['I'],original_category=actual['category'],inheritance_checks=case_ancestry,
                        block=key[0],context=c,replicate=key[2],raw_sha256=record['sha256'])
                    for field,value in row.items():
                        supplied=bykey[key][field]
                        if type(value) is float:
                            require(math.isfinite(float(supplied)),'nonfinite case value');max_error=max(max_error,abs(float(supplied)-value))
                        else:require(supplied==('' if value is None else str(value)),'all-case field differs: '+field)
                    rows.append(row);ancestry+=case_ancestry
    require(seen=={(b,c,r) for b in ('main','confirmation') for c in range(9) for r in range(128)},'incomplete all-start scope')
    summary=aggregate(rows)
    for name,value in summary.items():require(readout[name]==value,'summary differs: '+name)
    for cell in readout['cells']:
        expected=aggregate([r for r in rows if (r['block'],r['context'])==(cell['block'],cell['context'])])
        for name,value in expected.items():require(cell[name]==value,'cell table differs')
    require(ancestry==readout['inheritance_checks'] and readout['new_biological_histories']==0 and max_error<=1e-12,'admission/closure failed')
    require(readout['source_sha256']==frozen['audit_access.py'] and readout['protocol_sha256']==frozen['PROTOCOL.md'],'execution identity differs')
    sources()
    receipt=dict(status='ALL2304_DIRECTIONAL_SUPPORT_AND_ANCESTRY_INDEPENDENTLY_VERIFIED',cases=2304,census_descriptor_checks=scalar_checks,
        parent_homolog_checks=ancestry,max_scalar_error=max_error,readout_sha256=sha(readout_raw),cases_sha256=sha(cases_raw),arrays_sha256=sha(arrays_raw),
        verifier_sha256=frozen['verify_access.py'],producer_imported=False,new_biological_histories=0)
    with args.receipt.open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
