from pathlib import Path

import pytest

from scripts.render_island_ecology_submission_manuscript import (
    FINAL_TITLE,
    FORBIDDEN_SUBMISSION_TOKENS,
    SOURCE,
    render_submission_manuscript,
    render_to_path,
)


def test_renderer_removes_internal_thesis_routing_and_preserves_four_act_science():
    text = render_submission_manuscript()
    lower = text.lower()
    assert text.startswith(f"# {FINAL_TITLE}\n")
    for token in FORBIDDEN_SUBMISSION_TOKENS:
        assert token.lower() not in lower
    assert "dissertation" not in lower
    assert "the paper therefore proceeds through four inferential acts" in lower
    assert "**theory:**" in lower
    assert "**global confrontation:**" in lower
    assert "**identifiability:**" in lower
    assert "**izu continuity-system zoom:**" in lower
    assert "## theory — possibility:" in lower
    assert "## theory — relational branch identity:" in lower
    assert "## global confrontation:" in lower
    assert "## identifiability:" in lower
    assert "## izu mechanistic zoom:" in lower
    assert "five linked questions" not in lower
    assert "## reality:" not in lower
    assert "## resolution:" not in lower
    assert "response direction is therefore relational rather than intrinsic" in lower
    assert "53/96" in text
    assert "partner arrival/replacement" in lower
    assert "null-corrected matching" in lower
    assert "measurement continuity across the bottleneck" in lower
    assert "not proximity, logistical convenience, representativeness or positive agreement" in lower
    assert "prespecified oshima-source bridge was unsupported (supporting information)" in lower
    assert "(appendix)" not in lower
    assert "fig. s" not in lower
    assert "figure s" not in lower
    assert "appendix s" not in lower
    assert "cell-level simulation variation" not in lower
    assert "Izu Islands" in text


def test_renderer_preserves_descriptive_breadth_and_selected_world_roles_without_reopening_formal_n():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "42 research entries across 37 exact geographic labels" in lower
    assert "affre & thompson, 1997" in lower
    assert "feinsinger et al., 1982" in lower
    assert "ægisdóttir & thórhallsdóttir, 2006" in lower
    assert "philipp & adsersen, 2014" in lower
    assert "andrews et al., 2022" in lower
    assert "gutiérrez-flores et al., 2018" in lower
    assert "did not reopen the frozen 25-entry formal denominator" in lower
    assert "formal external prediction remains `not_evaluable`" in lower


def test_renderer_embeds_active_reference_list_and_excludes_ledger_audit_metadata():
    text = render_submission_manuscript()
    lower = text.lower()
    assert "## references" in lower
    assert "inoue, k. & amano, m. (1986)" in lower
    assert "hiraiwa, m.k. & ushimaru, a. (2024)" in lower
    assert "andrews, c.e., anderson, s.h." in lower
    assert "philipp, m. & adsersen, h. (2014)" in lower
    assert "hygiene decisions" not in lower
    assert "world-saturation synthesis source boundary" not in lower
    assert "value-selected breadth source boundary" not in lower
    assert "docs/" not in lower
    assert "data/design/" not in lower


def test_renderer_writes_clean_submission_file(tmp_path: Path):
    output = tmp_path / "manuscript.md"
    assert render_to_path(output) == output
    text = output.read_text(encoding="utf-8")
    lower = text.lower()
    assert text.startswith(f"# {FINAL_TITLE}\n")
    assert "At the dissertation scale" not in text
    assert "chapter 1" not in lower
    assert "chapter 2" not in lower
    assert "chapter 3" not in lower
    assert "four inferential acts" in lower
    assert "measurement continuity" in lower


def test_renderer_fails_closed_if_source_header_contract_changes(tmp_path: Path):
    broken = tmp_path / "broken.md"
    source = SOURCE.read_text(encoding="utf-8")
    original = "**Status:** active Chapter 2 scientific manuscript — world-saturation / Izu-continuity synthesis; submission metadata still fail-closed"
    assert original in source
    broken.write_text(source.replace(original, "**Status:** changed", 1), encoding="utf-8")
    with pytest.raises(ValueError, match="header changed"):
        render_submission_manuscript(broken)


def test_renderer_fails_closed_if_introduction_funnel_contract_changes(tmp_path: Path):
    broken = tmp_path / "broken.md"
    source = SOURCE.read_text(encoding="utf-8")
    broken.write_text(source.replace("The paper follows five linked questions.", "The paper follows several questions.", 1), encoding="utf-8")
    with pytest.raises(ValueError, match="five-question Introduction funnel changed"):
        render_submission_manuscript(broken)


def test_renderer_fails_closed_if_izu_continuity_bridge_contract_changes(tmp_path: Path):
    broken = tmp_path / "broken.md"
    source = SOURCE.read_text(encoding="utf-8")
    original = "The move from breadth to Izu is therefore an inferential decision, not a geographic convenience."
    assert original in source
    broken.write_text(source.replace(original, "The move to Izu is convenient.", 1), encoding="utf-8")
    with pytest.raises(ValueError, match="Izu continuity Introduction bridge changed"):
        render_submission_manuscript(broken)


def test_renderer_fails_closed_if_focal_selection_section_contract_changes(tmp_path: Path):
    broken = tmp_path / "broken.md"
    source = SOURCE.read_text(encoding="utf-8")
    broken.write_text(source.replace("## Focal-system selection after world saturation", "## Focal selection", 1), encoding="utf-8")
    with pytest.raises(ValueError, match="focal-system selection section changed"):
        render_submission_manuscript(broken)


def test_renderer_fails_closed_on_new_specific_supporting_information_reference(tmp_path: Path):
    broken = tmp_path / "broken.md"
    source = SOURCE.read_text(encoding="utf-8")
    source = source.replace(
        "The prespecified Oshima-source bridge was unsupported (Appendix),",
        "The prespecified Oshima-source bridge was unsupported (Appendix), see Fig. S9,",
        1,
    )
    broken.write_text(source, encoding="utf-8")
    with pytest.raises(ValueError, match="specific Supporting information reference"):
        render_submission_manuscript(broken)
