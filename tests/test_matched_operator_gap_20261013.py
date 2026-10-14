from dataclasses import replace
import numpy as np
import pytest
from scripts.run_model3_assurance_intervention import founders,config
from scripts.model3_island.population import subset
from scripts.model3_island.types import VisitorState
from scripts.model3_island.density import make_grid,project_state,density_step
from scripts.audit_matched_operator_gap_20261013 import density_return,partition_step


def fixture():
    s=subset(founders(),np.arange(4));a=np.array([[[.2,.2],[.2,.2],[.5,.5]],[[.2,.2],[.7,.7],[.5,.5]],[[.7,.7],[.2,.2],[.5,.5]],[[.7,.7],[.7,.7],[.5,.5]]])
    s=replace(s,alleles=a);c=replace(config('delayed_control',0.,'evolving'),survival=0.)
    v=VisitorState(np.arange(2),np.array([.2,.7]),np.array([.2,.2]),np.ones(2))
    return s,c,v


def test_density_reduction_matches_original_inheritance_and_ledger():
    s,c,v=fixture();grid=make_grid(tuple(np.unique(s.alleles[:,k]) for k in range(3)));_,counts=project_state(s,grid)
    for n in [4.,48.]:
        scaled=counts*n/4.;empty=subset(s,np.array([],int));w,l=density_step(scaled,grid,v,empty,c,mutation_traits=(False,False,False))
        r=density_return(s.alleles,v,c,n)
        np.testing.assert_allclose(r['mean'],w@grid.genotypes.mean(2)/w.sum(),rtol=0,atol=1e-12)
        assert abs(r['rate']-l.maternal.sum())<1e-12
        keep=np.flatnonzero(scaled)
        np.testing.assert_allclose(r['maternal_outcross'],l.outcross.sum(0)[keep],rtol=0,atol=1e-12)
        np.testing.assert_allclose(r['paternal_outcross'],l.outcross.sum(1)[keep],rtol=0,atol=1e-12)
        np.testing.assert_allclose(r['self_viable'],l.self_viable[keep],rtol=0,atol=1e-12)


def test_empirical_distribution_replication_keeps_same_density_return():
    s,c,v=fixture();r=density_return(s.alleles,v,c,24.)
    rr=density_return(np.repeat(s.alleles,3,axis=0),v,c,24.)
    np.testing.assert_allclose(r['mean'],rr['mean'],atol=1e-12,rtol=0)
    assert abs(r['rate']-rr['rate'])<1e-12


def test_partition_telescopes_without_treating_feedback_as_noise():
    p=partition_step(.5,.48,.6,.59,.49,.485,.475)
    assert abs(sum(p.values())-((.48-.59)-(.5-.6)))<1e-12
    assert p['remaining_path_feedback']!=0


def test_density_reduction_rejects_undefined_state_and_census():
    s,c,v=fixture()
    for a,n in [(s.alleles[:0],4.),(s.alleles,np.nan),(s.alleles,49.)]:
        with pytest.raises(ValueError):density_return(a,v,c,n)
