import hashlib
import json

import pytest

from scripts.readaptation_contract_20261019 import (
    CONTRACT_PATH, load_contract, preflight, validate, seed_for, check_file,
    allocation_keys, validate_seed_uniqueness,
)


def test_exact_proposed_allocation_and_no_production_authorization():
    contract = load_contract(CONTRACT_PATH)
    result = preflight(contract)
    assert contract['execution_authorized'] is False
    assert result['donors'] == 32
    assert result['cohort_draws'] == 64
    assert result['future_paths'] == 10240
    assert result['future_updates'] == 819200
    assert result['future_censuses'] == 829440
    assert result['state_bytes_per_census'] == 5664
    assert result['state_bytes_upper'] == 829440 * 5664
    assert result['parentage_bytes_upper'] == 819200 * 48 * 3 * 8
    assert result['assay_population_evaluations_upper'] == 10240 * 2
    assert result['assay_focal_evaluations_upper'] == 10240 * 2 * 48
    assert result['zero_failure_upper_95'] == pytest.approx(1-.05**(1/32))
    assert result['production_ready'] is False


@pytest.mark.parametrize('key,value', [
    ('execution_authorized', True), ('execution_authorized', 0),
    ('founder_indices', [0]*4), ('visitor_indices', list(range(4))),
    ('activity', [.25,1,5]), ('future_repeats', 31),
    ('future_costs', [0,.5]), ('horizon', True), ('extra', 1),
])
def test_modified_design_fails_closed(key, value):
    contract = load_contract(CONTRACT_PATH)
    contract[key] = value
    with pytest.raises(ValueError):
        validate(contract)


def test_source_pin_tampering_and_absent_pin_are_rejected(tmp_path):
    contract = load_contract(CONTRACT_PATH)
    name = next(iter(contract['source_sha256']))
    contract['source_sha256'][name] = '0'*64
    path = tmp_path/'contract.json'
    path.write_text(json.dumps(contract))
    with pytest.raises(ValueError, match='hash'):
        load_contract(path)
    del contract['source_sha256'][name]
    with pytest.raises(ValueError):
        validate(contract)


def test_file_admission_checks_bytes(tmp_path):
    path = tmp_path/'asset'
    path.write_bytes(b'original')
    sha = hashlib.sha256(b'original').hexdigest()
    check_file(path, sha)
    path.write_bytes(b'changed')
    with pytest.raises(ValueError, match='hash'):
        check_file(path, sha)


def test_keys_pair_cohorts_but_separate_future_treatments_and_repeats():
    contract = load_contract(CONTRACT_PATH)
    keys = allocation_keys(contract)
    first = next(keys)
    second = next(keys)
    assert first[:-1] == second[:-1]
    assert first[-1] == 0 and second[-1] == 1
    assert seed_for(contract, 'future', first) != seed_for(contract, 'future', second)
    assert seed_for(contract, 'cohort', first[:4]) == seed_for(contract, 'cohort', second[:4])
    assert seed_for(contract, 'future', first) == seed_for(contract, 'future', first)
    with pytest.raises(ValueError):
        seed_for(contract, 'unknown', first)


def test_collision_audit_rejects_duplicate_seed():
    with pytest.raises(ValueError, match='collision'):
        validate_seed_uniqueness([1,2,1])
    assert validate_seed_uniqueness([1,2,3]) == 3
