"""Raw arithmetic/inheritance audit. Imports neither model nor producer.

Archive admission checks allocation, identities and arithmetic. Donor-source
linkage, reproductive probabilities and assay biology require separate checks.
"""
import hashlib
import itertools
import json
from pathlib import Path
import re
import zipfile

import numpy as np
from scipy.stats import beta


FIELDS=('alleles','allele_origin','mutation_flags','ids','birth_years')


def _canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def admit_manifest(manifest,contract):
    """Check every declared allocation before opening any trajectory file."""
    require(set(manifest)=={'format','contract_sha256','cohorts','futures'} and
            manifest['format']=='readaptation_manifest_v1','manifest schema')
    require(manifest['contract_sha256']==hashlib.sha256(_canonical(contract)).hexdigest(),
            'manifest contract mismatch')
    cohorts=list(itertools.product(contract['founder_indices'],contract['visitor_indices'],
                                   contract['donor_policies'],range(contract['cohort_draws'])))
    keys=[(*k,d,c,r) for k in cohorts
          for d in range(1+len(contract['activity'])*len(contract['optima']))
          for c in contract['future_costs'] for r in range(contract['future_repeats'])]
    def sha(value):
        return isinstance(value,str) and re.fullmatch('[0-9a-f]{64}',value) is not None
    admitted={}
    for row in manifest['cohorts']:
        require(set(row)=={'key','cohort_sha256'},'cohort receipt schema')
        key=tuple(row['key'])
        require(key in cohorts and key not in admitted and sha(row['cohort_sha256']),
                'cohort receipt mismatch')
        admitted[key]=row['cohort_sha256']
    require(set(admitted)==set(cohorts),'missing cohort receipt')
    seen=set(); filenames=set(); expected=set(keys)
    for row in manifest['futures']:
        require(set(row)=={'key','file','sha256','bytes'},'future receipt schema')
        key=tuple(row['key']); filename=row['file']
        require(key in expected and key not in seen,'unknown/duplicate future allocation')
        require(isinstance(filename,str) and re.fullmatch('[a-z0-9_-]+[.]npz',filename)
                and filename not in filenames,'unsafe or duplicate future path')
        require(sha(row['sha256']) and type(row['bytes']) is int and 0<row['bytes']<=16*1024**2,
                'future receipt hash/size')
        seen.add(key); filenames.add(filename)
    require(seen==expected,'missing future allocation')
    return keys,admitted


def audit_archive(path,contract):
    """Audit complete future directory under the repository's exact proposal.

    PASS here never admits donor provenance or authorizes a production run.
    """
    root=Path(__file__).resolve().parents[1]
    frozen=json.loads((root/'docs/protocols/CHAPTER2_READAPTATION_PROPOSED_20261019.json').read_text())
    require(_canonical(contract)==_canonical(frozen),'archive contract differs from proposal')
    for name,digest in frozen['source_sha256'].items():
        require(hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,'pinned source hash mismatch')
    base=json.loads((root/'data/design/model3_island_v2.json').read_text())['base_config']
    path=Path(path)
    manifest=json.loads((path/'manifest.json').read_text(encoding='utf8'))
    return _audit_files(path,manifest,contract,base)


def _audit_files(path,manifest,contract,base):
    """Internal streaming reader; contract and base must already be admitted."""
    path=Path(path)
    keys,cohorts=admit_manifest(manifest,contract)
    expected={row['file'] for row in manifest['futures']}
    require({p.name for p in path.glob('*.npz')}==expected,'future file inventory mismatch')
    summaries=[]
    for receipt in manifest['futures']:
        file=path/receipt['file']
        require(not file.is_symlink() and file.is_file(),'future path must be a regular file')
        require(file.stat().st_size==receipt['bytes'],'future file size mismatch')
        key=receipt['key']; cohort_sha=cohorts[tuple(key[:4])]
        record=load_future(file,receipt['sha256'],key)
        audit_identity(record,key,contract,base,cohort_sha)
        summary=audit_future(record)
        summary.update(key=key,cohort_sha256=cohort_sha)
        summaries.append(summary)
        del record
    result=summarize_allocations(summaries,keys)
    result.update(status='PASS_FUTURE_ARCHIVE_INTERNAL',source_admission=False,
                  biological_replay=False,
                  contract_sha256=manifest['contract_sha256'],
                  limitation='Cohort digests agree internally; donor source and native biological replay remain unverified')
    return result


