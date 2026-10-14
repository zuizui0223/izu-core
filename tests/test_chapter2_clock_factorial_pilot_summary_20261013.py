"""Pre-outcome descriptive policy tests. ALL receipt data are SYNTHETIC MOCKS.

The real original genome/parentage source replay is tested in the parent PR;
these tests check only the downstream, frozen factorial effect description.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import types

import pytest

# Standalone scratchpad lacks the full repository. Under a genuine repository
# checkout this branch uses the real six-shard aggregator. The tests *always*
# monkeypatch a deliberately synthetic aggregator to exercise only reporting.
if 'scripts.aggregate_chapter2_clock_pilot_verified_shards_20261013' not in sys.modules:
    try:
        import scripts.aggregate_chapter2_clock_pilot_verified_shards_20261013
    except ImportError:
        fake = types.ModuleType('scripts.aggregate_chapter2_clock_pilot_verified_shards_20261013')
        fake.aggregate = lambda *a,**k: (_ for _ in ()).throw(AssertionError('mock required'))
        def synthetic_event_rule(e):
            a,i=e['A'],e['I']
            if a is None: lab='neither' if i is None else 'investment_only'
            elif i is None: lab='assurance_only'
            elif abs(a-i)<=5: lab='near_simultaneous'
            else: lab='assurance_first' if a<i else 'investment_first'
            if lab!=e['category']: raise ValueError('contradicts original A/I event onsets')
            if any(type(x) is not int or not 0<=x<=181 for x in (a,i) if x is not None):
                raise ValueError('bad event onset')
            return lab
        fake.verify_six_class_event = synthetic_event_rule
        sys.modules[fake.__name__] = fake

from scripts import summarize_chapter2_clock_factorial_pilot_20261013 as summary

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT/'data/design/chapter2_clock_factorial_pilot_analysis_contract_20261013.json'
LABELS = summary.LABELS


def dyadic_case(block, ctx, a, i, rep):
    return f'{block}_c{ctx}_A{a}_I{i}_r{rep:03d}'


def event_for(awidth, ihidden):
    if awidth=='L' and ihidden=='0': return {'A':None,'I':None,'category':'neither'}
    if awidth=='L' and ihidden=='1': return {'A':None,'I':20,'category':'investment_only'}
    if awidth=='H' and ihidden=='0': return {'A':20,'I':None,'category':'assurance_only'}
    return {'A':20,'I':45,'category':'assurance_first'}


def mock_artifacts(tmp_path, monkeypatch):
    paths=[];all_cases=[];names=[]
    for block in ('main','confirmation'):
        for context in (0,3,4):
            case_rows=[]
            for a in 'LH':
                for i in '01':
                    for rep in range(64):
                        case=dyadic_case(block,context,a,i,rep)
                        row={'case_key':case,'updates':200,'case_sha256':'a'*64,
                             'event_0p05':event_for(a,i),
                             'genotype_record_source_years':48*200,'parent_pairs':48*200}
                        case_rows.append(row);all_cases.append(case)
            path=tmp_path/f'{block}_c{context}_independently_verified.json'
            obj={'schema':'chapter2_clock_factorial_producer_independent_raw_reader_v1',
                 'status':'ALL_256_PILOT_SHARD_RAW_GENOMES_REPLAYED',
                 'pilot_registry_git_blob':'f18eae09e3f569ae7edefe970ea17d93c64b1bd5',
                 'cases':256,'updates':51200,'new_pilot_biological_histories':256,
                 'original_model3_biological_source_replayed':True,
                 'producer_loaded_as_python_module':False,
                 'original_case_receipts':case_rows}
            path.write_text(json.dumps(obj)+'\n')
            paths.append(path); names.append(f'{block}_c{context}')
    registry=tmp_path/'MOCK_NOT_SOURCE_REGISTRY.json'
    registry.write_text(json.dumps({'case_identifiers':all_cases,
                                  'independent_stochastic_stream_clusters':128,
                                  'total_input_trajectories':1536})+'\n')
    cohort={'source_registry_blob':'f18eae09e3f569ae7edefe970ea17d93c64b1bd5',
            'all_starts':1536,'paired_history_clusters':128,
            'total_native_reproductive_updates':307200,
            'six_class_labels': {k:384 if k in ('neither','investment_only','assurance_only','assurance_first') else 0
                                 for k in LABELS},
            'original_shard_readback_files_sha256': {
                k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in zip(names,paths)},
            'source_result_is_mock':True}
    external=tmp_path/'MOCK_NOT_REAL_EXTERNAL_READBACK.json'
    provenance={name:{'source_archive_sha256':hashlib.sha256(name.encode()).hexdigest(),
                      'separately_read_mirror_sha256':hashlib.sha256(name.encode()).hexdigest(),
                      'new_reader_receipt_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
                for name,path in zip(names,paths)}
    external_record={'schema':'chapter2_clock_all_six_re_downloaded_native_review_v1',
                     'status':'SIX_ORIGINAL_EXTERNAL_RAW_ARCHIVES_INDEPENDENTLY_REPLAYED',
                     'source_manifest_sha256':'a'*64,
                     'new_biological_histories_generated_by_reviewer':0,
                     'raw_and_reader_sha256':provenance,'whole_cohort':cohort,
                     'mock_for_tests_only':True}
    external.write_text(json.dumps(external_record)+'\n')
    def fake_aggregate(readouts,reg):
        assert reg==registry and set(readouts)==set(paths)
        return cohort
    monkeypatch.setattr(summary,'aggregate',fake_aggregate)
    return paths,registry,external,cohort


def test_frozen_source_scope_and_no_biological_authorization():
    c=summary.contract_file(CONTRACT)
    assert c['execution_policy']['prospective_pilot_histories_currently_executed']==0
    assert c['basis']['source_gate']=='SIX_ORIGINAL_EXTERNAL_RAW_ARCHIVES_INDEPENDENTLY_REPLAYED'
    assert c['basis']['approved_case_keys']==1536 and c['basis']['registered_stochastic_clusters']==128
    assert c['execution_policy']['this_contract_does_not_authorize_pilot_execution'] is True


def test_dyadic_four_arm_factorial_and_stochastic_cluster_contrasts():
    arms={('L','0'):summary.flags(event_for('L','0')),
          ('L','1'):summary.flags(event_for('L','1')),
          ('H','0'):summary.flags(event_for('H','0')),
          ('H','1'):summary.flags(event_for('H','1'))}
    got=summary.contrasts(arms)
    assert got['Awidth_to_A_incidence']==1
    assert got['Ihidden_to_I_incidence']==1
    assert got['Awidth_to_D']==.5
    assert got['Ihidden_to_D']==.5
    assert got['Awidth_x_Ihidden_to_D']==1
    assert summary.mean_sd([2.,2.,2.])['sample_sd_across_history_clusters']==0
    with pytest.raises(ValueError,match='missing'):
        summary.contrasts({('L','0'):arms['L','0']})


def test_complete_synthetic_six_class_and_24_cell_source_bound_descriptive_report(tmp_path,monkeypatch):
    paths,reg,external,_=mock_artifacts(tmp_path,monkeypatch)
    result=summary.describe_audited_pilot(paths,reg,external,CONTRACT)
    assert result['status']=='EXPLORATORY_SOURCE_BOUND_PILOT_DESCRIPTION_NOT_Q1_Q2_CONFIRMATION'
    assert result['all_starts']==1536 and result['n_paired_stochastic_history_clusters']==128
    assert sum(result['overall_six_class_counts'].values())==1536
    assert result['overall_six_class_counts']['assurance_first']==384
    assert len(result['all_24_original_factorial_cell_rows'])==24
    assert all(row['n_starts']==64 for row in result['all_24_original_factorial_cell_rows'])
    assert len(result['paired_effect_rows_by_founder_ecology'])==30
    pooled=result['average_effect_across_original_three_contexts_128_history_clusters']
    assert pooled['Awidth_to_A_incidence']['mean']==1
    assert pooled['Ihidden_to_I_incidence']['mean']==1
    assert pooled['Awidth_x_Ihidden_to_D']['mean']==1
    assert all(x['n_paired_history_clusters']==128 for x in pooled.values())
    assert all(x['sample_sd_across_history_clusters']==0 for x in pooled.values())
    assert 'power estimate or score-difference SD' not in ' '.join(result['analysis_claim_limits'])


def test_missing_external_source_receipt_is_hold_not_pilot_result(tmp_path,monkeypatch):
    paths,reg,external,_=mock_artifacts(tmp_path,monkeypatch)
    data=json.loads(external.read_text());data['status']='PENDING_RAW_ARCHIVES_NEVER_RUN'
    external.write_text(json.dumps(data)+'\n')
    with pytest.raises(ValueError,match='external raw source reviewer receipt absent'):
        summary.describe_audited_pilot(paths,reg,external,CONTRACT)


def test_forged_external_readout_hash_or_mirror_hash_rejected(tmp_path,monkeypatch):
    paths,reg,external,_=mock_artifacts(tmp_path,monkeypatch)
    d=json.loads(external.read_text())
    d['raw_and_reader_sha256']['main_c0']['new_reader_receipt_sha256']='f'*64
    external.write_text(json.dumps(d)+'\n')
    with pytest.raises(ValueError,match='bytes disagree'):
        summary.describe_audited_pilot(paths,reg,external,CONTRACT)
    d['raw_and_reader_sha256']['main_c0']['new_reader_receipt_sha256']=hashlib.sha256(paths[0].read_bytes()).hexdigest()
    d['raw_and_reader_sha256']['main_c0']['separately_read_mirror_sha256']='e'*64
    external.write_text(json.dumps(d)+'\n')
    with pytest.raises(ValueError,match='bytes disagree'):
        summary.describe_audited_pilot(paths,reg,external,CONTRACT)


def test_missing_observed_path_or_duplicate_own_case_is_rejected(tmp_path,monkeypatch):
    paths,reg,external,cohort=mock_artifacts(tmp_path,monkeypatch)
    d=json.loads(paths[0].read_text());d['original_case_receipts'][0]['case_key']=d['original_case_receipts'][1]['case_key']
    paths[0].write_text(json.dumps(d)+'\n')
    manifest=json.loads(external.read_text())
    corrected_sha=hashlib.sha256(paths[0].read_bytes()).hexdigest()
    manifest['raw_and_reader_sha256']['main_c0']['new_reader_receipt_sha256']=corrected_sha
    # Fully synchronize the deliberately MOCKED earlier 6-shard aggregator so
    # that the descriptive parser, not just the upstream SHA guard, is tested.
    manifest['whole_cohort']['original_shard_readback_files_sha256']['main_c0']=corrected_sha
    cohort['original_shard_readback_files_sha256']['main_c0']=corrected_sha
    external.write_text(json.dumps(manifest)+'\n')
    with pytest.raises(ValueError,match='duplicate paired history'):
        summary.describe_audited_pilot(paths,reg,external,CONTRACT)


def test_original_six_class_label_must_match_original_A_I_onsets():
    with pytest.raises(ValueError):
        summary.flags({'A':10,'I':80,'category':'investment_first'})
    assert summary.flags({'A':None,'I':None,'category':'neither'})=={'A_incidence':0,'I_incidence':0,'D':0}
    assert summary.flags({'A':15,'I':18,'category':'near_simultaneous'})['D']==0


def test_analysis_contract_drift_fails_before_outcome_read(tmp_path):
    cloned=tmp_path/'edited_contract.json';cloned.write_bytes(CONTRACT.read_bytes()+b' ')
    with pytest.raises(ValueError,match='Git blob changed'):
        summary.contract_file(cloned)
