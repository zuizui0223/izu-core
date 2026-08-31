from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METADATA = ROOT / "data/design/island_ecology_submission_metadata_template.json"
DEFAULT_TITLE_PAGE = ROOT / "dist/ISLAND_ECOLOGY_TITLE_PAGE.md"
DEFAULT_COVER_LETTER = ROOT / "dist/ISLAND_ECOLOGY_COVER_LETTER.md"
DEFAULT_SIGNIFICANCE = ROOT / "dist/OIKOS_SIGNIFICANCE_STATEMENT.md"
DEFAULT_STATEMENTS = ROOT / "dist/OIKOS_SUBMISSION_STATEMENTS.md"

REQUIRED_AUTHOR_FIELDS = ("full_name", "affiliations")
REQUIRED_TOP_LEVEL_TEXT = (
    "significance_statement",
    "significance_prior_work_context",
    "author_contributions",
    "inclusion_statement",
    "conflict_of_interest",
    "ethics_statement",
    "planned_public_repository",
    "data_availability",
)
REQUIRED_DECLARATIONS = (
    "not_published_or_under_consideration_elsewhere",
    "all_authors_approve_submission",
    "all_entitled_authors_included",
    "necessary_acknowledgements_made",
    "legal_and_policy_requirements_met",
    "third_party_data_reuse_is_permitted",
)


def load_metadata(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_metadata(metadata: dict) -> list[str]:
    errors: list[str] = []
    authors = metadata.get("authors")
    if not isinstance(authors, list) or not authors:
        errors.append("authors must contain the final ordered author list")
    else:
        for idx, author in enumerate(authors):
            if not isinstance(author, dict):
                errors.append(f"authors[{idx}] must be an object")
                continue
            for field in REQUIRED_AUTHOR_FIELDS:
                if not author.get(field):
                    errors.append(f"authors[{idx}].{field} is required")
            affiliations = author.get("affiliations")
            if affiliations and not isinstance(affiliations, list):
                errors.append(f"authors[{idx}].affiliations must be a list")

    corr = metadata.get("corresponding_author_index")
    if not isinstance(corr, int):
        errors.append("corresponding_author_index must identify one author")
    elif isinstance(authors, list) and authors and not (0 <= corr < len(authors)):
        errors.append("corresponding_author_index is outside authors")
    elif isinstance(authors, list) and authors:
        corresponding = authors[corr]
        if not corresponding.get("email"):
            errors.append("corresponding author email is required")
        if not corresponding.get("postal_address"):
            errors.append("corresponding author postal_address is required")
        if not corresponding.get("orcid"):
            errors.append("corresponding author orcid is required by Oikos at submission")

    for field in REQUIRED_TOP_LEVEL_TEXT:
        value = metadata.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} requires an explicit statement")

    for optional_explicit in ("acknowledgements", "funding"):
        value = metadata.get(optional_explicit)
        if value is None:
            errors.append(f"{optional_explicit} must be explicitly set to text or 'None'")

    declarations = metadata.get("submission_declarations", {})
    for field in REQUIRED_DECLARATIONS:
        if declarations.get(field) is not True:
            errors.append(f"submission_declarations.{field} must be explicitly true")
    return errors


def _format_author(author: dict, index: int) -> str:
    aff = ", ".join(str(x) for x in author["affiliations"])
    orcid = author.get("orcid") or "not supplied"
    return f"{index + 1}. **{author['full_name']}** — {aff}; ORCID: {orcid}"


def render_title_page(metadata: dict) -> str:
    errors = validate_metadata(metadata)
    if errors:
        raise ValueError("submission metadata incomplete:\n- " + "\n- ".join(errors))
    authors = metadata["authors"]
    corresponding = authors[metadata["corresponding_author_index"]]
    author_lines = "\n".join(_format_author(author, idx) for idx, author in enumerate(authors))
    return f"""# Title page — {metadata['journal']}\n\n## Title\n\n**{metadata['manuscript_title']}**\n\n## Authors and affiliations\n\n{author_lines}\n\n## Corresponding author\n\n**{corresponding['full_name']}**  \n{corresponding['email']}  \n{corresponding['postal_address']}  \nORCID: {corresponding['orcid']}\n"""


def render_significance_statement(metadata: dict) -> str:
    errors = validate_metadata(metadata)
    if errors:
        raise ValueError("submission metadata incomplete:\n- " + "\n- ".join(errors))
    return (
        f"# Significance statement — {metadata['journal']}\n\n"
        f"{metadata['significance_statement'].strip()}\n\n"
        "## Relation to previous work\n\n"
        f"{metadata['significance_prior_work_context'].strip()}\n"
    )


def render_data_archiving_statement(metadata: dict) -> str:
    errors = validate_metadata(metadata)
    if errors:
        raise ValueError("submission metadata incomplete:\n- " + "\n- ".join(errors))
    return (
        "We confirm that data and custom code supporting an accepted version of this article will be deposited "
        f"in {metadata['planned_public_repository'].strip()} and made publicly accessible in accordance with Oikos policy.\n\n"
        f"{metadata['data_availability'].strip()}\n"
    )


