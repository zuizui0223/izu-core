import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/results/cross_archipelago_context_convergence_summary.json"


def test_galapagos_convergence_is_cross_scale_but_not_numeric_meta_analysis():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    within = summary["within_lineage_source_native_evidence"]
    between = summary["between_lineage_published_directional_evidence"]

    assert within["galapagos_minus_other_islands_mm"] < -8
    assert abs(within["bioclimate_excluding_galapagos_island_minus_continent_mm"]) < 0.1
    assert between["n_contrasts"] == 136
    assert between["source_native_pair_table_recovered"] is False
    assert between["numeric_effect_admitted"] is False
    assert summary["formal_cross_system_numeric_fit_ready"] is False
    assert summary["effect_registry_eligible"] is False
    assert summary["causal_claim_allowed"] is False


def test_convergence_does_not_relabel_context_as_universal_island_effect():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    synthesis = summary["synthesis"].lower()
    boundary = summary["claim_boundary"].lower()
    assert "neither study supports universal island floral dwarfism" in synthesis
    assert "candidate moderator" in synthesis
    assert "not a pooled effect" in boundary
    assert "competing explanations" in boundary
