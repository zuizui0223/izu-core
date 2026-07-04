"""Joint, interval-aware profile comparison for the Izu Campanula channels.

This module is intentionally a *descriptive partial-identification analysis*.
It does not estimate a historical pollinator effect. It compares whether a
single low-parameter profile can fit three source-locked response channels over
all admissible endpoint choices for the published outcrossing intervals:

* flower length;
* multilocus outcrossing; and
* bagged capsule set (autonomous reproductive capacity, not realised selfing).

The analysis is restricted to the six Izu islands with all three recorded
climate covariates. Honshu is excluded from the climate-comparable profile
rather than assigning it a guessed climate proxy.

Profiles are intentionally simple:

* ``environment_pc1``: one observed climate PC1 drives all channels;
* ``single_island_order``: one continuous ordinal island axis drives all;
* ``two_stage_hybrid``: flower length and outcrossing follow island order,
  while autonomous capacity has an Oshima-to-Toshima step;
* ``no_second_threshold``: flower length follows island order but the two
  reproductive channels are flat, representing the shared testable component
  of body-size-only and complete-small-bee-substitution scenarios.

The output is a profile diagnostic. Summed AICc values are neither Bayes
factors nor evidence of causal identification.
"""
from __future__ import annotations

import csv
import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

ENV_COLUMNS = ("mean_temp_c", "annual_precip_mm", "precip_cv")
TRAITS = ("flower_length_mm", "outcrossing", "autonomous_capacity")
PROFILE_CHANNELS = {
    "environment_pc1": {
        "flower_length_mm": "climate_pc1_cline",
        "outcrossing": "climate_pc1_cline",
        "autonomous_capacity": "climate_pc1_cline",
    },
    "single_island_order": {
        "flower_length_mm": "island_order_cline",
        "outcrossing": "island_order_cline",
        "autonomous_capacity": "island_order_cline",
    },
    "two_stage_hybrid": {
        "flower_length_mm": "island_order_cline",
        "outcrossing": "island_order_cline",
        "autonomous_capacity": "oshima_to_toshima_step",
    },
    "no_second_threshold": {
        "flower_length_mm": "island_order_cline",
        "outcrossing": "null",
        "autonomous_capacity": "null",
    },
}


@dataclass(frozen=True)
class IslandRecord:
    island_id: str
    region_order: int
    flower_length_mm: float | None
    outcross_min: float
    outcross_max: float
    autonomous_capacity: float
    climate: tuple[float, float, float]


@dataclass(frozen=True)
class Fit:
    trait: str
    model: str
    n: int
    aicc: float
    rss: float


def _clean(value: object) -> str:
    return str(value or "").strip()


def _float(value: object, label: str) -> float:
    text = _clean(value)
    if not text:
        raise ValueError(f"missing numeric value: {label}")
    return float(text)


def _optional_float(value: object) -> float | None:
    text = _clean(value)
    return None if not text else float(text)


def load_izu_records(path: str | Path) -> tuple[IslandRecord, ...]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "island_id", "region_order", "flower_length_mm", "outcrossing_rate_min",
        "outcrossing_rate_max", "bagged_capsule_set_pct", *ENV_COLUMNS,
    }
    if not rows:
        raise ValueError("input table is empty")
    missing = sorted(required.difference(rows[0]))
    if missing:
        raise ValueError("input table missing columns: " + ", ".join(missing))
    records: list[IslandRecord] = []
    for row in rows:
        climate_values = tuple(_optional_float(row[name]) for name in ENV_COLUMNS)
        # The mainland row has no matching climate source in the locked table;
        # excluding it is safer than a fabricated mainland climate proxy.
        if any(value is None for value in climate_values):
            continue
        minimum = _float(row["outcrossing_rate_min"], f"{row['island_id']} outcrossing minimum")
        maximum = _float(row["outcrossing_rate_max"], f"{row['island_id']} outcrossing maximum")
        if minimum > maximum:
            raise ValueError(f"{row['island_id']}: outcrossing minimum exceeds maximum")
        records.append(IslandRecord(
            island_id=_clean(row["island_id"]),
            region_order=int(_float(row["region_order"], f"{row['island_id']} region order")),
            flower_length_mm=_optional_float(row["flower_length_mm"]),
            outcross_min=minimum,
            outcross_max=maximum,
            autonomous_capacity=_float(row["bagged_capsule_set_pct"], f"{row['island_id']} bagged capsule set") / 100.0,
            climate=(float(climate_values[0]), float(climate_values[1]), float(climate_values[2])),
        ))
    if len(records) < 4:
        raise ValueError("need at least four climate-complete Izu island rows")
    return tuple(sorted(records, key=lambda row: row.region_order))


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def _sd(values: Sequence[float]) -> float:
    if len(values) < 2:
        raise ValueError("at least two values are required")
    mean = _mean(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / (len(values) - 1))


