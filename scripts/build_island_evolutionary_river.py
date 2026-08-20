from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
V4_RESULT = ROOT / "data/results/abm_v4_global_continuous_isolation_gradient.json"
V6_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v6_local_support.py"
V5_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
OUT_SVG = ROOT / "data/results/island_evolutionary_river_v1.svg"
OUT_JSON = ROOT / "data/results/island_evolutionary_river_v1.json"

WIDTH = 1400
HEIGHT = 860
X0 = 120.0
X1 = 1280.0
RIVER_CENTER = 300.0
MAX_HALF_WIDTH = 220.0
STATE_TOP = 610.0
STATE_BOTTOM = 790.0


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sx(value: float) -> float:
    return X0 + value * (X1 - X0)


def path_from_points(points: list[tuple[float, float]]) -> str:
    if not points:
        return ""
    head = f"M {points[0][0]:.2f} {points[0][1]:.2f}"
    rest = " ".join(f"L {x:.2f} {y:.2f}" for x, y in points[1:])
    return f"{head} {rest}" if rest else head


def polygon_path(upper: list[tuple[float, float]], lower: list[tuple[float, float]]) -> str:
    points = upper + list(reversed(lower))
    return path_from_points(points) + " Z"


def normalized(values: list[float], *, invert: bool = False) -> list[float]:
    lo = min(values)
    hi = max(values)
    if math.isclose(lo, hi):
        scaled = [0.5 for _ in values]
    else:
        scaled = [(value - lo) / (hi - lo) for value in values]
    return [1.0 - value for value in scaled] if invert else scaled


def metric_y(value01: float, band_index: int) -> float:
    band_height = 46.0
    gap = 10.0
    base = STATE_TOP + band_index * (band_height + gap)
    return base + (1.0 - value01) * band_height


def local_channel_paths(
    gradient: list[dict],
    river_half_widths: list[float],
    support_strengths: list[float],
) -> list[dict]:
    # Channels are schematic v6 alternatives inside the frozen v4 envelope.
    # Their amplitudes depend only on the generic support-strength envelope.
    channels = []
    nonzero = [value for value in support_strengths if value > 0]
    for index, support_strength in enumerate(nonzero):
        phase = (index + 1) * 1.7
        sign = -1.0 if index % 2 == 0 else 1.0
        points = []
        widths = []
        for row, half_width in zip(gradient, river_half_widths):
            isolation = float(row["isolation_index"])
            # Branching is visually weak near the mainland and stronger once
            # island-scale constraint is established; this is presentation logic,
            # not an empirical probability model.
            gate = max(0.0, min(1.0, (isolation - 0.12) / 0.45))
            offset = (
                sign
                * gate
                * half_width
                * (0.16 + 0.12 * support_strength)
                * math.sin(phase + isolation * 4.2)
            )
            points.append((sx(isolation), RIVER_CENTER + offset))
            widths.append(max(4.0, half_width * (1.0 - support_strength) * 0.16))
        channels.append(
            {
                "support_strength": support_strength,
                "points": points,
                "stroke_widths": widths,
            }
        )
    return channels


