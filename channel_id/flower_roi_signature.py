"""Flower-region crop helpers for public visual signatures.

The raw full-frame public-image signature recovered many images, but it failed
Ajania negative-control calibration because backgrounds dominated the signal.
This module implements a deliberately simple, auditable ROI operator: find a
high-saturation/high-brightness mask, crop the largest plausible visual target,
and then run the existing scale-free descriptors on that crop.

The operator is not a flower detector and must pass negative-control calibration
before broad biological interpretation.
"""
from __future__ import annotations

import io
from dataclasses import dataclass


@dataclass(frozen=True)
class RoiResult:
    crop_bytes: bytes
    bbox_left: int
    bbox_top: int
    bbox_right: int
    bbox_bottom: int
    mask_fraction: float
    status: str


def _deps():
    try:
        import numpy as np
        from PIL import Image
    except ImportError as error:  # pragma: no cover
        raise RuntimeError("flower ROI extraction requires numpy and Pillow") from error
    return np, Image


def saliency_roi_crop(image_bytes: bytes, padding_fraction: float = 0.08, max_side: int = 512) -> RoiResult:
    """Return a saliency crop based on saturation and brightness.

    The crop favours visually salient floral material but is intentionally
    generic. If the mask is nearly empty or covers most of the frame, the whole
    image is returned with a diagnostic status rather than inventing a crop.
    """
    np, Image = _deps()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    original_width, original_height = image.size
    scale = min(1.0, max_side / float(max(original_width, original_height)))
    if scale < 1.0:
        image = image.resize((max(32, round(original_width * scale)), max(32, round(original_height * scale))))
    hsv = np.asarray(image.convert("HSV"), dtype=np.float32) / 255.0
    saturation = hsv[..., 1]
    value = hsv[..., 2]
    mask = (saturation >= max(0.12, float(np.quantile(saturation, 0.70)))) & (value >= max(0.18, float(np.quantile(value, 0.40))))
    fraction = float(mask.mean())
    if fraction < 0.01 or fraction > 0.65:
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return RoiResult(buffer.getvalue(), 0, 0, image.width, image.height, fraction, "fallback_full_frame")
    rows, cols = np.where(mask)
    top, bottom = int(rows.min()), int(rows.max()) + 1
    left, right = int(cols.min()), int(cols.max()) + 1
    pad_x = max(4, int((right - left) * padding_fraction))
    pad_y = max(4, int((bottom - top) * padding_fraction))
    left = max(0, left - pad_x)
    right = min(image.width, right + pad_x)
    top = max(0, top - pad_y)
    bottom = min(image.height, bottom + pad_y)
    crop = image.crop((left, top, right, bottom))
    buffer = io.BytesIO()
    crop.save(buffer, format="PNG")
    return RoiResult(buffer.getvalue(), left, top, right, bottom, fraction, "roi_crop")
