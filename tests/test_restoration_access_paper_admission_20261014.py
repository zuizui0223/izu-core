import json
import shutil
from pathlib import Path
import pytest
from scripts import build_chapter2_unified_el_submission_bundle as builder


def test_verified_restoration_audit_enters_one_paper_evidence():
    members,provenance=builder.restoration_access_materials()
    review=json.loads(members['EVIDENCE/RESTORATION_ACCESS_FRESH_INDEPENDENT.json'])
    assert review['totals']['triggered']==61 and review['totals']['excluded']==19
    assert review['annual_updates']==7740 and review['annual_max_error']==0
    assert review['no_new_biological_histories'] is True
    assert 'EVIDENCE/RESTORATION_ACCESS_CASES.csv' in members
    assert set(members)==set(provenance)


def test_changed_restoration_case_table_is_not_deliverable(monkeypatch,tmp_path):
    data=tmp_path/'data/results';data.mkdir(parents=True)
    original=builder.ROOT/'data/results'
    for p in original.glob('restoration_access*20261014.*'):
        shutil.copyfile(p,data/p.name)
    (data/'restoration_access_cases_20261014.csv').write_bytes(b'changed case table')
    monkeypatch.setattr(builder,'ROOT',tmp_path)
    with pytest.raises(ValueError):builder.restoration_access_materials()


def test_missing_fresh_raw_review_is_not_deliverable(monkeypatch,tmp_path):
    data=tmp_path/'data/results';data.mkdir(parents=True)
    for p in (builder.ROOT/'data/results').glob('restoration_access*20261014.*'):
        if 'fresh_independent' not in p.name:shutil.copyfile(p,data/p.name)
    monkeypatch.setattr(builder,'ROOT',tmp_path)
    with pytest.raises((ValueError,FileNotFoundError)):
        builder.restoration_access_materials()
