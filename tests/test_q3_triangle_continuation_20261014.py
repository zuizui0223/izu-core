import copy
import importlib
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))


def prior_evidence():
    run = dict(id=38528315875, head_sha='b51c374ac77e04254cb99e07fa492fc87113b7dc',
               run_attempt=1, status='completed', conclusion='failure')
    jobs = [dict(name=f'triangle-shard-{i}', status='completed', conclusion='cancelled', steps=[])
            for i in range(18)]
    jobs[0].update(conclusion='failure', started_at='2026-10-14T07:26:21Z',
                   completed_at='2026-10-14T07:26:52Z', steps=[
                       dict(name='Reserved production and complete independent replay', conclusion='failure', status='completed'),
                       dict(name='Preserve partial failure without restarting biology', conclusion='success', status='completed')])
    jobs.append(dict(name='triangle-verify-and-publish', status='completed', conclusion='skipped', steps=[]))
    return run, jobs


def test_exact_failed_attempt_is_admissible():
    m = importlib.import_module('q3_triangle_continuation_20261014')
    m.validate_prior(*prior_evidence())


@pytest.mark.parametrize('mutation', [
    lambda r,j:r.update(id=12), lambda r,j:r.update(head_sha='a'*40),
    lambda r,j:r.update(run_attempt=2), lambda r,j:r.update(conclusion='success'),
    lambda r,j:r.update(status='in_progress'), lambda r,j:j.pop(),
    lambda r,j:j[1].update(steps=[dict(name='biology', conclusion='success')]),
    lambda r,j:j[1].update(conclusion='success'), lambda r,j:j[0].update(conclusion='cancelled'),
    lambda r,j:j[0].update(completed_at='2026-10-14T07:27:22Z'),
    lambda r,j:j[0]['steps'][0].update(conclusion='success'),
])
def test_prior_work_or_identity_drift_is_rejected(mutation):
    m = importlib.import_module('q3_triangle_continuation_20261014')
    run, jobs = prior_evidence(); mutation(run, jobs)
    with pytest.raises(ValueError):
        m.validate_prior(run, jobs)


def test_cumulative_accounting_includes_consumed_fixtures_and_time():
    m = importlib.import_module('q3_triangle_continuation_20261014')
    current = dict(native_updates=6687364, fixture_updates=4, trajectories=26352)
    result = m.cumulative_accounting(current)
    assert result['native_updates'] == 6687368 and result['fixture_updates'] == 8
    assert result['reserved_hosted_runner_minutes'] == 300
    assert result['continuation_hosted_runner_minutes'] == 299
    assert result['prior_scientific_trajectories'] == 0
    with pytest.raises(ValueError):
        m.cumulative_accounting(dict(current, native_updates=6687392))


def test_workflow_activates_only_continuation_and_preserves_cumulative_timeout():
    text = (Path(__file__).resolve().parents[1]/'.github/workflows/q3-distribution-triangle-20261014.yml').read_text()
    assert 'paths: [data/designs/q3_triangle_continuation_20261014.json]' in text
    assert 'timeout-minutes: 29' in text
    assert 'timeout-minutes: 30' not in text
