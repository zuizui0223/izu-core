import json
from copy import deepcopy
from pathlib import Path

from scripts.run_chapter2_route_A_robustness_surface import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_route_A_robustness_surface_20261002.json"
RESULT = ROOT / "data/results/chapter2_route_A_robustness_surface_20261002.json"


def test_frozen_route_A_robustness_falsification_receipt() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_frozen_before_execution"
    assert result["status"] == "complete_prospective_route_A_robustness_falsification"
    assert result["surface"]["surface_nonisolated"] is True
    assert result["surface"]["central_contiguous"] is False
    assert result["life_history_propagation"] is False
    assert result["route_A_robust"] is False
    assert result["headline_decision"] == "drop_route_A_from_headline_retain_as_model_conditional_SI"


def test_route_A_robustness_runner_smoke() -> None:
    design = deepcopy(json.loads(DESIGN.read_text(encoding="utf-8")))
    design["fixed_surface"]["activities"] = [0.05, 0.1]
    design["fixed_surface"]["fixed_assurance"] = [0.5]
    design["fixed_surface"]["investment_cost"] = [0.5]
    design["fixed_surface"]["inbreeding_depression"] = [0.5]
    design["trajectory_check"]["activities"] = [0.05]
    design["trajectory_check"]["inbreeding_depression"] = [0.5]
    design["trajectory_check"]["demographic_replicates"] = [501]
    design["trajectory_check"]["life_histories"] = {
        "annual": design["trajectory_check"]["life_histories"]["annual"]
    }
    result = run(design)
    assert len(result["surface_rows"]) == 2
    assert len(result["trajectory_rows"]) == 1
