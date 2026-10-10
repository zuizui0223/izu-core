"""Draw Figure 1 from three ORIGINAL byte-validated cohort JSONs.

No biological simulation, new bootstrap, pooled standard error, or evidence-
rank promotion. Uses the existing cross-cohort audit() as the source of truth.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from xml.sax.saxutils import escape

from scripts.audit_chapter2_k_at_b48_crosscohort import audit


XMIN = -0.005
XMAX = 0.022
LEFT = 224
WIDTH = 652
YS = (147, 229, 311)
LABELS = (
    "K×B four-arm cohort",
    "Fixed-B48 K primary",
    "Timed-viability cohort",
)
RANKS = ("Secondary/descriptive", "Preregistered primary", "Secondary/descriptive")


def xp(x):
    if not XMIN <= x <= XMAX:
        raise AssertionError("Original cohort interval exceeds fixed visible axis")
    return LEFT + (x - XMIN) / (XMAX - XMIN) * WIDTH


def render_svg():
    data = audit()  # original JSON SHA-256 and separate primary evidence ranks
    rows = data["rows"]
    if (len(rows) != 3 or data["model_family_count"] != 1
            or sum(r["evidence_rank"] == "preregistered_primary_supported"
                   for r in rows) != 1):
        raise AssertionError("Unexpected inference/evidence rank")
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="465" viewBox="0 0 1100 465" role="img" aria-labelledby="chartTitle chartDesc">',
        '<title id="chartTitle">Three separate independent cohorts: K moderation at fixed B48</title>',
        '<desc id="chartDesc">Original 64-visitor-history paired bootstrap 95 percent intervals for three distinct cohorts; only the middle study preregistered this as its primary test.</desc>',
        '<rect width="1100" height="465" fill="#ffffff"/>',
        '<text x="42" y="43" font-size="22" font-weight="700" fill="#15283b" font-family="Arial, sans-serif">Population-capacity moderation at fixed pollen background (B=48)</text>',
        '<text x="42" y="70" font-size="14" fill="#46596b" font-family="Arial, sans-serif">Original point estimates and original 95% paired visitor-history bootstrap intervals</text>',
        '<line x1="42" x2="1057" y1="87" y2="87" stroke="#dce3e9"/>',
    ]
    for t in (-0.005, 0.0, 0.005, 0.010, 0.015, 0.020):
        x = xp(t)
        color = "#738598" if t == 0 else "#dce3e9"
        dash = ' stroke-dasharray="5,4"' if t == 0 else ""
        parts += [
            f'<line x1="{x:.2f}" x2="{x:.2f}" y1="101" y2="357" stroke="{color}" stroke-width="{2 if t == 0 else 1}"{dash}/>',
            f'<text x="{x:.2f}" y="382" text-anchor="middle" font-size="12" fill="#435365" font-family="Arial, sans-serif">{t:+.3f}</text>',
        ]
    for i, row in enumerate(rows):
        y = YS[i]
        est = float(row["effect_mean"])
        lo, hi = map(float, row["bootstrap95"])
        if not lo <= est <= hi:
            raise AssertionError("Original CI/mean mismatch")
        primary = row["evidence_rank"] == "preregistered_primary_supported"
        color = "#177d76" if primary else "#7d8da1"
        lo_x, hi_x, m_x = xp(lo), xp(hi), xp(est)
        parts += [
            f'<text x="42" y="{y-11}" font-size="16" font-weight="{700 if primary else 500}" fill="#203449" font-family="Arial, sans-serif">{escape(LABELS[i])}</text>',
            f'<text x="42" y="{y+13}" font-size="12" fill="#576b80" font-family="Arial, sans-serif">{escape(RANKS[i])} · 64 visitor histories</text>',
            f'<line x1="{lo_x:.2f}" x2="{hi_x:.2f}" y1="{y}" y2="{y}" stroke="{color}" stroke-width="5" stroke-linecap="round"/>',
            f'<line x1="{lo_x:.2f}" x2="{lo_x:.2f}" y1="{y-8}" y2="{y+8}" stroke="{color}" stroke-width="2"/>',
            f'<line x1="{hi_x:.2f}" x2="{hi_x:.2f}" y1="{y-8}" y2="{y+8}" stroke="{color}" stroke-width="2"/>',
        ]
        if primary:
            parts.append(f'<rect x="{m_x-6:.2f}" y="{y-6}" width="12" height="12" rx="2" fill="{color}" stroke="#ffffff" stroke-width="2"/>')
        else:
            parts.append(f'<circle cx="{m_x:.2f}" cy="{y}" r="6" fill="{color}" stroke="#ffffff" stroke-width="2"/>')
        parts.append(f'<text x="902" y="{y+5}" font-size="14" font-weight="{700 if primary else 400}" fill="#243a4c" font-family="Arial, sans-serif">{est:+.4f}</text>')
    parts += [
        '<text x="550" y="413" text-anchor="middle" font-size="14" fill="#34465a" font-family="Arial, sans-serif">Difference in viability sensitivity, K8 minus K48 (absolute occupancy probability)</text>',
        '<text x="42" y="448" font-size="12" fill="#5c6b7a" font-family="Arial, sans-serif">Square: one preregistered primary. Circles: secondary/descriptive. Not a pooled meta-analysis or three confirmations.</text>',
        '</svg>',
    ]
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    target = args.out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_svg(), encoding="utf-8")
    print(f"Read-only SVG rendered from three SHA-pinned original machine results: {target}")


if __name__ == "__main__":
    main()
