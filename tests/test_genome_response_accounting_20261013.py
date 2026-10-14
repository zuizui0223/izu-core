"""Known selection, parent-lottery, transmission and mutation contrasts."""
import numpy as np
import pytest
from types import SimpleNamespace
import scripts.audit_genome_response_accounting_20261013 as audit_module

from scripts.audit_genome_response_accounting_20261013 import decompose_step


def sample():
    source=np.array([[.5,.5,.5],[.5,.5,.5]])
    mothers=np.array([[.25,.5,.25],[.25,.5,.25]])
    fathers=mothers.copy()
    expected=np.array([.75,.5,.75])
    premut=np.full((2,3,2),.5)
    final=premut.copy();final[:,[0,2],:]=.6
    return source,mothers,fathers,expected,premut,final


def test_four_distinct_components_match_hand_calculated_change():
    r=decompose_step(*sample())
    np.testing.assert_allclose(r['selection'],[.25,0,.25])
    np.testing.assert_allclose(r['parent_sampling'],[-.5,0,-.5])
    np.testing.assert_allclose(r['transmission'],[.25,0,.25])
    np.testing.assert_allclose(r['birth_mutation'],[.1,0,.1])
    np.testing.assert_allclose(r['observed_change'],[.1,0,.1])
    assert r['closure_error']<1e-14


def test_stochastic_parent_choice_is_not_called_mutation():
    x=list(sample());x[4]=np.repeat(x[1][:,:,None],2,axis=2);x[5]=x[4].copy()
    r=decompose_step(*x)
    np.testing.assert_array_equal(r['birth_mutation'],np.zeros(3))
    np.testing.assert_array_equal(r['transmission'],np.zeros(3))
    np.testing.assert_allclose(r['parent_sampling'],[-.5,0,-.5])


def test_density_change_does_not_change_mean_accounting_denominator():
    x=list(sample());x[1]=x[1][:1];x[2]=x[2][:1];x[4]=x[4][:1];x[5]=x[5][:1]
    r=decompose_step(*x)
    np.testing.assert_allclose(r['observed_change'],[.1,0,.1])
    assert r['source_census']==2 and r['offspring_census']==1


def test_extinction_has_no_imputed_trait_change():
    x=list(sample());x[1]=x[1][:0];x[2]=x[2][:0];x[4]=x[4][:0];x[5]=x[5][:0]
    r=decompose_step(*x)
    assert r['eligible'] is False and r['reason']=='no_offspring_trait_mean'
    assert 'observed_change' not in r


@pytest.mark.parametrize('index,value',[
    (0,np.full((2,3),np.nan)),(3,np.array([np.inf,.5,.5])),
    (4,np.full((2,3,2),1.1)),(1,np.zeros((1,3))),
])
def test_nonfinite_or_incompatible_genetic_inputs_refused(index,value):
    x=list(sample());x[index]=value
    with pytest.raises(ValueError):decompose_step(*x)


def recorded_ledger():
    ledger=SimpleNamespace(maternal=np.array([3.]),paternal=np.array([3.]),
       outcross=np.array([[1.]]),self_viable=np.array([2.]),self_raw=np.array([4.]),
       exported=np.array([5.]),delivered=np.array([3.]),lost=np.array([2.]))
    record=dict(maternal_total=3.,paternal_total=3.,outcross_total=1.,self_viable=2.,
                self_raw=4.,pollen_export=5.,pollen_delivered=3.,pollen_lost=2.)
    return ledger,record


def test_actual_self_viable_field_is_checked_not_silently_skipped():
    ledger,record=recorded_ledger();record['self_viable']=2.1
    with pytest.raises(ValueError,match='self_viable'):
        audit_module.check_recorded_ledger(ledger,record)


def test_missing_required_ledger_is_not_an_alias_or_optional_field():
    ledger,record=recorded_ledger();record['self_viable_total']=record.pop('self_viable')
    with pytest.raises(ValueError,match='self_viable'):
        audit_module.check_recorded_ledger(ledger,record)


def test_nonfinite_pollen_diagnostic_and_valid_full_ledger():
    ledger,record=recorded_ledger()
    assert audit_module.check_recorded_ledger(ledger,record)==0.
    record['pollen_export']=np.nan
    with pytest.raises(ValueError,match='pollen_export'):
        audit_module.check_recorded_ledger(ledger,record)
