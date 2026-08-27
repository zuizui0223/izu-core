from __future__ import annotations

import numpy as np
import pandas as pd

from analyze_izu_signed_position_tm_response import _fit_clustered, site_metrics


def test_site_metrics_do_not_double_weight_seasons() -> None:
    raw = pd.DataFrame(
        {
            "siteid": [1, 1, 1, 4],
            "season": [1, 2, 3, 1],
            "plant": ["Plant a", "Plant a", "Plant a", "Plant a"],
            "tube": [10.0, 10.0, 10.0, 11.0],
            "TM_sp": [1.0, 2.0, 3.0, 4.0],
        }
    )
    result = site_metrics(raw)
    mainland = result.loc[result["site"].eq("hitachi")].iloc[0]
    assert mainland["tube"] == 10.0
    assert mainland["TM"] == 2.0
    assert mainland["n_seasons"] == 3


def test_clustered_fit_recovers_positive_geometry_with_island_offsets() -> None:
    rows = []
    for plant_index in range(12):
        plant = f"p{plant_index}"
        for island_index, island in enumerate(["oshima", "niijima", "kozu"]):
            predicted = -2.0 + plant_index * 0.4 + island_index * 0.1
            delta = 1.75 * predicted + {"oshima": -1.0, "niijima": 0.5, "kozu": 1.2}[island]
            delta += (plant_index % 3 - 1) * 0.02
            rows.append(
                {
                    "plant": plant,
                    "island": island,
                    "predicted_matching_change_mm": predicted,
                    "delta_TM_sp": delta,
                }
            )
    fit = _fit_clustered(pd.DataFrame(rows))
    assert fit["positive_direction"] is True
    assert np.isclose(fit["slope"], 1.75, atol=0.03)
    assert fit["p_two_sided"] < 0.001
