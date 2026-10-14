"""Inert activation validation and durable reservations; no biological imports.

Approval is a human decision recorded by the activation publisher. These checks
bind that record to one reviewed source tree and one GitHub Actions run; they do
not infer approval from a successful test, a goal continuation or a PR comment.
"""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import time
import urllib.request

from q3_triangle_contract_20261014 import NAMESPACE, require

REF = 'refs/heads/design/chapter2-q3-distribution-triangle-20261014'
ACTIVATION = 'data/designs/q3_triangle_execution_20261014.json'
PREFLIGHT_SHA = 'e6d08dc779688192e99b27c8f0344cfef8e633f4be32678a2c9f6d64a680067d'
DESIGN_SHA = '00649680789935168017627a917288939d6786604e32fbcdb065e059a68c9ba3'
ARCHIVE_SHA = '8a2462910025b4a386e789583578cb1380349097393916dac4e50d01c9637b7e'
SOURCE_FILES = (
    'scripts/q3_triangle_contract_20261014.py',
    'scripts/build_q3_triangle_preflight_20261014.py',
    'scripts/build_q3_triangle_activation_20261014.py',
    'scripts/q3_triangle_execution_gate_20261014.py',
    'scripts/q3_triangle_io_20261014.py',
    'scripts/run_q3_triangle_20261014.py',
    'scripts/verify_q3_triangle_paths_20261014.py',
    'scripts/verify_q3_triangle_archives_20261014.py',
    'scripts/publish_q3_triangle_campaign_20261014.py',
    'scripts/q3_distribution_triangle_20261014.py',
    'scripts/q3_event_conditions_20261014.py',
    'scripts/q3_futures_contract_20261014.py',
    'scripts/verify_q3_futures_paths_20261014.py',
    '.github/workflows/q3-distribution-triangle-20261014.yml',
)
LIMITS = dict(new_trajectories=26352, triplets=8784, shards=18,
              replicates_per_state=144, max_native_updates=6687392,
              max_fixture_updates=32, max_hosted_runner_minutes=300,
              max_parallel_shards=1, native_workers=2,
              minimum_free_local_bytes=6*1024**3, max_remote_bytes=64*1024**3,
              archive_bound_per_shard=1616530176)


def digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b''):
            result.update(chunk)
    return result.hexdigest()


def validate_document(doc):
    require(isinstance(doc, dict) and doc.get('approved') is True, 'explicit approval required')
    require(doc.get('namespace') == NAMESPACE, 'new experiment approval scope')
    approval = doc.get('approval', {})
    require(isinstance(approval, dict) and approval.get('scope') == NAMESPACE
            and isinstance(approval.get('reference'), str) and approval['reference'].strip(),
            'explicit approval reference required')
    for name, expected in [('preflight_sha256', PREFLIGHT_SHA),
                           ('design_sha256', DESIGN_SHA), ('archive_sha256', ARCHIVE_SHA)]:
        require(doc.get(name) == expected, 'frozen identity '+name)
    limits = doc.get('limits', {})
    require(limits == LIMITS and all(type(v) is int for v in limits.values()), 'approved limits drift')
    require(isinstance(doc.get('reviewed_commit'), str)
            and re.fullmatch('[0-9a-f]{40}', doc['reviewed_commit']), 'reviewed commit')
    hashes = doc.get('code_sha256', {})
    require(isinstance(hashes, dict) and set(hashes) == set(SOURCE_FILES), 'complete source inventory')
    require(all(isinstance(v, str) and re.fullmatch('[0-9a-f]{64}', v)
                for v in hashes.values()), 'source digest format')
    require((doc.get('python'), doc.get('numpy')) == ('3.11.14', '2.2.6'), 'frozen runtime')


def validate_activation(doc, repo, env, evidence, *, runtime):
    validate_document(doc)
    for key, value in dict(GITHUB_ACTIONS='true', GITHUB_RUN_ATTEMPT='1',
                           GITHUB_REPOSITORY='zuizui0223/izu-core', GITHUB_REF=REF).items():
        require(env.get(key) == value, 'execution environment '+key)
    require(runtime == ('3.11.14', '2.2.6'), 'runtime identity')
    require(evidence['parent'] == doc['reviewed_commit'], 'activation parent')
    require(evidence['head'] == env.get('GITHUB_SHA'), 'activation head')
    require(evidence['added'] == [ACTIVATION] and evidence['changed'] == [ACTIVATION],
            'activation must only add a new manifest')
    runs = evidence['runs']
    require(runs['total_count'] == 1 and len(runs['workflow_runs']) == 1, 'duplicate campaign')
    run = runs['workflow_runs'][0]
    require(str(run['id']) == env.get('GITHUB_RUN_ID') and run['head_sha'] == evidence['head']
            and type(run['run_attempt']) is int and run['run_attempt'] == 1, 'run identity or retry')
    for name, expected in doc['code_sha256'].items():
        require(digest(Path(repo)/name) == expected, 'source drift: '+name)
    return dict(namespace=NAMESPACE, run_id=str(run['id']), head=evidence['head'])


