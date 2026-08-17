import json
from pathlib import Path

from scripts.analyze_island_response_evidence_architecture import analyze


def test_generated_result_matches_committed_result():
    matrix = json.loads(Path("data/design/island_system_response_axis_matrix.json").read_text(encoding="utf-8"))
    expected = json.loads(Path("data/results/island_response_evidence_architecture.json").read_text(encoding="utf-8"))
    assert analyze(matrix) == expected


def test_visual_signal_is_active_but_not_yet_directly_represented():
    result = json.loads(Path("data/results/island_response_evidence_architecture.json").read_text(encoding="utf-8"))
    assert result["axis_summary"]["visual_signal"] == {
        "direct_systems": 0,
        "partial_systems": 0,
        "missing_systems": 10,
    }
    assert result["key_findings"]["visual_signal_is_active_but_empirically_empty_in_current_matrix"] is True


def test_functional_reproductive_three_axis_backbone_is_repeated_in_three_systems():
    result = json.loads(Path("data/results/island_response_evidence_architecture.json").read_text(encoding="utf-8"))
    backbone = result["key_findings"]["strongest_three_axis_direct_backbone"]
    assert backbone["axes"] == [
        "mating_and_reproductive_assurance",
        "pollinator_effectiveness",
        "reproductive_outcome",
    ]
    assert backbone["n_systems"] == 3
    assert backbone["systems"] == ["canary", "galapagos", "seychelles"]


def test_analysis_does_not_claim_effect_direction():
    result = json.loads(Path("data/results/island_response_evidence_architecture.json").read_text(encoding="utf-8"))
    assert result["analysis_type"] == "evidence_architecture_not_effect_direction"
    assert "do not imply common response direction" in result["claim_boundary"]
