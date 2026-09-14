from __future__ import annotations

import json
import math
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
HIGHER = ROOT / "data/results/chapter2_el_higher_order_sufficiency_20260913.json"
NONLINEAR = ROOT / "data/results/chapter2_el_nonlinear_reduction_audit_20260913.json"
AUDIT_DOC = ROOT / "paper/README.md"
DEFAULT_OUT = ROOT / "data/results/chapter2_nee_v03_figures"

COORDINATE_FILES = [
    ROOT / "data/results/chapter2_hawaii_natural_regime_coordinate_20260914.json",
    ROOT / "data/results/chapter2_mallorca_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_tenerife_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_cabrera_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_martinique_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_roberts_england_natural_regime_coordinates_20260915.json",
]

SOURCE_LABELS = {
    "aslan_etal_2019_hawaii_native_pollination": "Hawaii",
    "lazaro_etal_2022_mallorca_stability": "Mallorca",
    "lara_romero_etal_2019_tenerife_pollination": "Tenerife",
    "serra_marin_etal_2025_cabrera_pollination": "Cabrera",
    "cyrille_etal_2025_martinique_gardens": "Martinique",
    "euppollnet_31_roberts_england_step": "Great Britain",
}


def _save(fig, path: Path) -> tuple[Path, Path]:
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf = path.with_suffix(".pdf")
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)
    return path, pdf


def _load_coordinate_rows() -> list[dict]:
    rows: list[dict] = []
    for path in COORDINATE_FILES:
        payload = json.loads(path.read_text(encoding="utf-8"))
        current = payload.get("systems")
        if current is None:
            current = [payload["coordinate"]]
        source = payload.get("source") or {}
        for raw in current:
            row = dict(raw)
            row.setdefault("source_study_id", source.get("source_study_id"))
            row.setdefault("archipelago_id", source.get("archipelago_id"))
            if not row.get("source_study_id"):
                raise RuntimeError(f"{path}: missing source_study_id")
            rows.append(row)
    if len(rows) != 42:
        raise RuntimeError(f"expected frozen 42-system plane, observed {len(rows)}")
    return rows


def render_figure1(out: Path) -> tuple[Path, Path]:
    data = json.loads(HIGHER.read_text(encoding="utf-8"))["analytic"]["common_factor_contours"]
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3))
    for ax, contour in zip(axes, data):
        rows = contour["rows"]
        k = [row["k"] for row in rows]
        ax.plot(k, [row["variance_factor"] for row in rows], marker="o", label="second cumulant")
        ax.plot(k, [row["kappa3_factor"] for row in rows], marker="o", label="third cumulant")
        ax.plot(k, [row["kappa4_factor"] for row in rows], marker="o", label="fourth cumulant")
        ax.set_xscale("log", base=2)
        ax.set_xlabel("nominal pooled units, k")
        ax.set_ylabel("common-factor multiplier")
        ax.set_title(f"fixed $k_{{eff}}={contour['k_eff']:.0f}$")
        ax.legend(frameon=False, fontsize=8)
    fig.suptitle("A variance-equivalent effective number fixes the second moment only", y=1.02)
    return _save(fig, out / "figure1_sufficiency_boundary.svg")


