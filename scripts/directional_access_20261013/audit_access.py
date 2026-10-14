"""Retrospective directional allele-support bound, no biological execution."""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile
import numpy as np

OUTER_SHA='819741aa4a9f5bc1aaf2dadddbd56b79d158fc9295d07fc3bffe362693fc056a'
COMPACT_BLOB='5608ad2cdcbef167fe9062ab5f26318abf2e1bd9'
LAW_SHA='c03fc6fccdf4efb660ece8fa5ee016d4de14f84f3b234dfb6322666b89ec34c1'
PRODUCER_SHA='cd9779c89c643c9daf4a9c9001ce14dcf5d3cf95300d98f50c4ba3a4d1998fae'
CLASSES=('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')


def digest(raw):return hashlib.sha256(raw).hexdigest()


def require(ok,message):
    if not ok:raise ValueError(message)


def excluded(minimum_scaled,initial_scaled_sum,initial_n):
    require(initial_n>0,'empty founder state')
    return 10*initial_n*int(minimum_scaled)>5*int(initial_scaled_sum)-4*initial_n


def events(means,census):
    result={}
    for label,trait,direction in [('A',2,1),('I',1,-1)]:
        flags=(census>0)&(direction*(means[:,trait]-means[0,trait])>=.05)
        hits=np.flatnonzero(np.convolve(flags.astype(int),np.ones(20,dtype=int),mode='valid')==20)
        result[label]=int(hits[0]) if len(hits) else None
    a,i=result['A'],result['I']
    result['category']=('neither' if a is None and i is None else 'investment_only' if a is None
                        else 'assurance_only' if i is None else 'near_simultaneous' if abs(a-i)<=5
                        else 'assurance_first' if a<i else 'investment_first')
    return result


def homolog_matches(values,origins,chosen,child_values,child_origins):
    return ((values[chosen]==child_values[:,None]) & (origins[chosen]==child_origins[:,None])).any(axis=1)


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


