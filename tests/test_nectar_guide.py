from channel_id.nectar_guide import (
    GuideSelectionDirection,
    NectarGuideParameters,
    NectarGuideRegime,
    NectarGuideTrait,
    compare_guide_phenotypes,
    simulate_nectar_guide_life_history,
)


def parameters(**changes: float) -> NectarGuideParameters:
    values = dict(
        seed_budget=10.0,
        display_cost=0.0,
        guide_cost=0.0,
        assurance_cost=0.0,
        baseline_visit_rate=0.4,
        display_visit_gain=0.0,
        guide_visit_gain=0.0,
        baseline_legitimate_fraction=0.2,
        guide_handling_gain=0.0,
        pollen_to_outcross_fraction=1.0,
        selfing_viability=0.6,
        baseline_establishment=0.2,
    )
    values.update(changes)
    return NectarGuideParameters(**values)


def test_visit_pathway_changes_visits_without_changing_handling_fraction() -> None:
    regime = NectarGuideRegime(pollinator_service=0.8)
    low = simulate_nectar_guide_life_history(
        NectarGuideTrait(guide_contrast=0.0, display=0.5, assurance=0.2),
        regime,
        parameters(guide_visit_gain=1.0),
    )
    high = simulate_nectar_guide_life_history(
        NectarGuideTrait(guide_contrast=1.0, display=0.5, assurance=0.2),
        regime,
        parameters(guide_visit_gain=1.0),
    )

    assert high.expected_visits > low.expected_visits
    assert high.legitimate_contact_fraction == low.legitimate_contact_fraction
    assert high.outcross_viable_seeds > low.outcross_viable_seeds


def test_handling_pathway_changes_handling_without_changing_visits() -> None:
    regime = NectarGuideRegime(pollinator_service=0.8)
    low = simulate_nectar_guide_life_history(
        NectarGuideTrait(guide_contrast=0.0, display=0.5, assurance=0.2),
        regime,
        parameters(guide_handling_gain=0.6),
    )
    high = simulate_nectar_guide_life_history(
        NectarGuideTrait(guide_contrast=1.0, display=0.5, assurance=0.2),
        regime,
        parameters(guide_handling_gain=0.6),
    )

    assert high.expected_visits == low.expected_visits
    assert high.legitimate_contact_fraction > low.legitimate_contact_fraction
    assert high.outcross_viable_seeds > low.outcross_viable_seeds


def test_cost_only_pathway_reduces_budget_and_recruits() -> None:
    regime = NectarGuideRegime(pollinator_service=0.8)
    low = simulate_nectar_guide_life_history(
        NectarGuideTrait(guide_contrast=0.0, display=0.5, assurance=0.2),
        regime,
        parameters(guide_cost=4.0),
    )
    high = simulate_nectar_guide_life_history(
        NectarGuideTrait(guide_contrast=1.0, display=0.5, assurance=0.2),
        regime,
        parameters(guide_cost=4.0),
    )

    assert high.expected_visits == low.expected_visits
    assert high.legitimate_contact_fraction == low.legitimate_contact_fraction
    assert high.remaining_seed_budget < low.remaining_seed_budget
    assert high.retained_recruits < low.retained_recruits


def test_relative_performance_can_favour_higher_or_lower_guide() -> None:
    low_trait = NectarGuideTrait(guide_contrast=0.0, display=0.5, assurance=0.2)
    high_trait = NectarGuideTrait(guide_contrast=1.0, display=0.5, assurance=0.2)
    regime = NectarGuideRegime(pollinator_service=0.8)

    benefit = compare_guide_phenotypes(
        low_trait,
        high_trait,
        regime,
        parameters(guide_visit_gain=1.0),
    )
    cost = compare_guide_phenotypes(
        low_trait,
        high_trait,
        regime,
        parameters(guide_cost=4.0),
    )

    assert benefit.direction is GuideSelectionDirection.FAVOURS_HIGHER_GUIDE
    assert cost.direction is GuideSelectionDirection.FAVOURS_LOWER_GUIDE


def test_factorisation_holds() -> None:
    result = simulate_nectar_guide_life_history(
        NectarGuideTrait(guide_contrast=0.7, display=0.5, assurance=0.6),
        NectarGuideRegime(pollinator_service=0.4, establishment_multiplier=1.2),
        parameters(guide_visit_gain=0.5, guide_handling_gain=0.3, guide_cost=0.4),
    )

    assert result.local_viable_seed_output == (
        result.outcross_viable_seeds + result.selfed_viable_seeds
    )
    assert result.retained_recruits == (
        result.local_viable_seed_output * result.establishment
    )
