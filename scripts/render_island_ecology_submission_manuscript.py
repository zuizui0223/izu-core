from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md"
REFERENCE_LEDGER = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md"
DEFAULT_OUTPUT = ROOT / "dist/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUBMISSION_CLEAN.md"

FINAL_TITLE = (
    "Response geometry under community reorganization: from ecological possibility "
    "to mechanistic resolution in island plant–pollinator systems"
)

INTRO_THESIS_PARAGRAPH = (
    "That audit motivates, rather than competes with, the Izu focal analysis. Izu was not selected as an outcome-independent "
    "winner from a global ranking. It is the island series in which source floral state, source and island pollinator composition, "
    "numeric pollinator traits, interaction structure, raw realized matching and null-corrected matching can be connected at higher "
    "resolution. The contrast between raw and corrected matching attacks a specific mechanistic distinction: background "
    "community-composition structure versus additional within-community non-random partner sorting. Chapter 2 ends at this "
    "distinction and at the measurements still required to connect matching to reproduction; Chapter 3 is the next measurement "
    "stage, not causal validation of the present model."
)

INTRO_STANDALONE_PARAGRAPH = (
    "That audit motivates, rather than competes with, the Izu focal analysis. Izu was not selected as an outcome-independent "
    "winner from a global ranking. It is the island series in which source floral state, source and island pollinator composition, "
    "numeric pollinator traits, interaction structure, raw realized matching and null-corrected matching can be connected at higher "
    "resolution. The contrast between raw and corrected matching attacks a specific mechanistic distinction: background "
    "community-composition structure versus additional within-community non-random partner sorting. The analysis ends at this "
    "distinction and at the prospective measurements still required to connect matching to reproductive propagation."
)

FIVE_QUESTION_PARAGRAPH = (
    "The paper follows five linked questions. **Possibility:** can the same broad interaction reorganization generate opposite biological responses? "
    "**Mechanism:** what controls response sign and branch identity? **Reality:** does empirical island ecology require a response vocabulary richer than one syndrome? "
    "**Identifiability:** do existing studies jointly measure the state, community, local context and comparable plant outcome required to distinguish those mechanisms? "
    "**Resolution:** what becomes distinguishable when analysis moves from global breadth to one data-rich island series?"
)

FOUR_ACT_PARAGRAPH = (
    "The paper therefore proceeds through four inferential acts. **Theory:** simulation defines a relational response geometry and separates regime movement, "
    "state-by-community branch identity, local filtering and downstream assurance. **Global confrontation:** that response vocabulary is carried into the island literature "
    "to ask whether empirical response diversity requires more than a single syndrome; empirical systems are not assigned to synthetic regime labels. "
    "**Identifiability:** a source audit asks whether the process coordinates needed to distinguish those mechanisms are jointly measured. "
    "**Izu mechanistic-resolution zoom:** the focal island series then increases depth to separate source-state/background-composition structure from additional within-community sorting."
)

REFERENCE_HANDOFF_PARAGRAPH = (
    "Use the source-audited active reference ledger in `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_REFERENCE_LEDGER_20260827.md`. "
    "Hiraiwa & Ushimaru (2017, 2024) are the empirical sources for the Izu triangulation. "
    "Affre & Thompson (1997), Feinsinger et al. (1982) and Ægisdóttir & Thórhallsdóttir (2006) are cited only for the three value-selected breadth roles above. "
    "Other external-system references remain in the comparative-grounding supplement and are not presented as validation coverage."
)

THESIS_SECTION_RE = re.compile(
    r"\n## Chapter 2 hands a measurement contract to Chapter 3\n.*?(?=\n## Limits\n)",
    flags=re.DOTALL,
)

FORBIDDEN_SUBMISSION_TOKENS = (
    "At the dissertation scale",
    "preceding comparative chapter",
    "Chapter 1",
    "Chapter 2",
    "Chapter 3",
    "Campanula microdonta",
    "**Status:** active Chapter 2 scientific manuscript",
    "**Inference architecture:**",
    "**Controlling state:**",
    "## Working title",
)

