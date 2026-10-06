from scripts.render_chapter2_submission_manuscript import render_manuscript


def test_submission_renderer_keeps_confirmed_process_spine():
    text = render_manuscript()
    lower = " ".join(text.lower().split())

    assert text.startswith(
        "# How island isolation generates floral change: selection conditions, evolutionary sequence and finite realization"
    )
    assert "51/64" in text
    assert "0.6875–0.8906" in text
    assert "assurance evolution is not required for investment decline" in lower
    assert "visitor limitation lowers the return on attraction before plant traits evolve" in lower
    assert "lower pollen deficit does not necessarily mean greater viable reproduction" in lower
    assert "prior selfing with positive mutation" in lower


def test_submission_renderer_moves_supporting_diagnostics_out_of_main_text():
    text = render_manuscript()
    forbidden = [
        "## Continuous replenishment extension: completed finite-population gradient",
        "## Prospective isolation-bridge controls",
        "## Current flowers do not uniquely determine inherited response",
        "## Isolation can strengthen existing selection rather than initiate it",
        "## Reciprocal coupling of selection on capacity and investment",
        "## Reproductive assumptions delimit reciprocal selection",
        "## Genetic diversity, fitness and model scope",
        "## Realized evolution across continuous replenishment",
        "## Numerical sensitivity and branch-identifiability limits",
        "## Independent connection to Q1",
    ]
    for heading in forbidden:
        assert heading not in text


def test_submission_has_three_main_figures_and_genetic_realization_is_supporting():
    text = render_manuscript()
    assert "**Main Figure 1." in text
    assert "**Main Figure 2." in text
    assert "**Main Figure 3." in text
    assert "**Main Figure 4." not in text
    assert "**Supporting Figure S1. Finite genetic realization" in text
