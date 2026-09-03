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
    assert computed["resolved_or_umbrella_indexed_targets"] == 42
    assert computed["targets_requiring_further_source_work"] == 68
    assert computed["directly_not_yet_source_gated"] == 56


def test_systematic_universe_does_not_redefine_frozen_chapter2_denominators():
    computed = build_audit()
    boundary = computed["claim_boundary"].lower()
    assert "frozen 25-entry identifiability denominator" in boundary
    assert "current 36-entry descriptive confrontation" in boundary
    assert "source verification" in boundary
    assert "overlap/de-duplication" in boundary


def test_high_priority_search_pool_is_explicit():
    computed = build_audit()
    assert computed["priority_counts"]["high"] == 37
    assert computed["coverage_status_counts"]["source_found_needs_ledger_gate"] == 7
    assert computed["coverage_status_counts"]["umbrella_source_verified"] == 11
    assert computed["coverage_status_counts"]["nested_target_needs_specific_gate"] == 5
