import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from q3_distribution_triangle_20261014 import construct, POLICIES


def source(v=0.375, n=48):
    a = np.full((n, 3, 2), v)
    a[:, 0] = 0.25
    a[:, 2] = 0.75
    return dict(alleles=a, allele_origin=np.zeros(a.shape, dtype=int),
                mutation_flags=np.zeros(a.shape, dtype=bool), ids=np.arange(n),
                birth_years=np.zeros(n, dtype=int))


def test_triangle_exact_support_and_variance_preserves_other_fields():
    s = source()
    outputs = {}
    for name, policy in POLICIES.items():
        out = construct(s, name, list(range(policy['heterozygotes'])))
        outputs[name] = out['alleles'][:, 1, :]
        assert np.all(outputs[name].mean(axis=1) == 0.375)
        assert outputs[name].var() == policy['variance']
        assert set(outputs[name].flat) == {0.375-policy['width'], 0.375, 0.375+policy['width']}
        for field in s:
            if field != 'alleles':
                assert np.array_equal(s[field], out[field])
        assert np.array_equal(s['alleles'][:, (0, 2), :], out['alleles'][:, (0, 2), :])
    assert set(outputs['A'].flat) == set(outputs['B'].flat)
    assert outputs['B'].var() == outputs['C'].var()
    assert np.all(s['alleles'][:, 1] == 0.375)


@pytest.mark.parametrize('state,name,indices', [
    (source(n=47), 'B', list(range(12))),
    (source(v=0.9375), 'C', [0, 1, 2]),
    (source(), 'B', [0] * 12),
    (source(), 'C', [0, 1, 48]),
    (source(), 'C', [0, 1, 2.0]),
])
def test_invalid_state_or_subset_rejected(state, name, indices):
    with pytest.raises(ValueError):
        construct(state, name, indices)


def test_nonfixed_input_rejected():
    s = source()
    s['alleles'][0, 1, 0] = 0.5
    with pytest.raises(ValueError):
        construct(s, 'C', [0, 1, 2])
