import json
from copy import deepcopy
from pathlib import Path

from scripts.run_chapter2_investment_mutation_rescue_diagnostic import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_investment_mutation_rescue_diagnostic_20261002.json"
RESULT = ROOT / "data/results/chapter2_investment_mutation_rescue_diagnostic_20261002.json"


def test_frozen_investment_mutation_rescue_receipt() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_diagnostic_frozen_before_execution"
    assert result["status"] == "complete_prospective_investment_mutation_rescue_diagnostic"
    assert result["n_trajectories"] == 128
    assert result["decisions"] == {
        "standing_variation_bottleneck": True,
        "de_novo_mutation_rescue": True,
        "finite_establishment_bottleneck": True,
    }
    assert result["contrasts"]["standing_variation_effect"] > result["contrasts"]["mutation_rescue_effect"] > 0
    assert 0 < result["contrasts"]["capacity_modulation_of_mutation_rescue"] < result["contrasts"]["mutation_rescue_effect"]


def test_investment_mutation_rescue_runner_smoke() -> None:
    design = deepcopy(json.loads(DESIGN.read_text(encoding="utf-8")))
    design["baseline"]["years"] = 5
    design["baseline"]["founder_seeds"] = [77301]
    design["baseline"]["demographic_seeds"] = [401]
    design["baseline"]["visitor_histories"] = {"left4": [0.15, 0.25, 0.35, 0.45]}
    design["factors"]["capacity"] = [48]
    result = run(design)
    assert result["n_trajectories"] == 4
    assert len(result["cell_summary"]) == 4
