import importlib
import numpy as np
import pytest


def test_partial_campaign_is_rejected_before_data_read(tmp_path):
    m=importlib.import_module('scripts.summarize_model3_assurance_intervention')
    with pytest.raises(ValueError,match='incomplete'):
        m.require_complete(tmp_path)


def test_interaction_uses_only_same_four_surviving_cells():
    m=importlib.import_module('scripts.summarize_model3_assurance_intervention')
    values=np.zeros((1,2,2,2,3))
    values[:,:,0,1,:]=1
    values[:,:,1,1,:]=3
    values[:,1,1,1,:]=100
    alive=np.ones((1,2,2,2),dtype=bool);alive[0,1,0,0]=False
    d,counts=m.interaction(values,alive)
    assert np.array_equal(d,[[2,2,2]])
    assert counts.tolist()==[1]


def test_empty_history_remains_undefined():
    m=importlib.import_module('scripts.summarize_model3_assurance_intervention')
    values=np.ones((2,2,3));mask=np.array([[True,False],[False,False]])
    means,counts=m.history_means(values,mask)
    assert counts.tolist()==[1,0]
    assert np.array_equal(means[0],[1,1,1]) and np.isnan(means[1]).all()
