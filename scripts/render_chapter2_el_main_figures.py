from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
GENERIC_DESIGN = ROOT / "data/design/chapter2_el_rank_crossover_generalization_freeze_20260912.json"
NONLINEAR = ROOT / "data/results/chapter2_el_nonlinear_reduction_audit_20260913.json"
PHASE = ROOT / "data/results/chapter2_el_dense_phase_map_20260913.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_el_figures"

ORDER_CODES = {"CIS": 0, "ICS": 1, "ISC": 2, "SIC": 3, "CSI": 4, "SCI": 5}
ORDER_LABELS = ["CIS", "ICS", "ISC", "SIC", "CSI", "SCI"]


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def render_figure1(out: Path) -> None:
    design = json.loads(GENERIC_DESIGN.read_text(encoding="utf-8"))["generic_exact_audit"]
    s = float(design["a"]) ** 2 * float(design["x_variance"])
    b2_sigma2 = float(design["b"]) ** 2 * float(design["z_variance"])

    x = np.linspace(1.0, 16.0, 420)
    r = np.linspace(0.1, 4.0, 360)
    xx, rr = np.meshgrid(x, r)
    community = b2_sigma2 / xx
    interaction = rr * community
    starting = np.full_like(community, s)
    stack = np.stack([starting, community, interaction], axis=-1)
    labels = np.asarray(list("SCI"))
    order = np.empty(stack.shape[:2], dtype=int)
    for iy in range(stack.shape[0]):
        for ix in range(stack.shape[1]):
            text = "".join(labels[np.argsort(stack[iy, ix])[::-1]])
            order[iy, ix] = ORDER_CODES[text]

    fig, ax = plt.subplots(figsize=(6.7, 4.9))
    image = ax.imshow(
        order,
        origin="lower",
        aspect="auto",
        extent=[x.min(), x.max(), r.min(), r.max()],
        interpolation="nearest",
    )
    ax.axhline(1.0, linewidth=1.0, linestyle="--", label="C = I")
    x_sc = b2_sigma2 / s
    ax.axvline(x_sc, linewidth=1.0, linestyle=":", label="S = C")
    ax.plot(x, s * x / b2_sigma2, linewidth=1.0, label="S = I")
    ax.set_xlabel("variance-equivalent effective independence, $k_{eff}$")
    ax.set_ylabel("bilinear interaction/community ratio, $I/C$")
    ax.set_xlim(1, 16)
    ax.set_ylim(0.1, 4.0)
    colorbar = fig.colorbar(image, ax=ax, ticks=range(len(ORDER_LABELS)))
    colorbar.ax.set_yticklabels(ORDER_LABELS)
    colorbar.set_label("determinant order")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Exact bilinear phase structure")
    _save(fig, out / "figure1_exact_bilinear_phase.svg")


def render_figure2(out: Path) -> None:
    data = json.loads(NONLINEAR.read_text(encoding="utf-8"))
    chapter = data["chapter2_abm_existing"]["rows"]
    consumer = data["adaptive_consumer_resource"]["illustrative_central_setting"]["rows"]

    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    for rows, label, s_key, c_key, i_key in (
        (chapter, "plant–pollinator nonlinear system", "S", "C", "I"),
        (consumer, "adaptive consumer–resource system", "median_S", "median_C", "median_I"),
    ):
        xs = [row[s_key] / row[c_key] for row in rows]
        ys = [row[i_key] / row[c_key] for row in rows]
        ks = [row["k"] for row in rows]
        ax.plot(xs, ys, marker="o", label=label)
        for x, y, k in zip(xs, ys, ks):
            ax.annotate(f"k={k}", (x, y), xytext=(4, 3), textcoords="offset points", fontsize=7)

    design = json.loads(GENERIC_DESIGN.read_text(encoding="utf-8"))["generic_exact_audit"]
    bilinear_ratio = float(design["c"]) ** 2 * float(design["x_variance"]) / float(design["b"]) ** 2
    ax.axhline(1.0, linewidth=1.0, linestyle="--", label="C/I reversal boundary")
    ax.axhline(bilinear_ratio, linewidth=1.0, linestyle=":", label="exact bilinear I/C")
    ax.set_xlabel("state/community ratio, $S/C$")
    ax.set_ylabel("interaction/community ratio, $I/C$")
    ax.set_title("Nonlinear trajectories cross the bilinear C/I constraint")
    ax.legend(frameon=False, fontsize=8)
    _save(fig, out / "figure2_nonlinear_ratio_trajectories.svg")


