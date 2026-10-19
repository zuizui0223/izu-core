"""Explicit same-implementation replay; never an independent biology verdict.

These functions execute transitions when called. Only synthetic fixtures have
been replayed under the current implementation/technical-testing authorization.
No production loop or scientific-source dispatch is provided.
"""
import numpy as np

from scripts.model3_island.randomness import STREAM_IDS,stream
from scripts.readaptation_contract_20261019 import canonical,load_contract,seed_for
from scripts.readaptation_transfer_20261019 import make_cohort,STATE_FIELDS
from scripts.readaptation_futures_20261019 import run_future


def _seed(saved,contract,key,stage):
    if canonical(contract)!=canonical(load_contract()):
        raise ValueError('replay contract mismatch')
    if len(key)!=(4 if stage=='cohort' else 7):
        raise ValueError('replay key shape')
    f,v,policy,draw=key[:4]
    if (f not in contract['founder_indices'] or v not in contract['visitor_indices']
            or policy not in contract['donor_policies'] or type(draw) is not int
            or not 0<=draw<contract['cohort_draws']):
        raise ValueError('replay cohort allocation')
    if stage=='future':
        destination,cost,repeat=key[4:]
        if (type(destination) is not int or not 0<=destination<5
                or cost not in contract['future_costs'] or type(repeat) is not int
                or not 0<=repeat<contract['future_repeats']):
            raise ValueError('replay future allocation')
    seed=seed_for(contract,stage,key)
    if type(saved.get('stream_key')) is not int or saved['stream_key']!=seed:
        raise ValueError('replay stream mismatch')
    return seed


def _compare(saved,expected):
    if set(saved)!=set(expected):
        raise ValueError('replay record inventory mismatch')
    for name,value in expected.items():
        actual=saved[name]
        if isinstance(value,np.ndarray):
            if (not isinstance(actual,np.ndarray) or actual.shape!=value.shape
                    or actual.dtype!=value.dtype or actual.tobytes()!=value.tobytes()):
                raise ValueError('replay array mismatch: '+name)
        elif canonical(actual)!=canonical(value):
            raise ValueError('replay metadata mismatch: '+name)


def replay_cohort(saved,donor,config,visitors,contract,key):
    seed=_seed(saved,contract,key,'cohort')
    if config.assurance_mode!=key[2] or config.fixed_assurance!=.5:
        raise ValueError('replay donor policy mismatch')
    streams={name:stream(seed,name,0) for name in STREAM_IDS}
    cohort,receipt=make_cohort(donor,config,visitors,streams,key)
    expected={name:getattr(cohort,name) for name in STATE_FIELDS}
    expected.update(receipt=receipt,stream_key=seed)
    _compare(saved,expected)
    return dict(status='PASS_SAME_IMPLEMENTATION_REPLAY',stage='cohort',
                independent_biological_implementation=False)


def replay_future(saved,cohort,config,visitors,contract,key):
    seed=_seed(saved,contract,key,'future')
    expected=run_future(cohort,config,visitors,seed,contract['horizon'])
    _compare(saved,expected)
    return dict(status='PASS_SAME_IMPLEMENTATION_REPLAY',stage='future',updates=contract['horizon'],
                independent_biological_implementation=False)