def describe_case(a,original):
    schema(a)
    offsets=a['offsets'];census=a['population'];means=a['means']
    require(offsets.shape==(202,) and census.shape==(201,) and means.shape==(201,3),'original shapes differ')
    require(offsets[0]==0 and offsets[-1]==len(a['ids']) and np.array_equal(np.diff(offsets),census),'census/genome offsets differ')
    require(np.all((census>=0)&(census<=48)) and census[0]==48,'original census domain differs')
    require(np.isfinite(means[census>0]).all() and np.isnan(means[census==0]).all(),'undefined trait means differ')
    require(events(means,census)==original,'original biological events differ')
    first_extinct=next((t for t,n in enumerate(census) if n==0),None)
    require(first_extinct is None or not np.any(census[first_extinct:]),'extinction not absorbing')
    minimum=np.full(201,np.nan);maximum=minimum.copy();allele_var=minimum.copy();phenotype_var=minimum.copy()
    support=np.zeros(201,dtype=int);blocked=np.zeros(201,dtype=bool)
    require(a['parent_offsets'].shape==(201,) and a['parent_offsets'][0]==0 and a['parent_offsets'][-1]==len(a['parentage']), 'parent offsets differ')
    require(np.array_equal(np.diff(a['parent_offsets']),census[1:]),'birth/parent count offsets differ')
    founder=a['alleles'][offsets[0]:offsets[1],1,:]
    require(np.isfinite(founder).all() and np.isin(founder,[.375,.5,.625]).all(),'invalid founder standing support')
    scaled=np.rint(founder*8).astype(int);s0=int(scaled.sum());n0=int(census[0])
    target=float(founder.mean())-.05
    first_block=None;first_fixed=None;inheritance_checks=0
    for t,n in enumerate(census):
        lo,hi=offsets[t:t+2]
        require(len(np.unique(a['ids'][lo:hi]))==n,'duplicate living ID')
        if not n:continue
        alleles=a['alleles'][lo:hi,1,:];origins=a['allele_origin'][lo:hi,1,:]
        require(alleles.shape==(n,2) and np.isfinite(alleles).all(),'invalid living I genome')
        require(np.isin(alleles,[.375,.5,.625]).all() and not a['mutation_flags'][lo:hi,1,:].any(),'I standing support or mutation law differs')
        require(abs(float(alleles.mean())-means[t,1])<=1e-12,'archived I phenotype mean differs')
        minimum[t]=alleles.min();maximum[t]=alleles.max();support[t]=len(np.unique(alleles))
        allele_var[t]=np.var(alleles);phenotype_var[t]=np.var(alleles.mean(axis=1))
        blocked[t]=excluded(int(round(minimum[t]*8)),s0,n0)
        require(blocked[t]==(minimum[t]>target),'integer/float support boundary differs')
        if blocked[t]:require(minimum[t]-target>1e-12,'support boundary lacks numerical separation')
        if first_block is None and blocked[t]:first_block=t
        if first_fixed is None and support[t]==1:first_fixed=t
        if t==200:continue
        nxlo,nxhi=offsets[t+1:t+3];offspring=int(census[t+1])
        start,end=a['parent_offsets'][t:t+2];parents=a['parentage'][start:end]
        require(parents.shape==(offspring,3) and np.array_equal(parents[:,0],a['ids'][nxlo:nxhi]),'birth/parent IDs differ')
        index={int(pid):i for i,pid in enumerate(a['ids'][lo:hi])}
        for role in (0,1):
            try:chosen=np.array([index[int(pid)] for pid in parents[:,role+1]],dtype=int)
            except KeyError as exc:raise ValueError('unknown recorded parent') from exc
            child_values=a['alleles'][nxlo:nxhi,1,role]
            child_origins=a['allele_origin'][nxlo:nxhi,1,role]
            matches=homolog_matches(alleles,origins,chosen,child_values,child_origins)
            require(np.all(matches),'I child homolog not inherited from recorded parent')
            inheritance_checks+=offspring
    living=np.flatnonzero(census>0)
    require(np.all(np.diff(minimum[living])>=0),'I support lower bound decreased')
    if first_block is not None:
        require(np.all(blocked[living[living>=first_block]]),'directional access recovered without a source')
        if original['I'] is not None:require(original['I']+19<first_block,'source I window contradicts bound')
    row=dict(first_exclusion=first_block,first_single_allele_fixation=first_fixed,
             initial_I=float(founder.mean()),target=target,terminal_alive=bool(census[-1]>0),
             terminal_support=int(support[-1]),terminal_excluded=bool(blocked[-1]),
             exclusion_support=int(support[first_block]) if first_block is not None else None,
             exclusion_allele_variance=float(allele_var[first_block]) if first_block is not None else None,
             exclusion_phenotype_variance=float(phenotype_var[first_block]) if first_block is not None else None,
             exclusion_before_fixation=first_block is not None and (first_fixed is None or first_block<first_fixed),
             missing_I=original['I'] is None,original_A=original['A'],original_I=original['I'],
             original_category=original['category'],inheritance_checks=inheritance_checks)
    return row,(minimum,maximum,support,allele_var,phenotype_var)


