import json
from pathlib import Path


def load_summary():
    return json.loads(
        Path("data/design/external_bridge_system_registry_summary.json")
        .read_text(encoding="utf-8")
    )


def test_three_independent_partial_bridges_do_not_create_a_complete_bridge():
    summary = load_summary()
    assert summary["counts"]["independent_system_clusters_screened_as_partial_or_stronger"] == 3
    assert summary["counts"]["bridge_system_partial"] == 3
    assert summary["counts"]["bridge_system_complete"] == 0
    assert summary["formal_cross_system_mechanism_fit_ready"] is False


def test_cordia_is_current_best_but_still_partial():
    summary = load_summary()
    assert summary["current_best_bridge"] == "xisha_cordia_subcordata_two_island_system"
    cordia = next(row for row in summary["systems"] if row["system_id"] == summary["current_best_bridge"])
    assert cordia["admission_state"] == "bridge_system_partial"
    assert cordia["complete"] is False


def test_every_registry_row_points_to_an_existing_audit():
    summary = load_summary()
    for row in summary["systems"]:
        assert Path(row["audit"]).is_file()


def test_external_partial_recurrence_cannot_substitute_for_issue_91():
    summary = load_summary()
    text = " ".join(summary["why_formal_fit_remains_closed"])
    assert "Issue #91" in text
