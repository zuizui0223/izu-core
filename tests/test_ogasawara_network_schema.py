import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "audit_ogasawara_network_schema.py"
SPEC = importlib.util.spec_from_file_location("ogasawara_schema", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_contextual_long_table_is_detected_without_biological_relabelling():
    headers = [
        "island",
        "site",
        "month",
        "habitat type",
        "green anole presence",
        "plant species",
        "pollinator species",
        "legitimate interaction count",
    ]
    record = MODULE.table_record(Path("network.csv"), None, headers, 100, len(headers), ",")
    assert record["long_network_candidate"] is True
    assert record["contextual_long_network_candidate"] is True
    assert record["role_matches"]["anole_context"] == ["green anole presence"]


def test_wide_matrix_remains_a_candidate_not_a_confirmed_network():
    headers = ["plant species", "Apis mellifera", "small bees", "flies"]
    record = MODULE.table_record(Path("matrix.xlsx"), "May", headers, 20, 4, None)
    assert record["long_network_candidate"] is False
    assert record["wide_interaction_matrix_candidate"] is True


def test_interaction_headers_do_not_create_effectiveness_or_dependency_roles():
    roles = MODULE.map_fields(["plant", "pollinator", "visit count"])
    assert set(roles) == set(MODULE.ALIASES)
    assert "effectiveness" not in roles
    assert "dependency" not in roles