def audit_identity(d,key,contract,base_config,cohort_sha256):
    """Bind raw metadata to an externally admitted contract/base/cohort digest.

    This does not itself verify the supplied contract or the donor archive.
    Configuration is compared in full, including fields not changed by treatment.
    """
    require(len(key)==7,'allocation key shape')
    f,v,policy,cohort,destination,cost,repeat=key
    require(all(type(x) is int for x in (f,v,cohort,destination,repeat)),'integer allocation indices')
    require(f in contract['founder_indices'] and v in contract['visitor_indices']
            and policy in contract['donor_policies'] and 0<=cohort<contract['cohort_draws']
            and 0<=repeat<contract['future_repeats'] and cost in contract['future_costs']
            and 0<=destination<1+len(contract['activity'])*len(contract['optima']),
            'allocation key outside contract')
    seed=int.from_bytes(hashlib.sha256(_canonical([contract['namespace'],'future',list(key)])).digest()[:16],'big')
    require(type(d['stream_key']) is int and d['stream_key']==seed,'future stream mismatch')
    require(raw_state_digest(d,0)==cohort_sha256,'initial cohort mismatch')
    expected=json.loads(json.dumps(base_config))
    expected.update(capacity=contract['capacity'],years=contract['horizon'],
                    assurance_mode=contract['future_assurance_mode'],assurance_cost=cost,
                    assurance_timing=contract['assurance_timing'],pollen_discount=contract['pollen_discount'],
                    depression=contract['depression'],survival=contract['survival'],
                    mutation_rate=contract['mutation_rate'],ovule_budget=contract['future_budget'],
                    activity_mode=contract['activity_mode'])
    expected['seed_arrival']['supply']=0
    expected['visitor_arrival']['supply']=0
    if destination==0:
        expected['activity']=0
        visitors=dict(ids=[],optima=[],breadths=[],effectiveness=[])
    else:
        ai,mi=divmod(destination-1,len(contract['optima']))
        expected['activity']=float(contract['activity'][ai])
        optima=contract['optima'][mi]; n=len(optima)
        visitors=dict(ids=list(range(n)),optima=optima,breadths=[contract['breadth']]*n,
                      effectiveness=[float(contract['effectiveness'])]*n)
    # Numeric equality is appropriate for validated Config scalar values;
    # canonical JSON handles tuple/list normalization after serialization.
    require(json.loads(_canonical(d['config']))==expected,'future configuration mismatch')
    require(d['visitors']==visitors,'future destination mismatch')


def load_future(path,expected_sha256,expected_key):
    """Read one bounded NPZ independently of the writer; no pickle or extraction."""
    path=Path(path)
    require(path.stat().st_size<=16*1024**2,'compressed future size bound')
    require(hashlib.sha256(path.read_bytes()).hexdigest()==expected_sha256,'future hash mismatch')
    with zipfile.ZipFile(path) as archive:
        infos=archive.infolist()
        names=[info.filename for info in infos]
        require(len(names)==len(set(names)),'duplicate archive member')
        require(sum(info.file_size for info in infos)<=16*1024**2,'expanded future size bound')
        require('__metadata__.npy' in names,'missing future metadata')
    with np.load(path,allow_pickle=False) as archive:
        raw=archive['__metadata__']
        require(raw.ndim==1 and raw.dtype==np.dtype('uint8'),'metadata representation')
        header=json.loads(raw.tobytes().decode('utf8'))
        require(set(header)=={'format','key','metadata','arrays'} and
                header['format']=='readaptation_npz_v1','archive format')
        require(json.dumps(header['key'])==json.dumps(list(expected_key)),'future key mismatch')
        keys=header['arrays']
        require(isinstance(keys,list) and all(isinstance(k,str) for k in keys)
                and len(keys)==len(set(keys)),'array inventory')
        require(set(names)=={k+'.npy' for k in keys}|{'__metadata__.npy'},'archive inventory mismatch')
        metadata=header['metadata']
        require(isinstance(metadata,dict) and not set(keys)&set(metadata),'metadata inventory')
        json.dumps(metadata,allow_nan=False)
        result=dict(metadata)
        for key in keys:
            value=archive[key]
            require(value.dtype.kind in 'biuf','non-numeric archive array')
            result[key]=value
    return result


