import shutil
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / 'data/results/update_factorial_20260925'


def test_complete_artifact_recomputes_from_cells():
    from scripts.validate_chapter2_update_factorial import validate
    assert validate(SOURCE)['verified_rule_rows'] == 270


def test_missing_batch_rejected(tmp_path):
    from scripts.validate_chapter2_update_factorial import validate
    shutil.copytree(SOURCE, tmp_path/'run')
    next((tmp_path/'run').glob('*.npz')).unlink()
    with pytest.raises(ValueError, match='batch'):
        validate(tmp_path/'run')


def test_changed_result_rejected(tmp_path):
    from scripts.validate_chapter2_update_factorial import validate
    shutil.copytree(SOURCE, tmp_path/'run')
    result = tmp_path/'run/results.json'
    result.write_text(result.read_text() + ' ')
    with pytest.raises(ValueError, match='hash'):
        validate(tmp_path/'run')
