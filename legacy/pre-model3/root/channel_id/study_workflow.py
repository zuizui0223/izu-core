"""Reusable small-regime cline-versus-threshold workflow.

The workflow accepts summary statistics supplied by a researcher, validates the
study design, classifies each channel, and calibrates the decision with a
simulation matched to the reported sampling precision.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from channel_id.threshold_identifiability import Regime, classify_profile, run_recovery_audit

REQUIRED_COLUMNS = {"channel", "regime_id", "order", "second_step_state", "mean", "n"}


@dataclass(frozen=True)
class SummaryRow:
    channel: str
    regime_id: str
    order: int
    second_step_state: int
    mean: float
    n: int
    sd: float | None
    se: float | None

    @property
    def resolved_sd(self) -> float | None:
        if self.sd is not None:
            return self.sd
        if self.se is not None:
            return self.se * math.sqrt(self.n)
        return None


def _number(value: str | None) -> float | None:
    if value is None or not value.strip():
        return None
    return float(value)


def load_summary(path: str | Path) -> tuple[SummaryRow, ...]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")
        rows = tuple(
            SummaryRow(
                channel=str(row["channel"]).strip(),
                regime_id=str(row["regime_id"]).strip(),
                order=int(row["order"]),
                second_step_state=int(row["second_step_state"]),
                mean=float(row["mean"]),
                n=int(row["n"]),
                sd=_number(row.get("sd")),
                se=_number(row.get("se")),
            )
            for row in reader
        )
    return rows


def validate_summary(rows: Iterable[SummaryRow]) -> list[str]:
    rows = list(rows)
    errors: list[str] = []
    if not rows:
        return ["input contains no rows"]
    for row in rows:
        if not row.channel or not row.regime_id:
            errors.append("channel and regime_id must be non-empty")
        if row.n <= 0:
            errors.append(f"{row.channel}/{row.regime_id}: n must be positive")
        if row.second_step_state not in (0, 1):
            errors.append(f"{row.channel}/{row.regime_id}: second_step_state must be 0 or 1")
        if row.sd is not None and row.sd < 0:
            errors.append(f"{row.channel}/{row.regime_id}: sd must be non-negative")
        if row.se is not None and row.se < 0:
            errors.append(f"{row.channel}/{row.regime_id}: se must be non-negative")
    for channel in sorted({row.channel for row in rows}):
        subset = [row for row in rows if row.channel == channel]
        if len(subset) < 3:
            errors.append(f"{channel}: at least three ordered regimes are required")
        if len({row.regime_id for row in subset}) != len(subset):
            errors.append(f"{channel}: duplicate regime_id")
        if len({row.order for row in subset}) != len(subset):
            errors.append(f"{channel}: duplicate order")
        if {row.second_step_state for row in subset} != {0, 1}:
            errors.append(f"{channel}: threshold groups must contain both 0 and 1")
    return sorted(set(errors))


def _pooled_sd(rows: list[SummaryRow]) -> float:
    available = [(row.resolved_sd, row.n) for row in rows if row.resolved_sd is not None]
    if not available:
        return 1.0
    numerator = sum((n - 1) * sd * sd for sd, n in available if sd is not None and n > 1)
    denominator = sum(n - 1 for _, n in available if n > 1)
    return math.sqrt(numerator / denominator) if denominator > 0 else max(sd for sd, _ in available if sd is not None)


def analyze_summary(rows: Iterable[SummaryRow], *, replicates: int = 5000, seed: int = 20260717) -> dict[str, object]:
    rows = list(rows)
    errors = validate_summary(rows)
    if errors:
        return {"status": "invalid", "errors": errors}
    channels: dict[str, object] = {}
    for channel in sorted({row.channel for row in rows}):
        subset = sorted((row for row in rows if row.channel == channel), key=lambda row: row.order)
        regimes = tuple(Regime(row.regime_id, row.order, row.second_step_state) for row in subset)
        observed = tuple(row.mean for row in subset)
        selected, scores = classify_profile(regimes, observed)
        effect_size = max(observed) - min(observed)
        pooled_sd = _pooled_sd(subset)
        samples = max(1, round(sum(row.n for row in subset) / len(subset)))
        audit = run_recovery_audit(
            regimes,
            replicates=replicates,
            effect_size=max(effect_size, pooled_sd * 0.1, 1e-9),
            noise_sd=max(pooled_sd, 1e-9),
            samples_per_regime=samples,
            seed=seed,
        )
        channels[channel] = {
            "selected_shape": selected,
            "scores": scores,
            "observed_means": {row.regime_id: row.mean for row in subset},
            "design": {"average_n": samples, "pooled_sd": pooled_sd, "observed_range": effect_size},
            "simulation_audit": audit,
            "interpretation": (
                f"Observed summaries favour {selected}; this is compatibility, not causal proof. "
                f"Under the matched simulation, the cline false-threshold rate is "
                f"{audit['cline_false_second_step_rate']:.3f} and threshold recovery is "
                f"{audit['second_step_recovery_rate']:.3f}."
            ),
        }
    return {
        "status": "ok",
        "channels": channels,
        "claim_boundary": "Results compare a predeclared cline with a predeclared second-step shape. They do not establish historical causation or discover an unconstrained breakpoint.",
    }


def run_workflow(input_path: str | Path, output_path: str | Path, *, replicates: int = 5000, seed: int = 20260717) -> dict[str, object]:
    result = analyze_summary(load_summary(input_path), replicates=replicates, seed=seed)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result
