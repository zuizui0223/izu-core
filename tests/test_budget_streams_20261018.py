"""Read-only reconciliation tests: no new Model3 history is executed."""
import copy
import json
from pathlib import Path
import pytest
from scripts.audit_chapter2_budget_streams_20261018 import review, SOURCE, OLD_SOURCE

def inputs():
    return json.loads(SOURCE.read_text()), json.loads(OLD_SOURCE.read_text())

def test_two_stream_families_are_not_independent_founder_replication():
    d, old = inputs()
    result = review(d, old)
    assert result["independent_axes"] == {"founders":6,"visitors":6}
    assert result["shared_historical_pairs"] == 72
    assert result["new_unique_biological_histories"] == 0
    assert result["confirmation_authorized"] is False
    assert result["by_stream"]["90"]["arms"]["fixed_B4.5"]["alive"] == 1
    assert result["by_stream"]["104"]["arms"]["fixed_B4.5"]["alive"] == 5
    for block in result["by_stream"].values():
        for a in block["arms"].values():
            assert a["alive_accessible"]+a["alive_closed"]+a["extinct"] == 72

def test_unconditional_four_arm_interactions_and_common_genetic_endpoint():
    result = review(*inputs())
    s90, s104 = result["by_stream"]["90"], result["by_stream"]["104"]
    assert s90["survival_interaction"]["estimate"] == pytest.approx(70/72)
    assert s104["survival_interaction"]["estimate"] == pytest.approx(66/72)
    assert s90["access_interaction"]["estimate"] == pytest.approx(25/72)
    assert s104["access_interaction"]["estimate"] == pytest.approx(26/72)
    assert result["old_genetic_loss"]["fixed"] == 42
    assert result["old_genetic_loss"]["evolving"] == 58
    assert result["old_genetic_loss"]["unchanged_old_result"] is True

def test_different_namespaces_missing_states_and_pseudoreplication_fail_closed():
    d, old = inputs()
    cases = []
    p = copy.deepcopy(d)
    p["streams"]["104"]["seed_prefix"] = [20261018,90]
    cases.append(p)
    p = copy.deepcopy(d)
    p["streams"]["104"]["terminal_status_codes"]["fixed_B8"] = "1"*71
    cases.append(p)
    p = copy.deepcopy(d)
    p["shared_source"]["existing_founder_ids"] = list(range(12))
    cases.append(p)
    for p in cases:
        with pytest.raises(ValueError):
            review(p, old)

def test_population_of_future_runs_does_not_erase_old_power_constraints():
    result = review(*inputs())
    row = next(r for r in result["power_screen_only"] if r["F"]==16)
    assert .16 < row["genetic_loss_mde"] < .17
    assert row["genetic_loss_mde"] > max(row["survival_mde_by_stream"].values())
    assert result["selected_SESOI"] is None
    assert result["new_confirmatory_sample_size"] is None
    assert result["power_screen_is_not_approval"] is True
