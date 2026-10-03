import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pytest

from scripts.model3r_empirical_emulator import run_search, simulate_summary

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_model3r_empirical_emulation_20261003.json"
TARGET = ROOT / "data/design/chapter1_empirical_emulation_targets_20261003.json"


def _load():
    return (
        json.loads(DESIGN.read_text(encoding="utf-8")),
        json.loads(TARGET.read_text(encoding="utf-8")),
    )


def test_model3r_empirical_target_is_external_and_frozen() -> None:
    design, target = _load()
    assert design["status"] == "prospective_model3r_emulation_design_frozen_before_fit"
    assert target["status"] == "external_empirical_target_frozen_before_model3r_fit"
    assert target["source_repository"] == "zuizui0223/island"
    assert target["source_repository_head"] == "625c1e4ea67daa4b9d447807d5d049e7254843f9"
    assert design["holdout_targets"]["H1"] == [
        "four context-specific colour-dulling isolation slopes"
    ]


def test_model3r_single_parameter_smoke_is_finite() -> None:
    design, _ = _load()
    bounds = design["fit_strategy"]["stage_1_parameter_search"]["shared_parameter_bounds"]
    params = {k: float(np.mean(v)) for k, v in bounds.items()}
    summary = simulate_summary(design, params)
    assert np.isfinite(summary["H3_pollen_limitation_isolation_beta"])
    assert np.isfinite(summary["H4_assurance_to_pollen_limitation_beta"])
    assert np.isfinite(summary["H4_generalization_to_pollen_limitation_beta"])
    assert set(summary["context_stats"]) == set(design["environment"]["contexts"])


@pytest.mark.skipif(sys.version_info[:2] != (3, 11), reason="frozen 64-draw empirical preflight runs once on Python 3.11")
def test_model3r_frozen_empirical_preflight() -> None:
    design, target = _load()
    search = design["fit_strategy"]["stage_1_parameter_search"]
    result = run_search(
        design,
        target,
        draws=int(search["preflight_draws"]),
        seed=int(search["seed"]),
    )
    assert result["status"] == "complete_model3r_deterministic_preflight"
    assert result["draws"] == 64
    warnings.warn(
        "MODEL3R_PREFLIGHT "
        + json.dumps(
            {
                "passes": result["passes"],
                "best": [
                    {
                        "draw": x["draw"],
                        "params": x["params"],
                        "score": x["score"],
                        "H3": x["summary"]["H3_pollen_limitation_isolation_beta"],
                        "H4a": x["summary"]["H4_assurance_to_pollen_limitation_beta"],
                        "H4g": x["summary"]["H4_generalization_to_pollen_limitation_beta"],
                        "context_stats": x["summary"]["context_stats"],
                    }
                    for x in result["best"][:3]
                ],
            },
            sort_keys=True,
        )
    )
