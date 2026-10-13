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


def write_mock_zip(zipfile_path:Path, registry, shard='main_c0', bad=None):
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
            'pilot_registry_git_blob':REGISTRY_GIT_BLOB,
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
                   tmp_path/'no-reviewed-archive-receipt.json',
                   tmp_path/'no-registry.json',
                   tmp_path/'no-original-fixture.json',
                   tmp_path/'no-design.json',output)
    assert not output.exists()


def test_review_never_replaces_prior_source_readout(tmp_path):
    output=tmp_path/'prior-reviewed-artifacts'
    output.mkdir()
    with pytest.raises(FileExistsError,match='do not replace'):
        review_six({},tmp_path/'receipt.json',tmp_path/'reg.json',
                   tmp_path/'fixture.json',tmp_path/'design.json',output)
