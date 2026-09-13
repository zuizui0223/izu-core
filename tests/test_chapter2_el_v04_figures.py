from pathlib import Path

from scripts.render_chapter2_el_v04_figures import render_all


def test_el_v04_figures_render_from_committed_results(tmp_path: Path) -> None:
    paths = render_all(tmp_path)
    assert len(paths) == 8
    assert {path.suffix for path in paths} == {".svg", ".pdf"}
    assert len({path.stem for path in paths}) == 4
    for path in paths:
        assert path.is_file()
        assert path.stat().st_size > 500
