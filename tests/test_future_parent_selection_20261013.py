import numpy as np
import pytest
from scripts import future_parent_selection_20261013 as assay


def test_uniform_parent_weights_preserve_total_and_self_outcross_classes():
    o=np.array([[0.,1.,2.],[3.,0.,1.],[2.,1.,0.]])
    s=np.array([1.,2.,3.])
    p=assay.equal_parent_weights(o,s)
    np.testing.assert_allclose(p.sum(),o.sum()+s.sum(),atol=1e-12)
    np.testing.assert_allclose(np.trace(p),s.sum(),atol=1e-12)
    np.testing.assert_allclose(p.sum()-np.trace(p),o.sum(),atol=1e-12)
    np.testing.assert_allclose(p.sum(0)+p.sum(1),np.full(3,2*p.sum()/3),atol=1e-12)


def test_equal_parent_expected_all_locus_response_zero():
    o=np.array([[0.,2.,0.],[0.,0.,1.],[3.,0.,0.]])
    s=np.array([0.,2.,1.]);p=assay.equal_parent_weights(o,s)
    genes=np.array([[.1,.2,.9],[.3,.8,.2],[.9,.1,.7]])
    contribution=(p.sum(0)+p.sum(1))/(2*p.sum())
    np.testing.assert_allclose(contribution@genes,genes.mean(0),atol=1e-12)


def test_empty_singleton_and_zero_return_are_preserved():
    assert assay.equal_parent_weights(np.empty((0,0)),np.empty(0)).shape==(0,0)
    np.testing.assert_array_equal(assay.equal_parent_weights(np.zeros((1,1)),np.array([3.])),[[3.]])
    np.testing.assert_array_equal(assay.equal_parent_weights(np.zeros((2,2)),np.zeros(2)),np.zeros((2,2)))


@pytest.mark.parametrize('o,s',[(np.ones((1,1)),np.ones(1)),(np.zeros((2,3)),np.ones(2)),(np.zeros((2,2)),np.array([-1.,2.])),(np.array([[0.,float('nan')],[0.,0.]]),np.zeros(2))])
def test_invalid_reproductive_inputs_fail_closed(o,s):
    with pytest.raises(ValueError):assay.equal_parent_weights(o,s)


def test_sampling_adapter_preserves_native_biological_record():
    from types import SimpleNamespace
    n=SimpleNamespace(outcross=np.array([[0.,2.],[1.,0.]]),self_viable=np.array([1.,3.]),ovules=np.array([5.,8.]))
    before=n.outcross.copy();p=assay.sampling_ledger(n)
    np.testing.assert_array_equal(n.outcross,before)
    np.testing.assert_array_equal(p.ovules,n.ovules)
    assert p.outcross.sum()==n.outcross.sum()
    assert p.self_viable.sum()==n.self_viable.sum()


def test_all4096_tasks_and_four_contrasts_are_fixed_and_all_start():
    tasks=assay.tasks()
    assert len(tasks)==4096 and len({tuple(sorted(t.items())) for t in tasks})==4096
    assert all(t['policy']==assay.POLICY for t in tasks)
    x=np.zeros((2,512,2,3,2),dtype=np.int8)
    x[:,:,:,0,0]=1
    r=assay.analyze(x,bootstrap_count=9)
    assert len(r['primary'])==4
    assert [a['estimate'] for a in r['primary']]==[1.,0.,1.,0.]
    with pytest.raises(ValueError):assay.analyze(x[:,:511],bootstrap_count=9)
    bad=x.astype(float);bad[0,0,0,0,0]=float('nan')
    with pytest.raises(ValueError):assay.analyze(bad,bootstrap_count=9)


def test_reference_admission_rejects_unpinned_prior_before_extraction(tmp_path):
    from scripts import admit_parent_selection_references_20261013 as admission
    bad=tmp_path/'wrong.zip';bad.write_bytes(b'not original prior')
    with pytest.raises(ValueError,match='prior original byte identity'):
        admission.admit(bad,tmp_path/'missing-input.zip',tmp_path/'out')
    assert not (tmp_path/'out').exists()


def test_reference_assembly_selects_mean_equal_native_not_original_native():
    old=np.zeros((2,512,2,3,2),dtype=np.int8)
    old[:,:,:,0,:]=1
    old[:,:,:,1,0]=1
    uniform=np.zeros((2,512,2,2),dtype=np.int8)
    x=assay.assemble_outcomes(old,uniform)
    np.testing.assert_array_equal(x[:,:,:,0,:],old[:,:,:,1,:])
    np.testing.assert_array_equal(x[:,:,:,1,:],uniform)
    np.testing.assert_array_equal(x[:,:,:,2,:],old[:,:,:,2,:])
    assert not np.array_equal(x[:,:,:,0,:],old[:,:,:,0,:])
    with pytest.raises(ValueError):assay.assemble_outcomes(old[:,:511],uniform)


def test_native_trajectory_identity_full_states_and_seeded_adapter_replay():
    from dataclasses import replace
    from scripts.run_model3_assurance_intervention import founders,config
    from scripts.run_model3_persistent_isolation import exposure
    from scripts import run_future_parent_selection_20261013 as runner
    from scripts import persistence_expression_mechanism_20261012 as old
    state=founders();cfg=replace(config('assurance_cost',.01,'evolving'),years=4,survival=0.)
    visitors=exposure(76001,'near').visitors[0]
    trace=runner.trajectory(state,visitors,cfg,17,'native',horizon=4)
    reference=old.trajectory(state,visitors,cfg,17,'native',horizon=4)
    for f in old.FIELDS+('population','offsets','means','diagnostics','parentage'):
        np.testing.assert_array_equal(trace[f],reference[f])
    runner.verify(trace,state,visitors,cfg,17,'native')
    neutral=runner.trajectory(state,visitors,cfg,17,assay.POLICY,horizon=4)
    runner.verify(neutral,state,visitors,cfg,17,assay.POLICY)
    bad={k:v.copy() for k,v in neutral.items()};bad['mutation_flags'][0,0,0]=~bad['mutation_flags'][0,0,0]
    with pytest.raises(AssertionError):runner.verify(bad,state,visitors,cfg,17,assay.POLICY)
    bad={k:v.copy() for k,v in neutral.items()};bad['sampling_weights'][0]+=1
    with pytest.raises(AssertionError):runner.verify(bad,state,visitors,cfg,17,assay.POLICY)


