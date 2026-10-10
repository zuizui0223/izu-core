"""Conditional demographic K48 ceiling is not a future extinction result."""
import json
from pathlib import Path
import numpy as np
from scipy.stats import poisson
import pytest
from scripts.audit_chapter2_original_evolved_demographic_ceiling import (
    poisson_capped_moments, audit,
)

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"data/results/chapter2_original_evolved_K48_ceiling_receipt_20261010.json"


def test_poisson_cap_formula_matches_truncated_exact_sum():
    for mu in (0.,.1,5.,12.,48.,100.,200.):
        d=poisson_capped_moments(mu,48)
        expected=sum(n*poisson.pmf(n,mu) for n in range(48))
        expected+=48*poisson.sf(47,mu)
        np.testing.assert_allclose(
            d["expected_next_census"], expected,atol=1e-11,rtol=0)
        np.testing.assert_allclose(
            d["probability_below_capacity"],poisson.cdf(47,mu),atol=0,rtol=0)
        assert 0<=d["expected_next_census"]<=48
    with pytest.raises(ValueError):
        poisson_capped_moments(-1)


def test_original_near_source_capacity_ceiling_remains_a_bounded_null():
    a=json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert a["status"]=="SOURCE_REPLAY_EXACT_POSTOUTCOME_NO_LONGRUN_DEMOGRAPHY"
    assert a["n_history_blocks"]==64
    assert a["n_nested_repeats"]==1
    assert a["n_new_histories"]==0
    assert len(a["near_t400"])==4
    assert a["original_result_json_sha256"]==(
        "7eef0707dd3ec7aac1b56e50e64238a087f7269c8777a9f2e9ba79bd18cf48ff")
    for x in a["near_t400"]:
        assert x["K"]==48
        assert x["min_viable_mu_either_branch"]>48
        assert x["max_probability_below_K"]<.006
        assert abs(x["mean_expected_census_delta"])<.00025
    assert "ONE-YEAR" in a["claim_ceiling"]


def test_raw_replay_requires_sha_original_json(tmp_path):
    bad=tmp_path/"bad.json"
    bad.write_text('{"n_reproduced_state_ledgers":1024}')
    with pytest.raises(ValueError):
        audit(bad)
