from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R1 = ROOT / "data" / "design" / "chapter2_nee_r1_scope_architecture_20260913.json"


def _load() -> dict:
    return json.loads(R1.read_text(encoding="utf-8"))


def test_r1_architecture_is_frozen_without_false_site_closure() -> None:
    data = _load()
    assert data["status"] == "R1_architecture_frozen_exact_site_registry_open"
    assert data["focal_context"]["taxon"] == "Campanula microdonta"
    assert data["focal_context"]["candidate_pair_is_final_R1_site_registry"] is False
    assert data["block_architecture"]["no_fixed_final_n"] is True


def test_r1_transport_is_prospective_farfugium_not_retrospective_rescue() -> None:
    data = _load()
    transport = data["transport_context"]
    assert transport["taxon"] == "Farfugium japonicum"
    assert transport["selection_status"] == "prospectively_selected_before_focal_outcomes"
    assert "H2" in transport["P6_primary_target"]
    assert transport["same_archipelago_fallback_allowed"] is True
    assert "genuine transport challenge" in transport["same_archipelago_fallback_rule"]


def test_r1_uses_block_scale_screen_without_calling_it_power() -> None:
    data = _load()
    blocks = data["block_architecture"]
    screen = blocks["prepilot_screen_reference_only"]
    assert screen["32_blocks_low_dependence_crossover_separation"] == 0.835
    assert "not empirical power" in screen["note"]
    assert "fewer than 32" in blocks["R1_screening_floor"]
    assert "flowers, visits or SVD repeats" in blocks["R1_screening_floor"]


def test_exact_r1_closure_still_requires_real_sites_and_time_windows() -> None:
    requirements = "\n".join(_load()["exact_R1_closure_requirements"])
    assert "actual focal Campanula population/site units" in requirements
    assert "actual Farfugium transport population/site units" in requirements
    assert "time-window construction" in requirements
    assert "SVD background controls" in requirements
    assert "dependence coordinate" in requirements


def test_r1_route_logic_preserves_retreat_line_and_oikos_firewall() -> None:
    data = _load()
    route = data["route_logic"]
    assert "EL/Ecology" in route["if_focal_scope_is_strong_but_transport_context_is_not_feasible"]
    assert "H1-H4" in route["if_focal_scope_cannot_supply_independent_blocks_for_H5"]
    assert route["oikos_chapter2_effect"] == "none"
    forbidden = "\n".join(data["forbidden"])
    assert "logistically convenient" in forbidden
    assert "synthetic rho" in forbidden
    assert "preserve an NEE label" in forbidden
