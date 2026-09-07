from __future__ import annotations

import json
import re
from pathlib import Path

from scripts.render_island_ecology_submission_manuscript import render_submission_manuscript as render_pre_richness_submission

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "data/results/chapter2_realized_richness_matching_decision_20260907.json"
DEFAULT_OUTPUT = ROOT / "dist/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUBMISSION_CLEAN.md"

OLD_ABSTRACT_OPENING = (
    "The same environmental change can produce opposite biological responses, yet mean effects do not identify the state–community relationship that determines response direction. "
    "We ask whether pollinator-community reorganization is better represented as a conditional response geometry and what resolution is required to distinguish its mechanisms."
)

NEW_ABSTRACT_OPENING = (
    "Island-associated pollinator change is often summarized as diversity loss, but changes in partner identity and functional composition can expose established plants to qualitatively different interaction environments. "
    "We ask whether pollinator-community reorganization produces a hierarchical response architecture in which realized richness positions a coarse response regime while plant starting state evaluated against realized community composition determines response branches."
)

OLD_ABSTRACT_METHOD = (
    "We exposed the interaction kernel in a frozen matching model, separated regime movement from state-by-community branch identity, local filtering and downstream assurance, and confronted that vocabulary with island research. "
    "The formal source audit remained outcome-rich but process-poor: responses were directly measured in 21/25 entries, partner arrival/replacement in 2/25, and no entry supplied the full outcome-independent contract. "
    "A geography-first expansion reached a two-tranche zero-novelty stopping rule; a small-island supplement recovered transition chronology but still no full matched contract. "
    "Izu was then selected for depth by measurement continuity rather than proximity, representativeness or positive model fit."
)

NEW_ABSTRACT_METHOD = (
    "We first used a frozen plant–pollinator matching model to separate richness-sensitive regime placement from state-by-community branching. "
    "We then tested whether the ecological exposure required by that mechanism—compositional reorganization not reducible to richness loss—occurs in source-native island interaction networks, using Wanshan–Yongxing and Ogasawara contrasts. "
    "Finally, source-locked contemporary Izu networks tested whether pollinator functional structure maps onto plant trait matching and whether that signal propagates uniformly to pollen receipt and floral responses. "
    "Literature identifiability audits were retained only to bound historical causal claims."
)

OLD_ABSTRACT_RESULT = (
    "Across 96 matched community realizations, 41 contained both positive and negative responses, and mixed geometry persisted when initial pollinator richness was equalized (53/96). "
    "Partner loss and arrival were the strongest sign-stable regime associations. Community realization remained the largest additive component across prespecified sensitivities, while state-by-community non-additivity remained consequential. "
    "In Izu, contemporary pollinator functional diversity positively predicted corrected trait matching with leave-one-island sign stability; matching-to-pollen propagation was weaker, and eight shared plant targets with lower corrected matching split into shorter, longer and unchanged floral responses and into higher versus lower pollen receipt."
)

NEW_ABSTRACT_RESULT = (
    "Across 96 baseline community realizations, 41 contained both positive and negative responses. Matching realized richness at every simulated step shifted the ensemble mean geometry to all-positive in all six prespecified matching seeds, yet 51–65/96 individual communities remained mixed and state × community non-additivity remained 42.7–48.5%. "
    "In Wanshan–Yongxing and Ogasawara, partner turnover was high (0.980 and 0.682) while pollinator-richness contrasts were less decisive. "
    "In Izu, pollinator functional diversity positively predicted corrected trait matching with leave-one-island sign stability; matching-to-pollen propagation was weaker, and eight plant targets sharing lower corrected matching split into shorter, longer and unchanged floral responses and into higher versus lower pollen receipt."
)

OLD_ABSTRACT_CONCLUSION = (
    "Response direction is therefore relational rather than intrinsic. World expansion localizes the empirical bottleneck to transition-linked process measurement, while Izu resolves the contemporary functional-realization half of the chain without identifying historical partner turnover. "
    "The remaining coordinate is a matched pre-transition state, observed partner transition and post-transition reproductive response on matched units."
)

