"""Compare a single observed climate axis with a staged channel profile.

This is a deliberately limited *adversary audit*, not a causal pollinator
model.  It asks a narrower question using only the source-locked Campanula
summary table:

Can one observed environmental axis (PC1 of island mean temperature, annual
precipitation, and precipitation CV) reproduce the three empirical channels as
well as a descriptive hybrid profile in which flower length and outcrossing
change along the island order while bagged autonomous capacity changes at the
Oshima--Toshima boundary?

The answer is informative but bounded.  A poor fit of this PC1 does not reject
all environmental mechanisms; a good fit of the hybrid does not identify a
historical Bombus event.  The analysis is a transparent requirement test for
what an environment-only explanation must reproduce.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence


TRAITS = (
    ("flower_length_mm", "flower_length_mm", "floral_size"),
    ("outcrossing_midpoint", "outcrossing_midpoint", "outcrossing"),
    ("bagged_capsule_set_proportion", "bagged_capsule_set_proportion", "autonomous_assurance"),
)
ENV_COLUMNS = ("mean_temp_c", "annual_precip_mm", "precip_cv")
STEP_BASELINE = "Oshima"
STEP_FOCAL_START_ORDER = 2  # Toshima; keeps Oshima in the B. ardens proxy state.


@dataclass(frozen=True)
class IslandRow:
    island_id: str
    region_order: int
    flower_length_mm: float | None
    outcrossing_midpoint: float | None
    bagged_capsule_set_proportion: float | None
    mean_temp_c: float | None
    annual_precip_mm: float | None
    precip_cv: float | None


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
    if not text:
        return None
    return float(text)


def load_island_rows(path: str | Path) -> tuple[IslandRow, ...]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "island_id", "region_order", "bagged_capsule_set_pct", "outcrossing_rate_min",
        "outcrossing_rate_max", "flower_length_mm", *ENV_COLUMNS,
    }
    if not rows:
        raise ValueError("island trait table is empty")
    missing = sorted(required.difference(rows[0]))
    if missing:
        raise ValueError("island trait table missing columns: " + ", ".join(missing))
    output: list[IslandRow] = []
    seen: set[str] = set()
    for raw in rows:
        island = _clean(raw["island_id"])
        if island in seen:
            raise ValueError(f"duplicate island_id: {island}")
        seen.add(island)
        out_min = _optional_float(raw["outcrossing_rate_min"])
        out_max = _optional_float(raw["outcrossing_rate_max"])
        if (out_min is None) != (out_max is None):
            raise ValueError(f"{island}: outcrossing interval must provide both bounds or neither")
        output.append(IslandRow(
            island_id=island,
            region_order=int(_clean(raw["region_order"])),
            flower_length_mm=_optional_float(raw["flower_length_mm"]),
            outcrossing_midpoint=None if out_min is None else (out_min + out_max) / 2.0,
            bagged_capsule_set_proportion=(None if _optional_float(raw["bagged_capsule_set_pct"]) is None else _optional_float(raw["bagged_capsule_set_pct"]) / 100.0),
            mean_temp_c=_optional_float(raw["mean_temp_c"]),
            annual_precip_mm=_optional_float(raw["annual_precip_mm"]),
            precip_cv=_optional_float(raw["precip_cv"]),
        ))
    return tuple(sorted(output, key=lambda row: row.region_order))


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def _sample_sd(values: Sequence[float]) -> float:
    if len(values) < 2:
        raise ValueError("at least two values required for standardisation")
    mean = _mean(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / (len(values) - 1))


def _symmetric_eigenvector_3x3(matrix: list[list[float]], iterations: int = 200) -> list[float]:
    """Power iteration for the leading eigenvector of a 3×3 symmetric matrix."""
    vector = [1.0, 1.0, 1.0]
    for _ in range(iterations):
        candidate = [sum(matrix[i][j] * vector[j] for j in range(3)) for i in range(3)]
        norm = math.sqrt(sum(value * value for value in candidate))
        if norm == 0:
            raise ValueError("environment covariance matrix is singular")
        vector = [value / norm for value in candidate]
    # Orient PC1 so warmer/wetter, lower-variability conditions have negative score
    # only for stable reporting; sign has no effect on fitted likelihoods.
    if vector[0] > 0:
        vector = [-value for value in vector]
    return vector


def climate_pc1(rows: Iterable[IslandRow]) -> tuple[dict[str, float], dict[str, float]]:
    """Return island PC1 and loadings using only rows with all three climate fields."""
    available = [row for row in rows if all(getattr(row, field) is not None for field in ENV_COLUMNS)]
    if len(available) < 4:
        raise ValueError("at least four islands with all climate covariates are required")
    raw = [[float(getattr(row, field)) for field in ENV_COLUMNS] for row in available]
    means = [_mean([record[index] for record in raw]) for index in range(3)]
    sds = [_sample_sd([record[index] for record in raw]) for index in range(3)]
    standardized = [[(record[index] - means[index]) / sds[index] for index in range(3)] for record in raw]
    covariance = [
        [sum(record[i] * record[j] for record in standardized) / (len(standardized) - 1) for j in range(3)]
        for i in range(3)
    ]
    vector = _symmetric_eigenvector_3x3(covariance)
    scores = {row.island_id: sum(standardized[index][j] * vector[j] for j in range(3)) for index, row in enumerate(available)}
    return scores, {ENV_COLUMNS[i]: vector[i] for i in range(3)}


def _linear_prediction(x: Sequence[float], y: Sequence[float], train: Sequence[bool]) -> list[float]:
    xx = [x[index] for index, use in enumerate(train) if use]
    yy = [y[index] for index, use in enumerate(train) if use]
    xbar, ybar = _mean(xx), _mean(yy)
    denominator = sum((value - xbar) ** 2 for value in xx)
    if denominator == 0:
        return [ybar for _ in x]
    slope = sum((xx[i] - xbar) * (yy[i] - ybar) for i in range(len(xx))) / denominator
    intercept = ybar - slope * xbar
    return [intercept + slope * value for value in x]


def _null_prediction(_: Sequence[float], y: Sequence[float], train: Sequence[bool]) -> list[float]:
    mean = _mean([y[index] for index, use in enumerate(train) if use])
    return [mean for _ in y]


def _oshima_step_prediction(order: Sequence[float], y: Sequence[float], train: Sequence[bool]) -> list[float]:
    baseline = [y[i] for i, use in enumerate(train) if use and order[i] < STEP_FOCAL_START_ORDER]
    focal = [y[i] for i, use in enumerate(train) if use and order[i] >= STEP_FOCAL_START_ORDER]
    if not baseline or not focal:
        return [float("nan") for _ in y]
    baseline_mean, focal_mean = _mean(baseline), _mean(focal)
    return [baseline_mean if value < STEP_FOCAL_START_ORDER else focal_mean for value in order]


def _aicc(y: Sequence[float], prediction: Sequence[float], k: int) -> float | None:
    n = len(y)
    if n <= k + 1:
        return None
    rss = sum((y[i] - prediction[i]) ** 2 for i in range(n))
    rss = max(rss, 1e-15)
    log_likelihood = -n / 2.0 * (math.log(2.0 * math.pi) + 1.0 + math.log(rss / n))
    aic = 2.0 * k - 2.0 * log_likelihood
    return aic + 2.0 * k * (k + 1.0) / (n - k - 1.0)


def _loo_mse(x: Sequence[float], y: Sequence[float], predictor: Callable[[Sequence[float], Sequence[float], Sequence[bool]], list[float]], conditional_step: bool = False) -> float | None:
    errors: list[float] = []
    for held_out in range(len(y)):
        # A step model cannot predict a held-out sole baseline state.  Its useful
        # CV target is generalisation to an additional focal/no-Bombus island.
        if conditional_step and x[held_out] < STEP_FOCAL_START_ORDER:
            continue
        train = [index != held_out for index in range(len(y))]
        prediction = predictor(x, y, train)
        if math.isnan(prediction[held_out]):
            continue
        errors.append((y[held_out] - prediction[held_out]) ** 2)
    return _mean(errors) if errors else None


def _trait_values(rows: Sequence[IslandRow], attribute: str, climate_scores: dict[str, float] | None = None) -> tuple[list[IslandRow], list[float], list[float], list[float]]:
    selected = [row for row in rows if getattr(row, attribute) is not None and (climate_scores is None or row.island_id in climate_scores)]
    values = [float(getattr(row, attribute)) for row in selected]
    order = [float(row.region_order) for row in selected]
    climate = [float(climate_scores[row.island_id]) for row in selected] if climate_scores is not None else []
    return selected, values, order, climate


def fit_channel_models(rows: Sequence[IslandRow]) -> tuple[tuple[TraitFit, ...], dict[str, float]]:
    climate_scores, loadings = climate_pc1(rows)
    output: list[TraitFit] = []
    for trait_id, attribute, family in TRAITS:
        selected, y, order, climate = _trait_values(rows, attribute, climate_scores)
        if len(y) < 4:
            raise ValueError(f"{trait_id}: too few source-locked observations")
        specs = (
            ("null", [0.0 for _ in y], _null_prediction, 1, False),
            ("climate_pc1_cline", climate, _linear_prediction, 2, False),
            ("island_order_cline", order, _linear_prediction, 2, False),
            ("oshima_to_toshima_step", order, _oshima_step_prediction, 2, True),
        )
        for model_id, x, predictor, k, is_step in specs:
            prediction = predictor(x, y, [True] * len(y))
            rss = sum((y[index] - prediction[index]) ** 2 for index in range(len(y)))
            output.append(TraitFit(
                trait_id=trait_id, trait_family=family, model_id=model_id, n=len(y),
                parameter_count=k, rss=rss, aicc=_aicc(y, prediction, k),
                loo_mse=_loo_mse(x, y, predictor, conditional_step=is_step),
                loo_kind="leave_no_bombus_out" if is_step else "leave_one_island_out",
            ))
    return tuple(output), loadings


def composite_fits(trait_fits: Iterable[TraitFit]) -> tuple[CompositeFit, ...]:
    indexed = {(fit.trait_id, fit.model_id): fit for fit in trait_fits}
    specifications = {
        "null": ("null", "null", "null"),
        "single_climate_pc1": ("climate_pc1_cline", "climate_pc1_cline", "climate_pc1_cline"),
        "single_island_order": ("island_order_cline", "island_order_cline", "island_order_cline"),
        "two_stage_hybrid": ("island_order_cline", "island_order_cline", "oshima_to_toshima_step"),
    }
    output: list[CompositeFit] = []
    ordered_traits = [item[0] for item in TRAITS]
    for model_id, channels in specifications.items():
        selected = [indexed[(trait, channel)] for trait, channel in zip(ordered_traits, channels)]
        valid = [fit.aicc for fit in selected if fit.aicc is not None]
        output.append(CompositeFit(
            model_id=model_id, channel_models=channels,
            composite_aicc=sum(valid) if len(valid) == len(selected) else None,
            channels_ranked=len(valid),
        ))
    return tuple(sorted(output, key=lambda fit: (fit.composite_aicc is None, fit.composite_aicc if fit.composite_aicc is not None else math.inf)))


def write_outputs(output_dir: str | Path, fits: Sequence[TraitFit], composites: Sequence[CompositeFit], loadings: dict[str, float]) -> None:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "trait_model_fits.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("trait_id", "trait_family", "model_id", "n", "parameter_count", "rss", "aicc", "loo_mse", "loo_kind"))
        writer.writeheader()
        for fit in fits:
            writer.writerow({
                "trait_id": fit.trait_id, "trait_family": fit.trait_family, "model_id": fit.model_id,
                "n": fit.n, "parameter_count": fit.parameter_count, "rss": f"{fit.rss:.12g}",
                "aicc": "" if fit.aicc is None else f"{fit.aicc:.12g}",
                "loo_mse": "" if fit.loo_mse is None else f"{fit.loo_mse:.12g}",
                "loo_kind": fit.loo_kind,
            })
    with (destination / "composite_model_fits.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("model_id", "flower_length_mm_model", "outcrossing_midpoint_model", "bagged_capsule_set_proportion_model", "composite_aicc", "channels_ranked"))
        writer.writeheader()
        for fit in composites:
            writer.writerow({
                "model_id": fit.model_id,
                "flower_length_mm_model": fit.channel_models[0],
                "outcrossing_midpoint_model": fit.channel_models[1],
                "bagged_capsule_set_proportion_model": fit.channel_models[2],
                "composite_aicc": "" if fit.composite_aicc is None else f"{fit.composite_aicc:.12g}",
                "channels_ranked": fit.channels_ranked,
            })
    summary = {
        "climate_pc1_loadings": loadings,
        "best_composite": composites[0].model_id if composites else None,
        "boundary": (
            "Descriptive source-locked channel-shape audit. Climate PC1 is limited to the three measured island covariates and does not represent all environmental or historical alternatives. Island order is an ordinal scaffold, not a causal exposure. Composite AICc values are a channel-wise diagnostic, not Bayes factors or causal evidence."
        ),
    }
    (destination / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def render_markdown(fits: Sequence[TraitFit], composites: Sequence[CompositeFit], loadings: dict[str, float]) -> str:
    lines = [
        "# Campanula environmental-adversary audit",
        "",
        "This is a descriptive comparison of four low-parameter channel shapes. It does not identify pollinator causality or reject unmeasured environmental/history mechanisms.",
        "",
        "## Climate axis",
        "",
        "PC1 uses mean temperature, annual precipitation, and precipitation CV for the six Izu islands with all three values. Loadings:",
        "",
    ]
    for key, value in loadings.items():
        lines.append(f"- `{key}`: {value:.4f}")
    lines.extend((
        "", "## Channel fits", "",
        "| trait | model | n | AICc | cross-validation MSE | CV target |",
        "|---|---|---:|---:|---:|---|",
    ))
    for fit in sorted(fits, key=lambda item: (item.trait_id, item.aicc is None, item.aicc if item.aicc is not None else math.inf)):
        lines.append(
            f"| {fit.trait_id} | {fit.model_id} | {fit.n} | "
            f"{'NA' if fit.aicc is None else f'{fit.aicc:.3f}'} | "
            f"{'NA' if fit.loo_mse is None else f'{fit.loo_mse:.6g}'} | {fit.loo_kind} |"
        )
    lines.extend((
        "", "## Composite channel diagnostic", "",
        "| composite profile | flower length | outcrossing | bagged capsule set | composite AICc |", "|---|---|---|---|---:|",
    ))
    for fit in composites:
        lines.append(
            f"| {fit.model_id} | {fit.channel_models[0]} | {fit.channel_models[1]} | {fit.channel_models[2]} | "
            f"{'NA' if fit.composite_aicc is None else f'{fit.composite_aicc:.3f}'} |"
        )
    lines.extend((
        "", "## Interpretation boundary", "",
        "The only step model is the Oshima-to-Toshima contrast. Its cross-validation target omits the sole Oshima baseline and therefore asks whether the step generalises to additional no-Bombus islands; it is not a symmetric leave-one-island-out test. The climate model uses only observed island climate covariates and cannot rule out unmeasured environmental or colonisation-history mechanisms.",
    ))
    return "\n".join(lines) + "\n"