def require(condition,message):
    if not condition:
        raise ValueError(message)


def raw_state_digest(d,t):
    digest=hashlib.sha256()
    start,end=d['state_offsets'][t:t+2]
    for name in FIELDS:
        a=np.ascontiguousarray(d['state_'+name][start:end])
        header=json.dumps([name,a.shape,a.dtype.str],sort_keys=True,
                          separators=(',',':'),allow_nan=False).encode()
        digest.update(header); digest.update(a.tobytes())
    return digest.hexdigest()


def audit_cohort(donor,cohort,receipt):
    """Check recorded offspring against recorded donor parents, without biology.

    Donor linkage to the original archive and probability replay are external.
    """
    for state,field in ((donor,'donor_sha256'),(cohort,'cohort_sha256')):
        n=len(state['ids'])
        for name in FIELDS:
            value=np.asarray(state[name])
            shape=(n,3,2) if name in FIELDS[:3] else (n,)
            require(value.shape==shape,'cohort state dimensions')
        require(len(set(state['ids']))==n,'duplicate source/cohort IDs')
        raw={'state_'+k:state[k] for k in FIELDS}
        raw['state_offsets']=np.array([0,n])
        require(raw_state_digest(raw,0)==receipt[field],'cohort/donor digest mismatch')
    n=len(cohort['ids']); source_n=len(donor['ids'])
    potential=receipt['source_production']
    require(type(potential) is int and potential>=0 and receipt['propagule_cap']==12
            and receipt['transferred']==n==min(potential,12),'source production/cap mismatch')
    require(np.array_equal(cohort['ids'],np.arange(n)) and (cohort['birth_years']==0).all(),
            'cohort entry identity/clock')
    require(receipt['allocated'] is True and receipt['cohort_key'][2]==receipt['donor_assurance_mode'],
            'cohort historical policy')
    total=receipt['expected_viable_production']
    require(np.isfinite(total) and total>=0,'expected source production')
    probabilities=np.asarray(receipt['parent_probability_matrix'],dtype=float)
    if source_n==0:
        require(probabilities.size==0 and n==0 and total==0,'empty donor production')
        probabilities=np.empty((0,0))
    require(probabilities.shape==(source_n,source_n) and np.isfinite(probabilities).all()
            and (probabilities>=0).all(),'parent matrix')
    require(np.isclose(probabilities.sum(),1 if total>0 else 0,rtol=0,atol=1e-12),
            'parent matrix normalization')
    require(total>0 or potential==0,'zero production cannot produce offspring')
    mothers=receipt['mother_source_ids']; fathers=receipt['father_source_ids']
    require(len(mothers)==len(fathers)==n,'parent receipt length')
    lookup={int(v):i for i,v in enumerate(donor['ids'])}
    for i,(mother,father) in enumerate(zip(mothers,fathers)):
        require(mother in lookup and father in lookup,'source parent missing')
        require(probabilities[lookup[father],lookup[mother]]>0,'impossible parent pair')
        for side,parent in enumerate((mother,father)):
            for locus in range(3):
                require(any(all(cohort[name][i,locus,side]==donor[name][lookup[parent],locus,k]
                                for name in FIELDS[:3]) for k in range(2)),
                        'source offspring inheritance mismatch')
    return dict(status='PASS_COHORT_PARENTAGE',transferred=n,
                donor_archive_admission=False,production_probability_replay=False)


def _assay(a,n):
    require(a['population']==n and a['occupied']==bool(n)
            and a['reference_competitors']==47,'assay population/context')
    names=('maternal_outcross','paternal_outcross','viable_self','genetic_return')
    v=[np.asarray(a[k],dtype=float) for k in names]
    require(all(x.shape==(n,) and np.isfinite(x).all() and (x>=0).all() for x in v),
            'assay component shape or value')
    require(np.allclose(.5*v[0]+.5*v[1]+v[2],v[3],rtol=0,atol=1e-12),'assay return')
    if n:
        require(np.isclose(a['mean_genetic_return'],v[3].mean(),rtol=0,atol=1e-12),'assay mean')
    else:
        require(a['mean_genetic_return'] is None,'empty assay must be undefined')
    return a['mean_genetic_return']