def render_figure3(out: Path) -> None:
    data = json.loads(PHASE.read_text(encoding="utf-8"))
    rows = data["grid_rows"]
    ks = sorted({int(row["k"]) for row in rows})
    rhos = sorted({float(row["rho"]) for row in rows})
    lookup = {(int(row["k"]), float(row["rho"])): row for row in rows}
    matrix = np.asarray([[ORDER_CODES[lookup[(k, rho)]["order"]] for k in ks] for rho in rhos], dtype=float)
    xpos = np.arange(len(ks), dtype=float)

    fig, ax = plt.subplots(figsize=(6.8, 4.9))
    image = ax.imshow(matrix, origin="lower", aspect="auto", interpolation="nearest")
    ax.set_xticks(xpos, labels=ks)
    ax.set_yticks(np.arange(len(rhos)), labels=[f"{rho:.2g}" for rho in rhos])
    ax.set_xlabel("pooled community copies, k")
    ax.set_ylabel("pairwise copy correlation, rho")
    for iy, rho in enumerate(rhos):
        for ix, k in enumerate(ks):
            ax.text(ix, iy, lookup[(k, rho)]["order"], ha="center", va="center", fontsize=8)

    # Exact k_eff=2 contour, expressed in the categorical plotting coordinates.
    contour = [row for row in data["exact_k_eff_contours"] if row["target_k_eff"] == 2.0]
    cx = [ks.index(int(row["k"])) for row in contour]
    cy = [np.interp(float(row["rho"]), rhos, np.arange(len(rhos))) for row in contour]
    ax.plot(cx, cy, marker="o", linewidth=1.5, label="$k_{eff}=2$ exact contour")
    for x, y, row in zip(cx, cy, contour):
        ax.annotate(
            f"D={row['support']:.2f}\n{row['order']}",
            (x, y), xytext=(5, 5), textcoords="offset points", fontsize=7,
        )
    colorbar = fig.colorbar(image, ax=ax, ticks=range(len(ORDER_LABELS)))
    colorbar.ax.set_yticklabels(ORDER_LABELS)
    colorbar.set_label("determinant order")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_title("Equal $k_{eff}$ does not preserve nonlinear phase")
    _save(fig, out / "figure3_dense_keff_phase_map.svg")


def render_figure4(out: Path) -> None:
    data = json.loads(NONLINEAR.read_text(encoding="utf-8"))
    chapter = data["chapter2_abm_existing"]["rows"]
    consumer = data["adaptive_consumer_resource"]["illustrative_central_setting"]["rows"]
    corr = data["identity_preserving_event_correlation"]["rows"]

    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    ax.plot([row["k"] for row in chapter], [row["I_over_C"] for row in chapter], marker="o", label="plant–pollinator: independent pooling")
    ax.plot([row["k"] for row in consumer], [row["median_I_over_C"] for row in consumer], marker="o", label="consumer–resource: independent pooling")
    ax.plot(
        [row["count_variance_equivalent_k_eff"] for row in corr],
        [row["median_I_over_C"] for row in corr],
        marker="s", linestyle="--", label="plant–pollinator: shared-event correlation",
    )
    design = json.loads(GENERIC_DESIGN.read_text(encoding="utf-8"))["generic_exact_audit"]
    bilinear_ratio = float(design["c"]) ** 2 * float(design["x_variance"]) / float(design["b"]) ** 2
    ax.axhline(bilinear_ratio, linewidth=1.0, linestyle=":", label="exact bilinear I/C")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("raw k (independent pooling) or variance-equivalent $k_{eff}$ (correlated audit)")
    ax.set_ylabel("interaction/community ratio, $I/C$")
    ax.set_title("I/C diagnoses departure from the linearized reduction")
    ax.legend(frameon=False, fontsize=7)
    _save(fig, out / "figure4_interaction_community_diagnostic.svg")


def render_all(out: Path = DEFAULT_OUT) -> list[Path]:
    render_figure1(out)
    render_figure2(out)
    render_figure3(out)
    render_figure4(out)
    return [
        out / "figure1_exact_bilinear_phase.svg",
        out / "figure2_nonlinear_ratio_trajectories.svg",
        out / "figure3_dense_keff_phase_map.svg",
        out / "figure4_interaction_community_diagnostic.svg",
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    for path in render_all(args.out_dir):
        print(path)


if __name__ == "__main__":
    main()
