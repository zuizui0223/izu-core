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
    assert "conditional island responses: from functional matching to finite-population evolutionary realization" in lower
    assert "fixed-state reproductive assay" in lower
    assert "deterministic genotype-density counterpart" in lower
    assert "finite-population abm" in lower
    assert "2.3768" in text and "0.1891" in text
    assert "annual response-blind richness matching" in lower
    assert "68/128" in text
    assert "pooling eight independent visitor histories" in lower
    assert "increasing plant capacity from 48 to 192" in lower
    assert "41.5%" in text
    assert "real islands occupy different stages of the same response architecture" in lower
    assert "all eight shared oshima-to-post targets" in lower
    assert "same-direction propagation case" in lower
    assert "counterdirectional case" in lower
    assert "21/25" in text and "2/25" in text and "0/25" in text
    assert "figure 1. one model 3, three nested levels" in lower
    assert "figure 4. real-island layer confrontation and empirical claim ceiling" in lower
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
    assert "# Appendix S18A. Unified Model 3 projection onto real-island evidence" in markdown
    assert "# Appendix S18B. Prospective Model 3 isolation bridge" in markdown
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
    assert "unified model 3 projection onto real-island evidence" in lower
    assert "prospective model 3 isolation bridge" in lower
    assert "68/128" in text and "41.5%" in text
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
