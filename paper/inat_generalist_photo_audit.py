"""Audit iNaturalist research-grade photo availability for generalist controls.

The output is availability metadata only. It does not infer island membership,
flower traits, pollinator interactions, or biological absence. Every query is
retained with its URL, timestamp and retrieval outcome so an HTTP failure cannot
be silently read as a zero.
"""
from __future__ import annotations

import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HERE = Path(__file__).parent
MAX_ATTEMPTS = 4
BASE_SLEEP_SECONDS = 1.2
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
FIELDS = [
    "species", "island_proxy", "photo_count", "retrieval_status", "http_status",
    "attempts", "retrieved_at_utc", "query_url", "boundary",
]
BOUNDARY = (
    "Proxy-radius research-grade photo availability only; not an island assignment, "
    "flowering confirmation, trait observation, pollination interaction, or absence datum."
)


def query_url(species: str, lat: float, lng: float, radius: int) -> str:
    params = {
        "taxon_name": species, "lat": lat, "lng": lng, "radius": radius,
        "quality_grade": "research", "photos": "true", "per_page": 1,
    }
    return "https://api.inaturalist.org/v1/observations?" + urlencode(params)


def fetch_count(url: str) -> tuple[int, int, int]:
    """Return count, HTTP status and successful attempt number or raise final error."""
    last_error: Exception | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        request = Request(url, headers={"User-Agent": "izu-meta-analysis-generalist-audit/1.1"})
        try:
            with urlopen(request, timeout=45) as response:  # nosec B310: fixed HTTPS API
                return int(json.load(response).get("total_results", 0)), int(response.status), attempt
        except HTTPError as error:
            last_error = error
            retry_after = error.headers.get("Retry-After") if error.headers else None
            sleep = float(retry_after) if retry_after and retry_after.isdigit() else BASE_SLEEP_SECONDS * attempt
            if error.code not in (429, 500, 502, 503, 504) or attempt == MAX_ATTEMPTS:
                raise
            time.sleep(sleep)
        except URLError as error:
            last_error = error
            if attempt == MAX_ATTEMPTS:
                raise
            time.sleep(BASE_SLEEP_SECONDS * attempt)
    assert last_error is not None
    raise last_error


def main() -> None:
    rows: list[dict[str, object]] = []
    for species in SPECIES:
        for island, (lat, lng, radius) in ISLANDS.items():
            url = query_url(species, lat, lng, radius)
            timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            try:
                total, status, attempts = fetch_count(url)
                row = {"photo_count": total, "retrieval_status": "retrieved", "http_status": status, "attempts": attempts}
            except HTTPError as error:
                row = {"photo_count": "", "retrieval_status": f"error:HTTPError:{error.code}", "http_status": error.code, "attempts": MAX_ATTEMPTS}
            except URLError as error:
                row = {"photo_count": "", "retrieval_status": f"error:URLError:{error.reason}", "http_status": "", "attempts": MAX_ATTEMPTS}
            rows.append({"species": species, "island_proxy": island, **row, "retrieved_at_utc": timestamp, "query_url": url, "boundary": BOUNDARY})
            time.sleep(BASE_SLEEP_SECONDS)
    output = HERE / "evidence_screening" / "inat_generalist_photo_availability.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    print(f"wrote {len(rows)} availability rows to {output}")


if __name__ == "__main__":
    main()
