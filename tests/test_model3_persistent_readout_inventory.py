"""Readout admission tests; no biological simulation or frozen-data edits."""
import copy
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from scripts import verify_model3_persistent_readout as verifier

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def inventory():
    result = json.loads((ROOT / 'data/results/model3_persistent_isolation_summary_20261005.json').read_text())
    plan = json.loads((ROOT / 'data/design/model3_temporal_order_diagnostic_20261005.json').read_text())
    # Only layout is under test; actual historical means/events remain untouched.
    curves = {f"{r['setting']}_u{r['mutation_rate']}_{r['contrast']}": np.zeros((64, 1001, 3))
              for r in result['temporal_order']}
    return result, plan, curves


def test_committed_result_has_complete_declared_inventory(inventory):
    verifier.validate_inventory(*inventory)


@pytest.mark.parametrize('field', ['temporal_order', 'endpoints'])
@pytest.mark.parametrize('corruption', ['empty', 'missing', 'duplicate', 'foreign'])
def test_reject_incomplete_or_duplicated_result_grid(inventory, field, corruption):
    result, plan, curves = inventory
    rows = result[field]
    if corruption == 'empty':
        rows.clear()
    elif corruption == 'missing':
        rows.pop()
    elif corruption == 'duplicate':
        rows[-1] = copy.deepcopy(rows[0])
    else:
        rows[-1]['setting'] = 'unregistered'
    with pytest.raises(ValueError, match='readout inventory'):
        verifier.validate_inventory(result, plan, curves)


@pytest.mark.parametrize('corruption', ['missing_curve', 'short_curve', 'missing_event', 'duplicate_event', 'extra_event'])
def test_reject_incomplete_arrays_and_history_bindings(inventory, corruption):
    result, plan, curves = inventory
    name = next(iter(curves))
    events = result['temporal_order'][0]['events']
    if corruption == 'missing_curve':
        del curves[name]
    elif corruption == 'short_curve':
        curves[name] = curves[name][:-1]
    elif corruption == 'missing_event':
        events.pop()
    elif corruption == 'duplicate_event':
        events[-1] = copy.deepcopy(events[0])
    else:
        events.append(copy.deepcopy(events[0]))
    with pytest.raises(ValueError, match='curve inventory|history events'):
        verifier.validate_inventory(result, plan, curves)


def test_main_cannot_verify_empty_readout_with_matching_hashes(tmp_path, monkeypatch):
    monkeypatch.setattr(verifier, '__file__', str(tmp_path / 'scripts/verifier.py'))
    output = tmp_path / 'outputs/model3_persistent_isolation_20261005'
    output.mkdir(parents=True)
    np.savez(output / 'temporal_order_curves.npz')
    result = {'temporal_order': [], 'endpoints': []}
    files = [
        ('data/design/model3_temporal_order_diagnostic_20261005.json', 'plan_sha256',
         json.dumps({'threshold_sensitivity': [.025, .05, .1]})),
        ('outputs/model3_persistent_isolation_20261005/sources.json', 'source_manifest_sha256', '{}'),
        ('scripts/summarize_model3_persistent_order.py', 'analysis_source_sha256', '# fixture; never executed'),
    ]
    for name, key, text in files:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        result[key] = hashlib.sha256(path.read_bytes()).hexdigest()
    result['curve_sha256'] = hashlib.sha256((output / 'temporal_order_curves.npz').read_bytes()).hexdigest()
    destination = tmp_path / 'data/results/model3_persistent_isolation_summary_20261005.json'
    destination.parent.mkdir(parents=True)
    destination.write_text(json.dumps(result))
    with pytest.raises(ValueError, match='readout inventory'):
        verifier.main()
