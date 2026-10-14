import importlib.util
from pathlib import Path

import numpy as np
import pytest

spec = importlib.util.spec_from_file_location(
    'restoration_access', Path(__file__).resolve().parents[1] / 'scripts/audit_restoration_access_20261014.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def test_heterozygous_restoration_is_not_expressed_variance():
    r = audit.moments(np.array([[.4375, .5625]] * 4))
    assert r['allele_variance'] == 1 / 256
    assert r['expressed_variance'] == 0
    assert r['fixed'] is False
    assert r['mean'] == .5


def test_directional_exclusion_can_precede_fixation():
    r = audit.moments(np.array([[.5, .5625], [.5625, .5]]))
    assert not r['fixed']
    assert not audit.supports_target(r['minimum'], .5)
    assert audit.supports_target(.4375, .5)


def test_event_requires_twenty_finite_censuses_and_reports_start():
    assert audit.event_start([.5] + [.4375] * 19, .5) is None
    assert audit.event_start([.5] + [.4375] * 20, .5) == 1
    assert audit.event_start([.4375] * 10 + [None] + [.4375] * 19, .5) is None
    assert audit.event_start([.4375] * 21, .5, start=2) is None
    assert audit.event_start([.4375] * 22, .5, start=2) == 2


def test_empty_population_is_undefined_not_zero():
    r = audit.moments(np.empty((0, 2)))
    assert r['mean'] is None and r['minimum'] is None and r['fixed'] is None
    assert audit.supports_target(None, .5) is None


@pytest.mark.parametrize('genes', [np.array([[np.nan, .5]]), np.array([[1.1, .5]]), np.ones((3, 3))])
def test_invalid_genes_fail_closed(genes):
    with pytest.raises(ValueError):
        audit.moments(genes)


def test_sparse_or_nonintegral_offsets_are_rejected():
    a = dict(offsets=np.array([0, 1, 2]), alleles=np.ones((2, 3, 2)) / 2)
    assert len(audit.trajectory(a, 2)) == 2
    with pytest.raises(ValueError):
        audit.trajectory(a, 201)
    a['offsets'] = np.array([0., 1.5, 2.])
    with pytest.raises(ValueError):
        audit.trajectory(a, 2)


def test_no_trigger_requires_unchanged_terminal_all_fields():
    a = {k: np.array([1, 2]) for k in audit.STATE_FIELDS}
    b = {k: v.copy() for k, v in a.items()}
    audit.check_state_equal(a, b)
    b['mutation_flags'][0] = 3
    with pytest.raises(ValueError):
        audit.check_state_equal(a, b)


def test_duplicate_inventory_rejected():
    with pytest.raises(ValueError):
        audit.unique_by_key([{'key': 'a'}, {'key': 'a'}])
