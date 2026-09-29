"""Apply the step/cline/none shape classifier to island trait vectors.

Run on the *Campanula microdonta* calibration seed now; the same call applies to
any multi-species trait table (one row per species x island) once populated.

  python paper/threshold_analysis.py
"""

from __future__ import annotations

import csv
import pathlib

from channel_id.gradient_shape import classify_gradient_shape

HERE = pathlib.Path(__file__).parent
DATA = HERE.parent / "data" / "inoue_literature_island_traits.csv"

# island region_order gives the ordered gradient position
TRAITS = [
    "outcrossing_rate_min", "outcrossing_rate_max",
    "bagged_capsule_set_pct", "flower_length_mm",
    "mean_temp_c", "annual_precip_mm",
]


def _num(s: str):
    s = (s or "").strip()
    if s in ("", "NA"):
        return None
    return float(s)


def main() -> None:
    rows = list(csv.DictReader(DATA.open(encoding="utf-8")))
    order = [float(r["region_order"]) for r in rows]

    print(f"{'trait':24s} {'shape':6s} {'dir':10s} {'bp@order':>9s}  {'effect':>9s}")
    for trait in TRAITS:
        vals = [_num(r[trait]) for r in rows]
        try:
            g = classify_gradient_shape(order, vals)
        except ValueError as e:
            print(f"{trait:24s} (skipped: {e})")
            continue
        bp = "" if g.breakpoint_position is None else f"{g.breakpoint_position:.1f}"
        print(f"{trait:24s} {g.shape:6s} {g.direction:10s} {bp:>9s}  {g.effect:>9.3f}")

    print("\nInterpretation: reproductive traits that STEP at bp~1.5 fall at the")
    print("Oshima(1)->Toshima(2) bumblebee-loss boundary; smooth CLINE traits do not")
    print("localise to it. Climate traits are the contrast (expect none/weak).")


if __name__ == "__main__":
    main()
