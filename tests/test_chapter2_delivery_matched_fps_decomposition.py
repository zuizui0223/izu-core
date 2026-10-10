"""Reproducible source-only paternal/maternal/self decomposition checks."""
import numpy as np
import pytest

from scripts.audit_chapter2_delivery_matched_fps_decomposition import (
    STATUS, contract, focal_contributions, run_all,
)
from scripts.audit_chapter2_visitor_export_normalized_sensitivity import (
    parent, visitor, REFERENCE,
)
from scripts.audit_chapter2_visitor_richness_composition_factorial import (
    config as baseline_config,
)


@pytest.fixture(scope="module")
def result():
    return run_all()


def test_contract_preserves_prior_matched_receipt_grid():
    d=contract()
    assert d["registered_blocks"]==36
    assert d["registered_arms"]==72
    assert d["registered_focals"]==576
    assert d["classification_deadband"]==.02
    assert d["grid"]["n_parent"]==8


def test_source_sex_components_add_to_focal_gradient():
    s=parent("mixed_diploid",.2)
    cfg=baseline_config("fixed")
    o=focal_contributions(s,visitor(REFERENCE,.18,1.),cfg)
    assert len(o["focals"])==8
    for f in o["focals"]:
        np.testing.assert_allclose(
            f["beta_total"],
            f["beta_F"]+f["beta_P"]+f["beta_S"],
            rtol=0,atol=1e-10,
        )
    np.testing.assert_allclose(o["F_total"],o["P_total"],atol=1e-11)


def test_full_36_blocks_all_source_accounting_retained(result):
    assert result["status"]==STATUS
    assert result["n_fixtures"]==36
    assert result["n_arms"]==72
    assert result["n_focal_gradients"]==576
    assert result["max_abs_matching_error"]<1e-8
    assert result["natural_systems"]==result["new_ecological_histories"]==0
    for c in result["cases"]:
        d=c["contrast"]
        assert len(d["per_focal"])==8
        assert 0 <= d["father_share_L1"] <= 2+1e-12
        np.testing.assert_allclose(d["delta_P"],d["delta_F"],
                                   rtol=0,atol=1e-10)
        np.testing.assert_allclose(d["delta_seed"],d["delta_F"]+d["delta_S"],
                                   rtol=0,atol=1e-10)
        np.testing.assert_allclose(
           d["delta_beta_median"],
           c["delivery_matched"]["beta_median"]-c["reference"]["beta_median"],
           rtol=0,atol=1e-12,
        )
        for x in d["per_focal"]:
            np.testing.assert_allclose(
                x["delta_beta_total"],
                x["delta_beta_F"]+x["delta_beta_P"]+x["delta_beta_S"],
                rtol=0,atol=1e-10,
            )


def test_clonal_fathers_exchangeable_even_when_visitor_optima_shift(result):
    clone=[c for c in result["cases"] if c["genetic"]=="monomorphic"]
    assert len(clone)==18
    assert max(abs(c["contrast"]["delta_seed"]) for c in clone)<1e-7
    assert max(abs(c["contrast"]["father_share_L1"]) for c in clone)<1e-10


def test_anchored_previous_mixed_and_clonal_gradients(result):
    for genotype,old_beta,old_gamma in (
        ("monomorphic",-.063173669540878,.15822876051396761),
        ("mixed_diploid",-.06868910508269488,.14050823583708905),
    ):
        x=[c for c in result["cases"] if c["genetic"]==genotype
           and c["matching"]==.2 and c["breadth"]==.18
           and c["effectiveness"]==1.]
        assert len(x)==1
        np.testing.assert_allclose(
            [x[0]["reference"]["beta_median"],
             x[0]["reference"]["gamma_seed"]],
            [old_beta,old_gamma],rtol=1e-9,atol=1e-9)
