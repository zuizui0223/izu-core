"""Only a private mirror SELECTION snapshot; never approves scientific biology."""
from __future__ import annotations
import json
from pathlib import Path
import pytest
from scripts.audit_chapter2_clock_private_mirror_selection_20261013 import validate, audit, blob_sha

HERE=Path(__file__).resolve().parents[1]
CONFIG=HERE/'data/design/chapter2_clock_private_mirror_selection_20261013.json'


def source():return json.loads(CONFIG.read_bytes())


def test_private_selection_is_not_scientific_approval():
    r=validate(source(),HERE,verify_sources=False)
    assert r['status']=='HOLD_SCIENTIFIC_PILOT_PRIVATE_MIRROR_SELECTED'
    assert r['pilot_original_zip_files_present']==0
    assert r['approved_source_execution'] is False
    assert r['private_mirror_staging_provider']=='Google Drive'
    assert r['independently_replayed_shards_present']==0
    assert len(r['historical_source_blob_inventory'])==9


def test_mirror_location_may_not_publish_private_identifiers():
    c=source();c['private_mirror_provider_decision']['private_folder_identifiers_and_urls_committed_to_public_repo']=True
    with pytest.raises(ValueError,match='custody/public-identifier'):
        validate(c,HERE,verify_sources=False)


def test_unapproved_public_release_is_rejected():
    c=source();c['prospective_source_publication_proposal']['public_distribution_approved']=True
    with pytest.raises(ValueError,match='source public release'):
        validate(c,HERE,verify_sources=False)


def test_authorization_cannot_be_inferred_from_drive_selection():
    c=source();c['execution_authorization']['scientific_pilot_run_authorized_by_this_record']=True
    with pytest.raises(ValueError,match='launch authorization'):
        validate(c,HERE,verify_sources=False)


def test_biological_trajectories_must_not_be_forged():
    c=source();c['execution_authorization']['registered_pilot_biological_cases_executed']=1536
    with pytest.raises(ValueError,match='nonexistent clock pilot'):
        validate(c,HERE,verify_sources=False)


def fake_source_tree(c,root):
    """Make *explicitly synthetic* fixture bytes for source-identity unit tests."""
    for key,meta in c['current_frozen_source_blobs'].items():
        p=root/meta['path'];p.parent.mkdir(parents=True,exist_ok=True)
        if key=='original_model3_producer':
            raw=b'# synthetic source only\nAPPROVAL_GIT_BLOB = None\n'
        elif key=='invalid_until_sources_exist_external_manifest':
            raw=(json.dumps({'status':'PENDING_RAW_ARCHIVES_NEVER_RUN',
                  'archives':{name:{'sha256':None} for name in c['pilot_scope']['source_shards']}})+'\n').encode()
        elif key=='pre_outcome_factorial_report':
            raw=(json.dumps({'status':'PRE_OUTCOME_FROZEN_ANALYSIS_RULES_NO_BIOLOGICAL_EXECUTION',
                  'execution_policy':{'prospective_pilot_histories_currently_executed':0}})+'\n').encode()
        else:
            raw=('# synthetic non-biological mock of '+key+'\n').encode()
        p.write_bytes(raw)
        meta['git_blob']=blob_sha(raw)


def test_source_blob_mismatch_fails_closed(tmp_path):
    c=source();fake_source_tree(c,tmp_path)
    assert validate(c,tmp_path)['status']=='HOLD_SCIENTIFIC_PILOT_PRIVATE_MIRROR_SELECTED'
    c['current_frozen_source_blobs']['lossless_shard_packer']['git_blob']='0'*40
    with pytest.raises(ValueError,match='source Git blob drift'):
        validate(c,tmp_path)


def test_exact_real_repo_source_fingerprints_when_checkout_has_them():
    c=source();candidate=HERE/c['current_frozen_source_blobs']['pilot_registry']['path']
    if not candidate.exists():
        pytest.skip('real original Model3 source only in connected GitHub checkout')
    assert validate(c,HERE)['status']=='HOLD_SCIENTIFIC_PILOT_PRIVATE_MIRROR_SELECTED'


def test_malformed_source_directory_paths_rejected():
    c=source();c['current_frozen_source_blobs']['lossless_shard_packer']['path']='../../shadow.json'
    with pytest.raises(ValueError,match='unsafe registered source'):
        validate(c,HERE,verify_sources=False)


def test_original_producer_approval_must_remain_unset():
    c=source();c['execution_authorization']['original_200_update_producer_approval_git_blob']='ab'*20
    with pytest.raises(ValueError,match='missing source/approval/DOI evidence'):
        validate(c,HERE,verify_sources=False)


def test_six_source_zip_ids_and_registered_history_grain_are_unchanged():
    c=source();c['pilot_scope']['source_shards']=c['pilot_scope']['source_shards'][:5]
    with pytest.raises(ValueError,match='six-shard biological source'):
        validate(c,HERE,verify_sources=False)
    c=source();c['pilot_scope']['paired_founder_history_clusters']=1536
    with pytest.raises(ValueError,match='grain drift'):
        validate(c,HERE,verify_sources=False)


def test_prerequisite_schemas_are_source_frozen():
    c=source();c['current_frozen_source_blobs']['pilot_registry']['path']='data/design/nonexistent.json'
    with pytest.raises(FileNotFoundError):
        validate(c,HERE)
