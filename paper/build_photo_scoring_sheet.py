"""Assemble a BLINDED flower-photo scoring sheet from iNaturalist (Tier-C).

For a species, pull research-grade, photographed observations from a mainland
reference box and from each Izu island, then emit two files:

  * <species>_blind_sheet.csv  -- shuffled rows with only {card_id, image_url};
        the scorer records relative traits (corolla size class, colour
        intensity, guide/spot) WITHOUT knowing the origin -> removes island bias.
  * <species>_key.csv          -- card_id -> region (kept separate; join only
        AFTER scoring to compute the mainland vs island direction).

Blinding is the point: relative floral-trait scores are only Tier-C evidence if
the scorer cannot see which island a photo comes from. Usage:

  python paper/build_photo_scoring_sheet.py "Hydrangea macrophylla" --per-region 6
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

REGIONS = {  # lat, lng, radius_km
    "MAINLAND": (34.75, 138.95, 25),
    "Oshima": (34.7385, 139.4024, 8),
    "Toshima": (34.5230, 139.2800, 5),
    "Niijima": (34.3813, 139.2654, 6),
    "Kozushima": (34.2142, 139.1523, 6),
    "Miyake": (34.0854, 139.5213, 8),
    "Hachijo": (33.1025, 139.8077, 8),
}


def fetch(sp: str, lat: float, lng: float, radius: float, n: int):
    params = {
        "taxon_name": sp, "lat": lat, "lng": lng, "radius": radius,
        "quality_grade": "research", "photos": "true",
        "per_page": n, "order_by": "votes",
    }
    url = "https://api.inaturalist.org/v1/observations?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "izu-meta-analysis"})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = json.load(r)
    out = []
    for res in data.get("results", []):
        photos = res.get("photos") or []
        if not photos:
            continue
        # medium-size version
        u = photos[0]["url"].replace("square", "medium")
        out.append((res["id"], u))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("species")
    ap.add_argument("--per-region", type=int, default=6)
    ap.add_argument("--seed", type=int, default=20260703)
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    cards = []
    for region, (lat, lng, rad) in REGIONS.items():
        try:
            obs = fetch(args.species, lat, lng, rad, args.per_region)
        except Exception as e:
            print(f"  {region}: fetch error {e}")
            obs = []
        for obs_id, url in obs:
            cards.append({"region": region, "obs_id": obs_id, "image_url": url})
        print(f"  {region:10s} {len(obs)} photos")
        time.sleep(0.7)

    rng = random.Random(args.seed)
    rng.shuffle(cards)
    slug = args.species.lower().replace(" ", "_")
    for i, c in enumerate(cards):
        c["card_id"] = f"{slug[:6]}_{i:03d}"

    blind = OUT / f"{slug}_blind_sheet.csv"
    key = OUT / f"{slug}_key.csv"
    with blind.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["card_id", "image_url", "corolla_size_class_1to5", "colour_intensity_1to5", "notes"])
        for c in cards:
            w.writerow([c["card_id"], c["image_url"], "", "", ""])
    with key.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["card_id", "region", "obs_id"])
        for c in cards:
            w.writerow([c["card_id"], c["region"], c["obs_id"]])
    print(f"\n{len(cards)} cards -> {blind.name} (blinded) + {key.name} (hidden key)")


if __name__ == "__main__":
    main()
