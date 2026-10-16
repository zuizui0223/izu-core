"""Negative admission and independent six-class Q2 consumer checks; no full biology."""
from __future__ import annotations

import hashlib
import json

import numpy as np
import pytest

from scripts.chapter2_q2_i_support_order_20261016 import (
    DEFAULT_DESIGN, declared_tasks, load_protocol, response_class, simulate,
)
from scripts.run_chapter2_q2_i_support_production_20261016 import (
    admission, case_key, execute_shard, save_case,
)
from scripts.verify_chapter2_q2_i_support_order_20261016 import (
    _scores, _arrays_checked, classify_independently, readout,
)


def _trace(a, i, extinct=None):
    z = np.full((201, 5), np.nan)
    z[:, 0] = 48.
    z[:, 1] = z[:, 2] = .5
    z[:, 3] = .421875
    z[:, 4] = 24
    if a is not None: z[a:, 1] = .56
    if i is not None: z[i:, 2] = .44
    if extinct is not None:
        z[extinct:, 0] = 0
        z[extinct:, 1:] = np.nan
    return z


@pytest.mark.parametrize("a,i,ext", [
    (2, 20, None), (18, 2, None), (3, 6, None),
    (2, None, None), (None, 4, None), (None, None, None),
    (8, None, 11), (2, 20, 17),
])
def test_independent_scalar_classifier_matches_frozen_window_loop(a, i, ext):
    d = load_protocol()
    trace = _trace(a, i, ext)
    expected = response_class(trace, d["response"])
    alternative = classify_independently(trace, d["response"])
    assert expected == alternative


def test_without_approval_no_frozen_production(tmp_path):
    target = tmp_path / "approval.json"
    target.write_text(json.dumps({
        "status":"author_reviewed_scientific_execution_approved",
        "owner_explicit_approval":True,
        "design_sha256":"f" * 64,
        "source_manifest_sha256":"a"*64,
        "study":"ch2_q2_I_support_order_20261016",
        "declared_full_cases":384,
        "approval_is_new_not_reused":True,
    }))
    with pytest.raises(ValueError,match="HOLD"):
        admission(target, DEFAULT_DESIGN)
    with pytest.raises(ValueError,match="HOLD"):
        execute_shard(tmp_path / "shard-00", target, DEFAULT_DESIGN, 0)
    assert not (tmp_path / "shard-00").exists()


def test_full_case_writer_refuses_smoke_and_source_is_immutable(tmp_path, monkeypatch):
    d = load_protocol()
    from scripts import run_chapter2_q2_i_support_production_20261016 as producer
    task = declared_tasks(d)[0]
    technical = simulate(d, task, steps=4)
    monkeypatch.setattr(producer, "simulate", lambda *a, **kw: technical)
    with pytest.raises(ValueError,match="technical smoke"):
        save_case(tmp_path, d, task, {"provenance":"technical"})
    assert list(tmp_path.iterdir()) == []


def test_full_inventory_required_before_any_readout(tmp_path):
    with pytest.raises(ValueError, match="all 32"):
        readout(tmp_path, DEFAULT_DESIGN)


def test_two_way_pairs_retained_as_founder_by_visitor_cells():
    d = load_protocol()
    rows = {}
    for fs, vs, arm, policy in declared_tasks(d):
        rows[case_key((fs,vs,arm,policy))] = {
            "label":"assurance_first" if policy=="dense_reachable" else
                    "investment_first" if policy=="sparse_reachable" else "assurance_only",
            "I_event":policy!="dense_unreachable",
        }
    contrasts = _scores(rows, d)
    assert contrasts.shape == (8,8,2)
    np.testing.assert_array_equal(contrasts[:,:,0], 2)
    np.testing.assert_array_equal(contrasts[:,:,1], 0)


def test_case_keys_bijectively_map_original_tasks():
    d = load_protocol()
    keys = [case_key(task) for task in declared_tasks(d)]
    assert len(keys) == len(set(keys)) == 384
    assert len(keys[:12]) == 12



@pytest.mark.parametrize("damage", ["none", "wrong_origin", "duplicated_newborn",
                                    "foreign_mother", "illegal_I_mutation"])
def test_archived_technical_genomes_and_parentage_are_independently_verified(tmp_path, damage):
    """Four-update fixtures only; exercise the full 201-point reader at H=4."""
    original = load_protocol()
    d = {**original, "horizon": 4}
    task = declared_tasks(original)[0]
    record = simulate(original, task, steps=4)
    values = {name: value.copy() for name,value in record.items()
              if isinstance(value,np.ndarray)}
    newborn_offset = int(values["offsets"][1])
    if damage == "wrong_origin":
        values["allele_origin"][newborn_offset, 1, 0] = 999999999
    elif damage == "duplicated_newborn":
        assert len(values["parentage"]) >= 2
        values["parentage"][1, 0] = values["parentage"][0, 0]
    elif damage == "foreign_mother":
        values["parentage"][0, 1] = 999999999
    elif damage == "illegal_I_mutation":
        values["mutation_flags"][newborn_offset, 1, 0] = True
    p = tmp_path / "source_case.npz"
    np.savez_compressed(p, **values)
    if damage == "none":
        np.testing.assert_array_equal(_arrays_checked(p, d, task), record["trace"])
        np.testing.assert_array_equal(_arrays_checked(p, d, task, native_replay=True), record["trace"])
    else:
        with pytest.raises(ValueError):
            _arrays_checked(p, d, task)



def test_native_replay_detects_plausible_mutation_record_tamper(tmp_path):
    """A genomic A-mutation flag can pass structural genealogy but fails exact RNG replay."""
    original = load_protocol()
    d = {**original, "horizon": 4}
    task = declared_tasks(original)[0]
    record = simulate(original, task, steps=4)
    arrays = {k:v.copy() for k,v in record.items() if isinstance(v,np.ndarray)}
    lo,hi = map(int, arrays["offsets"][1:3])
    candidates = np.flatnonzero(~arrays["mutation_flags"][lo:hi,2,0])
    assert len(candidates) > 0
    arrays["mutation_flags"][lo+int(candidates[0]),2,0] = True
    p = tmp_path / "source_mutation_tamper.npz"
    np.savez_compressed(p, **arrays)
    # The ancestral identity and source allele support are still coherent:
    _arrays_checked(p, d, task)
    # But frozen native reproducibility detects the fabricated genome outcome.
    with pytest.raises(ValueError, match="native replay mismatch"):
        _arrays_checked(p, d, task, native_replay=True)
