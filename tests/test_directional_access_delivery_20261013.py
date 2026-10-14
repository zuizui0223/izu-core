import json
import shutil
import pytest
import scripts.build_chapter2_unified_el_submission_bundle as builder


def test_directional_evidence_retains_original_cohort_and_executed_sources():
    members, derivations = builder.directional_access_materials()
    value = json.loads(members['EVIDENCE/DIRECTIONAL_ACCESS_READOUT.json'])
    assert value['cases'] == 2304 and len(value['cells']) == 18
    assert value['excluded_before_fixation'] == value['excluded_with_expressed_variance'] == 703
    assert value['missing_I_terminal_excluded_alive'] == 1159
    assert value['missing_I_excluded_before_fixation'] == 702
    assert value['new_biological_histories'] == 0
    assert len(members) == len(derivations) == 12
    assert builder.sha(members['EVIDENCE/DIRECTIONAL_ACCESS_ARRAYS.npz']) == value['arrays_sha256']


@pytest.mark.parametrize('changed', ['ALL_CENSUS_SUPPORT.npz', 'ALL_CASES.csv', 'INDEPENDENT_REVIEW.json'])
def test_directional_admission_rejects_replaced_verified_bytes(tmp_path, monkeypatch, changed):
    copied = tmp_path / 'directional_access_20261013'
    shutil.copytree(builder.MINIMAL_RESULTS / copied.name, copied)
    target = copied / changed
    target.write_bytes(target.read_bytes() + b' ')
    monkeypatch.setattr(builder, 'MINIMAL_RESULTS', tmp_path)
    with pytest.raises(ValueError, match='directional'):
        builder.directional_access_materials()
