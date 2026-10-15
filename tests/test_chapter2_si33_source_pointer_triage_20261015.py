"""Read-only SI source-pointer manifest guards: no raw archive retrieval or simulation.

Literal filename mentions and candidate preflight provenance must never be
mistaken for full original-data admissions, independent cohorts, or DOI deposit.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SI = ROOT / "docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md"
PREFLIGHT = ROOT / "docs/deposit/chapter2_zenodo_unpublished_preflight_20261015.json"
ADDENDUM = ROOT / "docs/deposit/chapter2_single_paper_raw_scope_addendum_20261015.json"
INVENTORY = ROOT / "docs/deposit/chapter2_si33_source_pointer_triage_20261015.json"
NOTE = ROOT / "docs/deposit/CHAPTER2_SI33_SOURCE_POINTER_TRIAGE_20261015.md"
TOKEN = re.compile(r"[A-Za-z0-9_./-]+\.(?:json\.gz|tar\.gz|json|zip|tar|npz|py)(?![A-Za-z0-9_])")


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def test_current_si_has_all_thirty_three_source_pointer_rows():
    data, text = read(INVENTORY), SI.read_text(encoding="utf-8")
    found = list(re.finditer(r"^## S(\d+)\.\s*(.*)$", text, flags=re.MULTILINE))
    assert len(found) == data["sections_total"] == 33
    assert git_blob(SI) == data["si_source_git_blob"]
    assert data["source_main_commit"] == "c1b08577dd2a2432ce71df001df45a90ad0f0d74"
    assert [r["section"] for r in data["si_sections"]] == [
        f"S{i}" for i in range(1, 34)
    ]
    for k, (match, entry) in enumerate(zip(found, data["si_sections"])):
        body = text[match.start():found[k + 1].start() if k + 1 < len(found) else len(text)]
        expected = sorted(set(TOKEN.findall(body)))
        assert entry["section"] == f"S{match.group(1)}"
        assert entry["heading"] == match.group(2).strip()
        assert entry["literal_file_tokens"] == expected
        assert entry["review_packet_member_literals"] == [
            x for x in expected if x.startswith("EVIDENCE/")
        ]
        assert entry["archive_coverage_status"] == "NOT_YET_VERIFIED_FOR_FULL_SI_SECTION"
        assert entry["cross_host_independently_verified_by_this_audit"] is False
    with_tokens = [x for x in data["si_sections"] if x["literal_file_tokens"]]
    no_tokens = [x["section"] for x in data["si_sections"] if not x["literal_file_tokens"]]
    assert data["sections_with_literal_file_token"] == len(with_tokens) == 21
    assert data["sections_without_literal_file_token"] == no_tokens
    assert len(no_tokens) == 12


def test_ten_candidate_containers_retain_exact_previous_sha_and_size():
    d, old, more = read(INVENTORY), read(PREFLIGHT), read(ADDENDUM)
    assert d["preflight_git_blob"] == git_blob(PREFLIGHT)
    assert d["addendum_git_blob"] == git_blob(ADDENDUM)
    prior = [
        (x, "six_core_preflight") for x in old["six_core_packages"]
    ] + [
        (x, "prior_additional_candidate")
        for x in old["additional_documented_archives_not_yet_admitted"]
    ] + [
        (x, "new_addendum_candidate") for x in more["extra_source_candidates"]
    ]
    candidates = d["known_archive_candidates"]
    assert len(prior) == len(candidates) == 10
    assert len({x["filename"] for x in candidates}) == 10
    for (original, stage), cand in zip(prior, candidates):
        assert (cand["filename"], cand["bytes"], cand["sha256"], cand["stage"]) == (
            original["filename"], original["bytes"], original["sha256"], stage
        )
        assert re.fullmatch("[0-9a-f]{64}", cand["sha256"])
        assert cand["bytes"] > 0
    assert more["this_is_a_complete_submission_source_inventory"] is False
    assert more["deposit_status"]["remote_zenodo_draft_created"] is False


def test_only_explicit_and_bounded_candidate_hints_are_used():
    d = read(INVENTORY)
    links = [
        (row["section"], hint["filename"], hint["strength"])
        for row in d["si_sections"]
        for hint in row["known_archive_candidate_context"]
    ]
    assert links == [
        ("S5", "izu_core_functional_loss_tempo_full_20261011.zip",
         "candidate_group_correspondence_only"),
        ("S7", "completed_atom_abm_20261011.zip",
         "candidate_group_correspondence_only"),
        ("S14", "ecological_order_actual_github_38312090996.zip",
         "documented_original_cohort_candidate"),
        ("S33", "izu_core_island_demographic_stress_20261008.zip",
         "documented_original_cohort_candidate"),
    ]
    assert all(x[1] in {v["filename"] for v in d["known_archive_candidates"]}
               for x in links)
    assert d["no_original_archive_bytes_downloaded_by_this_audit"] is True
    assert d["no_external_deposit_or_doi_created_by_this_audit"] is True
    assert d["explicit_unresolved_source_mapping_required"] is True


def test_human_review_note_does_not_promote_literal_files_to_data_admission():
    t = NOTE.read_text(encoding="utf-8")
    for claim in ("21", "12", "33", "S14", "S33", "ten documented candidate",
                  "not a 21/33", "not re-computed", "not", "DOI", "520/521"):
        assert claim.lower() in t.lower()
    assert "new biological trajectories" not in t.lower()
