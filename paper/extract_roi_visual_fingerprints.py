"""Recalculate public-image visual signatures after saliency ROI cropping."""
from __future__ import annotations

import argparse
import csv
import json
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError

from channel_id.flower_roi_signature import saliency_roi_crop
from channel_id.public_visual_signature import extract_image_descriptors

ROI_FIELDS = (
    "image_id", "taxon", "analysis_group", "image_url", "source_observation_id", "feature_status",
    "roi_status", "roi_left", "roi_top", "roi_right", "roi_bottom", "roi_mask_fraction",
    "mean_brightness", "mean_saturation", "colourfulness", "radial_chroma_contrast", "hue_entropy",
    "edge_density", "error", "boundary",
)
BOUNDARY = "Saliency ROI features are exploratory image signatures, not validated flower measurements."


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "izu-core-roi-signature/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:  # nosec B310 fixed HTTPS endpoint
        return response.read()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ROI_FIELDS, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def run(blind_features: Path) -> list[dict[str, object]]:
    rows = read_csv(blind_features)
    required = {"image_id", "taxon", "analysis_group", "image_url", "source_observation_id"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("blind feature table is empty or missing required columns")
    output: list[dict[str, object]] = []
    for row in rows:
        result: dict[str, object] = {
            "image_id": row["image_id"], "taxon": row["taxon"], "analysis_group": row["analysis_group"],
            "image_url": row["image_url"], "source_observation_id": row["source_observation_id"],
            "feature_status": "ok", "error": "", "boundary": BOUNDARY,
        }
        try:
            roi = saliency_roi_crop(download(row["image_url"]))
            result.update({
                "roi_status": roi.status, "roi_left": roi.bbox_left, "roi_top": roi.bbox_top,
                "roi_right": roi.bbox_right, "roi_bottom": roi.bbox_bottom,
                "roi_mask_fraction": roi.mask_fraction,
            })
            result.update(extract_image_descriptors(roi.crop_bytes))
        except (HTTPError, URLError, OSError, RuntimeError, ValueError) as error:
            result["feature_status"] = "error"
            result["roi_status"] = "error"
            result["error"] = type(error).__name__
        output.append(result)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blind-features", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()
    try:
        rows = run(args.blind_features)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    write_csv(args.output, rows)
    report = {
        "images_requested": len(rows),
        "images_with_roi_features": sum(row["feature_status"] == "ok" for row in rows),
        "roi_crops": sum(row.get("roi_status") == "roi_crop" for row in rows),
        "fallback_full_frame": sum(row.get("roi_status") == "fallback_full_frame" for row in rows),
        "boundary": BOUNDARY,
    }
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
