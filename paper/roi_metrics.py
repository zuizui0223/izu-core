"""Run ROI crop proposals against the manually scored Ajania control.

Only cards that already passed blinded stage-0 review as open, focal-flower
visible and comparable are used. The output separates crop candidates from the
post-lock region key and renders contact sheets without geography.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from channel_id.roi_observation_calibration import (
    calibrate_against_ajania,
    crop_feature_rows,
    render_contact_page,
)

CANDIDATE_FIELDS = (
    "card_id", "taxon", "proposal", "image_url", "box_x0", "box_y0", "box_x1", "box_y1",
    "crop_width_px", "crop_height_px", "feature_status", "error", "source_width_px", "source_height_px",
    "processed_width_px", "processed_height_px", "mean_brightness", "mean_saturation", "colourfulness",
    "radial_chroma_contrast", "hue_entropy", "edge_density",
)
KEY_FIELDS = (
    "card_id", "obs_id", "region_after_key_join", "pollinator_regime_after_key_join", "manual_trait_score",
)
CALIBRATION_FIELDS = (
    "proposal", "accepted_cards", "large_to_ardens_delta", "ardens_to_no_bombus_delta",
    "absolute_delta_sum", "max_abs_delta", "passes_flat_negative_control", "calibration_boundary",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def accepted_ajania(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected = [
        row for row in rows
        if row.get("taxon") == "Ajania pacifica"
        and row.get("flowering_state") == "open"
        and row.get("focal_flower_visible") == "yes"
        and row.get("comparable") == "yes"
        and row.get("trait_score") == "3"
    ]
    if len(selected) < 6:
        raise ValueError("expected at least six accepted Ajania negative-control cards")
    return selected


def image_url_for_observation(obs_id: str) -> str:
    url = f"https://api.inaturalist.org/v1/observations/{obs_id}"
    request = Request(url, headers={"User-Agent": "izu-core-roi-calibration/1.0"})
    with urlopen(request, timeout=60) as response:  # nosec B310 fixed HTTPS endpoint
        payload = json.load(response)
    results = payload.get("results", [])
    if not isinstance(results, list) or not results or not isinstance(results[0], dict):
        raise ValueError(f"observation {obs_id} missing result")
    photos = results[0].get("photos", [])
    if not isinstance(photos, list) or not photos or not isinstance(photos[0], dict):
        raise ValueError(f"observation {obs_id} has no photo")
    raw = str(photos[0].get("url") or "").strip()
    if not raw:
        raise ValueError(f"observation {obs_id} has no photo URL")
    return raw.replace("square", "medium")


def download(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "izu-core-roi-calibration/1.0"})
    with urlopen(request, timeout=60) as response:  # nosec B310 fixed HTTPS endpoint
        return response.read()


def render_pages(panels: list[tuple[str, object]], out_dir: Path) -> None:
    try:
        from PIL import Image
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("ROI calibration rendering requires Pillow") from error
    out_dir.mkdir(parents=True, exist_ok=True)
    per_page = 4
    for start in range(0, len(panels), per_page):
        subset = panels[start:start + per_page]
        page = Image.new("RGB", (1120, 960), "white")
        for index, (_, panel) in enumerate(subset):
            page.paste(panel, ((index % 2) * 560, (index // 2) * 480))
        page.save(out_dir / f"ajania_roi_proposals_{start // per_page + 1:02d}.png")


def render_report(rows: list[dict[str, object]]) -> str:
    lines = [
        "# Ajania ROI observation-model calibration", "",
        "All cards were manually scored as visual-signal 3 before region keys were opened. A background-robust crop operator should keep both known-flat regime contrasts close to zero.", "",
        "| crop proposal | large→ardens delta | ardens→no-Bombus delta | max absolute delta | passes flat control |", "|---|---:|---:|---:|---|",
    ]
    for row in rows:
        def format_value(name: str) -> str:
            raw = row[name]
            return "NA" if raw == "" or (isinstance(raw, float) and not math.isfinite(raw)) else f"{float(raw):.3f}"
        lines.append(f"| {row['proposal']} | {format_value('large_to_ardens_delta')} | {format_value('ardens_to_no_bombus_delta')} | {format_value('max_abs_delta')} | {row['passes_flat_negative_control']} |")
    lines.extend(("", "## Boundary", "", "Passing means only that the automatic crop did not manufacture a large regime difference in the known-flat control. It does not prove the crop isolates floral tissue; the blinded contact sheets must still be checked."))
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sleep-seconds", type=float, default=0.2)
    args = parser.parse_args()
    if args.sleep_seconds < 0:
        raise SystemExit("sleep-seconds must be nonnegative")
    manual_rows = accepted_ajania(read_csv(args.ledger))
    candidates: list[dict[str, object]] = []
    keys: list[dict[str, object]] = []
    panels: list[tuple[str, object]] = []
    audit: list[dict[str, str]] = []
    for row in manual_rows:
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        card_id, obs_id = row["card_id"], row["obs_id"]
        try:
            image_url = image_url_for_observation(obs_id)
            image_bytes = download(image_url)
            candidates.extend(crop_feature_rows(image_bytes, "Ajania pacifica", card_id, image_url))
            panels.append((card_id, render_contact_page(image_bytes, card_id)))
            audit.append({"card_id": card_id, "obs_id": obs_id, "status": "ok", "retrieved_at_utc": timestamp, "error": ""})
        except (HTTPError, URLError, OSError, ValueError, RuntimeError) as error:
            audit.append({"card_id": card_id, "obs_id": obs_id, "status": "error", "retrieved_at_utc": timestamp, "error": type(error).__name__})
        keys.append({"card_id": card_id, "obs_id": obs_id, "region_after_key_join": row["region_after_key_join"], "pollinator_regime_after_key_join": row["pollinator_regime_after_key_join"], "manual_trait_score": row["trait_score"]})
        time.sleep(args.sleep_seconds)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "ajania_roi_candidates_blind.csv", CANDIDATE_FIELDS, candidates)
    write_csv(args.output_dir / "ajania_roi_key.csv", KEY_FIELDS, keys)
    write_csv(args.output_dir / "ajania_roi_download_audit.csv", ("card_id", "obs_id", "status", "retrieved_at_utc", "error"), audit)
    render_pages(panels, args.output_dir / "blinded_contact_sheets")
    calibration = calibrate_against_ajania(candidates, manual_rows)
    write_csv(args.output_dir / "ajania_roi_operator_calibration.csv", CALIBRATION_FIELDS, calibration)
    (args.output_dir / "AJANIA_ROI_CALIBRATION.md").write_text(render_report(calibration), encoding="utf-8")
    summary = {
        "manually_accepted_ajania_cards": len(manual_rows),
        "images_recovered": sum(row["status"] == "ok" for row in audit),
        "proposals_tested": len(calibration),
        "proposals_passing_flat_control": sum(row["passes_flat_negative_control"] == "yes" for row in calibration),
        "boundary": "Automatic crops are candidate observation operators. Passing a known-flat control is necessary but insufficient for a floral phenotype proxy.",
    }
    (args.output_dir / "ajania_roi_calibration.summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
