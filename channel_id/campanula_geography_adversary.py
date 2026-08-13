"""Audit measured island area and connectivity as Campanula geography adversaries.

This extends the straight-line mainland-distance audit without pretending that a
single geographic proxy is demographic history.  All nine island areas come from
the same frozen GSHHG 2.3.7 polygon source.  Coordinates come from the frozen Izu
regime scaffold.  The module derives three outcome-independent geography axes:

* mainland great-circle distance;
* log island area;
* nearest-island centroid distance.

It also defines a declared equal-weight ``geography_pressure_index`` from
standardised mainland distance, negative log area, and nearest-island distance.
The standardisation is performed on the full nine-island universe before the
Campanula response table is joined, so the response cannot tune the index.

The audit is a compatibility/adversary analysis.  It does not estimate gene flow,
founder history, habitat similarity, volcanic disturbance, or pollinator effects.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence


EARTH_RADIUS_KM = 6371.0088
STEP_FOCAL_START_ORDER = 2
TRAITS = (
    ("flower_length_mm", "floral_size"),
    ("outcrossing_midpoint", "outcrossing"),
    ("bagged_capsule_set_proportion", "autonomous_assurance"),
)
ISLAND_TO_SCAFFOLD = {
    "Oshima": "izu_oshima",
    "Toshima": "toshima",
    "Niijima": "niijima",
    "Kozushima": "kozushima",
    "Miyake": "miyakejima",
    "Hachijo": "hachijojima",
}


@dataclass(frozen=True)
class GeographyAxis:
    unit_id: str
    order: int
    latitude: float
    longitude: float
    area_km2: float
    log_area: float
    mainland_distance_km: float
    nearest_island_distance_km: float
    geography_pressure_index: float


@dataclass(frozen=True)
class IslandObservation:
    island_id: str
    unit_id: str
    order: int
    mainland_distance_km: float
    log_area: float
    nearest_island_distance_km: float
    geography_pressure_index: float
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


def _sample_sd(values: Sequence[float]) -> float:
    if len(values) < 2:
        raise ValueError("at least two values required for standardisation")
    centre = _mean(values)
    sd = math.sqrt(sum((value - centre) ** 2 for value in values) / (len(values) - 1))
    if sd <= 0:
        raise ValueError("cannot standardise a constant geography covariate")
    return sd


def _standardise(values: Sequence[float]) -> list[float]:
    centre = _mean(values)
    sd = _sample_sd(values)
    return [(value - centre) / sd for value in values]


def _great_circle_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    value = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    return 2.0 * EARTH_RADIUS_KM * math.asin(math.sqrt(value))


def load_area_table(path: str | Path) -> dict[str, float]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("Izu geography covariate table is empty")
    required = {"unit_id", "area_km2", "area_source", "source_locator", "source_commit"}
    missing = sorted(required.difference(rows[0]))
    if missing:
        raise ValueError("Izu geography covariate table missing columns: " + ", ".join(missing))
    output: dict[str, float] = {}
    for row in rows:
        unit_id = _clean(row["unit_id"])
        if not unit_id or unit_id in output:
            raise ValueError("geography unit_id values must be non-empty and unique")
        area = float(row["area_km2"])
        if area <= 0:
            raise ValueError(f"{unit_id}: area_km2 must be positive")
        if not _clean(row["area_source"]) or not _clean(row["source_locator"]) or not _clean(row["source_commit"]):
            raise ValueError(f"{unit_id}: area provenance fields are required")
        output[unit_id] = area
    return output


def build_geography_axes(
    scaffold_path: str | Path,
    geography_path: str | Path,
) -> tuple[tuple[GeographyAxis, ...], tuple[float, float]]:
    areas = load_area_table(geography_path)
    with Path(scaffold_path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"unit_id", "unit_type", "sequence_order", "latitude_seed", "longitude_seed"}
    if not rows:
        raise ValueError("Izu regime scaffold is empty")
    missing = sorted(required.difference(rows[0]))
    if missing:
        raise ValueError("Izu regime scaffold missing columns: " + ", ".join(missing))

    mainland = [row for row in rows if _clean(row["unit_type"]) == "mainland_reference"]
    if len(mainland) != 1:
        raise ValueError("Izu regime scaffold must contain exactly one mainland_reference")
    anchor = (float(mainland[0]["latitude_seed"]), float(mainland[0]["longitude_seed"]))

    islands = [row for row in rows if _clean(row["unit_type"]) == "island"]
    if len(islands) != 9:
        raise ValueError(f"expected nine islands in scaffold, found {len(islands)}")
    scaffold_ids = {_clean(row["unit_id"]) for row in islands}
    if scaffold_ids != set(areas):
        missing_area = sorted(scaffold_ids - set(areas))
        extra_area = sorted(set(areas) - scaffold_ids)
        raise ValueError(f"geography/scaffold mismatch; missing_area={missing_area}; extra_area={extra_area}")

    islands = sorted(islands, key=lambda row: int(row["sequence_order"]))
    preliminary = []
    for row in islands:
        unit_id = _clean(row["unit_id"])
        latitude = float(row["latitude_seed"])
        longitude = float(row["longitude_seed"])
        preliminary.append({
            "unit_id": unit_id,
            "order": int(row["sequence_order"]),
            "latitude": latitude,
            "longitude": longitude,
            "area_km2": areas[unit_id],
            "log_area": math.log(areas[unit_id]),
            "mainland_distance_km": _great_circle_km(anchor[0], anchor[1], latitude, longitude),
        })

    nearest = []
    for row in preliminary:
        distances = [
            _great_circle_km(row["latitude"], row["longitude"], other["latitude"], other["longitude"])
            for other in preliminary
            if other["unit_id"] != row["unit_id"]
        ]
        nearest.append(min(distances))

    z_mainland = _standardise([float(row["mainland_distance_km"]) for row in preliminary])
    z_log_area = _standardise([float(row["log_area"]) for row in preliminary])
    z_nearest = _standardise(nearest)

    output = []
    for index, row in enumerate(preliminary):
        pressure = (z_mainland[index] - z_log_area[index] + z_nearest[index]) / 3.0
        output.append(GeographyAxis(
            unit_id=str(row["unit_id"]),
            order=int(row["order"]),
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            area_km2=float(row["area_km2"]),
            log_area=float(row["log_area"]),
            mainland_distance_km=float(row["mainland_distance_km"]),
            nearest_island_distance_km=float(nearest[index]),
            geography_pressure_index=float(pressure),
        ))
    return tuple(output), anchor


def load_observations(
    trait_path: str | Path,
    scaffold_path: str | Path,
    geography_path: str | Path,
) -> tuple[tuple[IslandObservation, ...], tuple[GeographyAxis, ...]]:
    axes, _ = build_geography_axes(scaffold_path, geography_path)
    axis_by_id = {row.unit_id: row for row in axes}
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

    output = []
    for row in rows:
        island = _clean(row["island_id"])
        if island == "Honshu":
            continue
        unit_id = ISLAND_TO_SCAFFOLD.get(island)
        if unit_id is None:
            continue
        axis = axis_by_id.get(unit_id)
        if axis is None:
            raise ValueError(f"missing geography axis for {island}: {unit_id}")
        out_min = _optional_float(row["outcrossing_rate_min"])
        out_max = _optional_float(row["outcrossing_rate_max"])
        if (out_min is None) != (out_max is None):
            raise ValueError(f"{island}: outcrossing interval must provide both bounds or neither")
        bagged_pct = _optional_float(row["bagged_capsule_set_pct"])
        output.append(IslandObservation(
            island_id=island,
            unit_id=unit_id,
            order=int(_clean(row["region_order"])),
            mainland_distance_km=axis.mainland_distance_km,
            log_area=axis.log_area,
            nearest_island_distance_km=axis.nearest_island_distance_km,
            geography_pressure_index=axis.geography_pressure_index,
            flower_length_mm=_optional_float(row["flower_length_mm"]),
            outcrossing_midpoint=None if out_min is None else (out_min + out_max) / 2.0,
            bagged_capsule_set_proportion=None if bagged_pct is None else bagged_pct / 100.0,
        ))
    output.sort(key=lambda row: row.order)
    if not output or output[0].island_id != "Oshima":
        raise ValueError("island-only Campanula series must begin with Oshima")
    return tuple(output), axes


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
    errors = []
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
    output = []
    for trait_id, trait_family in TRAITS:
        selected = [row for row in rows if getattr(row, trait_id) is not None]
        y = [float(getattr(row, trait_id)) for row in selected]
        order = [float(row.order) for row in selected]
        if len(y) < 4:
            raise ValueError(f"{trait_id}: too few island observations")
        specifications = (
            ("null", [0.0] * len(y), _null_prediction, 1, False),
            ("island_order_cline", order, _linear_prediction, 2, False),
            ("mainland_distance_cline", [row.mainland_distance_km for row in selected], _linear_prediction, 2, False),
            ("log_area_cline", [row.log_area for row in selected], _linear_prediction, 2, False),
            ("nearest_island_distance_cline", [row.nearest_island_distance_km for row in selected], _linear_prediction, 2, False),
            ("geography_pressure_cline", [row.geography_pressure_index for row in selected], _linear_prediction, 2, False),
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
    traits = [trait_id for trait_id, _ in TRAITS]
    specifications = {
        "null": ("null",) * 3,
        "single_island_order": ("island_order_cline",) * 3,
        "single_mainland_distance": ("mainland_distance_cline",) * 3,
        "single_log_area": ("log_area_cline",) * 3,
        "single_nearest_island_distance": ("nearest_island_distance_cline",) * 3,
        "single_geography_pressure": ("geography_pressure_cline",) * 3,
        "two_stage_order_hybrid": ("island_order_cline", "island_order_cline", "oshima_to_toshima_step"),
        "two_stage_distance_hybrid": ("mainland_distance_cline", "mainland_distance_cline", "oshima_to_toshima_step"),
        "two_stage_area_hybrid": ("log_area_cline", "log_area_cline", "oshima_to_toshima_step"),
        "two_stage_nearest_hybrid": ("nearest_island_distance_cline", "nearest_island_distance_cline", "oshima_to_toshima_step"),
        "two_stage_geography_hybrid": ("geography_pressure_cline", "geography_pressure_cline", "oshima_to_toshima_step"),
    }
    output = []
    for model_id, channel_models in specifications.items():
        selected = [indexed[(trait_id, model)] for trait_id, model in zip(traits, channel_models)]
        valid = [fit.aicc for fit in selected if fit.aicc is not None]
        output.append(CompositeFit(
            model_id=model_id,
            channel_models=channel_models,
            composite_aicc=sum(valid) if len(valid) == len(selected) else None,
            channels_ranked=len(valid),
        ))
    return tuple(sorted(output, key=lambda fit: (
        fit.composite_aicc is None,
        fit.composite_aicc if fit.composite_aicc is not None else math.inf,
    )))


def run_audit(
    trait_path: str | Path,
    scaffold_path: str | Path,
    geography_path: str | Path,
) -> dict[str, object]:
    rows, axes = load_observations(trait_path, scaffold_path, geography_path)
    fits = fit_trait_models(rows)
    composites = composite_fits(fits)
    return {
        "geography_axes": [asdict(row) for row in axes],
        "trait_fits": [asdict(row) for row in fits],
        "composite_fits": [asdict(row) for row in composites],
        "best_composite": composites[0].model_id if composites and composites[0].composite_aicc is not None else None,
        "claim_boundary": (
            "Area, mainland distance, nearest-island distance, and the declared equal-weight geography index "
            "are measured/static geography adversaries. Poor fit does not reject demographic history, "
            "stepping-stone gene flow, source-population identity, habitat, volcanism, or pollinator causation."
        ),
    }


def write_outputs(output_dir: str | Path, result: dict[str, object]) -> None:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "summary.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    with (destination / "geography_axes.csv").open("w", encoding="utf-8", newline="") as handle:
        rows = result["geography_axes"]
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]))
        writer.writeheader(); writer.writerows(rows)

    with (destination / "trait_model_fits.csv").open("w", encoding="utf-8", newline="") as handle:
        rows = result["trait_fits"]
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]))
        writer.writeheader(); writer.writerows(rows)

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
