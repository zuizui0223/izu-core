"""Pinned zero-production HOLD and cumulative accounting; no biological imports."""
from datetime import datetime
from q3_triangle_contract_20261014 import require

HOLD_FILE = 'data/results/q3_triangle_hold_20261014.json'
SPEC_FILE = 'docs/CHAPTER2_Q3_TRIANGLE_CONTINUATION_20261014.md'
PRIOR = dict(run_id=38528315875, head='b51c374ac77e04254cb99e07fa492fc87113b7dc',
    execution_sha256='af6af3ad9b350f4399d5861a222042a5c9ba4bf0bec5fe45adb7a14e2f8167d8',
    artifact_sha256='f2e0ea8a6682d2ce8e4ece88adec8d7530e089c5c8a555d4d9f7bb4c94e6e92e',
    artifact_bytes=10346505, native_updates=4, scientific_trajectories=0,
    reserved_hosted_runner_minutes=1, continuation_hosted_runner_minutes=299,
    hold_receipt_sha256='3d2dfdce61f5572fa81fc2d2172f199e9a0c87bca1bf1015e2154866b15b72ab',
    specification_sha256='428fcc24f8361218db84bd402d2298f112421d6c71092aad82640565d6996d73',
    release_url='https://github.com/zuizui0223/izu-core/releases/tag/q3-distribution-triangle-hold-20261014')


def validate_prior(run, jobs):
    require(run.get('id') == PRIOR['run_id'] and run.get('head_sha') == PRIOR['head'] and
            type(run.get('run_attempt')) is int and run['run_attempt'] == 1 and
            run.get('status') == 'completed' and run.get('conclusion') == 'failure', 'pinned prior failure')
    expected = {f'triangle-shard-{s}' for s in range(18)} | {'triangle-verify-and-publish'}
    require(len(jobs) == 19 and {j['name'] for j in jobs} == expected and
            all(j['status'] == 'completed' for j in jobs), 'prior complete job inventory')
    for job in jobs:
        if job['name'] == 'triangle-shard-0':
            require(job['conclusion'] == 'failure', 'prior shard0 failure')
            elapsed = (datetime.fromisoformat(job['completed_at'].replace('Z', '+00:00')) -
                       datetime.fromisoformat(job['started_at'].replace('Z', '+00:00'))).total_seconds()
            require(0 < elapsed <= 60, 'prior one-minute reservation')
            steps = {s['name']:s for s in job['steps']}
            require(steps.get('Reserved production and complete independent replay', {}).get('conclusion') == 'failure'
                    and steps.get('Preserve partial failure without restarting biology', {}).get('conclusion') == 'success',
                    'prior preserved failure')
        else:
            conclusion = 'skipped' if job['name'] == 'triangle-verify-and-publish' else 'cancelled'
            require(job['conclusion'] == conclusion and not job['steps'], 'prior unstarted remaining jobs')


def cumulative_accounting(current):
    require(type(current['fixture_updates']) is int and current['fixture_updates'] >= 0 and
            current['native_updates'] == 6687360+current['fixture_updates'] and
            current['trajectories'] == 26352, 'continuation native accounting')
    fixtures = current['fixture_updates']+4
    updates = current['native_updates']+4
    require(fixtures <= 32 and updates <= 6687392, 'cumulative native ceiling')
    return dict(native_updates=updates, fixture_updates=fixtures,
                prior_scientific_trajectories=0, scientific_trajectories=26352,
                prior_native_updates=4, continuation_native_updates=current['native_updates'],
                prior_hosted_runner_minutes_reserved=1, continuation_hosted_runner_minutes=299,
                reserved_hosted_runner_minutes=300)
