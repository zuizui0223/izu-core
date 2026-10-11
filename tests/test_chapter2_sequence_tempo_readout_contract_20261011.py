"""Pre-outcome readout regressions; long traces below are synthetic, never ABM runs."""
import copy
import json
from hashlib import sha256

import numpy as np
import pytest

from scripts import run_chapter2_sequence_abrupt_gradual_functional_loss_20261011 as runner
from scripts import run_chapter2_sequence_abrupt_gradual_batch_20261011 as batch
from scripts import summarize_chapter2_sequence_abrupt_gradual_functional_loss_20261011 as summary


def synthetic_record(schedule, *, late=False, missing=False):
    # Explicit artificial means, not realized original-Model3 evolutionary results.
    trace=np.zeros((401,10),dtype=float)
    trace[:,0]=48
    trace[:,1:4]=.5
    trace[:,4:7]=.02
    trace[:,7:]=2
    if schedule=='abrupt':
        trace[81:,3]=.6
        trace[120 if late else 82:,2]=.4
    else:
        trace[82:,3]=.6
        trace[120 if late else 92:,2]=.4
    if missing:
        trace[90:,0]=0
        trace[90:,1:]=np.nan
    d,_=runner.contract()
    metric={'delivered':2. if schedule=='abrupt' else 1.,
            'functional_overlap':.4 if schedule=='abrupt' else .2,
            'expected_I_change_pre_mutation':-.01,
            'expected_A_change_pre_mutation':.02,
            'resident_selfed_recruits':3,'resident_outcross_recruits':5,
            'parentage':[[48,0,0],[49,0,1]]}
    gradients=[{'t':t,'investment':{'median':-.2,'n_evaluated':8,
        'n_boundary':1,'n_positive':0,'n_negative':7,'n_near_zero':0},
        'assurance':{'median':.3,'n_evaluated':8,'n_boundary':0,
        'n_positive':8,'n_negative':0,'n_near_zero':0}}
        for t in runner.SAMPLE_TIMES]
    rows=[dict(metric,t=t) for t in range(400)]
    if missing:
        for row in rows[90:]:
            row.update(delivered=0.,functional_overlap=None,expected_I_change_pre_mutation=None,
                       expected_A_change_pre_mutation=None,resident_selfed_recruits=0,
                       resident_outcross_recruits=0,parentage=[])
        for row in gradients:
            if row['t']>=90:
                for trait in ('investment','assurance'):
                    row[trait]={key:None if key=='median' else 0 for key in row[trait]}
    return {'trace':runner.json_safe_trait_trace(trace),
            'order':runner.order_from_trace(trace,400,d),
            'pollen_and_price_series':rows,
            'focal_gradient_samples':gradients}


def test_passive_native_parentage_genotypes_overlap_and_founder_hashes(monkeypatch):
    native=runner.advance
    observed=[]
    def capture(*args,**kwargs):
        result,info=native(*args,**kwargs)
        observed.append((args[0],result,info))
        return result,info
    monkeypatch.setattr(runner,'advance',capture)
    result=runner.simulate(48271001,49271001,'abrupt','delayed',.5,.01,years=3)
    assert result['runtime_identity']['numpy_version']==np.__version__
    assert len(result['founder_identity']['digest'])==64
    assert set(result['founder_identity']['array_sha256'])=={'alleles','allele_origin','mutation_flags','ids','birth_years'}
    assert len(result['genetic_state_series'])==4
    start,end=runner.visitor_profile(48271001,runner.contract()[0])
    for t,(before,after,info) in enumerate(observed):
        row=result['pollen_and_price_series'][t]
        assert row['parentage']==info['parentage'].tolist()
        assert row['resident_selfed_recruits']==info['resident_selfed_recruits']
        assert row['resident_outcross_recruits']==info['resident_outcross_recruits']
        assert result['genetic_state_series'][t]['adult_ids']==before.ids.tolist()
        assert result['genetic_state_series'][t]['diploid_alleles']==before.alleles.tolist()
        visitors=runner.functional_visitors(start,end,row['lambda'])
        expected=np.exp(-((before.alleles.mean(axis=2)[:,0,None]-visitors.optima)/visitors.breadths)**2).mean()
        assert row['functional_overlap']==pytest.approx(expected)
    assert result['genetic_state_series'][-1]['diploid_alleles']==observed[-1][1].alleles.tolist()


