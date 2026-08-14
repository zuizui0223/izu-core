import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
LOCKED_PACKAGE_SHA256 = "d1d8d0a372c1717ed0f5b73203018474ec5a59446192d9339dddad3c012f7f6f"


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ACQUIRE = load_module(
    "canary_balearic_plos_acquire",
    "scripts/acquire_canary_balearic_plos_support.py",
)
AUDIT = load_module(
    "canary_balearic_plos_audit",
    "scripts/audit_canary_balearic_plos_support.py",
)


def test_payload_and_logical_id_guards():
    assert ACQUIRE.payload_kind(b"PK\x03\x04payload") == "zip"
    assert (
        ACQUIRE.payload_kind(bytes.fromhex("d0cf11e0a1b11ae1") + b"payload")
        == "ole_doc"
    )
    assert ACQUIRE.payload_kind(b"<!doctype html><html>") == "html"
    assert ACQUIRE.logical_id_from_name("pone.0150824.s003.doc") == "s003"
    assert ACQUIRE.logical_id_from_name("unrelated.doc") is None


def test_archive_member_rejects_traversal():
    assert ACQUIRE.safe_archive_member("nested/pone.s001.doc") == Path(
        "nested/pone.s001.doc"
    )
    with pytest.raises(ValueError, match="unsafe archive"):
        ACQUIRE.safe_archive_member("../escape.doc")


def test_direct_candidates_include_open_repository_routes():
    urls = ACQUIRE.direct_candidates(
        "10.1371/journal.pone.0150824", "PMC4777429", "s001"
    )
    assert len(urls) == 3
    assert any("journals.plos.org" in url for url in urls)
    assert any("pmc.ncbi.nlm.nih.gov" in url for url in urls)
    assert all("s001" in url for url in urls)


def test_community_codes_require_exact_tokens():
    text = "SB CM CB LC but SBCM is not another code token"
    counts = AUDIT.count_codes(text)
    assert counts == {"SB": 1, "CM": 1, "CB": 1, "LC": 1}


def test_pairwise_header_requires_plant_visitor_and_weight():
    assert AUDIT.has_pairwise_header(
        ["community\tplant species\tflower visitor\tflower visitation rate"]
    ) is True
    assert AUDIT.has_pairwise_header(
        ["zone\tplant species\tlinkage level\tselectiveness"]
    ) is False


def test_numeric_matrix_blocks_require_consecutive_rows():
    lines = [
        "plant\tv1\tv2\tv3",
        "p1\t1\t0\t2",
        "p2\t0\t3\t0",
        "p3\t1\t1\t0",
    ]
    rows = AUDIT.table_like_lines(lines)
    blocks = AUDIT.numeric_matrix_blocks(rows)
    assert len(blocks) == 1
    assert blocks[0]["n_rows"] == 3


def test_derived_table_does_not_become_raw_pair_header():
    lines = [
        "zone\tplant code\tlinkage level\td prime\tspecificity",
        "SB\tP01\t8\t0.2\tgeneralized",
        "CM\tP02\t2\t0.8\tspecialized",
        "CB\tP03\t5\t0.4\topportunistic",
        "LC\tP04\t3\t0.7\tselective",
    ]
    assert AUDIT.has_pairwise_header(lines) is False
    present = {
        code
        for code, count in AUDIT.count_codes("\n".join(lines)).items()
        if count
    }
    assert present == {"SB", "CM", "CB", "LC"}


def test_picture_only_antiword_output_triggers_render_fallback():
    assert AUDIT.needs_render_fallback("Table S3a\n[pic]\nTable S3b\n[pic]")
    assert not AUDIT.needs_render_fallback(
        "Table S1\nZone Family Plant species sp.cod L d-prime specificity"
    )


def test_split_vector_table_header_is_recognized_as_derived_summary():
    text = """
    Functional Rank Evenness of
    Specificity Zone sp.cod Month L
    richness abundance abundances
    Generalized CB las.sp 1 (January) 3 3 3.00 0.314
    """
    assert AUDIT.is_derived_partner_summary(text) is True
    assert AUDIT.has_pairwise_header(text.splitlines()) is False


def test_species_code_crosswalk_retains_source_mismatches():
    plant = set(AUDIT.species_codes("cak.mar teu.dun myo.ten"))
    visitor = set(AUDIT.species_codes("las.sp api.mel cam.fea"))
    derived = set(AUDIT.species_codes("las.sp api.mel ana.pro"))
    summary = AUDIT.overlap_summary(derived, visitor)
    assert plant.isdisjoint(visitor)
    assert summary["n_shared_codes"] == 2
    assert summary["query_only_codes"] == ["ana.pro"]
    assert summary["reference_only_codes"] == ["cam.fea"]


def test_package_lock_survives_transport_failure_without_claiming_redownload():
    record = ACQUIRE.reconcile_package_record(
        None,
        {"locked_package_sha256": LOCKED_PACKAGE_SHA256},
    )
    assert record == {
        "status": "not_recovered_this_run_locked_checksum_retained",
        "sha256": LOCKED_PACKAGE_SHA256,
        "provenance": "repository_locked_prior_successful_package",
    }


def test_package_lock_rejects_checksum_drift():
    with pytest.raises(ValueError, match="checksum drift"):
        ACQUIRE.reconcile_package_record(
            {"status": "downloaded", "sha256": "0" * 64},
            {"locked_package_sha256": LOCKED_PACKAGE_SHA256},
        )
