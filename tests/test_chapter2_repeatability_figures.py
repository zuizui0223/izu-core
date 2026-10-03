import json
from pathlib import Path

from scripts.generate_chapter2_repeatability_figures import build_repeatability_figure3

ROOT=Path(__file__).resolve().parents[1]


def test_repeatability_figure3_regenerates_from_committed_diagnostic():
    payload=build_repeatability_figure3()
    assert payload["status"]=="repeatability_figure3_regenerates_from_exact_source_diagnostic"
    assert payload["mixed_histories_eps0"]==[12,0,1]
    rel=payload["eight_repeat_reliability"]
    assert rel[1] < rel[0] < rel[2]
    split=payload["split_half_history_correlation"]
    assert split[1] < split[0] < split[2]
    hist=payload["history_structured_variance"]
    resid=payload["demographic_residual_variance"]
    assert hist[1] < hist[0] < hist[2]
    assert resid[2] < resid[0] < resid[1]
    assert "not equated with geometric parallelism" in payload["claim_boundary"]

    for relpath in payload["figure_outputs"]:
        p=ROOT/relpath
        assert p.exists() and p.stat().st_size > 1000

    inputs=json.loads((ROOT/"data/results/chapter2_repeatability_figure_inputs_20261003.json").read_text())
    assert inputs==payload