def test_empty_gradients_and_overlap_remain_missing():
    d,_=runner.contract()
    empty=runner.empty_source_seeds(0)
    grad=runner.sample_gradients(empty,runner.functional_visitors(*runner.visitor_profile(48271001,d),1),runner.original_model_config('delayed',.5,0,d))
    assert grad['investment']['n_near_zero']==0
    assert grad['assurance']['median'] is None


def test_source_pins_all_native_modules_and_event_classifier():
    files=batch.source_identity()['files']
    assert 'scripts/model3_temporal_order.py' in files
    assert {str(p.relative_to(runner.ROOT)) for p in (runner.ROOT/'scripts/model3_island').glob('*.py')}<=files.keys()


def test_primary_by100_category_does_not_use_full400_order():
    record=synthetic_record('abrupt',late=True)
    o=record['order']
    assert o['A_confirmation_update']==100
    assert o['I_confirmation_update']==139
    assert o['order']=='assurance_first'
    assert o['order_by100']=='assurance_only'
    metrics=summary.metrics_for_record(record)
    assert metrics['A_first']==1
    assert metrics['A_only_by100']==1
    assert metrics['A_first_by100']==0
    # Independently recalculate even if a derived field was edited and rehashed.
    altered=copy.deepcopy(record)
    altered['order']['A_crossed_by100']=False
    with pytest.raises(ValueError,match='derived'):
        summary.metrics_for_record(altered)


def test_all_secondary_endpoints_and_paired_eligible_profile_support():
    records={case:synthetic_record(case[-1],missing=(case[0]==48271001 and case[-1]=='gradual')) for case in batch.tasks()}
    out=summary.clustered_summary(records)
    block=out['results'][0]
    assert block['outcomes']['A_first']['horizon_updates']==400
    assert block['outcomes']['A_only_by100']['horizon_updates']==100
    secondary=block['secondary_endpoints']
    assert secondary['pollen_delivery_mean']['abrupt_minus_gradual']==pytest.approx(1+.775/16)
    assert secondary['functional_overlap_mean']['abrupt_minus_gradual']==pytest.approx(.2)
    lag=secondary['A_minus_I_crossing_lag_by400']
    assert lag['abrupt_minus_gradual']==9
    assert lag['eligible_paired_profiles']==15
    assert lag['eligible_paired_trajectories']==60
    assert lag['eligible_gradual_trajectories']==60
    assert len(lag['profile_support'])==16
    assert lag['profile_support'][0]['paired_repeats']==0
    assert secondary['X_mean_at100']['eligible_paired_profiles']==15
    assert secondary['X_variance_at400']['mean_abrupt']==pytest.approx(.02)
    assert secondary['gradient_investment_median_at100']['eligible_paired_profiles']==15
    assert secondary['I_mean_at10']['eligible_paired_profiles']==16
    assert secondary['A_mean_at400']['eligible_paired_profiles']==15
    for t in runner.SAMPLE_TIMES:
        for trait in ('investment','assurance'):
            assert f'gradient_{trait}_median_at{t}' in secondary
            assert f'gradient_{trait}_n_near_zero_at{t}' in secondary
    for name in ('pollen_delivery_min','pollen_delivery_max','functional_overlap_min',
                 'functional_overlap_max','expected_I_change_pre_mutation_mean',
                 'expected_A_change_pre_mutation_mean','resident_selfed_recruits_total',
                 'resident_outcross_recruits_total','parentage_updates_available'):
        assert name in secondary
    json.dumps(out,allow_nan=False)


def test_resume_rejects_rehashed_runtime_founder_and_horizon_changes(tmp_path):
    case=batch.tasks()[0]
    stem=batch.run_one(tmp_path,case,smoke_years=2)
    path=tmp_path/(stem+'.json');receipt=tmp_path/(stem+'.receipt.json')
    original=path.read_text();original_rec=receipt.read_text()
    for field,value in [('years',3),('runtime_identity',{'numpy_version':'changed'}),('founder_identity',{'digest':'changed'})]:
        data=json.loads(original);data[field]=value
        path.write_text(json.dumps(data))
        rec=json.loads(original_rec);rec['sha256']=sha256(path.read_bytes()).hexdigest()
        receipt.write_text(json.dumps(rec))
        with pytest.raises(ValueError,match='provenance|horizon|founder|runtime'):
            batch.run_one(tmp_path,case,smoke_years=2)
    path.write_text(original);receipt.write_text(original_rec)
    with pytest.raises(ValueError,match='horizon|provenance'):
        batch.run_one(tmp_path,case,smoke_years=3)


