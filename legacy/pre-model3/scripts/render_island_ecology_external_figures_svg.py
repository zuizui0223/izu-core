from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/results/simulation_manuscript_figure_data_frozen.json"
DEFAULT_OUT = ROOT / "figures/generated"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(x: float, y: float, value: object, *, size: int = 14, weight: str = "normal", anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{esc(value)}</text>'


def rect(x: float, y: float, w: float, h: float, *, fill: str = "#f7f7f7", stroke: str = "none") -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" />'


def line(x1: float, y1: float, x2: float, y2: float, *, stroke: str = "#222", width: float = 1.5) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" />'


def svg(width: int, height: int, body: list[str], title_value: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n<title>{esc(title_value)}</title>\n' + "\n".join(body) + "\n</svg>\n"


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def state_group(target: str) -> str:
    mapping = {
        "branches_downstream": "branching",
        "propagates_same_direction": "same-direction propagation",
        "buffered_or_resilient": "buffering / alternative",
        "buffered_or_alternative_mechanism": "buffering / alternative",
        "reproductive_axes_decouple": "axis decoupling",
        "counterdirectional_to_frozen_signed_position_prediction": "retained falsification",
    }
    return mapping[target]


def render_fig4(data: dict) -> str:
    systems = data["fig4_external_state_and_identifiability"]["systems"]
    grouped = {name: [] for name in ["branching", "same-direction propagation", "buffering / alternative", "axis decoupling", "retained falsification"]}
    for row in systems:
        grouped[state_group(row["target_state"])].append(row)

    short = {
        "izu_multi_taxon_hiraiwa": "Izu multi-taxon",
        "caribbean_gesneriaceae_island_mainland": "Caribbean Gesneriaceae",
        "canary_teide_honeybee_network": "Canary Teide honeybee network",
        "ogasawara_psychotria_homalosperma": "Ogasawara Psychotria",
        "new_zealand_rhabdothamnus": "New Zealand Rhabdothamnus",
        "mariana_guam_saipan_bird_loss": "Marianas bird loss",
        "seychelles_ant_disruption": "Seychelles ant disruption",
        "mauritius_roussea_ant_disruption": "Mauritius Roussea",
        "bahamas_pavonia_hurricane_pollination": "Bahamas Pavonia",
        "hawaii_lobelioids_2026": "Hawaiian lobelioids",
        "california_channel_islands_nicotiana_glauca": "Channel Islands Nicotiana",
        "puerto_rico_mona_guaiacum": "Puerto Rico-Mona Guaiacum",
        "dominica_heliconia": "Dominica Heliconia",
    }

    width, height = 1260, 790
    body = [text(40, 40, "Fig4. Cross-island recurrence of response states", size=22, weight="bold")]
    order = ["branching", "same-direction propagation", "buffering / alternative", "axis decoupling", "retained falsification"]
    counts = Counter(state_group(row["target_state"]) for row in systems)
    max_count = max(counts.values())
    left, top, plot_h = 70, 100, 145
    body += [text(45, 78, "A  Strict external challenge set", size=16, weight="bold"), line(left, top + plot_h, 1160, top + plot_h), line(left, top, left, top + plot_h)]
    for idx, name in enumerate(order):
        count = counts[name]
        x = 130 + idx * 205
        h = count / max_count * plot_h
        body.append(rect(x, top + plot_h - h, 120, h, fill=["#222", "#555", "#777", "#999", "#bbb"][idx]))
        body.append(text(x + 60, top + plot_h - h - 8, str(count), size=14, weight="bold", anchor="middle"))
        body.append(text(x + 60, top + plot_h + 22, name, size=10, anchor="middle"))

    boxes = [
        (55, 330, 550, 145, "Branching (3)", "branching"),
        (650, 330, 550, 205, "Same-direction propagation (6)", "same-direction propagation"),
        (55, 510, 550, 120, "Buffering / alternative (2)", "buffering / alternative"),
    ]
    body.append(text(45, 305, "B  Named island systems", size=16, weight="bold"))
    for x, y, w, h, title_value, group in boxes:
        body.append(rect(x, y, w, h, fill="#f7f7f7", stroke="#888"))
        body.append(text(x + 15, y + 24, title_value, size=14, weight="bold"))
        for ridx, row in enumerate(grouped[group]):
            body.append(text(x + 20, y + 50 + ridx * 23, "• " + short[row["system_id"]], size=11))

    body.append(rect(650, 570, 550, 120, fill="#f7f7f7", stroke="#888"))
    body.append(text(665, 594, "Protected exceptions", size=14, weight="bold"))
    for ridx, group in enumerate(["axis decoupling", "retained falsification"]):
        row = grouped[group][0]
        body.append(text(670, 622 + ridx * 28, "• " + short[row["system_id"]] + " — " + group, size=11))

    generative = counts["branching"] + counts["same-direction propagation"] + counts["buffering / alternative"]
    body.append(text(630, 750, f"{generative}/11 generative challenges are covered or sign-compatible; the 13-system set is a strict challenge set, not a prevalence sample.", size=12, weight="bold", anchor="middle"))
    return svg(width, height, body, "Cross-island recurrence of response states")


def render_figS1(data: dict) -> str:
    rows = data["fig4_external_state_and_identifiability"]["diagnostics"]
    width, height = 1120, 470
    body = [text(40, 40, "FigS1. State-separability diagnostics", size=21, weight="bold")]
    body += [text(50, 82, "diagnostic", size=11, weight="bold"), text(610, 82, "sensitivity", size=11, weight="bold"), text(760, 82, "false-positive", size=11, weight="bold"), text(930, 82, "specificity", size=11, weight="bold")]
    y = 115
    for row in rows:
        body.append(text(50, y, row["diagnostic"], size=10))
        body.append(text(650, y, f"{row['sensitivity']:.3f}", size=11, anchor="middle"))
        body.append(text(805, y, f"{row['false_positive_rate']:.3f}", size=11, anchor="middle"))
        body.append(text(970, y, f"{row['specificity']:.3f}", size=11, anchor="middle"))
        y += 72
    body.append(text(560, 435, "Supporting inference guard: response-state compatibility does not imply one-to-one real-world mechanism identification.", size=12, anchor="middle"))
    return svg(width, height, body, "State-separability diagnostics")


def render_all(output_dir: Path) -> list[Path]:
    data = load()
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [("Fig4_cross_island_response_architecture.svg", render_fig4(data)), ("FigS1_state_separability.svg", render_figS1(data))]
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
