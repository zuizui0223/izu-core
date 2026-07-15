import csv
import gzip
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "acquire_supplemental_izu_gbif.py"
SPEC = importlib.util.spec_from_file_location("_supplemental_izu_gbif", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_point_in_ring() -> None:
    ring = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0), (0.0, 0.0)]
    assert MODULE._point_in_ring(1.0, 1.0, ring)
    assert not MODULE._point_in_ring(3.0, 1.0, ring)


def test_scaffold_exposes_three_supplemental_targets() -> None:
    lock = MODULE._read_json(ROOT / "config" / "izu_supplemental_gbif_source.json")
    targets = MODULE._scaffold_targets(
        ROOT / "data" / "design" / "izu_regime_scaffold.csv",
        set(lock["targets_from_scaffold"]),
    )
    assert [row["unit_id"] for row in targets] == [
        "toshima",
        "shikinejima",
        "aogashima",
    ]


def test_aggregate_records_keeps_effort_separate_from_species_rows() -> None:
    records = [
        {
            "key": 1,
            "species": "Alpha beta",
            "speciesKey": 10,
            "basisOfRecord": "HUMAN_OBSERVATION",
            "datasetKey": "dataset-a",
            "year": 2020,
            "coordinateUncertaintyInMeters": 20,
        },
        {
            "key": 2,
            "species": "Alpha beta",
            "speciesKey": 10,
            "basisOfRecord": "PRESERVED_SPECIMEN",
            "datasetKey": "dataset-b",
            "year": 1990,
        },
        {
            "key": 3,
            "scientificName": "Unresolved record",
            "basisOfRecord": "HUMAN_OBSERVATION",
            "datasetKey": "dataset-a",
        },
    ]
    rows, effort = MODULE.aggregate_records("test", "Test Island", records)

    assert effort["n_records"] == 3
    assert effort["n_species"] == 2
    alpha = next(row for row in rows if row["species"] == "Alpha beta")
    assert alpha["n_records"] == 2
    assert alpha["n_unique_gbif_ids"] == 2
    assert alpha["year_min"] == 1990
    assert alpha["year_max"] == 2020


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]], compressed: bool = False) -> None:
    opener = gzip.open if compressed else open
    with opener(path, "wt", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_combines_six_and_supplemental_islands(tmp_path: Path) -> None:
    six = tmp_path / "six"
    output = tmp_path / "out"
    six.mkdir()
    _write_csv(
        six / "izu_island_species.csv.gz",
        ["island_id", "island_name", "species", "n_records", "n_unique_gbif_ids", "basis_of_record_set", "review_status"],
        [{
            "island_id": "oshima",
            "island_name": "Izu Oshima",
            "species": "Alpha beta",
            "n_records": 2,
            "n_unique_gbif_ids": 2,
            "basis_of_record_set": "HUMAN_OBSERVATION",
            "review_status": "unresolved_taxonomy",
        }],
        compressed=True,
    )
    _write_csv(
        six / "izu_island_effort.csv",
        ["island_id", "island_name", "n_records", "n_species"],
        [{"island_id": "oshima", "island_name": "Izu Oshima", "n_records": 2, "n_species": 1}],
    )
    supplemental_species = [{
        "island_id": "toshima",
        "island_name": "Toshima",
        "species_key": "10",
        "species": "Alpha beta",
        "n_records": 1,
        "n_unique_gbif_ids": 1,
        "basis_of_record_set": "PRESERVED_SPECIMEN",
        "dataset_key_set": "dataset-a",
        "establishment_means_set": "",
        "year_min": 2000,
        "year_max": 2000,
        "review_status": "occurrence_candidate_unreviewed",
    }]
    supplemental_effort = [{
        "island_id": "toshima",
        "island_name": "Toshima",
        "n_records": 1,
        "n_species": 1,
        "acquisition_source": "gbif_live_polygon_search",
    }]

    summary = MODULE.combine_with_six_islands(
        six,
        supplemental_species,
        supplemental_effort,
        output,
    )
    assert summary["n_islands"] == 2
    assert summary["n_unique_species_labels"] == 1
    assert summary["n_records"] == 3
    assert (output / "izu_9island_species.csv.gz").exists()
