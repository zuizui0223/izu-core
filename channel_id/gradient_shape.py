"""Classify the shape of a trait response along an ordered island gradient.

Given a trait measured across ordered islands, decide whether the response is:

  * ``none``  — flat (best explained by a single mean),
  * ``cline`` — a smooth monotonic trend (linear in gradient position), or
  * ``step``  — a threshold / breakpoint (two levels split at one boundary).

This is the multi-species generalisation of the anti-cline threshold observation
in *Campanula microdonta* (autonomous selfing jumps at the bumblebee-loss
boundary rather than clining smoothly). Model choice uses AICc, which is
appropriate for the very small per-species samples (typically 5-7 islands).

The module makes no ecological claim by itself: it reports which of three
descriptive shapes best fits one trait vector, plus the breakpoint location for
a step. Whether a shared breakpoint across species implies a common driver is a
separate, downstream inference.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class GradientShape:
    shape: str                 # "none" | "cline" | "step"
    n: int
    breakpoint_index: int | None   # step: split is between points [i] and [i+1] (0-based, on sorted positions)
    breakpoint_position: float | None
    effect: float              # step: (mean_after - mean_before); cline: slope; none: 0.0
    direction: str             # "increase" | "reduction" | "flat"
    aicc: dict                 # aicc per model
    sse: dict


def _aicc(sse: float, n: int, k: int) -> float:
    # k = number of estimated parameters INCLUDING the error variance
    if sse <= 0:
        sse = 1e-12
    aic = n * math.log(sse / n) + 2 * k
    denom = n - k - 1
    if denom <= 0:
        return math.inf
    return aic + (2 * k * (k + 1)) / denom


def _linfit_sse(xs: list[float], ys: list[float]) -> tuple[float, float]:
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return 0.0, sum((y - my) ** 2 for y in ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    intercept = my - slope * mx
    sse = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys))
    return slope, sse


def classify_gradient_shape(
    positions: list[float],
    values: list[float | None],
    min_points: int = 4,
) -> GradientShape:
    """Return the best-fitting shape (none/cline/step) for one trait vector.

    ``positions`` are ordered gradient positions (island rank or archipelago
    position); ``values`` may contain ``None`` for missing islands.
    """
    pairs = sorted(
        [(p, v) for p, v in zip(positions, values) if v is not None],
        key=lambda t: t[0],
    )
    n = len(pairs)
    if n < min_points:
        raise ValueError(f"need >= {min_points} non-missing points, got {n}")
    xs = [p for p, _ in pairs]
    ys = [v for _, v in pairs]

    my = sum(ys) / n
    sse_null = sum((y - my) ** 2 for y in ys)
    slope, sse_cline = _linfit_sse(xs, ys)

    # best single-breakpoint two-level step
    best = None
    for i in range(n - 1):
        left, right = ys[: i + 1], ys[i + 1:]
        ml, mr = sum(left) / len(left), sum(right) / len(right)
        sse = sum((y - ml) ** 2 for y in left) + sum((y - mr) ** 2 for y in right)
        if best is None or sse < best[0]:
            best = (sse, i, mr - ml)
    sse_step, bp_idx, step_effect = best

    # k counts mean-structure parameters only (variance not counted separately),
    # keeping AICc usable at the small per-species n (5-8 islands).
    aicc = {
        "none": _aicc(sse_null, n, 1),    # one level
        "cline": _aicc(sse_cline, n, 2),  # slope + intercept
        "step": _aicc(sse_step, n, 3),    # two levels + breakpoint location
    }
    sse = {"none": sse_null, "cline": sse_cline, "step": sse_step}
    shape = min(aicc, key=aicc.get)

    if shape == "step":
        effect = step_effect
        bp_pos = (xs[bp_idx] + xs[bp_idx + 1]) / 2
        direction = "increase" if effect > 0 else "reduction"
        return GradientShape(shape, n, bp_idx, bp_pos, effect, direction, aicc, sse)
    if shape == "cline":
        direction = "increase" if slope > 0 else "reduction"
        return GradientShape(shape, n, None, None, slope, direction, aicc, sse)
    return GradientShape("none", n, None, None, 0.0, "flat", aicc, sse)
