from __future__ import annotations

from scripts.generate_chapter2_manuscript_tables import build as build_base_tables
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript as render_base_manuscript

NEW_TITLE = "Response geometry under community reorganization: richness-sensitive regimes and state-dependent branching"

TABLE_ROW_ANCHOR = (
    "| Joint 240-step + trait adjustment = 0 mixed count | 75/96 | branching persists when the two existing structural sensitivities are imposed simultaneously; no new parameter values |"
)
TABLE_ROW_EQUAL_TURNOVER = (
    "| Equal turnover rates: mixed count / state × community non-additivity | 70/96 / 65.61% | baseline mainland–island partner-arrival/loss asymmetry is not required for branching; all other scenario differences retained |"
)
TABLE_ROW_SYSTEM_SIZE = (
    "| Finite-community system-size pooling, k=1 → 16 | island CV 0.575–0.691 → 0.134–0.172; mixed at k=16 44–60/96 | finite-community sampling variance is reduced strongly, but branching persists; zero-trait-adjustment diagnostic, not an exact mean-field limit |"
)
TABLE_ROW_GAUSSIAN_LIMIT = (
    "| Exact finite-k moments + Gaussian limit | mean-field all-positive; Gaussian mixed error 0.0689 → 0.00654 from k=1 → 16 | branch heterogeneity is finite-community asymptotically but not a rare-extinction artifact; Gaussian branch probabilities only, not a full LNA |"
)
TABLE_ROW_RANK_CROSSOVER = (
    "| Active-adjustment system-size rank crossover | median starting/community SS 2.55%/72.98% at k=1 → 55.84%/12.72% at k=16; starting > community in 6/6 seeds from k=4 | determinant ordering is regime dependent; mixed branching persists at k=16 (28–42/96); numerical crossover is model-specific |"
)


def render_submission_manuscript() -> str:
    """Return the already-integrated canonical Chapter 2 manuscript.

    Historical overlay logic used literal replacements on an older empirical
    three-act source.  The active manuscript now owns the final scientific
    narrative, so this layer only validates the submission-facing claim lock.
    """
    text = render_base_manuscript()
    first_line = text.splitlines()[0]
    if NEW_TITLE not in first_line:
        raise ValueError("canonical Oikos title missing from active manuscript")

    lower = text.lower()
    required = (
        "ensemble-level regime shifts rather than deterministic lineage-level trait rules",
        "how a coherent island-level tendency can coexist with opposing lineage-level responses",
        "scale-dependent response architecture",
        "dominant source of response variation need not be fixed",
        "the syndrome is therefore the shifted response regime and its variance architecture",
        "equalizing the baseline mainland–island partner-arrival and partner-loss rates",
        "does not make the two scenarios identical",
        "finite-community stochastic formulation",
        "deterministic mean-field reduction would average over community-realization variation",
        "44–60/96",
        "0.575–0.691",
        "0.134–0.172",
        "deterministic mean-field kernel contrast was all-positive",
        "minimum contrast 0.0208",
        "absolute error fell from 0.0689 at `k=1` to 0.00654 at `k=16`",
        "not presented as an exact fokker–planck or full linear-noise solution",
        "the ordering of response determinants is itself regime dependent",
        "2.55% at `k=1`",
        "55.84% at `k=16`",
        "72.98%",
        "12.72%",
        "6/6 seeds at `k=4`",
        "28–42/96",
        "the numerical crossover is model-specific",
        "optional future validation programme",
    )
    for token in required:
        if token.lower() not in lower:
            raise ValueError(f"Oikos canonical manuscript missing claim-lock token: {token}")
    return text


def build_supporting_tables() -> str:
    text = build_base_tables()
    rows = (
        TABLE_ROW_EQUAL_TURNOVER,
        TABLE_ROW_SYSTEM_SIZE,
        TABLE_ROW_GAUSSIAN_LIMIT,
        TABLE_ROW_RANK_CROSSOVER,
    )
    if TABLE_ROW_RANK_CROSSOVER in text:
        return text
    if TABLE_ROW_ANCHOR not in text:
        raise ValueError("Table S4 structural-generality insertion anchor missing")
    insertion = TABLE_ROW_ANCHOR + "\n" + "\n".join(rows)
    return text.replace(TABLE_ROW_ANCHOR, insertion, 1)
