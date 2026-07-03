"""Assemble a BLINDED flower-photo review sheet from iNaturalist (Tier-C).

For a species, pull research-grade photographed observations from a mainland
reference box and each Izu island. The scorer sees only card ID and image URL,
not region. Review is explicitly two-stage:

1. Stage 0 eligibility: flowering, visible focal structure, scale/reference and
   comparability are checked while geography remains hidden.
2. Trait scoring: only eligible cards can receive a score for a predeclared,
   species-appropriate trait. A generic corolla-size score is never mandatory.

The hidden key is joined only after review. Availability, a proxy radius, or an
unscored image is never an island trait observation.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import random
import time
import urllib.parse
import urllib.request

OUT = pathlib.Path(__file__).parent / "photo_sheets"

REGIONS = {
    "MAINLAND": (34.75, 138.95, 25),
    "Oshima": (34.7385, 139.4024, 8),
    "Toshima": (34.5230, 139.2800, 5),
    "Niijima": (34.3813, 139.2654, 6),
    "Kozushima": (34.2142, 139.1523, 6),
    "Miyake": (34.0854, 139.5213, 8),
    "Hachijo": (33.1025, 139.8077, 8),
}


def fetch(species: str, lat: float, lng: float, radius: float, count: int):
    params = {
        "taxon_name": species, "lat": lat, "lng": lng, "radius": radius,
        "quality_grade": "research", "photos": "true", "per_page": count,
        "order_by": "votes",
    }
    url = "https://api.inaturalist.org/v1/observations?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "izu-meta-analysis"})
    with urllib.request.urlopen(request, timeout=40) as response:  # nosec B310 fixed HTTPS API
        data = json.load(response)
    output = []
    for result in data.get("results", []):
        photos = result.get("photos") or []
        if photos:
            output.append((result["id"], photos[0]["url"].replace("square", "medium")))
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("species")
    parser.add_argument("--per-region", type=int, default=6)
    parser.add_argument("--seed", type=int, default=20260703)
    args = parser.parse_args()

    OUT.mkdir(exist_ok=True)
    cards = []
    for region, (lat, lng, radius) in REGIONS.items():
        try:
            observations = fetch(args.species, lat, lng, radius, args.per_region)
        except Exception as error:
            print(f"  {region}: fetch error {error}")
            observations = []
        cards.extend({"region": region, "obs_id": obs_id, "image_url": url} for obs_id, url in observations)
        print(f"  {region:10s} {len(observations)} photos")
        time.sleep(0.7)

    random.Random(args.seed).shuffle(cards)
    slug = args.species.lower().replace(" ", "_")
    for index, card in enumerate(cards):
        card["card_id"] = f"{slug[:6]}_{index:03d}"

    blind = OUT / f"{slug}_blind_sheet.csv"
    key = OUT / f"{slug}_key.csv"
    eligibility = [
        "card_id", "image_url", "flowering_state_open_closed_fruit_vegetative_unclear",
        "focal_flower_visible_yes_no_unclear", "interior_visible_yes_no_na",
        "scale_or_reference_present_yes_no", "comparable_for_predeclared_trait_yes_no",
        "trait_definition_id", "trait_score_if_eligible", "reviewer_notes",
    ]
    with blind.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(eligibility)
        for card in cards:
            writer.writerow([card["card_id"], card["image_url"], "", "", "", "", "", "", "", ""])
    with key.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["card_id", "region", "obs_id"])
        for card in cards:
            writer.writerow([card["card_id"], card["region"], card["obs_id"]])
    print(f"\n{len(cards)} cards -> {blind.name} (blinded stage-0 gate) + {key.name} (hidden key)")


if __name__ == "__main__":
    main()
