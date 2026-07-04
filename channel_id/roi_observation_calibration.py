"""Candidate flower-ROI proposals and negative-control calibration utilities.

This module does not claim to solve flower segmentation. It deliberately turns
that uncertainty into a testable observation-model problem. Given a photographed
open flower that has already passed blinded stage-0 review, it proposes several
scale-free crop operators and asks whether any operator preserves the known
flat visual-signal pattern of the *Ajania pacifica* negative control.

A crop operator that fails the negative control is rejected as a public-image
phenotype proxy. Passing the control is necessary but not sufficient: visual
inspection of the crop sheets remains required before an operator can be used
for the wider specialist screen.
"""
from __future__ import annotations

import io
import math
from collections import defaultdict
from typing import Iterable, Sequence

from channel_id.public_visual_signature import (
    add_within_taxon_salience,
    extract_image_descriptors,
    transition_contrasts,
)

PROPOSALS = ("full_frame", "centre_65", "max_chroma_65", "max_chroma_edge_65")


def _image_dependencies():
    try:
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as error:  # pragma: no cover - optional runtime dependency
        raise RuntimeError("ROI proposal calibration requires Pillow and numpy") from error
    return np, Image, ImageDraw, ImageFont


def _integral_mean(score, x0: int, y0: int, x1: int, y1: int) -> float:
    """Mean score inside a rectangle using a zero-padded integral image."""
    total = score[y1, x1] - score[y0, x1] - score[y1, x0] + score[y0, x0]
    return float(total / max(1, (x1 - x0) * (y1 - y0)))


def _best_window(score, crop_width: int, crop_height: int, grid: int = 13) -> tuple[int, int, int, int]:
    """Search a coarse grid for a high-score crop window."""
    np, _, _, _ = _image_dependencies()
    height, width = score.shape
    crop_width = max(16, min(crop_width, width))
    crop_height = max(16, min(crop_height, height))
    integral = np.pad(score.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)), mode="constant")
    max_x, max_y = width - crop_width, height - crop_height
    x_positions = sorted({round(max_x * index / max(1, grid - 1)) for index in range(grid)})
    y_positions = sorted({round(max_y * index / max(1, grid - 1)) for index in range(grid)})
    best = (-math.inf, 0, 0)
    for y0 in y_positions:
        for x0 in x_positions:
            value = _integral_mean(integral, x0, y0, x0 + crop_width, y0 + crop_height)
            if value > best[0]:
                best = (value, x0, y0)
    return best[1], best[2], best[1] + crop_width, best[2] + crop_height


