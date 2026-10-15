"""Technical guards for exact historical t0→200 Model 3 reproduction replay."""
import numpy as np
import pytest

from scripts.replay_chapter2_far_original_0_200_20261015 import (
    annual_source_replay, original_streams, source_protocol, END,
)
from scripts.run_chapter2_assurance_generality import load_design, DEFAULT_DESIGN


def test_source_contract_frozen_and_shard_count():
    p, original, design=source_protocol()
    assert p["original_demographic_seed"]==26111601
    assert p["expected_source_case_replays"]==512
    assert p["expected_original_source_updates"]==102400
    assert END==200


def test_original_full_history_stream_is_reproducible():
    a=original_streams(26110601)
    b=original_streams(26110601)
    assert a["segregation"].integers(0,2)==b["segregation"].integers(0,2)
    assert a["parents"].random()==b["parents"].random()


@pytest.mark.parametrize("mode,t200_I",[
    ("fixed",0.22926080271881497),
    ("evolving",0.5368553594048959),
])
def test_first_original_history_t200_source_trait_and_accounting(mode,t200_I):
    d=load_design(DEFAULT_DESIGN)
    a=annual_source_replay(d,"delayed_control",26110601,mode)
    assert np.isclose(a["mean_I"][-1],t200_I,rtol=0,atol=1e-10)
    assert a["mean_I"].shape==(201,)
    assert a["parentage"].shape==(200,48,3)
    assert np.all(a["N"]>0)
    assert np.allclose(a["realized_delta_I"],
                       a["survivor_sampling_I"]+
                       a["weighted_parental_Price_I"]+
                       a["recruit_transmission_residual_I"],
                       rtol=0,atol=1e-12)
    assert np.isclose(np.sum(a["realized_delta_I"]),
                      a["mean_I"][-1]-a["mean_I"][0],rtol=0,atol=1e-12)
    if mode=="fixed":
        assert np.all(a["mean_A_expressed"]==.5)
