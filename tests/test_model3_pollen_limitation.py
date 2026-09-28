import numpy as np
import pytest

from scripts.model3_pollen_limitation import pollination_counterfactual


def test_no_visitors_distinguishes_raw_assurance_from_inbreeding_loss():
    report=pollination_counterfactual(np.zeros((2,2)),np.array([8.,8.]),1.,.5,.9)
    assert report['pollen_limitation_before_selfing']==1
    assert report['viable_seed_limitation']==pytest.approx(.95)
    assert report['selfed_raw']==8
    assert report['selfed_viable']==pytest.approx(.8)
    assert report['inbreeding_loss']==pytest.approx(7.2)
    assert report['supplemented_outcross']==16


def test_complete_depression_can_remove_assurance_benefit():
    report=pollination_counterfactual(np.zeros((2,2)),np.array([8.,8.]),1.,1.,1.)
    assert report['selfed_raw']==16
    assert report['open_viable']==0
    assert report['viable_seed_limitation']==1


def test_no_selfing_makes_depression_irrelevant():
    transfer=np.array([[0.,.5],[.5,0.]])
    a=pollination_counterfactual(transfer,np.array([8.,8.]),1.,0.,0.)
    b=pollination_counterfactual(transfer,np.array([8.,8.]),1.,0.,1.)
    assert a==b


def test_more_compatible_pollen_reduces_limitation_at_same_resources():
    transfer=np.array([[0.,.5],[.5,0.]])
    a=pollination_counterfactual(transfer,np.array([8.,8.]),1.,.5,.5)
    b=pollination_counterfactual(transfer*4,np.array([8.,8.]),1.,.5,.5)
    assert b['pollen_limitation_before_selfing']<a['pollen_limitation_before_selfing']
    assert b['viable_seed_limitation']<a['viable_seed_limitation']


def test_zero_ovules_is_not_evidence_of_no_pollen_limitation():
    report=pollination_counterfactual(np.zeros((2,2)),np.zeros(2),1.,.5,.5)
    assert report['pollen_limitation_before_selfing'] is None
    assert report['viable_seed_limitation'] is None
