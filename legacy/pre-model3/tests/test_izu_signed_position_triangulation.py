from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "analyze_izu_signed_position_triangulation.py"
SPEC = importlib.util.spec_from_file_location("izu_signed_position", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_aggregate_plant_site_deduplicates_seasons() -> None:
    frame = pd.DataFrame(
        {
            "siteid": [1, 1, 4, 4],
            "season": [1, 2, 1, 2],
            "plant": ["Plant a", "Plant a", "Plant a", "Plant a"],
            "tube": [5.0, 5.0, 5.5, 5.5],
            "TM_sp": [-2.0, -1.0, -0.5, 0.5],
        }
    )
    result = MODULE.aggregate_plant_site(frame)
    assert len(result) == 2
    mainland = result.loc[result["site"].eq("hitachi")].iloc[0]
    assert mainland["tube"] == pytest.approx(5.0)
    assert mainland["TM_sp"] == pytest.approx(-1.5)
    assert mainland["n_seasons"] == 2


def test_aggregate_plant_site_rejects_tube_change_within_site() -> None:
    frame = pd.DataFrame(
        {
            "siteid": [1, 1],
            "season": [1, 2],
            "plant": ["Plant a", "Plant a"],
            "tube": [5.0, 6.0],
            "TM_sp": [-2.0, -1.0],
        }
    )
    with pytest.raises(ValueError, match="tube is not fixed"):
        MODULE.aggregate_plant_site(frame)


def test_center_geometry_positive_signal_survives_clustered_fit() -> None:
    source_center = 5.0
    centers = {"island_a": 3.0, "island_b": 4.0}
    rows = []
    for index in range(12):
        plant = f"Plant {index:02d}"
        tube = 1.0 + index * 0.7
        rows.append({"plant": plant, "site": "source", "tube": tube, "TM_sp": 0.0, "n_seasons": 1})
        for site, offset in [("island_a", 0.25), ("island_b", -0.15)]:
            position = tube - source_center
            shift = centers[site] - source_center
            predicted = abs(position) - abs(position - shift)
            rows.append(
                {
                    "plant": plant,
                    "site": site,
                    "tube": tube,
                    "TM_sp": 1.8 * predicted + offset,
                    "n_seasons": 1,
                }
            )
    frame = pd.DataFrame(rows)
    projection = MODULE.build_projection_rows(
        frame,
        source_sites=["source"],
        source_center_mm=source_center,
        target_sites=["island_a", "island_b"],
        site_centers_mm=centers,
    )
    fit = MODULE.fit_clustered_island_fe(projection)
    assert projection["plant"].nunique() == 12
    assert fit["slope"] == pytest.approx(1.8, abs=1e-10)
    assert fit["p_one_sided_positive"] < 1e-8
    sign = MODULE.sign_concordance(projection)
    assert sign["fraction"] > 0.9


def test_center_geometry_is_signed_not_unsigned() -> None:
    frame = pd.DataFrame(
        [
            {"plant": "left", "site": "source", "tube": 4.0, "TM_sp": 0.0, "n_seasons": 1},
            {"plant": "right", "site": "source", "tube": 6.0, "TM_sp": 0.0, "n_seasons": 1},
            {"plant": "left", "site": "island", "tube": 4.0, "TM_sp": 0.0, "n_seasons": 1},
            {"plant": "right", "site": "island", "tube": 6.0, "TM_sp": 0.0, "n_seasons": 1},
        ]
    )
    projection = MODULE.build_projection_rows(
        frame,
        source_sites=["source"],
        source_center_mm=5.0,
        target_sites=["island"],
        site_centers_mm={"island": 4.0},
    ).set_index("plant")
    assert projection.loc["left", "initial_signed_position_mm"] == pytest.approx(-1.0)
    assert projection.loc["right", "initial_signed_position_mm"] == pytest.approx(1.0)
    assert projection.loc["left", "predicted_matching_change_mm"] > 0
    assert projection.loc["right", "predicted_matching_change_mm"] < 0
    assert not np.isclose(
        projection.loc["left", "predicted_matching_change_mm"],
        projection.loc["right", "predicted_matching_change_mm"],
    )