def build() -> tuple[str, dict]:
    v4 = json.loads(V4_RESULT.read_text())
    gradient = list(v4["gradient"])
    v6 = load_module(V6_SCRIPT, "island_river_v6")
    v5 = load_module(V5_SCRIPT, "island_river_v5")
    support_strengths = [float(value) for value in v6.SUPPORT_STRENGTHS]
    weight_strengths = [float(value) for value in v5.CONTEXT_STRENGTHS]

    partner_values = [float(row["final_partner_types"]) for row in gradient]
    max_partner = max(partner_values)
    half_widths = [MAX_HALF_WIDTH * value / max_partner for value in partner_values]
    upper = [
        (sx(float(row["isolation_index"])), RIVER_CENTER - half_width)
        for row, half_width in zip(gradient, half_widths)
    ]
    lower = [
        (sx(float(row["isolation_index"])), RIVER_CENTER + half_width)
        for row, half_width in zip(gradient, half_widths)
    ]
    river_path = polygon_path(upper, lower)

    channels = local_channel_paths(gradient, half_widths, support_strengths)

    diversity = normalized([float(row["interaction_diversity_proxy"]) for row in gradient])
    overlap = normalized([float(row["plant_niche_overlap_proxy"]) for row in gradient])
    reproduction = normalized([float(row["mean_reproduction"]) for row in gradient])
    state_series = [
        ("Interaction diversity", diversity),
        ("Plant niche overlap", overlap),
        ("Mean reproduction", reproduction),
    ]

    lines = []
    lines.append(
        '<svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">'
    )
    lines.append("<title>Island Evolutionary River</title>")
    lines.append(
        "<desc>Increasing island constraint narrows the v4 feasible partner-opportunity river. "
        "Inside that envelope, v6 local partner support branches into alternative local channels, "
        "while v5 reorganizes weights within each channel. Lower trajectories show frozen v4 "
        "interaction diversity, plant niche overlap, and reproduction patterns along the same "
        "isolation index. This is a constrained state-space visualization, not chronological history.</desc>"
    )
    lines.append("<defs>")
    lines.append(
        '<linearGradient id="riverFill" x1="0%" y1="0%" x2="100%" y2="0%">'
        '<stop offset="0%" stop-color="#1d5f6f" stop-opacity="0.72"/>'
        '<stop offset="100%" stop-color="#1d5f6f" stop-opacity="0.28"/>'
        "</linearGradient>"
    )
    lines.append(
        '<pattern id="weightTexture" width="16" height="16" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(18)">'
        '<line x1="0" y1="0" x2="0" y2="16" stroke="#ffffff" stroke-opacity="0.24" stroke-width="2"/>'
        "</pattern>"
    )
    lines.append("</defs>")
    lines.append('<rect width="100%" height="100%" fill="#fbfbf8"/>')

    # Header / axis language.
    lines.append('<text x="120" y="48" font-family="sans-serif" font-size="28" font-weight="600" fill="#17202a">Island Evolutionary River</text>')
    lines.append('<text x="120" y="76" font-family="sans-serif" font-size="15" fill="#4d5a63">A constrained ecological state space — not an ABM agent animation and not chronological time</text>')
    lines.append('<text x="120" y="112" font-family="sans-serif" font-size="14" fill="#4d5a63">weak island constraint</text>')
    lines.append('<text x="1280" y="112" text-anchor="end" font-family="sans-serif" font-size="14" fill="#4d5a63">strong island constraint</text>')
    lines.append(f'<line x1="{X0}" y1="124" x2="{X1}" y2="124" stroke="#7a858c" stroke-width="1.5"/>')
    lines.append(f'<path d="M {X1-8} 119 L {X1} 124 L {X1-8} 129" fill="none" stroke="#7a858c" stroke-width="1.5"/>')

    # Unavailable state-space field and river.
    lines.append('<rect x="100" y="148" width="1200" height="320" rx="22" fill="#e9eceb"/>')
    lines.append('<text x="118" y="174" font-family="sans-serif" font-size="13" fill="#6d7478">unavailable / excluded by current island-scale constraint</text>')
    lines.append(f'<path d="{river_path}" fill="url(#riverFill)" stroke="#174d59" stroke-width="2.2"/>')
    lines.append(f'<path d="{river_path}" fill="url(#weightTexture)" stroke="none"/>')

    # A central backbone keeps the idea of a shared island-scale opportunity axis.
    backbone = path_from_points([(sx(float(row["isolation_index"])), RIVER_CENTER) for row in gradient])
    lines.append(f'<path d="{backbone}" fill="none" stroke="#123842" stroke-width="2" stroke-dasharray="8 7" opacity="0.75"/>')

    # Local support branches.
    channel_colors = ["#6e5978", "#9c6a3d", "#496c55"]
    for channel_index, channel in enumerate(channels):
        color = channel_colors[channel_index % len(channel_colors)]
        points = channel["points"]
        mean_width = sum(channel["stroke_widths"]) / len(channel["stroke_widths"])
        path = path_from_points(points)
        lines.append(
            f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{mean_width:.2f}" '
            'stroke-linecap="round" stroke-linejoin="round" opacity="0.38"/>'
        )
        # v5 within-support realization is shown as a thin internal trace.
        trace_points = [
            (x, y + math.sin(i * 1.3 + channel_index) * 5.0)
            for i, (x, y) in enumerate(points)
        ]
        lines.append(
            f'<path d="{path_from_points(trace_points)}" fill="none" stroke="#ffffff" '
            'stroke-width="2.2" stroke-dasharray="5 6" opacity="0.78"/>'
        )

    # Hierarchy labels.
    lines.append('<g font-family="sans-serif" font-size="14" fill="#17202a">')
    lines.append('<text x="145" y="510" font-weight="600">1  island feasible opportunity</text>')
    lines.append('<text x="495" y="510" font-weight="600">2  local partner availability</text>')
    lines.append('<text x="865" y="510" font-weight="600">3  realized weighted architecture</text>')
    lines.append('</g>')
    lines.append('<line x1="365" y1="504" x2="465" y2="504" stroke="#7a858c" stroke-width="1.5"/>')
    lines.append('<line x1="760" y1="504" x2="835" y2="504" stroke="#7a858c" stroke-width="1.5"/>')

    # Evidence marker: qualitative only; no Menorca amplitude enters geometry.
    lines.append('<rect x="940" y="166" width="318" height="66" rx="10" fill="#fffdf7" stroke="#9a8f73"/>')
    lines.append('<text x="958" y="190" font-family="sans-serif" font-size="13" font-weight="600" fill="#554e3e">Empirical falsification marker</text>')
    lines.append('<text x="958" y="211" font-family="sans-serif" font-size="12" fill="#554e3e">Menorca (PR #195): v5 reweighting alone was insufficient.</text>')
    lines.append('<text x="958" y="227" font-family="sans-serif" font-size="12" fill="#554e3e">Its amplitudes do not set v6 branch widths here.</text>')

    # Locked partner-type labels on three reference cross-sections.
    for target in (0.0, 0.5, 1.0):
        row = min(gradient, key=lambda item: abs(float(item["isolation_index"]) - target))
        x = sx(float(row["isolation_index"]))
        value = float(row["final_partner_types"])
        y = RIVER_CENTER - MAX_HALF_WIDTH * value / max_partner - 14
        lines.append(f'<line x1="{x:.2f}" y1="{RIVER_CENTER-245:.2f}" x2="{x:.2f}" y2="{RIVER_CENTER+245:.2f}" stroke="#ffffff" stroke-opacity="0.32" stroke-width="1"/>')
        lines.append(
            f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" font-family="sans-serif" '
            f'font-size="12" fill="#17343b">feasible partners ≈ {value:.2f}</text>'
        )

    # State signatures, sharing the same isolation x-axis.
    lines.append('<text x="120" y="580" font-family="sans-serif" font-size="16" font-weight="600" fill="#17202a">Ecological state signatures along the same isolation axis</text>')
    state_colors = ["#1d5f6f", "#7a5a86", "#9b6a42"]
    for band_index, ((label, values), color) in enumerate(zip(state_series, state_colors)):
        points = [
            (sx(float(row["isolation_index"])), metric_y(value, band_index))
            for row, value in zip(gradient, values)
        ]
        y_mid = STATE_TOP + band_index * 56 + 23
        lines.append(f'<line x1="{X0}" y1="{y_mid:.2f}" x2="{X1}" y2="{y_mid:.2f}" stroke="#d5d9d8" stroke-width="1"/>')
        lines.append(f'<path d="{path_from_points(points)}" fill="none" stroke="{color}" stroke-width="3"/>')
        lines.append(
            f'<text x="{X1+10:.2f}" y="{points[-1][1]+4:.2f}" font-family="sans-serif" '
            f'font-size="12" fill="{color}">{escape(label)}</text>'
        )

    # Directional annotations.
    lines.append('<text x="120" y="825" font-family="sans-serif" font-size="12" fill="#59636a">Frozen v4 direction: partner types ↓, effective links ↓, interaction diversity ↓, plant niche overlap ↑; reproduction is not forced to decline monotonically.</text>')
    lines.append('<text x="1280" y="844" text-anchor="end" font-family="sans-serif" font-size="11" fill="#747d82">Isolation index is a normalized process gradient, not time or kilometres.</text>')
    lines.append('</svg>')

    sidecar = {
        "schema_version": "1.0",
        "visualization": "island_evolutionary_river_v1",
        "concept": "constrained evolutionary state space rather than agent animation",
        "sources": {
            "v4_gradient": str(V4_RESULT.relative_to(ROOT)),
            "v6_mechanism": str(V6_SCRIPT.relative_to(ROOT)),
            "v5_mechanism": str(V5_SCRIPT.relative_to(ROOT)),
            "empirical_falsification_marker": "PR #195, qualitative marker only",
        },
        "encodings": {
            "x_axis": "v4 isolation_index; process constraint, not chronological time",
            "outer_river_half_width": "MAX_HALF_WIDTH * final_partner_types / max(final_partner_types)",
            "outer_river_semantics": "island-scale feasible partner opportunity",
            "local_channels": "schematic v6 local-support alternatives; geometry uses generic SUPPORT_STRENGTHS only",
            "internal_channel_trace": "v5 within-support weight realization; subordinate texture only",
            "outside_river": "unavailable under the current island-scale opportunity constraint",
            "lower_trajectories": [
                "normalized frozen v4 interaction_diversity_proxy",
                "normalized frozen v4 plant_niche_overlap_proxy",
                "normalized frozen v4 mean_reproduction",
            ],
        },
        "frozen_v4_gradient": gradient,
        "v6_support_strengths": support_strengths,
        "v5_weight_strengths": weight_strengths,
        "menorca_amplitudes_used_in_geometry": False,
        "agent_animation": False,
        "chronological_reconstruction": False,
        "claim_boundary": (
            "This visualizes a constrained ecological/evolutionary state space. River width is model-derived "
            "from the frozen v4 partner-opportunity gradient; local branches represent the v6 support-varying "
            "mechanism class; internal traces represent v5 reweighting. It does not reconstruct historical time, "
            "assign causal habitats, or estimate the probability of a particular island trajectory."
        ),
    }
    return "\n".join(lines) + "\n", sidecar


def main() -> None:
    svg, sidecar = build()
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    OUT_SVG.write_text(svg)
    OUT_JSON.write_text(json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "svg": str(OUT_SVG),
        "json": str(OUT_JSON),
        "support_strengths": sidecar["v6_support_strengths"],
        "agent_animation": sidecar["agent_animation"],
        "chronological_reconstruction": sidecar["chronological_reconstruction"],
    }, indent=2))


if __name__ == "__main__":
    main()
