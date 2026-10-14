import json
import shutil
import pytest
from scripts import build_chapter2_unified_el_submission_bundle as builder


def test_all4096_verified_control_and_weak_results_are_deliverable():
    members,provenance=builder.assurance_parent_materials()
    value=json.loads(members['EVIDENCE/ASSURANCE_PARENT_READOUT.json'])
    assert value['cases']==4096 and value['primary_family']==4
    assert [r['decision'] for r in value['primary']]==['unresolved']*4
    assert value['occupied_counts'][1]==[[864,863],[794,770],[852,857]]
    assert set(members)==set(provenance)


def test_counts_only_v1_receipt_cannot_replace_full_domain_admission(monkeypatch,tmp_path):
    relative='data/results/assurance_parent_control_20261014'
    shutil.copytree(builder.ROOT/relative,tmp_path/relative)
    p=tmp_path/relative/'ALL4096_INDEPENDENT_ADMISSION_V2.json'
    r=json.loads(p.read_bytes());r['status']='COUNTS_ONLY_PENDING'
    p.write_text(json.dumps(r),encoding='utf-8')
    monkeypatch.setattr(builder,'ROOT',tmp_path)
    with pytest.raises(ValueError):builder.assurance_parent_materials()


def test_missing_independent_arithmetic_prevents_delivery(monkeypatch,tmp_path):
    relative='data/results/assurance_parent_control_20261014'
    source=builder.ROOT/relative;target=tmp_path/relative;target.mkdir(parents=True)
    for p in source.iterdir():
        if p.name!='INDEPENDENT_ARITHMETIC.json':shutil.copyfile(p,target/p.name)
    monkeypatch.setattr(builder,'ROOT',tmp_path)
    with pytest.raises((ValueError,FileNotFoundError)):
        builder.assurance_parent_materials()


def test_lossless_compressed_reference_preserves_original_proof(monkeypatch,tmp_path):
    import gzip
    import hashlib
    relative='data/results/assurance_parent_control_20261014'
    shutil.copytree(builder.ROOT/relative,tmp_path/relative)
    target=tmp_path/relative
    p=target/'REFERENCE_ADMISSION.json'
    original=p.read_bytes() if p.exists() else gzip.decompress((target/'REFERENCE_ADMISSION.json.gz').read_bytes())
    if p.exists():p.unlink()
    compressed=target/'REFERENCE_ADMISSION.json.gz'
    compressed.write_bytes(gzip.compress(original,mtime=0))
    monkeypatch.setattr(builder,'ROOT',tmp_path)
    members,provenance=builder.assurance_parent_materials()
    key='EVIDENCE/ASSURANCE_PARENT_REFERENCE_ADMISSION.json'
    assert members[key]==original
    assert provenance[key]['original_sha256']==hashlib.sha256(original).hexdigest()
    compressed.write_bytes(gzip.compress(original+b' ',mtime=0))
    with pytest.raises(ValueError):builder.assurance_parent_materials()
