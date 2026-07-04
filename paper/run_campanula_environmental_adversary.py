"""Run the source-locked Campanula environmental-adversary shape audit."""
from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.campanula_environmental_adversary import (
    composite_fits,
    fit_channel_models,
    load_island_rows,
    render_markdown,
    write_outputs,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        rows = load_island_rows(args.input)
        fits, loadings = fit_channel_models(rows)
        composites = composite_fits(fits)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    write_outputs(args.output_dir, fits, composites, loadings)
    (args.output_dir / "CAMPANULA_ENVIRONMENTAL_ADVERSARY.md").write_text(
        render_markdown(fits, composites, loadings), encoding="utf-8"
    )
    best = composites[0]
    print(
        "best composite:", best.model_id,
        "aicc=", "NA" if best.composite_aicc is None else f"{best.composite_aicc:.6f}",
    )


if __name__ == "__main__":
    main()