def write_synthetic_complete_cohort(folder):
    """Full factorial provenance fixture, built without a biological full run."""
    base=runner.simulate(48271001,49271001,'abrupt','delayed',.5,.01,years=1)
    base['runtime_identity']['numpy_version']='uniform-remote-runtime-fixture'
    d,digest=runner.contract();source=batch.source_identity()
    first=np.asarray(base['trace'][0])
    trace=np.full((401,10),np.nan);trace[:,0]=0;trace[0]=first
    empty_grad={trait:{'n_evaluated':0,'n_boundary':0,'n_positive':0,
                'n_negative':0,'n_near_zero':0,'median':None}
                for trait in ('investment','assurance')}
    for case in batch.tasks():
        p,r,timing,cost,mu,schedule=case
        x=copy.deepcopy(base)
        x.update(case_key=batch.key(case),full_declared_case=True,years=400,
            history_profile_seed=p,nested_demography_seed=r,mating_timing=timing,
            direct_assurance_cost=cost,mutation_rate=mu,schedule=schedule,
            trace=runner.json_safe_trait_trace(trace),end_persistence=False,
            order=runner.order_from_trace(trace,400,d))
        plan=runner.profile_plan(p)
        lambdas=plan['abrupt_lambdas'] if schedule=='abrupt' else plan['ramp_lambdas']
        visitors=runner.functional_visitors(*runner.visitor_profile(p,d),lambdas[0])
        alleles=np.asarray(x['genetic_state_series'][0]['diploid_alleles'])
        overlap=float(np.exp(-((alleles.mean(axis=2)[:,0,None]-visitors.optima)/visitors.breadths)**2).mean())
        x['genetic_state_series']=x['genetic_state_series'][:1]+[
            {'t':t,'adult_ids':[],'diploid_alleles':[]} for t in range(1,401)]
        x['pollen_and_price_series']=[{'t':t,'N':48 if t==0 else 0,
            'lambda':float(lambdas[t]) if t<100 else 1.,'delivered':0.,
            'outcross':0.,'viable_self':0.,'functional_overlap':overlap if t==0 else None,
            'expected_I_change_pre_mutation':None,'expected_A_change_pre_mutation':None,
            'resident_selfed_recruits':0,'resident_outcross_recruits':0,'parentage':[]}
            for t in range(400)]
        x['focal_gradient_samples']=[{'t':t,**copy.deepcopy(empty_grad)} for t in runner.SAMPLE_TIMES]
        x['focal_gradient_samples'][0]=base['focal_gradient_samples'][0]
        data=json.dumps(x,separators=(',',':')).encode()
        (folder/(batch.key(case)+'.json')).write_bytes(data)
        receipt={'case':list(case),'sha256':sha256(data).hexdigest(),
            'design_sha256':digest,'source_identity_sha256':source['digest'],
            'source_file_sha256':source['files'],'years':400,'full_declared_case':True,
            'runtime_identity':x['runtime_identity'],
            'founder_identity_sha256':x['founder_identity']['digest']}
        (folder/(batch.key(case)+'.receipt.json')).write_text(json.dumps(receipt))
    for index in range(16):
        (folder/f'shard_{index:02d}_complete.json').write_text(json.dumps({
            'status':'COMPLETE_FROZEN_SHARD','shard_index':index,'shard_count':16,
            'case_count':64,'design_sha256':digest,'source_identity_sha256':source['digest'],
            'case_keys':[batch.key(c) for j,c in enumerate(batch.tasks()) if j%16==index],
            'runtime_identity':base['runtime_identity'],
            'founder_identity_sha256':base['founder_identity']['digest']}))


def rehash_case(folder,case,change):
    path=folder/(batch.key(case)+'.json')
    x=json.loads(path.read_text());change(x);path.write_text(json.dumps(x))
    receipt=folder/(batch.key(case)+'.receipt.json')
    r=json.loads(receipt.read_text());r['sha256']=sha256(path.read_bytes()).hexdigest()
    receipt.write_text(json.dumps(r))


def test_complete_reader_checks_raw_endpoints_and_prunes_only_heavy_payload(tmp_path):
    write_synthetic_complete_cohort(tmp_path)
    records=summary.read_all(tmp_path)
    assert len(records)==1024
    assert 'genetic_state_series' not in next(iter(records.values()))
    assert 'parentage' not in next(iter(records.values()))['pollen_and_price_series'][0]
    assert next(iter(records.values()))['pollen_and_price_series'][0]['parentage_available'] is True
    case=batch.tasks()[0]
    rehash_case(tmp_path,case,lambda x:x['order'].update(A_crossed_by100=True))
    with pytest.raises(ValueError,match='derived'):
        summary.read_all(tmp_path)


