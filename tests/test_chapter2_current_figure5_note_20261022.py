"""Editorial Figure 5 layout and claim-boundary regression check (no biology)."""
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT / "figures/chapter2_nee_five_results/figure_05_persistence_options.svg"
NS = {"s": "http://www.w3.org/2000/svg"}


def test_current_figure_five_note_clears_last_row_and_does_not_claim_restoration():
    root = ET.parse(SVG).getroot()
    lines = [(el, "".join(el.itertext())) for el in root.findall(".//s:text", NS)]
    note = [(el, text) for el, text in lines if text.startswith("Green percentage =")]
    assert len(note) == 1
    el, value = note[0]
    assert "orange = alive but target closed" in value
    assert "gray = extinct" in value
    assert "recovered" not in value.lower()
    assert 1006 <= float(el.get("y")) <= 1016  # below bars, above panel D
    assert "evolving - fixed" in " ".join(t for _, t in lines)
    assert "−" not in " ".join(t for _, t in lines)
    original = SVG.read_bytes()
    assert b"<metadata" in original and b"source-lock" in original
    # Data-value/count/denominator marks must remain present, separately
    # checked numerically by tests/test_chapter2_paper_figures_20261019.py.
    assert len([n for n in root.findall(".//s:rect", NS)
                if n.get("data-kind") in ("survival", "closure")]) == 6
