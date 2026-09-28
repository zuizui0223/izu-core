from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
HIGHER = ROOT / "data/results/chapter2_el_higher_order_sufficiency_20260913.json"
NONLINEAR = ROOT / "data/results/chapter2_el_nonlinear_reduction_audit_20260913.json"
PHASE = ROOT / "data/results/chapter2_el_dense_phase_map_20260913.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_el_v04_figures"


def _save(fig, path: Path) -> tuple[Path, Path]:
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf = path.with_suffix(".pdf")
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)
    return path, pdf


def render_figure1(out: Path) -> tuple[Path, Path]:
    data = json.loads(HIGHER.read_text(encoding="utf-8"))["analytic"]["common_factor_contours"]
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3), sharey=False)
    for ax, contour in zip(axes, data):
        rows = contour["rows"]
        k = [row["k"] for row in rows]
        ax.plot(k, [row["variance_factor"] for row in rows], marker="o", label="second cumulant factor")
        ax.plot(k, [row["kappa3_factor"] for row in rows], marker="o", label="third cumulant factor")
        ax.plot(k, [row["kappa4_factor"] for row in rows], marker="o", label="fourth cumulant factor")
        ax.set_xscale("log", base=2)
        ax.set_xlabel("nominal pooled units, k")
        ax.set_ylabel("common-factor multiplier")
        ax.set_title(f"exact $k_{{eff}}={contour['k_eff']:.0f}$ contour")
        ax.legend(frameon=False, fontsize=8)
    fig.suptitle("Equal effective independence fixes variance, not higher cumulants", y=1.02)
    return _save(fig, out / "figure1_higher_cumulant_sufficiency.svg")


def render_figure2(out: Path) -> tuple[Path, Path]:
    data = json.loads(NONLINEAR.read_text(encoding="utf-8"))
    chapter = data["chapter2_abm_existing"]["rows"]
    consumer = data["adaptive_consumer_resource"]["illustrative_central_setting"]["rows"]
    fig, ax = plt.subplots(figsize=(6.5, 4.7))
    for rows, label, sk, ck, ik in (
        (chapter, "plant–pollinator", "S", "C", "I"),
        (consumer, "consumer–resource", "median_S", "median_C", "median_I"),
    ):
        x = [row[sk] / row[ck] for row in rows]
        y = [row[ik] / row[ck] for row in rows]
        ax.plot(x, y, marker="o", label=label)
        for xx, yy, row in zip(x, y, rows):
            ax.annotate(f"k={row['k']}", (xx, yy), xytext=(4, 3), textcoords="offset points", fontsize=7)
    ax.axhline(1.0, linestyle="--", linewidth=1.0, label="C = I")
    ax.set_xlabel("state/community ratio, S/C")
    ax.set_ylabel("interaction/community ratio, I/C")
    ax.set_title("Nonlinear systems cross the bilinear C/I boundary")
    ax.legend(frameon=False, fontsize=8)
    return _save(fig, out / "figure2_nonlinear_ci_crossing.svg")


def render_figure3(out: Path) -> tuple[Path, Path]:
    data = json.loads(HIGHER.read_text(encoding="utf-8"))
    failed = data["prespecified_handling_only_prediction"]
    fresh = data["fresh_mixed_feedback_validation"]["secondary"]["component_medians"]

    fig, (ax_fail, ax_fresh) = plt.subplots(1, 2, figsize=(10.8, 4.5))
    handling = [1.0, 2.0, 4.0]
    flips = [failed["by_handling"][str(h)]["sum_seed_flips"] for h in handling]
    h4 = np.asarray([failed["by_handling"][str(h)]["H4"] for h in handling], dtype=float)
    h4_scaled = h4 / h4.max() * max(flips)
    ax_fail.bar(np.arange(len(handling)), flips, alpha=0.65, label="C/I reversal seed-count")
    ax_fail.plot(np.arange(len(handling)), h4_scaled, marker="o", label="H4(h), scaled")
    ax_fail.set_xticks(np.arange(len(handling)), labels=[str(int(h)) for h in handling])
    ax_fail.set_xlabel("Holling handling h")
    ax_fail.set_ylabel("count / scaled predictor")
    ax_fail.set_title("Prespecified scalar-curvature prediction fails")
    ax_fail.legend(frameon=False, fontsize=8)

    for alpha, label in ((0.0, "feedback knockout, alpha=0"), (0.15, "active feedback, alpha=0.15")):
        rows = sorted([row for row in fresh if float(row["alpha"]) == alpha], key=lambda row: int(row["k"]))
        ax_fresh.plot(
            [row["k"] for row in rows],
            [row["C_gt_I_count"] / 108.0 for row in rows],
            marker="o",
            label=label,
        )
    ax_fresh.set_xscale("log", base=2)
    ax_fresh.set_ylim(-0.03, 0.55)
    ax_fresh.set_xlabel("pooled units, k")
    ax_fresh.set_ylabel("fraction of fresh cases with C > I")
    ax_fresh.set_title("Fresh intervention changes phase topology")
    ax_fresh.legend(frameon=False, fontsize=8)
    fig.suptitle("Scalar curvature is insufficient; state–community feedback shapes the phase", y=1.02)
    return _save(fig, out / "figure3_failed_predictor_fresh_feedback.svg")


def render_figure4(out: Path) -> tuple[Path, Path]:
    phase = json.loads(PHASE.read_text(encoding="utf-8"))
    nonlinear = json.loads(NONLINEAR.read_text(encoding="utf-8"))
    contour = sorted(
        [row for row in phase["exact_k_eff_contours"] if float(row["target_k_eff"]) == 2.0],
        key=lambda row: int(row["k"]),
    )
    corr = nonlinear["identity_preserving_event_correlation"]["rows"]

    fig, (ax_support, ax_corr) = plt.subplots(1, 2, figsize=(10.9, 4.5))
    support = [row["support"] for row in contour]
    for key, label in (("S", "S"), ("C", "C"), ("I", "I")):
        ax_support.plot(support, [row[key] for row in contour], marker="o", label=label)
    ax_support.set_xlabel("expected distinct trajectory support")
    ax_support.set_ylabel("variance share")
    ax_support.set_title("Exact $k_{eff}=2$: support changes")
    ax_support.legend(frameon=False, fontsize=8)

    ax_corr.plot(
        [row["count_variance_equivalent_k_eff"] for row in corr],
        [row["median_I_over_C"] for row in corr],
        marker="s",
        linestyle="--",
        label="identity-preserving shared events",
    )
    chapter = nonlinear["chapter2_abm_existing"]["rows"]
    ax_corr.plot(
        [row["k"] for row in chapter],
        [row["I_over_C"] for row in chapter],
        marker="o",
        label="independent pooling",
    )
    ax_corr.axhline(1.0, linestyle=":", linewidth=1.0, label="C = I")
    ax_corr.set_xscale("log", base=2)
    ax_corr.set_xlabel("variance-equivalent effective independence")
    ax_corr.set_ylabel("I/C")
    ax_corr.set_title("Mismatch persists with independent identities")
    ax_corr.legend(frameon=False, fontsize=7)
    fig.suptitle("Equal second-moment coordinates can fail by support or distributional routes", y=1.02)
    return _save(fig, out / "figure4_support_and_identity_preserving_routes.svg")


def render_all(out: Path = DEFAULT_OUT) -> list[Path]:
    paths: list[Path] = []
    for renderer in (render_figure1, render_figure2, render_figure3, render_figure4):
        paths.extend(renderer(out))
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    for path in render_all(args.out_dir):
        print(path)


if __name__ == "__main__":
    main()
