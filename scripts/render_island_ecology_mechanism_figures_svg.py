from __future__ import annotations

import argparse
from pathlib import Path

from scripts.render_simulation_manuscript_figures_svg import load, render_fig2, render_fig3

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "figures/generated"


def render_all(output_dir: Path) -> list[Path]:
    data = load()
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        ("Fig2_minimal_branch_generator.svg", render_fig2(data)),
        ("Fig3_branch_allocation_buffering_attenuation.svg", render_fig3(data)),
    ]
    paths = []
    for filename, content in outputs:
        path = output_dir / filename
        path.write_text(content, encoding="utf-8")
        paths.append(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    for path in render_all(args.output_dir):
        print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


if __name__ == "__main__":
    main()
