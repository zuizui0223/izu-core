"""Candidate extraction for a blind Campanula inner-corolla calibration set.

Unlike the original bundle builder, this layer keeps every attached photograph
from each research-grade observation rather than only the first image.  The
regional key is written separately and is never needed by the blind renderer.
"""
from __future__ import annotations

import random
from typing import Iterable

REGIONS = {
    "Oshima": {"lat": 34.7385, "lng": 139.4024, "radius": 8, "regime": "ardens"},
    "Toshima": {"lat": 34.5230, "lng": 139.2800, "radius": 5, "regime": "no_bombus"},
    "Niijima": {"lat": 34.3813, "lng": 139.2654, "radius": 6, "regime": "no_bombus"},
    "Kozushima": {"lat": 34.2142, "lng": 139.1523, "radius": 6, "regime": "no_bombus"},
    "Miyake": {"lat": 34.0854, "lng": 139.5213, "radius": 8, "regime": "no_bombus"},
    "Hachijo": {"lat": 33.1025, "lng": 139.8077, "radius": 8, "regime": "no_bombus"},
}

KNOWN_INELIGIBLE_PHOTO_IDS = {
    "232356741",
    "413359016",
    "413784530",
    "232380133",
}


def medium_url(photo: dict[str, object]) -> str:
    url = str(photo.get("url") or "").strip()
    if not url:
        return ""
    return url.replace("square", "medium")


def flatten_observations(
    observations: Iterable[dict[str, object]],
    region: str,
    regime: str,
    excluded_photo_ids: set[str] | None = None,
) -> list[dict[str, str]]:
    excluded = KNOWN_INELIGIBLE_PHOTO_IDS if excluded_photo_ids is None else excluded_photo_ids
    output: list[dict[str, str]] = []
    seen: set[str] = set()
    for observation in observations:
        obs_id = str(observation.get("id") or "").strip()
        for photo_index, photo in enumerate(observation.get("photos") or []):
            if not isinstance(photo, dict):
                continue
            photo_id = str(photo.get("id") or "").strip()
            image_url = medium_url(photo)
            if not obs_id or not photo_id or not image_url:
                continue
            if photo_id in excluded or photo_id in seen:
                continue
            seen.add(photo_id)
            output.append({
                "obs_id": obs_id,
                "photo_id": photo_id,
                "photo_index": str(photo_index),
                "image_url": image_url,
                "region": region,
                "pollinator_regime": regime,
            })
    return output


def deduplicate_photos(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        photo_id = str(row["photo_id"])
        if photo_id in seen:
            continue
        seen.add(photo_id)
        output.append(dict(row))
    return output


def select_and_blind(
    rows: Iterable[dict[str, str]],
    per_region: int = 24,
    seed: int = 20260710,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    if per_region <= 0:
        raise ValueError("per_region must be positive")
    source = deduplicate_photos(rows)
    by_region: dict[str, list[dict[str, str]]] = {}
    for row in source:
        by_region.setdefault(row["region"], []).append(row)
    selected: list[dict[str, str]] = []
    for region in REGIONS:
        candidates = sorted(by_region.get(region, []), key=lambda row: (row["obs_id"], row["photo_id"]))
        random.Random(f"{seed}:{region}").shuffle(candidates)
        selected.extend(candidates[:per_region])
    random.Random(seed).shuffle(selected)

    blind: list[dict[str, str]] = []
    key: list[dict[str, str]] = []
    for index, row in enumerate(selected):
        card_id = f"campint_{index:03d}"
        blind.append({
            "card_id": card_id,
            "image_url": row["image_url"],
            "flowering_state": "",
            "focal_flower_visible": "",
            "interior_visible": "",
            "comparable_for_guide_score": "",
            "trait_definition_id": "campanula_inner_guide_strength_0_3",
            "guide_score_0_3": "",
            "reviewer_notes": "",
        })
        key.append({
            "card_id": card_id,
            "region": row["region"],
            "pollinator_regime": row["pollinator_regime"],
            "obs_id": row["obs_id"],
            "photo_id": row["photo_id"],
            "photo_index": row["photo_index"],
        })
    return blind, key
