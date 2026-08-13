import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "predictive_meta" / "current_mechanistic_leverage.csv"


def rows():
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_no_current_evidence_unit_is_promoted_to_a_causal_claim():
    records = rows()
    assert records
    assert {row["causal_claim_allowed"] for row in records} == {"no"}


def test_autonomous_capacity_is_the_unique_strongest_breakpoint_leverage():
    records = rows()
    strongest = [row for row in records if row["mechanistic_leverage"] == "strongest_current_breakpoint_leverage"]
    assert len(strongest) == 1
    assert strongest[0]["evidence_unit"] == "campanula_autonomous_capacity"
    assert strongest[0]["response_shape_or_mode"] == "second_transition_step"


def test_continuous_campanula_channels_keep_history_confounders_live():
    indexed = {row["evidence_unit"]: row for row in rows()}
    for evidence_unit in ("campanula_flower_size", "campanula_outcrossing"):
        confounder = indexed[evidence_unit]["main_live_confounder"].lower()
        assert "history" in confounder or "colonisation" in confounder
        assert indexed[evidence_unit]["causal_claim_allowed"] == "no"


def test_controls_and_alternative_modes_are_not_treated_as_primary_holdout_effects():
    indexed = {row["evidence_unit"]: row for row in rows()}
    assert indexed["ligustrum_morphology"]["mechanistic_leverage"] == "negative_control_against_specialists_only_change"
    assert indexed["goodyera_henryi_hybrid"]["analysis_role"] == "alternative_response"
    assert indexed["goodyera_similis_control"]["analysis_role"] == "matched_dependency_control"
    assert indexed["lilium_alternative"]["analysis_role"] == "alternative_mechanism"
