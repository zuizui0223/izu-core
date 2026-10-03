import json
from copy import deepcopy
from pathlib import Path

from scripts.run_chapter2_model3e_empirical_screening import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_model3e_empirical_screening_20261003.json"
TARGETS = ROOT / "data/design/chapter2_model3e_chapter1_empirical_targets_20261003.json"
RESULT = ROOT / "data/results/chapter2_model3e_h1_h3_screening_20261003.json"


def _load():
    return (
        json.loads(DESIGN.read_text(encoding="utf-8")),
        json.loads(TARGETS.read_text(encoding="utf-8")),
    )


def test_frozen_model3e_h1_h3_screening_receipt() -> None:
    design, targets = _load()
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_frozen_before_model3e_screening"
    assert targets["status"] == "frozen_empirical_targets_before_model3e_execution"
    assert result["status"] == "complete_first_model3e_h1_h3_screening"
    assert result["held_out_H2_H4_opened"] is False
    assert result["n_parameter_sets"] == 48
    assert result["n_eligible"] == 13
    assert result["accepted_parameter_ids"] == ["p010", "p046", "p036", "p032", "p029"]
    assert result["interpretation"]["display"].startswith("not reproduced")


def test_model3e_screening_runner_smoke() -> None:
    design, targets = _load()
    design = deepcopy(design)
    design["search"]["n_parameter_sets"] = 1
    design["common_operator"]["years"] = 12
    design["pseudo_islands"]["terminal_window_years"] = 4
    design["pseudo_islands"]["distances"] = [0.0, 1.5, 3.0]
    design["pseudo_islands"]["history_seeds"] = [81201]
    result = run(design, targets)
    assert result["n_parameter_sets"] == 1
    assert result["held_out_H2_H4_opened"] is False