def proposal_boxes(image_bytes: bytes, crop_fraction: float = 0.65) -> dict[str, tuple[int, int, int, int]]:
    """Return deterministic candidate crop boxes for one image.

    `max_chroma` is intentionally only a proposal: bright foliage, rocks, or
    clothing can still win. The calibration against manually accepted Ajania
    cards determines whether this proposal is sufficiently background-robust.
    """
    np, Image, _, _ = _image_dependencies()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = image.size
    if min(width, height) < 48:
        raise ValueError("image too small for ROI proposals")
    rgb = np.asarray(image, dtype=np.float32) / 255.0
    max_channel = rgb.max(axis=2)
    min_channel = rgb.min(axis=2)
    chroma = max_channel - min_channel
    brightness = rgb.mean(axis=2)
    gray = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    dx = np.abs(np.diff(gray, axis=1, prepend=gray[:, :1]))
    dy = np.abs(np.diff(gray, axis=0, prepend=gray[:1, :]))
    edges = 0.5 * (dx + dy)
    crop_width = max(48, round(width * crop_fraction))
    crop_height = max(48, round(height * crop_fraction))
    centre_x = max(0, (width - crop_width) // 2)
    centre_y = max(0, (height - crop_height) // 2)
    chroma_score = chroma * (0.25 + brightness)
    chroma_edge_score = 0.75 * chroma_score + 0.25 * edges
    return {
        "full_frame": (0, 0, width, height),
        "centre_65": (centre_x, centre_y, min(width, centre_x + crop_width), min(height, centre_y + crop_height)),
        "max_chroma_65": _best_window(chroma_score, crop_width, crop_height),
        "max_chroma_edge_65": _best_window(chroma_edge_score, crop_width, crop_height),
    }


def crop_feature_rows(image_bytes: bytes, taxon: str, card_id: str, image_url: str) -> list[dict[str, object]]:
    """Build descriptor rows for all proposal crops while keeping regime hidden."""
    _, Image, _, _ = _image_dependencies()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    rows: list[dict[str, object]] = []
    for proposal, (x0, y0, x1, y1) in proposal_boxes(image_bytes).items():
        crop = image.crop((x0, y0, x1, y1))
        payload = io.BytesIO()
        crop.save(payload, format="PNG")
        descriptors = extract_image_descriptors(payload.getvalue())
        rows.append({
            "card_id": card_id,
            "taxon": taxon,
            "proposal": proposal,
            "image_url": image_url,
            "box_x0": x0,
            "box_y0": y0,
            "box_x1": x1,
            "box_y1": y1,
            "crop_width_px": x1 - x0,
            "crop_height_px": y1 - y0,
            "feature_status": "ok",
            "error": "",
            **descriptors,
        })
    return rows


def render_contact_page(image_bytes: bytes, card_id: str) -> object:
    """Return a labelled original-plus-candidates review panel without geography."""
    np, Image, ImageDraw, ImageFont = _image_dependencies()
    del np
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    panels: list[tuple[str, object]] = [("original", image)]
    for proposal, box in proposal_boxes(image_bytes).items():
        if proposal == "full_frame":
            continue
        panels.append((proposal, image.crop(box)))
    cell_width, cell_height = 280, 240
    canvas = Image.new("RGB", (cell_width * 2, cell_height * 2), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    for index, (label, panel) in enumerate(panels):
        fitted = panel.copy()
        fitted.thumbnail((cell_width - 16, cell_height - 38))
        x = (index % 2) * cell_width + (cell_width - fitted.width) // 2
        y = (index // 2) * cell_height + 8
        canvas.paste(fitted, (x, y))
        draw.text(((index % 2) * cell_width + 8, (index // 2) * cell_height + cell_height - 24), f"{card_id} | {label}", fill="black", font=font)
    return canvas


def _proposal_salience_rows(rows: Iterable[dict[str, object]], proposal: str, key_by_card: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    subset: list[dict[str, object]] = []
    for row in rows:
        if str(row.get("proposal")) != proposal or str(row.get("feature_status")) != "ok":
            continue
        card_id = str(row["card_id"])
        if card_id not in key_by_card:
            raise ValueError(f"ROI candidate row missing key: {card_id}")
        joined = dict(row)
        joined["analysis_group"] = "generalist"
        # Standardise within one taxon/operator calibration unit, not across crop types.
        joined["taxon"] = f"Ajania pacifica::{proposal}"
        joined["pollinator_regime"] = key_by_card[card_id]["pollinator_regime_after_key_join"]
        subset.append(joined)
    return add_within_taxon_salience(subset)


def calibrate_against_ajania(
    candidate_rows: Iterable[dict[str, object]],
    manual_ledger_rows: Iterable[dict[str, str]],
    tolerance: float = 0.25,
) -> list[dict[str, object]]:
    """Rank crop proposals by preservation of Ajania's known flat signal.

    Only cards declared open, focal-visible and comparable in the earlier blind
    review are used. This calibration uses regime labels after the prior scoring
    lock, because its purpose is to test whether an image operator introduces
    a false regime effect into a known flat signal.
    """
    accepted = {
        row["card_id"]: row
        for row in manual_ledger_rows
        if row.get("taxon") == "Ajania pacifica"
        and row.get("flowering_state") == "open"
        and row.get("focal_flower_visible") == "yes"
        and row.get("comparable") == "yes"
        and row.get("trait_score") == "3"
    }
    if len(accepted) < 6:
        raise ValueError("Ajania calibration requires at least six manually accepted flat-signal cards")
    output: list[dict[str, object]] = []
    for proposal in PROPOSALS:
        enriched = _proposal_salience_rows(candidate_rows, proposal, accepted)
        contrasts = transition_contrasts(enriched, min_images_per_regime=2, bootstrap_draws=500, tolerance=tolerance)
        by_transition = {str(row["transition"]): row for row in contrasts}
        required = ("large_to_ardens", "ardens_to_no_bombus")
        complete = all(transition in by_transition for transition in required)
        deltas = [abs(float(by_transition[transition]["delta_focal_minus_reference"])) for transition in required if transition in by_transition]
        output.append({
            "proposal": proposal,
            "accepted_cards": len(enriched),
            "large_to_ardens_delta": "" if "large_to_ardens" not in by_transition else by_transition["large_to_ardens"]["delta_focal_minus_reference"],
            "ardens_to_no_bombus_delta": "" if "ardens_to_no_bombus" not in by_transition else by_transition["ardens_to_no_bombus"]["delta_focal_minus_reference"],
            "absolute_delta_sum": sum(deltas) if complete else math.inf,
            "max_abs_delta": max(deltas) if complete else math.inf,
            "passes_flat_negative_control": "yes" if complete and max(deltas) <= tolerance else "no",
            "calibration_boundary": "Passing this test means the crop operator did not create a large artificial regime contrast in the manually flat Ajania control. It does not prove the crop contains only floral tissue.",
        })
    return sorted(output, key=lambda row: (row["max_abs_delta"], row["proposal"]))
