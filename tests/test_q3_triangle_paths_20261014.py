"""Short deterministic stand-in transitions: zero real native calls or draws."""
import importlib
import json
from pathlib import Path
import sys
import time
from types import SimpleNamespace

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))


def prepared(tmp_path, monkeypatch):
    run = importlib.import_module('run_q3_triangle_20261014')
    check = importlib.import_module('verify_q3_triangle_paths_20261014')
    from q3_triangle_contract_20261014 import seed_for
    fields = dict(alleles=np.full((48, 3, 2), .5), ids=np.arange(48),
                  allele_origin=np.zeros((48, 3, 2), dtype=np.int64),
                  mutation_flags=np.zeros((48, 3, 2), dtype=bool), birth_years=np.zeros(48, dtype=int))
    original = {k: np.concatenate([v]*201) for k, v in fields.items()}
    original.update(offsets=np.arange(202)*48,
                    metadata=np.array(json.dumps(dict(config={}, task=dict(composition='x')))))
    (tmp_path/'original').mkdir()
    (tmp_path/'raw').mkdir()
    path = tmp_path/'original'/'synthetic.npz'
    np.savez_compressed(path, **original)
    (tmp_path/'campaign.json').write_text('{"compositions":{"x":[0.5]}}')
    case = dict(key='synthetic', trigger=199, remaining_updates=1, fixed_I=.5,
                block='causal_main', original_npz_sha256=run.digest(path),
                seeds=[dict(replicate=0, **{p: str(seed_for('synthetic', 0, p))
                                           for p in ('allocation', 'dynamics')})])
    calls = []
    class State(SimpleNamespace):
        pass
    def advance(state, repro, empty, cfg, streams, **kwargs):
        calls.append(kwargs)
        values = {k: getattr(state, k).copy() for k in fields}
        parents = np.column_stack((state.ids+48, state.ids, state.ids))
        values['ids'] += 48
        return State(**values), dict(parentage=parents)
    native = (SimpleNamespace(PlantState=State, Config=SimpleNamespace(from_dict=lambda x:x),
                              VisitorState=lambda *x:x),
              SimpleNamespace(advance=advance), SimpleNamespace(reproduce=lambda *x:None),
              SimpleNamespace(STREAM_IDS=('one',), stream=lambda *x:object()))
    monkeypatch.setattr(run, 'load_native', lambda *a:native)
    monkeypatch.setattr(check, 'load_native', lambda *a:native)
    # Intercept both RNG constructors: no PCG state or actual permutation draw.
    class FixedGenerator:
        def permutation(self, n):
            return np.arange(n-1, -1, -1)
    monkeypatch.setattr(np.random, 'PCG64', lambda seed:seed)
    monkeypatch.setattr(np.random, 'Generator', lambda seed:FixedGenerator())
    return run, check, case, calls


def test_three_arms_independent_replay_full_fields_and_parents(tmp_path, monkeypatch):
    run, check, case, calls = prepared(tmp_path, monkeypatch)
    saved = run.produce_triplet(case, 0, tmp_path, 'd'*64, time.monotonic()+30)
    result = check.verify_triplet(case, 0, tmp_path, 'd'*64, time.monotonic()+30, saved)
    assert result['native_updates'] == 3 and len(calls) == 6
    assert result['state_field_checks'] == 30 and result['parent_checks'] == 3
    assert result['permutation'] == list(range(47, -1, -1))
    assert result['arms'] == {p: dict(I=.5, survived=True, event=False) for p in 'ABC'}
    assert all(c['mutation_traits'] == (False, False, True) for c in calls)
    with pytest.raises(FileExistsError):
        run.produce_triplet(case, 0, tmp_path, 'd'*64, time.monotonic()+30)