def audit_future(d):
    require(d['schema']=='readaptation_future_v1' and d['horizon']==80,'future schema/horizon')
    pop=np.asarray(d['population'])
    require(pop.shape==(81,) and pop.dtype.kind in 'iu' and ((pop>=0)&(pop<=48)).all(),
            'population inventory')
    offsets=np.asarray(d['state_offsets'])
    require(offsets.dtype.kind in 'iu' and np.array_equal(offsets,np.r_[0,np.cumsum(pop)]),'state offsets')
    total=int(pop.sum())
    for name in FIELDS:
        a=np.asarray(d['state_'+name])
        shape=(total,3,2) if name in FIELDS[:3] else (total,)
        kind='f' if name=='alleles' else 'b' if name=='mutation_flags' else 'iu'
        require(a.shape==shape and a.dtype.kind in kind,'raw state shape/type')
    alleles=d['state_alleles']; origins=d['state_allele_origin']; flags=d['state_mutation_flags']
    require(np.isfinite(alleles).all() and ((alleles>=0)&(alleles<=1)).all(),'allele range')
    require(len(d['state_sha256'])==81,'missing census digest')
    parent_offsets=np.asarray(d['parentage_offsets'])
    require(parent_offsets.dtype.kind in 'iu' and
            np.array_equal(parent_offsets,np.r_[0,np.cumsum(pop[1:])]),'parent offsets')
    parents=np.asarray(d['parentage'])
    require(parents.shape==(int(pop[1:].sum()),3) and parents.dtype.kind in 'iu','parent inventory')
    means=np.full((81,3),np.nan)
    variances=means.copy(); lows=means.copy(); highs=means.copy()
    for t in range(81):
        lo,hi=offsets[t:t+2]
        require(raw_state_digest(d,t)==d['state_sha256'][t],'state digest mismatch')
        ids=d['state_ids'][lo:hi]
        require(len(set(ids))==len(ids),'duplicate individual IDs')
        require(np.all(d['state_birth_years'][lo:hi]==t),'birth census mismatch')
        if pop[t]:
            traits=alleles[lo:hi].mean(axis=2)
            means[t]=traits.mean(axis=0); variances[t]=traits.var(axis=0)
            lows[t]=alleles[lo:hi].min(axis=(0,2)); highs[t]=alleles[lo:hi].max(axis=(0,2))
        if t:
            p=parents[parent_offsets[t-1]:parent_offsets[t]]
            require(np.array_equal(p[:,0],ids),'child IDs mismatch')
            oldlo,oldhi=offsets[t-1:t+1]
            lookup={int(v):oldlo+i for i,v in enumerate(d['state_ids'][oldlo:oldhi])}
            for i,row in enumerate(p):
                for side,parent_id in enumerate(row[1:]):
                    require(int(parent_id) in lookup,'missing parent')
                    parent=lookup[int(parent_id)]
                    for locus in range(3):
                        require(any(alleles[lo+i,locus,side]==alleles[parent,locus,k]
                                    and origins[lo+i,locus,side]==origins[parent,locus,k]
                                    and flags[lo+i,locus,side]==flags[parent,locus,k]
                                    for k in range(2)),'inheritance mismatch')
    for key,expected in [('trait_mean',means),('trait_variance',variances),
                         ('allele_min',lows),('allele_max',highs)]:
        observed=np.asarray(d[key])
        require(observed.shape==expected.shape and np.allclose(observed,expected,rtol=0,
                atol=1e-12,equal_nan=True),'trait summary mismatch')
    absent=np.flatnonzero(pop==0)
    extinction=int(absent[0]) if len(absent) else None
    require(d['first_extinction']==extinction,'extinction time mismatch')
    require(extinction is None or not pop[extinction:].any(),'reappearance without immigration')
    first=_assay(d['assays']['0'],int(pop[0]))
    last=_assay(d['assays']['80'],int(pop[-1]))
    return dict(status='PASS_RAW_STATE_ARITHMETIC',initial_population=int(pop[0]),
                final_population=int(pop[-1]),occupied=bool(pop[-1]),first_extinction=extinction,
                change=(means[-1]-means[0]).tolist() if pop[0] and pop[-1] else None,
                assay_change=last-first if first is not None and last is not None else None,
                limitation='No allocation admission or biological probability replay')


