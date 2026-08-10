import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "audit_southwest_pacific_pair_schema.py"
SPEC = importlib.util.spec_from_file_location("southwest_pair_schema", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_wide_pair_table_requires_island_and_mainland_values():
    record = MODULE.classify(
        Path("pairs.xlsx"),
        "Data",
        [
            "comparison id",
            "archipelago",
            "island species",
            "mainland species",
            "floral trait",
            "unit",
            "island value",
            "mainland value",
            "pollination mode",
        ],
        [[1, "Fiji", "A", "B", "flower size", "mm", 10, 12, "animal"]],
        130,
        9,
        None,
    )
    assert record["paired_wide_candidate"] is True
    assert record["quantitative_pair_candidate"] is True
    assert record["moderator_table_candidate"] is True


def test_long_pair_table_is_detected_but_not_promoted_without_trait_or_unit():
    record = MODULE.classify(
        Path("long.csv"),
        None,
        ["pair id", "island-mainland", "trait value", "pollination system"],
        [[1, "island", 10, "animal"], [1, "mainland", 12, "animal"]],
        3,
        4,
        ",",
    )
    assert record["paired_long_candidate"] is True
    assert record["quantitative_pair_candidate"] is False


def test_p_values_or_moderators_alone_are_not_quantitative_pair_data():
    record = MODULE.classify(
        Path("summary.csv"),
        None,
        ["archipelago", "pollination mode", "p value"],
        [["Fiji", "animal", 0.04]],
        2,
        3,
        ",",
    )
    assert record["moderator_table_candidate"] is True
    assert record["paired_wide_candidate"] is False
    assert record["paired_long_candidate"] is False
    assert record["quantitative_pair_candidate"] is False


def test_uncertainty_and_sample_size_are_tracked_separately():
    record = MODULE.classify(
        Path("effects.csv"),
        None,
        [
            "comparison id",
            "trait",
            "unit",
            "island value",
            "mainland value",
            "sample size",
            "standard error",
        ],
        [[1, "flower size", "mm", 10, 12, 20, 1.2]],
        2,
        7,
        ",",
    )
    assert record["quantitative_pair_candidate"] is True
    assert record["contains_sample_size_field"] is True
    assert record["contains_uncertainty_field"] is True
