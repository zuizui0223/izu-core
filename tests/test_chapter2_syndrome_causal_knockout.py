import json
from pathlib import Path

from scripts.run_chapter2_syndrome_causal_knockout import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_syndrome_causal_knockout_20261002.json"


def test_prospectively_frozen_syndrome_causal_knockout() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_frozen_before_execution"
    assert design["operator"]["operator_changes_allowed"] is False
    assert design["operator"]["new_trait_axes_allowed"] is False

    result = run(design)

    # These are the prospectively declared scientific predictions. A failure is
    # a scientific result; do not relax these assertions after inspecting output.
    assert result["route_A_supported"] is True
    assert result["route_B_supported"] is True
    assert result["stage_B_trait_accessibility_allowed"] is True
