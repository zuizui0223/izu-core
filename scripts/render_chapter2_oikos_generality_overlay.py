from __future__ import annotations

from scripts.generate_chapter2_manuscript_tables import build as build_base_tables
from scripts.render_chapter2_realized_richness_reframe import render_submission_manuscript as render_base_manuscript

OLD_TITLE = "Response geometry under community reorganization: from ecological possibility to mechanistic resolution in island plant–pollinator systems"
NEW_TITLE = "Response geometry under community reorganization: richness-sensitive regimes and state-dependent branching"

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

METHODS_ANCHOR = (
    "The synthetic plant coordinate is standardized to [0,1] and is not identified with a named empirical floral trait. Synthetic sign transitions, variance shares, realization frequencies and time horizons are design diagnostics rather than calibrated ecological thresholds or population parameters."
)
METHODS_ADDITION = (
    " The finite-community stochastic formulation was retained because variation among realized partner communities is itself a focal response component. Conditional on a realized pollinator trajectory, plant-state motion is deterministic, so the 21 starting positions sample the conditional flow map rather than interacting plant agents. A deterministic mean-field reduction would average over community-realization variation by construction; the present model is therefore a finite-community Markov process coupled to deterministic plant-state dynamics, not a contrast between a stochastic ABM and an inherently deterministic PDE. The zero-trait-adjustment limit was additionally analyzed by exact terminal count and kernel moments; only the branch-class probability was approximated with a multivariate Gaussian, so this audit is not presented as an exact Fokker–Planck or full linear-noise solution."
)

RESULT_SIZE_ANCHOR = (
    "Realized richness differences therefore help position the ensemble mean regime, but they do not explain away response branching across realized community compositions."
)
RESULT_SIZE_ADDITION = (
    "\n\nA prespecified system-size audit then reduced finite-community sampling without changing the per-copy Markov process. At zero trait adjustment, we pooled k={1,2,4,8,16} independent copies of each mainland-like and island-like community before evaluating the same mean-match service function. Across the six prespecified seeds, the island-like final-community coefficient of variation fell from 0.575–0.691 at k=1 to 0.134–0.172 at k=16, and empty final island-like communities fell from 7.3–13.5% to 0%. The additive community-realization share likewise declined from 51.4–67.3% to 20.3–34.5%. Mixed individual response geometry nevertheless remained in 44–60/96 realizations at k=16, with state × community non-additivity still 50.6–65.4%. Thus finite-community sampling contributes materially to realization variance but does not by itself generate response branching over the audited system-size range."
    "\n\nAn exact finite-k moment analysis of the same zero-trait-adjustment submodel resolved the asymptote. The deterministic mean-field kernel contrast was all-positive across all 21 starting states (minimum contrast 0.0208), so mixed branching must vanish as system size tends to infinity. A multivariate Gaussian approximation using the exact finite-k kernel mean and covariance increasingly matched the pooled six-seed ABM mixed fraction: absolute error fell from 0.0689 at k=1 to 0.00654 at k=16. Branching is therefore finite-community in the asymptotic sense, while its persistence after empty-community probability is effectively zero shows that it is not a rare-extinction or N≈2 artifact."
)

DISCUSSION_ANCHOR = (
    "The robust inference is therefore not that richness is irrelevant, but that richness-sensitive regime placement coexists with strong relational contingency that cannot be reduced to an additive starting-state effect."
)
DISCUSSION_ADDITION = (
    " Equalizing the baseline mainland–island partner-arrival and partner-loss rates strengthened rather than erased this contingency: mixed individual community realizations increased from 41/96 to 70/96 and the state × community non-additive fraction increased from 17.64% to 65.61%. "
    "This control removes the baseline turnover-rate asymmetry specifically; it does not make the two scenarios identical or establish transportability beyond the declared plant–pollinator model class."
    "\n\nThe system-size audit separates the need to represent finite communities from the stronger claim that branching is merely finite-N noise. Pooling independent copies sharply reduced count variation, empty-community events and the additive community-realization share, yet mixed response geometry and large relative state × community non-additivity persisted at k=16. This supports the finite-community formulation for quantifying realization heterogeneity while showing that the branching result is not reducible to small-N extinction or sampling noise over the audited range."
    "\n\nThe exact-moment/Gaussian limit analysis sharpens that statement further. The zero-adjustment deterministic mean-field contrast is all-positive, so branch heterogeneity is ultimately a finite-community composition-realization phenomenon; however, the Gaussian approximation already reproduces the ABM mixed fraction closely at k=16, when empty island-like communities are effectively absent. Deterministic mean-field therefore removes the focal branch distribution by averaging over finite realized composition, whereas second-order finite-size structure retains it over a broad intermediate regime."
)

