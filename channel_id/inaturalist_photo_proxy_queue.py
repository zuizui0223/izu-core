"""Create a reviewer queue using distances to declared island proxy points.

This module is deliberately not an island-assignment method. A nearest point on
an island is only a reproducible navigation hint for reviewing a public record's
actual coordinates and precision. The resulting fields must never be used as
population membership or as an island trait observation without geometry review.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any


APPENDED_COLUMNS = (
    "nearest_declared_proxy",
    "nearest_proxy_distance_km",
    "second_nearest_declared_proxy",
    "second_nearest_proxy_distance_km",
    "nearest_proxy_gap_km",
    "proxy_assignment_boundary",
    "reviewer_island_decision",
    "reviewer_notes",
)


def haversine_km(latitude_a: float, longitude_a: float, latitude_b: float, longitude_b: float) -> float:
    radius_km = 6371.0088
    lat_a, lon_a, lat_b, lon_b = map(math.radians, (latitude_a, longitude_a, latitude_b, longitude_b))
    value = math.sin((lat_b - lat_a) / 2.0) ** 2 + math.cos(lat_a) * math.cos(lat_b) * math.sin((lon_b - lon_a) / 2.0) ** 2
    return radius_km * 2.0 * math.asin(math.sqrt(value))


def load_proxy_points(path: Path) -> tuple[dict[str, float | str], ...]:
    config = json.loads(path.read_text(encoding="utf-8"))
    points = config.get("points")
    if not isinstance(points, list) or not points:
        raise ValueError("proxy config needs a nonempty points list")
    result: list[dict[str, float | str]] = []
    seen: set[str] = set()
    for point in points:
        if not isinstance(point, dict):
            raise ValueError("proxy point is not an object")
        island_id = str(point.get("island_id") or "").strip()
        if not island_id or island_id in seen:
            raise ValueError("proxy island IDs must be unique and nonempty")
        seen.add(island_id)
        result.append(
            {
                "island_id": island_id,
                "latitude": float(point["latitude"]),
                "longitude": float(point["longitude"]),
            }
        )
    return tuple(result)


def _coordinates(row: dict[str, str]) -> tuple[float, float] | None:
    try:
        latitude = float(row.get("latitude", ""))
        longitude = float(row.get("longitude", ""))
    except ValueError:
        return None
    if not -90.0 <= latitude <= 90.0 or not -180.0 <= longitude <= 180.0:
        return None
    return latitude, longitude


def queue_rows(candidates: list[dict[str, str]], proxies: tuple[dict[str, float | str], ...]) -> list[dict[str, str]]:
    """Append nearest-proxy metadata while retaining no proxy-based island decision."""
    rows: list[dict[str, str]] = []
    boundary = (
        "Nearest declared island proxy point is a review aid only; it is not an island polygon, "
        "population assignment, or trait observation. Review the original geometry and accuracy before use."
    )
    for candidate in candidates:
        output = dict(candidate)
        coordinate = _coordinates(candidate)
        if coordinate is None:
            output.update(
                {
                    "nearest_declared_proxy": "",
                    "nearest_proxy_distance_km": "",
                    "second_nearest_declared_proxy": "",
                    "second_nearest_proxy_distance_km": "",
                    "nearest_proxy_gap_km": "",
                }
            )
        else:
            latitude, longitude = coordinate
            distances = sorted(
                (
                    haversine_km(latitude, longitude, float(point["latitude"]), float(point["longitude"])),
                    str(point["island_id"]),
                )
                for point in proxies
            )
            nearest_distance, nearest = distances[0]
            second_distance, second = distances[1]
            output.update(
                {
                    "nearest_declared_proxy": nearest,
                    "nearest_proxy_distance_km": f"{nearest_distance:.6f}",
                    "second_nearest_declared_proxy": second,
                    "second_nearest_proxy_distance_km": f"{second_distance:.6f}",
                    "nearest_proxy_gap_km": f"{second_distance - nearest_distance:.6f}",
                }
            )
        output.update(
            {
                "proxy_assignment_boundary": boundary,
                "reviewer_island_decision": "unreviewed",
                "reviewer_notes": "",
            }
        )
        rows.append(output)
    return rows


def read_candidates(path: Path) -> tuple[list[dict[str, str]], tuple[str, ...]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        if not fieldnames:
            raise ValueError("candidate CSV needs a header")
        required = {"candidate_id", "target_id", "latitude", "longitude"}
        missing = required - set(fieldnames)
        if missing:
            raise ValueError("candidate CSV missing columns: " + ", ".join(sorted(missing)))
        return list(reader), fieldnames


def write_queue(rows: list[dict[str, str]], input_columns: tuple[str, ...], output_csv: Path, output_md: Path) -> None:
    fieldnames = tuple(input_columns) + tuple(column for column in APPENDED_COLUMNS if column not in input_columns)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    focal = [row for row in rows if row.get("target_id") == "campanula_microdonta"]
    by_proxy: dict[str, int] = {}
    for row in focal:
        proxy = row["nearest_declared_proxy"] or "missing_coordinates"
        by_proxy[proxy] = by_proxy.get(proxy, 0) + 1
    lines = [
        "# iNaturalist flower-photo proxy review queue",
        "",
        "The nearest-proxy columns are navigation aids only. No row has been assigned to an island by this workflow.",
        "",
        f"All photo candidates: {len(rows)}",
        f"Focal `Campanula microdonta` photo candidates: {len(focal)}",
        "",
        "## Focal candidate count by nearest declared proxy",
        "",
        "| nearest proxy | photo candidates |",
        "|---|---:|",
    ]
    for proxy, count in sorted(by_proxy.items()):
        lines.append(f"| {proxy} | {count} |")
    lines.extend(
        [
            "",
            "## Required reviewer decision",
            "",
            "Inspect the original observation URL, coordinates, positional accuracy, taxon, and photo. Enter a reviewer island decision only after geometry review. Then independently score inner-corolla visibility and comparability before considering any directional guide/spot claim.",
        ]
    )
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
