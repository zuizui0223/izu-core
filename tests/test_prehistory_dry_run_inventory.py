"""Plan-only CLI must report real manifest counts without starting biology."""
import importlib
import json
import sys

import pytest


@pytest.mark.parametrize('name', [
    'chapter2_kb_prehistory_source_runner',
    'chapter2_k_fixedB48_prehistory',
    'chapter2_timed_self_viability_prehistory',
    'chapter2_orthogonal_prehistory_source_runner',
])
@pytest.mark.parametrize('shard', [0, 63])
def test_dry_run_reports_complete_source_shard_without_biology(name, shard, monkeypatch, capsys):
    module = importlib.import_module('scripts.' + name)

    def forbidden(*args, **kwargs):
        pytest.fail('dry-run must not call biological production')

    monkeypatch.setattr(module, 'run_shard', forbidden)
    monkeypatch.setattr(module, 'simulate_prehistory', forbidden)
    monkeypatch.setattr(sys, 'argv', [name, '--dry-run', '--shard-index', str(shard)])
    module.main()
    result = json.loads(capsys.readouterr().out)
    assert result == {
        'status': 'PLAN_ONLY_NO_BIOLOGY', 'shard': shard,
        'sources': 32, 'scientific_outcomes_generated': False,
    }
