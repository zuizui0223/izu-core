import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "analyze_ogasawara_network_context.py"
SPEC = importlib.util.spec_from_file_location("ogasawara_context", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def candidate(path: Path):
    return {
        "file": str(path),
        "sheet": None,
        "delimiter": ",",
        "role_matches": {
            "island": ["island"],
            "site": ["site"],
            "season": ["month"],
            "habitat": ["habitat"],
            "anole_context": ["green anole context"],
            "plant": ["plant species"],
            "pollinator": ["pollinator species"],
            "interaction_count": ["legitimate interaction count"],
        },
        "contextual_long_network_candidate": True,
    }


def test_source_resolved_rows_and_network_metrics(tmp_path: Path):
    table = tmp_path / "network.csv"
    table.write_text(
        "island,site,month,habitat,green anole context,plant species,pollinator species,legitimate interaction count\n"
        "Chichi,A,May,natural,present,P1,B1,4\n"
        "Chichi,A,May,natural,present,P1,B2,2\n"
        "Haha,B,May,natural,absent,P1,B1,1\n"
        "Haha,B,May,natural,absent,P2,B3,3\n",
        encoding="utf-8",
    )
    rows, columns = MODULE.standardize_rows(candidate(table))
    assert len(rows) == 4
    assert columns["interaction_count"] == "legitimate interaction count"
    metrics = MODULE.grouped_metrics(rows, ("island",))
    assert {row["island"] for row in metrics} == {"Chichi", "Haha"}
    pairs, plant_rows = MODULE.island_pair_summaries(rows)
    assert len(pairs) == 1
    assert pairs[0]["n_shared_plants"] == 1
    assert {row["plant_name"] for row in plant_rows} == {"P1"}


def test_source_native_n_int_header_is_accepted(tmp_path: Path):
    table = tmp_path / "network.csv"
    table.write_text(
        "island,plant species,pollinator species,N.Int\nI,P,B,3\n",
        encoding="utf-8",
    )
    record = candidate(table)
    record["role_matches"]["interaction_count"] = ["N.Int"]
    rows, columns = MODULE.standardize_rows(record)
    assert columns["interaction_count"] == "N.Int"
    assert len(rows) == 1
    assert rows[0]["interaction_count"] == 3.0


def test_generic_count_header_is_not_promoted_to_legitimate_interaction(tmp_path: Path):
    table = tmp_path / "network.csv"
    table.write_text("island,plant,pollinator,count\nI,P,B,1\n", encoding="utf-8")
    record = candidate(table)
    record["role_matches"]["interaction_count"] = ["count"]
    try:
        MODULE.standardize_rows(record)
    except ValueError as error:
        assert "too generic" in str(error)
    else:
        raise AssertionError("generic count header should be blocked")


def test_generic_n_header_is_not_promoted_to_legitimate_interaction(tmp_path: Path):
    table = tmp_path / "network.csv"
    table.write_text("island,plant,pollinator,N\nI,P,B,1\n", encoding="utf-8")
    record = candidate(table)
    record["role_matches"]["interaction_count"] = ["N"]
    try:
        MODULE.standardize_rows(record)
    except ValueError as error:
        assert "too generic" in str(error)
    else:
        raise AssertionError("generic N header should be blocked")


def test_write_csv_unions_heterogeneous_context_columns(tmp_path: Path):
    output = tmp_path / "context.csv"
    MODULE.write_csv(
        output,
        [
            {"island": "I", "season": "May", "metric": 1},
            {"island": "I", "habitat": "Natural", "metric": 2},
        ],
    )
    with output.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    assert reader.fieldnames == ["island", "season", "metric", "habitat"]
    assert rows[0]["season"] == "May"
    assert rows[0]["habitat"] == ""
    assert rows[1]["season"] == ""
    assert rows[1]["habitat"] == "Natural"


def test_multiple_candidate_tables_remain_blocked_by_main_gate(tmp_path: Path, monkeypatch):
    schema = tmp_path / "schema.json"
    first = candidate(tmp_path / "a.csv")
    second = candidate(tmp_path / "b.csv")
    schema.write_text(json.dumps({"tables": [first, second], "claim_boundary": "guard"}), encoding="utf-8")
    output = tmp_path / "out"
    monkeypatch.setattr(
        "sys.argv",
        ["analyze", "--schema", str(schema), "--output-dir", str(output)],
    )
    MODULE.main()
    result = json.loads((output / "analysis_blocked.json").read_text())
    assert result["status"] == "blocked_schema_not_uniquely_resolved"
    assert result["n_contextual_long_candidates"] == 2
