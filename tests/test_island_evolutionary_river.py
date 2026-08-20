from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_island_evolutionary_river.py"


def load_module():
    spec = importlib.util.spec_from_file_location("island_evolutionary_river_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_visualization_uses_locked_v4_gradient_and_v6_support_strengths():
    module = load_module()
    svg, sidecar = module.build()
    frozen = json.loads(module.V4_RESULT.read_text())
    assert sidecar["frozen_v4_gradient"] == frozen["gradient"]
    assert sidecar["v6_support_strengths"] == [0.0, 0.25, 0.5, 0.75]
    assert "island feasible opportunity" in svg
    assert "local partner availability" in svg
    assert "realized weighted architecture" in svg


def test_visualization_is_state_space_not_agent_animation_or_chronology():
    module = load_module()
    svg, sidecar = module.build()
    assert sidecar["agent_animation"] is False
    assert sidecar["chronological_reconstruction"] is False
    assert "not chronological time" in svg
    assert "not an ABM agent animation" in svg
    assert "unavailable / excluded by current island-scale constraint" in svg


def test_river_narrows_with_frozen_partner_opportunity():
    module = load_module()
    _, sidecar = module.build()
    partner_types = [float(row["final_partner_types"]) for row in sidecar["frozen_v4_gradient"]]
    assert all(left >= right for left, right in zip(partner_types, partner_types[1:]))
    assert partner_types[0] > partner_types[-1]


def test_menorca_amplitudes_do_not_control_geometry():
    module = load_module()
    _, sidecar = module.build()
    assert sidecar["menorca_amplitudes_used_in_geometry"] is False
    assert sidecar["sources"]["empirical_falsification_marker"] == "PR #195, qualitative marker only"


def test_svg_has_accessible_title_and_description():
    module = load_module()
    svg, _ = module.build()
    assert '<svg xmlns="http://www.w3.org/2000/svg" role="img"' in svg
    assert "<title>Island Evolutionary River</title>" in svg
    assert "<desc>" in svg
