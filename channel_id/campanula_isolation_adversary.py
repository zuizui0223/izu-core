"""Audit mainland isolation as an adversary to the staged Campanula profile.

This module adds one measured-geography adversary that was missing from the
climate-only audit: great-circle distance from the frozen mainland geographic
anchor in ``data/design/izu_regime_scaffold.csv``.

The analysis is intentionally island-only.  The Honshu floral-size calibration
value in the source table is not assigned the scaffold anchor coordinate, because
the biological measurement locality and the geographic anchor are not the same
thing.  The mainland row supplies only the coordinate from which island isolation
is calculated.

For each adopted Campanula channel the audit compares four simple response shapes:

* null;
* ordinal island-order cline;
* mainland-distance cline; and
* the predeclared Oshima-to-Toshima second step.

It is an adversary/compatibility audit, not a historical dispersal model or a
causal estimate of pollinator loss.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence


TRAITS = (
    ("flower_length_mm", "floral_size"),
    ("outcrossing_midpoint", "outcrossing"),
    ("bagged_capsule_set_proportion", "autonomous_assurance"),
)
MODEL_IDS = ("null", "island_order_cline", "mainland_distance_cline", "oshima_to_toshima_step")
STEP_FOCAL_START_ORDER = 2
EARTH_RADIUS_KM = 6371.0088

ISLAND_TO_SCAFFOLD = {
    "Oshima": "izu_oshima",
    "Toshima": "toshima",
    "Niijima": "niijima",
    "Kozushima": "kozushima",
    "Miyake": "miyakejima",
    "Hachijo": "hachijojima",
}


@dataclass(frozen=True)
class IslandObservation:
    island_id: str
    order: int
    mainland_distance_km: float
    flower_length_mm: float | None
    outcrossing_midpoint: float | None
    bagged_capsule_set_proportion: float | None


@dataclass(frozen=True)
class TraitFit:
    trait_id: str
    trait_family: str
    model_id: str
    n: int
    parameter_count: int
    rss: float
    aicc: float | None
    loo_mse: float | None
    loo_kind: str


@dataclass(frozen=True)
class CompositeFit:
    model_id: str
    channel_models: tuple[str, ...]
    composite_aicc: float | None
    channels_ranked: int


def _clean(value: object) -> str:
    return str(value or "").strip()


def _optional_float(value: object) -> float | None:
    text = _clean(value)
    return None if not text else float(text)


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def _great_circle_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    value = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    return 2.0 * EARTH_RADIUS_KM * math.asin(math.sqrt(value))


def load_scaffold_distances(path: str | Path) -> tuple[dict[str, float], tuple[float, float]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"unit_id", "unit_type", "latitude_seed", "longitude_seed"}
    if not rows:
        raise ValueError("Izu regime scaffold is empty")
    missing = sorted(required.difference(rows[0]))
    if missing:
        raise ValueError("Izu regime scaffold missing columns: " + ", ".join(missing))

    mainland = [row for row in rows if _clean(row["unit_type"]) == "mainland_reference"]
    if len(mainland) != 1:
        raise ValueError("Izu regime scaffold must contain exactly one mainland_reference")
    anchor = (float(mainland[0]["latitude_seed"]), float(mainland[0]["longitude_seed"]))

    distances: dict[str, float] = {}
    for row in rows:
        unit_id = _clean(row["unit_id"])
        if _clean(row["unit_type"]) != "island":
            continue
        if unit_id in distances:
            raise ValueError(f"duplicate scaffold unit_id: {unit_id}")
        distances[unit_id] = _great_circle_km(
            anchor[0], anchor[1], float(row["latitude_seed"]), float(row["longitude_seed"])
        )
    return distances, anchor


def load_observations(
    trait_path: str | Path,
    scaffold_path: str | Path,
) -> tuple[tuple[IslandObservation, ...], tuple[float, float]]:
    distances, anchor = load_scaffold_distances(scaffold_path)
    with Path(trait_path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "island_id", "region_order", "flower_length_mm", "outcrossing_rate_min",
        "outcrossing_rate_max", "bagged_capsule_set_pct",
    }
    if not rows:
        raise ValueError("Campanula trait table is empty")
    missing = sorted(required.difference(rows[0]))
    if missing:
        raise ValueError("Campanula trait table missing columns: " + ", ".join(missing))

    output: list[IslandObservation] = []
    for row in rows:
        island = _clean(row["island_id"])
        if island == "Honshu":
            continue
        scaffold_id = ISLAND_TO_SCAFFOLD.get(island)
        if scaffold_id is None:
            continue
        if scaffold_id not in distances:
            raise ValueError(f"missing scaffold distance for {island}: {scaffold_id}")
        out_min = _optional_float(row["outcrossing_rate_min"])
        out_max = _optional_float(row["outcrossing_rate_max"])
        if (out_min is None) != (out_max is None):
            raise ValueError(f"{island}: outcrossing interval must provide both bounds or neither")
        bagged_pct = _optional_float(row["bagged_capsule_set_pct"])
        output.append(IslandObservation(
            island_id=island,
            order=int(_clean(row["region_order"])),
            mainland_distance_km=distances[scaffold_id],
            flower_length_mm=_optional_float(row["flower_length_mm"]),
            outcrossing_midpoint=None if out_min is None else (out_min + out_max) / 2.0,
            bagged_capsule_set_proportion=None if bagged_pct is None else bagged_pct / 100.0,
        ))
    output.sort(key=lambda row: row.order)
    if not output or output[0].island_id != "Oshima":
        raise ValueError("island-only Campanula series must begin with Oshima")
    return tuple(output), anchor


def _linear_prediction(x: Sequence[float], y: Sequence[float], train: Sequence[bool]) -> list[float]:
    xx = [x[index] for index, use in enumerate(train) if use]
    yy = [y[index] for index, use in enumerate(train) if use]
    xbar, ybar = _mean(xx), _mean(yy)
    denominator = sum((value - xbar) ** 2 for value in xx)
    if denominator == 0:
        return [ybar for _ in x]
    slope = sum((xx[index] - xbar) * (yy[index] - ybar) for index in range(len(xx))) / denominator
    intercept = ybar - slope * xbar
    return [intercept + slope * value for value in x]


def _null_prediction(_: Sequence[float], y: Sequence[float], train: Sequence[bool]) -> list[float]:
    centre = _mean([y[index] for index, use in enumerate(train) if use])
    return [centre for _ in y]


def _step_prediction(order: Sequence[float], y: Sequence[float], train: Sequence[bool]) -> list[float]:
    baseline = [y[index] for index, use in enumerate(train) if use and order[index] < STEP_FOCAL_START_ORDER]
    focal = [y[index] for index, use in enumerate(train) if use and order[index] >= STEP_FOCAL_START_ORDER]
    if not baseline or not focal:
        return [float("nan") for _ in y]
    baseline_mean, focal_mean = _mean(baseline), _mean(focal)
    return [baseline_mean if value < STEP_FOCAL_START_ORDER else focal_mean for value in order]


def _aicc(y: Sequence[float], prediction: Sequence[float], k: int) -> float | None:
    n = len(y)
    if n <= k + 1:
        return None
    rss = max(sum((y[index] - prediction[index]) ** 2 for index in range(n)), 1e-15)
    log_likelihood = -n / 2.0 * (math.log(2.0 * math.pi) + 1.0 + math.log(rss / n))
    aic = 2.0 * k - 2.0 * log_likelihood
    return aic + 2.0 * k * (k + 1.0) / (n - k - 1.0)


def _loo_mse(
    x: Sequence[float],
    y: Sequence[float],
    predictor: Callable[[Sequence[float], Sequence[float], Sequence[bool]], list[float]],
    *,
    conditional_step: bool = False,
) -> float | None:
    errors: list[float] = []
    for held_out in range(len(y)):
        if conditional_step and x[held_out] < STEP_FOCAL_START_ORDER:
            continue
        train = [index != held_out for index in range(len(y))]
        prediction = predictor(x, y, train)
        if math.isnan(prediction[held_out]):
            continue
        errors.append((y[held_out] - prediction[held_out]) ** 2)
    return _mean(errors) if errors else None


def fit_trait_models(rows: Sequence[IslandObservation]) -> tuple[TraitFit, ...]:
    output: list[TraitFit] = []
    for trait_id, trait_family in TRAITS:
        selected = [row for row in rows if getattr(row, trait_id) is not None]
        y = [float(getattr(row, trait_id)) for row in selected]
        order = [float(row.order) for row in selected]
        distance = [row.mainland_distance_km for row in selected]
        if len(y) < 4:
            raise ValueError(f"{trait_id}: too few island observations")
        specifications = (
            ("null", [0.0] * len(y), _null_prediction, 1, False),
            ("island_order_cline", order, _linear_prediction, 2, False),
            ("mainland_distance_cline", distance, _linear_prediction, 2, False),
            ("oshima_to_toshima_step", order, _step_prediction, 2, True),
        )
        for model_id, x, predictor, k, conditional_step in specifications:
            prediction = predictor(x, y, [True] * len(y))
            rss = sum((y[index] - prediction[index]) ** 2 for index in range(len(y)))
            output.append(TraitFit(
                trait_id=trait_id,
                trait_family=trait_family,
                model_id=model_id,
                n=len(y),
                parameter_count=k,
                rss=rss,
                aicc=_aicc(y, prediction, k),
                loo_mse=_loo_mse(x, y, predictor, conditional_step=conditional_step),
                loo_kind="leave_no_bombus_out" if conditional_step else "leave_one_island_out",
            ))
    return tuple(output)


def composite_fits(fits: Iterable[TraitFit]) -> tuple[CompositeFit, ...]:
    indexed = {(fit.trait_id, fit.model_id): fit for fit in fits}
    ordered_traits = [trait_id for trait_id, _ in TRAITS]
    specifications = {
        "null": ("null", "null", "null"),
        "single_island_order": ("island_order_cline",) * 3,
        "single_mainland_distance": ("mainland_distance_cline",) * 3,
        "two_stage_order_hybrid": (
            "island_order_cline", "island_order_cline", "oshima_to_toshima_step",
        ),
        "two_stage_distance_hybrid": (
            "mainland_distance_cline", "mainland_distance_cline", "oshima_to_toshima_step",
        ),
    }
    output: list[CompositeFit] = []
    for model_id, channel_models in specifications.items():
        selected = [indexed[(trait_id, channel)] for trait_id, channel in zip(ordered_traits, channel_models)]
        valid = [fit.aicc for fit in selected if fit.aicc is not None]
        output.append(CompositeFit(
            model_id=model_id,
            channel_models=channel_models,
            composite_aicc=sum(valid) if len(valid) == len(selected) else None,
            channels_ranked=len(valid),
        ))
    return tuple(sorted(
        output,
        key=lambda fit: (
            fit.composite_aicc is None,
            fit.composite_aicc if fit.composite_aicc is not None else math.inf,
        ),
    ))


def run_audit(
    trait_path: str | Path,
    scaffold_path: str | Path,
) -> dict[str, object]:
    rows, anchor = load_observations(trait_path, scaffold_path)
    fits = fit_trait_models(rows)
    composites = composite_fits(fits)
    return {
        "mainland_anchor": {"latitude": anchor[0], "longitude": anchor[1]},
        "island_distances_km": {row.island_id: row.mainland_distance_km for row in rows},
        "trait_fits": [asdict(fit) for fit in fits],
        "composite_fits": [asdict(fit) for fit in composites],
        "best_composite": composites[0].model_id if composites and composites[0].composite_aicc is not None else None,
        "claim_boundary": (
            "Mainland great-circle distance is a measured geographic-isolation adversary only. "
            "A poor distance fit does not reject all environment, demography, colonisation history, "
            "or unmeasured geographic structure; a step fit does not establish pollinator causation."
        ),
    }


def write_outputs(output_dir: str | Path, result: dict[str, object]) -> None:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    trait_rows = result["trait_fits"]
    with (destination / "trait_model_fits.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = ("trait_id", "trait_family", "model_id", "n", "parameter_count", "rss", "aicc", "loo_mse", "loo_kind")
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(trait_rows)

    composite_rows = []
    for row in result["composite_fits"]:
        composite_rows.append({
            "model_id": row["model_id"],
            "flower_length_mm_model": row["channel_models"][0],
            "outcrossing_midpoint_model": row["channel_models"][1],
            "bagged_capsule_set_proportion_model": row["channel_models"][2],
            "composite_aicc": row["composite_aicc"],
            "channels_ranked": row["channels_ranked"],
        })
    with (destination / "composite_model_fits.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = (
            "model_id", "flower_length_mm_model", "outcrossing_midpoint_model",
            "bagged_capsule_set_proportion_model", "composite_aicc", "channels_ranked",
        )
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(composite_rows)
