import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/results/chapter2_empirical_emulation_negative_audit_20261003.json"
LOCK = ROOT / "data/design/chapter2_vnext_syndrome_integration_lock_20261002.json"


def test_empirical_emulation_sequence_is_closed_negative() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["status"] == "closed_negative_empirical_emulation_sequence"
    assert len(audit["attempts"]) == 4
    assert [a["name"] for a in audit["attempts"]] == [
        "Model3R-v1",
        "Model3R-v2",
        "Model3R-v3-assembly",
        "Model3E-v1",
    ]
    assert audit["attempts"][0]["passes"] == 0
    assert audit["attempts"][1]["passes"] == 0
    assert audit["attempts"][2]["passes"] == 0
    assert audit["attempts"][3]["heldout_successes"] == 0
    assert audit["integrated_interpretation"]["quantitative_chapter1_emulation_established"] is False


def test_model3r_model3e_exploration_is_not_on_active_surface() -> None:
    forbidden = (
        "scripts/model3e_empirical.py",
        "scripts/run_chapter2_model3e_empirical_screening.py",
        "scripts/run_chapter2_model3e_heldout_validation.py",
        "data/design/chapter2_model3e_chapter1_empirical_targets_20261003.json",
        "data/design/chapter2_model3e_empirical_screening_20261003.json",
        "data/results/chapter2_model3e_h1_h3_screening_20261003.json",
        "data/results/chapter2_model3e_heldout_H2_H4_20261003.json",
        "docs/CHAPTER2_MODEL3E_EMPIRICAL_EMULATION_V1_20261003.md",
    )
    for rel in forbidden:
        assert not (ROOT / rel).exists(), rel


def test_vnext_lock_treats_external_emulation_as_nonrequired_provenance() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    boundary = lock["empirical_emulation_boundary"]
    assert boundary["status"] == "nonrequired_external_emulation_provenance"
    assert boundary["chapter2_success_criterion"] is False
    assert boundary["quantitative_external_coefficient_reproduction_required"] is False
    assert boundary["audit"] == "docs/CHAPTER2_EMPIRICAL_EMULATION_NEGATIVE_AUDIT_20261003.md"