DISCUSSION_SYNDROME_ANCHOR = (
    "Together, the three results support a hierarchical response architecture under community reorganization."
)
DISCUSSION_SYNDROME_ADDITION = (
    " They also change how an island syndrome can be interpreted: as an ensemble-level shift in the distribution of possible responses rather than a deterministic lineage-level trait rule. "
    "In this view, insularity can generate a coherent mean tendency while finite realized communities expose lineages to opposing branches; the syndrome is the shifted regime, not a universal phenotype."
)

FIG2_ANCHOR = (
    "The stronger exact realized-richness control shifts the ensemble mean geometry to all-positive in all six matching seeds while retaining mixed individual communities."
)
FIG2_ADDITION = (
    " A separate equal-turnover control, which sets island partner arrival and loss rates to the frozen mainland baseline while retaining all other scenario differences, yields 70/96 mixed individual communities and 65.61% state × community non-additivity. A separate finite-community system-size audit reduces island-like final-count CV from 0.575–0.691 at k=1 to 0.134–0.172 at k=16 while retaining 44–60/96 mixed realizations at k=16."
)

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


def _replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"Oikos generality overlay source changed for {label}: expected one occurrence")
    return text.replace(old, new, 1)


def render_submission_manuscript() -> str:
    text = render_base_manuscript()
    text = _replace_once(text, OLD_TITLE, NEW_TITLE, "title")
    text = _replace_once(text, ABSTRACT_OLD, ABSTRACT_NEW, "abstract island-syndrome novelty")
    text = _replace_once(text, INTRO_ANCHOR, INTRO_ANCHOR + INTRO_ADDITION, "Introduction novelty gap")
    text = _replace_once(text, METHODS_ANCHOR, METHODS_ANCHOR + METHODS_ADDITION, "finite-community model rationale")
    text = _replace_once(text, RESULT_SIZE_ANCHOR, RESULT_SIZE_ANCHOR + RESULT_SIZE_ADDITION, "finite-community system-size result")
    text = _replace_once(text, DISCUSSION_ANCHOR, DISCUSSION_ANCHOR + DISCUSSION_ADDITION, "Discussion generality sentences")
    text = _replace_once(text, DISCUSSION_SYNDROME_ANCHOR, DISCUSSION_SYNDROME_ANCHOR + DISCUSSION_SYNDROME_ADDITION, "Discussion island-syndrome implication")
    text = _replace_once(text, FIG2_ANCHOR, FIG2_ANCHOR + FIG2_ADDITION, "Figure 2 caption")
    lower = text.lower()
    for token in (
        "70/96",
        "65.61%",
        "equalizing the baseline mainland–island partner-arrival and partner-loss rates",
        "does not make the two scenarios identical",
        "finite-community stochastic formulation",
        "44–60/96",
        "0.134–0.172",
        "deterministic mean-field kernel contrast was all-positive",
        "0.00654",
        "not presented as an exact fokker–planck or full linear-noise solution",
        "ensemble-level regime shifts rather than deterministic lineage-level trait rules",
        "how a coherent island-level tendency can coexist with opposing lineage-level responses",
        "the syndrome is the shifted regime, not a universal phenotype",
    ):
        if token.lower() not in lower:
            raise ValueError(f"Oikos generality overlay missing from manuscript: {token}")
    if "in island plant–pollinator systems" in lower.splitlines()[0].lower():
        raise ValueError("island-scoped subtitle survived Oikos title overlay")
    return text


def build_supporting_tables() -> str:
    text = build_base_tables()
    insertion = (
        TABLE_ROW_ANCHOR
        + "\n"
        + TABLE_ROW_EQUAL_TURNOVER
        + "\n"
        + TABLE_ROW_SYSTEM_SIZE
        + "\n"
        + TABLE_ROW_GAUSSIAN_LIMIT
    )
    text = _replace_once(text, TABLE_ROW_ANCHOR, insertion, "Table S4 structural-generality rows")
    for row in (TABLE_ROW_EQUAL_TURNOVER, TABLE_ROW_SYSTEM_SIZE, TABLE_ROW_GAUSSIAN_LIMIT):
        if row not in text:
            raise ValueError("structural-generality Table S4 row missing")
    return text
