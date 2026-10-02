import json
import sys
import warnings
from copy import deepcopy
from pathlib import Path

from scripts.run_chapter2_deterministic_backbone_depression_sensitivity import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_deterministic_backbone_depression_sensitivity_20261002.json"
PARENT = ROOT / "data/design/model3_ch2_bridge_20260927.json"

SHARD_BY_PYTHON = {
    (3, 10): 0.25,
    (3, 11): 0.50,
    (3, 12): 0.75,
}


def _load():
    return (
        json.loads(DESIGN.read_text(encoding="utf-8")),
        json.loads(PARENT.read_text(encoding="utf-8")),
    )


def test_backbone_depression_design_is_frozen() -> None:
    design, parent = _load()
    assert design["status"] == "prospective_frozen_before_execution"
    assert design["intervention"]["depression"] == [0.25, 0.5, 0.75]
    assert design["model"] == "deterministic genotype-density only"
    assert parent["base_config"]["depression"] == 0.5


def test_prospective_deterministic_backbone_depression_shard() -> None:
    design, parent = _load()
    depression = SHARD_BY_PYTHON[sys.version_info[:2]]
    shard = deepcopy(design)
    shard["intervention"]["depression"] = [depression]
    result = run(shard, parent)

    assert result["n_density_trajectories"] == 128 * 3 * 2
    assert len(result["reports"]) == 1
    report = result["reports"][0]
    assert report["depression"] == depression
    warnings.warn(
        "BACKBONE_DEPRESSION_SHARD "
        + json.dumps(
            {
                "python": f"{sys.version_info.major}.{sys.version_info.minor}",
                "depression": depression,
                "report": report,
            },
            sort_keys=True,
        )
    )


def test_backbone_depression_runner_smoke() -> None:
    design, parent = _load()
    parent = deepcopy(parent)
    parent["history_seeds"] = parent["history_seeds"][:1]
    parent["starts"] = [0.5]
    shard = deepcopy(design)
    shard["intervention"]["depression"] = [0.5]
    result = run(shard, parent)
    assert result["n_density_trajectories"] == 1 * 1 * 1 * 2
    assert len(result["reports"]) == 1
