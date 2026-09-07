from __future__ import annotations

import json
from pathlib import Path

from scripts.render_island_ecology_submission_manuscript import render_submission_manuscript as render_pre_richness_submission

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "data/results/chapter2_realized_richness_matching_decision_20260907.json"
DEFAULT_OUTPUT = ROOT / "dist/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUBMISSION_CLEAN.md"

OLD_ABSTRACT_RESULT = (
    "Across 96 matched community realizations, 41 contained both positive and negative responses, and mixed geometry persisted when initial pollinator richness was equalized (53/96). "
    "Partner loss and arrival were the strongest sign-stable regime associations. Community realization remained the largest additive component across prespecified sensitivities, while state-by-community non-additivity remained consequential. "
    "In Izu, contemporary pollinator functional diversity positively predicted corrected trait matching with leave-one-island sign stability; matching-to-pollen propagation was weaker, and eight shared plant targets with lower corrected matching split into shorter, longer and unchanged floral responses and into higher versus lower pollen receipt."
)

NEW_ABSTRACT_RESULT = (
    "Across 96 baseline community realizations, 41 contained both positive and negative responses. Equalizing initial pollinator richness retained 53/96 mixed realizations, but a stronger prespecified control that matched realized richness at every simulated step shifted the ensemble mean geometry to all-positive in all six matching seeds. "
    "Mixed-sign individual communities nevertheless remained common (51–65/96), with state-by-community non-additivity of 42.7–48.5%. Partner loss and arrival remained the strongest sign-stable regime associations. "
    "In Izu, contemporary pollinator functional diversity positively predicted corrected trait matching with leave-one-island sign stability; matching-to-pollen propagation was weaker, and downstream floral and pollen responses branched among shared plant targets."
)

OLD_ABSTRACT_CONCLUSION = (
    "Response direction is therefore relational rather than intrinsic. World expansion localizes the empirical bottleneck to transition-linked process measurement, while Izu resolves the contemporary functional-realization half of the chain without identifying historical partner turnover. "
    "The remaining coordinate is a matched pre-transition state, observed partner transition and post-transition reproductive response on matched units."
)

NEW_ABSTRACT_CONCLUSION = (
    "Mean regime placement is therefore richness-sensitive, while response branching remains relational to starting state and realized community composition. World expansion localizes the empirical bottleneck to transition-linked process measurement, while Izu resolves the contemporary functional-realization half of the chain without identifying historical partner turnover. "
    "The remaining coordinate is a matched pre-transition state, observed partner transition and post-transition reproductive response on matched units."
)

OLD_METHOD = (
    "After an independent code audit identified model horizon and ensemble dependence as unreported sensitivities, we froze an additional structural audit before execution. The historical baseline (`seed=20260826`, `steps=120`, trait adjustment 0.03) was retained and could not be replaced after inspection. "
    "We evaluated `steps={30,60,120,240}`, trait adjustment `{0,0.01,0.03,0.06}`, and the historical seed plus five prespecified sensitivity seeds. We separately equalized initial pollinator richness at 9 mainland-like versus 9 island-like types while retaining all other baseline differences in loss, arrival, trait dispersion, generalist fraction and replacement fraction. "
    "The equal-richness sensitivity therefore tests only whether richness reduction is necessary for mixed geometry."
)

NEW_METHOD = (
    "After an independent code audit identified model horizon and ensemble dependence as unreported sensitivities, we froze an additional structural audit before execution. The historical baseline (`seed=20260826`, `steps=120`, trait adjustment 0.03) was retained and could not be replaced after inspection. "
    "We evaluated `steps={30,60,120,240}`, trait adjustment `{0,0.01,0.03,0.06}`, and the historical seed plus five prespecified sensitivity seeds. We first equalized initial pollinator richness at 9 mainland-like versus 9 island-like types while retaining all other baseline differences. Because this did not equalize richness after loss and arrival, we then froze a second, stronger control before execution. "
    "For the same 96 BASE trajectory pairs, at every simulated step we set both communities to `min(realized mainland richness, realized island richness)` by uniformly subsampling only the larger snapshot without replacement. Subsampling was independent of plant state, pollinator traits, breadth and response, and six matching seeds were specified in advance. The matched trajectories, rather than the original trajectories, were then supplied to trait adjustment and endpoint service."
)

OLD_RESULT = (
    "Mixed response geometry was not a mechanical consequence of reduced initial pollinator richness. When island-like initial pollinator richness was increased from four to nine, matching the mainland-like initial richness while all other scenario differences remained unchanged, 53/96 realizations were mixed-sign, 31 all-positive and 12 all-negative. "
    "Thus richness reduction is not necessary for mixed response geometry; the sensitivity does not remove other forms of community reorganization."
)

NEW_RESULT = (
    "Equalizing only initial pollinator richness did not remove mixed individual realizations: when island-like initial richness was increased from four to nine, 53/96 realizations were mixed-sign, 31 all-positive and 12 all-negative. This sensitivity retained subsequent richness divergence caused by loss and arrival and therefore did not isolate realized richness.\n\n"
    "The stronger hard control did. Across 11,520 step-pairs per matching seed, mainland-like and island-like realized richness was exactly equal after matching in every case. Under this control, the mean response geometry became all-positive in all six prespecified matching seeds. Individual community realizations still branched strongly: 51–65 of 96 remained mixed-sign across matching seeds. State × community non-additivity remained 42.72–48.51%, community-realization share 50.04–55.92%, and the additive starting-position share only 0.94–2.21%. Realized richness differences therefore help position the ensemble mean regime, but they do not explain away response branching across realized community compositions."
)

