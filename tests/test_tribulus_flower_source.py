import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "tribulus_flower_source",
    ROOT / "scripts" / "audit_tribulus_flower_source.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_literal_role_matching_does_not_invent_semantics():
    headers = ["Habitat", "Petal_Length", "Population", "RandomNumeric"]
    roles = MODULE.role_matches(headers)
    assert roles["island_continent"] == ["Habitat"]
    assert roles["petal_length"] == ["Petal_Length"]
    assert roles["population"] == ["Population"]
    assert "RandomNumeric" not in sum(roles.values(), [])


def test_column_summary_preserves_low_cardinality_values():
    rows = [
        {"Habitat": "Island"},
        {"Habitat": "Island"},
        {"Habitat": "Continent"},
        {"Habitat": ""},
    ]
    summary = MODULE.column_summary("Habitat", rows)
    assert summary["n_present"] == 3
    assert summary["n_missing"] == 1
    assert summary["distinct_value_counts"] == {"Island": 2, "Continent": 1}


def test_numeric_summary_is_descriptive_only():
    rows = [{"x": "1"}, {"x": "2.5"}, {"x": "NA"}, {"x": ""}]
    summary = MODULE.column_summary("x", rows)
    assert summary["numeric_fraction_present"] == 2 / 3
    assert summary["numeric_min"] == 1.0
    assert summary["numeric_max"] == 2.5


def test_config_locks_raw_flower_filename_and_doi():
    import json

    config = json.loads(
        (ROOT / "config" / "tribulus_dryad_source.json").read_text(encoding="utf-8")
    )
    assert config["dataset_doi"] == "10.5061/dryad.h70rxwdnz"
    assert config["analysis_filename"] == "Tribulus_flower_data_clean.csv"
    assert "effective pollinator dependency" in config["claim_boundary"]
