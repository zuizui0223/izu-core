import math

import pytest

from channel_id.causal_admissibility import (
    CandidateObservation,
    ObservationOutcome,
    causal_replaceability_cost,
    expected_observation_value,
    summarise_admissible_region,
)
from channel_id.channel_identifiability import (
    VitalRateState,
    construct_net_only_symmetry,
    construct_proxy_calibration_ambiguity,
    identify_relative_change_from_stable_proxy,
    reconstruct_from_net_and_factor,
)
from channel_id.evidence_projection import (
    ProjectionStatus,
    projection_for,
    validate_projection_ledger,
)


def test_n1_net_only_symmetry_constructs_same_w_from_different_channels() -> None:
    baseline = VitalRateState(
        trait=(0.0, 1.0, 2.0),
        local=(2.0, 3.0, 4.0),
        establishment=(0.8, 0.7, 0.6),
    )
    result = construct_net_only_symmetry(baseline, (0.9, 0.7, 0.5))

    assert result.net_equal
    assert result.local_change.local != result.establishment_change.local
    assert result.local_change.establishment != result.establishment_change.establishment
    assert result.local_change.net == pytest.approx(result.establishment_change.net)


def test_n2_w_plus_one_factor_recovers_the_other() -> None:
    state = reconstruct_from_net_and_factor(
        trait=(0.0, 1.0),
        net=(1.2, 2.0),
        observed_factor=(2.0, 4.0),
        factor="local",
    )
    assert state.establishment == pytest.approx((0.6, 0.5))
    assert state.net == pytest.approx((1.2, 2.0))


def test_n3_stable_proxy_identifies_relative_channel_change() -> None:
    result = identify_relative_change_from_stable_proxy(
        net_before=(1.0, 1.0),
        net_after=(0.5, 0.75),
        proxy_before=(10.0, 20.0),
        proxy_after=(5.0, 15.0),
        proxy_channel="local",
    )
    assert result.local_ratio == pytest.approx((0.5, 0.75))
    assert result.establishment_ratio == pytest.approx((1.0, 1.0))
    assert result.conclusion == "local_only"


def test_n4_calibration_drift_restores_nonidentifiability() -> None:
    result = construct_proxy_calibration_ambiguity(
        net_before=(1.0, 1.0),
        net_after=(0.5, 0.75),
        proxy_before=(10.0, 20.0),
        proxy_after=(5.0, 15.0),
        baseline_calibration=(2.0, 2.0),
        calibration_shift=(0.5, 2.0),
    )
    assert result.same_observed_data
    assert result.stable_calibration.local_ratio != pytest.approx(
        result.drifting_calibration.local_ratio
    )


def test_zero_boundary_is_rejected_instead_of_divided_through() -> None:
    with pytest.raises(ValueError, match="strictly positive"):
        reconstruct_from_net_and_factor(
            trait=(0.0, 1.0),
            net=(1.0, 0.0),
            observed_factor=(1.0, 1.0),
            factor="local",
        )


def test_admissible_region_keeps_competing_explanations_visible() -> None:
    rows = [
        {"pollination": True, "history": False},
        {"pollination": True, "history": False},
        {"pollination": False, "history": True},
        {"pollination": False, "history": True},
    ]
    summary = summarise_admissible_region(rows, ("pollination", "history"))

    assert summary.n_accepted == 4
    assert summary.degeneracy_bits == pytest.approx(1.0)
    assert summary.resolvability == pytest.approx(0.5)
    assert len(summary.explanation_mass) == 2
    assert causal_replaceability_cost(rows, "pollination") == pytest.approx(1.0)
    assert causal_replaceability_cost(rows, "history") == pytest.approx(1.0)


def test_next_observation_can_rank_a_discriminating_measurement() -> None:
    rows = [
        {"pollination": True, "history": False, "marker": "P"},
        {"pollination": True, "history": False, "marker": "P"},
        {"pollination": False, "history": True, "marker": "H"},
        {"pollination": False, "history": True, "marker": "H"},
    ]
    candidate = CandidateObservation(
        name="direct_channel_measurement",
        cost=2.0,
        outcomes=(
            ObservationOutcome("P", 0.5, lambda row: row["marker"] == "P"),
            ObservationOutcome("H", 0.5, lambda row: row["marker"] == "H"),
        ),
    )
    value = expected_observation_value(rows, ("pollination", "history"), candidate)

    assert value.baseline_resolvability == pytest.approx(0.5)
    assert value.expected_resolvability_gain == pytest.approx(0.5)
    assert value.expected_gain_per_cost == pytest.approx(0.25)


def test_current_izu_evidence_is_not_silently_promoted_to_wfe_theorem() -> None:
    validate_projection_ledger()

    historical = projection_for("historical_campanula_three_channel_record")
    fdq = projection_for("hiraiwa_ushimaru_fdq_matching")
    field = projection_for("issue91_linked_dependency_field_chain")

    assert historical.status is ProjectionStatus.NOT_APPLICABLE
    assert "Nectar-guide change is excluded" in historical.current_output
    assert fdq.status is ProjectionStatus.NOT_APPLICABLE
    assert field.status is ProjectionStatus.REQUIRES_FACTORIZATION_EXTENSION
    assert not historical.theorem_ids
    assert not fdq.theorem_ids
    assert not field.theorem_ids


def test_abstract_model_is_the_only_exact_current_projection() -> None:
    abstract = projection_for("abstract_positive_wfe_model")
    assert abstract.status is ProjectionStatus.EXACT
    assert abstract.theorem_ids == ("N1", "N2", "N3", "N4")
    assert not abstract.missing_requirements
