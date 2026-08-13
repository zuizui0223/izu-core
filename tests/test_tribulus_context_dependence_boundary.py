import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/results/tribulus_island_continent/context_dependence_summary.json"


def load_summary():
    return json.loads(SUMMARY.read_text(encoding="utf-8"))


def test_tribulus_boundary_is_galapagos_dependent_not_universal_dwarfism():
    summary = load_summary()
    results = summary["id_level_results"]

    adjusted = results["bioclimate_adjusted_island_minus_continent_mm"]
    assert adjusted["estimate"] < 0
    assert adjusted["hc3_ci_95"][1] < 0

    without_galapagos = results[
        "bioclimate_excluding_galapagos_island_minus_continent_mm"
    ]
    assert abs(without_galapagos["estimate"]) < 0.1
    assert without_galapagos["hc3_ci_95"][0] < 0 < without_galapagos["hc3_ci_95"][1]

    galapagos = results["galapagos_minus_other_islands_mm"]
    assert galapagos["estimate"] < -8
    assert galapagos["hc3_ci_95"][1] < -6


def test_tribulus_boundary_cannot_inflate_formal_response_shape_replication():
    summary = load_summary()
    assert summary["cross_system_role"] == "boundary_adversarial_evidence_only"
    assert summary["formal_same_family_response_shape_replication"] is False
    assert summary["effect_registry_eligible"] is False
    boundary = summary["claim_boundary"].lower()
    assert "do not create independent island-mainland sister-pair systems" in boundary
    assert "2/2" in boundary
