"""Tests only enumerate frozen tasks; no visitor/plant simulation."""
import copy

import pytest

from scripts.chapter2_orthogonal_cohort_manifest import (
    compile_manifest, tasks, validate_manifest,
)


def test_manifest_is_complete_independent_and_unadjudicated():
    m = compile_manifest()
    assert m["status"] == "PLAN_ONLY_NO_OUTCOMES"
    assert m["n_histories"] == 64
    assert m["n_sources"] == 2048
    assert m["futures_per_source"] == 84
    assert m["expected_futures"] == 172032
    assert len(m["shards"]) == 64
    assert [s["visitor_history_id"] for s in m["shards"]] == list(
        range(39110901, 39110965)
    )
    assert all(s["n_sources"] == 32 and s["expected_futures"] == 2688
               for s in m["shards"])
    assert len({k for s in m["shards"] for k in s["case_keys"]}) == 2048
    validate_manifest(m)


def test_shard_is_entire_history_not_random_future_cells():
    grouped = tasks()
    for n, group in enumerate(grouped):
        assert len(group) == 32
        assert len({t.visitor_history for t in group}) == 1
        assert group[0].visitor_history == 39110901 + n
        assert {t.expression_order for t in group} == {
            "assurance_first", "investment_first"
        }


@pytest.mark.parametrize("damage", [
    lambda m: m["shards"].pop(),
    lambda m: m["shards"][0]["case_keys"].pop(),
    lambda m: m["shards"][0].update({"visitor_history_id": 38110901}),
    lambda m: m.update({"status": "RESULTS_ADMITTED"}),
    lambda m: m.update({"expected_futures": 229376}),
    lambda m: m.update({"protocol_sha256": "bad"}),
])
def test_fail_closed_on_source_or_protocol_tampering(damage):
    m = copy.deepcopy(compile_manifest())
    damage(m)
    with pytest.raises(AssertionError):
        validate_manifest(m)