def test_complete_reader_rejects_mixed_runtime_even_when_receipt_matches(tmp_path):
    write_synthetic_complete_cohort(tmp_path)
    case=batch.tasks()[0]
    rehash_case(tmp_path,case,lambda x:x['runtime_identity'].update(numpy_version='different'))
    receipt=tmp_path/(batch.key(case)+'.receipt.json')
    r=json.loads(receipt.read_text());r['runtime_identity']['numpy_version']='different'
    receipt.write_text(json.dumps(r))
    with pytest.raises(ValueError,match='runtime|provenance'):
        summary.read_all(tmp_path)


def test_missing_native_parentage_is_not_claimed_available_for_empty_recruitment():
    x=runner.simulate(48271001,49271001,'abrupt','delayed',.5,.01,years=1)
    x['pollen_and_price_series'][0].pop('parentage')
    x['genetic_state_series'][1]={'t':1,'adult_ids':[],'diploid_alleles':[]}
    x['trace'][1]=[0]+[None]*9
    x['pollen_and_price_series'][0].update(resident_selfed_recruits=0,resident_outcross_recruits=0)
    x['end_persistence']=False
    x['order']=runner.order_from_trace(np.asarray(x['trace'],dtype=float),1,runner.contract()[0])
    with pytest.raises(ValueError,match='missing.*passive|parentage'):
        summary.validate_passive_history(x)


def test_raw_validation_rejects_rehashed_overlap_genotype_and_parentage_changes():
    original=runner.simulate(48271001,49271001,'gradual','prior',.5,.01,years=3)
    summary.validate_passive_history(copy.deepcopy(original))
    for change in (
        lambda x:x['trace'][1].__setitem__(2,.123),
        lambda x:x['pollen_and_price_series'][0].__setitem__('functional_overlap',.123),
        lambda x:x['pollen_and_price_series'][0]['parentage'][0].__setitem__(1,999999),
        lambda x:x['focal_gradient_samples'].clear(),
    ):
        altered=copy.deepcopy(original);change(altered)
        with pytest.raises(ValueError):
            summary.validate_passive_history(altered)


def test_recording_matches_a_short_uninstrumented_native_trajectory():
    from scripts.model3_island.randomness import stream,STREAM_IDS
    d,_=runner.contract()
    cfg=runner.original_model_config('prior',.5,.01,d)
    profile,rep=48271001,49271001
    result=runner.simulate(profile,rep,'gradual','prior',.5,.01,years=12)
    native_state=runner.founders(d)
    master=int(np.random.SeedSequence([profile,rep]).generate_state(1)[0])
    streams={name:stream(master,name,0) for name in STREAM_IDS}
    start,end=runner.visitor_profile(profile,d)
    for t in range(13):
        recorded=result['genetic_state_series'][t]
        assert recorded['adult_ids']==native_state.ids.tolist()
        np.testing.assert_array_equal(recorded['diploid_alleles'],native_state.alleles)
        if t<12:
            visitor=runner.functional_visitors(start,end,(t+.5)/100)
            ledger=runner.reproduce(native_state,visitor,cfg)
            native_state,info=runner.advance(native_state,ledger,runner.empty_source_seeds(t+1),cfg,streams,year=t)
            assert result['pollen_and_price_series'][t]['parentage']==info['parentage'].tolist()


def test_conditional_contrasts_use_common_repeats_and_equal_profile_weights():
    pairs=[]
    for profile in range(16):
        repeats=[]
        for rep in range(4):
            # First profile has a single common repeat, but still one profile's weight.
            value=100. if profile==0 else 0.
            repeats.append(({'value':value},{'value':0. if profile or rep==0 else None}))
        pairs.append(repeats)
    draw=np.random.default_rng(48272026).integers(0,16,size=(9999,16))
    out=summary.secondary_summary(pairs,list(range(16)),draw)['value']
    assert out['abrupt_minus_gradual']==6.25
    assert out['eligible_paired_trajectories']==61
    assert out['eligible_paired_profiles']==16
    absent=summary.secondary_summary([[({'lag':None},{'lag':None})]*4]*16,list(range(16)),draw)['lag']
    assert absent['abrupt_minus_gradual'] is None
    assert absent['descriptive_history_profile_bootstrap95'] is None
    assert absent['bootstrap_nonempty_resamples']==0