def render_figure2(out: Path) -> tuple[Path, Path]:
    nonlinear = json.loads(NONLINEAR.read_text(encoding="utf-8"))
    higher = json.loads(HIGHER.read_text(encoding="utf-8"))
    chapter = nonlinear["chapter2_abm_existing"]["rows"]
    consumer = nonlinear["adaptive_consumer_resource"]["illustrative_central_setting"]["rows"]
    failed = higher["prespecified_handling_only_prediction"]
    fresh = higher["fresh_mixed_feedback_validation"]["secondary"]["component_medians"]

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 8.4))
    ax_a, ax_b, ax_c, ax_d = axes.flat

    for rows, label, sk, ck, ik in (
        (chapter, "plant–pollinator", "S", "C", "I"),
        (consumer, "consumer–resource", "median_S", "median_C", "median_I"),
    ):
        ax_a.plot([row[sk] / row[ck] for row in rows], [row[ik] / row[ck] for row in rows], marker="o", label=label)
    ax_a.axhline(1.0, linestyle="--", linewidth=1.0)
    ax_a.set_xlabel("state/community ratio, S/C")
    ax_a.set_ylabel("interaction/community ratio, I/C")
    ax_a.set_title("a  Two nonlinear systems cross C = I")
    ax_a.legend(frameon=False, fontsize=8)

    for rows, label, sk, ck, ik in (
        (chapter, "plant–pollinator", "S", "C", "I"),
        (consumer, "consumer–resource", "median_S", "median_C", "median_I"),
    ):
        k = [row["k"] for row in rows]
        ax_b.plot(k, [row[ik] / row[ck] for row in rows], marker="o", label=label)
    ax_b.axhline(1.0, linestyle="--", linewidth=1.0)
    ax_b.set_xscale("log", base=2)
    ax_b.set_xlabel("pooled units, k")
    ax_b.set_ylabel("I/C")
    ax_b.set_title("b  Aggregation changes determinant order")

    handling = [1.0, 2.0, 4.0]
    flips = [failed["by_handling"][str(h)]["sum_seed_flips"] for h in handling]
    h4 = np.asarray([failed["by_handling"][str(h)]["H4"] for h in handling], dtype=float)
    h4_scaled = h4 / h4.max() * max(flips)
    ax_c.bar(np.arange(len(handling)), flips, alpha=0.65, label="observed reversal count")
    ax_c.plot(np.arange(len(handling)), h4_scaled, marker="o", label="H4(h), scaled")
    ax_c.set_xticks(np.arange(len(handling)), labels=[str(int(h)) for h in handling])
    ax_c.set_xlabel("Holling handling, h")
    ax_c.set_ylabel("count / scaled predictor")
    ax_c.set_title("c  Prespecified scalar-curvature prediction fails")
    ax_c.legend(frameon=False, fontsize=8)

    for alpha, label in ((0.0, "feedback knockout"), (0.15, "active feedback")):
        rows = sorted([row for row in fresh if float(row["alpha"]) == alpha], key=lambda row: int(row["k"]))
        ax_d.plot([row["k"] for row in rows], [row["C_gt_I_count"] / 108.0 for row in rows], marker="o", label=label)
    ax_d.set_xscale("log", base=2)
    ax_d.set_ylim(-0.03, 0.55)
    ax_d.set_xlabel("pooled units, k")
    ax_d.set_ylabel("fraction with C > I")
    ax_d.set_title("d  Fresh feedback intervention reshapes the phase")
    ax_d.legend(frameon=False, fontsize=8)

    fig.suptitle("Nonlinear determinant order is phase dependent", y=0.995)
    fig.tight_layout()
    return _save(fig, out / "figure2_nonlinear_phase_and_feedback.svg")


def render_figure3(out: Path) -> tuple[Path, Path]:
    rows = _load_coordinate_rows()
    fig, ax = plt.subplots(figsize=(7.5, 5.8))
    sources = list(SOURCE_LABELS)
    markers = ["o", "s", "^", "D", "v", "P"]

    for source, marker in zip(sources, markers):
        current = [row for row in rows if row["source_study_id"] == source]
        x = np.asarray([float(row["breadth_D1"]) for row in current])
        y = np.asarray([float(row["phi"]) for row in current])
        xlo = np.asarray([float(row["breadth_D1_ci95"][0]) for row in current])
        xhi = np.asarray([float(row["breadth_D1_ci95"][1]) for row in current])
        ylo = np.asarray([float(row["phi_ci95"][0]) for row in current])
        yhi = np.asarray([float(row["phi_ci95"][1]) for row in current])
        ax.errorbar(
            x,
            y,
            xerr=np.vstack([x - xlo, xhi - x]),
            yerr=np.vstack([y - ylo, yhi - y]),
            fmt=marker,
            markersize=5.5,
            capsize=0,
            elinewidth=0.55,
            alpha=0.72,
            label=f"{SOURCE_LABELS[source]} (n={len(current)})",
        )

    ax.set_xscale("log")
    ax.set_xlabel("partner breadth, Hill $D_1$")
    ax.set_ylabel("temporal synchrony, $\phi$")
    ax.set_title("Natural island interaction systems occupy a two-dimensional regime plane")
    ax.legend(frameon=False, fontsize=8, ncol=2)

    summary = (
        "42 systems · 6 studies · 5 island groups\n"
        "$D_1$ q90/q10 = 4.52 · $\phi$ span = 0.352\n"
        "source-balanced |Spearman| = 0.325\n"
        "largest-source removal: $D_1$ ratio = 5.49, $\phi$ span = 0.352"
    )
    ax.text(0.02, 0.98, summary, transform=ax.transAxes, va="top", ha="left", fontsize=8,
            bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "alpha": 0.82, "edgecolor": "0.7"})
    return _save(fig, out / "figure3_natural_breadth_synchrony_plane.svg")


