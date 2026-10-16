"""Adversarial ALL48 inventory tests; no source biology re-executed."""
import itertools

import numpy as np
import pytest

from scripts.kernel_expression_accounting_20261013.verify_kernel_expression_independent_v2 import (
    ARMS, BUDGETS, FRACTIONS, POLICIES, SETTINGS, expected_cases,
    expected_kernel_key, validate_arrays, validate_metadata, validate_pair_keys,
)


def _inventory():
    pairs = list(itertools.product(FRACTIONS, SETTINGS, BUDGETS, ARMS))
    records = [dict(mismatch_fraction=x[0], setting=x[1], budget=x[2],
                    visitor_arm=x[3]) for x in pairs]
    keys = [expected_kernel_key(x, p) for x in pairs for p in POLICIES]
    return records, keys


def test_full_permutation_passes_and_has_48_declared_contexts():
    rows, keys = _inventory()
    assert len(expected_cases()) == 48
    assert validate_metadata(rows, keys) == list(itertools.product(FRACTIONS, SETTINGS, BUDGETS, ARMS))


@pytest.mark.parametrize("damage", ["empty", "delete", "duplicate", "foreign", "boolean", "nan"])
def test_bad_comparison_inventory_fails_closed(damage):
    rows, keys = _inventory()
    if damage == "empty": rows = []
    if damage == "delete": rows.pop()
    if damage == "duplicate": rows[-1] = dict(rows[0])
    if damage == "foreign": rows[-1]["setting"] = "unexpected"
    if damage == "boolean": rows[0]["mismatch_fraction"] = True
    if damage == "nan": rows[0]["mismatch_fraction"] = float("nan")
    with pytest.raises(ValueError):
        validate_metadata(rows, keys)


@pytest.mark.parametrize("damage", ["delete", "duplicate", "foreign"])
def test_bad_kernel_inventory_fails_closed(damage):
    rows, keys = _inventory()
    if damage == "delete": keys.pop()
    if damage == "duplicate": keys[-1] = keys[0]
    if damage == "foreign": keys[-1] = "invented_source"
    with pytest.raises(ValueError):
        validate_metadata(rows, keys)


def _arrays():
    states = np.array([(a,b,c) for a in range(9) for b in range(9-a)
                       for c in range(9-a-b)], dtype=int)
    eye = np.eye(165)
    kernels = np.broadcast_to(eye, (96,165,165))
    probs = np.zeros((96,81,165))
    probs[:,:,0] = 1
    terms = np.zeros((48,2,80,165))
    return kernels, states, probs, terms.copy(), terms.copy()


def test_exact_original_shape_state_inventory():
    assert len(validate_arrays(*_arrays())) == 5


@pytest.mark.parametrize("damage", ["state_duplicate", "kernel_negative", "curve_nan", "term_inf", "term_short"])
def test_corrupted_array_rejected(damage):
    arrays = list(_arrays())
    if damage == "state_duplicate":
        arrays[1] = arrays[1].copy()
        arrays[1][0] = arrays[1][1]
    if damage == "kernel_negative":
        arrays[0] = arrays[0].copy()
        arrays[0][0,0,0] = -1
    if damage == "curve_nan": arrays[2][0,0,0] = float("nan")
    if damage == "term_inf": arrays[3][0,0,0,0] = float("inf")
    if damage == "term_short": arrays[4] = arrays[4][:-1]
    with pytest.raises(ValueError):
        validate_arrays(*arrays)


def test_signed_array_axis_identity_cannot_be_swapped():
    rows, keys = _inventory()
    pairs = validate_metadata(rows, keys)
    labels = [str(tuple(p)) for p in pairs]
    validate_pair_keys(labels, pairs)
    labels[0], labels[1] = labels[1], labels[0]
    with pytest.raises(ValueError, match="signed contribution rows"):
        validate_pair_keys(labels, pairs)
