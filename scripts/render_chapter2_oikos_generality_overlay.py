from __future__ import annotations

from scripts.generate_chapter2_manuscript_tables import build as build_base_tables
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript as render_base_manuscript

OLD_TITLE = "Response geometry under community reorganization: from ecological possibility to mechanistic resolution in island plant–pollinator systems"
NEW_TITLE = "Response geometry under community reorganization: richness-sensitive regimes and state-dependent branching"

DISCUSSION_ANCHOR = (
    "The robust inference is therefore not that richness is irrelevant, but that richness-sensitive regime placement coexists with strong relational contingency that cannot be reduced to an additive starting-state effect."
)
DISCUSSION_ADDITION = (
    " Equalizing the baseline mainland–island partner-arrival and partner-loss rates strengthened rather than erased this contingency: mixed individual community realizations increased from 41/96 to 70/96 and the state × community non-additive fraction increased from 17.64% to 65.61%. "
    "This control removes the baseline turnover-rate asymmetry specifically; it does not make the two scenarios identical or establish transportability beyond the declared plant–pollinator model class."
)

FIG2_ANCHOR = (
    "The stronger exact realized-richness control shifts the ensemble mean geometry to all-positive in all six matching seeds while retaining mixed individual communities."
)
FIG2_ADDITION = (
    " A separate equal-turnover control, which sets island partner arrival and loss rates to the frozen mainland baseline while retaining all other scenario differences, yields 70/96 mixed individual communities and 65.61% state × community non-additivity."
)

TABLE_ROW_ANCHOR = (
    "| Joint 240-step + trait adjustment = 0 mixed count | 75/96 | branching persists when the two existing structural sensitivities are imposed simultaneously; no new parameter values |"
)
TABLE_ROW_EQUAL_TURNOVER = (
    "| Equal turnover rates: mixed count / state × community non-additivity | 70/96 / 65.61% | baseline mainland–island partner-arrival/loss asymmetry is not required for branching; all other scenario differences retained |"
)


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"Oikos generality overlay source changed for {label}: expected one occurrence")
    return text.replace(old, new, 1)


def render_submission_manuscript() -> str:
    text = render_base_manuscript()
    text = _replace_once(text, OLD_TITLE, NEW_TITLE, "title")
    text = _replace_once(text, DISCUSSION_ANCHOR, DISCUSSION_ANCHOR + DISCUSSION_ADDITION, "Discussion generality sentences")
    text = _replace_once(text, FIG2_ANCHOR, FIG2_ANCHOR + FIG2_ADDITION, "Figure 2 caption")
    lower = text.lower()
    for token in (
        "70/96",
        "65.61%",
        "equalizing the baseline mainland–island partner-arrival and partner-loss rates",
        "does not make the two scenarios identical",
    ):
        if token.lower() not in lower:
            raise ValueError(f"equal-turnover Oikos overlay missing from manuscript: {token}")
    if "in island plant–pollinator systems" in lower.splitlines()[0].lower():
        raise ValueError("island-scoped subtitle survived Oikos title overlay")
    return text


def build_supporting_tables() -> str:
    text = build_base_tables()
    insertion = TABLE_ROW_ANCHOR + "\n" + TABLE_ROW_EQUAL_TURNOVER
    text = _replace_once(text, TABLE_ROW_ANCHOR, insertion, "Table S4 equal-turnover row")
    if TABLE_ROW_EQUAL_TURNOVER not in text:
        raise ValueError("equal-turnover Table S4 row missing")
    return text
