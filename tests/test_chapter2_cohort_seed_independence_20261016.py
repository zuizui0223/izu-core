"""Reject false 'independent visitor history' claims without banning CRNs.

No scientific model or historic source/result is changed by these tests.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from scripts.audit_chapter2_cohort_seed_independence_20261016 import (
    LEDGER, ROOT, audit_registry, scan_design_seed_fields, seed_ids,
)


def _registry():
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def _row(data, name):
    return next(x for x in data["cohorts"] if x["id"] == name)


def test_frozen_high_impact_history_ledger_and_execution_status():
    report = audit_registry(_registry(), ROOT)
    assert report["status"] == "PASS_EXPLICIT_COHORT_SEED_NAMESPACE_AUDIT"
    assert report["executed_registered_cohorts"] == 6
    assert report["superseded_without_outcomes"] == 1
    rows = {r["id"]: r for r in report["cohorts"]}
    assert rows["fhs_new_visitor_retired_20261003"]["result"] is None
    assert rows["fhs_new_visitor_20261004"]["visitor_count"] == 128
    assert rows["q1_new_founders_20261016"]["visitor_count"] == 8
    assert rows["q1_new_founders_20261016"]["founder_seed_count"] == 8
    assert rows["q1_single_founder_20261006"]["founder_seed_count"] == 1
    assert rows["q4_island_independent32_20261008"]["visitor_count"] == 32
    overlaps = [r for r in report["overlaps"] if r["both_executed"] and r["visitor_overlap"]]
    assert len(overlaps) == 1
    assert {overlaps[0]["a"], overlaps[0]["b"]} == {
        "fhs_discovery_20261003", "fhs_new_demography_20261003"
    }
    assert overlaps[0]["visitor_overlap"] == 128
    assert overlaps[0]["intentional_visitor_matching"] is True


def test_false_visitor_history_independence_claim_is_rejected():
    data = _registry()
    _row(data, "fhs_new_demography_20261003")["claims_independent_visitor_from"] = [
        "fhs_discovery_20261003"
    ]
    with pytest.raises(ValueError, match="False independent visitor-history"):
        audit_registry(data, ROOT)


def test_unexplained_reuse_of_executed_visitor_histories_is_rejected():
    data = _registry()
    _row(data, "fhs_new_demography_20261003")["intentional_visitor_sharing_with"] = []
    with pytest.raises(ValueError, match="reuse visitor histories"):
        audit_registry(data, ROOT)


def test_independent_demography_claim_must_not_reuse_original_demography():
    data = _registry()
    _row(data, "fhs_new_demography_20261003")["demographic_seeds"]["ids"] = list(range(101, 105))
    # The frozen design also rejects these numbers via its original source.
    with pytest.raises(ValueError, match="Registry seeds do not match"):
        audit_registry(data, ROOT)


def test_shared_q1_q4_founder_does_not_imply_new_independent_founder():
    data = _registry()
    _row(data, "q4_island_independent32_20261008")["claims_independent_founder_from"] = [
        "q1_single_founder_20261006"
    ]
    with pytest.raises(ValueError, match="False independent founder-genome"):
        audit_registry(data, ROOT)


def test_superseded_protocol_is_not_a_second_executed_validation():
    data = _registry()
    record = _row(data, "fhs_new_visitor_retired_20261003")
    record["execution"] = "completed"
    record["result"] = "data/results/chapter2_finite_history_signal_environment_validation_20261004.json"
    with pytest.raises(ValueError, match="Cohort result design pointer differs"):
        audit_registry(data, ROOT)


@pytest.mark.parametrize("entry", [
    None, {"ids": [1, 1]}, {"ids": [True]},
    {"first": 3, "last": 2}, {"first": -1, "last": 1},
    {"ids": []}, {"first": 1, "last": 200005}, {"ids": "101"},
])
def test_explicit_namespace_seed_validation(entry):
    if entry is None:
        assert seed_ids(entry) == set()
    else:
        with pytest.raises(ValueError):
            seed_ids(entry)


def test_seed_numeric_equality_across_genetic_and_visitor_namespaces_is_not_a_collision():
    data = _registry()
    first = _row(data, "fhs_discovery_20261003")
    second = _row(data, "q1_single_founder_20261006")
    # Numeric founder 74001 equals a bridge visitor-history seed 74001.
    assert second["founder_seeds"]["ids"] == [74001]
    assert first["visitor_seeds"]["first"] == 74001
    # They belong to distinct generator/biological RNG namespaces, and must
    # not be interpreted as duplicated visitor histories or founders.
    assert audit_registry(data, ROOT)["executed_registered_cohorts"] == 6


def test_all_design_seed_field_sites_are_inventoried_without_inferred_replicates():
    scan = scan_design_seed_fields(ROOT)
    assert scan["json_design_files_scanned"] >= 135
    assert scan["designs_with_declared_seed_fields"] >= 10
    assert scan["invalid_json_designs"] == []
    all_paths = {v["path"] for v in scan["seed_field_inventory"]}
    assert "data/design/chapter2_assurance_generality_20261006.json" in all_paths
    assert "data/design/chapter2_q1_fresh_founder_generality_20261016.json" in all_paths
    assert "data/design/chapter2_finite_history_signal_environment_validation_20261004.json" in all_paths
    assert "does NOT infer RNG stream independence" in scan["caution"]
