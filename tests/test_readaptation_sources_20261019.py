import copy

import pytest

from scripts.readaptation_contract_20261019 import load_contract
from scripts.readaptation_sources_20261019 import donor_specs, iter_donors


def test_source_subset_is_fixed_and_not_outcome_selected():
    specs=donor_specs(load_contract())
    assert len(specs)==32
    assert {s['shard'] for s in specs}=={0,8,16,24}
    assert {s['founder'] for s in specs}=={501001,501041,501081,501121}
    assert {s['visitor'] for s in specs}=={502001,502041,502081,502121}
    assert {s['policy'] for s in specs}=={'fixed','evolving'}
    assert len({tuple(s['key']) for s in specs})==32
    assert all(s['stage']=='B8' and s['end']==80 for s in specs)


def test_changed_selection_rejected_before_reading_sources(tmp_path):
    c=copy.deepcopy(load_contract()); c['founder_indices']=[1]
    with pytest.raises(ValueError):
        list(iter_donors(tmp_path,c))


def test_missing_source_is_not_regenerated(tmp_path):
    with pytest.raises(FileNotFoundError):
        list(iter_donors(tmp_path,load_contract()))
