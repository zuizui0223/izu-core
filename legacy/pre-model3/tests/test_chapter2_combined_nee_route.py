from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUPERSESSION = ROOT / "docs/CHAPTER2_COMBINED_NEE_SUPERSESSION_20260913.md"
GATE = ROOT / "data/design/chapter2_natural_regime_admission_gate_20260913.json"


def test_combined_route_explicitly_supersedes_lane_separation_without_erasing_scientific_boundaries() -> None:
    text = SUPERSESSION.read_text(encoding="utf-8")
    lower = text.lower()
    assert "supersedes" in lower
    assert "chapter2_submission_route_firewall_20260912.md" in lower
    assert "synthetic `k≈4` is **not** a natural richness threshold" in text
    assert "2026-09-27" in text
    assert "nee route" in lower
    assert "ecology letters route" in lower
    assert "fallback route" in lower


def test_natural_regime_gate_is_frozen_and_outcome_blind() -> None:
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    assert gate["status"] == "frozen_before_candidate_extraction"
    assert gate["hard_stop_date_asia_tokyo"] == "2026-09-27"
    requirements = gate["hard_admission_requirements"]
    assert requirements["minimum_aligned_time_bins"] == 6
    assert requirements["minimum_nonconstant_partner_series"] == 3
    assert requirements["outcome_data_required"] is False
    boundaries = " ".join(gate["nonnegotiable_boundaries"]).lower()
    assert "do not map natural partner richness" in boundaries
    assert "do not use reproductive or performance outcomes" in boundaries


def test_route_decision_has_predeclared_failure_and_promotion_paths() -> None:
    route = json.loads(GATE.read_text(encoding="utf-8"))["route_decision"]
    assert set(route) == {"fallback_Oikos_plus_EL", "NEE_candidate", "Ecology_Letters_combined"}
    nee = route["NEE_candidate"]
    assert nee["minimum_admitted_island_systems"] == 12
    assert nee["minimum_independent_source_studies"] == 3
    assert nee["minimum_island_or_archipelago_groups"] == 2
    robustness = nee["source_robustness"].lower()
    assert "largest source study" in robustness
    assert "leav" in robustness
