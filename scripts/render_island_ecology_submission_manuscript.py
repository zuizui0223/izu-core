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

FOUR_ACT_PARAGRAPH = (
    "The paper therefore proceeds through four inferential acts. **Theory:** simulation defines a relational response geometry and separates regime movement, "
    "state-by-community branch identity, local filtering and downstream assurance. **Global confrontation:** that response vocabulary is carried into island research "
    "to ask whether empirical response diversity requires more than a single syndrome, followed by geography-first expansion to test whether the vocabulary saturates. "
    "**Identifiability:** a source audit asks whether the process coordinates needed to distinguish those mechanisms are jointly measured and whether the same bottleneck persists after breadth expansion. "
    "**Izu continuity-system zoom:** after the breadth stopping rule is met, one source-linked island series increases depth to separate historical-transition inference, present functional structure and downstream response propagation."
)

INTRO_STANDALONE_PARAGRAPH = (
    "The move from breadth to Izu is therefore an inferential decision rather than a geographic convenience. Once geography-first expansion stopped adding materially new mechanism states, "
    "the focal system was selected for continuity across the unresolved measurement chain. Izu links historical Campanula reproductive and floral-response evidence, repeated contemporary plant–pollinator networks, "
    "numeric pollinator functional traits and downstream reproductive-function measurements while retaining explicit population-history alternatives and important negative model-facing results. "
    "This combination permits competing explanations to be separated rather than merely illustrated; independently measured downstream phenotype is not used to tune the present mechanism."
)

FOCAL_SELECTION_STANDALONE = """## Focal-system selection after world saturation

The focal depth system was selected only after the geography-first stopping rule was met. The selection criterion was **measurement continuity across the bottleneck exposed by the world audit**, not proximity, logistical convenience, representativeness or positive agreement with the simulation.

Izu met that criterion because the same regional series contains historical Campanula reproductive and floral-response evidence (Inoue & Amano, 1986; Inoue, 1988, 1990), an explicit population-history alternative (Inoue & Kawahara, 1990; Oiki et al., 2001), repeated contemporary interaction networks, source-native numeric pollinator traits for most named taxa, and present matching and pollen-response measurements. Negative or fragile model-facing results were retained rather than used to exclude the system. The focal value is therefore mechanism discrimination within one source-linked series, not illustration by a hand-picked positive case.
"""

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
    "## Identifiability: the literature was outcome-rich but process-poor":
        "## Identifiability: the formal literature audit was outcome-rich but process-poor",
    "## Identifiability: geography-first expansion saturated before the transition contract closed":
        "## Identifiability: geography-first expansion saturated before the transition contract closed",
    "## Resolution: Izu localized the raw signed-position signal to source state and composition":
        "## Izu mechanistic zoom: raw signed-position matching localized the signal to source state and composition",
    "## Resolution: the historical signed-position predictor did not explain null-corrected matching":
        "## Izu mechanistic zoom: the historical signed-position predictor did not explain null-corrected matching",
    "## Resolution: contemporary functional diversity predicted corrected matching within Izu":
        "## Izu mechanistic zoom: contemporary functional diversity predicted corrected matching within Izu",
    "## Resolution: matching-to-pollen propagation was weaker and downstream responses branched":
        "## Izu mechanistic zoom: downstream propagation weakened and plant responses branched",
}

DISCUSSION_HEADING_REPLACEMENTS = {
    "## Response direction is relational rather than intrinsic":
        "## Theory: response direction is relational rather than intrinsic",
    "## The proximal WHY separates regime, relational branch identity and downstream propagation":
        "## Theory: the proximal mechanism separates regime, relational branch identity and downstream propagation",
    "## World confrontation establishes necessity, saturation and a measurement agenda":
        "## Global confrontation and identifiability: breadth saturates before the transition contract closes",
    "## Why Izu is the focal continuity system":
        "## Izu mechanistic zoom: continuity and falsification justify focal depth",
}

FORBIDDEN_SUBMISSION_TOKENS = (
    "At the dissertation scale",
    "preceding comparative chapter",
    "Chapter 1",
    "Chapter 2",
    "Chapter 3",
    "**Status:** active Chapter 2 scientific manuscript",
    "**Inference architecture:**",
    "**Controlling state:**",
    "## Working title",
    "zuizui0223",
    "shimahotarubukuro",
    "THESIS_CHAPTER_POSITIONING",
    "data/design/chapter2_izu_focal_system_rationale_20260906.json",
)

SPECIFIC_SI_REFERENCE_TOKENS = (
    "(Appendix)",
    "Fig. S",
    "Figure S",
    "Appendix S",
)


def _replace_exact_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"{label} changed; expected exactly one source occurrence")
    return text.replace(old, new, 1)


def _replace_paragraph_starting(text: str, start: str, new: str, label: str) -> str:
    idx = text.find(start)
    if idx < 0:
        raise ValueError(f"{label} changed; paragraph start not found")
    end = text.find("\n\n", idx)
    if end < 0:
        raise ValueError(f"{label} changed; paragraph end not found")
    return text[:idx] + new + text[end:]


def render_active_reference_list() -> str:
    text = REFERENCE_LEDGER.read_text(encoding="utf-8")
    active_heading = "## Active references\n\n"
    boundary_heading = "\n## Izu continuity-system source boundary\n"
    if text.count(active_heading) != 1 or text.count(boundary_heading) != 1:
        raise ValueError("active reference-ledger section contract changed; refuse silent reference rendering")
    body = text.split(active_heading, 1)[1].split(boundary_heading, 1)[0].strip()
    if not body:
        raise ValueError("active reference list is empty")
    return "## References\n\n" + body


