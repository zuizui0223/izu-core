import json
from copy import deepcopy
from pathlib import Path

from scripts.run_chapter2_deterministic_backbone_depression_sensitivity import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_deterministic_backbone_depression_sensitivity_20261002.json"
PARENT = ROOT / "data/design/model3_ch2_bridge_20260927.json"
RESULT = ROOT / "data/results/chapter2_deterministic_backbone_depression_sensitivity_20261002.json"


def _load():
    return (
        json.loads(DESIGN.read_text(encoding="utf-8")),
        json.loads(PARENT.read_text(encoding="utf-8")),
        json.loads(RESULT.read_text(encoding="utf-8")),
    )


def test_frozen_backbone_depression_sensitivity_receipt() -> None:
    design, parent, result = _load()
    assert design["status"] == "prospective_frozen_before_execution"
    assert parent["base_config"]["depression"] == 0.5
    assert result["status"] == "complete_prospective_deterministic_backbone_depression_sensitivity"
    assert result["backbone_mean_direction_robust"] is True
    assert result["uniform_history_direction_robust"] is False
    assert result["sign_reversal_at_depression_0.75"] is False
    assert result["conditional_uniformity_at_depression_0.75"] is True
    reports = {r["depression"]: r for r in result["reports"]}
    assert reports[0.25]["negative_only_histories_eps0"] == 128
    assert reports[0.5]["negative_only_histories_eps0"] == 128
    assert reports[0.75]["mixed_histories_eps0"] == 11
    assert reports[0.75]["positive_only_histories_eps0"] == 1
    assert all(r["overall_mean_effect"] < 0 for r in reports.values())
    assert all(all(v < 0 for v in r["mean_effect_by_start"].values()) for r in reports.values())


def test_backbone_depression_runner_smoke() -> None:
    design, parent, _ = _load()
    parent = deepcopy(parent)
    parent["history_seeds"] = parent["history_seeds"][:1]
    parent["starts"] = [0.5]
    shard = deepcopy(design)
    shard["intervention"]["depression"] = [0.75]
    result = run(shard, parent)
    assert result["n_density_trajectories"] == 2
    assert len(result["reports"]) == 1
