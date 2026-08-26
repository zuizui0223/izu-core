import json
import zipfile
from pathlib import Path

import pytest

from scripts.build_island_ecology_submission_bundle import build_submission_bundle

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/design/island_ecology_submission_metadata_template.json"
V3 = "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V3_20260826.md"


def completed_metadata() -> dict:
    metadata = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    metadata["authors"] = [
        {
            "full_name": "Example Author",
            "affiliations": ["Example Institute, Example University, Example City, Example Country"],
            "email": "example@example.org",
            "postal_address": "Example Institute, Example City, Example Country",
        }
    ]
    metadata["corresponding_author_index"] = 0
    metadata["acknowledgements"] = "None"
    metadata["funding"] = "None"
    metadata["author_contributions"] = "Example Author conceived the study, performed the analyses and wrote the manuscript."
    metadata["inclusion_statement"] = "This study used secondary literature and simulation data and involved no new local field data collection."
    metadata["conflict_of_interest"] = "The author declares no conflict of interest."
    for key in metadata["submission_declarations"]:
        metadata["submission_declarations"][key] = True
    return metadata


def test_submission_bundle_fails_closed_on_unresolved_metadata(tmp_path: Path):
    with pytest.raises(ValueError):
        build_submission_bundle(TEMPLATE, tmp_path / "bundle.zip")


def test_submission_bundle_contains_v3_review_and_identity_separated_files(tmp_path: Path):
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text(json.dumps(completed_metadata()), encoding="utf-8")
    output = build_submission_bundle(metadata_path, tmp_path / "bundle.zip")
    assert output.exists()
    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        assert "ISLAND_ECOLOGY_TITLE_PAGE.md" in names
        assert "ISLAND_ECOLOGY_COVER_LETTER.md" in names
        assert "island_ecology_anonymous_review_archive.zip" in names
        assert "SUBMISSION_BUNDLE_MANIFEST.json" in names
        assert V3 in names
        assert "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md" not in names
        manuscript = archive.read(V3).decode("utf-8")
        assert "sign(Δ reproduction) = sign(Δ service) = sign(Δ functional opportunity)" in manuscript
        title = archive.read("ISLAND_ECOLOGY_TITLE_PAGE.md").decode("utf-8")
        assert "Example Author" in title
        nested = archive.read("island_ecology_anonymous_review_archive.zip")
        nested_path = tmp_path / "nested.zip"
        nested_path.write_bytes(nested)
        with zipfile.ZipFile(nested_path) as review:
            review_names = set(review.namelist())
            assert V3 in review_names
            assert not any("TITLE_PAGE" in name.upper() for name in review_names)
            assert not any("COVER_LETTER" in name.upper() for name in review_names)
