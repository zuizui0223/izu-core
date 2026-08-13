import json
from pathlib import Path

import pytest

from channel_id.independent_source_acquisition import (
    dependency_moderation_ready,
    load_manifest,
    numeric_effect_ready,
    run_audit,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "design" / "independent_primary_source_acquisition.json"
NATIVE = ROOT / "data" / "predictive_meta" / "primary_source_native_evidence.csv"


def records():
    return load_manifest(MANIFEST)


def test_three_priority_sources_are_locked_and_linked_to_issue_92():
    rows = records()
    assert {row.source_id for row in rows} == {
        "weigela_yamada_2010",
        "ligustrum_yamada_2014",
        "hosta_yamada_2014",
    }
    assert all(row.issue_number == 92 for row in rows)
    assert all(row.directional_status == "active_B_grade" for row in rows)


def test_no_priority_source_is_promoted_to_numeric_or_dependency_moderation():
    rows = records()
    assert not any(numeric_effect_ready(row) for row in rows)
    assert not any(dependency_moderation_ready(row) for row in rows)
    assert all(row.numeric_effect_status == "blocked" for row in rows)
    assert all(row.dependency_moderation_status == "blocked" for row in rows)


def test_identified_but_unrecovered_routes_remain_below_numeric_gate():
    by_id = {row.source_id: row for row in records()}
    assert by_id["weigela_yamada_2010"].access_status == (
        "publisher_article_route_and_external_supplement_listing_binary_unrecovered"
    )
    assert by_id["ligustrum_yamada_2014"].access_status == (
        "publisher_supporting_files_identified_binary_delivery_blocked"
    )
    assert by_id["hosta_yamada_2014"].access_status == (
        "publisher_supporting_files_identified_binary_delivery_blocked"
    )
    for row in by_id.values():
        assert row.numeric_gate["source_recovered"] is False
        assert numeric_effect_ready(row) is False
        assert dependency_moderation_ready(row) is False


def test_publisher_supplement_filenames_are_routes_not_effect_sizes():
    by_id = {row.source_id: row for row in records()}
    assert by_id["weigela_yamada_2010"].supplements == ()
    assert [
        item["filename"] for item in by_id["ligustrum_yamada_2014"].supplements
    ] == [
        "boj12092-sup-0001-si.doc",
        "boj12092-sup-0002-si.doc",
    ]
    assert len(by_id["hosta_yamada_2014"].supplements) == 5
    assert all(
        item["sufficient_for_numeric_gate"] is False
        for row in records()
        for item in row.supplements
    )


def test_directional_layer_does_not_claim_the_shared_second_step():
    rows = records()
    assert all(row.shared_second_step_status == "does_not_demonstrate" for row in rows)
    weigela = next(row for row in rows if row.source_id == "weigela_yamada_2010")
    assert "gradual mainland-distance decline" in weigela.directional_pattern
    hosta = next(row for row in rows if row.source_id == "hosta_yamada_2014")
    assert "complex non-monotonic" in hosta.directional_pattern
    assert "Southern Izu is not automatically" in hosta.claim_boundary


def test_audit_links_to_source_native_registry_and_reports_blocked_state():
    report = run_audit(MANIFEST, NATIVE)
    summary = report["summary"]
    assert summary["n_priority_sources"] == 3
    assert summary["numeric_effect_ready_sources"] == []
    assert summary["dependency_moderation_ready_sources"] == []
    assert summary["shared_second_step_support_sources"] == []
    assert summary["independent_numeric_test_status"] == (
        "blocked_no_population_level_numeric_source"
    )
    assert summary["dependency_moderation_test_status"] == (
        "blocked_no_dependency_matched_numeric_source"
    )
    assert "not trait values" in summary["claim_boundary"]


def test_ready_status_is_rejected_when_only_metadata_exist(tmp_path):
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["sources"][0]["numeric_effect_status"] = "ready"
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="numeric_effect_status disagrees"):
        load_manifest(path)
