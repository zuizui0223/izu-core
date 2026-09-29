from __future__ import annotations

import copy
import json
from pathlib import Path

from scripts.validate_chapter2_nee_initial_submission_metadata import validate

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/design/chapter2_nee_initial_submission_metadata.json"


def load_template() -> dict:
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


def test_template_is_fail_closed_until_author_confirmation() -> None:
    errors = validate(load_template())
    joined = "\n".join(errors)
    assert "peer_review_model" in joined
    assert "corresponding_author" in joined
    assert "related_manuscripts_under_consideration_or_in_press" in joined
    assert "prior_discussions_with_nee_editor" in joined
    assert "competing_interests" in joined
    assert "ethics_statement_confirmed" in joined
    assert "llm_use_statement_confirmed" in joined
    assert "all_authors_approve_submission" in joined


def test_orcid_is_not_an_initial_submission_blocker() -> None:
    metadata = ready_metadata()
    metadata["authors"][0]["orcid"] = ""
    assert validate(metadata) == []


def test_ready_metadata_passes() -> None:
    assert validate(ready_metadata()) == []


def ready_metadata() -> dict:
    metadata = copy.deepcopy(load_template())
    metadata["peer_review_model"] = "single-anonymized"
    metadata["authors"][0]["corresponding_author"] = True
    metadata["related_manuscripts_under_consideration_or_in_press"] = "None"
    metadata["prior_discussions_with_nee_editor"] = "None"
    metadata["competing_interests"] = "The authors declare no competing interests."
    metadata["ethics_statement_confirmed"] = True
    metadata["llm_use_statement_confirmed"] = True
    for key in metadata["submission_declarations"]:
        metadata["submission_declarations"][key] = True
    metadata["status"] = "INITIAL_SUBMISSION_METADATA_READY"
    return metadata
