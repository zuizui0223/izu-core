import json
from pathlib import Path

import numpy as np

from scripts.model3r_v2_realistic_emulator import _prepare_world, _summary

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_model3r_v2_empirical_emulation_20261003.json"
TARGET = ROOT / "data/design/chapter1_corrected_empirical_emulation_targets_20261003.json"
RESULT = ROOT / "data/results/chapter2_model3r_v2_empirical_preflight_20261003.json"
SAMPLE = ROOT / "data/input/chapter1_corrected_covariate_sample_512_20261003.csv"


def _load():
    return (
        json.loads(DESIGN.read_text(encoding="utf-8")),
        json.loads(TARGET.read_text(encoding="utf-8")),
        json.loads(RESULT.read_text(encoding="utf-8")),
    )


def test_model3r_v2_failure_is_frozen_on_corrected_target() -> None:
    design, target, result = _load()
    assert design["status"] == "prospective_model3r_v2_design_frozen_before_fit"
    assert target["population"]["island_universe"] == 8264
    assert result["status"] == "complete_prospective_model3r_v2_preflight_failure"
    assert result["passes"] == 0
    assert result["decision"].startswith("do_not_expand_v2_search")
    assert SAMPLE.exists()


def test_model3r_v2_midpoint_smoke_is_finite() -> None:
    design, _, _ = _load()
    bounds = design["stage1_search"]["bounds"]
    params = {k: float(np.mean(v)) for k, v in bounds.items()}
    world = _prepare_world(design, mode="preflight")
    summary = _summary(world, params)
    assert len(world["cov"]) == 128
    assert np.isfinite(summary["H3_pollen_limitation_isolation_beta"])
    assert np.isfinite(summary["H4_assurance_to_pollen_limitation_beta"])
    assert np.isfinite(summary["H4_generalization_to_pollen_limitation_beta"])
