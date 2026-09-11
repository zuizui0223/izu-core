from scripts.render_oikos_submission_rtf import (
    render_manuscript_rtf,
    render_plain_text_rtf,
    render_supporting_information_markdown,
    render_supporting_information_rtf,
)


def test_main_manuscript_rtf_has_oikos_review_format_controls_and_mechanism_mainline():
    text = render_manuscript_rtf()
    assert text.startswith("{\\rtf1")
    assert "\\paperw11907" in text
    assert "\\sl480\\slmult1" in text
    assert "\\linemod1" in text
    assert "\\linecont" in text
    assert "fldinst PAGE" in text
    assert "\\page" in text
    lower = text.lower()
    assert "response geometry under community reorganization: richness-sensitive regimes and state-dependent branching" in lower
    assert "conditional response geometry" in lower
    assert "realized richness differences therefore help position the ensemble mean regime" in lower
    assert "ordering of response determinants is itself regime dependent" in lower
    assert "51" in text and "65/96" in text
    assert "all six prespecified matching seeds" in lower
    assert "70/96" in text and "65.61%" in text
    assert "55.84%" in text and "12.72%" in text
    assert "deterministic mean-field kernel contrast was all-positive" in lower
    assert "figure 1. conditional-response architecture and scale-dependent determinant hierarchy" in lower
    assert "figure 4. empirical claim boundary and future validation" in lower
    assert "figure 1. three-result inference chain" not in lower
    assert "result 1—mechanistic prediction" not in lower
    assert "result 2—real-world exposure" not in lower
    assert "result 3—biological consequence" not in lower
    assert "(appendix)" not in lower
    assert "fig. s" not in lower


def test_supporting_information_rtf_preserves_relational_world_izu_and_generality_material():
    markdown = render_supporting_information_markdown()
    assert "# Appendix S17. Geography-first saturation and final world synthesis" in markdown
    assert "# Appendix S18. Contemporary Izu functional-chain sensitivity" in markdown
    assert "# Appendix S19. Exact realized-richness matching hard control" in markdown
    assert "# Appendix S20. Finite-community system-size audit" in markdown
    assert "# Appendix S21. Exact finite-community moments and Gaussian mean-field limit" in markdown
    assert "# Appendix S22. Regime-dependent response hierarchy under active plant adjustment" in markdown
    assert "# Supporting Tables" in markdown
    assert "# Supporting Table S9. Exact realized-richness matching sensitivity" in markdown
    assert "70/96 / 65.61%" in markdown
    assert "Active-adjustment system-size rank crossover" in markdown
    assert "55.84%/12.72%" in markdown

    text = render_supporting_information_rtf()
    assert text.startswith("{\\rtf1")
    assert "\\sl480\\slmult1" in text
    lower = text.lower()
    assert "exact realized-richness matching hard control" in lower
    assert "finite-community system-size audit" in lower
    assert "gaussian mean-field limit" in lower
    assert "regime-dependent response hierarchy" in lower
    assert "70/96" in text and "65.61%" in text
    assert "55.84%" in text and "72.98%" in text
    assert "partner arrival/replacement" in lower
    assert "2/25" in text
    assert "cell-level simulation variation" not in lower


def test_plain_text_rtf_escapes_unicode_and_uses_same_submission_spacing():
    text = render_plain_text_rtf("# Example\n\nstate–community × response")
    assert text.startswith("{\\rtf1")
    assert "\\sl480\\slmult1" in text
    assert "\\u8211?" in text
    assert "\\u215?" in text
