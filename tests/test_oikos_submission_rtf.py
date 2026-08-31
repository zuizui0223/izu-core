from scripts.render_oikos_submission_rtf import (
    render_manuscript_rtf,
    render_plain_text_rtf,
    render_supporting_information_rtf,
)


def test_main_manuscript_rtf_has_oikos_review_format_controls():
    text = render_manuscript_rtf()
    assert text.startswith("{\\rtf1")
    assert "\\paperw11907" in text
    assert "\\sl480\\slmult1" in text
    assert "\\linemod1" in text
    assert "\\linecont" in text
    assert "fldinst PAGE" in text
    assert "\\page" in text
    lower = text.lower()
    assert "response direction is therefore relational rather than intrinsic" in lower
    assert "supporting information" in lower
    assert "(appendix)" not in lower
    assert "fig. s" not in lower
    assert "chapter 3" not in lower


def test_supporting_information_rtf_preserves_corrected_relational_audit():
    text = render_supporting_information_rtf()
    assert text.startswith("{\\rtf1")
    assert "\\sl480\\slmult1" in text
    lower = text.lower()
    assert "prespecified relational-robustness audit" in lower
    assert "69.34" in text and "80.17" in text
    assert "53/96" in text
    assert "partner arrival/replacement" in lower
    assert "2/25" in text
    assert "cell-level simulation variation" not in lower
    assert "chapter 3" not in lower


def test_plain_text_rtf_escapes_unicode_and_uses_same_submission_spacing():
    text = render_plain_text_rtf("# Example\n\nstate–community × response")
    assert text.startswith("{\\rtf1")
    assert "\\sl480\\slmult1" in text
    assert "\\u8211?" in text
    assert "\\u215?" in text
