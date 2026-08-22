import json
from pathlib import Path

from scripts.analyze_island_response_evidence_architecture import analyze


def test_generated_result_matches_committed_result():
    matrix = json.loads(Path("data/design/island_system_response_axis_matrix.json").read_text(encoding="utf-8"))
    expected = json.loads(Path("data/results/island_response_evidence_architecture.json").read_text(encoding="utf-8"))
    assert analyze(matrix) == expected
    assert expected["n_systems"] == 11


def test_visual_signal_is_active_but_not_yet_directly_represented():
    result = json.loads(Path("data/results/island_response_evidence_architecture.json").read_text(encoding="utf-8"))
    assert result["axis_summary"]["visual_signal"] == {
        "direct_systems": 0,
        "partial_systems": 0,
        "missing_systems": 11,
    }
    assert result["key_findings"]["visual_signal_is_active_but_empirically_empty_in_current_matrix"] is True


def test_functional_environment_axis_is_now_in_evidence_architecture():
    result = json.loads(Path("data/results/island_response_evidence_architecture.json").read_text(encoding="utf-8"))
    assert result["axis_summary"]["pollinator_functional_environment"] == {
        "direct_systems": 5,
        "partial_systems": 4,
        "missing_systems": 2,
    }
    assert result["key_findings"]["pollinator_functional_environment_direct_systems"] == 5


def test_ogasawara_adds_direct_morphology_and_reproduction_not_numeric_functional_position():
    result = json.loads(Path("data/results/island_response_evidence_architecture.json").read_text(encoding="utf-8"))
    profile = next(row for row in result["system_profiles"] if row["system_id"] == "ogasawara_psychotria_homalosperma")
    assert profile["direct_axes"] == ["floral_morphology", "reproductive_outcome"]
    assert set(profile["partial_axes"]) == {
        "interaction_network",
        "mating_and_reproductive_assurance",
        "pollinator_effectiveness",
        "pollinator_functional_environment",
    }
    assert profile["missing_axes"] == ["visual_signal"]


def test_strongest_three_axis_backbone_is_functional_environment_morphology_network():
    result = json.loads(Path("data/results/island_response_evidence_architecture.json").read_text(encoding="utf-8"))
    backbone = result["key_findings"]["strongest_three_axis_direct_backbone"]
    assert backbone["axes"] == [
        "pollinator_functional_environment",
        "floral_morphology",
        "interaction_network",
    ]
    assert backbone["n_systems"] == 4
    assert backbone["systems"] == [
        "caribbean_gesneriaceae",
        "hawaii",
        "izu",
        "xisha_cordia_subcordata",
    ]


def test_analysis_does_not_claim_effect_direction():
    result = json.loads(Path("data/results/island_response_evidence_architecture.json").read_text(encoding="utf-8"))
    assert result["analysis_type"] == "evidence_architecture_not_effect_direction"
    assert "do not imply common response direction" in result["claim_boundary"]
