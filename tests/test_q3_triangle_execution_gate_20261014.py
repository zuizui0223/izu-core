"""Authorization tests use synthetic files and no native modules or random draws."""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))


def gate():
    return importlib.import_module('q3_triangle_execution_gate_20261014')


def fixture(tmp_path):
    g = gate()
    hashes = {}
    for name in g.SOURCE_FILES:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'synthetic source')
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    document = dict(approved=True, namespace=g.NAMESPACE, reviewed_commit='a'*40,
                    approval=dict(reference='conversation:explicit-campaign-approval',
                                  scope=g.NAMESPACE),
                    preflight_sha256=g.PREFLIGHT_SHA, design_sha256=g.DESIGN_SHA,
                    archive_sha256=g.ARCHIVE_SHA, code_sha256=hashes,
                    limits=copy.deepcopy(g.LIMITS), python='3.11.14', numpy='2.2.6')
    env = dict(GITHUB_ACTIONS='true', GITHUB_RUN_ATTEMPT='1',
               GITHUB_REPOSITORY='zuizui0223/izu-core', GITHUB_REF=g.REF,
               GITHUB_RUN_ID='123', GITHUB_SHA='b'*40)
    evidence = dict(parent='a'*40, head='b'*40, added=[g.ACTIVATION],
                    changed=[g.ACTIVATION], runs=dict(total_count=1,
                    workflow_runs=[dict(id=123, head_sha='b'*40, run_attempt=1)]))
    return g, document, env, evidence


def validate(tmp_path, mutate=None):
    g, doc, env, evidence = fixture(tmp_path)
    if mutate:
        mutate(doc, env, evidence)
    return g.validate_activation(doc, tmp_path, env, evidence,
                                 runtime=('3.11.14', '2.2.6'))


def test_valid_synthetic_activation(tmp_path):
    result = validate(tmp_path)
    assert result['namespace'] == gate().NAMESPACE
    assert result['run_id'] == '123'


@pytest.mark.parametrize('field,value', [
    ('approved', False), ('approved', 1),
    ('namespace', 'izu-q3-conditional-restoration-v1-20261014'),
    ('preflight_sha256', '0'*64), ('design_sha256', '0'*64),
    ('archive_sha256', '0'*64), ('reviewed_commit', 'c'*40),
    ('approval', {}), ('code_sha256', {}), ('python', '3.10.0'),
])
def test_rejects_old_unapproved_or_modified_contract(tmp_path, field, value):
    with pytest.raises(ValueError):
        validate(tmp_path, lambda d, e, x: d.update({field: value}))


@pytest.mark.parametrize('field,value', [
    ('GITHUB_ACTIONS', 'false'), ('GITHUB_RUN_ATTEMPT', '2'),
    ('GITHUB_REPOSITORY', 'other/repo'), ('GITHUB_REF', 'refs/heads/main'),
    ('GITHUB_SHA', 'c'*40), ('GITHUB_RUN_ID', '124'),
])
def test_rejects_foreign_environment(tmp_path, field, value):
    with pytest.raises(ValueError):
        validate(tmp_path, lambda d, e, x: e.update({field: value}))


@pytest.mark.parametrize('mutation', [
    lambda d,e,x: x.update(added=[]),
    lambda d,e,x: x['changed'].append('unreviewed.py'),
    lambda d,e,x: x['runs'].update(total_count=2),
    lambda d,e,x: x['runs']['workflow_runs'][0].update(run_attempt=2),
    lambda d,e,x: x['runs']['workflow_runs'][0].update(head_sha='c'*40),
    lambda d,e,x: d['limits'].update(max_native_updates=9999999),
    lambda d,e,x: d['limits'].update(max_parallel_shards=True),
])
def test_rejects_reactivation_and_budget_drift(tmp_path, mutation):
    with pytest.raises(ValueError):
        validate(tmp_path, mutation)


def test_source_change_and_runtime_change_are_rejected(tmp_path):
    g, doc, env, evidence = fixture(tmp_path)
    with pytest.raises(ValueError, match='runtime'):
        g.validate_activation(doc, tmp_path, env, evidence, runtime=('3.11.14', '2.3.0'))
    (tmp_path / g.SOURCE_FILES[0]).write_bytes(b'altered')
    with pytest.raises(ValueError, match='source'):
        g.validate_activation(doc, tmp_path, env, evidence, runtime=('3.11.14', '2.2.6'))


def test_missing_approval_fails_before_runtime_git_or_network(tmp_path, monkeypatch):
    g = gate()
    def forbidden(*a, **kw):
        pytest.fail('external observation before approval')
    monkeypatch.setattr(g, 'observe', forbidden)
    with pytest.raises((FileNotFoundError, ValueError)):
        g.authorize(tmp_path)
    path = tmp_path / g.ACTIVATION
    path.parent.mkdir(parents=True)
    path.write_text('{"approved": false}')
    with pytest.raises(ValueError):
        g.authorize(tmp_path)


def test_reservations_are_persistent_nonrepeatable_and_shard_bound(tmp_path):
    g = gate()
    case = dict(key='causal_main_r0', trigger=12, remaining_updates=188)
    budget = g.ShardBudget(tmp_path, shard=0, execution_sha='d'*64, run_id='123', cases=[case])
    receipt = budget.reserve(case, 0)
    assert receipt['native_updates_reserved'] == 6*188
    assert budget.reserved_updates() == 6*188
    with pytest.raises(FileExistsError):
        budget.reserve(case, 0)
    with pytest.raises(FileExistsError):
        g.ShardBudget(tmp_path, shard=0, execution_sha='d'*64, run_id='123', cases=[case])
    with pytest.raises(ValueError):
        budget.reserve(case, 8)
    with pytest.raises(ValueError):
        budget.reserve(dict(case, key='foreign'), 1)
    with pytest.raises(ValueError):
        budget.reserve(dict(case, trigger=13, remaining_updates=187), 1)
    assert len(list(tmp_path.glob('claim-*.json'))) == 1


@pytest.mark.parametrize('shard', [-1, 18, True])
def test_invalid_shards_fail(tmp_path, shard):
    with pytest.raises(ValueError):
        gate().ShardBudget(tmp_path, shard=shard, execution_sha='d'*64, run_id='123', cases=[])


def test_job_deadline_includes_slow_setup_and_reserves_tail():
    g = gate()
    # 5 minutes have already elapsed. 15-minute job, 3-minute tail and
    # 30-second startup cushion leave 390 seconds for all remaining work.
    deadline = g.job_deadline({'Q3_JOB_STARTED_EPOCH':'1000'}, minutes=15,
                             tail_seconds=180, now_epoch=1300, now_monotonic=20)
    assert deadline == 410
    with pytest.raises(ValueError, match='remaining'):
        g.job_deadline({'Q3_JOB_STARTED_EPOCH':'1000'}, minutes=15,
                       tail_seconds=180, now_epoch=1700, now_monotonic=20)
    with pytest.raises(ValueError):
        g.job_deadline({}, minutes=15, tail_seconds=180, now_epoch=1300, now_monotonic=20)