def _strip_active_header(text: str) -> str:
    required_status = "**Status:** active Chapter 2 scientific manuscript — world-saturation / Izu-continuity synthesis; submission metadata still fail-closed"
    if not text.startswith("# Response geometry under community reorganization\n\n") or required_status not in text[:1600]:
        raise ValueError("active world-saturation manuscript header changed; refuse silent submission rendering")
    marker = f"## Working title\n\n**{FINAL_TITLE}**"
    if text.count(marker) != 1:
        raise ValueError("active world-saturation manuscript working title changed; refuse silent submission rendering")
    _, rest = text.split(marker, 1)
    return f"# {FINAL_TITLE}" + rest


def render_submission_manuscript(source: Path = SOURCE) -> str:
    text = source.read_text(encoding="utf-8")
    text = _strip_active_header(text)

    text = _replace_paragraph_starting(
        text,
        "The paper follows five linked questions.",
        FOUR_ACT_PARAGRAPH,
        "five-question Introduction funnel",
    )
    text = _replace_paragraph_starting(
        text,
        "The move from breadth to Izu is therefore an inferential decision, not a geographic convenience.",
        INTRO_STANDALONE_PARAGRAPH,
        "Izu continuity Introduction bridge",
    )

    focal_re = re.compile(
        r"\n## Focal-system selection after world saturation\n.*?(?=\n## Izu mechanistic-resolution zoom\n)",
        flags=re.DOTALL,
    )
    text, n_focal = focal_re.subn("\n" + FOCAL_SELECTION_STANDALONE + "\n", text, count=1)
    if n_focal != 1:
        raise ValueError("focal-system selection section changed; refuse silent submission rendering")

    # Remove dissertation routing while preserving the scientific Izu discussion.
    thesis_re = re.compile(
        r"\n## Chapter 2 closes at the continuity-system boundary\n.*?(?=\n## Limits\n)",
        flags=re.DOTALL,
    )
    text, n_removed = thesis_re.subn("\n", text, count=1)
    if n_removed != 1:
        raise ValueError("thesis continuity handoff section not found exactly once")

    text = _replace_paragraph_starting(
        text,
        "Chapter 2 therefore closes with a conditional response geometry, a world-level saturation/identifiability result and a justified continuity system for depth.",
        "The study therefore closes with a conditional response geometry, a world-level saturation/identifiability result and a justified continuity system for depth. The remaining transition-linked effectiveness-to-reproduction bridge is a prospective empirical target rather than retrospective validation. The contribution is a mechanistic coordinate system plus a sharply localized measurement contract—not a calibrated island predictor, natural-frequency estimate or ultimate historical explanation.",
        "thesis-specific conclusion routing",
    )

    for old, new in RESULT_HEADING_REPLACEMENTS.items():
        text = _replace_exact_once(text, old, new, f"Results heading: {old}")
    for old, new in DISCUSSION_HEADING_REPLACEMENTS.items():
        text = _replace_exact_once(text, old, new, f"Discussion heading: {old}")

    text = text.replace(
        "The prespecified Oshima-source bridge was unsupported (Appendix),",
        "The prespecified Oshima-source bridge was unsupported (Supporting information),",
        1,
    )

    figure1_start = "**Figure 1. Breadth-to-depth mechanistic-resolution funnel.**"
    fig_idx = text.find(figure1_start)
    if fig_idx < 0:
        raise ValueError("Figure 1 caption heading changed")
    fig_end = text.find("\n\n", fig_idx)
    if fig_end < 0:
        raise ValueError("Figure 1 caption paragraph changed")
    figure1 = (
        "**Figure 1. Four-act breadth-to-depth inference funnel.** The synthetic model defines ecological possibilities and a trajectory-conditioned interaction-kernel coordinate; "
        "the frozen comparative audit establishes response diversity and an outcome-rich/process-poor identifiability bottleneck; geography-first expansion reaches a declared saturation rule while small islands partially recover transition history; "
        "Izu is selected after saturation by measurement continuity rather than convenience or positive model fit; the Izu zoom separates historical signed-position inference from robust contemporary FDQ-to-matching structure and weaker downstream propagation; "
        "the remaining transition-linked effectiveness-to-reproduction bridge is prospective rather than a validation claim."
    )
    text = text[:fig_idx] + figure1 + text[fig_end:]

    if "\n## References\n" not in text:
        raise ValueError("reference handoff section missing")
    text = text.split("\n## References\n", 1)[0].rstrip() + "\n\n" + render_active_reference_list() + "\n"

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
        "42 research entries across 37 exact geographic labels",
        "affre & thompson, 1997",
        "feinsinger et al., 1982",
        "ægisdóttir & thórhallsdóttir, 2006",
        "philipp & adsersen, 2014",
        "andrews et al., 2022",
        "gutiérrez-flores et al., 2018",
        "response direction is therefore relational rather than intrinsic",
        "53/96",
        "partner arrival/replacement",
        "null-corrected matching",
        "measurement continuity across the bottleneck",
        "prespecified oshima-source bridge was unsupported (supporting information)",
        "## references",
    )
    missing = [token for token in required if token not in lower]
    if missing:
        raise ValueError(f"four-act continuity manuscript claim(s) disappeared from submission render: {missing}")
    if "cell-level simulation variation" in lower:
        raise ValueError("superseded nonadditivity wording survived submission render")
    if "five linked questions" in lower or "## reality:" in lower or "## resolution:" in lower:
        raise ValueError("superseded five-question labels survived the four-act submission render")
    if "hygiene decisions" in lower or "world-saturation synthesis source boundary" in lower or "value-selected breadth source boundary" in lower:
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
