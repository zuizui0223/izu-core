from pathlib import Path
import importlib.util
import numpy as np
import pytest

def api():
    p=Path(__file__).parents[1]/'scripts/audit_restored_investment_accounting_20261013.py'
    assert p.exists(),'restored investment accounting missing'
    spec=importlib.util.spec_from_file_location('restored_account',p)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def test_parent_sampling_can_offset_negative_expected_selection():
    # Source mean .5, expected return mean .47; sampled parents mean .55,
    # child copies mean .5625. Selection favors reduction; observed change increases.
    result=api().components(np.array([.4,.6]),np.array([.5,.6]),np.array([.5,.6]),
        np.array([[.5,.625],[.5,.625]]),-.03)
    assert result['selection']==-.03
    assert result['parent_sampling']==pytest.approx(.08)
    assert result['transmission']==pytest.approx(.0125)
    assert result['observed_change']==pytest.approx(.0625)
    assert sum(result[k] for k in ('selection','parent_sampling','transmission'))==pytest.approx(result['observed_change'])

def test_no_offspring_is_undefined_and_nonfinite_response_is_rejected():
    m=api()
    with pytest.raises(ValueError):m.components(np.array([.5]),np.array([]),np.array([]),np.empty((0,2)),0.)
    with pytest.raises(ValueError):m.components(np.array([.5]),np.array([.5]),np.array([.5]),np.array([[.5,.5]]),np.nan)
