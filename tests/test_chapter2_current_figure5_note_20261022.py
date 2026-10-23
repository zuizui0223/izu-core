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

 
def test_current_figure_four_rejects_corrupted_symbols_and_unidentified_variance_claim():
    p = ROOT / "figures/chapter2_nee_five_results/figure_04_predictability.svg"
    t = p.read_text(encoding="utf-8")
    assert "竕" not in t and "\uf8f0" not in t
    assert "endpoint agreement is not selection strength" in t
    assert "prediction skill is not a causal variance share" in t
    root = ET.parse(p).getroot()
    assert root.find("s:metadata", NS) is not None


def test_current_figure_six_retains_conditional_not_adaptation_claim():
    p = ROOT / "figures/chapter2_nee_five_results/figure_06_transfer.svg"
    t = p.read_text(encoding="utf-8")
    assert "Late transfer separates inherited support and response" in t
    assert "limits to adaptation" not in t
    assert "survivors" in t.lower()


def test_current_figure_five_caveat_has_no_unsupported_not_equal_glyph():
    t = SVG.read_text(encoding="utf-8")
    assert "G/S registered inference is not the descriptive joint endpoint" in t
    assert "≠" not in t
    assert "D · POST-HOC contrast; crossed-source intervals in source audit" in t
    assert "no newly estimated uncertainty" not in t

