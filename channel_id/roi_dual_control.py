"""Dual-control calibration for public-image flower ROI operators.

A usable operator must satisfy two separate technical requirements:

1. it must not manufacture regional differences in the manually flat Ajania
   negative control; and
2. it must remain sensitive to a deterministic attenuation of colour and local
   contrast applied to the exact same crop.

The second requirement is a technical sensitivity control, not a biological
positive control.  Broad specialist holdout analysis remains blocked until a
source-native or blinded-human biological positive control is available.
"""
from __future__ import annotations

import io
import math
from collections import defaultdict
from statistics import median
from typing import Iterable

from channel_id.roi_observation_calibration import PROPOSALS, proposal_boxes
from channel_id.roi_visual_core import image_descriptors, salience

TECHNICAL_VARIANTS = ("original", "attenuated")


def _pillow():
    try:
        from PIL import Image, ImageEnhance, ImageFilter
    except ImportError as error:  # pragma: no cover - optional runtime dependency
        raise RuntimeError("dual ROI calibration requires Pillow") from error
    return Image, ImageEnhance, ImageFilter


def attenuate_visual_signal(
    payload: bytes,
    saturation_factor: float = 0.25,
    contrast_factor: float = 0.70,
    blur_radius: float = 1.25,
) -> bytes:
    """Return a deterministic technical attenuation of one already-fixed crop."""
    if not 0 <= saturation_factor <= 1:
        raise ValueError("saturation_factor must be between 0 and 1")
    if not 0 < contrast_factor <= 1:
        raise ValueError("contrast_factor must be in (0, 1]")
    if blur_radius < 0:
        raise ValueError("blur_radius must be nonnegative")
    Image, ImageEnhance, ImageFilter = _pillow()
    image = Image.open(io.BytesIO(payload)).convert("RGB")
    image = ImageEnhance.Color(image).enhance(saturation_factor)
    image = ImageEnhance.Contrast(image).enhance(contrast_factor)
    if blur_radius:
        image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    output = io.BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def technical_positive_rows(
    image_bytes: bytes,
    taxon: str,
    card_id: str,
    image_url: str,
) -> list[dict[str, object]]:
    """Create paired original/attenuated descriptor rows for every fixed proposal."""
    Image, _, _ = _pillow()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    rows: list[dict[str, object]] = []
    for proposal, box in proposal_boxes(image_bytes).items():
        original_buffer = io.BytesIO()
        image.crop(box).save(original_buffer, format="PNG")
        original = original_buffer.getvalue()
        variants = {
            "original": original,
            "attenuated": attenuate_visual_signal(original),
        }
        for variant, payload in variants.items():
            rows.append({
                "pair_id": f"{card_id}::{proposal}",
                "card_id": card_id,
                "taxon": f"{taxon}::{proposal}::technical_positive",
                "proposal": proposal,
                "control_variant": variant,
                "image_url": image_url,
                "feature_status": "ok",
                **image_descriptors(payload),
            })
    return rows


def calibrate_technical_positive(
    rows: Iterable[dict[str, object]],
    minimum_pairs: int = 6,
    minimum_abs_median_delta: float = 0.50,
    minimum_negative_fraction: float = 0.80,
) -> list[dict[str, object]]:
    """Assess whether each proposal detects the known attenuation direction."""
    if minimum_pairs < 2:
        raise ValueError("minimum_pairs must be at least two")
    if minimum_abs_median_delta <= 0:
        raise ValueError("minimum_abs_median_delta must be positive")
    if not 0 < minimum_negative_fraction <= 1:
        raise ValueError("minimum_negative_fraction must be in (0, 1]")

    source = [dict(row) for row in rows if str(row.get("feature_status", "ok")) == "ok"]
    output: list[dict[str, object]] = []
    for proposal in PROPOSALS:
        proposal_rows = [row for row in source if str(row.get("proposal")) == proposal]
        scored = salience(proposal_rows)
        pairs: dict[str, dict[str, float]] = defaultdict(dict)
        for row in scored:
            variant = str(row.get("control_variant"))
            if variant in TECHNICAL_VARIANTS and "visual_salience_v1" in row:
                pairs[str(row["pair_id"])][variant] = float(row["visual_salience_v1"])
        deltas = [
            values["attenuated"] - values["original"]
            for values in pairs.values()
            if set(values) == set(TECHNICAL_VARIANTS)
        ]
        pair_count = len(deltas)
        median_delta = median(deltas) if deltas else math.inf
        negative_fraction = (
            sum(delta < 0 for delta in deltas) / pair_count if pair_count else 0.0
        )
        passes = (
            pair_count >= minimum_pairs
            and median_delta <= -minimum_abs_median_delta
            and negative_fraction >= minimum_negative_fraction
        )
        output.append({
            "proposal": proposal,
            "paired_cards": pair_count,
            "median_attenuated_minus_original": median_delta,
            "negative_pair_fraction": negative_fraction,
            "minimum_abs_median_delta": minimum_abs_median_delta,
            "minimum_negative_fraction": minimum_negative_fraction,
            "passes_technical_positive_control": "yes" if passes else "no",
            "positive_control_boundary": (
                "This is a deterministic image-sensitivity control. It does not "
                "show that the operator measures a biological flower trait."
            ),
        })
    return output


def combine_control_gates(
    negative_rows: Iterable[dict[str, object]],
    positive_rows: Iterable[dict[str, object]],
) -> list[dict[str, object]]:
    """Combine technical gates while keeping biological validation explicitly blocked."""
    negative = {str(row["proposal"]): dict(row) for row in negative_rows}
    positive = {str(row["proposal"]): dict(row) for row in positive_rows}
    if set(negative) != set(PROPOSALS) or set(positive) != set(PROPOSALS):
        raise ValueError("both control tables must contain every fixed ROI proposal")
    output: list[dict[str, object]] = []
    for proposal in PROPOSALS:
        flat_pass = negative[proposal].get("passes_flat_negative_control") == "yes"
        sensitivity_pass = positive[proposal].get("passes_technical_positive_control") == "yes"
        output.append({
            "proposal": proposal,
            "passes_flat_negative_control": "yes" if flat_pass else "no",
            "passes_technical_positive_control": "yes" if sensitivity_pass else "no",
            "passes_dual_technical_gate": "yes" if flat_pass and sensitivity_pass else "no",
            "biological_positive_control_status": "missing",
            "eligible_for_broad_specialist_holdout": "no",
            "gate_boundary": (
                "Even a dual technical pass remains exploratory until an independent "
                "biological positive control validates the observation operator."
            ),
        })
    return output
