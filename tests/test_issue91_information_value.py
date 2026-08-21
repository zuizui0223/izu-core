from channel_id.causal_admissibility import CandidateObservation, ObservationOutcome
from channel_id.issue91_information_value import (
    FieldEffortOption,
    PilotGateState,
    rank_issue91_field_effort,
)


def _rows():
    return [
        {"service_limited": True, "autonomous_assurance": False, "marker": "S"},
        {"service_limited": True, "autonomous_assurance": False, "marker": "S"},
        {"service_limited": False, "autonomous_assurance": True, "marker": "A"},
        {"service_limited": False, "autonomous_assurance": True, "marker": "A"},
    ]


def _candidate(name: str, cost: float, informative: bool = True) -> CandidateObservation:
    if informative:
        outcomes = (
            ObservationOutcome("S", 0.5, lambda row: row["marker"] == "S"),
            ObservationOutcome("A", 0.5, lambda row: row["marker"] == "A"),
        )
    else:
        outcomes = (
            ObservationOutcome("all1", 0.5, lambda row: True),
            ObservationOutcome("all2", 0.5, lambda row: True),
        )
    return CandidateObservation(name=name, cost=cost, outcomes=outcomes)


def test_missing_mandatory_gate_outranks_high_information_optional_measurement():
    state = PilotGateState(
        linked_ids_and_effort=True,
        no_visit_svd_control=False,
        svd_two_independent_plants=True,
        open_two_independent_plants=True,
        bagged_two_independent_plants=True,
        supplemental_two_independent_plants=True,
        terminal_fruit_seed_linkage=True,
    )
    options = (
        FieldEffortOption(
            "collect missing no-visit SVD control",
            gate_target="no_visit_svd_control",
        ),
        FieldEffortOption(
            "optional discriminating repeat",
            gate_target=None,
            candidate=_candidate("optional", cost=1.0, informative=True),
        ),
    )
    ranked = rank_issue91_field_effort(
        state, _rows(), ("service_limited", "autonomous_assurance"), options
    )
    assert ranked[0].name == "collect missing no-visit SVD control"
    assert ranked[0].tier == 1
    assert ranked[1].tier == 2


def test_when_gates_are_complete_marginal_effort_is_ranked_by_information_per_cost():
    state = PilotGateState(True, True, True, True, True, True, True)
    options = (
        FieldEffortOption(
            "cheap discriminating repeat",
            None,
            _candidate("cheap", cost=1.0, informative=True),
        ),
        FieldEffortOption(
            "expensive discriminating repeat",
            None,
            _candidate("expensive", cost=4.0, informative=True),
        ),
        FieldEffortOption(
            "uninformative repeat",
            None,
            _candidate("flat", cost=0.5, informative=False),
        ),
    )
    ranked = rank_issue91_field_effort(
        state, _rows(), ("service_limited", "autonomous_assurance"), options
    )
    assert [item.name for item in ranked] == [
        "cheap discriminating repeat",
        "expensive discriminating repeat",
        "uninformative repeat",
    ]
    assert all(item.tier == 2 for item in ranked)
    assert ranked[0].expected_gain_per_cost > ranked[1].expected_gain_per_cost
    assert ranked[2].expected_resolvability_gain == 0.0


def test_extra_replication_of_an_already_satisfied_gate_is_marginal_not_mandatory():
    state = PilotGateState(True, True, True, True, True, True, True)
    option = FieldEffortOption(
        "third SVD plant",
        gate_target="svd_two_independent_plants",
        candidate=_candidate("third_svd", cost=1.0, informative=True),
    )
    ranked = rank_issue91_field_effort(
        state, _rows(), ("service_limited", "autonomous_assurance"), (option,)
    )
    assert ranked[0].tier == 2
