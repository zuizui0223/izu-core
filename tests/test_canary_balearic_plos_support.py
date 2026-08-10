import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


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
