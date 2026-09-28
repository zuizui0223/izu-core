"""Audit pre-observation volcanic disturbance as a Campanula history adversary.

The history snapshot is deliberately frozen at 1986-01-01, before the first
article in the retained Izu Campanula evidence programme.  Eruptions after that
cutoff are never allowed to explain earlier biological observations.  The aim is
not to reconstruct vegetation history, but to test a concrete alternative:
recent volcanic disturbance or time since the latest source-supported eruptive
event could covary with the island trait pattern.

Toshima's latest eruption is reported only as an interval (9100-4000 yr BP), so
the analysis keeps both interval endpoints as separate sensitivity cases rather
than inventing a midpoint.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence


STEP_FOCAL_START_ORDER = 2
TRAITS = (
    ("flower_length_mm", "floral_size"),
    ("outcrossing_midpoint", "outcrossing"),
    ("bagged_capsule_set_proportion", "autonomous_assurance"),
)
HISTORY_CASES = ("toshima_young_endpoint", "toshima_old_endpoint")


@dataclass(frozen=True)
class HistoryRecord:
    island_id: str
    cutoff_year: int
    latest_pre_cutoff_event: str
    eruption_age_min_years_at_cutoff: float
    eruption_age_max_years_at_cutoff: float
    event_scope: str
    source_authority: str
    source_url: str
    notes: str


@dataclass(frozen=True)
class IslandObservation:
    island_id: str
    order: int
    eruption_age_years: float
    log_eruption_age: float
    recent_100y_state: int
    flower_length_mm: float | None
    outcrossing_midpoint: float | None
    bagged_capsule_set_proportion: float | None


@dataclass(frozen=True)
class TraitFit:
    history_case: str
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
    history_case: str
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


def load_history(path: str | Path) -> dict[str, HistoryRecord]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "island_id", "cutoff_year", "latest_pre_cutoff_event",
        "eruption_age_min_years_at_cutoff", "eruption_age_max_years_at_cutoff",
        "event_scope", "source_authority", "source_url", "notes",
    }
    if not rows:
        raise ValueError("volcanic history table is empty")
    missing = sorted(required.difference(rows[0]))
    if missing:
        raise ValueError("volcanic history table missing columns: " + ", ".join(missing))
    output: dict[str, HistoryRecord] = {}
    for row in rows:
        island = _clean(row["island_id"])
        if not island or island in output:
            raise ValueError("volcanic history island_id values must be non-empty and unique")
        minimum = float(row["eruption_age_min_years_at_cutoff"])
        maximum = float(row["eruption_age_max_years_at_cutoff"])
        if minimum <= 0 or maximum < minimum:
            raise ValueError(f"{island}: invalid eruption-age interval")
        if int(row["cutoff_year"]) != 1986:
            raise ValueError(f"{island}: history cutoff must remain frozen at 1986")
        if not _clean(row["source_authority"]) or not _clean(row["source_url"]):
            raise ValueError(f"{island}: source authority and URL are required")
        output[island] = HistoryRecord(
            island_id=island,
            cutoff_year=1986,
            latest_pre_cutoff_event=_clean(row["latest_pre_cutoff_event"]),
            eruption_age_min_years_at_cutoff=minimum,
            eruption_age_max_years_at_cutoff=maximum,
            event_scope=_clean(row["event_scope"]),
            source_authority=_clean(row["source_authority"]),
            source_url=_clean(row["source_url"]),
            notes=_clean(row["notes"]),
        )
    expected = {"Oshima", "Toshima", "Niijima", "Kozushima", "Miyake", "Hachijo"}
    if set(output) != expected:
        raise ValueError(f"history table must contain exactly the six Campanula islands; got {sorted(output)}")
    return output


def _history_age(record: HistoryRecord, history_case: str) -> float:
    if history_case not in HISTORY_CASES:
        raise ValueError(f"unknown history case: {history_case}")
    if record.island_id != "Toshima":
        if record.eruption_age_min_years_at_cutoff != record.eruption_age_max_years_at_cutoff:
            raise ValueError(f"unexpected non-Toshima eruption-age interval: {record.island_id}")
        return record.eruption_age_min_years_at_cutoff
    if history_case == "toshima_young_endpoint":
        return record.eruption_age_min_years_at_cutoff
    return record.eruption_age_max_years_at_cutoff


def load_observations(
    trait_path: str | Path,
    history_path: str | Path,
    *,
    history_case: str,
) -> tuple[IslandObservation, ...]:
    history = load_history(history_path)
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
        if island == "Honshu" or island not in history:
            continue
        record = history[island]
        age = _history_age(record, history_case)
        out_min = _optional_float(row["outcrossing_rate_min"])
        out_max = _optional_float(row["outcrossing_rate_max"])
        if (out_min is None) != (out_max is None):
            raise ValueError(f"{island}: outcrossing interval must provide both bounds or neither")
        bagged_pct = _optional_float(row["bagged_capsule_set_pct"])
        output.append(IslandObservation(
            island_id=island,
            order=int(_clean(row["region_order"])),
            eruption_age_years=age,
            log_eruption_age=math.log1p(age),
            recent_100y_state=int(age <= 100.0),
            flower_length_mm=_optional_float(row["flower_length_mm"]),
            outcrossing_midpoint=None if out_min is None else (out_min + out_max) / 2.0,
            bagged_capsule_set_proportion=None if bagged_pct is None else bagged_pct / 100.0,
        ))
    output.sort(key=lambda item: item.order)
    if [item.island_id for item in output] != ["Oshima", "Toshima", "Niijima", "Kozushima", "Miyake", "Hachijo"]:
        raise ValueError("Campanula volcanic-history join did not recover the frozen six-island order")
    return tuple(output)


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


def _binary_prediction(x: Sequence[float], y: Sequence[float], train: Sequence[bool]) -> list[float]:
    zero = [y[index] for index, use in enumerate(train) if use and x[index] < 0.5]
    one = [y[index] for index, use in enumerate(train) if use and x[index] >= 0.5]
    if not zero or not one:
        return [float("nan") for _ in y]
    zero_mean, one_mean = _mean(zero), _mean(one)
    return [one_mean if value >= 0.5 else zero_mean for value in x]


def _null_prediction(_: Sequence[float], y: Sequence[float], train: Sequence[bool]) -> list[float]:
    centre = _mean([y[index] for index, use in enumerate(train) if use])
    return [centre for _ in y]


def _second_step_prediction(order: Sequence[float], y: Sequence[float], train: Sequence[bool]) -> list[float]:
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
    skip_if_group_lost: bool = False,
) -> float | None:
    errors: list[float] = []
    for held_out in range(len(y)):
        train = [index != held_out for index in range(len(y))]
        prediction = predictor(x, y, train)
        if math.isnan(prediction[held_out]):
            if skip_if_group_lost:
                continue
            return None
        errors.append((y[held_out] - prediction[held_out]) ** 2)
    return _mean(errors) if errors else None


def fit_trait_models(rows: Sequence[IslandObservation], *, history_case: str) -> tuple[TraitFit, ...]:
    output: list[TraitFit] = []
    for trait_id, trait_family in TRAITS:
        selected = [row for row in rows if getattr(row, trait_id) is not None]
        y = [float(getattr(row, trait_id)) for row in selected]
        order = [float(row.order) for row in selected]
        recency = [row.log_eruption_age for row in selected]
        recent100 = [float(row.recent_100y_state) for row in selected]
        if len(y) < 4:
            raise ValueError(f"{trait_id}: too few island observations")
        specs = (
            ("null", [0.0] * len(y), _null_prediction, 1, False),
            ("island_order_cline", order, _linear_prediction, 2, False),
            ("volcanic_recency_cline", recency, _linear_prediction, 2, False),
            ("recent_100y_disturbance", recent100, _binary_prediction, 2, True),
            ("oshima_to_toshima_step", order, _second_step_prediction, 2, True),
        )
        for model_id, x, predictor, k, skip_group in specs:
            prediction = predictor(x, y, [True] * len(y))
            if any(math.isnan(value) for value in prediction):
                continue
            rss = sum((y[index] - prediction[index]) ** 2 for index in range(len(y)))
            output.append(TraitFit(
                history_case=history_case,
                trait_id=trait_id,
                trait_family=trait_family,
                model_id=model_id,
                n=len(y),
                parameter_count=k,
                rss=rss,
                aicc=_aicc(y, prediction, k),
                loo_mse=_loo_mse(x, y, predictor, skip_if_group_lost=skip_group),
                loo_kind="conditional_group_loo" if skip_group else "leave_one_island_out",
            ))
    return tuple(output)


def composite_fits(fits: Iterable[TraitFit], *, history_case: str) -> tuple[CompositeFit, ...]:
    indexed = {(fit.trait_id, fit.model_id): fit for fit in fits}
    traits = [item[0] for item in TRAITS]
    specifications = {
        "null": ("null", "null", "null"),
        "single_island_order": ("island_order_cline",) * 3,
        "single_volcanic_recency": ("volcanic_recency_cline",) * 3,
        "single_recent_100y": ("recent_100y_disturbance",) * 3,
        "two_stage_order_hybrid": (
            "island_order_cline", "island_order_cline", "oshima_to_toshima_step",
        ),
        "two_stage_volcanic_recency_hybrid": (
            "volcanic_recency_cline", "volcanic_recency_cline", "oshima_to_toshima_step",
        ),
        "two_stage_recent_100y_hybrid": (
            "recent_100y_disturbance", "recent_100y_disturbance", "oshima_to_toshima_step",
        ),
    }
    output: list[CompositeFit] = []
    for model_id, channel_models in specifications.items():
        selected = [indexed.get((trait, channel)) for trait, channel in zip(traits, channel_models)]
        if any(fit is None for fit in selected):
            continue
        values = [fit.aicc for fit in selected if fit is not None and fit.aicc is not None]
        output.append(CompositeFit(
            history_case=history_case,
            model_id=model_id,
            channel_models=channel_models,
            composite_aicc=sum(values) if len(values) == len(selected) else None,
            channels_ranked=len(values),
        ))
    return tuple(sorted(
        output,
        key=lambda item: (
            item.composite_aicc is None,
            item.composite_aicc if item.composite_aicc is not None else math.inf,
        ),
    ))


def run_audit(trait_path: str | Path, history_path: str | Path) -> dict[str, object]:
    cases: dict[str, object] = {}
    for history_case in HISTORY_CASES:
        rows = load_observations(trait_path, history_path, history_case=history_case)
        fits = fit_trait_models(rows, history_case=history_case)
        composites = composite_fits(fits, history_case=history_case)
        cases[history_case] = {
            "history_axis": {
                row.island_id: {
                    "eruption_age_years": row.eruption_age_years,
                    "log_eruption_age": row.log_eruption_age,
                    "recent_100y_state": row.recent_100y_state,
                }
                for row in rows
            },
            "trait_fits": [asdict(item) for item in fits],
            "composite_fits": [asdict(item) for item in composites],
            "best_composite": composites[0].model_id if composites and composites[0].composite_aicc is not None else None,
        }
    return {
        "cutoff": "1986-01-01",
        "cases": cases,
        "claim_boundary": (
            "This audit tests only pre-1986 eruptive recency and a recent-100-year disturbance indicator. "
            "It does not reconstruct vegetation reset, founder history, gene flow, habitat history, or pollinator causation."
        ),
    }


def write_outputs(output_dir: str | Path, result: dict[str, object]) -> None:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    trait_rows = []
    composite_rows = []
    axis_rows = []
    for history_case, payload in result["cases"].items():
        trait_rows.extend(payload["trait_fits"])
        for row in payload["composite_fits"]:
            composite_rows.append({
                "history_case": history_case,
                "model_id": row["model_id"],
                "flower_length_mm_model": row["channel_models"][0],
                "outcrossing_midpoint_model": row["channel_models"][1],
                "bagged_capsule_set_proportion_model": row["channel_models"][2],
                "composite_aicc": row["composite_aicc"],
                "channels_ranked": row["channels_ranked"],
            })
        for island, values in payload["history_axis"].items():
            axis_rows.append({"history_case": history_case, "island_id": island, **values})

    with (destination / "trait_model_fits.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = ("history_case", "trait_id", "trait_family", "model_id", "n", "parameter_count", "rss", "aicc", "loo_mse", "loo_kind")
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(trait_rows)
    with (destination / "composite_model_fits.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = ("history_case", "model_id", "flower_length_mm_model", "outcrossing_midpoint_model", "bagged_capsule_set_proportion_model", "composite_aicc", "channels_ranked")
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(composite_rows)
    with (destination / "volcanic_history_axes.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = ("history_case", "island_id", "eruption_age_years", "log_eruption_age", "recent_100y_state")
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(axis_rows)
