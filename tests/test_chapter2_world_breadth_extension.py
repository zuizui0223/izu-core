import json
from pathlib import Path

from scripts.audit_chapter2_world_breadth_extension import build_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_world_breadth_extension_audit_20260903.json"
DOC = ROOT / "docs/CHAPTER2_WORLD_BREADTH_EXTENSION_20260903.md"
UNIVERSE = ROOT / "docs/COMPARATIVE_ISLAND_SYSTEM_UNIVERSE_20260827.md"
SYNTHESIS = ROOT / "data/design/chapter2_world_breadth_synthesis_context_20260904.csv"


def test_world_breadth_extension_matches_deterministic_audit():
    computed = build_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["frozen_identifiability_denominator"]["research_entries"] == 25
    assert computed["frozen_identifiability_denominator"]["geographic_overlap_labels"] == 21
    assert computed["post_freeze_extension"]["research_entries"] == 17
    assert computed["post_freeze_extension"]["exact_geographic_groups"] == 16
    assert computed["combined_descriptive_universe"]["research_entries_before_cross_layer_deduplication"] == 42
    assert computed["combined_descriptive_universe"]["exact_overlap_labels_before_higher_level_archipelago_deduplication"] == 37
    assert computed["combined_descriptive_universe"]["independent_archipelago_denominator_claimed"] is False


def test_extension_strengthens_arrival_axis_without_reopening_prediction_gate():
    payload = build_audit()
    extension = payload["post_freeze_extension"]
    assert extension["direct_or_historical_arrival_entries"] == 4
    assert set(extension["direct_or_historical_arrival_ids"]) == {
        "new_caledonia_kato_kawakita_2004",
        "fiji_braunsapis_invasion_2015",
        "french_polynesia_apid_origins_2017",
        "samoa_apid_introductions_2014",
    }
    assert extension["arrival_evidence_class_counts"]["none"] == 9
    assert "vanuatu" in extension["geographic_groups"]
    assert "samoa" in extension["geographic_groups"]
    assert "lower_florida_keys" in extension["geographic_groups"]
    assert "socotra" in extension["geographic_groups"]
    assert "crete" in extension["geographic_groups"]
    assert "trinidad_tobago" in extension["geographic_groups"]
    assert "iceland" in extension["geographic_groups"]
    assert extension["manuscript_value_promoted_entries"] == 3
    assert set(extension["manuscript_value_promoted_ids"]) == {
        "crete_cyclamen_breeding_1997",
        "trinidad_tobago_hummingbird_pollination_1982",
        "iceland_campanula_uniflora_breeding_2006",
    }
    assert extension["full_chapter2_contract_passes"] == 0
    assert payload["frozen_identifiability_denominator"]["formal_external_prediction_reopened"] is False
    assert payload["frozen_identifiability_denominator"]["frozen_25_recomputed"] is False


def test_multi_group_synthesis_is_breadth_context_not_prediction_replication():
    payload = build_audit()
    context = payload["multi_group_breadth_context"]
    assert context["research_syntheses"] == 1
    assert context["southern_ocean_source_native_island_groups"] == 11
    assert context["southern_ocean_flowering_plant_species"] == 321
    assert context["included_in_formal_or_exact_group_denominators"] is False
    text = SYNTHESIS.read_text(encoding="utf-8").lower()
    assert "10.1093/aobpla/plv095" in text
    assert "southern ocean islands" in text


def test_world_breadth_documentation_keeps_denominators_separate():
    text = DOC.read_text(encoding="utf-8")
    lower = text.lower()
    assert "25 research entries" in lower
    assert "17 source-verified research entries" in lower
    assert "16 exact geographic groups" in lower
    assert "42 research entries" in lower
    assert "37 exact overlap labels" in lower
    assert "crete" in lower
    assert "trinidad and tobago" in lower
    assert "iceland" in lower
    assert "samoa" in lower
    assert "lower florida keys" in lower
    assert "socotra" in lower
    assert "11 southern ocean island groups" in lower
    assert "321 flowering plant species" in lower
    assert "0/25" in lower
    assert "not_evaluable" in lower
    assert "independent-archipelago denominator" in lower

    universe = UNIVERSE.read_text(encoding="utf-8").lower()
    assert "layer d — post-freeze source-verified exact-group breadth extension" in universe
    assert "layer e — multi-group breadth context kept outside exact-group denominators" in universe
    assert "combined descriptive universe of 42 research entries" in universe
    assert "formal identifiability audit remains frozen at 25 entries" in universe
