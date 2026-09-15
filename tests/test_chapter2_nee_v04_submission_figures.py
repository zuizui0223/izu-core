from pathlib import Path

from scripts.render_chapter2_nee_v04_submission_figures import render_all


def test_nee_v04_submission_figures_render_from_frozen_results(tmp_path: Path) -> None:
    paths = render_all(tmp_path)
    assert len(paths) == 8
    assert len([path for path in paths if path.suffix == ".pdf"]) == 4
    assert len([path for path in paths if path.suffix == ".svg"]) == 4
    assert all(path.is_file() and path.stat().st_size > 0 for path in paths)

    figure4_svg = tmp_path / "figure4_measurement_ceiling_and_transport.svg"
    text = figure4_svg.read_text(encoding="utf-8")
    for token in ("21/25", "2/25", "0/25", "42-system regime map estimates context"):
        assert token in text
