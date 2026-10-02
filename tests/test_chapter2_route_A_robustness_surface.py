import json
import warnings
from pathlib import Path

from scripts.run_chapter2_route_A_robustness_surface import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_route_A_robustness_surface_20261002.json"


def test_prospectively_frozen_route_A_robustness_surface() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_frozen_before_execution"

    result = run(design)

    # This is a falsification gate, not a preferred-outcome gate.
    assert result["headline_decision"] in {
        "retain_route_A_as_headline_model_mechanism",
        "drop_route_A_from_headline_retain_as_model_conditional_SI",
    }
    warnings.warn(
        "ROUTE_A_ROBUSTNESS_NUMERIC "
        + json.dumps(
            {
                "surface_diagnostics": result["surface_diagnostics"],
                "life_history_activity_0_05": result["life_history_activity_0_05"],
                "life_history_propagation": result["life_history_propagation"],
                "route_A_robust": result["route_A_robust"],
                "headline_decision": result["headline_decision"],
            },
            sort_keys=True,
        )
    )
