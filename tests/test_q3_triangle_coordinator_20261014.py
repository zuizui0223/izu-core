from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
import time

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_q3_triangle_20261014 as run


def test_dispatch_reserves_each_job_before_work_and_does_not_repeat(tmp_path, monkeypatch):
    cases = [dict(key='one', trigger=199, remaining_updates=1)]
    (tmp_path/'triplets').mkdir()
    monkeypatch.setattr(run, 'ProcessPoolExecutor', ThreadPoolExecutor, raising=False)
    def worker(case, replicate, out, execution_sha, deadline):
        claim = Path(out)/'budget'/f"claim-one-{replicate:03d}.json"
        assert json.loads(claim.read_text())['native_updates_reserved'] == 6
        return dict(key='one', replicate=replicate, production_updates=3, native_updates=3)
    monkeypatch.setattr(run, 'run_triplet', worker, raising=False)
    result = run.dispatch(cases, 0, tmp_path, 'd'*64, '123', time.monotonic()+30)
    assert {(r['key'], r['replicate']) for r in result} == {('one', r) for r in range(8)}
    assert len(list((tmp_path/'budget').glob('claim-*.json'))) == 8
    with pytest.raises(FileExistsError):
        run.dispatch(cases, 0, tmp_path, 'd'*64, '123', time.monotonic()+30)


def test_dispatch_failure_preserves_reserved_work_and_stops_submitting(tmp_path, monkeypatch):
    monkeypatch.setattr(run, 'ProcessPoolExecutor', ThreadPoolExecutor, raising=False)
    def worker(*args):
        raise ValueError('synthetic replay mismatch')
    monkeypatch.setattr(run, 'run_triplet', worker, raising=False)
    with pytest.raises(ValueError, match='synthetic replay mismatch'):
        run.dispatch([dict(key='one', trigger=199, remaining_updates=1)], 0, tmp_path,
                     'd'*64, '123', time.monotonic()+30)
    assert (tmp_path/'ABORT').exists()
    assert 1 <= len(list((tmp_path/'budget').glob('claim-*.json'))) <= 2


def test_deadline_prevents_first_submission(tmp_path, monkeypatch):
    monkeypatch.setattr(run, 'ProcessPoolExecutor', ThreadPoolExecutor, raising=False)
    monkeypatch.setattr(run, 'run_triplet', lambda *a:pytest.fail('worker after deadline'), raising=False)
    with pytest.raises(ValueError, match='deadline'):
        run.dispatch([dict(key='one', trigger=199, remaining_updates=1)], 0, tmp_path,
                     'd'*64, '123', time.monotonic()-1)
    assert not list((tmp_path/'budget').glob('claim-*.json'))
