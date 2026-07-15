#!/usr/bin/env python3
"""Acquire and extract the pinned six-island Izu public-data snapshot.

The upstream files are occurrence-derived products from the global ``island``
repository. This script downloads exactly one immutable commit, retains only the
six frozen Izu island IDs, and writes small auditable products for ``izu-core``.
It does not promote occurrence labels to a reviewed native flora.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import shutil
import tempfile
import urllib.request
from itertools import combinations
from pathlib import Path
from typing import Iterable

IZU_ISLANDS = {
    "gshhg_2.3.7_h_3f48d601bf60ade348ae": "Izu Oshima",
    "gshhg_2.3.7_h_80bd057071c9043cebcc": "Niijima",
    "gshhg_2.3.7_h_ab48ddfcdcd4ccc62870": "Kozushima",
    "gshhg_2.3.7_h_cc2a3ac665156bf28969": "Miyakejima",
    "gshhg_2.3.7_h_78b9099b78b447bab1fd": "Mikurajima",
    "gshhg_2.3.7_h_79143661e5762bf8fa25": "Hachijojima",
}


def _integer(value: str | None) -> int:
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


def _raw_url(repository: str, commit: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{repository}/{commit}/{path}"


def _download(url: str, destination: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "izu-core-public-data-acquisition/1.0"},
    )
    with urllib.request.urlopen(request, timeout=180) as response, destination.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def _reader(path: Path) -> Iterable[dict[str, str]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


def _write_csv(
    path: Path,
    fields: list[str],
    rows: Iterable[dict[str, object]],
    gzip_output: bool = False,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    opener = gzip.open if gzip_output else open
    with opener(path, "wt", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def extract(
    species_path: Path,
    effort_path: Path,
    output_dir: Path,
    provenance: dict[str, object],
) -> dict[str, object]:
    species_rows: list[dict[str, object]] = []
    island_species: dict[str, set[str]] = {name: set() for name in IZU_ISLANDS.values()}
    incidence: dict[str, dict[str, object]] = {}

    for row in _reader(species_path):
        island_id = row.get("island_id", "")
        if island_id not in IZU_ISLANDS:
            continue
        species = (row.get("species") or "").strip()
        if not species:
            continue
        island_name = IZU_ISLANDS[island_id]
        n_records = _integer(row.get("n_records"))
        n_unique = _integer(row.get("n_unique_gbif_ids"))
        retained = {
            "island_id": island_id,
            "island_name": island_name,
            "species": species,
            "n_records": n_records,
            "n_unique_gbif_ids": n_unique,
            "basis_of_record_set": row.get("basis_of_record_set", ""),
            "review_status": row.get("review_status", ""),
        }
        species_rows.append(retained)
        island_species[island_name].add(species)
        record = incidence.setdefault(
            species,
            {
                "species": species,
                "islands": set(),
                "n_records": 0,
                "n_unique_gbif_ids": 0,
            },
        )
        record["islands"].add(island_name)  # type: ignore[index]
        record["n_records"] = int(record["n_records"]) + n_records
        record["n_unique_gbif_ids"] = int(record["n_unique_gbif_ids"]) + n_unique

    species_rows.sort(key=lambda row: (str(row["island_name"]), str(row["species"])))

    effort_rows: list[dict[str, object]] = []
    for row in _reader(effort_path):
        island_id = row.get("island_id", "")
        if island_id not in IZU_ISLANDS:
            continue
        retained: dict[str, object] = {
            "island_id": island_id,
            "island_name": IZU_ISLANDS[island_id],
        }
        for key, value in row.items():
            if key == "island_id":
                continue
            retained[key] = value
        effort_rows.append(retained)
    effort_rows.sort(key=lambda row: str(row["island_name"]))

    incidence_rows: list[dict[str, object]] = []
    for species, record in sorted(incidence.items()):
        islands = sorted(record["islands"])  # type: ignore[arg-type]
        incidence_rows.append(
            {
                "species": species,
                "n_islands": len(islands),
                "islands": "|".join(islands),
                "n_records": record["n_records"],
                "n_unique_gbif_ids": record["n_unique_gbif_ids"],
            }
        )

    pair_rows: list[dict[str, object]] = []
    for first, second in combinations(sorted(IZU_ISLANDS.values()), 2):
        first_set = island_species[first]
        second_set = island_species[second]
        union = first_set | second_set
        pair_rows.append(
            {
                "island_a": first,
                "island_b": second,
                "n_a": len(first_set),
                "n_b": len(second_set),
                "n_shared": len(first_set & second_set),
                "jaccard": len(first_set & second_set) / len(union) if union else 0.0,
            }
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(
        output_dir / "izu_island_species.csv.gz",
        [
            "island_id",
            "island_name",
            "species",
            "n_records",
            "n_unique_gbif_ids",
            "basis_of_record_set",
            "review_status",
        ],
        species_rows,
        gzip_output=True,
    )
    effort_fields = list(effort_rows[0]) if effort_rows else ["island_id", "island_name"]
    _write_csv(output_dir / "izu_island_effort.csv", effort_fields, effort_rows)
    _write_csv(
        output_dir / "izu_species_incidence.csv",
        ["species", "n_islands", "islands", "n_records", "n_unique_gbif_ids"],
        incidence_rows,
    )
    _write_csv(
        output_dir / "izu_pairwise_jaccard.csv",
        ["island_a", "island_b", "n_a", "n_b", "n_shared", "jaccard"],
        pair_rows,
    )

    effort_ids = {str(row["island_id"]) for row in effort_rows}
    records_in_species_rows = sum(int(row["n_records"]) for row in species_rows)
    records_in_effort_table = sum(
        _integer(str(row.get("n_records", 0))) for row in effort_rows
    )
    summary = {
        "schema_version": "1.1",
        "scope": "six frozen exact-island Izu pilot polygons",
        "source": provenance,
        "n_islands_expected": len(IZU_ISLANDS),
        "n_islands_with_effort_rows": len(effort_ids),
        "missing_island_ids": sorted(set(IZU_ISLANDS) - effort_ids),
        "n_island_species_pairs": len(species_rows),
        "n_unique_species_labels": len(incidence_rows),
        "n_records_in_effort_table": records_in_effort_table,
        "n_records_in_species_rows": records_in_species_rows,
        "n_records_not_assigned_to_retained_species_rows": (
            records_in_effort_table - records_in_species_rows
        ),
        "n_species_on_all_six_islands": sum(
            int(row["n_islands"]) == 6 for row in incidence_rows
        ),
        "n_single_island_species_labels": sum(
            int(row["n_islands"]) == 1 for row in incidence_rows
        ),
        "island_rows": [
            {
                "island_name": row["island_name"],
                "n_records": _integer(str(row.get("n_records", 0))),
                "n_species": _integer(str(row.get("n_species", 0))),
                "n_datasets": _integer(str(row.get("n_datasets", 0))),
            }
            for row in effort_rows
        ],
        "limitations": [
            "Occurrence-based species labels are not a reviewed native flora.",
            "Cultivated, introduced, transient, and taxonomically unresolved records may remain.",
            "Toshima, Shikinejima, and Aogashima require a supplemental exact-polygon acquisition.",
            "Presence records do not measure pollinator dependence, floral evolution, or pollination service.",
            "The effort total can exceed the sum of retained species rows when records lack a retained non-empty species label or are excluded upstream from the species aggregation.",
        ],
    }
    (output_dir / "izu_public_data_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "SOURCE_PROVENANCE.json").write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return summary


def acquire(
    source_lock: Path,
    output_dir: Path,
    cache_dir: Path | None = None,
) -> dict[str, object]:
    lock = json.loads(source_lock.read_text(encoding="utf-8"))
    repository = str(lock["source_repository"])
    commit = str(lock["source_commit"])
    species_entry = dict(lock["species_snapshot"])
    effort_entry = dict(lock["effort_snapshot"])
    provenance = {
        "repository": repository,
        "commit": commit,
        "species_path": species_entry["path"],
        "species_blob_sha": species_entry["blob_sha"],
        "effort_path": effort_entry["path"],
        "effort_blob_sha": effort_entry["blob_sha"],
    }

    if cache_dir is None:
        with tempfile.TemporaryDirectory(prefix="izu_public_data_") as temporary:
            return _acquire_into(
                Path(temporary),
                output_dir,
                repository,
                commit,
                species_entry,
                effort_entry,
                provenance,
            )
    cache_dir.mkdir(parents=True, exist_ok=True)
    return _acquire_into(
        cache_dir,
        output_dir,
        repository,
        commit,
        species_entry,
        effort_entry,
        provenance,
    )


def _acquire_into(
    cache_dir: Path,
    output_dir: Path,
    repository: str,
    commit: str,
    species_entry: dict[str, object],
    effort_entry: dict[str, object],
    provenance: dict[str, object],
) -> dict[str, object]:
    species_path = cache_dir / "island_species_occurrences.csv.gz"
    effort_path = cache_dir / "island_observation_effort.csv"
    if not species_path.exists():
        _download(
            _raw_url(repository, commit, str(species_entry["path"])),
            species_path,
        )
    if not effort_path.exists():
        _download(
            _raw_url(repository, commit, str(effort_entry["path"])),
            effort_path,
        )
    return extract(species_path, effort_path, output_dir, provenance)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-lock", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path)
    args = parser.parse_args()
    summary = acquire(args.source_lock, args.output_dir, args.cache_dir)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
