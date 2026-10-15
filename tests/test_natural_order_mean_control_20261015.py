import numpy as np
import pytest

from scripts import natural_order_mean_control_20261015 as study


def test_original_seed_excludes_policy_target_and_width():
    a = dict(block='main', replicate=7, target=1.05, policy='normalized', width=99)
    b = dict(block='main', replicate=7, target=1.5, policy='native')
    assert study.future_seed(a) == study.future_seed(b)
    assert study.future_seed(a) != study.future_seed(dict(b, replicate=8))


def test_all_start_paired_gaps_use_fractions_and_declared_signs():
    records = [
        dict(block='main', target=1.05, category='assurance_first', native=1, normalized=0,
             native_duration=200, normalized_duration=100),
        dict(block='main', target=1.05, category='assurance_first', native=0, normalized=1,
             native_duration=20, normalized_duration=80),
        dict(block='main', target=1.05, category='investment_first', native=0, normalized=1,
             native_duration=40, normalized_duration=90),
    ]
    result = study.describe(records)
    row = next(r for r in result['strict_gaps'] if r['block']=='main' and r['target']==1.05)
    assert row['native_occupancy_gap'] == .5
    assert row['normalized_occupancy_gap'] == -.5
    assert row['occupancy_attenuation'] == 1
    assert row['native_duration_gap'] == 70
    assert row['normalized_duration_gap'] == 0
    group = next(r for r in result['groups'] if r['block']=='main' and
                 r['target']==1.05 and r['category']=='assurance_first')
    assert group['paired_gains'] == group['paired_losses'] == 1
    assert group['duration_change'] == -20


def test_empty_groups_are_undefined_and_all36_groups_retained():
    result = study.describe([])
    assert len(result['groups']) == 36
    assert all(r['native_fraction'] is None for r in result['groups'])
    assert all(r['occupancy_attenuation'] is None for r in result['strict_gaps'])


def test_completed_inventory_and_nonfinite_or_duplicate_outcomes_rejected():
    row = dict(block='main', target=1.05, category='neither', native=0, normalized=0,
               native_duration=0, normalized_duration=0)
    with pytest.raises(ValueError):
        study.describe([dict(row, native=np.nan)])
    with pytest.raises(ValueError):
        study.check_inventory([dict(row, replicate=0)]*2048)


def test_reservations_fail_closed_before_exceeding_frozen_cap():
    assert study.reserve_updates(820600, 200) == 820800
    with pytest.raises(ValueError):
        study.reserve_updates(820800, 200)


def test_bank_bytes_fail_closed(tmp_path):
    bad = tmp_path/'bad.zip'
    bad.write_bytes(b'not the source bank')
    with pytest.raises(ValueError, match='bank'):
        study.read_bank(bad)


def test_independent_initial_map_preserves_all_nonassurance_state():
    from scripts.natural_order_mean_replay_20261015 import independent_initial
    from scripts.model3_island.types import PlantState
    aa = np.full((8, 3, 2), .4)
    aa[:, 2, :] += np.arange(8)[:, None]/100
    state = PlantState(aa, np.arange(48).reshape(8,3,2), np.zeros((8,3,2),bool),
                       np.arange(8), np.full(8,200))
    changed = independent_initial(state)
    assert abs(changed.alleles[:,2,:].mean()-.5) < 1e-12
    np.testing.assert_array_equal(changed.alleles[:,:2,:], aa[:,:2,:])
    for f in ('allele_origin','mutation_flags','ids','birth_years'):
        np.testing.assert_array_equal(getattr(changed,f),getattr(state,f))
    assert not np.shares_memory(changed.alleles, state.alleles)


def test_execution_closure_rejects_source_or_runtime_drift(tmp_path):
    from scripts.run_natural_order_mean_control_20261015 import verify_closure
    p = tmp_path/'source.py'
    p.write_text('original\n')
    import sys
    frozen = dict(python=sys.version, numpy=np.__version__,
                  files={'source.py':study.digest(b'original\n')})
    verify_closure(frozen,tmp_path)
    p.write_text('changed\n')
    with pytest.raises(ValueError,match='source'):
        verify_closure(frozen,tmp_path)


def test_archive_layout_requires_all_censuses_and_inheritance_rows():
    from scripts.run_natural_order_mean_control_20261015 import validate_trace
    with pytest.raises(ValueError):
        validate_trace({'population':np.zeros(200,dtype=int)},horizon=200)


def test_native_three_column_parentage_and_absorbing_empty_trace():
    from scripts.run_natural_order_mean_control_20261015 import validate_trace
    d = dict(alleles=np.empty((0,3,2)), allele_origin=np.empty((0,3,2),int),
             mutation_flags=np.empty((0,3,2),bool), ids=np.empty(0,int), birth_years=np.empty(0,int),
             population=np.zeros(2,int), offsets=np.zeros(3,int), means=np.full((2,3),np.nan),
             diagnostics=np.zeros((1,11)), parentage=np.empty((0,3),int))
    validate_trace(d,horizon=1)


def test_worker_source_drift_stops_before_loading_bank_or_native_call(monkeypatch):
    from scripts import run_natural_order_mean_control_20261015 as runner
    def drift(*args, **kwargs):
        raise ValueError('source drift fixture')
    def forbidden(*args, **kwargs):
        pytest.fail('no bank load or native transition after source drift')
    monkeypatch.setattr(runner,'verify_closure',drift)
    monkeypatch.setattr(runner.contract,'read_bank',forbidden)
    monkeypatch.setattr(runner.native,'trajectory',forbidden)
    runner.init_worker('absent','absent','absent',0,{'files':{}})
    with pytest.raises(ValueError,match='worker source admission'):
        runner.work(('production',0,1.05))
