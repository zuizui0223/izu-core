#!/usr/bin/env python3
"""Acquire Toshima, Shikinejima, and Aogashima occurrence candidates.

The script extracts exact land polygons from the version-locked GSHHG high-
resolution shoreline, queries the GBIF occurrence search API inside those
polygons, and optionally combines the results with the six-island snapshot
already produced by ``acquire_izu_public_data.py``.

The result is an occurrence audit.  It is not a reviewed native flora, a
biological absence matrix, or evidence of pollinator effectiveness.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import shutil
import urllib.parse
import urllib.request
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence


USER_AGENT = "izu-core-supplemental-public-data/1.0"


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=300) as response, destination.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def _open_rows(path: Path) -> Iterable[dict[str, str]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


def _write_csv(path: Path, fields: Sequence[str], rows: Iterable[dict[str, object]], compressed: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    opener = gzip.open if compressed else open
    with opener(path, "wt", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)


def _scaffold_targets(path: Path, target_ids: set[str]) -> list[dict[str, str]]:
    rows = list(_open_rows(path))
    selected = [row for row in rows if row.get("unit_id") in target_ids]
    found = {row["unit_id"] for row in selected}
    missing = target_ids - found
    if missing:
        raise ValueError("targets missing from scaffold: " + ", ".join(sorted(missing)))
    return sorted(selected, key=lambda row: int(row["sequence_order"]))


def _point_in_ring(longitude: float, latitude: float, ring: Sequence[tuple[float, float]]) -> bool:
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        intersects = ((yi > latitude) != (yj > latitude)) and (
            longitude < (xj - xi) * (latitude - yi) / ((yj - yi) or 1e-30) + xi
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def _perpendicular_distance(point: tuple[float, float], start: tuple[float, float], end: tuple[float, float]) -> float:
    if start == end:
        return math.dist(point, start)
    x, y = point
    x1, y1 = start
    x2, y2 = end
    numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
    denominator = math.hypot(y2 - y1, x2 - x1)
    return numerator / denominator


def _rdp(points: Sequence[tuple[float, float]], tolerance: float) -> list[tuple[float, float]]:
    if len(points) <= 2:
        return list(points)
    start, end = points[0], points[-1]
    distances = [_perpendicular_distance(point, start, end) for point in points[1:-1]]
    if not distances:
        return [start, end]
    maximum = max(distances)
    index = distances.index(maximum) + 1
    if maximum <= tolerance:
        return [start, end]
    left = _rdp(points[: index + 1], tolerance)
    right = _rdp(points[index:], tolerance)
    return left[:-1] + right


def _simplify_closed_ring(ring: Sequence[tuple[float, float]], maximum_points: int = 700) -> list[tuple[float, float]]:
    points = list(ring)
    if points[0] == points[-1]:
        points = points[:-1]
    tolerance = 0.00001
    simplified = points
    while len(simplified) > maximum_points:
        simplified = _rdp(points + [points[0]], tolerance)[:-1]
        tolerance *= 2.0
    if simplified[0] != simplified[-1]:
        simplified.append(simplified[0])
    return simplified


def _rings(shape: object) -> list[list[tuple[float, float]]]:
    points = [tuple(point) for point in shape.points]
    parts = list(shape.parts) + [len(points)]
    output = []
    for index in range(len(parts) - 1):
        ring = points[parts[index] : parts[index + 1]]
        if len(ring) >= 4:
            if ring[0] != ring[-1]:
                ring.append(ring[0])
            output.append(ring)
    return output


def _extract_shapefile(archive: Path, destination: Path, member_prefix: str) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        for extension in (".shp", ".shx", ".dbf", ".prj"):
            candidates = [name for name in names if name.endswith(member_prefix + extension)]
            if not candidates:
                raise FileNotFoundError(member_prefix + extension)
            member = candidates[0]
            target = destination / Path(member).name
            with bundle.open(member) as source, target.open("wb") as handle:
                shutil.copyfileobj(source, handle)
    return destination / (Path(member_prefix).name + ".shp")


def extract_target_polygons(shapefile_path: Path, targets: Sequence[dict[str, str]]) -> list[dict[str, object]]:
    try:
        import shapefile  # type: ignore
    except ImportError as exc:  # pragma: no cover - exercised in acquisition workflow
        raise RuntimeError("pyshp is required for GSHHG extraction") from exc

    reader = shapefile.Reader(str(shapefile_path))
    fields = [field[0] for field in reader.fields[1:]]
    selected: list[dict[str, object]] = []
    for target in targets:
        longitude = float(target["longitude_seed"])
        latitude = float(target["latitude_seed"])
        candidates: list[tuple[float, int, list[tuple[float, float]], dict[str, object]]] = []
        for index, shape_record in enumerate(reader.iterShapeRecords()):
            shape = shape_record.shape
            minimum_x, minimum_y, maximum_x, maximum_y = shape.bbox
            if not (minimum_x <= longitude <= maximum_x and minimum_y <= latitude <= maximum_y):
                continue
            attributes = dict(zip(fields, shape_record.record))
            for ring in _rings(shape):
                if _point_in_ring(longitude, latitude, ring):
                    bbox_area = (maximum_x - minimum_x) * (maximum_y - minimum_y)
                    candidates.append((bbox_area, index, ring, attributes))
        if not candidates:
            raise ValueError(f"no GSHHG polygon contains seed for {target['unit_name']}")
        _, shape_index, ring, attributes = min(candidates, key=lambda item: item[0])
        simplified = _simplify_closed_ring(ring)
        selected.append(
            {
                "unit_id": target["unit_id"],
                "unit_name": target["unit_name"],
                "sequence_order": int(target["sequence_order"]),
                "shape_index": shape_index,
                "gshhg_attributes": attributes,
                "ring": simplified,
                "source_vertex_count": len(ring),
                "query_vertex_count": len(simplified),
            }
        )
    return selected


def _wkt(ring: Sequence[tuple[float, float]]) -> str:
    coordinates = ",".join(f"{longitude:.7f} {latitude:.7f}" for longitude, latitude in ring)
    return f"POLYGON(({coordinates}))"


def _query_page(base_url: str, parameters: dict[str, object]) -> dict[str, object]:
    query = urllib.parse.urlencode(parameters)
    request = urllib.request.Request(f"{base_url}?{query}", headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


def query_gbif_polygon(
    base_url: str,
    ring: Sequence[tuple[float, float]],
    taxon_key: int,
    page_size: int,
    maximum_offset: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    requests: list[dict[str, object]] = []
    offset = 0
    while True:
        parameters: dict[str, object] = {
            "geometry": _wkt(ring),
            "taxon_key": taxon_key,
            "has_coordinate": "true",
            "occurrence_status": "PRESENT",
            "limit": page_size,
            "offset": offset,
        }
        payload = _query_page(base_url, parameters)
        page = list(payload.get("results", []))
        records.extend(page)
        requests.append(
            {
                "offset": offset,
                "limit": page_size,
                "count_returned": len(page),
                "total_reported": int(payload.get("count", 0)),
                "end_of_records": bool(payload.get("endOfRecords", False)),
            }
        )
        if payload.get("endOfRecords", False) or not page:
            break
        offset += page_size
        if offset > maximum_offset:
            raise RuntimeError("GBIF result exceeded the configured maximum offset")
    deduplicated = {str(record.get("key")): record for record in records if record.get("key") is not None}
    return list(deduplicated.values()), requests


def _species_name(record: dict[str, object]) -> str:
    return str(
        record.get("acceptedScientificName")
        or record.get("species")
        or record.get("scientificName")
        or ""
    ).strip()


def aggregate_records(unit_id: str, unit_name: str, records: Sequence[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, object]]:
    by_species: dict[tuple[str, str], dict[str, object]] = {}
    datasets: set[str] = set()
    bases = Counter()
    uncertainties: list[float] = []
    years: list[int] = []
    for record in records:
        name = _species_name(record)
        if not name:
            continue
        key = str(record.get("acceptedTaxonKey") or record.get("speciesKey") or "")
        group = by_species.setdefault(
            (key, name),
            {
                "unit_id": unit_id,
                "island_name": unit_name,
                "species_key": key,
                "species": name,
                "n_records": 0,
                "gbif_ids": set(),
                "basis_of_record": set(),
                "dataset_keys": set(),
                "establishment_means": set(),
                "year_min": None,
                "year_max": None,
            },
        )
        group["n_records"] = int(group["n_records"]) + 1
        group["gbif_ids"].add(str(record.get("key")))
        basis = str(record.get("basisOfRecord") or "")
        dataset = str(record.get("datasetKey") or "")
        establishment = str(record.get("establishmentMeans") or "")
        if basis:
            group["basis_of_record"].add(basis)
            bases[basis] += 1
        if dataset:
            group["dataset_keys"].add(dataset)
            datasets.add(dataset)
        if establishment:
            group["establishment_means"].add(establishment)
        year = record.get("year")
        if isinstance(year, int):
            years.append(year)
            group["year_min"] = year if group["year_min"] is None else min(int(group["year_min"]), year)
            group["year_max"] = year if group["year_max"] is None else max(int(group["year_max"]), year)
        uncertainty = record.get("coordinateUncertaintyInMeters")
        if isinstance(uncertainty, (int, float)):
            uncertainties.append(float(uncertainty))

    rows = []
    for group in by_species.values():
        rows.append(
            {
                "island_id": unit_id,
                "island_name": unit_name,
                "species_key": group["species_key"],
                "species": group["species"],
                "n_records": group["n_records"],
                "n_unique_gbif_ids": len(group["gbif_ids"]),
                "basis_of_record_set": "|".join(sorted(group["basis_of_record"])),
                "dataset_key_set": "|".join(sorted(group["dataset_keys"])),
                "establishment_means_set": "|".join(sorted(group["establishment_means"])),
                "year_min": group["year_min"] if group["year_min"] is not None else "",
                "year_max": group["year_max"] if group["year_max"] is not None else "",
                "review_status": "occurrence_candidate_unreviewed",
            }
        )
    rows.sort(key=lambda row: str(row["species"]))
    sorted_uncertainty = sorted(uncertainties)
    median_uncertainty = (
        sorted_uncertainty[len(sorted_uncertainty) // 2] if sorted_uncertainty else None
    )
    effort = {
        "island_id": unit_id,
        "island_name": unit_name,
        "n_records": len(records),
        "n_unique_gbif_ids": len({str(record.get('key')) for record in records}),
        "n_species": len(rows),
        "n_datasets": len(datasets),
        "n_preserved_specimen": bases.get("PRESERVED_SPECIMEN", 0),
        "n_human_observation": bases.get("HUMAN_OBSERVATION", 0),
        "n_other_basis_of_record": len(records) - bases.get("PRESERVED_SPECIMEN", 0) - bases.get("HUMAN_OBSERVATION", 0),
        "n_uncertainty_reported": len(uncertainties),
        "median_coordinate_uncertainty_m": median_uncertainty if median_uncertainty is not None else "",
        "year_min": min(years) if years else "",
        "year_max": max(years) if years else "",
        "acquisition_source": "gbif_live_polygon_search",
    }
    return rows, effort


def _geojson(polygons: Sequence[dict[str, object]]) -> dict[str, object]:
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "unit_id": polygon["unit_id"],
                    "unit_name": polygon["unit_name"],
                    "sequence_order": polygon["sequence_order"],
                    "shape_index": polygon["shape_index"],
                    "source_vertex_count": polygon["source_vertex_count"],
                    "query_vertex_count": polygon["query_vertex_count"],
                    "gshhg_attributes": polygon["gshhg_attributes"],
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[list(point) for point in polygon["ring"]]],
                },
            }
            for polygon in polygons
        ],
    }


def combine_with_six_islands(six_dir: Path, supplemental_species: Sequence[dict[str, object]], supplemental_effort: Sequence[dict[str, object]], output_dir: Path) -> dict[str, object]:
    six_species = list(_open_rows(six_dir / "izu_island_species.csv.gz"))
    six_effort = list(_open_rows(six_dir / "izu_island_effort.csv"))
    combined_species: list[dict[str, object]] = []
    for row in six_species:
        combined_species.append(
            {
                "island_id": row.get("island_id", ""),
                "island_name": row.get("island_name", ""),
                "species_key": "",
                "species": row.get("species", ""),
                "n_records": row.get("n_records", "0"),
                "n_unique_gbif_ids": row.get("n_unique_gbif_ids", "0"),
                "basis_of_record_set": row.get("basis_of_record_set", ""),
                "dataset_key_set": "",
                "establishment_means_set": "",
                "year_min": "",
                "year_max": "",
                "review_status": row.get("review_status", "occurrence_candidate_unreviewed"),
                "acquisition_source": "pinned_six_island_snapshot",
            }
        )
    for row in supplemental_species:
        combined_species.append({**row, "acquisition_source": "gbif_live_polygon_search"})
    combined_species.sort(key=lambda row: (str(row["island_name"]), str(row["species"])))

    species_fields = [
        "island_id", "island_name", "species_key", "species", "n_records",
        "n_unique_gbif_ids", "basis_of_record_set", "dataset_key_set",
        "establishment_means_set", "year_min", "year_max", "review_status",
        "acquisition_source",
    ]
    _write_csv(output_dir / "izu_9island_species.csv.gz", species_fields, combined_species, compressed=True)

    combined_effort: list[dict[str, object]] = []
    for row in six_effort:
        combined_effort.append({**row, "acquisition_source": "pinned_six_island_snapshot"})
    combined_effort.extend(supplemental_effort)
    effort_fields = sorted({key for row in combined_effort for key in row})
    _write_csv(output_dir / "izu_9island_effort.csv", effort_fields, combined_effort)

    incidence: dict[str, dict[str, object]] = {}
    for row in combined_species:
        species = str(row["species"])
        entry = incidence.setdefault(species, {"species": species, "islands": set(), "n_records": 0})
        entry["islands"].add(str(row["island_name"]))
        entry["n_records"] = int(entry["n_records"]) + int(float(row["n_records"] or 0))
    incidence_rows = [
        {
            "species": species,
            "n_islands": len(entry["islands"]),
            "islands": "|".join(sorted(entry["islands"])),
            "n_records": entry["n_records"],
        }
        for species, entry in sorted(incidence.items())
    ]
    _write_csv(output_dir / "izu_9island_species_incidence.csv", ["species", "n_islands", "islands", "n_records"], incidence_rows)
    return {
        "n_islands": len({str(row["island_name"]) for row in combined_effort}),
        "n_island_species_rows": len(combined_species),
        "n_unique_species_labels": len(incidence_rows),
        "n_records": sum(int(float(row.get("n_records", 0) or 0)) for row in combined_effort),
    }


def acquire(source_lock: Path, scaffold: Path, output_dir: Path, cache_dir: Path, six_island_dir: Path | None = None) -> dict[str, object]:
    lock = _read_json(source_lock)
    gshhg = dict(lock["gshhg"])
    gbif = dict(lock["gbif"])
    target_ids = set(map(str, lock["targets_from_scaffold"]))
    targets = _scaffold_targets(scaffold, target_ids)

    archive = cache_dir / "gshhg-shp-2.3.7.zip"
    if not archive.exists():
        _download(str(gshhg["url"]), archive)
    shapefile_path = _extract_shapefile(archive, cache_dir / "gshhg", str(gshhg["archive_member_prefix"]))
    polygons = extract_target_polygons(shapefile_path, targets)

    output_dir.mkdir(parents=True, exist_ok=True)
    all_species: list[dict[str, object]] = []
    all_effort: list[dict[str, object]] = []
    request_log: dict[str, object] = {}
    raw_path = output_dir / "izu_supplemental_raw_occurrences.jsonl.gz"
    with gzip.open(raw_path, "wt", encoding="utf-8") as raw_handle:
        for polygon in polygons:
            records, requests = query_gbif_polygon(
                str(gbif["occurrence_search_url"]),
                polygon["ring"],
                int(gbif["taxon_key"]),
                int(gbif["page_size"]),
                int(gbif["maximum_offset"]),
            )
            for record in records:
                raw_handle.write(json.dumps({"unit_id": polygon["unit_id"], "record": record}, ensure_ascii=False) + "\n")
            species_rows, effort = aggregate_records(str(polygon["unit_id"]), str(polygon["unit_name"]), records)
            all_species.extend(species_rows)
            all_effort.append(effort)
            request_log[str(polygon["unit_id"])] = requests

    species_fields = [
        "island_id", "island_name", "species_key", "species", "n_records",
        "n_unique_gbif_ids", "basis_of_record_set", "dataset_key_set",
        "establishment_means_set", "year_min", "year_max", "review_status",
    ]
    _write_csv(output_dir / "izu_supplemental_island_species.csv.gz", species_fields, all_species, compressed=True)
    effort_fields = sorted({key for row in all_effort for key in row})
    _write_csv(output_dir / "izu_supplemental_island_effort.csv", effort_fields, all_effort)
    (output_dir / "izu_supplemental_polygons.geojson").write_text(
        json.dumps(_geojson(polygons), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    combined = None
    if six_island_dir is not None:
        combined = combine_with_six_islands(six_island_dir, all_species, all_effort, output_dir)

    summary = {
        "schema_version": "1.0",
        "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_lock": lock,
        "targets": [
            {
                "unit_id": polygon["unit_id"],
                "unit_name": polygon["unit_name"],
                "shape_index": polygon["shape_index"],
                "source_vertex_count": polygon["source_vertex_count"],
                "query_vertex_count": polygon["query_vertex_count"],
                "n_records": next(row["n_records"] for row in all_effort if row["island_id"] == polygon["unit_id"]),
                "n_species": next(row["n_species"] for row in all_effort if row["island_id"] == polygon["unit_id"]),
            }
            for polygon in polygons
        ],
        "combined_nine_island_summary": combined,
        "request_log": request_log,
        "limitations": [
            "GBIF search results are live and must be archived with their acquisition timestamp.",
            "Occurrence records are candidate evidence, not reviewed native establishment.",
            "Non-detection is not biological absence and observation effort is uneven.",
            "The GSHHG query ring is simplified only for API transport; the source vertex count is retained.",
            "Pollinator regime labels are working hypotheses and are not inferred from these plant occurrences.",
        ],
    }
    (output_dir / "izu_supplemental_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-lock", type=Path, default=Path("config/izu_supplemental_gbif_source.json"))
    parser.add_argument("--scaffold", type=Path, default=Path("data/design/izu_regime_scaffold.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/izu_supplemental_gbif"))
    parser.add_argument("--cache-dir", type=Path, default=Path(".cache/izu_supplemental_gbif"))
    parser.add_argument("--six-island-dir", type=Path)
    args = parser.parse_args()
    summary = acquire(args.source_lock, args.scaffold, args.output_dir, args.cache_dir, args.six_island_dir)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
