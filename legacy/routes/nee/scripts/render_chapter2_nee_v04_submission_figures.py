from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from scripts.render_chapter2_nee_v03_figures import (
    DEFAULT_OUT,
    _audit_counts,
    _box,
    _save,
    render_figure1,
    render_figure2,
    render_figure3,
)


DEFAULT_SUBMISSION_OUT = DEFAULT_OUT.parent / "chapter2_nee_v04_submission_figures"


def render_figure4(out: Path) -> tuple[Path, Path]:
    """Submission-layout-only redraw of the frozen 21/25, 2/25, 0/25 audit.

    This changes no scientific value, denominator, label meaning, or claim. The
    only purpose is to prevent long categorical labels from colliding when the
    figure is embedded at journal-manuscript width.
    """
    total, responses, arrivals, full = _audit_counts()
    fig, (ax_a, ax_b) = plt.subplots(
        1,
        2,
        figsize=(12.0, 5.3),
        gridspec_kw={"width_ratios": [1.0, 1.65]},
    )

    labels = [
        "Comparable plant\nresponse",
        "Direct partner\narrival/replacement",
        "Complete outcome-\nindependent contract",
    ]
    counts = [responses, arrivals, full]
    y_positions = [2, 1, 0]
    ax_a.barh(y_positions, counts)
    ax_a.set_yticks(y_positions, labels=labels)
    ax_a.set_xlim(0, total)
    ax_a.set_xlabel("research entries (of 25)")
    ax_a.set_title("a  Existing island evidence is outcome-rich but process-poor", loc="left")
    for y, count in zip(y_positions, counts):
        ax_a.text(count + 0.45 if count > 0 else 0.45, y, f"{count}/25", va="center", fontsize=9)

    ax_b.set_xlim(0, 1)
    ax_b.set_ylim(0, 1)
    ax_b.axis("off")
    y = 0.58
    w, h = 0.19, 0.20
    positions = [0.02, 0.27, 0.52, 0.77]
    texts = [
        "source\nstate",
        "transition /\nfiltering",
        "realized community\n(breadth, synchrony)",
        "plant\nresponse",
    ]
    for x, text in zip(positions, texts):
        _box(ax_b, (x, y), w, h, text, fontsize=9)
    for x1, x2 in zip(positions[:-1], positions[1:]):
        ax_b.annotate(
            "",
            xy=(x2 - 0.01, y + h / 2),
            xytext=(x1 + w + 0.01, y + h / 2),
            arrowprops={"arrowstyle": "->", "lw": 1.2},
        )
    ax_b.text(0.5, 0.91, "b  Transport requires the full determinant-response chain", ha="center", fontsize=10)
    ax_b.text(
        0.5,
        0.38,
        "42-system regime map estimates context; it does not add matched outcomes",
        ha="center",
        fontsize=9,
    )
    ax_b.text(
        0.5,
        0.20,
        "0/25 audited entries currently identify the complete chain",
        ha="center",
        fontsize=10,
        fontweight="bold",
    )
    ax_b.text(
        0.5,
        0.08,
        "Prospective tests should measure breadth and synchrony before opening response outcomes",
        ha="center",
        fontsize=8.5,
    )

    fig.suptitle("The natural measurement ceiling defines the next test", y=0.995, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return _save(fig, out / "figure4_measurement_ceiling_and_transport.svg")


def render_all(out: Path = DEFAULT_SUBMISSION_OUT) -> list[Path]:
    paths: list[Path] = []
    for renderer in (render_figure1, render_figure2, render_figure3, render_figure4):
        paths.extend(renderer(out))
    return paths


if __name__ == "__main__":
    for path in render_all():
        print(path)