NEW_ABSTRACT_CONCLUSION = (
    "Together, these results support a hierarchical view of island plant response: richness helps position the coarse opportunity regime, composition interacting with plant state retains branch contingency, and downstream biological responses propagate only contingently. "
    "The analysis does not establish one matched historical partner transition across all layers; that missing coordinate bounds causal interpretation rather than defining the study objective."
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

THREE_RESULT_INTRO = (
    "The paper therefore follows one three-step argument. **Result 1—mechanistic prediction:** the synthetic model separates richness-sensitive coarse regime placement from branch identity generated by plant starting state evaluated against realized community composition. "
    "**Result 2—real-world exposure:** source-native external network contrasts test whether island systems actually undergo compositional reorganization that is not reducible to richness loss. "
    "**Result 3—biological consequence:** the Izu series tests whether contemporary functional community structure maps onto plant–pollinator matching and whether that signal propagates uniformly or branches across downstream floral and reproductive responses. "
    "The identifiability audit is retained as a claim-boundary and robustness layer, not as a coequal study objective."
)

INTRO_BRIDGE = (
    "After defining the mechanism, we ask first whether the required ecological exposure exists in nature and then whether it reaches plants. "
    "Source-native Wanshan–Yongxing and Ogasawara network contrasts provide the exposure test because partner turnover can be compared directly with richness change. "
    "Izu then provides the consequence test within one source-linked regional series by connecting contemporary pollinator functional structure to corrected trait matching and downstream pollen and floral responses. "
    "Historical source-state analyses and the broader measurement audit are retained as adversarial boundary checks: they prevent present functional associations from being rewritten as proof of historical partner loss."
)

R2_EXPOSURE_PARAGRAPH = (
    "Result 1 requires more than a generic decline in diversity: branch contingency depends on which partners remain or replace one another. Two source-native external reanalyses show that this exposure occurs in real island systems. "
    "For the matched seven-plant Wanshan–Yongxing subnetwork, pollinator assemblage turnover was 0.9796 (Morisita–Horn turnover; exact bootstrap 95% interval 0.9443–1.0000), whereas the pollinator-richness log response ratio was −0.1054 with a 95% interval of −1.3218 to +0.2877 (Wang et al., 2025). "
    "Within the source-defined Anijima anole presence/absence contrast in Ogasawara, matched-plant turnover was 0.6817 (95% interval 0.4975–0.9653), whereas the richness log response ratio was −0.3146 with a 95% interval of −0.8755 to +0.4055 (Quitián et al., 2026). "
    "These contexts are not exchangeable replicates and neither contrast identifies a universal island cause, but together they establish the premise needed for Result 1: substantial partner reorganization can occur without a correspondingly decisive richness contrast."
)

OLD_DISCUSSION_HEADING = "## Theory: response direction is relational rather than intrinsic"
NEW_DISCUSSION_HEADING = "## Result 1 synthesis: richness positions the coarse regime while branch identity remains relational"

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

FINAL_SYNTHESIS = (
    "Together, the three results support a hierarchical response architecture under community reorganization. Realized richness helps position the coarse opportunity regime; partner composition interacting with plant state retains substantial branch contingency; source-native island networks demonstrate that such compositional reorganization can occur without a decisive richness contrast; and in Izu contemporary functional community structure maps onto plant matching while downstream floral and reproductive responses branch. "
    "The unresolved matched historical transition remains a limit on causal interpretation, not the central result. The contribution is therefore an ecological mechanism for why one island-response syndrome is insufficient, rather than an account of why previous studies failed to identify it."
)


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"realized-richness reframe source changed for {label}: expected exactly one occurrence")
    return text.replace(old, new, 1)


def _replace_paragraph_starting(text: str, start: str, new: str, label: str) -> str:
    idx = text.find(start)
    if idx < 0:
        raise ValueError(f"{label} changed; paragraph start not found")
    end = text.find("\n\n", idx)
    if end < 0:
        raise ValueError(f"{label} changed; paragraph end not found")
    return text[:idx] + new + text[end:]


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


