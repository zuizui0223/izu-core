#!/usr/bin/env python3
"""Acquire additional blind Farfugium japonicum Oshima photo candidates.

The purpose is strictly to repair the empty Oshima flowering cell in the
prospectively locked high-functional-generality control. Existing reviewed
Oshima observations are excluded. All attached photos may be rendered for
stage-0 visibility review, but the biological independence unit remains the
*iNaturalist observation*, never the individual photo.

The existing predeclared phenotype rubric remains unchanged:
farfugium_visible_signal_0_3 =
0 cryptic head display; 1 weak ray/disc contrast; 2 clear contrast;
3 highly conspicuous head display.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import random
import urllib.parse
import urllib.request
from pathlib import Path


TAXON = "Farfugium japonicum"
OSHIMA_LAT = 34.7385
OSHIMA_LNG = 139.4024
RADIUS_KM = 8
EXISTING_OSHIMA_OBSERVATIONS = {
    233837146,
    323971845,
    322899074,
    151847128,
    39141856,
    322898005,
}
AUTUMN_MONTHS = {9, 10, 11}
MAX_OBSERVATIONS = 80
MAX_PHOTOS_PER_OBSERVATION = 3
SEED = 20260808


def api_json(params: dict[str, object]) -> dict[str, object]:
    query = urllib.parse.urlencode(params)
    url = f"https://api.inaturalist.org/v1/observations?{query}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_month(observed_on: object) -> int | None:
    text = str(observed_on or "").strip()
    if len(text) < 7:
        return None
    try:
        return int(text[5:7])
    except ValueError:
        return None


def photo_medium_url(url: str) -> str:
    # iNaturalist API typically returns .../square.jpg; use medium for review.
    for token in ("square", "small", "thumb"):
        if f"/{token}." in url:
            return url.replace(f"/{token}.", "/medium.")
    return url


def card_id(observation_id: int, photo_id: int) -> str:
    digest = hashlib.sha256(f"farfugium-oshima-{SEED}-{observation_id}-{photo_id}".encode()).hexdigest()
    return "FO-" + digest[:10].upper()


def fetch_candidates() -> list[dict[str, object]]:
    params = {
        "taxon_name": TAXON,
        "lat": OSHIMA_LAT,
        "lng": OSHIMA_LNG,
        "radius": RADIUS_KM,
        "quality_grade": "research",
        "photos": "true",
        "per_page": 200,
        "order_by": "observed_on",
        "order": "desc",
    }
    payload = api_json(params)
    results = payload.get("results") or []
    observations = []
    for raw in results:
        observation_id = int(raw["id"])
        if observation_id in EXISTING_OSHIMA_OBSERVATIONS:
            continue
        photos = raw.get("photos") or []
        if not photos:
            continue
        month = parse_month(raw.get("observed_on"))
        observations.append({
            "observation_id": observation_id,
            "observed_on": raw.get("observed_on"),
            "month": month,
            "autumn_priority": month in AUTUMN_MONTHS if month is not None else False,
            "photo_records": photos,
            "uri": raw.get("uri") or f"https://www.inaturalist.org/observations/{observation_id}",
        })

    # Predeclared visibility-oriented ordering: autumn records first because the
    # candidate registry already declares autumn flowering; within strata use a
    # deterministic shuffle, not phenotype information.
    rng = random.Random(SEED)
    autumn = [row for row in observations if row["autumn_priority"]]
    other = [row for row in observations if not row["autumn_priority"]]
    rng.shuffle(autumn)
    rng.shuffle(other)
    return (autumn + other)[:MAX_OBSERVATIONS]


def build_rows(observations: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    blind = []
    key = []
    for observation in observations:
        obs_id = int(observation["observation_id"])
        photos = sorted(
            observation["photo_records"],
            key=lambda photo: int(photo.get("id") or 0),
        )[:MAX_PHOTOS_PER_OBSERVATION]
        for photo_index, photo in enumerate(photos, start=1):
            photo_id = int(photo.get("id") or 0)
            raw_url = str(photo.get("url") or "")
            if not raw_url:
                continue
            opaque = card_id(obs_id, photo_id)
            blind.append({
                "card_id": opaque,
                "observation_group": f"OBS-{hashlib.sha256(str(obs_id).encode()).hexdigest()[:8].upper()}",
                "photo_url": photo_medium_url(raw_url),
                "trait_definition_id": "farfugium_visible_signal_0_3",
                "stage0_open_flower": "",
                "stage0_focal_head_visible": "",
                "stage0_comparable": "",
                "stage0_notes": "",
                "score_0_3": "",
            })
            key.append({
                "card_id": opaque,
                "observation_group": blind[-1]["observation_group"],
                "observation_id": obs_id,
                "photo_id": photo_id,
                "photo_index_within_observation": photo_index,
                "observed_on": observation["observed_on"],
                "month": observation["month"],
                "autumn_priority": observation["autumn_priority"],
                "region": "oshima",
                "regime": "ardens",
                "source_uri": observation["uri"],
            })
    return blind, key


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/farfugium_oshima_blind"))
    args = parser.parse_args()
    observations = fetch_candidates()
    blind, key = build_rows(observations)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "blind_cards.csv", blind)
    write_csv(args.output_dir / "protected_key.csv", key)
    summary = {
        "taxon": TAXON,
        "region": "oshima",
        "query": {
            "lat": OSHIMA_LAT,
            "lng": OSHIMA_LNG,
            "radius_km": RADIUS_KM,
            "quality_grade": "research",
            "photos": True,
        },
        "existing_observations_excluded": sorted(EXISTING_OSHIMA_OBSERVATIONS),
        "candidate_registry_flowering_season": "autumn",
        "autumn_months_used_only_for_pre_review_priority": sorted(AUTUMN_MONTHS),
        "n_new_observations": len(observations),
        "n_blind_photo_cards": len(blind),
        "n_autumn_priority_observations": sum(bool(row["autumn_priority"]) for row in observations),
        "independence_unit": "iNaturalist observation",
        "rubric": {
            "trait_definition_id": "farfugium_visible_signal_0_3",
            "definition": "0=cryptic head display; 1=weak ray/disc contrast; 2=clear contrast; 3=highly conspicuous head display"
        },
        "claim_boundary": (
            "Candidate acquisition and autumn prioritisation are visibility-recovery steps, not phenotype data. "
            "Multiple photos from one observation are never independent biological samples. Region/date keys "
            "must not be joined before stage-0 visibility and phenotype scores are frozen."
        ),
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
