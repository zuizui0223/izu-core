import json
from pathlib import Path

from scripts.audit_chapter2_world_breadth_extension import build_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_world_breadth_extension_audit_20260903.json"
DOC = ROOT / "docs/CHAPTER2_WORLD_BREADTH_EXTENSION_20260903.md"
UNIVERSE = ROOT / "docs/COMPARATIVE_ISLAND_SYSTEM_UNIVERSE_20260827.md"


def test_world_breadth_extension_matches_deterministic_audit():
    computed = build_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["frozen_identifiability_denominator"]["research_entries"] == 25
    assert computed["frozen_identifiability_denominator"]["geographic_overlap_labels"] == 21
    assert computed["post_freeze_extension"]["research_entries"] == 10
    assert computed["post_freeze_extension"]["exact_geographic_groups"] == 9
    assert computed["combined_descriptive_universe"]["research_entries_before_cross_layer_deduplication"] == 35
    assert computed["combined_descriptive_universe"]["exact_overlap_labels_before_higher_level_archipelago_deduplication"] == 30
    assert computed["combined_descriptive_universe"]["independent_archipelago_denominator_claimed"] is False


def test_extension_strengthens_arrival_axis_without_reopening_prediction_gate():
    payload = build_audit()
    extension = payload["post_freeze_extension"]
    assert extension["direct_or_historical_arrival_entries"] == 3
    assert set(extension["direct_or_historical_arrival_ids"]) == {
        "new_caledonia_kato_kawakita_2004",
        "fiji_braunsapis_invasion_2015",
        "french_polynesia_apid_origins_2017",
    }
    assert extension["full_chapter2_contract_passes"] == 0
    assert payload["frozen_identifiability_denominator"]["formal_external_prediction_reopened"] is False
    assert payload["frozen_identifiability_denominator"]["frozen_25_recomputed"] is False


def test_world_breadth_documentation_keeps_denominators_separate():
    text = DOC.read_text(encoding="utf-8")
    lower = text.lower()
    assert "25 research entries" in lower
    assert "10 source-verified research entries" in lower
    assert "9 exact geographic groups" in lower
    assert "35 research entries" in lower
    assert "30 exact overlap labels" in lower
    assert "new caledonia" in lower
    assert "fiji" in lower
    assert "french polynesia" in lower
    assert "0/25" in lower
    assert "not_evaluable" in lower
    assert "independent-archipelago denominator" in lower

    universe = UNIVERSE.read_text(encoding="utf-8").lower()
    assert "layer d — post-freeze source-verified breadth extension" in universe
    assert "combined descriptive universe of 35 research entries" in universe
    assert "formal identifiability audit remains frozen at 25 entries" in universe
