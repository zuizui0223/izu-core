import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_q3_triangle_preflight_20261014 import first_trigger, source_inventory


def test_first_occupied_complete_fixation():
    a = np.full((6, 3, 2), 0.5)
    a[:2, 1, 0] = 0.375
    raw = dict(alleles=a, offsets=np.array([0, 2, 4, 6]))
    assert first_trigger(raw) == 1
    raw['offsets'] = np.array([0, 0, 2, 4, 6])
    assert first_trigger(raw) == 2
    a[2:, 1, 0] = 0.375
    assert first_trigger(raw) is None


def test_bad_offsets_or_nonfinite_alleles_rejected():
    for offsets, v in [(np.array([0, 2, 1]), 0.5), (np.array([0, 1]), float('nan'))]:
        with pytest.raises(ValueError):
            first_trigger(dict(alleles=np.full((1, 3, 2), v), offsets=offsets))


def test_only_registered_module_bytecode_is_ignored():
    source = 'frozen_source/scripts/model3_island/types.py'
    cache = 'frozen_source/scripts/model3_island/__pycache__/types.cpython-311.pyc'
    assert source_inventory({source, cache}, {source}) == [cache]
    for bad in ('frozen_source/extra.py', 'frozen_source/scripts/model3_island/__pycache__/extra.cpython-311.pyc'):
        with pytest.raises(ValueError):
            source_inventory({source, bad}, {source})
