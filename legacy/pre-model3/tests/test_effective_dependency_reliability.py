import json
from pathlib import Path

import pytest

from channel_id.effective_dependency_reliability import build_dependency_reliability_audit

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "design" / "effective_dependency_reliability_calibration.json"
READINESS = ROOT / "data" / "design" / "effective_pollinator_dependency_field_readiness.json"


def row(target: str, taxon: str, repeat: str, estimate: float, bundle_char: str, **overrides):
    value = {
        "calibration_id": f"{target}-{repeat}",
        "target_unit_id": target,
        "taxon": taxon,
        "site_id": f"site-{target}",
        "season_id": "2026-summer",
        "repeat_block_id": repeat,
        "estimand_name": "direct_reproductive_dependency_0_1",
        "dependency_estimate": str(estimate),
        "independent_plants": "4",
        "nonoverlapping_plant_panel": "yes",
        "protocol_id": "dep-v1",
        "source_bundle_sha256": bundle_char * 64,
        "notes": "",
    }
    value.update({key: str(item) for key, item in overrides.items()})
    return value


def repeated_rows():
    return (
        row("t1", "taxon-a", "r1", 0.10, "1"),
        row("t1", "taxon-a", "r2", 0.12, "2"),
        row("t2", "taxon-b", "r1", 0.50, "3"),
        row("t2", "taxon-b", "r2", 0.52, "4"),
        row("t3", "taxon-c", "r1", 0.90, "5"),
        row("t3", "taxon-c", "r2", 0.88, "6"),
    )


def test_current_machine_readable_state_keeps_final_estimand_reliability_blocked():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    assert design["status"] == "blocked_no_repeated_final_estimand"
    assert design["current_evidence"]["calibration_scope_reliability_identified"] is False
    assert design["dependency_fdq_design_injection"]["automatic"] is False
    gate = readiness["direct_dependency_reliability_calibration"]
    assert gate["ordinary_campanula_pilot_identifies_this_reliability"] is False
    assert gate["technical_svd_recount_identifies_this_reliability"] is False
    assert gate["automatic_dependency_fdq_injection"] is False


def test_empty_calibration_keeps_reliability_blocked():
    result = build_dependency_reliability_audit(())
    assert result["direct_dependency_reliability_identified_for_calibration_scope"] is False
    assert result["dependency_fdq_design_reliability_admitted"] is False
    assert result["automatic_design_simulation_injection_allowed"] is False
    assert result["calibration_scope_reliability"]["status"] == "not_estimable"


def test_independent_repeated_final_estimands_can_identify_calibration_scope_reliability():
    result = build_dependency_reliability_audit(repeated_rows())
    reliability = result["calibration_scope_reliability"]
    assert reliability["status"] == "estimable"
    assert 0.0 <= reliability["direct_dependency_repeat_reliability"] <= 1.0
    assert reliability["direct_dependency_repeat_reliability"] > 0.9
    assert result["direct_dependency_reliability_identified_for_calibration_scope"] is True
    assert result["distinct_taxa_in_repeated_targets"] == 3
    assert result["target_mean_dependency_span"] == pytest.approx(0.78)
    # Identification inside the calibration scope never auto-opens the cross-lineage simulation.
    assert result["dependency_fdq_design_reliability_admitted"] is False
    assert result["automatic_design_simulation_injection_allowed"] is False


def test_overlapping_plant_panels_do_not_count_as_independent_repeats():
    rows = tuple(dict(item, nonoverlapping_plant_panel="no") for item in repeated_rows())
    result = build_dependency_reliability_audit(rows)
    assert result["eligible_repeat_rows"] == 0
    assert result["direct_dependency_reliability_identified_for_calibration_scope"] is False
    assert all("plant_panel_not_independent" in item["reason"] for item in result["ineligible_rows"])


def test_reusing_one_frozen_bundle_cannot_create_an_independent_repeat():
    first = row("t1", "taxon-a", "r1", 0.10, "a")
    second = row("t1", "taxon-a", "r2", 0.12, "a")
    with pytest.raises(ValueError, match="source bundle reused"):
        build_dependency_reliability_audit((first, second))


def test_mixed_final_estimand_protocols_are_not_pooled():
    rows = list(repeated_rows())
    rows[-1] = dict(rows[-1], protocol_id="dep-v2")
    result = build_dependency_reliability_audit(tuple(rows))
    assert result["calibration_scope_reliability"]["status"] == "not_estimable"
    assert "multiple protocol_id" in result["calibration_scope_reliability"]["reason"]
    assert result["direct_dependency_reliability_identified_for_calibration_scope"] is False


def test_technical_or_nonfinal_estimand_cannot_open_gate():
    rows = tuple(dict(item, estimand_name="svd_technical_repeatability") for item in repeated_rows())
    result = build_dependency_reliability_audit(rows)
    assert result["eligible_repeat_rows"] == 0
    assert result["direct_dependency_reliability_identified_for_calibration_scope"] is False
    assert "technical SVD recount repeatability" in result["forbidden_substitutions"]
