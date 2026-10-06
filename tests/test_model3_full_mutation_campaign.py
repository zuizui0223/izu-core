"""Check the executed campaign's ecological contrasts and resume contract."""
import hashlib
import json
from dataclasses import replace

import numpy as np
import pytest

from scripts.run_model3_full_mutation import config, exposure, tasks, run_case
from scripts.model3_island.run import history_from_spec
from scripts.summarize_model3_full_mutation import read_case
from scripts import summarize_model3_full_mutation as summary


def test_campaign_preserves_stage1_and_declared_counts(tmp_path):
    stage1 = tasks(tmp_path, 'core', 32, 4)
    stage2 = tasks(tmp_path, 'core', 64, 8)
    assert len(stage1) == 1024
    assert len(stage2) == 4096
    assert set(stage1) <= set(stage2)
    assert len(tasks(tmp_path, 'density')) == 144
    assert len(tasks(tmp_path, 'benchmark')) == 128
    assert len({t[1] for t in stage2}) == len(stage2)


def test_common_environment_switch_and_no_plant_immigration():
    near, far = exposure(76001, 'near'), exposure(76001, 'far')
    c = config('assurance_cost', .01)
    original = history_from_spec(
        replace(c, visitor_arrival=replace(c.visitor_arrival, distance=3)),
        {'kind': 'assembly'}, 76001)
    assert c.assurance_mode == 'evolving'
    assert c.capacity == 48 and c.years == 1000
    for t in range(1000):
        expected = original.visitors[t] if t < 200 else near.visitors[t]
        for field in ('ids', 'optima', 'breadths', 'effectiveness'):
            np.testing.assert_array_equal(getattr(far.visitors[t], field), getattr(expected, field))
        assert len(near.seed_candidates[t].ids) == len(far.seed_candidates[t].ids) == 0


def test_corrupted_case_is_not_resumed_or_summarized(tmp_path):
    task = tasks(tmp_path, 'core', 1, 1)[0]
    key = task[1]
    path = tmp_path / (key + '.npz')
    np.savez(path, trace=np.zeros((1001, 10)))
    receipt = {'task': list(task[2:]), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    (tmp_path / (key + '.json')).write_text(json.dumps(receipt))
    assert run_case(task) == key
    with path.open('ab') as handle:
        handle.write(b'corruption')
    with pytest.raises(ValueError, match='invalid existing case'):
        run_case(task)
    with pytest.raises(ValueError, match='hash mismatch'):
        read_case(tmp_path, key)


def test_summary_retains_direction_alleles_and_history_level_precision(tmp_path, monkeypatch):
    for task in tasks(tmp_path, 'benchmark'):
        (tmp_path / (task[1] + '.json')).write_text('{}')

    def synthetic_trace(out, key):
        trace = np.zeros((1001, 10))
        trace[:, 0] = 48
        trace[:, 1:4] = .5
        trace[:, 7:] = [3, 5, 7]
        if key.endswith('_far'):
            trace[1:, 2] = .4
            trace[1:, 3] = .6
        return trace

    monkeypatch.setattr(summary, 'read_case', synthetic_trace)
    result = summary.core_summary(tmp_path, 32, 4, 'benchmark')
    assert result['n_cases'] == 128
    assert result['precision_all_pass']
    for row in result['rows']:
        assert row['paired_occupancy'] == 1
        investment = row['traits']['investment']
        assert investment['mean_gap'] == pytest.approx(-.1)
        assert investment['far_change_from_founders'] == pytest.approx(-.1)
        assert investment['near_mean_allele_count'] == 5
        assert investment['halfwidth'] == 0
        assert investment['mean_last100_change_far'] == 0
        assert row['traits']['assurance']['mean_gap'] == pytest.approx(.1)


def test_three_way_comparison_keeps_signed_discrepancies(tmp_path, monkeypatch):
    def synthetic_trace(out, key):
        trace = np.zeros((1001, 10))
        trace[:, 0] = 48
        value = .3 if key.startswith('benchmark') else (.6 if key.endswith('heat_fv') else .5)
        trace[:, 1:4] = value
        return trace

    monkeypatch.setattr(summary, 'read_case', synthetic_trace)
    result = summary.benchmark_comparison(tmp_path)
    assert len(result['rows']) == 96
    for row in result['rows']:
        np.testing.assert_allclose(
            np.array(row['abm_minus_density']) + row['density_minus_heat'],
            row['abm_minus_heat'], atol=1e-15)
        np.testing.assert_allclose(row['abm_minus_heat'], -.3 if row['mutation_rate'] else -.2)


def test_summary_rejects_valid_bytes_with_wrong_condition_receipt(tmp_path):
    near, far = tasks(tmp_path, 'core', 1, 1)[:2]
    path = tmp_path / (near[1] + '.npz')
    np.savez(path, trace=np.zeros((1001, 10)))
    receipt = {'task': list(far[2:]), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    (tmp_path / (near[1] + '.json')).write_text(json.dumps(receipt))
    with pytest.raises(ValueError, match='task mismatch'):
        read_case(tmp_path, near[1])


def test_density_summary_reports_both_refinements(tmp_path, monkeypatch):
    def synthetic_trace(out, key):
        trace = np.zeros((1001, 10))
        trace[:, 0] = 48
        trace[:, 1:4] = .2 if '_n5_' in key else (.3 if '_n7_' in key else .305)
        return trace
    monkeypatch.setattr(summary, 'read_case', synthetic_trace)
    result = summary.density_summary(tmp_path)
    rows = [row for row in result['rows'] if 'scheme' in row]
    assert len(rows) == 48
    for row in rows:
        assert row['terminal_grid_gap_5_to_7'] == pytest.approx(.1)
        assert row['full_trajectory_max_grid_gap_5_to_7'] == pytest.approx(.1)
        assert row['terminal_grid_gap'] == pytest.approx(.005)
        assert row['terminal_grid_pass']
