import csv
from pathlib import Path

import pytest

from scripts.analyze_tribulus_flower_context import (
    aggregate_ids,
    analyse,
    ols_group_coefficient,
    read_rows,
)


def synthetic_rows():
    rows = []
    index = 1
    groups = [
        ("C1", "continent", "", "", 20.0, 1950, 20, 100, 1000, 50),
        ("C2", "continent", "", "", 18.0, 1960, 21, 110, 900, 55),
        ("O1", "island", "other", "OtherA", 17.0, 1955, 22, 120, 800, 60),
        ("O2", "island", "other", "OtherB", 16.0, 1965, 23, 130, 700, 65),
        ("G1", "island", "galapagos", "Galapagos", 9.0, 1970, 24, 140, 600, 70),
        ("G2", "island", "galapagos", "Galapagos", 8.0, 1980, 25, 150, 500, 75),
    ]
    for identifier, island, gal, group, petal, year, b1, b4, b12, b15 in groups:
        for offset in (-0.2, 0.2):
            rows.append(
                {
                    "ind_num": index,
                    "ID": identifier,
                    "petal_length": petal + offset,
                    "year_collected": float(year),
                    "mainland_island": island,
                    "galapagos_other": gal,
                    "island_group": group,
                    "Bio_1": float(b1),
                    "Bio_4": float(b4),
                    "Bio_12": float(b12),
                    "Bio_15": float(b15),
                }
            )
            index += 1
    return rows


def test_aggregate_ids_does_not_treat_flowers_as_independent():
    ids = aggregate_ids(synthetic_rows())
    assert len(ids) == 6
    assert all(row["n_flowers"] == 2 for row in ids)
    assert next(row for row in ids if row["ID"] == "G1")["petal_length"] == pytest.approx(9.0)


def test_adjusted_model_returns_group_coefficient_on_specimen_ids():
    ids = aggregate_ids(synthetic_rows())
    # Use only year in this tiny synthetic panel to avoid a deliberately
    # collinear climate design.
    coefficient, n = ols_group_coefficient(
        ids,
        group_key="mainland_island",
        exposed_value="island",
        reference_value="continent",
        covariates=("year_collected",),
    )
    assert n == 6
    assert coefficient < 0


def test_full_audit_separates_galapagos_from_other_islands():
    # Build a larger panel with deterministic nonlinear specimen-by-replicate
    # perturbations.  Pure replicate offsets can remain exact linear combinations
    # of the original synthetic climate columns after ID aggregation, so they do
    # not actually test the full adjusted audit.
    rows = []
    base = synthetic_rows()
    for replicate in range(4):
        for source in base:
            row = dict(source)
            specimen = int(source["ind_num"])
            interaction = replicate * ((specimen % 7) + 1)
            row["ID"] = f"{source['ID']}_{replicate}"
            row["ind_num"] = specimen + 100 * replicate
            row["year_collected"] = (
                float(source["year_collected"])
                + replicate
                + 0.013 * interaction
            )
            row["Bio_1"] = (
                float(source["Bio_1"])
                + (replicate % 2) * 0.7
                + 0.017 * (replicate ** 2) * ((specimen % 5) + 1)
            )
            row["Bio_4"] = (
                float(source["Bio_4"])
                + replicate * 2.3
                + (specimen % 2)
                + 0.031 * interaction
            )
            row["Bio_12"] = (
                float(source["Bio_12"])
                - replicate * 13
                + (specimen % 3)
                + 0.047 * (replicate ** 2) * ((specimen % 4) + 1)
            )
            row["Bio_15"] = (
                float(source["Bio_15"])
                + replicate * 1.7
                + (specimen % 5)
                - 0.029 * interaction
            )
            rows.append(row)
    result = analyse(rows, repetitions=200)
    contrasts = {row["contrast"]: row for row in result["contrasts"]}
    assert result["n_measurement_rows"] == len(rows)
    assert result["n_specimen_ids"] == 24
    assert contrasts["galapagos_vs_other_islands"]["raw_mean_difference"] < 0
    assert contrasts["other_islands_vs_continents"]["raw_mean_difference"] < 0
    assert result["effect_registry_eligible"] is False
    assert result["causal_claim_allowed"] is False


def test_csv_reader_requires_source_hierarchy_and_climate_columns(tmp_path: Path):
    path = tmp_path / "flowers.csv"
    headers = [
        "ind_num",
        "ID",
        "year_collected",
        "mainland_island",
        "galapagos_other",
        "island_group",
        "petal_length",
        "Bio_1",
        "Bio_4",
        "Bio_12",
        "Bio_15",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerow(
            {
                "ind_num": 1,
                "ID": "A",
                "year_collected": 1950,
                "mainland_island": "continent",
                "galapagos_other": "NA",
                "island_group": "NA",
                "petal_length": 10,
                "Bio_1": 20,
                "Bio_4": 100,
                "Bio_12": 900,
                "Bio_15": 50,
            }
        )
    rows = read_rows(path)
    assert len(rows) == 1
    assert rows[0]["mainland_island"] == "continent"
