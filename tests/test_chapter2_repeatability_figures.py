import json
from pathlib import Path

from scripts.generate_chapter2_repeatability_figures import build_repeatability_figure3

ROOT = Path(__file__).resolve().parents[1]


def test_repeatability_figure3_regenerates_from_discovery_and_prospective_validation():
    payload = build_repeatability_figure3()
    assert payload["status"] == "repeatability_figure3_regenerates_from_discovery_and_prospective_validation"
    assert payload["discovery_mixed_histories_eps0"] == [12, 0, 1]
    assert payload["validation_mixed_histories_eps0"] == [23, 1, 4]

    corr = payload["discovery_validation_history_correlation"]
    assert corr[1] < corr[0] < corr[2]
    assert corr[2] > 0.9
    assert corr[1] < 0.2

    hist = payload["validation_history_structured_variance"]
    resid = payload["validation_demographic_residual_variance"]
    assert hist[1] < hist[0] < hist[2]
    assert resid[2] < resid[0] < resid[1]

    assert payload["large_minus_natural_correlation_ci95"][0] > 0
    assert payload["pooled_minus_natural_correlation_ci95"][1] < 0
    assert payload["validation_strong_success"] is True
    assert "not independent environmental-history" in payload["claim_boundary"]

    for relpath in payload["figure_outputs"]:
        p = ROOT / relpath
        assert p.exists() and p.stat().st_size > 1000

    inputs = json.loads(
        (ROOT / "data/results/chapter2_repeatability_figure_inputs_20261003.json").read_text()
    )
    assert inputs == payload
