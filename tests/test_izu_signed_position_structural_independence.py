from __future__ import annotations

import pandas as pd

from audit_izu_signed_position_structural_independence import (
    aggregate_site,
    fit_island_fe,
)


def test_aggregate_site_keeps_raw_and_corrected_targets_distinct() -> None:
    raw = pd.DataFrame(
        {
            "siteid": [1, 1, 4, 4],
            "season": [1, 2, 1, 2],
            "plant": ["Plant a"] * 4,
            "tube": [5.0, 5.0, 6.0, 6.0],
            "TM_sp": [-4.0, -2.0, -1.0, -3.0],
            "TM_sp_z": [1.0, 3.0, -2.0, 2.0],
        }
    )
    result = aggregate_site(raw)
    mainland = result.loc[result["site"].eq("hitachi")].iloc[0]
    island = result.loc[result["site"].eq("oshima")].iloc[0]
    assert mainland["TM_sp"] == -3.0
    assert mainland["TM_sp_z"] == 2.0
    assert island["TM_sp"] == -2.0
    assert island["TM_sp_z"] == 0.0


def test_island_fe_can_separate_geometry_from_island_offsets() -> None:
    rows = []
    for plant_index in range(10):
        for island_index, island in enumerate(["oshima", "niijima", "kozu"]):
            x = -1.5 + 0.3 * plant_index + 0.05 * island_index
            y = 1.25 * x + {"oshima": -2.0, "niijima": 0.5, "kozu": 1.5}[island]
            y += (plant_index % 2) * 0.01
            rows.append(
                {
                    "plant": f"p{plant_index}",
                    "island": island,
                    "predicted_matching_change_mm": x,
                    "delta_TM_sp_raw": y,
                }
            )
    fit = fit_island_fe(
        pd.DataFrame(rows), "delta_TM_sp_raw", "predicted_matching_change_mm"
    )
    assert abs(fit["slope"] - 1.25) < 0.03
    assert fit["p_one_sided_positive_t"] < 0.001
