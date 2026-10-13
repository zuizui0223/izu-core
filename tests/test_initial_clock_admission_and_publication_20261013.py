import importlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def canonical_input(tmp_path, name):
    raw = subprocess.check_output(['git', 'show', 'HEAD:data/results/' + name], cwd=ROOT)
    target = tmp_path / name
    target.write_bytes(raw)
    return target


def cli_inputs(tmp_path):
    return {
        '--compact': canonical_input(tmp_path, 'ecological_order_boundary_20261013.json'),
        '--t0': canonical_input(tmp_path, 'chapter2_initial_clock_t0_raw_20261013.json'),
        '--paired': canonical_input(tmp_path, 'chapter2_initial_clock_paired_events_20261013.json'),
    }


@pytest.mark.parametrize('suffix,function,flags', [
    ('identifiability', 'analyze', ('--input',)),
    ('raw', 'audit', ('--outer', '--compact')),
    ('paired_events', 'audit', ('--compact', '--shards')),
    ('paired_cv', 'run', ('--compact', '--t0', '--paired')),
    ('transfer', 'run', ('--compact', '--t0')),
    ('saturated_reference', 'run', ('--compact', '--paired')),
])
def test_all_clock_readers_preserve_a_concurrent_publication(tmp_path, monkeypatch, suffix, function, flags):
    module = importlib.import_module('scripts.audit_chapter2_initial_clock_' + suffix + '_20261013')
    inputs = cli_inputs(tmp_path)
    output = tmp_path / 'audit.json'
    def competing_publication(*args):
        output.write_text('first validated result', encoding='utf-8')
        return {}
    monkeypatch.setattr(module, function, competing_publication)
    argv = ['reader']
    for flag in flags:
        if flag == '--shards': argv.extend([flag] + ['unused.zip'] * 9)
        else: argv.extend([flag, str(inputs.get(flag, inputs['--compact']))])
    argv.extend(['--out', str(output)])
    monkeypatch.setattr(sys, 'argv', argv)
    with pytest.raises(FileExistsError): module.main()
    assert output.read_text(encoding='utf-8') == 'first validated result'


def test_paired_cv_rejects_changed_seed_pairing_before_fit(tmp_path, monkeypatch):
    from scripts import audit_chapter2_initial_clock_paired_cv_20261013 as module
    inputs = cli_inputs(tmp_path)
    paired = json.loads(inputs['--paired'].read_bytes())
    rows = {r['replicate']: r for r in paired['data'] if r['block'] == 'main'}
    a, b = list(rows[0]['sequence']), list(rows[2]['sequence'])
    assert a[0] != b[0]
    a[0], b[0] = b[0], a[0]
    rows[0]['sequence'], rows[2]['sequence'] = ''.join(a), ''.join(b)
    inputs['--paired'].write_text(json.dumps(paired), encoding='utf-8')
    def must_not_fit(*args): raise AssertionError('Tampered paired labels reached fitting')
    monkeypatch.setattr(module, 'run', must_not_fit)
    argv = ['reader']
    for flag, path in inputs.items(): argv.extend([flag, str(path)])
    argv.extend(['--out', str(tmp_path / 'out.json')])
    monkeypatch.setattr(sys, 'argv', argv)
    with pytest.raises(ValueError, match='paired.*identity'): module.main()


def test_workflow_passes_nine_quoted_shard_paths():
    bash = shutil.which('bash')
    git_bash = Path('C:/Program Files/Git/bin/bash.exe')
    if os.name == 'nt' and git_bash.exists(): bash = str(git_bash)
    if not bash: pytest.skip('Bash runtime unavailable')
    workflow = (ROOT / '.github/workflows/chapter2-initial-clock-readonly-20261013.yml').read_text(encoding='utf-8')
    expression = re.search(r'--shards (.+) \\', workflow).group(1)
    prefix = ''
    if 'shards=()' in workflow:
        prefix = workflow.split('shards=()', 1)[1].split('python -m scripts.audit_chapter2_initial_clock_paired_events', 1)[0]
        prefix = 'shards=()\n' + prefix
    command = prefix + '\nset -- ' + expression + '; printf "%s\\n" "$@"'
    env = dict(os.environ, RUNNER_TEMP='/tmp/a job with spaces')
    result = subprocess.run([bash, '-c', command], env=env, capture_output=True, text=True, check=True)
    assert result.stdout.splitlines() == [env['RUNNER_TEMP'] + f'/original_shards/shard_{i}.zip' for i in range(9)]


def test_event_publication_uses_platform_independent_lf(tmp_path, monkeypatch):
    from scripts import audit_chapter2_initial_clock_paired_events_20261013 as module
    out = tmp_path / 'events.json'
    monkeypatch.setattr(module, 'audit', lambda *args: {'data': [], 'status': 'publication-only-test'})
    monkeypatch.setattr(sys, 'argv', ['reader', '--compact', 'unused.json', '--shards'] + ['unused.zip'] * 9 + ['--out', str(out)])
    module.main()
    assert b'\r\n' not in out.read_bytes()
    assert out.read_bytes().endswith(b'\n')