def _audit_counts() -> tuple[int, int, int, int]:
    text = AUDIT_DOC.read_text(encoding="utf-8")
    expected = (("21/25", 21), ("2/25", 2), ("0/25", 0))
    for token, _ in expected:
        if token not in text:
            raise RuntimeError(f"frozen audit token missing from {AUDIT_DOC}: {token}")
    return 25, 21, 2, 0


def _box(ax, xy, width, height, text, fontsize=9):
    x, y = xy
    patch = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.02", linewidth=1.0, fill=False)
    ax.add_patch(patch)
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=fontsize)
    return patch


def render_figure4(out: Path) -> tuple[Path, Path]:
    total, responses, arrivals, full = _audit_counts()
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11.0, 4.8), gridspec_kw={"width_ratios": [0.9, 1.5]})

    labels = ["Comparable\nplant response", "Direct partner\narrival/replacement", "Complete\noutcome-independent contract"]
    counts = [responses, arrivals, full]
    bars = ax_a.bar(np.arange(3), counts)
    ax_a.set_ylim(0, total)
    ax_a.set_ylabel("research entries (of 25)")
    ax_a.set_xticks(np.arange(3), labels=labels)
    ax_a.set_title("a  Existing island evidence is outcome-rich but process-poor")
    for bar, count in zip(bars, counts):
        ax_a.text(bar.get_x() + bar.get_width() / 2, count + 0.7, f"{count}/25", ha="center", va="bottom", fontsize=9)

    ax_b.set_xlim(0, 1)
    ax_b.set_ylim(0, 1)
    ax_b.axis("off")
    y = 0.58
    w, h = 0.18, 0.20
    positions = [0.02, 0.28, 0.54, 0.80]
    texts = ["source\nstate", "transition /\nfiltering", "realized community\n(breadth, synchrony)", "plant\nresponse"]
    for x, text in zip(positions, texts):
        _box(ax_b, (x, y), w, h, text, fontsize=8.5)
    for x1, x2 in zip(positions[:-1], positions[1:]):
        ax_b.annotate("", xy=(x2 - 0.01, y + h / 2), xytext=(x1 + w + 0.01, y + h / 2),
                      arrowprops={"arrowstyle": "->", "lw": 1.2})
    ax_b.text(0.5, 0.90, "b  Transport requires the full determinant–response chain", ha="center", fontsize=10)
    ax_b.text(0.5, 0.38, "42-system regime map estimates context; it does not add matched outcomes", ha="center", fontsize=9)
    ax_b.text(0.5, 0.20, "0/25 audited entries currently identify the complete chain", ha="center", fontsize=10, fontweight="bold")
    ax_b.text(0.5, 0.08, "Prospective tests should measure breadth and synchrony before opening response outcomes", ha="center", fontsize=8.5)

    fig.suptitle("The natural measurement ceiling defines the next test", y=1.01)
    fig.tight_layout()
    return _save(fig, out / "figure4_measurement_ceiling_and_transport.svg")


def render_all(out: Path = DEFAULT_OUT) -> list[Path]:
    paths: list[Path] = []
    for renderer in (render_figure1, render_figure2, render_figure3, render_figure4):
        paths.extend(renderer(out))
    return paths


if __name__ == "__main__":
    for path in render_all():
        print(path)
