from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pytest
from scripts import assurance_parent_control_20261014 as design
from scripts import run_assurance_parent_control_20261014 as runner


@dataclass
class State:
    alleles: np.ndarray
    ids: np.ndarray


def test_registered_sampler_ledger_is_separate_from_native_book(monkeypatch):
    def reproduction(state, visitors, cfg, policy):
        traits = state.alleles.mean(2)
        n = len(traits)
        return SimpleNamespace(outcross=np.zeros((n, n)), self_viable=traits[:, 2], ovules=np.ones(n))
    monkeypatch.setattr(design.native, 'expression_ledger', reproduction)
    state = State(np.array([[[.5,.5],[.5,.5],[.2,.2]],[[.5,.5],[.5,.5],[.8,.8]]]), np.arange(2))
    native, sampled, matrix = runner.ledger_and_weights(state, None, None, design.POLICY)
    np.testing.assert_array_equal(native.self_viable, [.2,.8])
    np.testing.assert_allclose(sampled.self_viable, [.5,.5])
    np.testing.assert_allclose(matrix, [[.5,0],[0,.5]])
    same, native_sampler, _ = runner.ledger_and_weights(state, None, None, 'native')
    assert same is native_sampler
    with pytest.raises(ValueError):
        runner.ledger_and_weights(state, None, None, 'A_mean_equal_uniform_parents')


def test_source_gate_rejects_missing_declaration_before_output(monkeypatch, tmp_path):
    monkeypatch.setattr(runner, 'SOURCE_BINDINGS', tmp_path / 'missing.json')
    with pytest.raises(FileNotFoundError):
        runner.run(tmp_path / 'input', tmp_path / 'references', 0, tmp_path / 'out', technical=True)
    assert not (tmp_path / 'out').exists()


def test_bad_shard_rejected_without_starting_futures(tmp_path):
    with pytest.raises(ValueError, match='invalid shard'):
        runner.run(tmp_path / 'input', tmp_path / 'references', 16, tmp_path / 'out')
    assert not (tmp_path / 'out').exists()


def test_production_cannot_start_before_independent_reader_gate(monkeypatch, tmp_path):
    monkeypatch.setattr(runner, 'source_gate', lambda: {'production_gate_open': False})
    with pytest.raises(ValueError, match='independent controlled reader'):
        runner.run(tmp_path / 'input', tmp_path / 'references', 0, tmp_path / 'out')
    assert not (tmp_path / 'out').exists()


def test_old_self_reported_reference_receipt_is_insufficient(monkeypatch, tmp_path):
    import json
    root = tmp_path / 'references'
    (root / 'verified').mkdir(parents=True)
    raw = b'old outcomes'
    (root / 'verified/all_start_outcomes.npz').write_bytes(raw)
    (root / 'ADMISSION.json').write_text(json.dumps({
        'status': 'ALL4096_ORIGINAL_MEAN_NATIVE_REFERENCES_ADMITTED',
        'cases':4096,'prior_sha256':'f3045118f51947e9eaa2dd71f275b5bc1428aa2042dd0c2af95bcaa5ca2b14f5',
        'outcome_npz_sha256':runner.old.digest(raw)}),encoding='utf-8')
    monkeypatch.setattr(runner,'source_gate',lambda:{'production_gate_open':False})
    with pytest.raises(ValueError,match='independent reference receipt'):
        runner.admit_reference_root(root)


def test_production_requires_independent_native_control_receipt_before_reference_loading(monkeypatch,tmp_path):
    monkeypatch.setattr(runner,'source_gate',lambda:{'production_gate_open':True})
    with pytest.raises(ValueError,match='independent native control receipt'):
        runner.run(tmp_path/'input',tmp_path/'references',0,tmp_path/'out')
    assert not (tmp_path/'out').exists()