def summarize(rows):
    return dict(cases=len(rows),original_categories={k:sum(r['original_category']==k for r in rows) for k in CLASSES},
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
    ap=argparse.ArgumentParser();ap.add_argument('--outer',type=Path,required=True);ap.add_argument('--compact',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--frozen',type=Path,required=True);args=ap.parse_args()
    require(not args.out.exists(),'refuse existing output')
    frozen=json.loads(args.frozen.read_bytes());folder=Path(__file__).parent
    names={'PROTOCOL.md','audit_access.py','verify_access.py','test_access.py','POPULATION_SOURCE.py'}
    def source_gate():
        require(set(frozen)==names,'frozen source inventory differs')
        for name,identity in frozen.items():require(digest((folder/name).read_bytes())==identity,'frozen source differs: '+name)
        require(frozen['POPULATION_SOURCE.py']==LAW_SHA,'native inheritance law differs')
    source_gate()
    compact_raw=args.compact.read_bytes();require(hashlib.sha1(f'blob {len(compact_raw)}\0'.encode()+compact_raw).hexdigest()==COMPACT_BLOB,'original compact differs')
    compact=json.loads(compact_raw);outer_raw=args.outer.read_bytes();require(digest(outer_raw)==OUTER_SHA,'original outer differs')
    providers={r['file']:r['sha256'] for r in compact['provider_receipts']};rows=[];series=[];seen=set()
    with zipfile.ZipFile(io.BytesIO(outer_raw)) as outer:
        for c in range(9):
            shard_raw=outer.read(f'shard_{c}.zip');require(digest(shard_raw)==providers[f'shard_{c}.zip'],'provider differs')
            with zipfile.ZipFile(io.BytesIO(shard_raw)) as shard:
                records=json.loads(shard.read('_COMPLETION.json'))['records'];require(len(records)==256,'provider count differs')
                for rec in records:
                    task=rec['task'];key=(task['block'],c,task['replicate']);require(key not in seen and task['context']==c,'wrong/duplicate task');seen.add(key)
                    raw=shard.read(f'{key[0]}_c{c}_r{key[2]}.npz');require(digest(raw)==rec['sha256'],'original case differs')
                    with np.load(io.BytesIO(raw),allow_pickle=False) as z:a={name:z[name].copy() for name in z.files}
                    meta=json.loads(str(a['metadata'].item()));cfg=meta['config']
                    require(meta['task']==task and meta['mutation_mask']==[False,False,True] and cfg['survival']==0 and cfg['seed_arrival']['supply']==0,'biological access law differs')
                    require(meta['identity']['source_files']['scripts/model3_island/population.py']==LAW_SHA and meta['identity']['producer_sha256']==PRODUCER_SHA,'source identity differs')
                    row,values=describe_case(a,rec['events']['0.05']);row.update(block=key[0],context=c,replicate=key[2],raw_sha256=rec['sha256'])
                    rows.append(row);series.append(values)
    require(seen=={(b,c,r) for b in ('main','confirmation') for c in range(9) for r in range(128)},'incomplete original cohort')
    tables=[]
    for cell in compact['cells']:
        selected=[r for r in rows if (r['block'],r['context'])==(cell['block'],cell['context'])]
        counts={k:sum(r['original_category']==k for r in selected) for k in CLASSES};require(counts==cell['categories'],'source categories differ')
        tables.append(dict(block=cell['block'],context=cell['context'],**summarize(selected)))
    order=sorted(range(len(rows)),key=lambda j:(rows[j]['block'],rows[j]['context'],rows[j]['replicate']))
    rows=[rows[j] for j in order];series=np.asarray([series[j] for j in order])
    source_gate();args.out.mkdir(parents=True,exist_ok=False)
    np.savez_compressed(args.out/'ALL_CENSUS_SUPPORT.npz',keys=np.array([f"{r['block']}_c{r['context']}_r{r['replicate']}" for r in rows]),
        minimum=series[:,0],maximum=series[:,1],support_size=series[:,2].astype(int),allele_variance=series[:,3],phenotype_variance=series[:,4])
    with (args.out/'ALL_CASES.csv').open('x',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    result=dict(status='SOURCE_STRUCTURAL_DIRECTIONAL_ACCESS_NOT_CAUSAL_LOSS_ATTRIBUTION',**summarize(rows),cells=tables,
        inheritance_checks=sum(r['inheritance_checks'] for r in rows),census_checks=2304*201,new_biological_histories=0,
        outer_sha256=OUTER_SHA,compact_git_blob=COMPACT_BLOB,population_source_sha256=LAW_SHA,
        source_sha256=frozen['audit_access.py'],protocol_sha256=frozen['PROTOCOL.md'],
        arrays_sha256=digest((args.out/'ALL_CENSUS_SUPPORT.npz').read_bytes()),cases_sha256=digest((args.out/'ALL_CASES.csv').read_bytes()),
        limits=['Retrospective original cohort; no independent confirmation or significance test.',
                'No attribution of allele loss to selection/drift or causal A-order benefit.',
                'No continuous ecological root; absence of exclusion does not establish attainability.',
                'Same law only: I mutation/immigration could reopen access; no natural irreversibility claim.'])
    with (args.out/'READOUT.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cells'},indent=2))


if __name__=='__main__':main()
