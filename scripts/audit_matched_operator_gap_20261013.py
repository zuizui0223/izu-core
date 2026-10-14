"""Same-state reproductive reduction and retrospective investment-gap accounting."""
import numpy as np
import argparse,hashlib,io,json,zipfile,importlib.util,sys,subprocess
from pathlib import Path


def density_return(alleles,visitors,config,census):
    a=np.asarray(alleles,float)
    if (a.ndim!=3 or a.shape[1:]!=(3,2) or not len(a) or not np.isfinite(a).all()
        or (a<0).any() or (a>1).any() or not np.isfinite(census) or not 0<census<=config.capacity):
        raise ValueError('Occupied finite empirical genotype state and valid census required')
    x=a.mean(2);counts=np.full(len(a),float(census)/len(a));assurance=x[:,2] if config.assurance_mode=='evolving' else np.full(len(a),config.fixed_assurance)
    ovules=config.ovule_budget*np.exp(-config.investment_cost*x[:,1]**2-config.assurance_cost*assurance**2)
    donors=np.zeros((len(a),0));recipients=np.zeros((len(a),0))
    if len(visitors.ids) and config.activity:
        affinity=(.1+x[:,1,None])*np.exp(-((x[:,0,None]-visitors.optima)/visitors.breadths)**2)
        channels=np.divide(affinity,affinity.sum(1,keepdims=True),out=np.zeros_like(affinity),where=affinity.sum(1,keepdims=True)>0)
        activity=config.activity*(len(visitors.ids)/config.reference_visitor_count if config.activity_mode=='count_scaled' else 1)
        removed=config.pollen_budget*np.exp(-config.pollen_discount*assurance)*(-np.expm1(-activity*affinity.mean(1)))
        recipients=affinity/((counts[:,None]*affinity).sum(0)+config.capacity*config.background_ratio)
        donors=counts[:,None]*removed[:,None]*channels*visitors.effectiveness
    receipt=recipients@donors.sum(0)
    available=ovules*(1-assurance) if config.assurance_timing=='prior' else ovules
    female=counts*available*(-np.expm1(-receipt/(2*config.pollen_scale)))
    conversion=np.divide(female,receipt,out=np.zeros_like(female),where=receipt>0)
    paternal=donors@(recipients*conversion[:,None]).sum(0)
    self_raw=counts*ovules*assurance if config.assurance_timing=='prior' else assurance*(counts*ovules-female)
    self_viable=self_raw*(1-config.depression)
    rate=float((female+self_viable).sum())
    if rate<=0 or not np.isfinite(rate):raise ValueError('Undefined offspring mean at zero/invalid reproductive rate')
    if abs(float(female.sum()-paternal.sum()))>1e-10:raise ValueError('Density female/paternal conservation')
    weights=(female+paternal)/2+self_viable
    mean=weights@x/rate
    if not np.isfinite(mean).all() or (mean<0).any() or (mean>1).any():raise ValueError('Invalid density reproductive mean')
    return dict(mean=mean,rate=rate,maternal_outcross=female,paternal_outcross=paternal,self_viable=self_viable)


def partition_step(actual,next_actual,density,next_density,finite_mean,no_exclusion_mean,reference_mean):
    values=np.asarray([actual,next_actual,density,next_density,finite_mean,no_exclusion_mean,reference_mean],float)
    if not np.isfinite(values).all():raise ValueError('Undefined investment means')
    p=dict(realized_sampling_transmission=next_actual-finite_mean,
           finite_parent_operator=finite_mean-no_exclusion_mean,
           current_census_intervention=no_exclusion_mean-reference_mean,
           remaining_path_feedback=reference_mean-actual-(next_density-density))
    if abs(sum(p.values())-((next_actual-next_density)-(actual-density)))>1e-10:
        raise ValueError('Annual gap partition does not close')
    return p


ACCOUNT_SHA='115636a338c847fdf1f80ae9e39cdfc622fcf38c7f70575e37d245bf7c41b098'


def context(task):
    return (task['block'],task['supply'],task['composition'])


