import json
import pytest
import scripts.build_chapter2_unified_el_submission_bundle as builder


def test_original_f1_access_requires_independent_raw_mean_and_event_admission():
    members, provenance = builder.first_meiosis_access_materials()
    review = json.loads(members['EVIDENCE/FIRST_MEIOSIS_INDEPENDENT_RAW_REVIEW.json'])
    assert review['cases'] == 2304 and review['paired_clusters'] == 256
    assert review['trait_mean_components'] == 1389312
    assert review['max_trait_mean_error'] == review['max_case_scalar_error'] == 0
    assert review['exact_no_mutation_F1_support'] == 2304
    assert review['new_biological_histories'] == 0
    assert len(members) == len(provenance) == 7


def test_changed_original_f1_case_bytes_are_rejected(monkeypatch, tmp_path):
    import shutil
    relative = 'data/results/first_meiosis_access_20261014'
    target = tmp_path / relative
    shutil.copytree(builder.ROOT / relative, target)
    case = target / 'data/results/chapter2_original_first_meiosis_access_2304_case_20261014.csv'
    case.write_bytes(case.read_bytes() + b' ')
    monkeypatch.setattr(builder, 'ROOT', tmp_path)
    with pytest.raises(ValueError, match='first-meiosis frozen evidence differs'):
        builder.first_meiosis_access_materials()
