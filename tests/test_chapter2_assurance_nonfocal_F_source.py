"""One-state source operator checks, NOT #411 history-level mediation."""
import numpy as np

from scripts.audit_chapter2_assurance_nonfocal_F_source import assay, SETTINGS


def test_direct_nonfocal_F_is_zero_without_assurance_pollen_discount():
    out = assay()
    assert out["n_new_visitor_histories"] == out["n_natural_systems"] == 0
    assert out["no_dynamic_evolution_test"]
    rows = {r["setting"]:r for r in out["rows"]}
    assert set(rows) == set(SETTINGS)
    for key in ("delayed_control", "prior_selfing", "assurance_cost"):
        assert rows[key]["pollen_discount"] == 0.
        np.testing.assert_allclose(
            rows[key]["direct_assurance_delta_at_fixed_investment"],
            0., rtol=0., atol=1e-12,
        )


def test_pollen_discount_introduces_direct_negative_service_externality():
    row = {r["setting"]: r for r in assay()["rows"]}["pollen_discount"]
    assert row["pollen_discount"] > 0.
    assert row["direct_assurance_delta_at_fixed_investment"] < 0.


def test_finite_decomposition_is_accounting_not_history_mediation():
    for row in assay()["rows"]:
        np.testing.assert_allclose(
            row["combined_finite_contrast"],
            row["direct_assurance_delta_at_fixed_investment"] +
            row["investment_response_delta_at_high_assurance"],
            atol=1e-12, rtol=0.,
        )
        # With the explicitly imposed investment decline in this *single*
        # resident fixture, the nonfocal mating service is predicted to fall.
        assert row["investment_response_delta_at_high_assurance"] < 0