def test_technical_gate_rejects_duplicate_record_domain(tmp_path):
    import json
    from scripts import run_future_parent_selection_20261013 as runner
    from scripts import persistence_expression_mechanism_20261012 as old
    from scripts import future_parent_selection_20261013 as design
    task=[t for t in design.tasks() if t['replicate']==0][0]
    r={'status':'TECHNICAL8_FULL_NATIVE_REPLAY_ADMITTED','cases':8,'records':[{'task':task}]*8}
    (tmp_path/'SHARD.json').write_text(json.dumps(r))
    with pytest.raises(ValueError,match='technical8 domain'):
        runner.technical_gate(tmp_path,None,None,None,None,None)


def test_full_reader_rejects_missing_cases_source_or_horizon_before_raw_read():
    from scripts import aggregate_future_parent_selection_20261013 as reader
    r={'status':'COMPLETE_EQUAL_PARENT_SHARD','cases':256,'records':[{} for _ in range(256)],'shard':0,
       'input_sha256':'51a07a843a087059af3d67ad113f5d849644f5b03739a6df986d506bd636648f',
       'runner_sha256':'runner','design_sha256':'design','updates':51200}
    reader.admit_shard_header(r,0,'runner','design')
    for field,value in (('cases',255),('updates',51199),('runner_sha256','other'),('records',[{}]*255),('shard',1)):
        bad=dict(r);bad[field]=value
        with pytest.raises(ValueError):reader.admit_shard_header(bad,0,'runner','design')


def test_registered_workflow_requires_technical_before_all16_shards():
    from pathlib import Path
    s=Path('.github/workflows/chapter2-pr471-native-verification.yml').read_text(encoding='utf-8')
    assert 'future-parent-selection' in s
    technical=s.split('  future-parent-technical:',1)[1].split('  future-parent-biological:',1)[0]
    assert 'scipy==1.15.3' in technical
    assert 'psutil==7.2.2' in technical
    assert 'threadpoolctl==3.6.0' in technical
    assert 'needs: future-parent-technical' in s
    assert 'needs: future-parent-biological' in s
    assert 'python -m scripts.admit_parent_selection_references_20261013' in s
    assert 'python -m scripts.aggregate_future_parent_selection_20261013' in s


@pytest.fixture
def sampler_trace():
    from dataclasses import replace
    from scripts.run_model3_assurance_intervention import founders,config
    from scripts.run_model3_persistent_isolation import exposure
    from scripts import run_future_parent_selection_20261013 as r
    s=founders();c=replace(config('assurance_cost',.01,'evolving'),years=4,survival=0.)
    v=exposure(76001,'near').visitors[0]
    return r,s,v,c,r.trajectory(s,v,c,17,'native',horizon=4)


@pytest.mark.parametrize('field',['population','parentage'])
def test_replay_rejects_floating_identity_count_arrays(sampler_trace,field):
    r,s,v,c,z=sampler_trace;bad={k:a.copy() for k,a in z.items()};bad[field]=bad[field].astype(float)
    with pytest.raises(ValueError,match='integer'):
        r.verify(bad,s,v,c,17,'native')


def test_replay_rejects_unused_prepended_rows_with_shifted_offset_origins(sampler_trace):
    from scripts import persistence_expression_mechanism_20261012 as old
    r,s,v,c,z=sampler_trace;bad={k:a.copy() for k,a in z.items()}
    for f in old.FIELDS:bad[f]=np.concatenate([z[f][:1],z[f]])
    for f in ('offsets','matrix_offsets','parent_offsets'):bad[f]+=1
    for f in ('sampling_weights','native_outcross','native_self_viable'):bad[f]=np.concatenate([[0.],z[f]])
    bad['parentage']=np.concatenate([np.zeros((1,3),dtype=np.int64),z['parentage']])
    with pytest.raises(ValueError,match='zero'):
        r.verify(bad,s,v,c,17,'native')


def test_technical_gate_requires_full1600_updates_before_reading_cases(tmp_path):
    import json
    from scripts import run_future_parent_selection_20261013 as r
    tasks=[t for t in assay.tasks() if t['replicate']==0]
    header={'status':'TECHNICAL8_FULL_NATIVE_REPLAY_ADMITTED','cases':8,'updates':8,'records':[{'task':t} for t in tasks]}
    (tmp_path/'SHARD.json').write_text(json.dumps(header))
    with pytest.raises(ValueError,match='200-update'):
        r.technical_gate(tmp_path,None,None,None,None,None)


def test_descriptive_genetics_use_allele_variance_and_separate_occupied_states(sampler_trace):
    from scripts import aggregate_future_parent_selection_20261013 as reader
    r,s,v,c,z=sampler_trace
    result=reader.trace_summaries(z)
    np.testing.assert_array_equal(result['occupied'],z['population']>0)
    np.testing.assert_allclose(result['allele_variance'][0],s.alleles.var(axis=(0,2)),atol=1e-12)
    assert result['fixed'].shape==(5,3)
    assert result['fixed'][0,2]==1
    np.testing.assert_array_equal(result['native_diagnostics'],z['diagnostics'])
