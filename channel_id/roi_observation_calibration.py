"""Candidate flower-ROI proposals and negative-control calibration utilities.

Automatic crop proposals are tested against the manually flat Ajania control.
Passing this control is necessary but not sufficient for a usable floral ROI.
"""
from __future__ import annotations

import io
import math
from typing import Iterable

from channel_id.roi_visual_core import contrast_rows, image_descriptors, salience

PROPOSALS = ("full_frame", "centre_65", "max_chroma_65", "max_chroma_edge_65")


def _image_dependencies():
    try:
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as error:
        raise RuntimeError("ROI proposal calibration requires Pillow and numpy") from error
    return np, Image, ImageDraw, ImageFont


def _integral_mean(integral, x0: int, y0: int, x1: int, y1: int) -> float:
    total = integral[y1, x1] - integral[y0, x1] - integral[y1, x0] + integral[y0, x0]
    return float(total / max(1, (x1 - x0) * (y1 - y0)))


def _best_window(score, crop_width: int, crop_height: int, grid: int = 13) -> tuple[int, int, int, int]:
    np, _, _, _ = _image_dependencies()
    height, width = score.shape
    crop_width, crop_height = max(16, min(crop_width, width)), max(16, min(crop_height, height))
    integral = np.pad(score.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)), mode="constant")
    max_x, max_y = width - crop_width, height - crop_height
    xs = sorted({round(max_x * value / max(1, grid - 1)) for value in range(grid)})
    ys = sorted({round(max_y * value / max(1, grid - 1)) for value in range(grid)})
    best = (-math.inf, 0, 0)
    for y0 in ys:
        for x0 in xs:
            mean = _integral_mean(integral, x0, y0, x0 + crop_width, y0 + crop_height)
            if mean > best[0]:
                best = (mean, x0, y0)
    return best[1], best[2], best[1] + crop_width, best[2] + crop_height


def proposal_boxes(image_bytes: bytes, crop_fraction: float = 0.65) -> dict[str, tuple[int, int, int, int]]:
    np, Image, _, _ = _image_dependencies()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = image.size
    if min(width, height) < 48:
        raise ValueError("image too small for ROI proposals")
    rgb = np.asarray(image, dtype=np.float32) / 255.0
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    brightness = rgb.mean(axis=2)
    gray = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    edges = 0.5 * (np.abs(np.diff(gray, axis=1, prepend=gray[:, :1])) + np.abs(np.diff(gray, axis=0, prepend=gray[:1, :])))
    crop_width, crop_height = max(48, round(width * crop_fraction)), max(48, round(height * crop_fraction))
    centre_x, centre_y = max(0, (width - crop_width) // 2), max(0, (height - crop_height) // 2)
    chroma_score = chroma * (0.25 + brightness)
    return {
        "full_frame": (0, 0, width, height),
        "centre_65": (centre_x, centre_y, min(width, centre_x + crop_width), min(height, centre_y + crop_height)),
        "max_chroma_65": _best_window(chroma_score, crop_width, crop_height),
        "max_chroma_edge_65": _best_window(0.75 * chroma_score + 0.25 * edges, crop_width, crop_height),
    }


def crop_feature_rows(image_bytes: bytes, taxon: str, card_id: str, image_url: str) -> list[dict[str, object]]:
    _, Image, _, _ = _image_dependencies()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    rows: list[dict[str, object]] = []
    for proposal, (x0, y0, x1, y1) in proposal_boxes(image_bytes).items():
        payload = io.BytesIO()
        image.crop((x0, y0, x1, y1)).save(payload, format="PNG")
        rows.append({"card_id": card_id, "taxon": taxon, "proposal": proposal, "image_url": image_url, "box_x0": x0, "box_y0": y0, "box_x1": x1, "box_y1": y1, "crop_width_px": x1 - x0, "crop_height_px": y1 - y0, "feature_status": "ok", "error": "", **image_descriptors(payload.getvalue())})
    return rows


def render_contact_page(image_bytes: bytes, card_id: str) -> object:
    _, Image, ImageDraw, ImageFont = _image_dependencies()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    panels = [("original", image)] + [(proposal, image.crop(box)) for proposal, box in proposal_boxes(image_bytes).items() if proposal != "full_frame"]
    cell_width, cell_height = 280, 240
    canvas = Image.new("RGB", (cell_width * 2, cell_height * 2), "white")
    draw, font = ImageDraw.Draw(canvas), ImageFont.load_default()
    for index, (label, panel) in enumerate(panels):
        fitted = panel.copy()
        fitted.thumbnail((cell_width - 16, cell_height - 38))
        x, y = (index % 2) * cell_width + (cell_width - fitted.width) // 2, (index // 2) * cell_height + 8
        canvas.paste(fitted, (x, y))
        draw.text(((index % 2) * cell_width + 8, (index // 2) * cell_height + cell_height - 24), f"{card_id} | {label}", fill="black", font=font)
    return canvas


def calibrate_against_ajania(candidate_rows: Iterable[dict[str, object]], manual_ledger_rows: Iterable[dict[str, str]], tolerance: float = 0.25) -> list[dict[str, object]]:
    accepted = {row["card_id"]: row for row in manual_ledger_rows if row.get("taxon") == "Ajania pacifica" and row.get("flowering_state") == "open" and row.get("focal_flower_visible") == "yes" and row.get("comparable") == "yes" and row.get("trait_score") == "3"}
    if len(accepted) < 6:
        raise ValueError("Ajania calibration requires at least six manually accepted flat-signal cards")
    output = []
    for proposal in PROPOSALS:
        subset = []
        for row in candidate_rows:
            if str(row.get("proposal")) != proposal or str(row.get("feature_status")) != "ok":
                continue
            card_id = str(row["card_id"])
            if card_id not in accepted:
                continue
            joined = dict(row)
            joined["taxon"] = f"Ajania pacifica::{proposal}"
            joined["analysis_group"] = "generalist"
            joined["pollinator_regime"] = accepted[card_id]["pollinator_regime_after_key_join"]
            subset.append(joined)
        contrasts = {row["transition"]: row for row in contrast_rows(salience(subset), tolerance=tolerance)}
        required = ("large_to_ardens", "ardens_to_no_bombus")
        complete = all(name in contrasts for name in required)
        deltas = [abs(float(contrasts[name]["delta_focal_minus_reference"])) for name in required if name in contrasts]
        output.append({"proposal": proposal, "accepted_cards": len(subset), "large_to_ardens_delta": "" if "large_to_ardens" not in contrasts else contrasts["large_to_ardens"]["delta_focal_minus_reference"], "ardens_to_no_bombus_delta": "" if "ardens_to_no_bombus" not in contrasts else contrasts["ardens_to_no_bombus"]["delta_focal_minus_reference"], "absolute_delta_sum": sum(deltas) if complete else math.inf, "max_abs_delta": max(deltas) if complete else math.inf, "passes_flat_negative_control": "yes" if complete and max(deltas) <= tolerance else "no", "calibration_boundary": "Passing means the crop did not create a large artificial regime contrast in the manually flat Ajania control. It does not prove floral isolation."})
    return sorted(output, key=lambda row: (row["max_abs_delta"], row["proposal"]))