def audit(cohort_path,input_path,account_path,out):
    spec=importlib.util.spec_from_file_location('source_account_admission',Path(__file__).with_name('audit_genome_response_accounting_20261013.py'))
    original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
    raw=Path(cohort_path).read_bytes();account_raw=Path(account_path).read_bytes()
    if original.digest(raw)!=original.COHORT_SHA or original.digest(account_raw)!=ACCOUNT_SHA:
        raise ValueError('Original cohort/accounting provider archive differs')
    out=Path(out)
    if out.exists():raise ValueError('Refuse audit overwrite')
    source=original.prepare_source(input_path,out.with_name(out.name+'_source'))
    density_source=(Path(source['root'])/'scripts/model3_island/density.py').read_bytes()
    density_normalized_sha=original.digest(density_source.replace(b'\r\n',b'\n'))
    types,_,reproduction,_=original.load_native(source)
    root=Path(__file__).resolve().parents[1]
    comparison=json.loads((root/'data/results/atom_cell_completed_20261011/matched_comparison.json').read_bytes())
    admitted_density=json.loads((root/'data/results/atom_cell_completed_20261011/independent_verification.json').read_bytes())['archive_sha256']
    expected=comparison['abm_archive_sha256'];densities={};density_records=[]
    with zipfile.ZipFile(io.BytesIO(account_raw)) as az:
        accounts={Path(n).stem:json.loads(az.read(n)) for n in az.namelist() if n.startswith('causal_') and n.endswith('.json')}
    if {key+'.npz' for key in accounts}!=set(expected) or len(accounts)!=320:
        raise ValueError('Original full-genome account inventory differs')
    out.mkdir();results=[]
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        numerical=[n for n in z.namelist() if '/atom_cell_numerical/archives/' in n and n.endswith('.npz')]
        if len(numerical)!=30:raise ValueError('All30 density archive inventory differs')
        for n in numerical:
            b=z.read(n);receipt=json.loads(z.read(n[:-4]+'.json'))
            if original.digest(b)!=receipt['sha256'] or receipt['sha256']!=admitted_density[Path(n).name]:
                raise ValueError('Original admitted density bytes differ')
            with np.load(io.BytesIO(b),allow_pickle=False) as a:
                meta=json.loads(str(a['metadata'].item()));job=meta['job']
                if meta!=receipt['metadata'] or meta['technical']:raise ValueError('Numerical metadata differs')
                recorded=[h for p,h in meta['identity']['files'].items() if p.replace('\\','/').endswith('/scripts/model3_island/density.py')]
                if recorded!=[density_normalized_sha]:raise ValueError('Density reproductive source differs beyond explicit source newline normalization')
                if job['nodes']!=257:continue
                if job['task']['replicate']!=0:raise ValueError('Density template identity differs')
                key=context(job['task']);trace=a['trace'].copy()
                if key in densities or trace.shape!=(201,13) or not np.isfinite(trace).all():
                    raise ValueError('Incomplete/duplicate density reference')
                densities[key]=trace
                density_records.append(dict(context=list(key),archive=Path(n).name,sha256=receipt['sha256']))
        if len(densities)!=10:raise ValueError('Ten density references required')
        cases=[n for n in z.namelist() if '/assurance_causal_campaign_20261008/archives/' in n and n.endswith('.npz')]
        if {Path(n).name for n in cases}!=set(expected):raise ValueError('All320 source cases required')
        for ix,n in enumerate(sorted(cases)):
            b=z.read(n);sha=original.digest(b);receipt=json.loads(z.read(n[:-4]+'.json'));account=accounts[Path(n).stem]
            if sha!=expected[Path(n).name] or sha!=receipt['sha256'] or sha!=account['case_sha256']:
                raise ValueError('Original ABM/genome-account byte identity differs')
            with np.load(io.BytesIO(b),allow_pickle=False) as a:
                meta=json.loads(str(a['metadata'].item()));task=meta['task'];alleles=a['alleles'];offsets=a['offsets'];population=a['population'];means=a['means']
                state_arrays={f:a[f].copy() for f in original.FIELDS}
                if task!=account['task'] or task!=receipt['task'] or len(account['rows'])!=200:
                    raise ValueError('Full genetic account/task differs')
                d=densities[context(task)];cfg=meta['config'].copy()
                cfg['visitor_arrival']=types.ArrivalConfig(**cfg['visitor_arrival']);cfg['seed_arrival']=types.ArrivalConfig(**cfg['seed_arrival']);c=types.Config(**cfg)
                if c.capacity!=48 or c.years!=200 or c.survival!=0 or c.seed_arrival.supply!=0 or tuple(meta['mutation_mask'])!=(False,False,True):
                    raise ValueError('No-investment-mutation/all-birth scope differs')
                optima=[] if task['supply']==0 else source['campaign_design']['compositions'][task['composition']]
                v=types.VisitorState(np.arange(len(optima),dtype=np.int64),np.array(optima,float),np.full(len(optima),.2),np.ones(len(optima)))
                if means.shape!=(201,3) or population.shape!=(201,) or offsets.shape!=(202,) or (population<=0).any():
                    raise ValueError('Unavailable annual state means')
                rows=[];maximum=0.
                for t in range(200):
                    lo,hi=offsets[t:t+2];aa=alleles[lo:hi];x=aa.mean(2)
                    if len(x)!=population[t] or not np.allclose(x.mean(0),means[t],atol=1e-12,rtol=0):raise ValueError('Original annual genomes/means differ')
                    state=types.PlantState(**{f:state_arrays[f][lo:hi] for f in original.FIELDS})
                    ledger=reproduction.reproduce(state,v,c);w=(ledger.outcross.sum(0)+ledger.outcross.sum(1))/2+ledger.self_viable
                    finite=float(w@x[:,1]/w.sum());old=account['rows'][t]
                    if (not old['eligible'] or old['year']!=t or old['birth_mutation'][1]!=0
                        or abs((finite-means[t,1])-old['selection'][1])>1e-10):raise ValueError('Expected native genetic response differs')
                    f=density_return(aa,v,c,len(aa));ref=density_return(aa,v,c,48.)
                    p=partition_step(float(means[t,1]),float(means[t+1,1]),float(d[t,2]),float(d[t+1,2]),finite,float(f['mean'][1]),float(ref['mean'][1]))
                    err=abs(p['realized_sampling_transmission']-old['parent_sampling'][1]-old['transmission'][1]);maximum=max(maximum,err)
                    if err>1e-10:raise ValueError('Original realized sampling/transmission differs')
                    rows.append(dict(year=t,census=int(population[t]),actual=float(means[t,1]),next_actual=float(means[t+1,1]),density=float(d[t,2]),next_density=float(d[t+1,2]),finite_mean=finite,no_exclusion_mean=float(f['mean'][1]),reference_mean=float(ref['mean'][1]),components=p))
                sums={k:float(sum(r['components'][k] for r in rows)) for k in rows[0]['components']}
                initial=float(means[0,1]-d[0,2]);endpoint=float(means[-1,1]-d[-1,2]);err=abs(initial+sum(sums.values())-endpoint)
                if err>1e-10:raise ValueError('Full endpoint accounting differs')
                result=dict(task=task,case_sha256=sha,initial_gap=initial,endpoint_gap=endpoint,components=sums,max_source_account_error=maximum,closure_error=err,rows=rows)
                target=out/(Path(n).stem+'.json');target.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
                results.append({k:result[k] for k in result if k!='rows'})
            if (ix+1)%64==0:print(f'ACCOUNTED {ix+1}/320',flush=True)
    groups=[]
    for key in sorted(densities):
        group=[r for r in results if context(r['task'])==key]
        if len(group)!=32 or {r['task']['replicate'] for r in group}!=set(range(32)):raise ValueError('Complete context seeds required')
        groups.append(dict(context=list(key),cases=32,endpoint_gap=float(np.mean([r['endpoint_gap'] for r in group])),initial_gap=float(np.mean([r['initial_gap'] for r in group])),components={k:float(np.mean([r['components'][k] for r in group])) for k in group[0]['components']}))
    readout=dict(status='COMPLETE_MATCHED_OPERATOR_INVESTMENT_ACCOUNTING_NOT_UNIQUE_CAUSAL_ALLOCATION',cases=320,updates=64000,density_references=density_records,cohort_sha256=original.COHORT_SHA,input_sha256=original.INPUT_SHA,accounting_zip_sha256=ACCOUNT_SHA,source_manifest=source['manifest_sha256'],density_source_raw_sha256=original.digest(density_source),density_source_normalized_sha256=density_normalized_sha,contexts=groups,max_closure_error=max(r['closure_error'] for r in results),max_source_account_error=max(r['max_source_account_error'] for r in results),scope='Post-outcome signed accounting; census/parent terms conditional on actual genotypes. Remaining path feedback includes genetic feedback and admitted numerical representation error; not pure drift, autonomous intervention or natural-order benefit.')
    (out/'READOUT.json').write_text(json.dumps(readout,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    (out/'_COMPLETION.json').write_text(json.dumps(dict(status=readout['status'],files={p.name:original.digest(p.read_bytes()) for p in out.glob('*.json')}),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(readout,indent=2))


if __name__=='__main__':
    # Import archived scripts in a clean process, before a current scripts package.
    if __package__:
        raise SystemExit(subprocess.run([sys.executable,str(Path(__file__).resolve()),*sys.argv[1:]]).returncode)
    p=argparse.ArgumentParser();p.add_argument('--cohort',required=True);p.add_argument('--input',required=True);p.add_argument('--account',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();audit(a.cohort,a.input,a.account,a.out)
