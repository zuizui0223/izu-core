from scripts.render_oikos_submission_rtf import (
    render_manuscript_rtf,
    render_plain_text_rtf,
    render_supporting_information_markdown,
    render_supporting_information_rtf,
)


def test_main_manuscript_rtf_has_oikos_review_format_controls_and_three_result_reframe():
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
    assert "in island plant–pollinator systems" not in lower.split("introduction", 1)[0]
    assert "result 1" in lower and "result 2" in lower and "result 3" in lower
    assert "real island systems undergo compositional reorganization beyond richness loss" in lower
    assert "pollinator assemblage turnover was 0.9796" in lower
    assert "matched-plant turnover was 0.6817" in lower
    assert "functional community structure in izu" in lower
    assert "51" in text and "65/96" in text
    assert "all six prespecified matching seeds" in lower
    assert "70/96" in text and "65.61%" in text
    assert "equalizing the baseline mainland" in lower
    assert "does not make the two scenarios identical" in lower
    assert "figure 1. three-result inference chain" in lower
    assert "figure 4. result 2 exposure to result 3 biological consequence" in lower
    assert "figure 1. four-act breadth-to-depth inference funnel" not in lower
    assert "figure 4. from outcome-rich literature to izu mechanistic resolution" not in lower
    assert "richness reduction is not necessary for mixed response geometry" not in lower
    assert "response direction is therefore relational rather than intrinsic" not in lower
    assert "supporting information" in lower
    assert "(appendix)" not in lower
    assert "fig. s" not in lower
    assert "chapter 3" not in lower


def test_supporting_information_rtf_preserves_relational_world_izu_and_realized_richness_material():
    markdown = render_supporting_information_markdown()
    assert "# Appendix S17. Geography-first saturation and final world synthesis" in markdown
    assert "# Appendix S18. Contemporary Izu functional-chain sensitivity" in markdown
    assert "# Appendix S19. Exact realized-richness matching hard control" in markdown
    assert "# Supporting Tables" in markdown
    assert "## Table S1." in markdown
    assert "## Table S8." in markdown
    assert "# Supporting Table S9. Exact realized-richness matching sensitivity" in markdown
    assert "# Chapter 2 Supporting Tables" not in markdown
    assert "Equal turnover rates: mixed count / state × community non-additivity" in markdown
    assert "70/96 / 65.61%" in markdown

    text = render_supporting_information_rtf()
    assert text.startswith("{\\rtf1")
    assert "\\sl480\\slmult1" in text
    lower = text.lower()
    assert "prespecified relational-robustness audit" in lower
    assert "geography-first saturation and final world synthesis" in lower
    assert "contemporary izu functional-chain sensitivity" in lower
    assert "exact realized-richness matching hard control" in lower
    assert "supporting table s9. exact realized-richness matching sensitivity" in lower
    assert "51/96 to 65/96" in text
    assert "42.72" in text and "48.51" in text
    assert "mean regime is richness-sensitive" in lower
    assert "69.34" in text and "80.17" in text
    assert "53/96" in text
    assert "70/96" in text and "65.61%" in text
    assert "partner arrival/replacement" in lower
    assert "2/25" in text
    assert "+1.9426" in text and "+2.0590" in text
    assert "+0.0353" in text
    assert "cell-level simulation variation" not in lower
    assert "chapter 3" not in lower


def test_plain_text_rtf_escapes_unicode_and_uses_same_submission_spacing():
    text = render_plain_text_rtf("# Example\n\nstate–community × response")
    assert text.startswith("{\\rtf1")
    assert "\\sl480\\slmult1" in text
    assert "\\u8211?" in text
    assert "\\u215?" in text
