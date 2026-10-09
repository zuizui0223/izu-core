"""Check manuscript routing against immutable scientific result JSONs.

No simulations, no bootstrap recomputation, and no new inference in CI.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
LATEST=ROOT/"results/chapter2/k_fixedB48_independent_primary_20261009.json"
PREVIOUS=ROOT/"results/chapter2/kb_independent_full_readout_20261009.json"
EARLIER=ROOT/"results/chapter2/orthogonal_capacity_full_readout_20261009.json"
POSITION=ROOT/"docs/CHAPTER2_PERSISTENCE_CAPACITY_COMPANION_POSITION_20261009.md"
ROUTE=ROOT/"docs/CHAPTER2_JOURNAL_ROUTE_20261006.md"
MANUSCRIPT=ROOT/"docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md"


def test_latest_capacity_estimate_supports_only_its_frozen_model_primary():
    d=json.loads(LATEST.read_text(encoding="utf-8"))
    assert d["primary_verdict"]=="supported_controlled_demographic_K_moderation_at_fixed_B48"
    assert d["original_predeclared_primary"]=="tau(K8,B48)-tau(K48,B48)"
    assert (d["n_independent_visitor_histories"],
            d["n_t400_sources"],d["n_future_cells"])==(64,2048,114688)
    assert d["paired_bootstrap"]=={
        "unit":"visitor_history","draws":9999,"seed":2026100967
    }
    primary=d["contrasts"]["primary_K_at_fixed_B48"]
    assert abs(primary["mean"]-0.007745713876893593)<1e-14
    assert primary["bootstrap95"]==[
        0.002497158065469939,0.013015478808429596
    ]
    assert primary["bootstrap95"][0]>0 and primary["mean"]>=0.005


def test_old_inconclusive_primaries_are_not_promoted():
    old=json.loads(PREVIOUS.read_text(encoding="utf-8"))
    first=json.loads(EARLIER.read_text(encoding="utf-8"))
    assert old["primary_verdict"]=="inconclusive"
    assert old["original_predeclared_primary"]=="tau(K8,B8)-tau(K8,B48)"
    assert abs(old["contrasts"]["primary_B_at_K8"]["mean"]-(-0.0017526045561689334))<1e-14
    assert first["primary_decision"]=="inconclusive"
    assert abs(first["inference"]["contrasts"][
        "primary_capacity_conditional_fixed_eight"]["mean"]
        -0.0018484189036193578)<1e-14


def test_manuscript_remains_flower_investment_first_and_companion_is_bounded():
    manuscript=MANUSCRIPT.read_text(encoding="utf-8")
    route=ROUTE.read_text(encoding="utf-8")
    companion=POSITION.read_text(encoding="utf-8")
    assert manuscript.startswith(
        "# Reproductive assurance compresses floral-investment divergence"
    )
    assert "Allowing assurance to evolve consistently reduced those contrasts" in manuscript
    assert "Primary target: Ecology Letters" in route
    assert "separate" in route.lower() and "0.0077457139" in route
    assert "not" in companion.lower()
    for required in ("inconclusive","114,688","64 visitor-history clusters",
                     "not a natural", "not replicated across independent model families"):
        assert required.lower() in companion.lower()
