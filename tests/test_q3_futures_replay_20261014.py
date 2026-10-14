import importlib.util
from pathlib import Path
import sys

import numpy as np
import pytest


def api():
    scripts=Path(__file__).parents[1]/'scripts'
    sys.path.insert(0,str(scripts))
    path=scripts/'verify_q3_futures_paths_20261014.py'
    assert path.exists(), 'independent path verifier missing'
    spec=importlib.util.spec_from_file_location('q3_replay_test',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def fixture():
    return dict(offsets=np.array([0,2,3]), parent_offsets=np.array([0,1]),
                ids=np.array([0,1,48]), alleles=np.full((3,3,2),.5),
                allele_origin=np.zeros((3,3,2),dtype=np.int64), mutation_flags=np.zeros((3,3,2),dtype=bool),
                birth_years=np.array([0,0,1]), parentage=np.array([[48,0,1]]))


@pytest.mark.parametrize('field', ['offsets','parent_offsets','parentage','alleles','ids','birth_years'])
def test_raw_shape_bounds_parent_identity_and_time_corruption(field):
    m=api();a=fixture();m.validate_layout(a,0,1)
    if field=='offsets':a[field][-1]=4
    elif field=='parent_offsets':a[field][-1]=2
    elif field=='parentage':a[field][0,1]=99
    elif field=='alleles':a[field][0,1,0]=np.nan
    elif field=='ids':a[field][1]=0
    else:a[field][-1]=2
    with pytest.raises(ValueError):m.validate_layout(a,0,1)


def test_empty_census_retained_and_terminal_mean_undefined():
    m=api();a=fixture();a['offsets']=np.array([0,3,3]);a['parent_offsets']=np.array([0,0]);a['parentage']=np.empty((0,3),dtype=np.int64)
    a['birth_years'][:]=0
    m.validate_layout(a,0,1)
    assert m.mean_path(a)==[.5,None]
