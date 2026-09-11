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

    if metadata.get("ethics_statement_confirmed") is not True:
        errors.append("ethics_statement_confirmed must be explicitly true after author review")

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
    contributions = metadata.get("author_contributions")
    if not isinstance(contributions, str) or not contributions.strip():
        contributions = "CRediT roles will be supplied if a revised submission is invited, as required by Oikos."
    return f"""# Submission statements — {metadata['journal']}\n\n## Data archiving statement\n\n{render_data_archiving_statement(metadata)}\n## Conflict of interest\n\n{metadata['conflict_of_interest']}\n\n## Ethics statement\n\n{metadata['ethics_statement']}\n\n## Funding\n\n{metadata['funding']}\n\n## Acknowledgements\n\n{metadata['acknowledgements']}\n\n## Inclusion / EDI statement\n\n{metadata['inclusion_statement']}\n\n## Author contributions\n\n{contributions}\n"""


def render_cover_letter(metadata: dict) -> str:
    errors = validate_metadata(metadata)
    if errors:
        raise ValueError("submission metadata incomplete:\n- " + "\n- ".join(errors))
    corresponding = metadata["authors"][metadata["corresponding_author_index"]]
    return f"""Dear Editors,\n\nPlease consider our {metadata['article_type']}, **“{metadata['manuscript_title']},”** for publication in *{metadata['journal']}*.\n\nEcological syndromes are often summarized by one directional mean response, even when individual lineages can respond in opposite directions. We address this problem with a frozen plant–pollinator model that separates two operations that are usually collapsed: coarse placement of the ensemble response regime and allocation of lineage-level response branches within that regime.\n\nThe first result is that exact stepwise control of realized pollinator richness changes the ensemble mean response geometry but does not remove substantial branch contingency. The second is that the dominant source of response variation is not fixed. Across a prespecified finite-community system-size audit, realized community composition dominates in small stochastic systems, whereas plant starting state gains relative importance as community sampling stabilizes; under active plant adjustment the additive ordering reverses across the declared k sequence while mixed branching remains. Exact finite-k moments further show that branching disappears only in the deterministic mean-field limit. The numerical crossover is explicitly model-specific and is not interpreted as a natural field threshold.\n\nLocal filtering and reproductive assurance occupy downstream positions in the same architecture: filtering can reallocate branches bidirectionally but asymmetrically, whereas assurance changes response magnitude without sign rescue in the tested envelope. World and Izu evidence are used to establish biological plausibility and to define the historical measurement ceiling, not to calibrate synthetic k or to claim that the model has already been demonstrated as a historical natural causal chain. The prospective Izu same-block visitor–effectiveness–dependency–seed design is retained as optional future falsification rather than a completion requirement for the present paper.\n\nWe believe *{metadata['journal']}* is an appropriate venue because the contribution is a general ecological account of how ensemble-level syndromes can coexist with lineage-level branching and how the hierarchy of response determinants can itself change across finite-community regimes. The accompanying significance statement explains both the general contribution and how the manuscript builds on relevant prior work by the submitting authors/coauthors and by the wider field.\n\nWe preserve strict claim boundaries: synthetic branch frequencies do not estimate natural prevalence; the crossover near k=4 is not a natural threshold; visitor richness and Hill diversity are not treated as literal synthetic k; retrospective island systems are not presented as validation coverage; and present-day Izu associations are not used to identify historical pollinator causation. Data and custom analysis code are prepared for reviewer inspection through the anonymous review package, with accepted materials planned for public deposition in {metadata['planned_public_repository']}.\n\nWe confirm that this manuscript has not been published and is not under consideration elsewhere, that all authors approve submission, and that all required acknowledgements and permissions have been made.\n\nThank you for considering this manuscript.\n\nSincerely,\n\n{corresponding['full_name']}\n{', '.join(corresponding['affiliations'])}\n{corresponding['email']}\nORCID: {corresponding['orcid']}\n"""


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
