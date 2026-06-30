from channel_id.guide_inbreeding import PostSeedSurvival
from channel_id.guide_paternal import PaternalGuideParameters
from channel_id.guide_scenarios import GuideScenario, ScenarioSettings, ScenarioYear
from channel_id.izu_gradient_benchmark import IzuGradientLandscape, IzuGradientSite
from channel_id.izu_observational_equivalence import (
    observational_equivalence_groups,
    observationally_distinct_candidates,
)
from channel_id.nectar_guide import NectarGuideParameters, NectarGuideTrait


def settings(guide_cost: float) -> ScenarioSettings:
    return ScenarioSettings(
        trait=NectarGuideTrait(0.1, 0.4, 0.5),
        maternal_parameters=NectarGuideParameters(
            10.0,
            0.0,
            guide_cost,
            0.1,
            0.2,
            0.0,
            1.0,
            0.2,
            0.8,
            1.0,
            0.6,
            1.0,
        ),
        paternal_parameters=PaternalGuideParameters(1.0, 0.0, 1.0, 0.2),
        post_seed_survival=PostSeedSurvival(0.4, 0.5),
        years=(ScenarioYear("template", 0.7),),
    )


def landscape() -> IzuGradientLandscape:
    return IzuGradientLandscape(0.1, 0.9, 0.8, 0.4, 1.0, 0.7)


def test_zero_cost_collapses_null_and_cost_routes_but_not_visit() -> None:
    candidates = (GuideScenario.NULL, GuideScenario.COST, GuideScenario.VISIT_ATTRACTION)
    groups = observational_equivalence_groups(
        candidates,
        settings(guide_cost=0.0),
        landscape(),
        sites=(IzuGradientSite("north", 0.0), IzuGradientSite("south", 1.0)),
    )

    assert groups == (
        (GuideScenario.NULL, GuideScenario.COST),
        (GuideScenario.VISIT_ATTRACTION,),
    )
    assert observationally_distinct_candidates(
        candidates,
        settings(guide_cost=0.0),
        landscape(),
        sites=(IzuGradientSite("north", 0.0), IzuGradientSite("south", 1.0)),
    ) == (GuideScenario.NULL, GuideScenario.VISIT_ATTRACTION)


def test_positive_cost_restores_a_separate_cost_prediction() -> None:
    candidates = (GuideScenario.NULL, GuideScenario.COST)
    groups = observational_equivalence_groups(
        candidates,
        settings(guide_cost=1.0),
        landscape(),
        sites=(IzuGradientSite("north", 0.0), IzuGradientSite("south", 1.0)),
    )

    assert groups == ((GuideScenario.NULL,), (GuideScenario.COST,))
