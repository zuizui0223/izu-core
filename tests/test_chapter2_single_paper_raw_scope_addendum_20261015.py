"""Read-only current single-paper source-coverage integrity; never deposits data."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "docs/deposit/chapter2_zenodo_unpublished_preflight_20261015.json"
ADDENDUM = ROOT / "docs/deposit/chapter2_single_paper_raw_scope_addendum_20261015.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_original_six_core_preflight_preserved_as_incomplete():
    old = read(PARENT)
    assert old["six_core_file_count"] == 6
    assert old["six_core_bytes"] == 1_691_637_982
    assert old["ready_to_upload_or_publish"] is False
    assert old["external_draft_created"] is False
    assert len(old["additional_documented_archives_not_yet_admitted"]) == 2
    record = old["record"]
    assert record["ordered_creators"] is None
    assert record["data_license"] is None
    assert record["code_license"] is None


def test_new_q3_q4_source_candidates_are_sha_pinned_not_double_counted():
    preflight, add = read(PARENT), read(ADDENDUM)
    existing = {
        x["filename"] for x in preflight["six_core_packages"]
    } | {
        x["filename"] for x in preflight["additional_documented_archives_not_yet_admitted"]
    }
    added = add["extra_source_candidates"]
    assert len(existing) == 8 and len(added) == 2
    assert add["parent_six_core_package_count"] == 6
    assert add["parent_existing_additional_candidate_count"] == 2
    assert add["possible_known_candidates_after_addendum"] == 10
    assert add["this_is_a_complete_submission_source_inventory"] is False
    assert not any(x["filename"] in existing for x in added)
    assert len({x["filename"] for x in added}) == 2
    assert all(
        len(x["sha256"]) == 64 and x["bytes"] > 0
        and x["already_in_parent_six_or_two_extra"] is False
        and x["externally_deposited_and_crosshost_verified"] is False
        for x in added
    )

    q3 = next(x for x in added if x["paper_role"].startswith("Q3"))
    access = read(ROOT / "data/results/directional_access_20261013/READOUT.json")
    loss = read(ROOT / "data/results/low_allele_loss_20261014/extracted/READOUT.json")
    assert q3["original_cohort_count"] == access["cases"] == loss["cases"] == 2304
    assert q3["sha256"] == access["outer_sha256"] == loss["original_outer_sha256"]
    assert q3["bytes"] == 251_663_558
    assert q3["filename"] in (
        ROOT / "data/results/directional_access_20261013/README.md"
    ).read_text(encoding="utf-8")
    assert q3["filename"] in (
        ROOT / "data/results/low_allele_loss_20261014/README.md"
    ).read_text(encoding="utf-8")
    assert access["excluded_before_fixation"] == 703
    assert loss["direction_counts"]["favouring_needed"] == 315

    q4 = next(x for x in added if x["paper_role"].startswith("Q4"))
    official = read(ROOT / "data/results/chapter2_island_demographic_independent32_20261008.json")
    replay = read(ROOT / "data/results/chapter2_island_demographic_independent32_replay_receipt_20261013.json")
    assert q4["original_cohort_count"] == official["independent_histories"] == 32
    assert q4["filename"] == official["archive"]["file"] == replay["original_archive"]["name"]
    assert q4["sha256"] == official["archive"]["sha256"] == replay["original_archive"]["sha256"]
    assert q4["bytes"] == replay["original_archive"]["bytes"] == 335_015
    assert official["predeclared_pooled_primary"]["mean"] == 0.1083984375
    assert replay["validation"]["all_eight_biological_projection_hashes_exact"] is True


def test_main_manuscript_si_and_deposit_boundary_agree():
    add = read(ADDENDUM)
    route = read(ROOT / "data/design/chapter2_one_paper_route_20261010.json")
    main = (ROOT / route["active_manuscript"]).read_text(encoding="utf-8")
    si = (ROOT / "docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md").read_text(
        encoding="utf-8"
    )
    assert route["active_manuscript_count"] == 1
    assert "## Q3 —" in main and "## Q4 —" in main
    assert "+0.1084 [0.0654,0.1514]" in main
    assert "S33" in main
    assert "## S33. Independent 32-history" in si
    assert add["active_manuscript"] == route["active_manuscript"]
    gate = add["deposit_status"]
    assert gate["remote_zenodo_draft_created"] is False
    assert gate["bytes_uploaded_by_this_audit"] == 0
    assert gate["license_selected"] is False
    assert gate["ordered_creators_approved"] is False
    assert gate["external_version_or_doi_verified"] is False
    assert gate["fixed_b48_private_provider_safety_stop_remains"] is True
