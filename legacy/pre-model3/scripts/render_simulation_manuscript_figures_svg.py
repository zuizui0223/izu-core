from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/results/simulation_manuscript_figure_data_frozen.json"
DEFAULT_OUT = ROOT / "figures/generated"


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(x: float, y: float, value: object, *, size: int = 14, weight: str = "normal", anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{esc(value)}</text>'


def rect(x: float, y: float, w: float, h: float, *, fill: str = "#666", stroke: str = "none") -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" />'


def line(x1: float, y1: float, x2: float, y2: float, *, stroke: str = "#222", width: float = 1.5) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" />'


def svg(width: int, height: int, body: list[str], title_value: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n'
        f'<title>{esc(title_value)}</title>\n'
        + "\n".join(body)
        + "\n</svg>\n"
    )


def render_fig2(data: dict) -> str:
    rows = data["fig2_minimal_branch_generator"]
    width, height = 940, 520
    left, top, plot_w, plot_h = 90, 90, 760, 300
    body = [text(40, 40, "Fig2. Minimal generator of within-run branching", size=22, weight="bold")]
    body += [line(left, top + plot_h, left + plot_w, top + plot_h), line(left, top, left, top + plot_h)]
    for tick in range(6):
        value = tick / 5
        y = top + plot_h - value * plot_h
        body.append(line(left - 5, y, left + plot_w, y, stroke="#ddd", width=1))
        body.append(text(left - 12, y + 5, f"{value:.1f}", size=12, anchor="end"))
    bar_w = 110
    gap = 65
    labels = {
        "full_residual": "Full residual",
        "initial_trait_heterogeneity_off": "Initial trait OFF",
        "trait_adjustment_heterogeneity_off": "Adjustment het. OFF",
        "assurance_ceiling_heterogeneity_off": "Assurance ceiling het. OFF"
    }
    fills = ["#222", "#aaa", "#666", "#888"]
    for idx, row in enumerate(rows):
        x = left + 55 + idx * (bar_w + gap)
        value = row["mixed_sign_run_fraction"]
        h = value * plot_h
        y = top + plot_h - h
        body.append(rect(x, y, bar_w, h, fill=fills[idx]))
        body.append(text(x + bar_w / 2, y - 8, f"{value:.3f}", size=13, weight="bold", anchor="middle"))
        body.append(text(x + bar_w / 2, top + plot_h + 28, labels[row["configuration"]], size=11, anchor="middle"))
        body.append(text(x + bar_w / 2, top + plot_h + 47, f"sign changes={row['paired_sign_changes_vs_full']}", size=10, anchor="middle"))
    body.append(text(25, top + plot_h / 2, "mixed-sign run fraction", size=14, anchor="middle"))
    body.append(text(470, 485, "Initial trait-position heterogeneity is the only tested residual factor whose removal collapses mixed-sign branching.", size=13, anchor="middle"))
    return svg(width, height, body, "Minimal generator of within-run branching")


def render_fig3(data: dict) -> str:
    fig = data["fig3_branch_allocation_buffering_attenuation"]
    width, height = 1040, 640
    body = [text(40, 40, "Fig3. Branch allocation, buffering and attenuation", size=22, weight="bold")]

    # Panel A: paired branch-sign reallocation.
    body.append(text(50, 80, "A  Paired branch-sign reallocation", size=16, weight="bold"))
    rows = fig["branch_reallocation"]
    left, top, plot_w, plot_h = 70, 110, 390, 190
    body += [line(left, top + plot_h, left + plot_w, top + plot_h), line(left, top, left, top + plot_h)]
    for idx, row in enumerate(rows):
        x = left + 55 + idx * 120
        value = row["paired_sign_change_fraction"]
        h = value / 0.4 * plot_h
        body.append(rect(x, top + plot_h - h, 70, h, fill=["#222", "#777", "#bbb"][idx]))
        body.append(text(x + 35, top + plot_h - h - 7, f"{value:.3f}", size=12, anchor="middle"))
        body.append(text(x + 35, top + plot_h + 23, row["route"], size=10, anchor="middle"))

    # Panel B: network context versus assurance.
    body.append(text(535, 80, "B  Strong buffering versus attenuation", size=16, weight="bold"))
    routes = fig["buffering_and_attenuation"]
    labels = ["sign rescue", "magnitude attenuation", "worsening"]
    left2, top2, plot_h2 = 555, 110, 190
    body += [line(left2, top2 + plot_h2, 985, top2 + plot_h2), line(left2, top2, left2, top2 + plot_h2)]
    for ridx, route in enumerate(routes):
        base_x = left2 + 50 + ridx * 205
        for midx, key in enumerate(("sign_rescue_fraction", "magnitude_attenuation_fraction", "worsening_fraction")):
            value = route[key]
            if value is None:
                continue
            h = value * plot_h2
            x = base_x + midx * 52
            body.append(rect(x, top2 + plot_h2 - h, 38, h, fill=["#222", "#666", "#aaa"][midx]))
        body.append(text(base_x + 55, top2 + plot_h2 + 23, route["route"], size=11, anchor="middle"))
    body.append(text(770, 330, "bar order: " + " / ".join(labels), size=11, anchor="middle"))

    # Panel C: assurance across saturation.
    body.append(text(50, 370, "C  Assurance state across saturation", size=16, weight="bold"))
    sat = fig["assurance_by_saturation"]
    left3, top3, plot_w3, plot_h3 = 80, 400, 830, 150
    body += [line(left3, top3 + plot_h3, left3 + plot_w3, top3 + plot_h3), line(left3, top3, left3, top3 + plot_h3)]
    points = []
    for idx, row in enumerate(sat):
        x = left3 + 120 + idx * 290
        y = top3 + plot_h3 - row["magnitude_attenuation_fraction"] * plot_h3
        points.append((x, y))
        body.append(rect(x - 5, y - 5, 10, 10, fill="#222"))
        body.append(text(x, top3 + plot_h3 + 25, f"saturation {row['saturation']:.0f}", size=12, anchor="middle"))
        body.append(text(x, y - 10, f"attenuation {row['magnitude_attenuation_fraction']:.3f}; sign rescue 0", size=11, anchor="middle"))
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        body.append(line(x1, y1, x2, y2, stroke="#222", width=2))
    body.append(text(500, 610, "Network context can reverse or worsen sign; assurance remains an attenuation-only state across tested saturation.", size=13, anchor="middle"))
    return svg(width, height, body, "Branch allocation, buffering and attenuation")


def render_fig4(data: dict) -> str:
    fig = data["fig4_external_state_and_identifiability"]
    systems = fig["systems"]
    diagnostics = fig["diagnostics"]
    width, height = 1200, 760
    body = [text(40, 40, "Fig4. External island-state challenge and diagnostic asymmetry", size=22, weight="bold")]
    body.append(text(45, 78, "A  Thirteen strict external systems", size=16, weight="bold"))
    state_short = {
        "branches_downstream": "branching",
        "propagates_same_direction": "same-direction",
        "buffered_or_resilient": "buffering",
        "buffered_or_alternative_mechanism": "buffer/alternative",
        "reproductive_axes_decouple": "axis decoupling",
        "counterdirectional_to_frozen_signed_position_prediction": "falsification"
    }
    decision_short = {
        "qualitatively_covered_by_frozen_synthetic_branching": "covered",
        "sign_class_compatible_mechanism_mapping_not_validated": "sign-compatible",
        "synthetic_buffering_class_available_empirical_mechanism_unmapped": "class available",
        "empirical_axis_decoupling_constraint": "constraint",
        "retained_falsification": "retained failure"
    }
    y = 110
    body += [text(55, y, "system", size=12, weight="bold"), text(500, y, "observed state", size=12, weight="bold"), text(770, y, "frozen reading", size=12, weight="bold")]
    y += 18
    for row in systems:
        if row["system_id"] == fig["retained_falsification_system"]:
            body.append(rect(42, y - 14, 1000, 20, fill="#eee"))
        body.append(text(55, y, row["system_id"], size=10))
        body.append(text(500, y, state_short[row["target_state"]], size=10))
        body.append(text(770, y, decision_short[row["decision"]], size=10))
        y += 23

    body.append(text(45, 455, "B  Observation-to-mechanism diagnostics", size=16, weight="bold"))
    body += [text(55, 482, "diagnostic", size=11, weight="bold"), text(610, 482, "sensitivity", size=11, weight="bold"), text(750, 482, "false-positive", size=11, weight="bold"), text(910, 482, "specificity", size=11, weight="bold")]
    y = 510
    for row in diagnostics:
        body.append(text(55, y, row["diagnostic"], size=10))
        body.append(text(650, y, f"{row['sensitivity']:.3f}", size=11, anchor="middle"))
        body.append(text(800, y, f"{row['false_positive_rate']:.3f}", size=11, anchor="middle"))
        body.append(text(950, y, f"{row['specificity']:.3f}", size=11, anchor="middle"))
        body.append(rect(610, y + 7, 120 * row["sensitivity"], 7, fill="#444"))
        body.append(rect(760, y + 7, 120 * row["false_positive_rate"], 7, fill="#999"))
        body.append(rect(910, y + 7, 120 * row["specificity"], 7, fill="#222"))
        y += 48
    body.append(text(600, 730, "State-space compatibility is broad, but inverse mechanism identification is asymmetric; Dominica remains a protected failure.", size=13, anchor="middle"))
    return svg(width, height, body, "External island-state challenge and diagnostic asymmetry")


def render_all(output_dir: Path) -> list[Path]:
    data = load()
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        ("Fig2_minimal_branch_generator.svg", render_fig2(data)),
        ("Fig3_branch_allocation_buffering_attenuation.svg", render_fig3(data)),
        ("Fig4_external_state_identifiability.svg", render_fig4(data))
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
