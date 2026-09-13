from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/results/chapter2_el_dense_phase_map_20260913.json"
OUT = ROOT / "data/results/chapter2_el_dense_phase_map_20260913.svg"

ORDER_CODE = {"CIS": 0, "ICS": 1, "ISC": 2, "SIC": 3, "CSI": 4, "SCI": 5}


def build_figure(source: Path = SOURCE, out: Path = OUT) -> None:
    data = json.loads(source.read_text(encoding="utf-8"))
    rows = data["grid_rows"]
    ks = sorted({int(row["k"]) for row in rows})
    rhos = sorted({float(row["rho"]) for row in rows})
    lookup = {(int(row["k"]), float(row["rho"])): row for row in rows}

    matrix = np.asarray(
        [[ORDER_CODE[lookup[(k, rho)]["order"]] for k in ks] for rho in rhos],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(6.8, 4.7))
    image = ax.imshow(matrix, origin="lower", aspect="auto", interpolation="nearest")
    ax.set_xticks(range(len(ks)), labels=ks)
    ax.set_yticks(range(len(rhos)), labels=[f"{rho:.2g}" for rho in rhos])
    ax.set_xlabel("pooled community copies, k")
    ax.set_ylabel("pairwise copy correlation, rho")

    for y, rho in enumerate(rhos):
        for x, k in enumerate(ks):
            ax.text(x, y, lookup[(k, rho)]["order"], ha="center", va="center", fontsize=8)

    contour_two = [row for row in data["exact_k_eff_contours"] if row["target_k_eff"] == 2.0]
    annotation = "k_eff=2 exact contour: " + " -> ".join(
        f"k={row['k']}: {row['order']}" for row in contour_two
    )
    ax.text(0.0, -0.18, annotation, transform=ax.transAxes, fontsize=8, va="top")
    fig.colorbar(image, ax=ax, label="determinant-order code")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    build_figure(args.source, args.out)


if __name__ == "__main__":
    main()
