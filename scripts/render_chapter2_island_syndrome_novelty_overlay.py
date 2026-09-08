from __future__ import annotations

from scripts.render_chapter2_oikos_generality_overlay import (
    NEW_TITLE,
    build_supporting_tables as build_base_supporting_tables,
    render_submission_manuscript as render_base_manuscript,
)

ABSTRACT_OLD = (
    "Together, these results support a hierarchical view of island plant response: richness helps position the coarse opportunity regime, composition interacting with plant state retains branch contingency, and downstream biological responses propagate only contingently. "
    "The analysis does not establish one matched historical partner transition across all layers; that missing coordinate bounds causal interpretation rather than defining the study objective."
)
ABSTRACT_NEW = (
    "Together, these results recast island syndromes as ensemble-level regime shifts rather than deterministic lineage-level trait rules: richness positions the coarse opportunity regime, while realized composition interacting with plant state produces finite-community response branches. "
    "The unresolved matched historical transition bounds causal interpretation rather than this mechanism."
)

INTRO_ANCHOR = (
    "A single directional island syndrome can therefore obscure the response architecture that generates heterogeneous outcomes."
)
INTRO_ADDITION = (
    " Previous work has therefore established heterogeneity; the unresolved problem is how a coherent island-level tendency can coexist with opposing lineage-level responses. "
    "We treat that coexistence as a scale-dependent response architecture in which syndrome-like shifts can emerge in the ensemble while finite realized communities expose individual lineages to different response branches."
)

DISCUSSION_ANCHOR = (
    "Together, the three results support a hierarchical response architecture under community reorganization."
)
DISCUSSION_ADDITION = (
    " They also change how an island syndrome can be interpreted: as an ensemble-level shift in the distribution of possible responses rather than a deterministic lineage-level trait rule. "
    "In this view, insularity can generate a coherent mean tendency while finite realized communities expose lineages to opposing branches; the syndrome is the shifted regime, not a universal phenotype."
)


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"island-syndrome novelty overlay source changed for {label}: expected one occurrence")
    return text.replace(old, new, 1)


def render_submission_manuscript() -> str:
    text = render_base_manuscript()
    text = _replace_once(text, ABSTRACT_OLD, ABSTRACT_NEW, "abstract conclusion")
    text = _replace_once(text, INTRO_ANCHOR, INTRO_ANCHOR + INTRO_ADDITION, "Introduction novelty gap")
    text = _replace_once(text, DISCUSSION_ANCHOR, DISCUSSION_ANCHOR + DISCUSSION_ADDITION, "Discussion island-syndrome implication")
    lower = text.lower()
    required = (
        "ensemble-level regime shifts rather than deterministic lineage-level trait rules",
        "how a coherent island-level tendency can coexist with opposing lineage-level responses",
        "the syndrome is the shifted regime, not a universal phenotype",
    )
    for token in required:
        if token not in lower:
            raise ValueError(f"island-syndrome novelty framing missing from manuscript: {token}")
    if NEW_TITLE not in text:
        raise ValueError("Oikos title was lost in novelty overlay")
    return text


def build_supporting_tables() -> str:
    return build_base_supporting_tables()
