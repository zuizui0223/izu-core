import json
from pathlib import Path

from scripts.generate_chapter2_repeatability_figures import build_repeatability_figure3

ROOT=Path(__file__).resolve().parents[1]


def test_repeatability_figure3_uses_independent_visitor_history_validation():
    payload=build_repeatability_figure3()
    assert payload["status"]=="repeatability_figure3_uses_prospectively_frozen_independent_visitor_history_validation"
    assert payload["strong_success"] is True
    assert payload["visitor_history_seed_range"]==[75001,75128]

    assert payload["mixed_histories_eps0"]==[19,2,1]

    rel=payload["four_repeat_history_reliability"]
    assert rel[1] < rel[0] < rel[2]
    assert abs(rel[0]-0.4169402438063488) < 1e-12
    assert abs(rel[1]-0.15403351483184766) < 1e-12
    assert abs(rel[2]-0.7217688849932009) < 1e-12

    paired=payload["paired_bootstrap"]
    assert paired["large_capacity_minus_natural"]["bootstrap95"][0] > 0
    assert paired["visitor_pooled_minus_natural"]["bootstrap95"][1] < 0

    hist=payload["history_structured_variance"]
    resid=payload["demographic_residual_variance"]
    assert hist[1] < hist[0] < hist[2]
    assert resid[2] < resid[0] < resid[1]

    assert "prospectively frozen new synthetic visitor histories" in payload["claim_boundary"]
    assert "not to a different ecological process or natural islands" in payload["claim_boundary"]

    for relpath in payload["figure_outputs"]:
        p=ROOT/relpath
        assert p.exists() and p.stat().st_size > 1000

    inputs=json.loads((ROOT/"data/results/chapter2_repeatability_figure_inputs_20261003.json").read_text())
    assert inputs==payload
