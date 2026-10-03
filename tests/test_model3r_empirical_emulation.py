import json
from pathlib import Path

import numpy as np

from scripts.model3r_empirical_emulator import simulate_summary

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_model3r_empirical_emulation_20261003.json"
TARGET = ROOT / "data/design/chapter1_empirical_emulation_targets_20261003.json"
RESULT = ROOT / "data/results/chapter2_model3r_v1_empirical_preflight_20261003.json"


def _load():
    return (
        json.loads(DESIGN.read_text(encoding="utf-8")),
        json.loads(TARGET.read_text(encoding="utf-8")),
        json.loads(RESULT.read_text(encoding="utf-8")),
    )


def test_model3r_v1_empirical_failure_is_frozen() -> None:
    design, target, result = _load()
    assert design["status"] == "prospective_model3r_emulation_design_frozen_before_fit"
    assert target["status"] == "external_empirical_target_frozen_before_model3r_fit"
    assert result["status"] == "complete_prospective_model3r_v1_preflight_failure"
    assert result["passes"] == 0
    assert result["decision"].startswith("do_not_expand_v1_parameter_search")


def test_model3r_v1_single_parameter_smoke_is_finite() -> None:
    design, _, _ = _load()
    bounds = design["fit_strategy"]["stage_1_parameter_search"]["shared_parameter_bounds"]
    params = {k: float(np.mean(v)) for k, v in bounds.items()}
    summary = simulate_summary(design, params)
    assert np.isfinite(summary["H3_pollen_limitation_isolation_beta"])
    assert np.isfinite(summary["H4_assurance_to_pollen_limitation_beta"])
    assert np.isfinite(summary["H4_generalization_to_pollen_limitation_beta"])
