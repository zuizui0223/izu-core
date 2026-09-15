from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/design/chapter2_nee_initial_submission_metadata.json"

ALLOWED_REVIEW_MODELS = {"single-anonymized", "double-anonymized"}
REQUIRED_DECLARATIONS = {
    "not_published_or_under_consideration_elsewhere_except_disclosed_related_work",
    "all_authors_approve_submission",
    "all_entitled_authors_included",
    "necessary_acknowledgements_made",
    "legal_and_policy_requirements_met",
    "third_party_data_reuse_is_permitted",
}


def explicit_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(metadata: dict) -> list[str]:
    errors: list[str] = []

    if metadata.get("journal") != "Nature Ecology & Evolution":
        errors.append("journal must be Nature Ecology & Evolution")
    if metadata.get("article_type") != "Article":
        errors.append("article_type must be Article")

    review_model = metadata.get("peer_review_model")
    if review_model not in ALLOWED_REVIEW_MODELS:
        errors.append("peer_review_model must be single-anonymized or double-anonymized")

    authors = metadata.get("authors")
    if not isinstance(authors, list) or not authors:
        errors.append("authors must contain the final ordered author list")
        authors = []

    corresponding_count = 0
    for i, author in enumerate(authors, start=1):
        prefix = f"authors[{i}]"
        if not isinstance(author, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if not explicit_text(author.get("name")):
            errors.append(f"{prefix}.name is required")
        affiliations = author.get("affiliations")
        if not isinstance(affiliations, list) or not affiliations or not all(explicit_text(x) for x in affiliations):
            errors.append(f"{prefix}.affiliations must contain at least one explicit affiliation")
        if not explicit_text(author.get("email")):
            errors.append(f"{prefix}.email is required")
        if author.get("corresponding_author") is True:
            corresponding_count += 1
        elif author.get("corresponding_author") is not False:
            errors.append(f"{prefix}.corresponding_author must be explicitly true or false")

    if authors and corresponding_count != 1:
        errors.append("exactly one author must be marked corresponding_author=true")

    for field in (
        "related_manuscripts_under_consideration_or_in_press",
        "prior_discussions_with_nee_editor",
        "acknowledgements",
        "funding_statement",
        "competing_interests",
        "ethics_statement",
        "llm_use_statement",
    ):
        if not explicit_text(metadata.get(field)):
            errors.append(f"{field} requires explicit text; use 'None' where applicable")

    if metadata.get("ethics_statement_confirmed") is not True:
        errors.append("ethics_statement_confirmed must be explicitly true after author review")
    if metadata.get("llm_use_statement_confirmed") is not True:
        errors.append("llm_use_statement_confirmed must be explicitly true after author review")

    declarations = metadata.get("submission_declarations")
    if not isinstance(declarations, dict):
        errors.append("submission_declarations must be an object")
    else:
        missing = REQUIRED_DECLARATIONS - set(declarations)
        if missing:
            errors.append(f"submission_declarations missing: {sorted(missing)}")
        for key in sorted(REQUIRED_DECLARATIONS):
            if declarations.get(key) is not True:
                errors.append(f"submission_declarations.{key} must be explicitly true")

    return errors


def main(path: Path = DEFAULT) -> None:
    metadata = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(metadata)
    if errors:
        print(json.dumps({"status": "AUTHOR_INPUT_REQUIRED", "errors": errors}, indent=2, ensure_ascii=False))
        raise SystemExit(1)
    print(json.dumps({"status": "INITIAL_SUBMISSION_METADATA_READY", "authors": len(metadata["authors"])}, indent=2))


if __name__ == "__main__":
    main()
