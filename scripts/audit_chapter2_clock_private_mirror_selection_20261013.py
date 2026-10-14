"""Read-only, fail-closed audit of the selected PRIVATE mirror (not pilot approval).

No network, Drive credentials, source reproduction or pilot execution. Confirms
that a separately recorded owner-only mirror candidate does not masquerade as
an independent external release, source archive receipt, or execution permit.
Git blobs bind the existing CI-reviewed technical source surfaces.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

CONFIG = Path('data/design/chapter2_clock_private_mirror_selection_20261013.json')
EXPECTED = 'AUTHOR_SELECTED_PRIVATE_MIRROR_NO_BIOLOGICAL_DATA_OR_EXECUTION_APPROVAL'
SIX = ('main_c0','main_c3','main_c4','confirmation_c0','confirmation_c3','confirmation_c4')


def blob_sha(data:bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def validate(record:dict, root:Path, *, verify_sources:bool=True) -> dict:
    """Only produces HOLD until a separate, independently reviewed execution gate.

    Deliberately does not have a READY_TO_RUN branch: this file is a mirror
    selection snapshot, not a scientific run-approval or provider-auth API.
    """
    scope=record['pilot_scope'];mirror=record['private_mirror_provider_decision']
    pub=record['prospective_source_publication_proposal'];auth=record['execution_authorization']
    if record.get('schema')!='chapter2_clock_private_mirror_provider_selection_v1' or record.get('status')!=EXPECTED:
        raise ValueError('private mirror decision status/schema has drifted')
    if scope['registered_input_count']!=1536 or scope['paired_founder_history_clusters']!=128:
        raise ValueError('registered original pilot grain drift')
    if tuple(scope['source_shards'])!=SIX or scope['cases_per_shard']!=256 or scope['updates_per_case']!=200:
        raise ValueError('original six-shard biological source contract drift')
    if mirror['provider']!='Google Drive' or mirror['private_staging_provider_selected'] is not True:
        raise ValueError('selected private mirror provider drift')
    for k in ('source_provider_is_separate','storage_root_created_and_read_back',
              'root_in_existing_private_chapter2_backup_area',
              'raw_mirror_child_created_and_read_back',
              'independent_receipt_child_created_and_read_back',
              'metadata_returned_shared_false_owner_only'):
        if mirror[k] is not True:
            raise ValueError('private mirror historical metadata attestation incomplete: '+k)
    for k in ('private_folder_identifiers_and_urls_committed_to_public_repo',
              'independently_authenticated_storage_custody',
              'independently_approved_long_term_data_repository'):
        if mirror[k] is not False:
            raise ValueError('unapproved private mirror custody/public-identifier claim: '+k)
    if any(mirror[k]!=0 for k in ('original_zip_count_in_mirror_at_attestation',
                                   'independent_raw_readback_receipt_count_at_attestation')):
        raise ValueError('unexpected pre-existing biological raw source in newly selected mirror')
    for k in ('original_six_shard_release_created','github_release_as_scientific_public_doi_repository',
              'public_distribution_approved','license_or_embargo_approved',
              'separate_reviewer_and_data_custodian_approved'):
        if pub[k] is not False:
            raise ValueError('private mirror decision silently promoted source public release/custody: '+k)
    for k in ('registered_pilot_biological_cases_executed','new_pilot_original_shards_uploaded',
              'real_source_mirror_pairs_independently_retrieved',
              'new_pilot_independent_shard_readbacks_admitted'):
        if auth[k]!=0:raise ValueError('nonexistent clock pilot data counted as complete: '+k)
    for k in ('independent_scientific_reviewer_approval','external_data_custody_and_preservation_signoff',
              'scientific_pilot_run_authorized_by_this_record'):
        if auth[k] is not False:raise ValueError('private mirror destination falsely treated as launch authorization: '+k)
    for k in ('original_200_update_producer_approval_git_blob','source_zip_sha256s',
              'public_persistent_identifier_doi'):
        if auth[k] is not None:raise ValueError('missing source/approval/DOI evidence was fabricated: '+k)
    sources=record['current_frozen_source_blobs']; source_digests={}
    if len(sources)!=9:raise ValueError('incomplete historical technical source inventory')
    for label,entry in sources.items():
        path=Path(entry['path'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('unsafe registered source path: '+label)
        want=entry['git_blob']
        if len(want)!=40 or any(c not in '0123456789abcdef' for c in want):
            raise ValueError('not a 40-hex Git source blob: '+label)
        if verify_sources:
            actual=blob_sha((root/path).read_bytes())
            if actual!=want:raise ValueError('original source Git blob drift: '+label)
        source_digests[label]=want
    if verify_sources:
        producer=(root/sources['original_model3_producer']['path']).read_text(encoding='utf-8')
        if 'APPROVAL_GIT_BLOB = None' not in producer:
            raise ValueError('the 200-update source-run approval unexpectedly unlocked')
        template=json.loads((root/sources['invalid_until_sources_exist_external_manifest']['path']).read_bytes())
        if template['status']!='PENDING_RAW_ARCHIVES_NEVER_RUN':
            raise ValueError('original source release/mirror template is not held')
        if set(template['archives'])!=set(SIX) or any(any(v is not None for v in entry.values())
                for entry in template['archives'].values()):
            raise ValueError('original six source ZIPs or mirror URLs unexpectedly claimed present')
        analysis=json.loads((root/sources['pre_outcome_factorial_report']['path']).read_bytes())
        if analysis['status']!='PRE_OUTCOME_FROZEN_ANALYSIS_RULES_NO_BIOLOGICAL_EXECUTION' or analysis['execution_policy']['prospective_pilot_histories_currently_executed']!=0:
            raise ValueError('pre-outcome analysis lost its original scientific firewall')
    return {
        'schema':'chapter2_clock_selected_private_mirror_readiness_audit_v1',
        'status':'HOLD_SCIENTIFIC_PILOT_PRIVATE_MIRROR_SELECTED',
        'pilot_cases_registered':1536,
        'paired_history_clusters':128,
        'private_mirror_staging_provider':'Google Drive',
        'metadata_only_owner_only_at_previous_attestation':True,
        'private_drive_url_or_folder_id_in_public_result':False,
        'selected_target_writable_archive_bytes_verified':False,
        'pilot_original_zip_files_present':0,
        'independently_replayed_shards_present':0,
        'approved_source_execution':False,
        'author_approved_public_release':False,
        'independent_research_repository_doi_assigned':False,
        'historical_source_blob_inventory':source_digests,
        'unresolved_gates':['independent original-200-update source-run reviewer approval',
                            'original-archive and mirror custody/provenance signoff',
                            'six true source+mirror ZIPs after controlled biology',
                            'independent original genotype/parentage full six-shard replay'],
        'no_biological_simulation_performed':True,
    }


def audit(config:Path=CONFIG, root:Path=Path('.')) -> dict:
    return validate(json.loads(config.read_bytes()),root)


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--record',type=Path,default=CONFIG)
    p.add_argument('--root',type=Path,default=Path('.'))
    p.add_argument('--out',type=Path)
    args=p.parse_args()
    result=audit(args.record,args.root)
    out=json.dumps(result,indent=2,allow_nan=False)+'\n'
    if args.out is None:print(out,end='')
    else:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        with args.out.open('x',encoding='utf8') as dest:dest.write(out)


if __name__=='__main__':main()