SPECIFIC_SI_REFERENCE_TOKENS = (
    "(Appendix)",
    "Fig. S",
    "Figure S",
    "Appendix S",
)

RESULT_HEADING_REPLACEMENTS = {
    "## Possibility: the same reorganization generated opposite responses":
        "## Theory — possibility: the same reorganization generated opposite responses",
    "## Mechanism: turnover moved the system among response regimes":
        "## Theory — regime structure: turnover moved the system among response regimes",
    "## Mechanism: response direction was relational rather than a stable state-only effect":
        "## Theory — relational branch identity: response direction was not a stable state-only effect",
    "## Mechanism: local filtering reallocated branches asymmetrically":
        "## Theory — branch allocation: local filtering reallocated branches asymmetrically",
    "## Mechanism: downstream assurance attenuated magnitude without rescuing sign":
        "## Theory — downstream propagation: assurance attenuated magnitude without rescuing sign",
    "## Reality: the comparative universe required more than one response state":
        "## Global confrontation: real island systems required more than one response state",
    "## Resolution: Izu localized the raw signal to source state and composition":
        "## Izu mechanistic zoom: raw matching localized the signal to source state and composition",
    "## Resolution: Izu null-corrected matching did not support beyond-composition sorting":
        "## Izu mechanistic zoom: null-corrected matching did not support beyond-composition sorting",
}

DISCUSSION_HEADING_REPLACEMENTS = {
    "## Response direction is relational rather than intrinsic":
        "## Theory: response direction is relational rather than intrinsic",
    "## The proximal WHY separates regime, relational branch identity and downstream propagation":
        "## Theory: the proximal mechanism separates regime, relational branch identity and downstream propagation",
    "## World confrontation establishes necessity and a measurement agenda":
        "## Global confrontation and identifiability: empirical diversity exposes a process-measurement bottleneck",
    "## Izu increases resolution and localizes the present signal":
        "## Izu mechanistic zoom: increasing resolution localizes the present signal",
}


def _replace_exact_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"{label} changed; expected exactly one source occurrence")
    return text.replace(old, new, 1)


def render_active_reference_list() -> str:
    text = REFERENCE_LEDGER.read_text(encoding="utf-8")
    active_heading = "## Active references\n\n"
    boundary_heading = "\n## Izu empirical triangulation source boundary\n"
    if text.count(active_heading) != 1 or text.count(boundary_heading) != 1:
        raise ValueError("active reference-ledger section contract changed; refuse silent reference rendering")
    body = text.split(active_heading, 1)[1].split(boundary_heading, 1)[0].strip()
    if not body:
        raise ValueError("active reference list is empty")
    return "## References\n\n" + body


