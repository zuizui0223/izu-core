"""All-case bridge verification and prespecified replay before scientific summaries."""
import argparse,csv,json
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
import zipfile
import numpy as np
from threadpoolctl import threadpool_limits
from scripts.model3_island.design import canonical,digest
from scripts.model3_island.run import runtime_identity,founders_from_spec
from scripts.run_model3_ch2_bridge import sources
from scripts.model3_island_bridge_ops import prepare_arms
from scripts.model3_island.types import Config
from scripts.model3_island.density import make_grid,project_state
from scripts.model3_island.simulate import simulate
from scripts.model3_island.storage import verify_replay
from scripts.model3_island.audit import validate_arrays
from scripts.summarize_model3_ch2_bridge import effect_report,compare_effects,paired_mean,bounded_history_mean

VARIANTS=('', '_grid5','_grid11','_nested')
PAIRS=(('natural','near','far'),('richness_matched','matched_near','matched_far'),('visitor_pool','pool_near','pool_far'),('large_plants','large_near','large_far'))


@threadpool_limits.wrap(limits=1)
def audit_campaign(d,root,*,replay=True):
    root=Path(root);mh=digest(d)
    status=json.loads((root/'campaign_status.json').read_text())
    if not status.get('complete') or status['completed']!=d['cases'] or status['manifest_hash']!=mh:raise ValueError('campaign not completely terminal')
    if json.loads((root/'manifest.json').read_text())!=d or d['source_hashes']!=sources():raise ValueError('manifest/source mismatch')
    if json.loads((root/'runtime.json').read_text())!=runtime_identity():raise ValueError('replay runtime differs')
    attempts=json.loads(root.with_name(root.name+'.attempts.json').read_text())
    if attempts['manifest_hash']!=mh or not attempts['attempts'] or any(not a['closed'] for a in attempts['attempts']):raise ValueError('campaign attempt accounting incomplete')
    with zipfile.ZipFile(root/'sources.zip') as z:
        if set(z.namelist())!=set(d['source_hashes']):raise ValueError('source archive set mismatch')
        for name,h in d['source_hashes'].items():
            if sha256(z.read(name)).hexdigest()!=h:raise ValueError('source archive checksum mismatch')
    shape=(len(d['starts']),len(d['history_seeds']),len(d['demographic_seeds']))
    data={arm:{key:np.full(shape,np.nan) for key in ('individual','density','occupancy','density_occupancy','initial_investment','terminal_heterozygosity')} for arm in d['arms']}
    visits={arm:np.zeros((shape[1],d['years']),int) for arm in d['arms']}
    receipts=[];replayed=0;ids=set();grid=make_grid(d['grid_axes'])
    for hi,hs in enumerate(d['history_seeds']):
        arms=prepare_arms(Config.from_dict(d['base_config']),seed=hs,pool_size=d['pool_size'])
        for si,initial in enumerate(d['starts']):
            for arm in d['arms']:
                cfg,history=arms[arm];spec={'count':cfg.capacity,'draw_count':48,'means':[.5,initial,.5],'sd':.15,'birth_year':0}
                founders=founders_from_spec(spec,d['founder_seed'])
                if d.get('initial_projection_axes') is not None:founders,_=project_state(founders,make_grid(d['initial_projection_axes']))
                expected_visits=np.array([len(v.ids) for v in history.visitors])
                visits[arm][hi]=expected_visits
                for di,ds in enumerate(d['demographic_seeds']):
                    cid=f'{arm}-s{int(round(initial*10))}-h{hs}-d{ds}';ids.add(cid)
                    case={'id':cid,'config':asdict(cfg),'history_seed':hs,'demographic_seed':ds,'cell':{'kind':'trajectory','founders':spec},'manifest_hash':mh}
                    folder=root/cid;r=json.loads((folder/'receipt.json').read_text())
                    if r['status']!='complete' or r['manifest_hash']!=mh or r['case_hash']!=digest(case) or canonical(json.loads((folder/'input.json').read_text()))!=canonical(case):raise ValueError('case identity differs: '+cid)
                    path=folder/'arrays.npz'
                    if sha256(path.read_bytes()).hexdigest()!=r['arrays_sha256']:raise ValueError('array hash differs: '+cid)
                    with np.load(path,allow_pickle=False) as z:a={k:z[k] for k in z.files}
                    validate_arrays(a,case)
                    if not np.array_equal(a['visitor_count'],expected_visits):raise ValueError('visitor intervention differs: '+cid)
                    projected,_=project_state(founders,grid)
                    if not np.array_equal(a['initial_genotypes'],projected.alleles):raise ValueError('initial support differs: '+cid)
                    for mode,key,pop in (('individual','trait_mean','population'),('density','density_traits','density_mass')):
                        alive=bool(a[pop][-1]>0);start=a[key][0,1];end=a[key][-1,1]
                        data[arm][mode][si,hi,di]=float(end-start) if alive and np.isfinite([start,end]).all() else np.nan
                        data[arm]['occupancy' if mode=='individual' else 'density_occupancy'][si,hi,di]=float(alive)
                    data[arm]['initial_investment'][si,hi,di]=a['trait_mean'][0,1]
                    data[arm]['terminal_heterozygosity'][si,hi,di]=a['heterozygosity'][-1,1]
                    if replay and hi==di==0:
                        seed=int(np.random.SeedSequence([hs,ds]).generate_state(1)[0])
                        rr=simulate(cfg,history,founders,replicate=seed,grid=grid,projection_mode=d['projection_mode'])
                        verify_replay(a,rr,{'density_counts':'checkpoints_and_replay_digest','checkpoint_every':50});replayed+=1
                    receipts.append({'case_id':cid,'case_hash':r['case_hash'],'array_sha256':r['arrays_sha256'],'receipt_sha256':sha256((folder/'receipt.json').read_bytes()).hexdigest()})
    actual={p.parent.name for p in root.glob('*/receipt.json')}
    if ids!=actual or len(receipts)!=d['cases']:raise ValueError('unexpected/missing case receipts')
    if 'matched_near' in visits:
        n=np.minimum(visits['near'],visits['far'])
        if not np.array_equal(n,visits['matched_near']) or not np.array_equal(n,visits['matched_far']):raise ValueError('richness matching not exact')
    return data,visits,receipts,{'status':'passed','cases_checked':len(receipts),'replayed':replayed,'manifest_hash':mh,'attempt_elapsed_seconds':sum(a['elapsed_seconds'] for a in attempts['attempts']),'scope':'state/identity/count validation and first-history first-repeat per-arm/start exact replay; not ecological validation'}


