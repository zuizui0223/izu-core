from pathlib import Path

from scripts.render_chapter2_el_main_figures import render_all


def test_el_main_figures_render_as_nonempty_svg_and_pdf_files(tmp_path: Path):
    paths = render_all(tmp_path)
    assert len(paths) == 8

    svg_paths = [path for path in paths if path.suffix == ".svg"]
    pdf_paths = [path for path in paths if path.suffix == ".pdf"]
    assert len(svg_paths) == 4
    assert len(pdf_paths) == 4

    for path in svg_paths:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "<svg" in text
        assert path.stat().st_size > 1000

    for path in pdf_paths:
        assert path.exists()
        assert path.read_bytes().startswith(b"%PDF")
        assert path.stat().st_size > 1000


def test_figure3_shows_continuous_same_keff_decomposition_not_order_alone(tmp_path: Path):
    paths = render_all(tmp_path)
    figure3 = next(path for path in paths if "figure3" in path.name and path.suffix == ".svg")
    text = figure3.read_text(encoding="utf-8")
    assert "Equal" in text or "equal" in text
    assert "Same effective independence, different decomposition" in text
    assert "state S" in text
    assert "community C" in text
    assert "interaction I" in text
    assert "D=6.07" in text
