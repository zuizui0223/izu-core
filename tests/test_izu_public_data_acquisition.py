import csv
import gzip
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "acquire_izu_public_data.py"
SPEC = importlib.util.spec_from_file_location("_izu_public_data", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
extract = MODULE.extract


def _write(
    path: Path,
    fields: list[str],
    rows: list[dict[str, str]],
    compressed: bool = False,
) -> None:
    opener = gzip.open if compressed else open
    with opener(path, "wt", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_extracts_only_frozen_izu_islands(tmp_path: Path) -> None:
    species_path = tmp_path / "species.csv.gz"
    effort_path = tmp_path / "effort.csv"
    output_dir = tmp_path / "out"
    _write(
        species_path,
        [
            "island_id",
            "species",
            "n_records",
            "n_unique_gbif_ids",
            "basis_of_record_set",
            "review_status",
        ],
        [
            {
                "island_id": "gshhg_2.3.7_h_3f48d601bf60ade348ae",
                "species": "Alpha beta",
                "n_records": "2",
                "n_unique_gbif_ids": "2",
                "basis_of_record_set": "HUMAN_OBSERVATION",
                "review_status": "unresolved_taxonomy",
            },
            {
                "island_id": "gshhg_2.3.7_h_80bd057071c9043cebcc",
                "species": "Alpha beta",
                "n_records": "1",
                "n_unique_gbif_ids": "1",
                "basis_of_record_set": "PRESERVED_SPECIMEN",
                "review_status": "unresolved_taxonomy",
            },
            {
                "island_id": "gshhg_2.3.7_h_80bd057071c9043cebcc",
                "species": "Gamma delta",
                "n_records": "3",
                "n_unique_gbif_ids": "3",
                "basis_of_record_set": "HUMAN_OBSERVATION",
                "review_status": "unresolved_taxonomy",
            },
            {
                "island_id": "outside",
                "species": "Ignore me",
                "n_records": "9",
                "n_unique_gbif_ids": "9",
                "basis_of_record_set": "HUMAN_OBSERVATION",
                "review_status": "unresolved_taxonomy",
            },
        ],
        compressed=True,
    )
    _write(
        effort_path,
        ["island_id", "n_records", "n_species", "n_datasets"],
        [
            {
                "island_id": "gshhg_2.3.7_h_3f48d601bf60ade348ae",
                "n_records": "3",
                "n_species": "1",
                "n_datasets": "1",
            },
            {
                "island_id": "gshhg_2.3.7_h_80bd057071c9043cebcc",
                "n_records": "4",
                "n_species": "2",
                "n_datasets": "2",
            },
        ],
    )

    summary = extract(
        species_path,
        effort_path,
        output_dir,
        {"repository": "example/source", "commit": "abc"},
    )

    assert summary["n_island_species_pairs"] == 3
    assert summary["n_unique_species_labels"] == 2
    assert summary["n_records_in_species_rows"] == 6
    assert summary["n_records_in_effort_table"] == 7
    assert summary["n_records_not_assigned_to_retained_species_rows"] == 1
    assert (output_dir / "izu_island_species.csv.gz").exists()
    with (output_dir / "izu_species_incidence.csv").open(
        encoding="utf-8",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))
    alpha = next(row for row in rows if row["species"] == "Alpha beta")
    assert alpha["n_islands"] == "2"
    assert "Izu Oshima" in alpha["islands"]
    assert "Niijima" in alpha["islands"]
