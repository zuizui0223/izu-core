"""Adversarial mock ZIP/manifest checks; NO biological simulation or result."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import stat
import zipfile

import pytest
from scripts.review_chapter2_clock_external_archives_20261013 import (
    SHARDS, REGISTRY_GIT_BLOB, git_blob, inspect_zip,
    manifest_check, review_six,
)


def mock_registry():
    cases = [f'{block}_c{ctx}_A{a}_I{i}_r{rep:03d}'
             for block in ('main', 'confirmation')
             for ctx in (0, 3, 4)
             for a in 'LH' for i in '01' for rep in range(64)]
    assert len(cases) == 1536
    return {'case_identifiers': cases, 'total_input_trajectories': 1536,
            'independent_stochastic_stream_clusters': 128}


def manifest(sha='a'*64):
    return {
      'schema':'chapter2_clock_external_6_shard_archive_receipt_v1',
      'status':'RELEASE_ARCHIVED_AND_MIRROR_RECORDED',
      'original_pilot_registry_blob':REGISTRY_GIT_BLOB,
      'horizon_updates':200,'source_case_count':1536,
      'archives': {k:{'sha256':sha,
          'github_release_url':'https://github.com/zuizui0223/izu-core/releases/download/clock-pilot-review-v1/'+k+'.zip',
          'separate_mirror_receipt':'reviewed-mirror:'+k} for k in SHARDS}}


def test_manifest_requires_all_six_and_raw_sha_not_claimed_from_template(tmp_path, monkeypatch):
    from scripts import review_chapter2_clock_external_archives_20261013 as m
    fake=tmp_path/'registry.json'
    fake.write_text(json.dumps(mock_registry())+'\n')
    monkeypatch.setattr(m,'REGISTRY_GIT_BLOB',git_blob(fake.read_bytes()))
    d=manifest()
    d['original_pilot_registry_blob']=m.REGISTRY_GIT_BLOB
    assert len(manifest_check(d,fake)[0])==6
    d['status']='PENDING_RAW_ARCHIVES_NEVER_RUN'
    with pytest.raises(ValueError,match='not yet complete'):
        manifest_check(d,fake)
    d['status']='RELEASE_ARCHIVED_AND_MIRROR_RECORDED'
    del d['archives']['confirmation_c4']
    with pytest.raises(ValueError,match='six original'):
        manifest_check(d,fake)
    d['archives']['confirmation_c4']=dict(d['archives']['main_c0'])
    d['archives']['main_c0']['sha256']='not-an-actual-hash'
    with pytest.raises(ValueError,match='incomplete external'):
        manifest_check(d,fake)
    d['archives']['main_c0']['sha256']='a'*64
    d['archives']['main_c0']['separate_mirror_receipt']=''
    with pytest.raises(ValueError,match='incomplete external'):
        manifest_check(d,fake)


def write_mock_zip(zipfile_path:Path, registry, shard='main_c0', bad=None, registry_blob=REGISTRY_GIT_BLOB):
    members=[x+'.npz' for x in registry['case_identifiers'] if x.startswith(shard+'_')]
    assert len(members)==256
    if bad=='omit':members.pop()
    elif bad=='unexpected':members.append('../traversal.npz')
    with zipfile.ZipFile(zipfile_path,'w',compression=zipfile.ZIP_STORED) as z:
        for name in members:
            info=zipfile.ZipInfo(name)
            if bad=='symlink' and name==members[0]:
                info.create_system=3
                info.external_attr=(stat.S_IFLNK|0o777)<<16
            z.writestr(info,b'mock-not-biological-NPZ')
        z.writestr('_COMPLETION.json',json.dumps({
            'schema':'chapter2_clock_factorial_model3_native_raw_shard_v1',
            'status':'COMPLETE_REGISTERED_256_NATIVE_PATHS',
            'cases':256, 'updates_per_case':200,
            'pilot_registry_git_blob':registry_blob,
            'case_records':[{ 'mock':i } for i in range(256)]}))
    return zipfile_path


def test_zip_inventory_exactly_256_npzs_and_completion(tmp_path):
    registry=mock_registry()
    archive=write_mock_zip(tmp_path/'synthetic.zip',registry)
    result,_=inspect_zip(archive,registry,'main_c0')
    assert result['cases']==256
    with pytest.raises(ValueError,match='shard is not 256'):
        inspect_zip(archive,{'case_identifiers':[x for x in registry['case_identifiers'] if x!='main_c0_AL_I0_r000']},'main_c0')


@pytest.mark.parametrize('bad',['omit','unexpected','symlink'])
def test_raw_archive_malformed_or_untrusted_member_rejected(tmp_path,bad):
    registry=mock_registry()
    archive=write_mock_zip(tmp_path/('bad_'+bad+'.zip'),registry,bad=bad)
    with pytest.raises(ValueError,match='source members|unsafe source'):
        inspect_zip(archive,registry,'main_c0')


def test_missing_external_archive_manifest_cannot_start_review(tmp_path):
    output=tmp_path/'published'
    with pytest.raises(FileNotFoundError):
        review_six({k:tmp_path/(k+'.zip') for k in SHARDS},
                   {k:tmp_path/(k+'_mirror.zip') for k in SHARDS},
                   tmp_path/'no-reviewed-archive-receipt.json',
                   tmp_path/'no-registry.json',
                   tmp_path/'no-original-fixture.json',
                   tmp_path/'no-design.json',output)
    assert not output.exists()


def test_review_never_replaces_prior_source_readout(tmp_path):
    output=tmp_path/'prior-reviewed-artifacts'
    output.mkdir()
    with pytest.raises(FileExistsError,match='do not replace'):
        review_six({}, {},tmp_path/'receipt.json',tmp_path/'reg.json',
                   tmp_path/'fixture.json',tmp_path/'design.json',output)


def test_six_zip_review_orchestration_with_stubbed_nonbiological_reader(tmp_path, monkeypatch):
    """Exercise delivery mechanics only; NO native biology, NO genuine readout."""
    import sys
    import types
    from scripts import review_chapter2_clock_external_archives_20261013 as m

    registry=tmp_path/'source_registry.json'
    fake=mock_registry()
    registry.write_text(json.dumps(fake)+'\n')
    monkeypatch.setattr(m,'REGISTRY_GIT_BLOB',git_blob(registry.read_bytes()))
    archives={}
    mirrors={}
    hashes={}
    import shutil
    for name in SHARDS:
        path=write_mock_zip(tmp_path/(name+'.zip'),fake,shard=name,registry_blob=m.REGISTRY_GIT_BLOB)
        archives[name]=path
        mirror=tmp_path/(name+'_separate_copy.zip')
        shutil.copyfile(path,mirror)
        mirrors[name]=mirror
        hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    external=manifest()
    external['original_pilot_registry_blob']=m.REGISTRY_GIT_BLOB
    for name in SHARDS:
        external['archives'][name]['sha256']=hashes[name]
    receipt=tmp_path/'independently_attested_RELEASE_NOT_REAL.json'
    receipt.write_text(json.dumps(external)+'\n')

    # The fake verifier is explicitly labelled; no producer or Model3 code is
    # imported or run. It proves only that valid source file *shapes* are passed
    # to the existing independently replaying reader interface exactly once.
    invoked=[]
    def fake_independent_reviewer(folder,*args,**kwargs):
        names=sorted(x.name for x in folder.iterdir())
        assert len(names)==257 and '_COMPLETION.json' in names
        first=next(x for x in names if x.endswith('.npz'))
        assert (folder/first).read_bytes()==b'mock-not-biological-NPZ'
        invoked.append(first)
        return {'original_case_receipts':[{'case_key':n[:-4]} for n in names if n.endswith('.npz')]}
    fake_import=types.ModuleType('scripts.verify_chapter2_clock_pilot_raw_20261013')
    fake_import.verify=fake_independent_reviewer
    monkeypatch.setitem(sys.modules,'scripts.verify_chapter2_clock_pilot_raw_20261013',fake_import)
    def fake_aggregate(readouts,reg):
        assert len(readouts)==6 and reg==registry
        assert len({p.name for p in readouts})==6
        return {'all_starts':1536,'total_native_reproductive_updates':307200}
    monkeypatch.setattr(m,'aggregate',fake_aggregate)
    output=tmp_path/'mock-delivery-results'
    out=review_six(archives,mirrors,receipt,registry,tmp_path/'no-original-fixture',
                   tmp_path/'no-original-design',output)
    assert len(invoked)==6
    assert out['new_biological_histories_generated_by_reviewer']==0
    assert out['status']=='SIX_ORIGINAL_EXTERNAL_RAW_ARCHIVES_INDEPENDENTLY_REPLAYED'
    assert len(out['raw_and_reader_sha256'])==6
    assert len(list(output.iterdir()))==7
    for shard,record in out['raw_and_reader_sha256'].items():
        assert record['source_archive_sha256']==hashes[shard]
        assert record['separately_read_mirror_sha256']==hashes[shard]
        filename=output/(shard+'_independently_verified.json')
        assert record['new_reader_receipt_sha256']==hashlib.sha256(filename.read_bytes()).hexdigest()
    assert (output/'ALL_SIX_ORIGINAL_SOURCE_READBACK.json').exists()


def test_mirror_inventory_required_before_any_native_reader_import(tmp_path):
    existing=tmp_path/'not-created'
    # The source receipt is deliberately absent, and native biology may not
    # run. A missing external manifest cannot be replaced by six local files.
    with pytest.raises(FileNotFoundError):
        review_six({k:tmp_path/(k+'.zip') for k in SHARDS},
                   {k:tmp_path/(k+'_mirror.zip') for k in SHARDS},
                   tmp_path/'absent-published-source.json',tmp_path/'absent-registry.json',
                   tmp_path/'absent-fixture.json',tmp_path/'absent-design.json',existing)
    assert not existing.exists()


def test_same_inode_or_modified_separate_mirror_fails_closed(tmp_path, monkeypatch):
    """Byte-equality of two distinct supplied copies is mandatory; no biology."""
    import sys
    import types
    from scripts import review_chapter2_clock_external_archives_20261013 as m
    reg=mock_registry()
    reg_path=tmp_path/'reg.json';reg_path.write_text(json.dumps(reg)+'\n')
    monkeypatch.setattr(m,'REGISTRY_GIT_BLOB',git_blob(reg_path.read_bytes()))
    archives={}
    mirrors={}
    receipt=manifest()
    receipt['original_pilot_registry_blob']=m.REGISTRY_GIT_BLOB
    import shutil
    for shard in SHARDS:
        source=write_mock_zip(tmp_path/(shard+'.zip'),reg,shard=shard,
                              registry_blob=m.REGISTRY_GIT_BLOB)
        mirror=tmp_path/(shard+'_backup.zip')
        shutil.copyfile(source,mirror)
        archives[shard]=source; mirrors[shard]=mirror
        receipt['archives'][shard]['sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    manifest_file=tmp_path/'source-receipt.json'
    manifest_file.write_text(json.dumps(receipt))
    reader=types.ModuleType('scripts.verify_chapter2_clock_pilot_raw_20261013')
    reader.verify=lambda *a,**k: (_ for _ in ()).throw(AssertionError('Never read native data after mirror failure'))
    monkeypatch.setitem(sys.modules,'scripts.verify_chapter2_clock_pilot_raw_20261013',reader)

    same=dict(mirrors);same['main_c0']=archives['main_c0']
    with pytest.raises(ValueError,match='cannot be the same file'):
        review_six(archives,same,manifest_file,reg_path,tmp_path/'x',tmp_path/'y',tmp_path/'review_same')
    mirrors['main_c0'].write_bytes(mirrors['main_c0'].read_bytes()+b'changed-after-release')
    with pytest.raises(ValueError,match='separate mirror ZIP byte SHA256 differs'):
        review_six(archives,mirrors,manifest_file,reg_path,tmp_path/'x',tmp_path/'y',tmp_path/'review_modified')
