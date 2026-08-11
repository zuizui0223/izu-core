import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "tribulus_flower_divergence",
    ROOT / "scripts" / "analyze_tribulus_flower_divergence.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_source_mapping_matches_author_readme_and_scripts():
    mapping = json.loads(
        (ROOT / "data/design/tribulus_flower_source_mapping.json").read_text(
            encoding="utf-8"
        )
    )
    assert mapping["source_rows_expected_from_readme"] == 773
    assert mapping["source_columns_expected_from_readme"] == 29
    observed = mapping["source_dimensions_observed_in_author_blob"]
    assert observed == {
        "csv_lines_including_header": 773,
        "data_rows": 772,
        "header_fields": 28,
    }
    assert "no missing row or column is reconstructed" in mapping[
        "source_dimension_discrepancy"
    ]
    assert mapping["columns"]["petal_length"].endswith("millimetres")
    assert "(1|ID)" in mapping["author_model_anchors"]["bioclimate_mixed_model"][
        "formula"
    ]
    assert mapping["author_model_anchors"]["bioclimate_mixed_model"][
        "reported_emmean_mainland_mm"
    ] == 17.3
    assert mapping["author_model_anchors"]["bioclimate_mixed_model"][
        "reported_emmean_island_mm"
    ] == 15.8


def test_source_group_normalization_is_explicit():
    assert MODULE.normalize_group(" continent ") == "continent"
    assert MODULE.normalize_group("island") == "island"
    assert MODULE.galapagos_binary("Galapagos") == "galapagos"
    assert MODULE.galapagos_binary("other") == "other_islands"
    assert MODULE.galapagos_binary("NA") is None


def test_id_level_aggregation_rejects_conflicting_source_grouping():
    pd = pytest.importorskip("pandas")
    frame = pd.DataFrame(
        {
            "ID": ["x", "x"],
            "petal_length": [10.0, 11.0],
            "mainland_island_clean": ["continent", "island"],
            "is_island": [0, 1],
            "continent_clean": ["A", "A"],
            "galapagos_binary": [None, None],
            "island_group": [None, None],
            "year_collected": [2000, 2000],
            "Bio_1": [20.0, 20.0],
            "Bio_4": [100.0, 100.0],
            "Bio_12": [500.0, 500.0],
            "Bio_15": [50.0, 50.0],
        }
    )
    with pytest.raises(ValueError, match="conflicting"):
        MODULE.id_level_frame(frame)


def test_id_level_hc3_sensitivity_uses_ID_not_flower_rows():
    pd = pytest.importorskip("pandas")
    pytest.importorskip("statsmodels")
    rows = []
    for index in range(12):
        is_island = int(index >= 6)
        for flower in range(3):
            rows.append(
                {
                    "ID": f"id{index}",
                    "petal_length": 15.0 - is_island + 0.1 * flower + 0.01 * index,
                    "mainland_island_clean": "island" if is_island else "continent",
                    "is_island": is_island,
                    "continent_clean": "A" if index % 2 == 0 else "B",
                    "galapagos_binary": "other_islands" if is_island else None,
                    "island_group": "test" if is_island else None,
                    "year_collected": 1990 + index,
                    "Bio_1": 20.0 + 0.1 * index,
                    "Bio_4": 100.0 + index,
                    "Bio_12": 500.0 + 2 * index,
                    "Bio_15": 50.0 + 0.5 * index,
                }
            )
    frame = pd.DataFrame(rows)
    IDs = MODULE.id_level_frame(frame)
    assert len(IDs) == 12
    assert set(IDs["n_flower_rows"]) == {3}
    result = MODULE.id_level_sensitivities(frame)
    assert result["n_ID_total"] == 12
    assert result["year_adjusted"]["n_ID"] == 12
    assert result["year_adjusted"]["label"] == "ID_mean_island_minus_continent"


def test_claim_boundary_never_promotes_flower_size_to_dependency():
    mapping = json.loads(
        (ROOT / "data/design/tribulus_flower_source_mapping.json").read_text(
            encoding="utf-8"
        )
    )
    claim = mapping["claim_boundary"].casefold()
    assert "do not measure effective pollinator dependency" in claim
    assert "do not identify pollinator" in claim
