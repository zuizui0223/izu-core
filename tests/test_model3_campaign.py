from pathlib import Path

import pytest

from scripts.run_model3_evolution import build_cases, freeze, verify_freeze


def test_complete_factorial_and_unique_cases():
    cases = build_cases()
    assert len(cases) == 28672
    assert len({c['case_id'] for c in cases}) == 28672
    assert {c['environment'] for c in cases} == {'mainland','activity_only','community_only','both'}
    assert {c['control'] for c in cases} == {'selected','neutral','fixed'}
    assert sum(c['campaign']=='primary' for c in cases) == 24576
    assert sum(c['campaign']=='larger_population' for c in cases) == 4096
    assert {c['years'] for c in cases} == {400}


def test_freeze_is_exclusive_and_source_checked(tmp_path):
    path = tmp_path/'design.json'
    design = freeze(path)
    assert design['status'] == 'prospective_before_campaign'
    assert design['q1_role'] == 'inspiration_only'
    verify_freeze(path)
    with pytest.raises(FileExistsError):
        freeze(path)
    text = path.read_text(encoding='utf8')
    path.write_text(text.replace('"years": 400','"years": 399'),encoding='utf8')
    with pytest.raises(ValueError,match='design'):
        verify_freeze(path)
