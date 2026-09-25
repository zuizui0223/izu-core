from scripts.run_model3_robustness import build_cases, freeze, verify_freeze


def test_prospective_assurance_factorial_has_full_unique_coverage():
    cases=build_cases()
    assert len(cases)==30720
    assert len({c['case_id'] for c in cases})==30720
    assert sum(c['campaign']=='assurance' for c in cases)==24576
    assert sum(c['campaign']=='effort_separation' for c in cases)==6144
    assert {c['depression'] for c in cases}=={0.,.5,.9}
    assert {c['years'] for c in cases}=={400}


def test_robustness_freeze_checks_the_parameterized_sources(tmp_path):
    path=tmp_path/'freeze.json'
    frozen=freeze(path)
    assert 'scripts/model3_robustness.py' in frozen['source_sha256']
    assert verify_freeze(path)['design_sha256']==frozen['design_sha256']
