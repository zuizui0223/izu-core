from pathlib import Path
import hashlib,json,importlib.util
import pytest

ROOT=Path(__file__).resolve().parents[1]
def test_approved_copy_only_activates_actual_receipt():
    original=(ROOT/'scripts/prepare_chapter2_clock_pilot_archive_20261013.py').read_bytes()
    receipt=(ROOT/'data/design/chapter2_clock_pilot_author_execution_approval_20261014.json').read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(receipt)).encode()+b'\0'+receipt).hexdigest()
    approved=(ROOT/'scripts/clock_approved_execution_20261014/producer.py').read_bytes()
    token=b'APPROVAL_GIT_BLOB = None'
    assert original.count(token)==1
    assert approved==original.replace(token,('APPROVAL_GIT_BLOB = '+repr(blob)).encode())
    value=json.loads(receipt)
    assert value['status']=='APPROVED_TO_RUN_PILOT' and value['registered_cases']==1536
    assert value['registry_git_blob']=='f18eae09e3f569ae7edefe970ea17d93c64b1bd5'
    assert hashlib.sha256(original).hexdigest()==value['original_producer_sha256']
    assert value['biological_operator_or_threshold_changes'] is False
    assert value['additional_predictive_confirmation_authorized'] is False

def test_tampered_approval_rejected_before_output_creation(tmp_path):
    path=ROOT/'scripts/clock_approved_execution_20261014/producer.py'
    spec=importlib.util.spec_from_file_location('approved_clock_execution',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    receipt=tmp_path/'wrong.json'
    value=json.loads((ROOT/'data/design/chapter2_clock_pilot_author_execution_approval_20261014.json').read_bytes())
    value['registry_git_blob']='0'*40
    receipt.write_text(json.dumps(value),encoding='utf-8')
    out=tmp_path/'must-not-exist'
    with pytest.raises(ValueError,match='frozen input Git blob mismatch'):
        module.archive(out,ROOT/'data/design/chapter2_clock_factorial_pilot_input_inventory_20261013.json',ROOT/'data/design/chapter2_clock_original_t0_typed_fixture_20261013.json',ROOT/'data/design/chapter2_clock_factorial_pilot_protocol_20261013.json',ROOT/'data/results/chapter2_clock_t0_reproduction_equivalence_20261013.json',shard=0,approval_path=receipt)
    assert not out.exists()
