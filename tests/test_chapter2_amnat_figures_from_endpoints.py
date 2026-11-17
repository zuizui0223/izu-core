"""Check figure artists against archived endpoints without running the biological model."""
import csv
import gzip
import re
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import binomtest

from scripts import render_chapter2_amnat_editorial_figures as renderer


def test_order_bars_and_paired_test_from_saved_onsets(monkeypatch):
    path = renderer.ROOT / "data/results/chapter2_direct_return_order_pilot_20261112.csv.gz"
    with gzip.open(path, "rt") as stream:
        rows = list(csv.DictReader(stream))
    outcomes = {"native": {}, "pooled": {}}
    for row in rows:
        a, i = (int(row[k]) if row[k] else None for k in ("a_onset", "i_onset"))
        if a is None:
            label = "neither" if i is None else "investment_only"
        elif i is None:
            label = "assurance_only"
        elif abs(a-i) <= 5:
            label = "near_simultaneous"
        else:
            label = "assurance_first" if a < i else "investment_first"
        assert row["order"] == label
        assert int(row["terminal_size"]) > 0
        outcomes[row["arm"]][int(row["block"])] = label
    assert len(rows) == 64
    blocks = set(range(32))
    assert set(outcomes["native"]) == set(outcomes["pooled"]) == blocks
    first = [{k for k in blocks if arm[k] == "assurance_first"} for arm in outcomes.values()]
    wins, losses = len(first[0]-first[1]), len(first[1]-first[0])
    assert (wins, losses) == (17, 1)
    assert round(binomtest(wins, wins+losses).pvalue, 6) == .000145

    def check(fig, name):
        ax = fig.axes[0]
        labels = [tick.get_text().lower().replace(" ", "_") for tick in ax.get_yticklabels()]
        for bars, arm in zip(ax.containers, outcomes.values(), strict=True):
            counts = Counter(arm.values())
            assert [bar.get_width() for bar in bars] == [counts[label] for label in labels]
        plt.close(fig)

    monkeypatch.setattr(renderer, "save", check)
    renderer.order()


def test_gap_diamonds_from_all_matched_endpoints(monkeypatch):
    frame = pd.read_csv(renderer.ROOT / "data/results/chapter2_common_cohort_bridge_20261112.csv.gz")
    assert len(frame) == 256 and (frame.n80 > 0).all()
    contrasts = {}
    for budget, group in frame.groupby("budget"):
        values = group.pivot(index="block", columns=["policy", "activity"], values="i80")
        assert values.shape == (32, 4) and values.notna().all().all()
        gaps = values.xs(1.6, axis=1, level="activity") - values.xs(.4, axis=1, level="activity")
        contrasts[budget] = (gaps.fixed - gaps.evolving).mean()

    def check(fig, name):
        ax = fig.axes[0]
        report = (renderer.DOCS / "CHAPTER2_Q1_FRESH_FOUNDER_RESULTS_20261016.md").read_text(encoding="utf8")
        cases = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
        assert len(ax.containers) == len(cases)
        for bars, case in zip(ax.containers, cases, strict=True):
            row = next(line for line in report.splitlines() if line.startswith("| " + case + " |"))
            cells = row.replace("*", "").replace("\u2212", "-").split("|")
            expected = [float(cells[3]), *map(float, re.findall(r"[+-]?\d+\.\d+", cells[4]))]
            marker, _, whiskers = bars.lines
            ends = whiskers[0].get_segments()[0][:, 0]
            assert np.allclose([marker.get_xdata()[0], *ends], expected, rtol=0, atol=.00000051)
        points = [line for line in ax.lines if line.get_marker() == "D"]
        assert len(points) == 2
        for pt in points:
            label = ax.get_yticklabels()[int(pt.get_ydata()[0])].get_text()
            budget = float(label.split("=")[-1])
            assert np.isclose(pt.get_xdata()[0], contrasts[budget], atol=.00005, rtol=0)
        plt.close(fig)

    monkeypatch.setattr(renderer, "save", check)
    renderer.gap()