OLD_DISCUSSION_HEADING = "## Theory: response direction is relational rather than intrinsic"
NEW_DISCUSSION_HEADING = "## Theory: mean regime placement is richness-sensitive, while branch identity remains relational"

OLD_DISCUSSION_FIRST = (
    "The synthetic analysis rejects a one-direction description of post-establishment response within the declared model. The same broad pollinator reorganization can yield positive, mixed or negative regimes, and mixed geometry persists when initial pollinator richness is held equal between mainland-like and island-like scenarios. "
    "The interaction-kernel derivation clarifies the common object across these outcomes: response sign records which of two trajectory-conditioned community kernels provides greater endpoint service for a given starting state."
)

NEW_DISCUSSION_FIRST = (
    "The synthetic analysis separates two questions that the initial-richness sensitivity had conflated. Realized richness materially positions the ensemble mean regime: when richness was forced to be identical at every simulated step, all six prespecified matching seeds produced an all-positive mean geometry. "
    "Branch identity, however, did not collapse to one response. More than half of the individual community realizations remained mixed in every matching seed, and state × community non-additivity increased to 42.7–48.5%. The interaction-kernel derivation therefore remains the common object, but the hierarchy is sharper: richness changes the coarse opportunity regime, while starting state evaluated against realized composition determines substantial within-regime branching."
)

OLD_DISCUSSION_STRUCTURAL = (
    "The structural audit also changes what should be treated as robust. The historically frozen 80.17% community share is an upper-end value within the prespecified six-seed sensitivity and should not serve as a population-like headline. What survives is the ordering: community realization remained the largest component across all six seeds, all four audited horizons, all four trait-adjustment values and the equal-richness sensitivity, while starting position alone remained a weak additive component. The general inference is therefore structural rather than magnitude-specific."
)

NEW_DISCUSSION_STRUCTURAL = (
    "The structural audits also change what should be treated as robust. The historically frozen 80.17% community share is an upper-end value within the original six-seed sensitivity and should not serve as a population-like headline. Under exact realized-richness matching, community realization still accounted for 50.0–55.9% and state × community non-additivity for 42.7–48.5%, whereas starting position alone remained only 0.94–2.21%. The robust inference is therefore not that richness is irrelevant, but that richness-sensitive regime placement coexists with strong relational contingency that cannot be reduced to an additive starting-state effect."
)


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"realized-richness reframe source changed for {label}: expected exactly one occurrence")
    return text.replace(old, new, 1)


def _validate_decision() -> dict:
    payload = json.loads(DECISION.read_text(encoding="utf-8"))
    if payload.get("status") != "frozen_decision_20260907":
        raise ValueError("realized-richness decision is not frozen")
    gate = payload["prespecified_gate"]
    expected = {
        "hard_control_valid": True,
        "primary_mixed_geometry": False,
        "ensemble_mixed_geometry": False,
        "individual_mixed_realizations": True,
        "relational_nonadditivity": True,
        "decision": "blocker_failed_reframe_before_author_metadata",
    }
    if gate != expected:
        raise ValueError("realized-richness decision changed; refuse silent manuscript rendering")
    return payload


def render_submission_manuscript() -> str:
    _validate_decision()
    text = render_pre_richness_submission()
    for old, new, label in (
        (OLD_ABSTRACT_RESULT, NEW_ABSTRACT_RESULT, "abstract result"),
        (OLD_ABSTRACT_CONCLUSION, NEW_ABSTRACT_CONCLUSION, "abstract conclusion"),
        (OLD_METHOD, NEW_METHOD, "robustness methods"),
        (OLD_RESULT, NEW_RESULT, "richness result"),
        (OLD_DISCUSSION_HEADING, NEW_DISCUSSION_HEADING, "discussion heading"),
        (OLD_DISCUSSION_FIRST, NEW_DISCUSSION_FIRST, "discussion opening"),
        (OLD_DISCUSSION_STRUCTURAL, NEW_DISCUSSION_STRUCTURAL, "discussion structural audit"),
    ):
        text = _replace_once(text, old, new, label)

    lower = text.lower()
    stale = (
        "mixed geometry persisted when initial pollinator richness was equalized",
        "richness reduction is not necessary for mixed response geometry",
        "response direction is therefore relational rather than intrinsic",
    )
    survived = [token for token in stale if token in lower]
    if survived:
        raise ValueError(f"stale richness-independent claim survived final submission render: {survived}")
    required = (
        "mean regime placement is therefore richness-sensitive",
        "51–65 of 96 remained mixed-sign",
        "state × community non-additivity remained 42.72–48.51%",
        "all six prespecified matching seeds",
        "11,520 step-pairs per matching seed",
    )
    missing = [token for token in required if token.lower() not in lower]
    if missing:
        raise ValueError(f"realized-richness reframe disappeared from final submission render: {missing}")
    return text


def render_to_path(output: Path = DEFAULT_OUTPUT) -> Path:
    text = render_submission_manuscript()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return output


if __name__ == "__main__":
    print(render_to_path())
