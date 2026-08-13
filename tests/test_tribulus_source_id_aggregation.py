from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

from scripts import analyze_tribulus_flower_context_idaware as context
from scripts import analyze_tribulus_flower_divergence_idaware as divergence


ROOT = Path(__file__).resolve().parents[1]


def test_divergence_id_aggregation_averages_environment_but_not_broad_strata():
    frame = pd.DataFrame(
        [
            {
                "ID": "SITE1",
                "petal_length": 8.0,
                "mainland_island_clean": "island",
                "is_island": 1,
                "continent_clean": "north america",
                "galapagos_binary": "other",
                "island_group": "Jamaica",
                "year_collected": 2001.0,
                "Bio_1": 20.0,
                "Bio_4": 100.0,
                "Bio_12": 900.0,
                "Bio_15": 50.0,
            },
            {
                "ID": "SITE1",
                "petal_length": 10.0,
                "mainland_island_clean": "island",
                "is_island": 1,
                "continent_clean": "north america",
                "galapagos_binary": "other",
                "island_group": "West Indies",
                "year_collected": 2001.0,
                "Bio_1": 22.0,
                "Bio_4": 104.0,
                "Bio_12": 920.0,
                "Bio_15": 54.0,
            },
        ]
    )
    row = divergence.id_level_frame(frame).iloc[0]
    assert row["petal_length"] == pytest.approx(9.0)
    assert row["Bio_1"] == pytest.approx(21.0)
    assert row["Bio_12"] == pytest.approx(910.0)
    assert row["island_group"] == "<mixed:Jamaica|West Indies>"

    broken = frame.copy()
    broken.loc[1, "galapagos_binary"] = "galapagos"
    with pytest.raises(ValueError, match="model-defining galapagos_binary"):
        divergence.id_level_frame(broken)


def test_context_id_aggregation_does_not_coerce_mixed_island_group():
    rows = [
        {
            "ID": "SITE1",
            "petal_length": 8.0,
            "mainland_island": "island",
            "galapagos_other": "other",
            "island_group": "Jamaica",
            "year_collected": 2001.0,
            "Bio_1": 20.0,
            "Bio_4": 100.0,
            "Bio_12": 900.0,
            "Bio_15": 50.0,
        },
        {
            "ID": "SITE1",
            "petal_length": 10.0,
            "mainland_island": "island",
            "galapagos_other": "other",
            "island_group": "West Indies",
            "year_collected": 2001.0,
            "Bio_1": 22.0,
            "Bio_4": 104.0,
            "Bio_12": 920.0,
            "Bio_15": 54.0,
        },
    ]
    record = context.aggregate_ids(rows)[0]
    assert record["petal_length"] == pytest.approx(9.0)
    assert record["Bio_1"] == pytest.approx(21.0)
    assert record["island_group"] == ""
    assert record["island_group_ambiguous"] is True
    assert record["island_group_source_values"] == ["Jamaica", "West Indies"]

    broken = [dict(row) for row in rows]
    broken[1]["mainland_island"] = "continent"
    with pytest.raises(ValueError, match="conflicting mainland_island"):
        context.aggregate_ids(broken)


@pytest.mark.parametrize(
    "script_name",
    [
        "analyze_tribulus_flower_divergence_idaware.py",
        "analyze_tribulus_flower_context_idaware.py",
    ],
)
def test_idaware_entrypoints_are_directly_executable(script_name: str):
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script_name), "--help"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "usage:" in completed.stdout.lower()
