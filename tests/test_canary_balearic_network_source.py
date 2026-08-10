import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "audit_canary_balearic_network_source.py"
SPEC = importlib.util.spec_from_file_location("canary_balearic_audit", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_long_interaction_table_requires_plant_visitor_and_weight():
    headers = [
        "community",
        "island",
        "archipelago",
        "plant species",
        "flower visitor",
        "visit frequency",
        "sampling hours",
    ]
    record = MODULE.classify_table(
        Path("interactions.csv"),
        None,
        headers,
        [["site_a", "island_a", "Canary", "P1", "B1", 3, 10]],
        100,
        len(headers),
        ",",
    )
    assert record["long_interaction_candidate"] is True
    assert record["community_metadata_candidate"] is True
    assert record["wide_interaction_matrix_candidate"] is False


def test_metric_table_requires_community_or_island_identity():
    headers = [
        "network",
        "island type",
        "connectance",
        "nestedness",
        "interaction diversity",
    ]
    record = MODULE.classify_table(
        Path("metrics.docx"),
        "table_1",
        headers,
        [["site_a", "oceanic", 0.3, 22.0, 1.8]],
        5,
        len(headers),
        None,
    )
    assert record["network_metric_table_candidate"] is True
    assert record["community_metadata_candidate"] is True


def test_numeric_matrix_is_candidate_not_confirmed_network():
    headers = ["plant species", "visitor_a", "visitor_b", "visitor_c"]
    sample = [
        ["P1", 1, 0, 3],
        ["P2", 0, 2, 0],
        ["P3", 4, 1, 0],
    ]
    record = MODULE.classify_table(
        Path("matrix.xlsx"), "Canary_1", headers, sample, 4, 4, None
    )
    assert record["wide_interaction_matrix_candidate"] is True
    assert record["long_interaction_candidate"] is False
    assert record["sample_numeric_fraction_after_first_column"] == 1.0


def test_generic_numeric_table_without_plant_axis_is_not_matrix():
    headers = ["metric", "community_1", "community_2", "community_3"]
    record = MODULE.classify_table(
        Path("summary.xlsx"),
        "summary",
        headers,
        [["connectance", 0.2, 0.3, 0.4]],
        2,
        4,
        None,
    )
    assert record["wide_interaction_matrix_candidate"] is False


def test_schema_roles_do_not_include_effectiveness_or_dependency():
    roles = MODULE.role_matches(
        ["community", "plant", "pollinator", "interaction count"]
    )
    assert set(roles) == set(MODULE.ROLE_ALIASES)
    assert "effectiveness" not in roles
    assert "dependency" not in roles