def climate_pc1(records: Sequence[IslandRecord]) -> tuple[dict[str, float], dict[str, float]]:
    raw = [list(record.climate) for record in records]
    means = [_mean([row[i] for row in raw]) for i in range(3)]
    sds = [_sd([row[i] for row in raw]) for i in range(3)]
    z = [[(row[i] - means[i]) / sds[i] for i in range(3)] for row in raw]
    covariance = [[sum(row[i] * row[j] for row in z) / (len(z) - 1) for j in range(3)] for i in range(3)]
    vector = [1.0, 1.0, 1.0]
    for _ in range(250):
        candidate = [sum(covariance[i][j] * vector[j] for j in range(3)) for i in range(3)]
        norm = math.sqrt(sum(value * value for value in candidate))
        if norm == 0:
            raise ValueError("climate covariance matrix has no leading axis")
        vector = [value / norm for value in candidate]
    if vector[0] > 0:
        vector = [-value for value in vector]
    scores = {record.island_id: sum(z[index][j] * vector[j] for j in range(3)) for index, record in enumerate(records)}
    return scores, {ENV_COLUMNS[i]: vector[i] for i in range(3)}


def _linear(x: Sequence[float], y: Sequence[float]) -> tuple[list[float], int]:
    xbar, ybar = _mean(x), _mean(y)
    denominator = sum((value - xbar) ** 2 for value in x)
    slope = 0.0 if denominator == 0 else sum((x[i] - xbar) * (y[i] - ybar) for i in range(len(x))) / denominator
    intercept = ybar - slope * xbar
    return [intercept + slope * value for value in x], 2


def _null(_: Sequence[float], y: Sequence[float]) -> tuple[list[float], int]:
    return [_mean(y) for _ in y], 1


def _step(order: Sequence[float], y: Sequence[float]) -> tuple[list[float], int]:
    baseline = [y[i] for i, value in enumerate(order) if value < 2]
    focal = [y[i] for i, value in enumerate(order) if value >= 2]
    if not baseline or not focal:
        raise ValueError("step requires Oshima baseline and one or more focal islands")
    before, after = _mean(baseline), _mean(focal)
    return [before if value < 2 else after for value in order], 2


def _aicc(y: Sequence[float], prediction: Sequence[float], parameters: int) -> tuple[float, float]:
    n = len(y)
    if n <= parameters + 1:
        raise ValueError("too few observations for requested AICc model")
    rss = max(sum((y[i] - prediction[i]) ** 2 for i in range(n)), 1e-15)
    loglik = -n / 2.0 * (math.log(2.0 * math.pi) + 1.0 + math.log(rss / n))
    aic = 2.0 * parameters - 2.0 * loglik
    return aic + 2.0 * parameters * (parameters + 1.0) / (n - parameters - 1.0), rss


def _fit(trait: str, model: str, records: Sequence[IslandRecord], outcross_values: dict[str, float], pc1: dict[str, float]) -> Fit:
    if trait == "flower_length_mm":
        selected = [record for record in records if record.flower_length_mm is not None]
        y = [float(record.flower_length_mm) for record in selected]
    elif trait == "outcrossing":
        selected = list(records)
        y = [outcross_values[record.island_id] for record in selected]
    elif trait == "autonomous_capacity":
        selected = list(records)
        y = [record.autonomous_capacity for record in selected]
    else:
        raise ValueError(f"unknown trait: {trait}")
    order = [float(record.region_order) for record in selected]
    climate = [pc1[record.island_id] for record in selected]
    if model == "climate_pc1_cline":
        prediction, k = _linear(climate, y)
    elif model == "island_order_cline":
        prediction, k = _linear(order, y)
    elif model == "oshima_to_toshima_step":
        prediction, k = _step(order, y)
    elif model == "null":
        prediction, k = _null(order, y)
    else:
        raise ValueError(f"unknown channel model: {model}")
    aicc, rss = _aicc(y, prediction, k)
    return Fit(trait=trait, model=model, n=len(y), aicc=aicc, rss=rss)


def all_endpoint_cases(records: Sequence[IslandRecord]) -> Iterable[dict[str, float]]:
    for endpoints in itertools.product((0, 1), repeat=len(records)):
        yield {record.island_id: record.outcross_max if endpoint else record.outcross_min for record, endpoint in zip(records, endpoints)}


