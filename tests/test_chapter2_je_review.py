from pathlib import Path

import scripts.build_chapter2_je_review as builder
import scripts.verify_chapter2_je_review as verifier

ROOT = Path(__file__).resolve().parents[1]


def test_je_review_package_routes_three_submission_figures():
    assert builder.MAIN == {
        "Figure1.pdf": "figure1_return_components.pdf",
        "Figure2.pdf": "figure2_confirmed_sequence.pdf",
        "Figure3.pdf": "figure3_fixed_assurance.pdf",
    }
    assert len(builder.MAIN) == 3


def test_je_review_uses_confirmatory_history_level_evidence():
    required = {
        "data/results/chapter2_1005_confirmatory_replication_20261006.json",
        "data/results/chapter2_1005_confirmatory_primary_sequence_history_20261006.csv",
        "data/results/chapter2_1005_confirmatory_primary_fixed_assurance_history_20261006.csv",
        "data/results/chapter2_1005_confirmatory_artifact_manifest_20261006.json",
        "data/design/chapter2_1005_confirmatory_replication_20261006.json",
    }
    assert required.issubset(set(builder.INPUTS))
    for rel in required:
        assert (ROOT / rel).is_file(), rel


def test_je_review_redraws_only_submission_specific_figures():
    assert verifier.MODULES == [
        "scripts.figure_chapter2_je_return_components",
        "scripts.figure_chapter2_je_sequence",
        "scripts.figure_chapter2_je_fixed_assurance",
    ]


def test_je_review_keeps_public_doi_pending():
    source = (ROOT / "scripts/build_chapter2_je_review.py").read_text(encoding="utf-8")
    assert '"public_doi_deposited":False' in source
