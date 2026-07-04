"""Acquire public iNaturalist images and extract scale-free visual fingerprints.

Acquisition uses the project's fixed regional proxy circles, but image feature
extraction itself receives only image bytes.  The output is deliberately split:

* `visual_fingerprint_blind.csv` has taxa, opaque image IDs, image URLs and
  feature values, but no region/regime labels;
* `visual_fingerprint_key.csv` holds the region/regime mapping and is joined
  only by the downstream analysis step.

This is a broad, high-recall exploratory layer.  It does not require each taxon
to have all three regimes, and it does not claim every image shows an open
flower.  Image status and source metadata are retained so later audits can
subset, validate or reject the result without silently changing the pool.
"""
from __future__ import annotations

import argparse
import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError

from channel_id.public_visual_signature import extract_image_descriptors

REGIONS = {
    "MAINLAND": (34.7500, 138.9500, 25.0, "large_bombus"),
    "Oshima": (34.7385, 139.4024, 8.0, "ardens"),
    "Toshima": (34.5230, 139.2800, 5.0, "no_bombus"),
    "Niijima": (34.3813, 139.2654, 6.0, "no_bombus"),
    "Kozushima": (34.2142, 139.1523, 6.0, "no_bombus"),
    "Miyake": (34.0854, 139.5213, 8.0, "no_bombus"),
    "Hachijo": (33.1025, 139.8077, 8.0, "no_bombus"),
}
FEATURE_FIELDS = (
    "image_id", "taxon", "analysis_group", "functional_group", "group_confidence", "image_url",
    "source_observation_id", "feature_status", "source_width_px", "source_height_px",
    "processed_width_px", "processed_height_px", "mean_brightness", "mean_saturation",
    "colourfulness", "radial_chroma_contrast", "hue_entropy", "edge_density", "error",
    "retrieved_at_utc", "feature_boundary",
)
KEY_FIELDS = (
    "image_id", "taxon", "source_observation_id", "region_proxy", "pollinator_regime",
    "query_url", "observation_url", "retrieved_at_utc", "geographic_boundary",
)
QUERY_FIELDS = (
    "taxon", "analysis_group", "region_proxy", "pollinator_regime", "requested_images",
    "returned_observations", "retrieval_status", "http_status", "query_url", "retrieved_at_utc",
)
FEATURE_BOUNDARY = (
    "Scale-free image descriptors calculated from the full public-photo frame. They are not confirmed floral traits, flower sizes, "
    "guide measurements, pollinator observations, or evidence of causal history."
)
GEOGRAPHIC_BOUNDARY = (
    "Fixed proxy circle used for public-image acquisition. It is not a verified island assignment, a field pollinator regime measurement, "
    "or an absence claim."
)


def clean(value: object) -> str:
    return str(value or "").strip()


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"taxon", "analysis_group", "functional_group", "group_confidence"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("visual-signature manifest is empty or missing required columns")
    return rows


def observation_query_url(taxon: str, latitude: float, longitude: float, radius: float, per_region: int) -> str:
    params = {
        "taxon_name": taxon,
        "lat": latitude,
        "lng": longitude,
        "radius": radius,
        "quality_grade": "research",
        "photos": "true",
        "per_page": per_region,
        "order_by": "observed_on",
        "order": "desc",
    }
    return "https://api.inaturalist.org/v1/observations?" + urllib.parse.urlencode(params)