@pytest.mark.parametrize('field', ['allele_origin', 'mutation_flags', 'parentage', 'metadata'])
def test_raw_corruption_rejected_even_with_updated_transport_hash(tmp_path, monkeypatch, field):
    run, check, case, calls = prepared(tmp_path, monkeypatch)
    saved = run.produce_triplet(case, 0, tmp_path, 'd'*64, time.monotonic()+30)
    path = tmp_path/'raw'/saved['A']['name']
    with np.load(path, allow_pickle=False) as npz:
        arrays = {k: npz[k].copy() for k in npz.files}
    if field == 'metadata':
        doc = json.loads(str(arrays[field]));doc['permutation'] = list(range(48))
        arrays[field] = np.array(json.dumps(doc))
    else:
        arrays[field].flat[-1] = 1 if field != 'parentage' else 0
    np.savez_compressed(path, **arrays)
    saved['A'].update(sha256=run.digest(path), bytes=path.stat().st_size)
    with pytest.raises(ValueError):
        check.verify_triplet(case, 0, tmp_path, 'd'*64, time.monotonic()+30, saved)


def test_closed_main_without_approval_never_loads_native(tmp_path, monkeypatch):
    run = importlib.import_module('run_q3_triangle_20261014')
    monkeypatch.setattr(run, 'load_native', lambda *a:pytest.fail('native load before approval'))
    with pytest.raises(FileNotFoundError):
        run.main(['--repo', str(tmp_path), '--out', str(tmp_path/'output'), '--shard', '0',
                  '--archive', str(tmp_path/'input.zip')])


def test_full_history_event_survives_later_extinction_and_no_post_trigger_reset():
    check = importlib.import_module('verify_q3_triangle_paths_20261014')
    original = dict(alleles=np.full((201, 3, 2), .375), offsets=np.arange(202))
    original['alleles'][0, 1] = .5
    future = dict(alleles=np.full((1, 3, 2), .5), offsets=np.array([0, 1, 1]))
    assert check.read_endpoints(original, future, 199) == dict(I=None, survived=False, event=True)
    original['alleles'][:, 1] = .5
    assert check.read_endpoints(original, future, 199) == dict(I=None, survived=False, event=False)


def test_event_window_crosses_intervention_and_requires_twenty_censuses():
    check = importlib.import_module('verify_q3_triangle_paths_20261014')
    original = dict(alleles=np.full((201, 3, 2), .5), offsets=np.arange(202))
    original['alleles'][181:199, 1] = .375
    future = dict(alleles=np.full((2, 3, 2), .375), offsets=np.array([0, 1, 2]))
    assert check.read_endpoints(original, future, 199)['event'] is True
    original['alleles'][181, 1] = .5
    assert check.read_endpoints(original, future, 199)['event'] is False


def test_native_fixture_contract_uses_exactly_four_standin_calls(tmp_path, monkeypatch):
    run, check, case, calls = prepared(tmp_path, monkeypatch)
    result = run.native_fixtures(case, tmp_path, time.monotonic()+30)
    assert result['native_updates'] == len(calls) == 4
    assert result['scientific_trajectories'] == 0
    assert result['equal_state_parentage'] is True
    assert result['empty_continuation'] is True


def test_interruption_retains_durable_censuses_and_parentage(tmp_path, monkeypatch):
    run, check, case, calls = prepared(tmp_path, monkeypatch)
    case.update(trigger=198, remaining_updates=2)
    native = run.load_native(None);advance = native[1].advance
    def interrupted(*args, **kwargs):
        if len(calls) == 1:
            raise RuntimeError('synthetic interruption')
        return advance(*args, **kwargs)
    monkeypatch.setattr(native[1], 'advance', interrupted)
    with pytest.raises(RuntimeError, match='synthetic interruption'):
        run.produce_triplet(case, 0, tmp_path, 'd'*64, time.monotonic()+30)
    journal = tmp_path/'partial/synthetic__r000__A.journal'
    assert journal.exists()
    snapshots = list(run.read_journal(journal))
    assert [r['year'].item() for r in snapshots] == [198, 199]
    np.testing.assert_array_equal(snapshots[1]['parentage'][:, 0], np.arange(48, 96))
    np.testing.assert_array_equal(snapshots[1]['ids'], np.arange(48, 96))
    assert not (tmp_path/'raw/synthetic__r000__A.npz').exists()


def test_expired_fixture_deadline_cannot_spend_native_calls(tmp_path, monkeypatch):
    run, check, case, calls = prepared(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match='fixture deadline'):
        run.native_fixtures(case, tmp_path, time.monotonic()-1)
    assert calls == []
