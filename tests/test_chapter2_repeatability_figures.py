import json
from pathlib import Path

from scripts.generate_chapter2_repeatability_figures import build_repeatability_figure3

ROOT=Path(__file__).resolve().parents[1]


def test_repeatability_figure3_uses_prospective_validation_for_main_history_signal():
    payload=build_repeatability_figure3()
    assert payload["status"]=="repeatability_figure3_uses_posthoc_discovery_and_prospective_new_seed_validation"
    assert payload["strong_success"] is True

    assert payload["discovery_mixed_histories_eps0"]==[12,0,1]
    assert payload["validation_mixed_histories_eps0"]==[23,1,4]

    corr=payload["discovery_validation_history_correlation"]
    assert corr[1] < corr[0] < corr[2]
    assert abs(corr[0]-0.7321619738226453) < 1e-12
    assert abs(corr[1]-0.1654626963685096) < 1e-12
    assert abs(corr[2]-0.91832741451686) < 1e-12

    hist=payload["validation_history_structured_variance"]
    resid=payload["validation_demographic_residual_variance"]
    assert hist[1] < hist[0] < hist[2]
    assert resid[2] < resid[0] < resid[1]

    paired=payload["paired_validation_bootstrap"]
    assert paired["large_capacity_minus_natural"]["bootstrap95"][0] > 0
    assert paired["visitor_pooled_minus_natural"]["bootstrap95"][1] < 0

    assert "post-hoc discovery" in payload["claim_boundary"]
    assert "prospectively frozen new demographic seeds" in payload["claim_boundary"]
    assert "not environmental-history or natural-island validation" in payload["claim_boundary"]

    for relpath in payload["figure_outputs"]:
        p=ROOT/relpath
        assert p.exists() and p.stat().st_size > 1000

    inputs=json.loads((ROOT/"data/results/chapter2_repeatability_figure_inputs_20261003.json").read_text())
    assert inputs==payload
