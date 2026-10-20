"""Presentation-only checks against clipped Figure 4 annotation and tofu labels.

These do not adjudicate scientific data; numeric source-value checks remain
in tests/test_chapter2_paper_figures_20261019.py.
"""
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / "figures" / "chapter2_nee"
NS = {"s": "http://www.w3.org/2000/svg"}


def drawing(number, name):
    root = ET.parse(ROOT / f"figure_{number:02d}_{name}.svg").getroot()
    text = [(el, "".join(el.itertext())) for el in root.findall(".//s:text", NS)]
    return root, text


def test_ascii_safe_change_labels_in_figures_two_and_five():
    for number, label in ((2, "baseline_pollen"), (5, "variation_duration")):
        _, lines = drawing(number, label)
        assert lines
        joined = " ".join(text for _, text in lines)
        assert "\u2212" not in joined and "\u2192" not in joined
    _, lines2 = drawing(2, "baseline_pollen")
    words = " ".join(t for _, t in lines2)
    assert "decline - control" in words
    assert "q maintained to q declined" in words
    assert "0.142 to 0.017" in words


def test_figure_four_note_clears_bottom_bar_and_next_panel():
    root, lines = drawing(4, "access_survival")
    note = [el for el, text in lines if text.startswith("Green percentage at right =")]
    assert len(note) == 1
    baseline = float(note[0].get("y"))
    bars = []
    for rect in root.findall(".//s:rect", NS):
        y = float(rect.get("y", "0"))
        h = float(rect.get("height", "0"))
        if y > 750 and y < 1036 and abs(h - 37) < 1e-8:
            bars.append(y + h)
    assert bars and max(bars) == 981
    assert baseline >= max(bars) + 25  # text top clears the bar
    assert baseline <= 1036 - 20       # enough space before panel D
    assert "\u2212" not in " ".join(t for _, t in lines)
