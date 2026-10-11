"""Draw registered primary endpoints from the immutable complete readout."""
from pathlib import Path
import argparse
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--readout", type=Path, required=True)
parser.add_argument("--out-dir", type=Path, required=True)
args = parser.parse_args()
data = json.loads(args.readout.read_text())
assert data["status"] == "COMPLETE_SYNTHETIC_TEMPORAL_SEQUENCE_OUTCOME_SOURCE_ONLY_NOT_NATURAL_ECOLOGY"
assert data["total_verified_trajectory_cases"] == 1024
assert len(data["results"]) == 8
rows = data["results"]
labels = [f"{r['timing'].capitalize()} · cost {r['direct_assurance_cost']:g} · μ {r['mutation_rate']:g}" for r in rows]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.hashsalt": "izu-core-tempo-20261011"})
fig, axes = plt.subplots(1, 2, figsize=(12.3, 7.5), sharey=True)
fig.subplots_adjust(left=.255, right=.98, top=.80, bottom=.235, wspace=.11)
panels = [
    ("A_crossed_by100", "Assurance increase: A ≥ founder + 0.05", "#2864A0"),
    ("I_crossed_by100", "Investment decrease: I ≤ founder − 0.05", "#B45A28"),
]
for ax, (key, title, color) in zip(axes, panels):
    points = np.array([r["outcomes"][key]["abrupt_minus_gradual"] for r in rows]) * 100
    bounds = np.array([r["outcomes"][key]["descriptive_history_profile_bootstrap95"] for r in rows]) * 100
    ax.axvspan(-10, 10, color="#F0F1F3", zorder=0)
    ax.axvline(0, color="#676C75", linewidth=1, zorder=1)
    for edge in (-10, 10):
        ax.axvline(edge, color="#ABB0B8", linewidth=.8, linestyle="--", zorder=1)
    ax.errorbar(points, np.arange(8), xerr=np.vstack((points-bounds[:, 0], bounds[:, 1]-points)),
                fmt="o", color=color, ecolor=color, markersize=6, elinewidth=1.8, capsize=3, zorder=3)
    ax.set_xlim(-35, 60)
    ax.set_xticks([-20, 0, 20, 40, 60])
    ax.set_yticks(np.arange(8), labels)
    ax.set_ylim(7.6, -.6)
    ax.axhline(3.5, color="#BEC3C9", linewidth=.8)
    ax.grid(axis="y", color="#E3E5E8", linewidth=.6, zorder=0)
    ax.set_title(title, fontsize=11, fontweight="bold", pad=14)
    ax.set_xlabel("Abrupt − gradual (percentage points)", labelpad=12)
    ax.tick_params(axis="y", length=0, pad=10)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#BEC3C9")
axes[1].tick_params(labelleft=False)
fig.suptitle("Inherited trait crossings under abrupt vs gradual functional loss", x=.04, y=.975,
             ha="left", fontsize=17, fontweight="bold", color="#232B36")
fig.text(.04, .925, "Complete frozen Model 3 cohort · crossings sustained for 20 updates and confirmed by update 100",
         fontsize=11, color="#4D5966")
fig.text(.04, .135, "Points: paired profile differences. Bars: descriptive 95% bootstrap percentile intervals.", fontsize=10)
fig.text(.04, .102, "16 synthetic profiles × 4 nested repeats; 9,999 resamples. Gray band marks the registered ±10 pp magnitude reference;",
         fontsize=9.5, color="#4D5966")
fig.text(.04, .073, "it does not establish equivalence. All eight settings retained. Occupancy at updates 100 and 400 was 100% in both arms.",
         fontsize=9.5, color="#4D5966")
args.out_dir.mkdir(parents=True, exist_ok=True)
for suffix in ("png", "svg"):
    output = args.out_dir / ("crossing_by100." + suffix)
    if output.exists():
        raise FileExistsError(output)
    extra = {"dpi": 180} if suffix == "png" else {"metadata": {"Date": None}}
    fig.savefig(output, facecolor="white", **extra)
    print(output)
plt.close(fig)
