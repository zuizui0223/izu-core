import importlib.util
from pathlib import Path
import numpy as np
import pytest

def api():
    p=Path(__file__).parents[1]/'scripts/run_investment_variation_restoration_20261013.py'
    assert p.exists(), 'approved restoration adapter missing'
    spec=importlib.util.spec_from_file_location('restoration_probe',p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m

def test_restoration_preserves_every_expressed_mean_and_other_loci():
    a=np.array([[[.1,.2],[.375,.375],[.4,.7]],[[.8,.1],[.375,.375],[.2,.6]]])
    b=api().restore_alleles(a)
    np.testing.assert_array_equal(a.mean(axis=2),b.mean(axis=2))
    np.testing.assert_array_equal(a[:,[0,2],:],b[:,[0,2],:])
    assert b[:,1,:].var()==.0625**2
    assert np.all(a[:,1,:]==.375)

def test_nonfixed_and_out_of_bounds_edits_rejected():
    m=api()
    for pair in ([.3,.4],[0.,0.],[1.,1.]):
        a=np.full((2,3,2),.5);a[:,1,:]=pair
        with pytest.raises(ValueError):m.restore_alleles(a)

def test_primary_retains_no_trigger_pairs_and_never_zero_fills_extinction():
    m=api();rows=[]
    for block in ('causal_main','causal_confirmation'):
        for i in range(32):
            rows.append(dict(block=block,original_I=.375,restored_I=.25 if i else .375))
    result=m.primary(rows)
    assert result['estimate']==31/32*.125
    assert result['decision']=='supported_restored_reduction'
    rows[0]['restored_I']=None
    assert m.primary(rows)['decision']=='not_evaluable'
    with pytest.raises(ValueError):m.primary(rows[:-1])
