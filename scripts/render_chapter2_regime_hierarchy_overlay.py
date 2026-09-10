from __future__ import annotations

from scripts.render_chapter2_oikos_generality_overlay import (
    NEW_TITLE,
    build_supporting_tables as build_base_tables,
    render_submission_manuscript as render_base_manuscript,
)

RESULT_ANCHOR = (
    "Branching is therefore finite-community in the asymptotic sense, while its persistence after empty-community probability is effectively zero shows that it is not a rare-extinction or N≈2 artifact."
)
RESULT_ADDITION = (
    "\n\nA complementary prespecified system-size audit retained the headline plant response operator (`trait_adjustment=0.03`) and reused the existing six-seed ensemble. The variance hierarchy itself reversed as community sampling noise was reduced: median starting-position share rose monotonically from 2.55% at k=1 to 10.33%, 27.33%, 42.52% and 55.84% at k=2,4,8,16, whereas median community-realization share fell from 72.98% to 48.03%, 23.52%, 18.26% and 12.72%. Starting position exceeded community realization in 0/6 seeds at k=1 and k=2, but in 6/6 seeds at k=4, k=8 and k=16. Mixed-sign realizations nevertheless persisted at k=16 (28–42/96 across seeds). Thus the ordering of response determinants is itself regime dependent: realized community dominates in small stochastic communities, whereas starting state becomes the larger additive component as communities become larger and more stable under active plant adjustment."
)

DISCUSSION_ANCHOR = (
    "Deterministic mean-field therefore removes the focal branch distribution by averaging over finite realized composition, whereas second-order finite-size structure retains it over a broad intermediate regime."
)
DISCUSSION_ADDITION = (
    "\n\nAllowing plant state to respond dynamically reveals a further layer: the response hierarchy is not rank-stable across system size. In the active-adjustment audit, community realization dominated at k=1, but starting position overtook it in all six prespecified seeds by k=4 and reached a median 55.84% of total sum of squares at k=16 while community realization declined to 12.72%. The intermediate regime therefore differs from both extremes: branching remains common, yet variation is increasingly organized by where the plant starts rather than by which community realization is sampled. The numerical crossover is model-specific and is not a proposed natural threshold."
)

FIG2_ANCHOR = (
    "A separate finite-community system-size audit reduces island-like final-count CV from 0.575–0.691 at k=1 to 0.134–0.172 at k=16 while retaining 44–60/96 mixed realizations at k=16."
)
FIG2_ADDITION = (
    " With the headline trait-adjustment operator active, a complementary six-seed audit shows a rank crossover: median starting-position/community shares shift from 2.55%/72.98% at k=1 to 55.84%/12.72% at k=16, with starting position larger in 6/6 seeds from k=4 onward while 28–42/96 realizations remain mixed at k=16."
)

TABLE_ANCHOR = (
    "| Exact finite-k moments + Gaussian limit | mean-field all-positive; Gaussian mixed error 0.0689 → 0.00654 from k=1 → 16 | branch heterogeneity is finite-community asymptotically but not a rare-extinction artifact; Gaussian branch probabilities only, not a full LNA |"
)
TABLE_ROW = (
    "| Active-adjustment system-size rank crossover | median starting/community SS 2.55%/72.98% at k=1 → 55.84%/12.72% at k=16; starting > community in 6/6 seeds from k=4 | determinant ordering is regime dependent; mixed branching persists at k=16 (28–42/96); numerical crossover is model-specific |"
)


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"regime-hierarchy overlay source changed for {label}: expected one occurrence")
    return text.replace(old, new, 1)


def render_submission_manuscript() -> str:
    text = render_base_manuscript()
    text = _replace_once(text, RESULT_ANCHOR, RESULT_ANCHOR + RESULT_ADDITION, "Result 1 rank crossover")
    text = _replace_once(text, DISCUSSION_ANCHOR, DISCUSSION_ANCHOR + DISCUSSION_ADDITION, "Discussion rank crossover")
    text = _replace_once(text, FIG2_ANCHOR, FIG2_ANCHOR + FIG2_ADDITION, "Figure 2 rank crossover")
    lower = text.lower()
    for token in (
        "ordering of response determinants is itself regime dependent",
        "2.55% at k=1",
        "55.84% at k=16",
        "72.98%",
        "12.72%",
        "6/6 seeds at k=4",
        "28–42/96",
        "numerical crossover is model-specific",
    ):
        if token.lower() not in lower:
            raise ValueError(f"regime-hierarchy result missing from manuscript: {token}")
    return text


def build_supporting_tables() -> str:
    text = build_base_tables()
    text = _replace_once(text, TABLE_ANCHOR, TABLE_ANCHOR + "\n" + TABLE_ROW, "Table S4 rank crossover")
    if TABLE_ROW not in text:
        raise ValueError("rank-crossover Table S4 row missing")
    return text
