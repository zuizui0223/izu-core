import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "audit_galapagos_dryad_schema.py"
SPEC = importlib.util.spec_from_file_location("galapagos_schema", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_long_edge_and_island_covariate_tables_are_separate():
    edge = MODULE.classify_table(
        path=Path("edges.csv"),
        sheet=None,
        headers=["island", "plant species", "pollinator species", "visit count"],
        sample_rows=[["A", "P1", "B1", 3], ["B", "P2", "B2", 2]],
        n_rows=3,
        n_columns=4,
        delimiter=",",
    )
    assert edge["long_edge_list_candidate"] is True
    assert edge["island_covariate_candidate"] is False

    covariates = MODULE.classify_table(
        path=Path("islands.csv"),
        sheet=None,
        headers=["island", "area", "isolation distance", "geological age"],
        sample_rows=[["A", 10, 100, 2.5], ["B", 20, 50, 1.5]],
        n_rows=3,
        n_columns=4,
        delimiter=",",
    )
    assert covariates["island_covariate_candidate"] is True
    assert covariates["long_edge_list_candidate"] is False


def test_wide_matrix_requires_explicit_orientation_for_analysis():
    unresolved = MODULE.classify_table(
        path=Path("Santa_Cruz.csv"),
        sheet=None,
        headers=["taxon", "bee 1", "bee 2", "fly 1"],
        sample_rows=[["P1", 1, 0, 3], ["P2", 0, 2, 1]],
        n_rows=3,
        n_columns=4,
        delimiter=",",
    )
    assert unresolved["wide_numeric_matrix_candidate"] is True
    assert unresolved["matrix_orientation"] == "unresolved"
    assert unresolved["analysis_admissible_matrix"] is False

    oriented = MODULE.classify_table(
        path=Path("Santa_Cruz.csv"),
        sheet=None,
        headers=["plant species", "bee 1", "bee 2", "fly 1"],
        sample_rows=[["P1", 1, 0, 3], ["P2", 0, 2, 1]],
        n_rows=3,
        n_columns=4,
        delimiter=",",
    )
    assert oriented["matrix_orientation"] == "plants_by_pollinators"
    assert oriented["analysis_admissible_matrix"] is True


def test_sampling_effort_is_a_separate_schema_role():
    record = MODULE.classify_table(
        path=Path("effort.csv"),
        sheet=None,
        headers=["island", "sampling hours", "survey date"],
        sample_rows=[["A", 12, "2010-01-01"]],
        n_rows=2,
        n_columns=3,
        delimiter=",",
    )
    assert record["sampling_effort_candidate"] is True
    assert record["long_edge_list_candidate"] is False
