"""Scale-free public-image visual signature extraction and transition summaries.

This module provides an intentionally modest bridge between the staged
Campanula simulation and heterogeneous public flower photographs.  It does not
claim that pixels are direct floral traits.  Instead it extracts repeatable,
scale-free image descriptors and treats their within-taxon regime contrasts as
an exploratory *visual signature* layer.

The theory-facing contract is deliberately narrow:

* specialist-like flowers are predicted to show a late decline in a visual
  salience proxy after the ardens -> no-Bombus transition;
* open-generalist flowers are a negative control and are predicted to lack that
  common late signature;
* a taxon can contribute to any transition for which the two required regimes
  are available.  A complete three-regime series is not required.

Image-derived descriptors remain vulnerable to photo framing, lighting,
background, phenology and observer behavior.  They must therefore never be
reported as absolute floral size, pollinator effectiveness, outcrossing, or
causal history.
"""
from __future__ import annotations

import io
import math
import random
from collections import defaultdict
from statistics import median
from typing import Iterable, Sequence

REGIMES = ("large_bombus", "ardens", "no_bombus")
TRANSITIONS = {
    "large_to_ardens": ("large_bombus", "ardens"),
    "ardens_to_no_bombus": ("ardens", "no_bombus"),
    "large_to_no_bombus": ("large_bombus", "no_bombus"),
}
RAW_FEATURE_IDS = (
    "mean_saturation",
    "colourfulness",
    "radial_chroma_contrast",
    "hue_entropy",
    "edge_density",
)
SALIENT_COMPONENTS = RAW_FEATURE_IDS


def _numpy_and_pillow():
    """Import image dependencies lazily so standard library-only tests still run."""
    try:
        import numpy as np
        from PIL import Image
    except ImportError as error:  # pragma: no cover - depends on optional image extras
        raise RuntimeError(
            "Visual fingerprint extraction requires optional dependencies Pillow and numpy. "
            "Install them before running paper/extract_public_visual_fingerprints.py."
        ) from error
    return np, Image


def extract_image_descriptors(image_bytes: bytes, max_side: int = 256) -> dict[str, float]:
    """Extract scale-free frame descriptors from one image.

    The descriptors intentionally contain no length metric.  They quantify
    chromatic variation, centre-versus-periphery contrast, hue diversity and
    local edge density.  All higher values mean *more* visual variation on the
    respective image scale; they are not calibrated flower measurements.
    """
    np, Image = _numpy_and_pillow()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    width, height = image.size
    if min(width, height) < 32:
        raise ValueError("image is too small for visual descriptor extraction")
    scale = min(1.0, max_side / float(max(width, height)))
    if scale < 1.0:
        image = image.resize((max(32, round(width * scale)), max(32, round(height * scale))))
    rgb_uint8 = np.asarray(image, dtype=np.uint8)
    rgb = rgb_uint8.astype(np.float32) / 255.0
    hsv = np.asarray(image.convert("HSV"), dtype=np.float32) / 255.0
    saturation = hsv[..., 1]
    value = hsv[..., 2]
    hue = hsv[..., 0]

    red, green, blue = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    rg = red - green
    yb = 0.5 * (red + green) - blue
    colourfulness = math.sqrt(float(np.var(rg)) + float(np.var(yb))) + 0.3 * math.sqrt(float(np.mean(rg)) ** 2 + float(np.mean(yb)) ** 2)

    rows, cols = saturation.shape
    r0, r1 = rows // 4, rows - rows // 4
    c0, c1 = cols // 4, cols - cols // 4
    centre_mask = np.zeros((rows, cols), dtype=bool)
    centre_mask[r0:r1, c0:c1] = True
    outer_mask = ~centre_mask
    centre_rgb = rgb[centre_mask].mean(axis=0)
    outer_rgb = rgb[outer_mask].mean(axis=0)
    radial_contrast = float(np.sqrt(np.sum((centre_rgb - outer_rgb) ** 2)))

    weights = saturation * (value > 0.15)
    weighted_total = float(weights.sum())
    if weighted_total <= 1e-9:
        hue_entropy = 0.0
    else:
        bins = np.minimum((hue * 12).astype(int), 11)
        counts = np.bincount(bins.ravel(), weights=weights.ravel(), minlength=12)
        probabilities = counts[counts > 0] / counts.sum()
        hue_entropy = float(-(probabilities * np.log(probabilities)).sum() / math.log(12))

    gray = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    dx = np.abs(np.diff(gray, axis=1))
    dy = np.abs(np.diff(gray, axis=0))
    edge_density = float((dx > 0.08).mean() * 0.5 + (dy > 0.08).mean() * 0.5)

    return {
        "source_width_px": float(width),
        "source_height_px": float(height),
        "processed_width_px": float(image.width),
        "processed_height_px": float(image.height),
        "mean_brightness": float(value.mean()),
        "mean_saturation": float(saturation.mean()),
        "colourfulness": colourfulness,
        "radial_chroma_contrast": radial_contrast,
        "hue_entropy": hue_entropy,
        "edge_density": edge_density,
    }


def _mad_scale(values: Sequence[float]) -> tuple[float, float]:
    location = median(values)
    mad = median([abs(value - location) for value in values])
    # 1.4826 puts MAD approximately on an SD scale under a normal reference.
    scale = 1.4826 * mad
    return location, scale