def _reframe_results(text: str) -> str:
    heading_replacements = (
        (
            "## Theory — possibility: the same reorganization generated opposite responses",
            "## Result 1 — Community reorganization separated coarse regime placement from branch identity\n\nThe first result defines the mechanism needed by the empirical sections: richness can move the coarse response regime, while the identity of the realized partners can still allocate different plant states to different response branches.\n\n### Result 1 baseline — the same reorganization generated opposite responses",
        ),
        (
            "## Theory — regime structure: turnover moved the system among response regimes",
            "### Result 1 mechanism — turnover moved the system among response regimes",
        ),
        (
            "## Theory — relational branch identity: response direction was not a stable state-only effect",
            "### Result 1 mechanism — branch identity was not a stable state-only effect",
        ),
        (
            "## Theory — branch allocation: local filtering reallocated branches asymmetrically",
            "### Result 1 downstream modifier — local filtering reallocated branches asymmetrically",
        ),
        (
            "## Theory — downstream propagation: assurance attenuated magnitude without rescuing sign",
            "### Result 1 downstream modifier — assurance attenuated magnitude without rescuing sign",
        ),
        (
            "## Global confrontation: real island systems required more than one response state",
            "## Result 2 — Real island systems undergo compositional reorganization beyond richness loss\n\n"
            + R2_EXPOSURE_PARAGRAPH
            + "\n\n### Result 2 broader context — real island responses also require more than one response state",
        ),
        (
            "## Identifiability: the formal literature audit was outcome-rich but process-poor",
            "### Result 2 claim boundary — the formal literature audit was outcome-rich but process-poor",
        ),
        (
            "## Identifiability: geography-first expansion saturated before the transition contract closed",
            "### Result 2 robustness boundary — geography-first expansion saturated before a complete historical transition chain closed",
        ),
    )
    for old, new in heading_replacements:
        text = _replace_once(text, old, new, f"three-result Results heading {old}")

    izu_pattern = re.compile(
        r"\n## Izu mechanistic zoom: raw signed-position matching localized the signal to source state and composition\n(?P<raw>.*?)"
        r"\n## Izu mechanistic zoom: the historical signed-position predictor did not explain null-corrected matching\n(?P<corrected>.*?)"
        r"\n## Izu mechanistic zoom: contemporary functional diversity predicted corrected matching within Izu\n(?P<contemporary>.*?)"
        r"\n## Izu mechanistic zoom: downstream propagation weakened and plant responses branched\n(?P<downstream>.*?)(?=\n# Discussion)",
        flags=re.DOTALL,
    )
    match = izu_pattern.search(text)
    if match is None:
        raise ValueError("Izu Results block changed; refuse silent three-result reordering")
    replacement = (
        "\n## Result 3 — Functional community structure in Izu propagated into divergent plant responses\n\n"
        "Result 2 establishes that composition change beyond richness loss is a real island exposure. Izu then asks whether contemporary functional community structure maps onto the interaction state experienced by plants and whether that signal propagates uniformly downstream.\n\n"
        "### Result 3a — contemporary functional diversity predicted corrected matching within Izu\n"
        + match.group("contemporary").strip()
        + "\n\n### Result 3b — downstream propagation weakened and plant responses branched\n"
        + match.group("downstream").strip()
        + "\n\n### Historical boundary check — raw signed-position signal localized to source state and composition\n"
        + match.group("raw").strip()
        + "\n\n### Historical boundary check — the signed-position predictor did not explain null-corrected matching\n"
        + match.group("corrected").strip()
        + "\n"
    )
    return text[: match.start()] + replacement + text[match.end() :]


def _reframe_methods(text: str) -> str:
    inference_pattern = re.compile(
        r"## Inference architecture and claim boundary\n\n.*?(?=\nThe synthetic plant coordinate is standardized to \[0,1\])",
        flags=re.DOTALL,
    )
    replacement = (
        "## Inference architecture and claim boundary\n\n"
        "The paper uses one synthetic mechanism layer and two empirical layers in a sequential argument.\n\n"
        "1. **Mechanistic prediction.** The synthetic analysis separates richness-sensitive mean-regime placement from branch contingency associated with plant starting state and realized community composition. No empirical island outcome is used to fit synthetic thresholds.\n"
        "2. **Real-world compositional exposure.** Source-native Wanshan–Yongxing and Ogasawara network contrasts test whether substantial partner turnover can occur without a correspondingly decisive richness contrast. These are bounded context examples, not a pooled island effect or causal treatment. The broader source audit is retained only to bound stronger historical-transition claims.\n"
        "3. **Izu biological consequence.** Source-locked contemporary Izu analyses test whether pollinator functional structure is associated with corrected plant–pollinator matching and whether that interaction signal propagates uniformly to pollen receipt and floral responses. Historical signed-position analyses are adversarial boundary checks rather than validation of the synthetic mechanism.\n"
    )
    text, n = inference_pattern.subn(replacement, text, count=1)
    if n != 1:
        raise ValueError("inference architecture changed; refuse silent three-result methods reframe")
    text = text.replace(
        "## World confrontation and external identifiability audit",
        "## External compositional-reorganization test and historical claim boundary",
        1,
    )
    text = text.replace(
        "## Izu mechanistic-resolution zoom",
        "## Izu contemporary functional-chain analysis and historical boundary checks",
        1,
    )
    return text


