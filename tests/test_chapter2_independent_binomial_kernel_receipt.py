"""Original archived alternative-model results and strong inference firewall.

No new model outcomes are generated: only read immutable source execution receipt.
"""
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"data/results/chapter2_independent_binomial_kernel_2048_receipt_20261010.json"


def test_alternative_model_complete_and_distinct_from_model3():
    d=json.loads(RESULT.read_text())
    assert d["status"]=="SOURCE_EXECUTED_FULL_2048_PATHS_ANALYTIC_SIGN_BOUNDARY_INDEPENDENT_KERNEL"
    assert d["n_paths"]==2048
    assert d["n_alternative_model_families"]==1
    assert d["independent_natural_island_systems"]==0
    assert d["input_design_sha256"]=="1b7f00903e494b989cba9aed5722207d57a617c7d57e73dcd6f53a7e96f11575"
    assert len(d["full_H80_outcomes"])==8


def test_analytic_sign_conflict_is_not_stochastic_extinction_confirmation():
    d=json.loads(RESULT.read_text())
    cells={(r["timing"],r["pollen_q"],r["K"]):r
           for r in d["full_H80_outcomes"]}
    primary=cells["prior",.8,8]
    assert primary["heritable_occupied"]==57
    assert primary["expression_frozen_occupied"]==78
    assert primary["delta_heritable_minus_frozen"]==-21/128
    lo,hi=primary["paired_exact95"]
    assert lo<-.05 and hi>0
    assert primary["single_setting_decision"]=="inconclusive"
    for k in (8,48):
        scarcity=cells["prior",.4,k]
        assert scarcity["single_setting_decision"]=="positive"
        assert scarcity["expression_frozen_occupied"]==0
        assert scarcity["paired_exact95"][0]>.05


def test_father_gamete_constraint_and_density_threshold_pinned():
    d=json.loads(RESULT.read_text())
    assert "N=4" in d["analytical_identity"]["sign_boundary_at_abundant_q"]
    assert d["analytical_identity"]["not_novel"].startswith(
        "The automatic transmission advantage")
    assert d["analytical_identity"]["prior_beta"].startswith("2*0.9*")
    for r in d["full_H80_outcomes"]:
        assert r["heritable_occupied"] in range(129)
        assert r["expression_frozen_occupied"] in range(129)
        assert np.isclose(
            r["delta_heritable_minus_frozen"],
            (r["heritable_occupied"]-r["expression_frozen_occupied"])/128,
            atol=1e-12,rtol=0,
        )
        assert r["single_setting_decision"] in {
            "positive","negative","practically_equivalent","inconclusive"}
