import numpy as np
import pytest
from audit_access import excluded,homolog_matches,events,summarize,schema


def test_directional_exclusion_can_hold_with_two_alleles_remaining():
    # Initial I=.5, threshold .45; .5/.625 are variable but cannot reach .45.
    assert excluded(4,384,48)
    assert not excluded(3,384,48)


def test_exact_bound_equality_does_not_exclude_target():
    # Initial mean .55 at N5, target .5; equality remains allowed.
    assert not excluded(4,44,5)


def test_parent_value_and_origin_must_belong_to_same_homolog():
    values=np.array([[.375,.625]]);origins=np.array([[10,11]])
    assert not homolog_matches(values,origins,np.array([0]),np.array([.375]),np.array([11]))[0]
    assert homolog_matches(values,origins,np.array([0]),np.array([.375]),np.array([10]))[0]


def test_original_stable_windows_and_tie_rule_remain():
    means=np.full((201,3),.5);means[10:,2]=.5625;means[12:,1]=.4375
    assert events(means,np.full(201,48))=={'A':10,'I':12,'category':'near_simultaneous'}


def test_timing_coincidence_is_not_hidden_in_before_bucket():
    row=dict(original_category='assurance_only',first_exclusion=29,first_single_allele_fixation=29,
             exclusion_before_fixation=False,exclusion_phenotype_variance=0.,missing_I=True,
             terminal_alive=True,terminal_excluded=True,original_A=10)
    table=summarize([row])
    assert table['A_only_excluded_at_A_completion']==1
    assert table['A_only_excluded_before_A_completion']==0
    assert table['excluded_at_fixation']==1
    assert set(table['original_categories'])=={'assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither'}


def test_fractional_ancestry_id_is_rejected_before_casting():
    a=dict(ids=np.array([1.5]),alleles=np.full((1,3,2),.5),allele_origin=np.zeros((1,3,2),int),
           mutation_flags=np.zeros((1,3,2),bool),birth_years=np.zeros(1,int),population=np.zeros(201,int),
           offsets=np.zeros(202,int),parent_offsets=np.zeros(201,int),parentage=np.empty((0,3),int),means=np.full((201,3),np.nan))
    with pytest.raises(ValueError,match='integer source field'):
        schema(a)


@pytest.mark.parametrize('mode',['missing','duplicate'])
def test_independent_cell_inventory_cannot_omit_or_repeat_cells(mode):
    from verify_access import cell_inventory
    cells=[dict(block=b,context=c) for b in ('main','confirmation') for c in range(9)]
    if mode=='missing':cells.pop()
    else:cells[-1]=cells[0]
    with pytest.raises(ValueError,match='cell inventory'):
        cell_inventory(cells)