def render_submission_statements(metadata: dict) -> str:
    errors = validate_metadata(metadata)
    if errors:
        raise ValueError("submission metadata incomplete:\n- " + "\n- ".join(errors))
    return f"""# Submission statements — {metadata['journal']}\n\n## Data archiving statement\n\n{render_data_archiving_statement(metadata)}\n## Conflict of interest\n\n{metadata['conflict_of_interest']}\n\n## Ethics statement\n\n{metadata['ethics_statement']}\n\n## Funding\n\n{metadata['funding']}\n\n## Acknowledgements\n\n{metadata['acknowledgements']}\n\n## Inclusion / EDI statement\n\n{metadata['inclusion_statement']}\n\n## Author contributions\n\n{metadata['author_contributions']}\n"""


def render_cover_letter(metadata: dict) -> str:
    errors = validate_metadata(metadata)
    if errors:
        raise ValueError("submission metadata incomplete:\n- " + "\n- ".join(errors))
    corresponding = metadata["authors"][metadata["corresponding_author_index"]]
    return f"""Dear Editors,\n\nPlease consider our {metadata['article_type']}, **“{metadata['manuscript_title']},”** for publication in *{metadata['journal']}*.\n\nThe same broad ecological perturbation can produce opposite biological responses, yet average effects rarely identify the state–community relationship that determines response direction. We address this problem with a theory-first mechanistic funnel built around community reorganization rather than a universal island trajectory.\n\nThe manuscript defines the exact community-interaction-kernel coordinate embedded in a frozen matching model and separates roles that are commonly conflated: turnover reshapes the response regime; starting state is evaluated relative to the community actually realized; local filtering can reallocate branch identity; and downstream reproductive assurance mainly modifies response magnitude. Across prespecified seed and time-horizon sensitivities, realized community remained the largest additive component, starting state alone remained weak, and state-by-community nonadditivity remained consequential. Mixed geometry also persisted when trait adjustment was set to zero and when mainland-like and island-like initial pollinator richness was equalized, showing that the relational response architecture is not an artifact of either trait adjustment or richness reduction alone.\n\nThe paper then confronts this response vocabulary with empirical island ecology without converting retrospective examples into validation. The source-audited literature is outcome-rich but process-poor: response outcomes are directly measured in 21 of 25 entries, whereas partner arrival/replacement is directly measured in only 2 of 25, and no entry supplies the full outcome-independent state–community–context–outcome contract needed for formal external prediction. A focal Izu analysis then increases mechanistic resolution: the frozen source-state projection explains raw realized matching but not null-corrected matching, localizing the present signal to source state plus background community composition rather than additional non-random partner sorting.\n\nWe believe *{metadata['journal']}* is the appropriate venue because the contribution is not a regional extension of island pollination patterns. It is a general ecological account of why response direction can be relational under community reorganization, coupled to an explicit process-measurement bottleneck and a worked empirical resolution step. The accompanying significance statement explains both the general contribution and how the manuscript builds on relevant prior work by the submitting authors/coauthors and by the wider field.\n\nWe preserve strict claim boundaries: design-space frequencies and thresholds are not interpreted as natural prevalence or calibrated ecological thresholds; the comparative inventory is not validation coverage; and the Izu analysis is not used to infer causal floral evolution or beyond-composition partner sorting. Data and custom analysis code are prepared for reviewer inspection at first submission through the anonymous review package, with accepted materials planned for public deposition in {metadata['planned_public_repository']}.\n\nWe confirm that this manuscript has not been published and is not under consideration elsewhere, that all authors approve submission, and that all required acknowledgements and permissions have been made.\n\nThank you for considering this manuscript.\n\nSincerely,\n\n{corresponding['full_name']}\n{', '.join(corresponding['affiliations'])}\n{corresponding['email']}\nORCID: {corresponding['orcid']}\n"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--title-page", type=Path, default=DEFAULT_TITLE_PAGE)
    parser.add_argument("--cover-letter", type=Path, default=DEFAULT_COVER_LETTER)
    parser.add_argument("--significance", type=Path, default=DEFAULT_SIGNIFICANCE)
    parser.add_argument("--statements", type=Path, default=DEFAULT_STATEMENTS)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    metadata = load_metadata(args.metadata)
    errors = validate_metadata(metadata)
    if errors:
        raise SystemExit("submission metadata incomplete:\n- " + "\n- ".join(errors))
    if args.validate_only:
        print("submission metadata complete")
        return
    for output in (args.title_page, args.cover_letter, args.significance, args.statements):
        output.parent.mkdir(parents=True, exist_ok=True)
    args.title_page.write_text(render_title_page(metadata), encoding="utf-8")
    args.cover_letter.write_text(render_cover_letter(metadata), encoding="utf-8")
    args.significance.write_text(render_significance_statement(metadata), encoding="utf-8")
    args.statements.write_text(render_submission_statements(metadata), encoding="utf-8")
    print(args.title_page)
    print(args.cover_letter)
    print(args.significance)
    print(args.statements)


if __name__ == "__main__":
    main()
