import json
import sys
import warnings
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.run_chapter2_deterministic_backbone_depression_sensitivity import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_deterministic_backbone_depression_sensitivity_20261002.json"
PARENT = ROOT / "data/design/model3_ch2_bridge_20260927.json"


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


@pytest.mark.skipif(sys.version_info[:2] != (3, 11), reason="full prospective density sensitivity runs once on Python 3.11")
def test_prospective_deterministic_backbone_depression_sensitivity() -> None:
    design, parent = _load()
    result = run(design, parent)

    # Preferred outcome is not enforced. This test exposes the frozen result;
    # the preregistered reporting_action determines how the manuscript changes.
    assert result["n_density_trajectories"] == 3 * 128 * 3 * 2
    assert result["reporting_action"] in {
        "retain_uniform_negative_backbone_within_tested_depression_envelope",
        "qualify_backbone_direction_as_inbreeding_depression_dependent",
        "retain_negative_mean_but_drop_uniform_one_directional_backbone_claim",
    }
    warnings.warn(
        "BACKBONE_DEPRESSION_NUMERIC "
        + json.dumps(
            {
                "reports": result["reports"],
                "backbone_robust": result["backbone_robust"],
                "sign_reversal_at_depression_0_75": result["sign_reversal_at_depression_0_75"],
                "conditional_uniformity_at_depression_0_75": result["conditional_uniformity_at_depression_0_75"],
                "reporting_action": result["reporting_action"],
            },
            sort_keys=True,
        )
    )


def test_backbone_depression_runner_smoke() -> None:
    design, parent = _load()
    parent = deepcopy(parent)
    parent["history_seeds"] = parent["history_seeds"][:1]
    parent["starts"] = [0.5]
    result = run(design, parent)
    assert result["n_density_trajectories"] == 3 * 1 * 1 * 2
    assert len(result["reports"]) == 3