def summarize_campaign(d,data,visits):
    pairs={};effects={}
    for label,near,far in PAIRS:
        pairs[label]={}
        for mode in ('individual','density'):
            pairs[label][mode]=effect_report(data[near][mode],data[far][mode]);effects[label,mode]=data[far][mode]-data[near][mode]
        pairs[label]['occupancy_effect']=bounded_history_mean(data[far]['occupancy']-data[near]['occupancy'],-1,1)
    interventions={label:{mode:compare_effects(effects['natural',mode],effects[label,mode]) for mode in ('individual','density')} for label in ('richness_matched','visitor_pool','large_plants')}
    return {'pairs':pairs,'interventions':interventions,
        'arms':{arm:{'occupancy':bounded_history_mean(v['occupancy'],0,1),'investment_change':paired_mean(v['individual']),'initial_investment':paired_mean(v['initial_investment']),'terminal_heterozygosity':paired_mean(v['terminal_heterozygosity']),
            'mean_visitors':float(visits[arm].mean()),'zero_visitor_year_fraction':float((visits[arm]==0).mean())} for arm,v in data.items()},
        'analysis_contract':d['analysis_contract'],'claim_boundaries':d['claim_exclusions']}


def _select_base(base,main_design,other_design):
    indices=[main_design['starts'].index(x) for x in other_design['starts']]
    histories=[main_design['history_seeds'].index(x) for x in other_design['history_seeds']]
    repeats=[main_design['demographic_seeds'].index(x) for x in other_design['demographic_seeds']]
    return base[np.ix_(indices,histories,repeats)]


def numerical_comparison(main_design,other_design,main_data,other_data):
    result={}
    tolerance=main_design['analysis_contract']['numerical_tolerances']['trait']
    for label,near,far in PAIRS:
        result[label]={}
        for mode in ('individual','density'):
            baseline=_select_base(main_data[far][mode]-main_data[near][mode],main_design,other_design)
            changed=other_data[far][mode]-other_data[near][mode]
            r=paired_mean(changed-baseline);ci=r['mean_ci']
            r['tolerance']=tolerance
            r['assessment']='not_evaluable' if ci is None else 'interval_within_tolerance' if ci[0]>=-tolerance and ci[1]<=tolerance else 'interval_outside_tolerance' if ci[0]>tolerance or ci[1]<-tolerance else 'unresolved_at_declared_precision'
            r['scope']='focal paired isolation-effect sensitivity to initial allele discretization; not a pure numerical solver error'
            result[label][mode]=r
    return result


