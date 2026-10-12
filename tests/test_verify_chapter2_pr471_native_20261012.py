"""Fail-closed comparison tests. Fixtures are not new biological outputs."""
from __future__ import annotations

import copy
import csv
import importlib
from pathlib import Path
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / 'data/results/chapter2_pr471_independent_baseline_20261012.csv'
MODULE = 'scripts.verify_chapter2_pr471_native_20261012'


def tool():
    assert importlib.util.find_spec(MODULE) is not None, 'native comparator not implemented'
    return importlib.import_module(MODULE)


def payload():
    """Turn the committed numerical baseline into an explicit test fixture."""
    result = {
        'schema': 'chapter2_q3q4_statewise_total_pollen_equalized_v1',
        'status': 'EXPLORATORY_STATEWISE_EQUAL_TOTAL_POLLEN_NEGATIVE_CONTROL_NO_CAUSAL_MEDIATION',
        'n_independent_biological_histories': 0, 'n_visitor_types_each_arm': 4,
        'n_original_mating_systems': 4, 'n_resource_budgets': 2,
        'n_functional_shifts': 3, 'n_source_settings': 24,
        'states_per_operator': 165, 'results': [],
    }
    for source in csv.DictReader(BASELINE.open()):
        row = {'setting': source['setting'], 'full_arms': {}}
        for name, value in source.items():
            if name == 'setting':
                continue
            if '::' in name:
                arm, metric = name.split('::')
                row['full_arms'].setdefault(arm, {})[metric] = float(value)
            else:
                row[name] = float(value)
        result['results'].append(row)
    return result


def test_all_480_values_and_order_independence():
    m = tool()
    p = payload()
    p['results'].reverse()
    out = m.compare_results(p, m.load_expected(BASELINE))
    assert out['status'] == 'NATIVE_OUTPUT_MATCHES_INDEPENDENT_BASELINE'
    assert out['contexts'] == 24
    assert out['comparisons'] == 480
    assert out['max_absolute_error'] == 0.0


@pytest.mark.parametrize('change', ['duplicate', 'missing', 'unknown_context', 'wrong_count', 'wrong_schema', 'missing_arm'])
def test_coverage_or_contract_corruption_is_rejected(change):
    m = tool()
    p = payload()
    if change == 'duplicate':
        p['results'][-1] = copy.deepcopy(p['results'][0])
    elif change == 'missing':
        p['results'].pop()
    elif change == 'unknown_context':
        p['results'][0]['mismatch_fraction'] = .75
    elif change == 'wrong_count':
        p['n_independent_biological_histories'] = 24
    elif change == 'wrong_schema':
        p['schema'] = 'different_experiment'
    else:
        p['results'][0]['full_arms'].pop('native|shifted4')
    with pytest.raises(ValueError):
        m.compare_results(p, m.load_expected(BASELINE))


@pytest.mark.parametrize('value', [float('nan'), float('inf'), None, True, '0.0'])
def test_invalid_native_number_is_rejected(value):
    m = tool()
    p = payload()
    p['results'][0]['P80_native_shift_minus_equalized'] = value
    with pytest.raises(ValueError):
        m.compare_results(p, m.load_expected(BASELINE))


def test_small_residual_cannot_be_silently_zeroed():
    m = tool()
    p = payload()
    smallest = min(p['results'], key=lambda r: abs(r['P80_native_shift_minus_equalized']))
    smallest['P80_native_shift_minus_equalized'] = 0.0
    with pytest.raises(ValueError, match='numerical mismatch'):
        m.compare_results(p, m.load_expected(BASELINE))


def test_recorded_absolute_tolerance_not_relative_tolerance():
    m = tool()
    p = payload()
    p['results'][0]['full_arms']['native|shifted4']['P80_occupied'] += 5e-13
    assert m.compare_results(p, m.load_expected(BASELINE))['comparisons'] == 480
    p['results'][0]['full_arms']['native|shifted4']['P80_occupied'] += 5e-11
    with pytest.raises(ValueError, match='numerical mismatch'):
        m.compare_results(p, m.load_expected(BASELINE))


def test_baseline_byte_drift_is_rejected(tmp_path):
    m = tool()
    altered = tmp_path / 'altered.csv'
    altered.write_bytes(BASELINE.read_bytes() + b'\n')
    with pytest.raises(ValueError, match='baseline SHA-256'):
        m.load_expected(altered)


def test_checkout_requires_exact_commit_and_clean_tracked_source(tmp_path):
    m = tool()
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    tracked = tmp_path / 'native.py'
    tracked.write_text('x = 1\n')
    subprocess.run(['git', '-C', str(tmp_path), 'add', 'native.py'], check=True)
    subprocess.run(['git', '-C', str(tmp_path), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture'], check=True)
    head = subprocess.check_output(['git', '-C', str(tmp_path), 'rev-parse', 'HEAD'], text=True).strip()
    assert m.check_checkout(tmp_path, head)['commit'] == head
    with pytest.raises(ValueError, match='source commit'):
        m.check_checkout(tmp_path, '0' * 40)
    tracked.write_text('x = 2\n')
    with pytest.raises(ValueError, match='modified source'):
        m.check_checkout(tmp_path, head)


def test_native_workflow_is_manual_only():
    import re
    source = (ROOT / '.github/workflows/chapter2-pr471-native-verification.yml').read_text()
    block = source.split('\non:\n', 1)[1].split('\npermissions:', 1)[0]
    assert set(re.findall(r'^  ([A-Za-z0-9_-]+)\s*:', block, re.MULTILINE)) == {'workflow_dispatch'}
