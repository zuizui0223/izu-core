"""Audit iNaturalist research-grade photo availability for generalist controls.

The output is availability metadata only. It does not infer island membership,
flower traits, pollinator interactions, or biological absence.
"""
from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HERE = Path(__file__).parent
ISLANDS = {
    "Oshima": (34.7385, 139.4024, 8),
    "Toshima": (34.5230, 139.2800, 5),
    "Niijima": (34.3813, 139.2654, 6),
    "Kozushima": (34.2142, 139.1523, 6),
    "Miyake": (34.0854, 139.5213, 8),
    "Hachijo": (33.1025, 139.8077, 8),
}
SPECIES = [
    "Ligustrum ovalifolium", "Hydrangea macrophylla", "Ajania pacifica",
    "Deutzia crenata", "Hydrangea involucrata", "Angelica keiskei",
    "Elaeagnus umbellata", "Aralia elata", "Aster microcephalus",
    "Pittosporum tobira", "Rosa luciae", "Farfugium japonicum",
    "Ilex crenata", "Peucedanum japonicum", "Rubus trifidus", "Euonymus japonicus",
]


def count(species: str, lat: float, lng: float, radius: int) -> int:
    params = {
        "taxon_name": species, "lat": lat, "lng": lng, "radius": radius,
        "quality_grade": "research", "photos": "true", "per_page": 0,
    }
    request = Request(
        "https://api.inaturalist.org/v1/observations?" + urlencode(params),
        headers={"User-Agent": "izu-meta-analysis-generalist-audit"},
    )
    with urlopen(request, timeout=40) as response:  # nosec B310: fixed HTTPS API
        return int(json.load(response).get("total_results", 0))


def main() -> None:
    rows: list[dict[str, object]] = []
    for species in SPECIES:
        for island, (lat, lng, radius) in ISLANDS.items():
            try:
                total: object = count(species, lat, lng, radius)
                status = "retrieved"
            except Exception as error:  # retained as retrieval failure, not zero
                total, status = "", f"error:{type(error).__name__}"
            rows.append({"species": species, "island_proxy": island, "photo_count": total, "retrieval_status": status})
            time.sleep(0.7)
    output = HERE / "evidence_screening" / "inat_generalist_photo_availability.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["species", "island_proxy", "photo_count", "retrieval_status"])
        writer.writeheader(); writer.writerows(rows)
    print(f"wrote {len(rows)} availability rows to {output}")


if __name__ == "__main__":
    main()
