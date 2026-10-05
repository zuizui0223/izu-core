from importlib import import_module
from dataclasses import replace
import numpy as np
import pytest
from scripts.run_model3_assurance_intervention import founders, config
from scripts.run_model3_persistent_isolation import exposure


@pytest.mark.parametrize('timing', ['assurance_cost','prior_selfing'])
def test_no_visitor_exact_deficits_and_absolute_viable_output(timing):
    module=import_module('scripts.model3_trait_pollen_intervention')
    state=founders(); original=state.alleles.copy()
    visitors=exposure(76001,'near').visitors[0]
    visitors=replace(visitors, **{name:getattr(visitors,name)[:0] for name in visitors.__dataclass_fields__})
    c=config(timing,.01,'evolving')
    r=module.assay(state,visitors,c,investment=.25,capacity=.75)
    ovules=48*8*np.exp(-c.investment_cost*.25**2-c.assurance_cost*.75**2)
    assert r['raw_deficit']==pytest.approx(.25)
    expected=.625 if c.assurance_timing=='delayed' else .4
    assert r['viable_deficit']==pytest.approx(expected)
    assert r['natural_viable']==pytest.approx(ovules*.75*(1-c.depression))
    np.testing.assert_array_equal(state.alleles,original)


def test_rejects_fixed_config_that_would_ignore_assigned_capacity():
    module=import_module('scripts.model3_trait_pollen_intervention')
    with pytest.raises(ValueError):
        module.assay(founders(),exposure(76001,'near').visitors[0],config('assurance_cost',.01,'fixed'),investment=.5,capacity=.75)