def indicator_interval(count,n):
    """Exact binomial bounds conditional on one fixed starting cohort/environment."""
    require(type(count) is int and type(n) is int and 0<=count<=n and n>0,'indicator counts')
    low=0. if count==0 else float(beta.ppf(.025,count,n-count+1))
    high=1. if count==n else float(beta.ppf(.975,count+1,n-count))
    upper=1. if count==n else float(beta.ppf(.95,count+1,n-count))
    return dict(count=count,denominator=n,proportion=count/n,interval_95=[low,high],
                one_sided_upper_95=upper,scope='pointwise conditional; not simultaneous')


def summarize_allocations(rows,expected_keys):
    """Summarize admitted rows; caller must independently admit raw archives first.

    Expected keys come from the frozen contract, never from observed successes.
    Cohorts are kept separate; this helper does not validate a production contract.
    """
    expected=[tuple(k) for k in expected_keys]
    require(len(expected)==len(set(expected)) and len(expected)>0,'duplicate/empty expected allocation')
    require(all(len(k)==7 for k in expected),'allocation key shape')
    expected_set=set(expected)
    seen=set(); hashes={}; groups={}
    for row in rows:
        key=tuple(row['key'])
        require(key in expected_set and key not in seen,'unknown or duplicate allocation')
        seen.add(key)
        cohort=key[:4]
        digest=row['cohort_sha256']
        require(isinstance(digest,str) and len(digest)==64 and
                all(c in '0123456789abcdef' for c in digest),'invalid cohort digest')
        require(cohort not in hashes or hashes[cohort]==digest,'cohort identity mismatch')
        hashes[cohort]=digest
        require(type(row['occupied']) is bool,'occupancy must be boolean')
        if row['occupied']:
            change=np.asarray(row['change'],dtype=float)
            require(change.shape==(3,) and np.isfinite(change).all(),'occupied trait change')
            require(row['first_extinction'] is None,'survivor extinction inconsistency')
            require(isinstance(row['assay_change'],(int,float)) and np.isfinite(row['assay_change']),
                    'occupied assay change')
        else:
            require(row['change'] is None and row['assay_change'] is None,'extinct traits must be undefined')
            require(type(row['first_extinction']) is int and 0<=row['first_extinction']<=80,
                    'extinction census')
        groups.setdefault(key[:6],[]).append(row)
    require(seen==expected_set,'missing allocation')
    summaries=[]; lookup={}
    for key,values in sorted(groups.items()):
        values.sort(key=lambda r:r['key'][-1])
        require([r['key'][-1] for r in values]==list(range(32)),
                'each cohort/destination requires its own 32 repeats')
        n=len(values)
        alive=[r for r in values if r['occupied']]
        directions={}
        for locus,name in enumerate(('M','I','A')):
            counts=dict(negative=0,zero=0,positive=0,extinct=n-len(alive))
            for row in alive:
                value=row['change'][locus]
                counts['positive' if value>0 else 'negative' if value<0 else 'zero']+=1
            directions[name]={label:indicator_interval(count,n) for label,count in counts.items()}
        summary=dict(key=list(key),repeats=n,occupancy=indicator_interval(len(alive),n),
                     directions=directions,
                     survivor_mean_change=np.mean([r['change'] for r in alive],axis=0).tolist() if alive else None,
                     survivor_mean_assay_change=float(np.mean([r['assay_change'] for r in alive])) if alive else None,
                     changes_by_repeat=[r['change'] for r in values],
                     extinction_censuses_by_repeat=[r['first_extinction'] for r in values])
        summaries.append(summary); lookup[key]=summary
    pairs=[]
    for key,summary in sorted(lookup.items()):
        baseline_key=(*key[:4],0,key[5])
        require(baseline_key in lookup,'missing paired zero-visitor destination')
        for other_key,base in sorted(lookup.items()):
            if other_key[:4]!=key[:4] or other_key[5]!=key[5] or other_key[4]>=key[4]:
                continue
            pairs.append(dict(cohort=list(key[:4]),destination=key[4],reference_destination=other_key[4],cost=key[5],
                              occupancy_difference=summary['occupancy']['proportion']-base['occupancy']['proportion'],
                              scope='same cohort, independent future streams; descriptive difference'))
    return dict(allocated=len(seen),cohorts=len(hashes),groups=summaries,paired_destinations=pairs,
                scope='conditional estimation; no pooling cohorts into independent repeats')
