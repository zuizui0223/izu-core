import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "data/results/hawaii_lobelioid_controlled_dependency_named_source_check.json"
BUFFER_GATE = ROOT / "data/design/buffer_mechanism_discriminator_gate.json"
PRIORITY = ROOT / "data/design/system_agnostic_buffer_closure_priority.json"


def test_exact_taxon_historical_assurance_narrows_candidate_without_admission():
    data = json.loads(CHECK.read_text(encoding="utf-8"))
    assert data["decision"] == "named_sources_strengthen_exact_taxon_autonomous_assurance_candidate_but_same_context_numeric_dependency_gate_remains_open"
    assert data["abm_buffer_mechanism_admission"] is False
    overlaps = set()
    for source in data["sources_checked"]:
        overlaps.update(source.get("exact_2026_focal_taxon_overlap", []))
    assert "Clermontia lindseyana" in overlaps
    assert "Clermontia pyrularia" in overlaps
    assert "Cyanea shipmanii" not in overlaps


def test_buffer_gate_stays_closed_but_hawaii_candidate_is_source_supported():
    gate = json.loads(BUFFER_GATE.read_text(encoding="utf-8"))
    assert gate["summary"]["buffer_mechanism_ready_for_abm_admission"] == 0
    assert gate["summary"]["exact_taxon_historical_assurance_candidate"] == "hawaii_lobelioid_post_extinction_pollination_2026"
    hawaii = next(row for row in gate["systems"] if row["system_id"] == "hawaii_lobelioid_post_extinction_pollination_2026")
    assert hawaii["state"] == "exact_taxon_historical_assurance_candidate_found_same_context_numeric_dependency_still_missing"
    assert hawaii["named_source_check"] == "data/results/hawaii_lobelioid_controlled_dependency_named_source_check.json"


def test_hawaii_remains_rank_one_but_repeat_search_is_closed():
    priority = json.loads(PRIORITY.read_text(encoding="utf-8"))
    hawaii = priority["priorities"][0]
    assert hawaii["rank"] == 1
    assert hawaii["system_id"] == "hawaii_lobelioid_post_extinction_pollination_2026"
    assert "historical exact-taxon assurance support is available" in hawaii["current_block"]
    assert "do not repeat broad historical assurance searches" in hawaii["repeat_search_rule"]
