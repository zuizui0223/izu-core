"""No biological model run: exact 256-case synthetic-byte packager tests ONLY."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
import zipfile

import pytest

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts import package_chapter2_clock_pilot_shard_20261013 as packer


def setup_mock(tmp_path,monkeypatch,shard='main_c0'):
    # Deliberate fake ZIP member bodies; definitely NOT Model3 NPZs.
    case_keys=[f'{b}_c{c}_A{a}_I{i}_r{r:03d}'
        for b in ('main','confirmation') for c in ('0','3','4')
        for a in ('L','H') for i in ('0','1') for r in range(64)]
    assert len(case_keys)==1536
    registered={
      'status':'PRE_BIOLOGICAL_EXPLICIT_PILOT_INPUTS_RECORDED_NO_EXECUTION',
      'total_input_trajectories':1536,
      'independent_stochastic_stream_clusters':128,
      'updates_per_trajectory':200,
      'original_model_source_blobs':packer.MODEL_BLOBS,
      'case_identifiers':case_keys
    }
    file=tmp_path/'MOCK_registry.json'
    file.write_text(json.dumps(registered)+'\n')
    monkeypatch.setattr(packer,'REGISTRY_BLOB',packer.git_blob(file.read_bytes()))
    src=tmp_path/'MOCK_SOURCE_NOT_BIOLOGY'
    src.mkdir(exist_ok=True)
    rec=[]
    for k in case_keys:
        if not k.startswith(shard+'_'):continue
        data=(f'DELIBERATELY_NOT_A_REAL_MODEL3_NPZ:{k}\n').encode()
        (src/(k+'.npz')).write_bytes(data)
        rec.append({'case_key':k,'sha256':hashlib.sha256(data).hexdigest(),
                    'size':len(data),'status':'COMPLETE_ORIGINAL_200_UPDATE',
                    'event_0p05':{'A':None,'I':None,'category':'neither'}})
    assert len(rec)==256
    completion={
      'schema':'chapter2_clock_factorial_model3_native_raw_shard_v1',
      'status':'COMPLETE_REGISTERED_256_NATIVE_PATHS',
      'pilot_registry_git_blob':packer.REGISTRY_BLOB,
      'protocol_git_blob':packer.DESIGN_BLOB,
      'fixture_git_blob':packer.T0_BLOB,
      'model_biological_git_blobs':packer.MODEL_BLOBS,
      'execution_mode':'pilot','source_runtime_numpy':'2.2.6',
      'shard':packer.SHARDS.index(shard),
      'cases':256,'new_scientific_pilot_histories':256,'updates_per_case':200,
      'source_code_sha256':'c'*64,'case_records':rec,
    }
    (src/'_COMPLETION.json').write_text(json.dumps(completion)+'\n')
    return src,file,completion


def put_completion(src,c):
    (src/'_COMPLETION.json').write_text(json.dumps(c)+'\n')


def test_256_case_mock_bytes_are_losslessly_packed_crc_checked_and_deterministic(tmp_path,monkeypatch):
    src,reg,c=setup_mock(tmp_path,monkeypatch)
    target=tmp_path/'original-shard.zip';receipt=tmp_path/'receipt.json'
    o=packer.package(src,reg,'main_c0',target,receipt)
    assert o['status']=='SOURCE_ZIP_BYTES_VERIFIED_NOT_ARCHIVED_OR_INDEPENDENTLY_REPLAYED'
    assert o['zip_members']==257 and o['cases']==256
    assert o['updates_if_original_producer_admitted']==51200
    assert not o['external_re_download_verified'] and not o['native_original_source_independent_replay']
    assert o['external_github_release_url'] is None and o['external_mirror_receipt'] is None
    assert o['pilot_source_generated_by_this_packager'] is False
    assert o['ready_for_scientific_conclusion'] is False
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert len(z.namelist())==257
        assert set(z.namelist())==set(o['original_member_sha256'])
        for name in z.namelist():
            assert z.getinfo(name).compress_type==zipfile.ZIP_STORED
            assert z.read(name)==(src/name).read_bytes()
    assert json.loads(receipt.read_text())==o
    twin=tmp_path/'second-independent-pack.zip'
    twinreceipt=tmp_path/'another.json'
    r=packer.package(src,reg,'main_c0',twin,twinreceipt)
    assert r['zip_sha256']==o['zip_sha256'] and twin.read_bytes()==target.read_bytes()
    with pytest.raises(FileExistsError):
        packer.package(src,reg,'main_c0',target,tmp_path/'new.json')
    with pytest.raises(FileExistsError):
        packer.package(src,reg,'main_c0',tmp_path/'new.zip',receipt)
    assert not (tmp_path/'new.zip').exists()


def test_omitted_extra_and_corrupted_raw_member_fails_before_packaging(tmp_path,monkeypatch):
    src,reg,c=setup_mock(tmp_path,monkeypatch)
    k=c['case_records'][0]['case_key']+'.npz';p=src/k
    old=p.read_bytes()
    p.write_bytes(old+b'tamper')
    with pytest.raises(ValueError,match='differ from producer'):
        packer.inventory(src,reg,'main_c0')
    assert not (tmp_path/'unreleased.zip').exists()
    p.write_bytes(old)
    p.unlink()
    with pytest.raises(ValueError,match='extra/missing'):
        packer.inventory(src,reg,'main_c0')
    p.write_bytes(old)
    (src/'FORGED.json').write_text('{}')
    with pytest.raises(ValueError,match='extra/missing'):
        packer.inventory(src,reg,'main_c0')


def test_reject_source_parentage_meta_wrong_runtime_shard_and_technical_mode(tmp_path,monkeypatch):
    src,reg,c=setup_mock(tmp_path,monkeypatch)
    c['status']='TECHNICAL_ONLY_48_NATIVE_PATHS'
    put_completion(src,c)
    with pytest.raises(ValueError,match='completion'):
        packer.inventory(src,reg,'main_c0')
    c['status']='COMPLETE_REGISTERED_256_NATIVE_PATHS'
    c['source_runtime_numpy']='2.5.4'
    put_completion(src,c)
    with pytest.raises(ValueError,match='completion'):
        packer.inventory(src,reg,'main_c0')
    c['source_runtime_numpy']='2.2.6';c['shard']=5
    put_completion(src,c)
    with pytest.raises(ValueError,match='completion'):
        packer.inventory(src,reg,'main_c0')
    c['shard']=0
    c['model_biological_git_blobs']=dict(c['model_biological_git_blobs'],**{'population.py':'0'*40})
    put_completion(src,c)
    with pytest.raises(ValueError,match='completion'):
        packer.inventory(src,reg,'main_c0')


def test_missing_duplicate_and_forged_onset_case_receipts_refused(tmp_path,monkeypatch):
    src,reg,c=setup_mock(tmp_path,monkeypatch)
    c['case_records'][0]['case_key']=c['case_records'][1]['case_key']
    put_completion(src,c)
    with pytest.raises(ValueError,match='duplicate'):
        packer.inventory(src,reg,'main_c0')
    src,reg,c=setup_mock(tmp_path,monkeypatch)
    c['case_records'][0]['event_0p05']={'A':181,'I':0,'category':'assurance_first'}
    put_completion(src,c)
    with pytest.raises(ValueError,match='contradicts'):
        packer.inventory(src,reg,'main_c0')
    src,reg,c=setup_mock(tmp_path,monkeypatch)
    c['case_records'][0]['event_0p05']={'A':True,'I':None,'category':'assurance_only'}
    put_completion(src,c)
    with pytest.raises(ValueError,match='out of range'):
        packer.inventory(src,reg,'main_c0')


def test_registration_or_original_source_drift_refused(tmp_path,monkeypatch):
    src,reg,c=setup_mock(tmp_path,monkeypatch)
    original_registry=reg.read_bytes()
    reg.write_bytes(original_registry+b' ')
    with pytest.raises(ValueError,match='registry Git blob changed'):
        packer.inventory(src,reg,'main_c0')
    reg.write_bytes(original_registry[:-1])
    with pytest.raises(ValueError,match='registry Git blob changed'):
        packer.inventory(src,reg,'main_c0')
    with pytest.raises(ValueError,match='unregistered founder'):
        packer.registered_cases(reg,'invalid_c0')


def test_symlink_raw_case_and_symlink_original_shard_directory_refused(tmp_path,monkeypatch):
    src,reg,c=setup_mock(tmp_path,monkeypatch)
    filename=c['case_records'][0]['case_key']+'.npz'
    original=src/filename
    dest=tmp_path/'actually-same-source.bin';dest.write_bytes(original.read_bytes())
    original.unlink()
    original.symlink_to(dest)
    with pytest.raises(ValueError,match='ordinary file'):
        packer.inventory(src,reg,'main_c0')
    link=tmp_path/'symlink-folder';link.symlink_to(src,target_is_directory=True)
    with pytest.raises(ValueError,match='symlink'):
        packer.inventory(link,reg,'main_c0')


def test_existing_output_cannot_be_overwritten_even_with_valid_source(tmp_path,monkeypatch):
    src,reg,c=setup_mock(tmp_path,monkeypatch)
    out=tmp_path/'already-completed';out.write_text('IMMUTABLE')
    with pytest.raises(FileExistsError):
        packer.package(src,reg,'main_c0',out,tmp_path/'unused.json')
    assert out.read_text()=='IMMUTABLE'


def test_real_reviewer_can_open_only_canonical_257_member_archive(tmp_path,monkeypatch):
    # Original reviewer is a separate upstream module available in a true
    # branch checkout; scratchpad's standalone mock does not import it.
    try:
        from scripts import review_chapter2_clock_external_archives_20261013 as reviewer
    except ImportError:
        pytest.skip('standalone scratchpad lacks upstream external native review module')
    src,reg,_=setup_mock(tmp_path,monkeypatch)
    # The upstream reader pins the ORIGINAL source registry. This explicitly
    # MOCK registry must be injected in BOTH guards; otherwise a legitimate
    # test fixture would be rejected before checking the ZIP format. This
    # monkeypatch exists only in a synthetic-test function, never production.
    monkeypatch.setattr(reviewer,'REGISTRY_GIT_BLOB',packer.REGISTRY_BLOB)
    out=tmp_path/'synthetic.zip'
    packer.package(src,reg,'main_c0',out,tmp_path/'receipt.json')
    admitted,_=reviewer.inspect_zip(out,{'case_identifiers':json.loads(reg.read_text())['case_identifiers']},'main_c0')
    assert admitted['cases']==256
