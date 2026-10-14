import json
import pytest
from scripts import assurance_parent_admission_20261014 as gate


def test_missing_independent_reference_proof_fails_closed(tmp_path):
    with pytest.raises(ValueError,match='independent reference receipt'):
        gate.reference_proof(tmp_path,{},tmp_path)


def test_receipt_byte_changes_are_rejected(tmp_path):
    path=tmp_path/'receipt.json'
    path.write_text('{}',encoding='utf-8')
    binding={'reference_admission':{'receipt_relative':'receipt.json','receipt_sha256':'0'*64}}
    with pytest.raises(ValueError,match='receipt identity differs'):
        gate.reference_proof(tmp_path,binding,tmp_path)


def test_missing_independent_technical_proof_fails_closed(tmp_path):
    with pytest.raises(ValueError,match='independent native control receipt'):
        gate.technical_proof(tmp_path,{},tmp_path)


def test_self_reported_status_is_not_a_full_birth_proof(tmp_path):
    body=json.dumps({'status':'ALL4096_ORIGINAL_MEAN_NATIVE_REFERENCES_ADMITTED'}).encode()
    (tmp_path/'receipt.json').write_bytes(body)
    binding={'reference_admission':{'receipt_relative':'receipt.json','receipt_sha256':gate.digest(body)}}
    with pytest.raises(ValueError,match='complete original reference birth replay'):
        gate.reference_proof(tmp_path,binding,tmp_path)


def test_native_manifest_cannot_change_under_valid_independent_receipt(tmp_path):
    original=json.dumps({'execution_commit':'frozen','runner_sha256':'original'}).encode()
    (tmp_path/'SHARD.json').write_text(json.dumps({'execution_commit':'frozen','runner_sha256':'changed'}),encoding='utf-8')
    proof=dict(status='NATIVE8_INDEPENDENT_WEIGHT_AND_BIRTH_REPLAY',cases=8,updates=1600,
        new_control_producer_imported=False,new_sampler_imported=False,source_archive_sha256='archive',
        independent_reader_normalized_sha256='reader',source_bindings_sha256='historical',execution_commit='frozen')
    body=json.dumps(proof).encode();(tmp_path/'receipt.json').write_bytes(body)
    binding={'normalized_source_sha256':{gate.READER:'reader'},'technical_admission':{
        'receipt_relative':'receipt.json','receipt_sha256':gate.digest(body),'native_archive_sha256':'archive',
        'historical_source_bindings_sha256':'historical','native_manifest_sha256':gate.digest(original)}}
    with pytest.raises(ValueError,match='native control manifest changed'):
        gate.technical_proof(tmp_path,binding,tmp_path)


def reference_fixture(tmp_path):
    (tmp_path/'verified').mkdir()
    (tmp_path/'ADMISSION.json').write_bytes(b'authenticated admission')
    (tmp_path/'verified/all_start_outcomes.npz').write_bytes(b'authenticated outcomes')
    records=[]
    for block in ('main','confirmation'):
        for replicate in range(512):
            for origin in ('A_access_first','I_access_first'):
                for target in (1.05,1.5):
                    task=dict(block=block,replicate=replicate,origin=origin,target=target,policy='A_mean_equal_native')
                    key=gate.digest(json.dumps(task,sort_keys=True).encode())[:24]
                    records.append(dict(task=task,archive=key+'.npz',sha256='a'*64))
    proof=dict(status='ALL4096_IMMUTABLE_REFERENCE_CASES_AND_NATIVE_BIRTHS_INDEPENDENTLY_ADMITTED',
        cases=4096,updates=819200,new_biological_histories=0,new_control_producer_imported=False,
        new_sampler_imported=False,original_outer_sha256=gate.PRIOR,input_sha256=gate.INPUT,
        independent_reader_normalized_sha256='reader',source_bindings_sha256='historical',
        reference_admission_sha256=gate.digest(b'authenticated admission'),
        outcome_npz_sha256=gate.digest(b'authenticated outcomes'),records=records)
    binding={'normalized_source_sha256':{gate.READER:'reader'},'reference_admission':{
        'receipt_relative':'receipt.json','historical_source_bindings_sha256':'historical'}}
    return proof,binding


def store_fixture(tmp_path,proof,binding):
    raw=json.dumps(proof).encode();(tmp_path/'receipt.json').write_bytes(raw)
    binding['reference_admission']['receipt_sha256']=gate.digest(raw)


def test_full_reference_domain_is_accepted(tmp_path):
    proof,binding=reference_fixture(tmp_path);store_fixture(tmp_path,proof,binding)
    result,index=gate.reference_proof(tmp_path,binding,tmp_path)
    assert result['updates']==819200 and len(index)==4096


def test_duplicate_reference_record_is_not_full_domain(tmp_path):
    proof,binding=reference_fixture(tmp_path)
    proof['records'][-1]=proof['records'][0]
    store_fixture(tmp_path,proof,binding)
    with pytest.raises(ValueError,match='reference domain differs'):
        gate.reference_proof(tmp_path,binding,tmp_path)


def test_authenticated_reference_outcomes_cannot_change(tmp_path):
    proof,binding=reference_fixture(tmp_path);store_fixture(tmp_path,proof,binding)
    (tmp_path/'verified/all_start_outcomes.npz').write_bytes(b'changed')
    with pytest.raises(ValueError,match='reference files changed'):
        gate.reference_proof(tmp_path,binding,tmp_path)
