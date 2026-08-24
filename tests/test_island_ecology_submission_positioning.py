from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSITION = ROOT / "docs/ISLAND_ECOLOGY_JOURNAL_POSITIONING_20260824.md"
REFS = ROOT / "docs/ISLAND_ECOLOGY_REFERENCE_MAP_20260824.md"
CAPTIONS = ROOT / "docs/ISLAND_ECOLOGY_FIGURE_CAPTIONS_20260824.md"


def test_journal_positioning_is_ecology_first():
    text = POSITION.read_text(encoding="utf-8")
    assert "### First target: Journal of Ecology" in text
    assert "### Second target: Functional Ecology" in text
    assert "### Third target: Oikos" in text
    assert "MEE is **not** the current target" in text
    assert "do not" in text.lower()
    assert "retune" in text.lower()
    assert "Dominica" in text


def test_reference_map_covers_conceptual_frame_and_all_strict_systems():
    text = REFS.read_text(encoding="utf-8")
    for doi in [
        "10.1111/nph.14534",
        "10.1111/nph.20234",
        "10.1093/oso/9780198868569.003.0011",
        "10.1111/plb.12636",
        "10.1146/annurev-ento-120120-102424",
        "10.1111/ele.70146",
        "10.1111/1365-2435.14527",
        "10.1098/rspb.2016.2218",
        "10.1111/1365-2745.12457",
        "10.1038/s41598-019-41271-5",
        "10.1111/1442-1984.12183",
        "10.1126/science.1199092",
        "10.1016/j.biocon.2008.06.014",
        "10.1016/j.gecco.2023.e02413",
        "10.1111/j.1744-7429.2008.00473.x",
        "10.1890/0012-9658(2000)081[1951:HCRAPL]2.0.CO;2",
        "10.1111/1365-2435.70415",
        "10.3732/ajb.91.5.672",
        "10.26786/1920-7603(2022)669",
        "10.1111/jeb.12053",
    ]:
        assert doi in text

    for group in ["Branching — 3 systems", "Same-direction propagation — 6 systems", "Buffering / alternative — 2 systems", "Protected constraint and falsification"]:
        assert group in text

    assert "not a prevalence estimate" in text
    assert "do not" in text.lower()


def test_figure_captions_match_ecology_mainline():
    text = CAPTIONS.read_text(encoding="utf-8")
    assert "## Figure 1. Island ecological response architecture" in text
    assert "## Figure 2. Pre-existing functional position is the replicated minimal generator of branching" in text
    assert "## Figure 3. Local interaction context reallocates branches, whereas assurance mainly attenuates propagation" in text
    assert "## Figure 4. Cross-island recurrence of branching, propagation, buffering and protected exceptions" in text
    assert "## Supplementary Figure S1. Observation-to-mechanism state-separability diagnostics" in text
    assert "0.4167" in text
    assert "16/96" in text
    assert "11/96" in text
    assert "207/216" in text
    assert "3 branching, six same-direction propagation" in text or "three branching, six same-direction propagation" in text
    assert "not a prevalence sample" in text
