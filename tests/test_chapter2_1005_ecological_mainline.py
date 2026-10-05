import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_1005_ecological_mainline_is_active():
    lock = json.loads(
        (ROOT / "data/design/chapter2_1005_ecological_mainline_lock_20261006.json").read_text(
            encoding="utf-8"
        )
    )
    manuscript = (ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    process = (ROOT / "docs/CHAPTER2_PROCESS_MAINLINE_20261005.md").read_text(
        encoding="utf-8"
    )

    assert lock["status"] == "active_scientific_mainline"
    assert lock["source_date"] == "2026-10-05"
    assert lock["primary_evidence"]["independent_visitor_histories"] == 64
    assert lock["primary_evidence"]["delayed_assurance_first_histories"] == 51
    assert lock["primary_evidence"]["fixed_assurance_far_investment_change_delayed"] == -0.3099
    assert lock["primary_evidence"]["assurance_evolution_interaction_delayed"] == 0.08468
    assert "sequence ≠ necessity" in readme.lower()
    assert "2026-10-05 ecological results" in process
    assert manuscript.startswith(
        "# Reproductive assurance can evolve first without causing floral attraction loss under pollinator isolation"
    )
    assert "Assurance evolution is not required for investment decline" in manuscript
    assert "Lower pollen deficit does not necessarily mean greater viable reproduction" in manuscript
