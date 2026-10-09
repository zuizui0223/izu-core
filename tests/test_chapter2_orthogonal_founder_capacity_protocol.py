"""Protocol tests only: no real biological trajectories are generated."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.plan_chapter2_orthogonal_founder_capacity import (
    PROTOCOL, validate_protocol,
)


def _tamper(tmp_path: Path, mutator) -> Path:
    d = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    mutator(d)
    p = tmp_path / "protocol.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    return p


def test_complete_fixed_design_no_biological_execution():
    d = validate_protocol()
    assert d == {
        "status": "PRE_OUTCOME_PROTOCOL_ONLY_NOT_EXECUTABLE",
        "new_independent_visitor_histories": 64,
        "sources": 2048,
        "futures_per_source": 84,
        "planned_futures": 172032,
        "production_executed": False,
    }


def test_original_exposed_histories_cannot_be_reused(tmp_path):
    p = _tamper(
        tmp_path, lambda d: d["new_independent_cohort"].update({
            "visitor_history_first": 38110901,
            "visitor_history_last": 38110964,
        }),
    )
    with pytest.raises(AssertionError, match="overlap"):
        validate_protocol(p)


def test_cannot_silently_add_invalid_48_founders_capacity8(tmp_path):
    def violate(d):
        d["experimental_arms"].append({
            "name": "all_available_founders_capacity8",
            "founder_rule": "full",
            "capacity": 8,
            "founder_group": "full",
        })
    with pytest.raises(AssertionError, match="Exact three valid"):
        validate_protocol(_tamper(tmp_path, violate))


def test_full_grid_and_baseline_cannot_be_silently_changed(tmp_path):
    with pytest.raises(AssertionError, match="count mismatch"):
        validate_protocol(_tamper(
            tmp_path, lambda d: d["complete_future_grid"].update({
                "expected_future_records": 229376,
            }),
        ))
    with pytest.raises(AssertionError, match="Postzygotic"):
        validate_protocol(_tamper(
            tmp_path, lambda d: d["postzygotic_gates"][1].update({
                "outcrossed_seed_retention": 0.5,
            }),
        ))


def test_primary_64_history_inference_is_immutable(tmp_path):
    with pytest.raises(AssertionError, match="primary estimand"):
        validate_protocol(_tamper(
            tmp_path, lambda d: d["estimands"].update({
                "cluster_unit": "future_trajectory",
            }),
        ))


def test_unpaired_rng_seed_is_forbidden(tmp_path):
    with pytest.raises(AssertionError, match="random-stream"):
        validate_protocol(_tamper(
            tmp_path,
            lambda d: d["paired_future_randomness"].update({
                "same_random_stream_initialization_for_all_three_arms_and_both_viability_gates": False
            }),
        ))
