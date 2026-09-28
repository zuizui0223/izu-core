"""Minimal scale-free descriptor core used by ROI calibration.

This intentionally duplicates only the pieces needed to assess crop operators
against a known flat visual-signal control, keeping the calibration branch
independent of the broad exploratory screen.
"""
from __future__ import annotations

import io
import math
import random
from collections import defaultdict
from statistics import median
from typing import Iterable, Sequence

COMPONENTS = ("mean_saturation", "colourfulness", "radial_chroma_contrast", "hue_entropy", "edge_density")
TRANSITIONS = {"large_to_ardens": ("large_bombus", "ardens"), "ardens_to_no_bombus": ("ardens", "no_bombus")}


def _deps():
    try:
        import numpy as np
        from PIL import Image
    except ImportError as error:
        raise RuntimeError("ROI visual descriptors require Pillow and numpy") from error
    return np, Image


def image_descriptors(payload: bytes, max_side: int = 256) -> dict[str, float]:
    np, Image = _deps()
    image = Image.open(io.BytesIO(payload)).convert("RGB")
    source_width, source_height = image.size
    if min(source_width, source_height) < 32:
        raise ValueError("crop too small for descriptors")
    factor = min(1.0, max_side / max(source_width, source_height))
    if factor < 1:
        image = image.resize((max(32, round(source_width * factor)), max(32, round(source_height * factor))))
    rgb = np.asarray(image, dtype=np.float32) / 255.0
    hsv = np.asarray(image.convert("HSV"), dtype=np.float32) / 255.0
    sat, val, hue = hsv[..., 1], hsv[..., 2], hsv[..., 0]
    red, green, blue = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    rg = red - green
    yb = (red + green) * 0.5 - blue
    colourfulness = math.sqrt(float(np.var(rg)) + float(np.var(yb))) + 0.3 * math.sqrt(float(np.mean(rg)) ** 2 + float(np.mean(yb)) ** 2)
    rows, cols = sat.shape
    mask = np.zeros((rows, cols), dtype=bool)
    mask[rows // 4:rows - rows // 4, cols // 4:cols - cols // 4] = True
    radial_contrast = float(np.sqrt(np.sum((rgb[mask].mean(axis=0) - rgb[~mask].mean(axis=0)) ** 2)))
    weights = sat * (val > 0.15)
    if float(weights.sum()) <= 1e-9:
        entropy = 0.0
    else:
        bins = np.minimum((hue * 12).astype(int), 11)
        counts = np.bincount(bins.ravel(), weights=weights.ravel(), minlength=12)
        probabilities = counts[counts > 0] / counts.sum()
        entropy = float(-(probabilities * np.log(probabilities)).sum() / math.log(12))
    gray = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    edge_density = float(0.5 * (np.abs(np.diff(gray, axis=1)) > 0.08).mean() + 0.5 * (np.abs(np.diff(gray, axis=0)) > 0.08).mean())
    return {
        "source_width_px": float(source_width), "source_height_px": float(source_height),
        "processed_width_px": float(image.width), "processed_height_px": float(image.height),
        "mean_brightness": float(val.mean()), "mean_saturation": float(sat.mean()),
        "colourfulness": colourfulness, "radial_chroma_contrast": radial_contrast,
        "hue_entropy": entropy, "edge_density": edge_density,
    }


def salience(rows: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    output = [dict(row) for row in rows]
    groups: dict[str, list[int]] = defaultdict(list)
    for index, row in enumerate(output):
        if str(row.get("feature_status", "ok")) == "ok":
            groups[str(row["taxon"])].append(index)
    for _, indexes in groups.items():
        z_values: dict[str, dict[int, float]] = {}
        for feature in COMPONENTS:
            values = [float(output[index][feature]) for index in indexes]
            location = median(values)
            scale = 1.4826 * median([abs(value - location) for value in values])
            z_values[feature] = {index: 0.0 if scale <= 1e-12 else (float(output[index][feature]) - location) / scale for index in indexes}
        for index in indexes:
            output[index]["visual_salience_v1"] = sum(z_values[feature][index] for feature in COMPONENTS) / len(COMPONENTS)
    return output


def _percentile(values: Sequence[float], q: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lower, upper = int(position), math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def contrast_rows(rows: Iterable[dict[str, object]], tolerance: float = 0.25, draws: int = 500) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["pollinator_regime"])].append(row)
    result: list[dict[str, object]] = []
    for name, (reference_name, focal_name) in TRANSITIONS.items():
        reference_rows, focal_rows = grouped.get(reference_name, []), grouped.get(focal_name, [])
        if len(reference_rows) < 2 or len(focal_rows) < 2:
            continue
        reference = [float(row["visual_salience_v1"]) for row in reference_rows]
        focal = [float(row["visual_salience_v1"]) for row in focal_rows]
        point = median(focal) - median(reference)
        rng = random.Random(sum(ord(char) for char in name))
        boot = []
        for _ in range(draws):
            boot.append(median([focal[rng.randrange(len(focal))] for _ in focal]) - median([reference[rng.randrange(len(reference))] for _ in reference]))
        result.append({"transition": name, "delta_focal_minus_reference": point, "bootstrap_ci90_low": _percentile(boot, 0.05), "bootstrap_ci90_high": _percentile(boot, 0.95), "point_direction": "decrease" if point <= -tolerance else "increase" if point >= tolerance else "flat"})
    return result
