import json
import shutil
import pytest
import scripts.build_chapter2_unified_el_submission_bundle as builder


def test_original_admission_keeps_independent_scope_and_unchanged_primary():
    members, derivations=builder.pr490_original_materials()
    result=json.loads(members['EVIDENCE/PR490_ORIGINAL_DIRECT_ADMISSION.json'])
    assert len(members)==len(derivations)==4
    assert len(result['shards'])==8
    assert result['numerical_admission']['declared_byte_agreement'] is True
    assert result['numerical_admission']['pooled_primary']['mean']==0.1083984375
    assert result['original_annual_genomes_authenticated'] is False
    assert result['historical_executed_runtime_authenticated'] is False


def test_rejects_fabricated_archive_recovery_receipt(tmp_path,monkeypatch):
    for name in ['pr490_original_archive_direct_admission_20261014.json',
                 'pr490_original_archive_independent_review_20261014.json']:
        shutil.copyfile(builder.MINIMAL_RESULTS/name,tmp_path/name)
    p=tmp_path/'pr490_original_archive_direct_admission_20261014.json'
    value=json.loads(p.read_bytes());value['original_annual_genomes_authenticated']=True
    p.write_text(json.dumps(value),encoding='utf-8')
    monkeypatch.setattr(builder,'MINIMAL_RESULTS',tmp_path)
    with pytest.raises(ValueError,match='PR490'):builder.pr490_original_materials()
