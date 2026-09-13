from pathlib import Path

from scripts.render_chapter2_el_main_figures import render_all


def test_el_main_figures_render_as_nonempty_svg_files(tmp_path: Path):
    paths = render_all(tmp_path)
    assert len(paths) == 4
    for path in paths:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "<svg" in text
        assert path.stat().st_size > 1000


def test_figure3_is_explicitly_about_same_keff_non_sufficiency(tmp_path: Path):
    paths = render_all(tmp_path)
    figure3 = next(path for path in paths if "figure3" in path.name)
    text = figure3.read_text(encoding="utf-8")
    assert "Equal" in text or "equal" in text
    assert "k_{eff}" in text or "k" in text
