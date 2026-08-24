from __future__ import annotations

import argparse
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "figures/generated/Fig1_frozen_model_logic.svg"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(x: float, y: float, value: object, *, size: int = 14, weight: str = "normal", anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{esc(value)}</text>'


def rect(x: float, y: float, w: float, h: float, *, fill: str = "#f5f5f5", stroke: str = "#222", rx: int = 8) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5" />'


def line(x1: float, y1: float, x2: float, y2: float, *, stroke: str = "#222", width: float = 1.5, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="6 5"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}"{dash} marker-end="url(#arrow)" />'


def render() -> str:
    width, height = 1220, 650
    body: list[str] = []
    body.append('<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#222" /></marker></defs>')
    body.append(text(40, 42, "Fig1. Frozen model logic: state-dependent island responses", size=23, weight="bold"))

    body.append(text(70, 90, "A  Common upstream perturbation", size=16, weight="bold"))
    body.append(rect(55, 110, 250, 110))
    body.append(text(180, 145, "pollinator-functional", size=15, weight="bold", anchor="middle"))
    body.append(text(180, 168, "environment shift", size=15, weight="bold", anchor="middle"))
    body.append(text(180, 196, "shared model perturbation", size=11, anchor="middle"))

    body.append(text(365, 90, "B  Pre-existing lineage state", size=16, weight="bold"))
    body.append(rect(345, 110, 250, 110))
    body.append(text(470, 145, "different starting positions", size=14, weight="bold", anchor="middle"))
    body.append(text(470, 170, "in functional trait space", size=14, weight="bold", anchor="middle"))
    body.append(text(470, 198, "minimal branching source", size=11, anchor="middle"))

    body.append(line(305, 165, 345, 165))

    body.append(text(655, 90, "C  Branch allocation and filters", size=16, weight="bold"))
    body.append(rect(635, 110, 250, 110))
    body.append(text(760, 140, "local support / network context", size=12, weight="bold", anchor="middle"))
    body.append(text(760, 165, "partner effectiveness", size=12, weight="bold", anchor="middle"))
    body.append(text(760, 190, "autonomous assurance", size=12, weight="bold", anchor="middle"))
    body.append(line(595, 165, 635, 165))

    body.append(text(945, 90, "D  Observable response states", size=16, weight="bold"))
    body.append(rect(925, 110, 245, 110))
    body.append(text(1047, 140, "branching", size=13, weight="bold", anchor="middle"))
    body.append(text(1047, 165, "same-direction", size=13, weight="bold", anchor="middle"))
    body.append(text(1047, 190, "buffering / attenuation", size=13, weight="bold", anchor="middle"))
    body.append(line(885, 165, 925, 165))

    body.append(text(70, 285, "Mechanism distinctions recovered by frozen interventions", size=17, weight="bold"))

    body.append(rect(55, 310, 330, 120, fill="#fafafa"))
    body.append(text(220, 340, "Branch generator", size=15, weight="bold", anchor="middle"))
    body.append(text(220, 367, "initial trait heterogeneity OFF", size=13, anchor="middle"))
    body.append(text(220, 391, "mixed-sign runs: 0.4167 → 0", size=13, weight="bold", anchor="middle"))
    body.append(text(220, 414, "replicated in an independent seed block", size=11, anchor="middle"))

    body.append(rect(445, 310, 330, 120, fill="#fafafa"))
    body.append(text(610, 340, "Network context", size=15, weight="bold", anchor="middle"))
    body.append(text(610, 367, "sign rescue: 16 / 96", size=13, weight="bold", anchor="middle"))
    body.append(text(610, 391, "worsening: 11 / 96", size=13, weight="bold", anchor="middle"))
    body.append(text(610, 414, "buffering capacity, not universal protection", size=11, anchor="middle"))

    body.append(rect(835, 310, 330, 120, fill="#fafafa"))
    body.append(text(1000, 340, "Autonomous assurance", size=15, weight="bold", anchor="middle"))
    body.append(text(1000, 367, "magnitude attenuation: 207 / 216", size=13, weight="bold", anchor="middle"))
    body.append(text(1000, 391, "sign rescue: 0 / 216; 0 / 525", size=13, weight="bold", anchor="middle"))
    body.append(text(1000, 414, "robust attenuator, not robust sign buffer", size=11, anchor="middle"))

    body.append(text(70, 495, "Inverse problem", size=17, weight="bold"))
    body.append(rect(55, 515, 1110, 85, fill="#f7f7f7"))
    body.append(text(610, 545, "Observed state ≠ uniquely identified mechanism", size=17, weight="bold", anchor="middle"))
    body.append(text(610, 572, "mixed-sign and strong sign rescue are high-specificity / low-sensitivity; same-direction and magnitude attenuation are non-identifying", size=12, anchor="middle"))
    body.append(line(1047, 220, 1047, 515, dashed=True))

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
        '<title>Frozen model logic: state-dependent island responses</title>\n'
        + "\n".join(body)
        + "\n</svg>\n"
    )


def write(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(), encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    path = write(args.output)
    print(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


if __name__ == "__main__":
    main()
