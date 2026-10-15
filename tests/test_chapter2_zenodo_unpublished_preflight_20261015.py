"""Frozen offline Zenodo proposal must never imply a publication or raw upload."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.verify_chapter2_zenodo_unpublished_preflight_20261015 import (
    RECORD,
    ROOT,
    validate_record,
    validate_repo,
)


def proposal():
    return json.loads((ROOT / RECORD).read_text(encoding="utf-8"))


def test_frozen_receipts_and_six_package_totals():
    result = validate_repo()
    assert result["status"] == "PASS_READONLY_PREPARED_METADATA_NO_REMOTE_DRAFT"
    assert result["core_files"] == 6
    assert result["core_bytes"] == 1_691_637_982
    assert result["additional_source_candidates"] == 2
    assert result["eight_known_bytes_if_included"] == 2_845_283_074
    assert result["private_backup_coverage"] == "520/521"
    assert result["external_zenodo_draft_created"] is False
    assert result["doi_assigned"] is False
    assert result["complete_paper_source_inventory"] is False


@pytest.mark.parametrize("field,value", [
    ("external_draft_created", True),
    ("external_uploads_performed", True),
    ("doi_reserved", True),
    ("published", True),
    ("ready_to_upload_or_publish", True),
])
def test_reject_unapproved_remote_actions(field, value):
    d = copy.deepcopy(proposal())
    d[field] = value
    with pytest.raises(ValueError, match="unapproved"):
        validate_record(d)


@pytest.mark.parametrize("field,value", [
    ("ordered_creators", ["Unapproved Author"]),
    ("data_license", "cc-by-4.0"),
    ("access_or_embargo_choice", "public"),
])
def test_no_invented_author_licenses_or_access(field, value):
    d = copy.deepcopy(proposal())
    d["record"][field] = value
    with pytest.raises(ValueError, match="approval-required"):
        validate_record(d)


def test_preservation_safety_and_source_identity_are_not_overwritten():
    d = copy.deepcopy(proposal())
    d["demographic_external_private_copy_verified"] = "521/521"
    with pytest.raises(ValueError, match="520/521"):
        validate_record(d)
    d = copy.deepcopy(proposal())
    d["six_core_packages"][2]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="tar identity"):
        validate_repo(record=d)