def render_submission_manuscript(source: Path = SOURCE) -> str:
    text = source.read_text(encoding="utf-8")

    working_title_block = (
        "# Response geometry under community reorganization\n\n"
        "**Status:** active Chapter 2 scientific manuscript — relational-robustness revision; submission metadata still fail-closed\n"
        "**Updated:** 2026-08-31\n"
        "**Inference architecture:** model possibilities → world confrontation → identifiability bottleneck → focal Izu mechanistic-resolution zoom\n"
        "**Controlling state:** `docs/CHAPTER2_CANONICAL_STORY_20260827.md`, `docs/CHAPTER2_RELATIONAL_ROBUSTNESS_CORRECTION_20260831.md`, `data/results/chapter2_scientific_gate_decision_frozen_20260827.json`, `data/results/chapter2_relational_robustness_audit_frozen_20260831.json`\n\n"
        "## Working title\n\n"
        f"**{FINAL_TITLE}**"
    )
    if working_title_block not in text:
        raise ValueError("active relational manuscript header changed; refuse silent submission rendering")
    text = text.replace(working_title_block, f"# {FINAL_TITLE}", 1)

    text = _replace_exact_once(
        text,
        FIVE_QUESTION_PARAGRAPH,
        FOUR_ACT_PARAGRAPH,
        "five-question Introduction funnel",
    )

    if INTRO_THESIS_PARAGRAPH not in text:
        raise ValueError("thesis-specific Introduction bridge changed; refuse silent submission rendering")
    text = text.replace(INTRO_THESIS_PARAGRAPH, INTRO_STANDALONE_PARAGRAPH, 1)

    text, n_removed = THESIS_SECTION_RE.subn("\n", text, count=1)
    if n_removed != 1:
        raise ValueError("thesis handoff section not found exactly once")

    text = text.replace(
        "the remaining effectiveness-to-reproduction contract is handed to Chapter 3 without validation claims.",
        "the remaining effectiveness-to-reproduction contract is retained as a prospective measurement target without validation claims.",
        1,
    )

    for old, new in RESULT_HEADING_REPLACEMENTS.items():
        text = _replace_exact_once(text, old, new, f"Results heading: {old}")
    for old, new in DISCUSSION_HEADING_REPLACEMENTS.items():
        text = _replace_exact_once(text, old, new, f"Discussion heading: {old}")

    text = _replace_exact_once(
        text,
        "**Figure 1. Breadth-to-depth mechanistic-resolution funnel.**",
        "**Figure 1. Four-act breadth-to-depth inference funnel.**",
        "Figure 1 caption heading",
    )

    # Oikos requires generic main-text references to Supporting information rather than
    # subsection- or appendix-specific references.
    text = text.replace(
        "The prespecified Oshima-source bridge was unsupported (Appendix),",
        "The prespecified Oshima-source bridge was unsupported (Supporting information),",
        1,
    )

    # Oikos initial-submission guidance requires the reference list inside the blinded main text.
    text = _replace_exact_once(
        text,
        f"## References\n\n{REFERENCE_HANDOFF_PARAGRAPH}",
        render_active_reference_list(),
        "reference-list handoff",
    )

    for token in FORBIDDEN_SUBMISSION_TOKENS:
        if token.lower() in text.lower():
            raise ValueError(f"submission manuscript still contains internal token: {token}")
    for token in SPECIFIC_SI_REFERENCE_TOKENS:
        if token.lower() in text.lower():
            raise ValueError(f"submission manuscript contains a specific Supporting information reference: {token}")

    lower = text.lower()
    required = (
        "the paper therefore proceeds through four inferential acts",
        "## theory — possibility:",
        "## global confrontation:",
        "## identifiability:",
        "## izu mechanistic zoom:",
        "response direction is therefore relational rather than intrinsic",
        "53/96",
        "partner arrival/replacement",
        "null-corrected matching",
        "prespecified oshima-source bridge was unsupported (supporting information)",
        "## references",
        "affre, l. & thompson, j.d. (1997)",
        "feinsinger, p., wolfe, j.a. & swarm, l.a. (1982)",
        "ægisdóttir, h.h. & thórhallsdóttir, t.e. (2006)",
    )
    missing = [token for token in required if token not in lower]
    if missing:
        raise ValueError(f"four-act relational manuscript claim(s) disappeared from submission render: {missing}")
    if "cell-level simulation variation" in lower:
        raise ValueError("superseded nonadditivity wording survived submission render")
    if "five linked questions" in lower or "## reality:" in lower or "## resolution:" in lower:
        raise ValueError("superseded five-question labels survived the four-act submission render")
    if "value-selected breadth source boundary" in lower or "hygiene decisions" in lower:
        raise ValueError("reference-ledger audit metadata leaked into submission manuscript")

    return text.rstrip() + "\n"


def render_to_path(output: Path = DEFAULT_OUTPUT) -> Path:
    text = render_submission_manuscript()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(render_to_path(args.output))


if __name__ == "__main__":
    main()