def render_submission_manuscript() -> str:
    _validate_decision()
    text = render_pre_richness_submission()
    for old, new, label in (
        (OLD_ABSTRACT_OPENING, NEW_ABSTRACT_OPENING, "abstract opening"),
        (OLD_ABSTRACT_METHOD, NEW_ABSTRACT_METHOD, "abstract methods"),
        (OLD_ABSTRACT_RESULT, NEW_ABSTRACT_RESULT, "abstract result"),
        (OLD_ABSTRACT_CONCLUSION, NEW_ABSTRACT_CONCLUSION, "abstract conclusion"),
        (OLD_METHOD, NEW_METHOD, "robustness methods"),
        (OLD_RESULT, NEW_RESULT, "richness result"),
        (OLD_DISCUSSION_HEADING, NEW_DISCUSSION_HEADING, "discussion heading"),
        (OLD_DISCUSSION_FIRST, NEW_DISCUSSION_FIRST, "discussion opening"),
        (OLD_DISCUSSION_STRUCTURAL, NEW_DISCUSSION_STRUCTURAL, "discussion structural audit"),
    ):
        text = _replace_once(text, old, new, label)

    text = _replace_paragraph_starting(
        text,
        "The paper therefore proceeds through four inferential acts.",
        THREE_RESULT_INTRO,
        "four-act Introduction paragraph",
    )
    text = _replace_paragraph_starting(
        text,
        "The move from breadth to Izu is therefore an inferential decision rather than a geographic convenience.",
        INTRO_BRIDGE,
        "breadth-to-Izu Introduction bridge",
    )
    text = _reframe_methods(text)
    text = _reframe_results(text)

    discussion_heading_replacements = (
        (
            "## Theory: the proximal mechanism separates regime, relational branch identity and downstream propagation",
            "### Result 1 synthesis — downstream modifiers do not erase the richness/composition hierarchy",
        ),
        (
            "## Global confrontation and identifiability: breadth saturates before the transition contract closes",
            "## Result 2 synthesis: composition change beyond richness loss is a real island exposure",
        ),
        (
            "## Izu mechanistic zoom: continuity and falsification justify focal depth",
            "## Result 3 synthesis: functional community structure reaches plants, but downstream propagation branches",
        ),
    )
    for old, new in discussion_heading_replacements:
        text = _replace_once(text, old, new, f"Discussion three-result heading {old}")

    text = _replace_paragraph_starting(
        text,
        "The study therefore closes with a conditional response geometry, a world-level saturation/identifiability result and a justified continuity system for depth.",
        FINAL_SYNTHESIS,
        "final synthesis",
    )

    lower = text.lower()
    stale = (
        "mixed geometry persisted when initial pollinator richness was equalized",
        "richness reduction is not necessary for mixed response geometry",
        "response direction is therefore relational rather than intrinsic",
        "the paper therefore proceeds through four inferential acts",
    )
    survived = [token for token in stale if token in lower]
    if survived:
        raise ValueError(f"stale pre-reframe claim survived final submission render: {survived}")
    forbidden_top_level = (
        "\n## identifiability:",
        "\n## global confrontation:",
        "\n## izu mechanistic zoom:",
    )
    survived_headings = [token for token in forbidden_top_level if token in lower]
    if survived_headings:
        raise ValueError(f"superseded top-level result architecture survived: {survived_headings}")

    required = (
        "result 1—mechanistic prediction",
        "result 2—real-world exposure",
        "result 3—biological consequence",
        "## result 1 — community reorganization separated coarse regime placement from branch identity",
        "## result 2 — real island systems undergo compositional reorganization beyond richness loss",
        "wanshan–yongxing subnetwork",
        "pollinator assemblage turnover was 0.9796",
        "matched-plant turnover was 0.6817",
        "## result 3 — functional community structure in izu propagated into divergent plant responses",
        "all-positive in all six prespecified matching seeds",
        "51–65 of 96 remained mixed-sign",
        "state × community non-additivity remained 42.72–48.51%",
        "historical boundary check",
        "bounds causal interpretation rather than defining the study objective",
        "10.1111/btp.70027",
        "10.1111/cobi.70304",
    )
    missing = [token for token in required if token.lower() not in lower]
    if missing:
        raise ValueError(f"three-result reframe disappeared from final submission render: {missing}")
    return text


def render_to_path(output: Path = DEFAULT_OUTPUT) -> Path:
    text = render_submission_manuscript()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return output


if __name__ == "__main__":
    print(render_to_path())