def nested_consistency(main_design,nested_design,main_root,nested_root):
    coarse=make_grid(main_design['grid_axes']);fine=make_grid(nested_design['grid_axes'])
    lookup={tuple(x.ravel()):i for i,x in enumerate(fine.genotypes)}
    mapping=np.array([lookup[tuple(x.ravel())] for x in coarse.genotypes]);outside=np.ones(len(fine.genotypes),bool);outside[mapping]=False
    checked=0;max_trait=max_mass=max_frequency=max_outside=0.;individual_mismatches=[]
    for hs in nested_design['history_seeds']:
        for initial in nested_design['starts']:
            for arm in nested_design['arms']:
                for ds in nested_design['demographic_seeds']:
                    cid=f'{arm}-s{int(round(initial*10))}-h{hs}-d{ds}'
                    with np.load(Path(main_root)/cid/'arrays.npz',allow_pickle=False) as a,np.load(Path(nested_root)/cid/'arrays.npz',allow_pickle=False) as b:
                        for key in ('state_alleles','state_ids','population','initial_genotypes'):
                            if not np.array_equal(a[key],b[key]):individual_mismatches.append({'case':cid,'array':key})
                        if not np.array_equal(np.isnan(a['density_traits']),np.isnan(b['density_traits'])):raise ValueError('nested density trait support differs')
                        delta=np.abs(a['density_traits']-b['density_traits']);finite=delta[np.isfinite(delta)]
                        max_trait=max(max_trait,float(finite.max()) if finite.size else 0.)
                        max_mass=max(max_mass,float(np.max(abs(a['density_mass']-b['density_mass']))))
                        max_frequency=max(max_frequency,float(np.max(abs(a['final_density_counts']-b['final_density_counts'][mapping]))))
                        max_outside=max(max_outside,float(b['final_density_counts'][outside].sum()))
                        checked+=1
    return {'cases_checked':checked,'individual_mismatches':individual_mismatches,'max_density_trait_difference':max_trait,
        'max_density_mass_difference':max_mass,'max_density_final_count_difference':max_frequency,'max_added_node_mass':max_outside,
        'operator_consistency_at_1e_8':not individual_mismatches and max(max_trait,max_mass,max_frequency,max_outside)<=1e-8,
        'scope':'same fixed initial allele support, no mutation or immigration, actual 200-year histories; not continuous-founder convergence'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='data/results/model3_ch2_bridge_summary_20260927');args=parser.parse_args()
    configs={};roots={}
    # Preflight all four terminals before inspecting any new biological outcome.
    for variant in VARIANTS:
        name='model3_ch2_bridge'+variant+'_20260927';d=json.loads(Path('data/design',name+'.json').read_text());root=Path('data/results',name)
        status=json.loads((root/'campaign_status.json').read_text())
        if not status['complete'] or status['completed']!=d['cases'] or status['manifest_hash']!=digest(d):raise ValueError('all four campaigns must be complete')
        configs[variant]=d;roots[variant]=root
    output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
    if (output/'summary.json').exists():raise ValueError('preserve existing completed report; use a new output directory for a new report')
    all_data={};audits={};reports={};receipt_rows=[]
    with threadpool_limits(limits=1):
        for variant in VARIANTS:
            data,visits,receipts,audit=audit_campaign(configs[variant],roots[variant],replay=True)
            all_data[variant]=data;audits[variant or 'main']=audit
            reports[variant or 'main']=summarize_campaign(configs[variant],data,visits)
            for r in receipts:receipt_rows.append({'campaign':variant or 'main',**r})
            print(json.dumps({'stage':'campaign_audited','campaign':variant or 'main',**audit}),flush=True)
        nested=nested_consistency(configs[''],configs['_nested'],roots[''],roots['_nested'])
    numerical={v:numerical_comparison(configs[''],configs[v],all_data[''],all_data[v]) for v in ('_grid5','_grid11')}
    baseline=json.loads(Path('data/design/model3_island_frozen_baseline_hashes.json').read_text())
    if not all(sha256(Path(p).read_bytes()).hexdigest()==h for p,h in baseline.items()):raise ValueError('archived baseline changed')
    report_sources={p:sha256(Path(p).read_bytes()).hexdigest() for p in ('scripts/report_model3_ch2_bridge.py','scripts/summarize_model3_ch2_bridge.py','scripts/audit_model3_ch2_bridge.py')}
    complete={'status':'complete_audited_summary','audits':audits,'campaigns':reports,'numerical_sensitivity':numerical,'nested_consistency':nested,
        'report_source_hashes':report_sources,'old_baseline_unchanged':baseline,'uncertainty':'prespecified history bootstrap; occupancy Hoeffding; no multiplicity-adjusted equivalence or latent-sign claim',
        'claim_boundary':'restricted inherited-investment model; arbitrary continuously distributed alleles and field-calibrated island predictions not established'}
    with (output/'case_receipts.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(receipt_rows[0]));w.writeheader();w.writerows(receipt_rows)
    np.savez_compressed(output/'derived_tensors.npz',**{(variant or 'main')+'__'+arm+'__'+key:value for variant,data in all_data.items() for arm,v in data.items() for key,value in v.items()})
    (output/'summary.json').write_bytes(canonical(complete))
    (output/'provenance.json').write_bytes(canonical({'source_hashes':report_sources,'cases':len(receipt_rows),'artifacts':{p.name:sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file() and p.name!='provenance.json'},'raw_arrays_remotely_deposited':False}))
    print(json.dumps({'status':'complete_audited_summary','cases':len(receipt_rows),'replays':sum(r['replayed'] for r in audits.values())}),flush=True)

if __name__=='__main__':main()