def profile_cases(records: Sequence[IslandRecord]) -> tuple[list[dict[str, object]], dict[str, float], list[Fit]]:
    pc1, loadings = climate_pc1(records)
    cases: list[dict[str, object]] = []
    reference_fits: list[Fit] = []
    for case_index, outcross_values in enumerate(all_endpoint_cases(records)):
        profile_scores: dict[str, float] = {}
        case_fits: list[Fit] = []
        for profile, channels in PROFILE_CHANNELS.items():
            fits = [_fit(trait, channels[trait], records, outcross_values, pc1) for trait in TRAITS]
            profile_scores[profile] = sum(fit.aicc for fit in fits)
            if case_index == 0:
                case_fits.extend(fits)
        ordered = sorted(profile_scores.items(), key=lambda item: item[1])
        winner, winner_score = ordered[0]
        runner_up, runner_score = ordered[1]
        cases.append({
            "case_id": case_index, "winner": winner, "winner_aicc": winner_score,
            "runner_up": runner_up, "runner_up_aicc": runner_score,
            "delta_aicc": runner_score - winner_score,
            **{f"aicc_{profile}": value for profile, value in profile_scores.items()},
            **{f"outcross_{record.island_id}": outcross_values[record.island_id] for record in records},
        })
        if case_index == 0:
            reference_fits = case_fits
    return cases, loadings, reference_fits


def summarize(cases: Sequence[dict[str, object]], loadings: dict[str, float], records: Sequence[IslandRecord]) -> dict[str, object]:
    profiles = tuple(PROFILE_CHANNELS)
    wins = {profile: sum(case["winner"] == profile for case in cases) for profile in profiles}
    ranges = {
        profile: {
            "min_aicc": min(float(case[f"aicc_{profile}"]) for case in cases),
            "max_aicc": max(float(case[f"aicc_{profile}"]) for case in cases),
        }
        for profile in profiles
    }
    hybrid_deltas = [
        float(case[f"aicc_{profile}"]) - float(case["aicc_two_stage_hybrid"])
        for case in cases for profile in profiles if profile != "two_stage_hybrid"
    ]
    return {
        "scope": "Izu islands with all three measured climate covariates; mainland reference excluded rather than imputed.",
        "n_islands": len(records),
        "n_outcross_interval_cases": len(cases),
        "profile_wins": wins,
        "profile_aicc_ranges": ranges,
        "two_stage_hybrid_min_delta_against_any_alternative": min(hybrid_deltas),
        "two_stage_hybrid_max_delta_against_any_alternative": max(hybrid_deltas),
        "climate_pc1_loadings": loadings,
        "boundary": "This is an interval-aware channel-profile diagnostic. It does not estimate a latent pollinator service, identify a historical pollinator replacement, or reject environmental and colonisation-history alternatives outside the three measured climate covariates.",
    }


def write_outputs(output_dir: str | Path, records: Sequence[IslandRecord], cases: Sequence[dict[str, object]], summary: dict[str, object], reference_fits: Sequence[Fit]) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    with (output / "interval_profile_cases.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(cases[0]) if cases else [])
        writer.writeheader(); writer.writerows(cases)
    with (output / "reference_endpoint_trait_fits.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("trait", "model", "n", "aicc", "rss"))
        writer.writeheader()
        for fit in reference_fits:
            writer.writerow({"trait": fit.trait, "model": fit.model, "n": fit.n, "aicc": f"{fit.aicc:.12g}", "rss": f"{fit.rss:.12g}"})
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_markdown(summary: dict[str, object], cases: Sequence[dict[str, object]]) -> str:
    lines = [
        "# Joint interval-aware Campanula channel profile", "",
        "All admissible endpoints of the reported outcrossing intervals are enumerated. The analysis uses only Izu islands with complete observed climate covariates; it does not assign a climate proxy to Honshu.",
        "", "## Profile wins across outcrossing interval cases", "",
        "| profile | winning endpoint cases | total cases | AICc range |", "|---|---:|---:|---:|",
    ]
    for profile, count in summary["profile_wins"].items():
        window = summary["profile_aicc_ranges"][profile]
        lines.append(f"| {profile} | {count} | {summary['n_outcross_interval_cases']} | {window['min_aicc']:.3f}–{window['max_aicc']:.3f} |")
    lines.extend((
        "", "## Interpretation", "",
        "`two_stage_hybrid` means flower length and outcrossing are fitted by a continuous island-order trend while bagged capsule set is fitted by the Oshima-to-Toshima step. A stable win says this profile describes the three observed channels more compactly than the listed competitors under every admissible outcrossing endpoint choice. It is not a causal estimate.",
        "", "## Boundary", "", str(summary["boundary"]), "",
    ))
    return "\n".join(lines)