def observe(repo, env):
    """Read authoritative Git and GitHub identities, never launch a workflow."""
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=repo, text=True).strip()
    url = ('https://api.github.com/repos/zuizui0223/izu-core/actions/workflows/'
           'q3-distribution-triangle-20261014.yml/runs?per_page=100')
    request = urllib.request.Request(url, headers={
        'Authorization': 'Bearer '+env['GH_TOKEN'], 'Accept': 'application/vnd.github+json',
        'User-Agent': 'izu-q3-triangle-activation'})
    with urllib.request.urlopen(request, timeout=30) as response:
        runs = json.load(response)
    return dict(parent=git('rev-parse', 'HEAD^'), head=git('rev-parse', 'HEAD'),
                added=git('diff', '--name-only', '--diff-filter=A', 'HEAD^', 'HEAD').splitlines(),
                changed=git('diff', '--name-only', 'HEAD^', 'HEAD').splitlines(), runs=runs)


def authorize(repo):
    repo = Path(repo).resolve()
    raw = (repo/ACTIVATION).read_bytes()
    doc = json.loads(raw)
    validate_document(doc)  # No runtime inspection, Git, network, RNG or native imports before this.
    require(digest(repo/'data/designs/q3_triangle_preflight_20261014.json') == PREFLIGHT_SHA,
            'preflight bytes')
    require(digest(repo/'docs/CHAPTER2_Q3_TRIANGLE_EXECUTION_DESIGN_20261014.md') == DESIGN_SHA,
            'design bytes')
    result = validate_activation(doc, repo, os.environ, observe(repo, os.environ),
                                 runtime=(platform.python_version(), importlib.metadata.version('numpy')))
    return doc, hashlib.sha256(raw).hexdigest(), result


def exclusive_json(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(value, handle, sort_keys=True, indent=2)
        handle.write('\n')
        handle.flush()
        os.fsync(handle.fileno())


def job_deadline(env, *, minutes, tail_seconds, now_epoch=None, now_monotonic=None):
    """Bound remaining work by the first workflow step, including slow setup."""
    now_epoch = time.time() if now_epoch is None else now_epoch
    now_monotonic = time.monotonic() if now_monotonic is None else now_monotonic
    value = env.get('Q3_JOB_STARTED_EPOCH', '')
    require(isinstance(value, str) and value.isdecimal(), 'job start timestamp required')
    started = int(value)
    require(started <= now_epoch, 'job start cannot be in future')
    # Include a cushion for job startup before the timestamp-recording step.
    remaining = started+minutes*60-tail_seconds-30-now_epoch
    require(remaining > 0, 'insufficient remaining job time')
    return now_monotonic+remaining


class ShardBudget:
    """Single coordinator reserves calls before submitting work, never refunds.

    Exclusive START and claim files survive interruption. A shard cannot reopen
    or resume them. Across hosts, the one-run gate and disjoint shard IDs bind
    the cumulative ceiling; final aggregation must verify all 18 ledgers.
    """
    def __init__(self, directory, *, shard, execution_sha, run_id, cases):
        require(type(shard) is int and 0 <= shard < 18, 'shard range')
        require(isinstance(execution_sha, str) and re.fullmatch('[0-9a-f]{64}', execution_sha),
                'execution identity')
        require(isinstance(run_id, str) and run_id.isdecimal(), 'run identity')
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.shard, self.execution_sha, self.run_id = shard, execution_sha, run_id
        self.cases = {c['key']: (c['trigger'], c['remaining_updates']) for c in cases
                      if c['trigger'] is not None}
        exclusive_json(self.directory/'START.json', dict(shard=shard,
                       execution_sha256=execution_sha, run_id=run_id))

    def reserved_updates(self):
        return sum(json.loads(p.read_text(encoding='utf-8'))['native_updates_reserved']
                   for p in self.directory.glob('claim-*.json'))

    def reserve(self, case, replicate):
        require(type(replicate) is int and self.shard*8 <= replicate < (self.shard+1)*8,
                'replicate outside shard')
        require(isinstance(case['key'], str) and re.fullmatch(r'[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*', case['key']),
                'case key')
        t = case['trigger']
        require(self.cases.get(case['key']) == (t, case['remaining_updates']), 'registered case schedule')
        require(type(t) is int and 0 <= t <= 200 and case['remaining_updates'] == 200-t,
                'trigger schedule')
        count = 6*(200-t)
        require(self.reserved_updates()+count <= 371520, 'shard update ceiling')
        require(len(list(self.directory.glob('claim-*.json'))) < 488, 'shard triplet ceiling')
        receipt = dict(key=case['key'], replicate=replicate, shard=self.shard,
                       native_updates_reserved=count, execution_sha256=self.execution_sha,
                       run_id=self.run_id)
        exclusive_json(self.directory/f"claim-{case['key']}-{replicate:03d}.json", receipt)
        return receipt
