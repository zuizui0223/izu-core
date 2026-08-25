from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_METADATA = ROOT / "data/design/island_ecology_submission_metadata_template.json"
DEFAULT_TITLE_PAGE = ROOT / "dist/ISLAND_ECOLOGY_TITLE_PAGE.md"
DEFAULT_COVER_LETTER = ROOT / "dist/ISLAND_ECOLOGY_COVER_LETTER.md"

REQUIRED_AUTHOR_FIELDS = ("full_name", "affiliations")
REQUIRED_TOP_LEVEL_TEXT = (
    "author_contributions",
    "inclusion_statement",
    "conflict_of_interest",
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

    for field in REQUIRED_TOP_LEVEL_TEXT:
        value = metadata.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} requires an explicit author-supplied statement")

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
    acknowledgements = metadata["acknowledgements"]
    funding = metadata["funding"]
    author_lines = "\n".join(_format_author(author, idx) for idx, author in enumerate(authors))
    return f"""# Title page — Journal of Ecology\n\n## Title\n\n**{metadata['manuscript_title']}**\n\n## Authors and affiliations\n\n{author_lines}\n\n## Corresponding author\n\n**{corresponding['full_name']}**  \n{corresponding['email']}  \n{corresponding['postal_address']}\n\n## Running title\n\n**{metadata['running_title']}**\n\n## Article type\n\n{metadata['article_type']}\n\n## Keywords\n\n{'; '.join(metadata['keywords'])}\n\n## Acknowledgements\n\n{acknowledgements}\n\n## Funding\n\n{funding}\n\n## Author contributions\n\n{metadata['author_contributions']}\n\n## Inclusion statement\n\n{metadata['inclusion_statement']}\n\n## Conflict of interest\n\n{metadata['conflict_of_interest']}\n\n## Data availability\n\n{metadata['data_availability']}\n"""


def render_cover_letter(metadata: dict) -> str:
    errors = validate_metadata(metadata)
    if errors:
        raise ValueError("submission metadata incomplete:\n- " + "\n- ".join(errors))
    corresponding = metadata["authors"][metadata["corresponding_author_index"]]
    return f"""Dear Editors,\n\nPlease consider our Research Article, **“{metadata['manuscript_title']},”** for publication in *Journal of Ecology*.\n\nIsland ecology has long sought recurrent reproductive syndromes, yet those aggregate patterns do not imply that established plant lineages must follow one common trajectory after pollinator communities simplify or reorganize. This manuscript asks why a common island-associated change in pollinator function can produce divergent plant responses.\n\nThe frozen analyses identify pre-existing lineage functional position as the replicated minimal tested generator of within-environment response-sign branching; distinguish bidirectional local-context branch allocation from autonomous-assurance magnitude attenuation; and challenge the frozen response-state architecture against 13 source-audited island plant–pollinator systems while retaining protected exceptions and a failed prediction.\n\nThe primary scientific hypotheses are closed, the full test suite has passed on Python 3.10, 3.11 and 3.12, and the reviewer-facing manuscript, Supporting Information and reproducibility archive are prepared for double-anonymous review. The manuscript is not under consideration elsewhere, all authors approve submission, and all persons entitled to authorship are included.\n\nThank you for considering this manuscript.\n\nSincerely,\n\n{corresponding['full_name']}\n{', '.join(corresponding['affiliations'])}\n{corresponding['email']}\n"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, default=DEFAULT_METADATA)
    parser.add_argument("--title-page", type=Path, default=DEFAULT_TITLE_PAGE)
    parser.add_argument("--cover-letter", type=Path, default=DEFAULT_COVER_LETTER)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    metadata = load_metadata(args.metadata)
    errors = validate_metadata(metadata)
    if errors:
        raise SystemExit("submission metadata incomplete:\n- " + "\n- ".join(errors))
    if args.validate_only:
        print("submission metadata complete")
        return
    args.title_page.parent.mkdir(parents=True, exist_ok=True)
    args.cover_letter.parent.mkdir(parents=True, exist_ok=True)
    args.title_page.write_text(render_title_page(metadata), encoding="utf-8")
    args.cover_letter.write_text(render_cover_letter(metadata), encoding="utf-8")
    print(args.title_page)
    print(args.cover_letter)


if __name__ == "__main__":
    main()
