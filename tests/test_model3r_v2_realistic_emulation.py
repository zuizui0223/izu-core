import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pytest

from scripts.model3r_v2_realistic_emulator import _prepare_world, _summary, run_search

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_model3r_v2_empirical_emulation_20261003.json"
TARGET = ROOT / "data/design/chapter1_corrected_empirical_emulation_targets_20261003.json"
SAMPLE = ROOT / "data/input/chapter1_corrected_covariate_sample_512_20261003.csv"


def _load():
    return (
        json.loads(DESIGN.read_text(encoding="utf-8")),
        json.loads(TARGET.read_text(encoding="utf-8")),
    )


def test_model3r_v2_uses_corrected_current_chapter1_and_real_covariates() -> None:
    design, target = _load()
    assert design["status"] == "prospective_model3r_v2_design_frozen_before_fit"
    assert target["status"] == "current_corrected_chapter1_empirical_target_frozen_for_model3r_v2"
    assert target["population"]["island_universe"] == 8264
    assert SAMPLE.exists()
    world = _prepare_world(design, mode="preflight")
    assert len(world["cov"]) == 128
    assert world["lineages_per_island"] == 4


def test_model3r_v2_midpoint_smoke_is_finite() -> None:
    design, _ = _load()
    bounds = design["stage1_search"]["bounds"]
    params = {k: float(np.mean(v)) for k, v in bounds.items()}
    world = _prepare_world(design, mode="preflight")
    summary = _summary(world, params)
    assert np.isfinite(summary["H3_pollen_limitation_isolation_beta"])
    assert np.isfinite(summary["H4_assurance_to_pollen_limitation_beta"])
    assert np.isfinite(summary["H4_generalization_to_pollen_limitation_beta"])
    assert set(summary["context_stats"]) == set(design["empirical_covariates"]["controls"]) or len(summary["context_stats"]) == 4


@pytest.mark.skipif(sys.version_info[:2] != (3, 11), reason="frozen Model3R-v2 64-draw preflight runs once on Python 3.11")
def test_model3r_v2_frozen_realistic_preflight() -> None:
    design, target = _load()
    spec = design["stage1_search"]
    result = run_search(
        design,
        target,
        mode="preflight",
        draws=int(spec["preflight_draws"]),
        seed=int(spec["seed"]),
    )
    assert result["status"] == "complete_model3r_v2_realistic_search"
    assert result["draws"] == 64
    assert result["islands"] == 128
    assert result["lineages_per_island"] == 4
    warnings.warn(
        "MODEL3R_V2_PREFLIGHT "
        + json.dumps(
            {
                "passes": result["passes"],
                "best": [
                    {
                        "draw": x["draw"],
                        "params": x["params"],
                        "score": x["score"],
                        "summary": x["summary"],
                    }
                    for x in result["best"][:3]
                ],
            },
            sort_keys=True,
        )
    )
