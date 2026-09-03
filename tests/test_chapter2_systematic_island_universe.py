import json
from pathlib import Path

from scripts.audit_chapter2_systematic_island_universe import build_audit

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/chapter2_systematic_island_universe_audit_v1_20260903.json"


def test_systematic_island_universe_matches_frozen_audit():
    computed = build_audit()
    frozen = json.loads(RESULT.read_text(encoding="utf-8"))
    assert computed == frozen
    assert computed["target_rows"] == 110
    assert computed["macroregions"] == 8
    assert computed["resolved_or_umbrella_indexed_targets_after_first_wave"] == 49
    assert computed["targets_requiring_further_source_work_after_first_wave"] == 61
    assert computed["directly_not_yet_source_gated_after_first_wave"] == 55
    assert computed["source_found_needing_ledger_gate_after_first_wave"] == 1


def test_systematic_universe_does_not_redefine_frozen_chapter2_denominators():
    computed = build_audit()
    boundary = computed["claim_boundary"].lower()
    assert "frozen 25-entry identifiability denominator" in boundary
    assert "current 36-entry descriptive confrontation" in boundary
    assert "first-wave eligibility is not promotion" in boundary
    assert "overlap/de-duplication" in boundary


def test_first_wave_source_gate_is_explicit_and_bounded():
    computed = build_audit()
    gate = computed["first_wave_source_gate"]
    assert gate["gated_targets"] == 7
    assert gate["eligible_for_breadth_after_dedup_review"] == 6
    assert gate["retain_search_record_not_confrontation"] == 1
    assert gate["full_chapter2_contract_passes"] == 0
    assert gate["newly_source_resolved_targets"] == 7


def test_high_priority_search_pool_is_explicit():
    computed = build_audit()
    assert computed["priority_counts"]["high"] == 37
    assert computed["seed_coverage_status_counts"]["source_found_needs_ledger_gate"] == 7
    assert computed["seed_coverage_status_counts"]["umbrella_source_verified"] == 11
    assert computed["nested_targets_needing_specific_gate"] == 5
