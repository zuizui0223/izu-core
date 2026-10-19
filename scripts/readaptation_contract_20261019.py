"""Proposed numerical contract and read-only resource/stream admission.

No biological model imports, transitions, outcome selection or production entrypoint.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT/'docs/protocols/CHAPTER2_READAPTATION_PROPOSED_20261019.json'
ASSET_RECEIPT = 'docs/audits/CHAPTER2_CONFIRM160_ASSET_SHA256_20261019.json'
SOURCE_FILES = (
    'scripts/model3_island/types.py', 'scripts/model3_island/history.py',
    'scripts/model3_island/population.py', 'scripts/model3_island/reproduction.py',
    'scripts/model3_island/randomness.py', 'data/design/model3_island_v2.json',
    ASSET_RECEIPT,
)
DESIGN = dict(
    schema='readaptation_local_proposal_v1', execution_authorized=False,
    namespace='izu-readaptation-local-20261019-v1',
    source_commit='f7792629b35b07e93ac9c98f8feb4d3894da85eb',
    founder_indices=list(range(0,160,40)), visitor_indices=list(range(0,160,40)),
    donor_policies=['fixed','evolving'], donor_census=80, donor_budget=8,
    cohort_draws=2, propagule_cap=12, future_repeats=32, horizon=80,
    activity=[.25,1], future_costs=[.5],
    optima=[[.5]*6,[.7]*6],
    breadth=.2, effectiveness=1, activity_mode='fixed',
    capacity=48, future_budget=8, future_assurance_mode='evolving',
    assurance_timing='delayed', pollen_discount=0, depression=.5,
    survival=0, mutation_rate=0, immigration=0, assay_censuses=[0,80],
    initial_establishment=1, inference='conditional_estimation_only_pointwise',
)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def validate(contract):
    if not isinstance(contract, dict) or set(contract) != set(DESIGN)|{'source_sha256'}:
        raise ValueError('contract field inventory changed')
    for key, expected in DESIGN.items():
        if canonical(contract[key]) != canonical(expected):
            raise ValueError(f'proposed design changed: {key}')
    pins = contract['source_sha256']
    if not isinstance(pins,dict) or set(pins) != set(SOURCE_FILES):
        raise ValueError('source pin inventory changed')
    if any(not isinstance(s,str) or len(s)!=64 or any(c not in '0123456789abcdef' for c in s)
           for s in pins.values()):
        raise ValueError('invalid source hash')
    return contract


def check_file(path, expected_sha):
    sha = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024*1024), b''):
            sha.update(block)
    if sha.hexdigest() != expected_sha:
        raise ValueError(f'hash mismatch: {path}')


def load_contract(path=CONTRACT_PATH):
    contract = validate(json.loads(Path(path).read_text(encoding='utf8')))
    for name, sha in contract['source_sha256'].items():
        check_file(ROOT/name, sha)
    return contract


def verify_assets(contract, directory):
    """Byte admission of all original final assets; no genotype/outcome reads."""
    validate(contract)
    check_file(ROOT/ASSET_RECEIPT, contract['source_sha256'][ASSET_RECEIPT])
    hashes = json.loads((ROOT/ASSET_RECEIPT).read_text(encoding='utf8'))
    expected = {'SUMMARY160.json'} | {
        f'{prefix}-{i}.{suffix}' for i in range(32)
        for prefix,suffix in [('raw-shard','zip'),('seal','json'),('hashes','txt')]}
    if set(hashes) != expected:
        raise ValueError('asset inventory mismatch')
    for name, sha in hashes.items():
        check_file(Path(directory)/name, sha)
    return len(hashes)


def cohort_keys(contract):
    yield from itertools.product(contract['founder_indices'], contract['visitor_indices'],
                                 contract['donor_policies'], range(contract['cohort_draws']))


def allocation_keys(contract):
    # Keys: founder index, visitor index, history policy, cohort, destination, cost, repeat.
    for cohort in cohort_keys(contract):
        for destination,cost,repeat in itertools.product(
                range(1+len(contract['activity'])*len(contract['optima'])),
                contract['future_costs'], range(contract['future_repeats'])):
            yield (*cohort, destination, cost, repeat)


def seed_for(contract, stage, key):
    if stage not in ('cohort','future','technical'):
        raise ValueError('unknown seed stage')
    return int.from_bytes(hashlib.sha256(canonical([contract['namespace'],stage,key])).digest()[:16],'big')


def validate_seed_uniqueness(seeds):
    seen = set()
    for seed in seeds:
        if seed in seen:
            raise ValueError('random master seed collision')
        seen.add(seed)
    return len(seen)


def preflight(contract, *, check_streams=False):
    validate(contract)
    donors = len(contract['founder_indices'])*len(contract['visitor_indices'])*2
    cohorts = donors*contract['cohort_draws']
    destinations = 1+len(contract['activity'])*len(contract['optima'])
    paths = cohorts*destinations*len(contract['future_costs'])*contract['future_repeats']
    updates, censuses = paths*contract['horizon'], paths*(contract['horizon']+1)
    f8,i8,b1 = (np.dtype(t).itemsize for t in ('float64','int64','bool'))
    per_state = contract['capacity']*(6*f8+6*i8+6*b1+2*i8)
    result = dict(status='PROPOSED_NO_BIOLOGICAL_UPDATES', production_ready=False,
                  contract_sha256=hashlib.sha256(canonical(contract)).hexdigest(),
                  donors=donors, cohort_draws=cohorts, future_paths=paths,
                  future_updates=updates, future_censuses=censuses,
                  state_bytes_per_census=per_state,
                  state_bytes_upper=censuses*per_state,
                  parentage_bytes_upper=updates*contract['capacity']*3*i8,
                  assay_population_evaluations_upper=paths*len(contract['assay_censuses']),
                  assay_focal_evaluations_upper=paths*len(contract['assay_censuses'])*contract['capacity'],
                  full_replay_additional_updates=updates,
                  zero_failure_upper_95=1-.05**(1/contract['future_repeats']),
                  compression_measured=False, benchmark_completed=False,
                  byte_bound_excludes=['telemetry','containers','assay_records','replay_storage'])
    if check_streams:
        masters = itertools.chain(
            (seed_for(contract,'cohort',k) for k in cohort_keys(contract)),
            (seed_for(contract,'future',k) for k in allocation_keys(contract)))
        result['unique_master_seeds_checked'] = validate_seed_uniqueness(masters)
    return result