def fetch_json(url: str) -> tuple[dict[str, object], int]:
    request = urllib.request.Request(url, headers={"User-Agent": "izu-core-public-visual-signature/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:  # nosec B310 fixed HTTPS endpoint
        return json.load(response), int(response.status)


def download_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "izu-core-public-visual-signature/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:  # nosec B310 fixed HTTPS endpoint
        return response.read()


def image_url_from_observation(observation: dict[str, object]) -> str:
    photos = observation.get("photos", [])
    if not isinstance(photos, list) or not photos or not isinstance(photos[0], dict):
        return ""
    raw = clean(photos[0].get("url"))
    # medium is large enough for scale-free descriptors and avoids downloading originals.
    return raw.replace("square", "medium") if raw else ""


def slug(text: str) -> str:
    return "".join(character.lower() if character.isalnum() else "_" for character in text).strip("_")


def write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def run(manifest: list[dict[str, str]], per_region: int, sleep_seconds: float) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    blind_rows: list[dict[str, object]] = []
    key_rows: list[dict[str, object]] = []
    query_rows: list[dict[str, object]] = []
    seen_observations: set[tuple[str, str]] = set()
    for spec in manifest:
        taxon = clean(spec["taxon"])
        for region, (latitude, longitude, radius, regime) in REGIONS.items():
            timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            url = observation_query_url(taxon, latitude, longitude, radius, per_region)
            try:
                payload, status = fetch_json(url)
                results = payload.get("results", [])
                if not isinstance(results, list):
                    results = []
                query_rows.append({
                    "taxon": taxon, "analysis_group": spec["analysis_group"], "region_proxy": region,
                    "pollinator_regime": regime, "requested_images": per_region,
                    "returned_observations": len(results), "retrieval_status": "retrieved", "http_status": status,
                    "query_url": url, "retrieved_at_utc": timestamp,
                })
            except HTTPError as error:
                results = []
                query_rows.append({
                    "taxon": taxon, "analysis_group": spec["analysis_group"], "region_proxy": region,
                    "pollinator_regime": regime, "requested_images": per_region,
                    "returned_observations": 0, "retrieval_status": f"error:HTTPError:{error.code}", "http_status": error.code,
                    "query_url": url, "retrieved_at_utc": timestamp,
                })
            except (URLError, json.JSONDecodeError) as error:
                results = []
                query_rows.append({
                    "taxon": taxon, "analysis_group": spec["analysis_group"], "region_proxy": region,
                    "pollinator_regime": regime, "requested_images": per_region,
                    "returned_observations": 0, "retrieval_status": f"error:{type(error).__name__}", "http_status": "",
                    "query_url": url, "retrieved_at_utc": timestamp,
                })
            for observation in results:
                if not isinstance(observation, dict):
                    continue
                obs_id = clean(observation.get("id"))
                if not obs_id or (taxon, obs_id) in seen_observations:
                    continue
                seen_observations.add((taxon, obs_id))
                image_url = image_url_from_observation(observation)
                if not image_url:
                    continue
                image_id = f"pvs-{slug(taxon)}-{obs_id}"
                row: dict[str, object] = {
                    "image_id": image_id, "taxon": taxon, "analysis_group": spec["analysis_group"],
                    "functional_group": spec["functional_group"], "group_confidence": spec["group_confidence"],
                    "image_url": image_url, "source_observation_id": obs_id, "feature_status": "ok",
                    "error": "", "retrieved_at_utc": timestamp, "feature_boundary": FEATURE_BOUNDARY,
                }
                try:
                    row.update(extract_image_descriptors(download_bytes(image_url)))
                except (HTTPError, URLError, OSError, ValueError, RuntimeError) as error:
                    row["feature_status"] = "error"
                    row["error"] = type(error).__name__
                blind_rows.append(row)
                key_rows.append({
                    "image_id": image_id, "taxon": taxon, "source_observation_id": obs_id,
                    "region_proxy": region, "pollinator_regime": regime, "query_url": url,
                    "observation_url": f"https://www.inaturalist.org/observations/{obs_id}",
                    "retrieved_at_utc": timestamp, "geographic_boundary": GEOGRAPHIC_BOUNDARY,
                })
            time.sleep(sleep_seconds)
    return blind_rows, key_rows, query_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--per-region", type=int, default=6)
    parser.add_argument("--sleep-seconds", type=float, default=0.15)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.per_region <= 0:
        raise SystemExit("--per-region must be positive")
    try:
        manifest = load_manifest(args.manifest)
        blind_rows, key_rows, query_rows = run(manifest, args.per_region, args.sleep_seconds)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "visual_fingerprint_blind.csv", FEATURE_FIELDS, blind_rows)
    write_csv(args.output_dir / "visual_fingerprint_key.csv", KEY_FIELDS, key_rows)
    write_csv(args.output_dir / "visual_fingerprint_queries.csv", QUERY_FIELDS, query_rows)
    report = {
        "taxa_requested": len(manifest), "images_with_features": sum(row["feature_status"] == "ok" for row in blind_rows),
        "images_with_errors": sum(row["feature_status"] != "ok" for row in blind_rows),
        "boundary": FEATURE_BOUNDARY,
    }
    (args.output_dir / "visual_fingerprint_extraction.summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
