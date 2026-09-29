import json
from pathlib import Path


def load_audit():
    return json.loads(
        Path("data/design/external_bridge_caribbean_gesneriaceae_source_audit.json")
        .read_text(encoding="utf-8")
    )


def test_caribbean_gesneriaceae_is_partial_clade_level_bridge():
    audit = load_audit()
    assert audit["admission_state"] == "bridge_system_partial"
    assert audit["bridge_level"] == "clade_level"
    assert audit["bridge_complete"] is False
    assert audit["formal_cross_system_model_eligible"] is False


def test_visit_level_effectiveness_is_not_imputed():
    linkage = load_audit()["cross_source_linkage"]
    assert linkage["visit_level_effectiveness_measured"] is False
    assert linkage["pollen_function_measured_per_visit"] is False
    assert any("visitation rate" in item for item in linkage["blocked_claims"])


def test_island_autofertility_is_not_promoted_against_source_result():
    audit = load_audit()
    source = next(
        row for row in audit["sources"]
        if row["source_id"] == "marten_rodriguez_2015_island_mainland_reproductive_strategies"
    )
    assert source["source_native_numeric_anchors"]["island_mainland_autofertility_difference"] == "not detected"
    blocked = " ".join(audit["cross_source_linkage"]["blocked_claims"])
    assert "AFI comparison did not show" in blocked


def test_second_partial_bridge_does_not_open_formal_fit():
    comparison = load_audit()["comparison_with_nicotiana"]
    assert comparison["independent_system_cluster"] is True
    assert comparison["does_not_make_formal_cross_system_fit_ready"] is True