def add_within_taxon_salience(rows: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    """Append a robust, within-taxon visual-salience composite to feature rows."""
    source = [dict(row) for row in rows]
    by_taxon: dict[str, list[int]] = defaultdict(list)
    for index, row in enumerate(source):
        if str(row.get("feature_status", "ok")) == "ok":
            by_taxon[str(row["taxon"])].append(index)
    for taxon, indices in by_taxon.items():
        component_z: dict[str, dict[int, float]] = {}
        for feature in SALIENT_COMPONENTS:
            values = [float(source[index][feature]) for index in indices]
            location, scale = _mad_scale(values)
            component_z[feature] = {
                index: 0.0 if scale <= 1e-12 else (float(source[index][feature]) - location) / scale
                for index in indices
            }
        for index in indices:
            source[index]["visual_salience_v1"] = sum(component_z[feature][index] for feature in SALIENT_COMPONENTS) / len(SALIENT_COMPONENTS)
            source[index]["salience_component_count"] = len(SALIENT_COMPONENTS)
    return source


def percentile(values: Sequence[float], q: float) -> float:
    if not values:
        raise ValueError("cannot calculate percentile of an empty sequence")
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lower, upper = int(math.floor(position)), int(math.ceil(position))
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def bootstrap_median_delta(reference: Sequence[float], focal: Sequence[float], seed: int, draws: int = 500) -> tuple[float, float, float]:
    """Return focal-minus-reference median difference and 90% bootstrap interval."""
    if not reference or not focal:
        raise ValueError("both contrast groups require at least one value")
    point = median(focal) - median(reference)
    rng = random.Random(seed)
    simulated: list[float] = []
    for _ in range(draws):
        ref_draw = [reference[rng.randrange(len(reference))] for _ in reference]
        focal_draw = [focal[rng.randrange(len(focal))] for _ in focal]
        simulated.append(median(focal_draw) - median(ref_draw))
    return point, percentile(simulated, 0.05), percentile(simulated, 0.95)


def observed_direction(delta: float, tolerance: float) -> str:
    if delta <= -tolerance:
        return "decrease"
    if delta >= tolerance:
        return "increase"
    return "flat"


def transition_contrasts(
    rows: Iterable[dict[str, object]],
    min_images_per_regime: int = 2,
    bootstrap_draws: int = 500,
    tolerance: float = 0.25,
) -> list[dict[str, object]]:
    """Build taxon-level pairwise contrasts without requiring all three regimes."""
    grouped: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        if str(row.get("feature_status", "ok")) != "ok":
            continue
        if "visual_salience_v1" not in row:
            continue
        grouped[(str(row["taxon"]), str(row["analysis_group"]), str(row["pollinator_regime"]))].append(row)

    taxa = sorted({(taxon, group) for taxon, group, _ in grouped})
    output: list[dict[str, object]] = []
    for taxon, group in taxa:
        for transition, (reference_regime, focal_regime) in TRANSITIONS.items():
            reference_rows = grouped.get((taxon, group, reference_regime), [])
            focal_rows = grouped.get((taxon, group, focal_regime), [])
            if len(reference_rows) < min_images_per_regime or len(focal_rows) < min_images_per_regime:
                continue
            reference = [float(row["visual_salience_v1"]) for row in reference_rows]
            focal = [float(row["visual_salience_v1"]) for row in focal_rows]
            seed = sum(ord(character) for character in f"{taxon}|{transition}")
            delta, ci_low, ci_high = bootstrap_median_delta(reference, focal, seed=seed, draws=bootstrap_draws)
            output.append({
                "taxon": taxon,
                "analysis_group": group,
                "feature_id": "visual_salience_v1",
                "transition": transition,
                "reference_regime": reference_regime,
                "focal_regime": focal_regime,
                "n_reference_images": len(reference),
                "n_focal_images": len(focal),
                "reference_median": median(reference),
                "focal_median": median(focal),
                "delta_focal_minus_reference": delta,
                "bootstrap_ci90_low": ci_low,
                "bootstrap_ci90_high": ci_high,
                "point_direction": observed_direction(delta, tolerance),
                "tolerance": tolerance,
                "evidence_tier": "exploratory_public_image_signature",
            })
    return output


def summarize_group_signatures(contrasts: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    """Summarise taxon-level, not image-level, directional information."""
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in contrasts:
        grouped[(str(row["analysis_group"]), str(row["transition"]))].append(row)
    summary: list[dict[str, object]] = []
    for (group, transition), rows in sorted(grouped.items()):
        deltas = [float(row["delta_focal_minus_reference"]) for row in rows]
        directions = defaultdict(int)
        for row in rows:
            directions[str(row["point_direction"])] += 1
        summary.append({
            "analysis_group": group,
            "transition": transition,
            "taxa_contributing": len(rows),
            "median_taxon_delta": median(deltas),
            "taxa_decrease": directions["decrease"],
            "taxa_flat": directions["flat"],
            "taxa_increase": directions["increase"],
            "boundary": "Taxa are the aggregation unit. This is descriptive image-signature evidence, not a meta-analytic causal effect.",
        })
    return summary
