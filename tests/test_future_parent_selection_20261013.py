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
