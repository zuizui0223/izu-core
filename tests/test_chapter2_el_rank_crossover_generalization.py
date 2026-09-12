from scripts.audit_chapter2_el_rank_crossover_generalization import build


def test_generic_rank_crossover_sufficient_condition_and_countercondition():
    result = build()
    checks = result["checks"]
    assert all(checks.values())

    derived = result["derived_quantities"]
    assert derived["independent_exact_crossover_requires_k_greater_than"] == 4.0
    assert derived["correlation_floor_prevents_asymptotic_crossover_when_rho_at_least"] == 0.25

    independent = result["summaries"]["0.0"]
    assert independent["first_k_starting_exceeds_community"] == 8

    high_corr = result["summaries"]["0.4"]
    assert high_corr["first_k_starting_exceeds_community"] is None


def test_interaction_persists_at_finite_k_without_becoming_asymptotic_constant():
    result = build()
    independent_rows = result["summaries"]["0.0"]["rows"]
    assert all(row["interaction"] > 0 for row in independent_rows)
    assert independent_rows[-1]["interaction"] < independent_rows[0]["interaction"]
