import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mutation_history_mainline_is_consistent():
    lock = json.loads(
        (ROOT / "data/design/chapter2_mutation_history_mainline_lock_20261006.json").read_text(
            encoding="utf-8"
        )
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    manuscript = (ROOT / "docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md").read_text(
        encoding="utf-8"
    )
    process = (ROOT / "docs/CHAPTER2_PROCESS_MAINLINE_20261005.md").read_text(
        encoding="utf-8"
    )

    assert lock["status"] == "active_scientific_mainline"
    assert lock["central_claim"] == "Evolutionary memory is not equivalent to evolutionary arrest."
    assert "CHAPTER2_MUTATION_HISTORY_MAINLINE_20261006.md" in readme
    assert "Evolutionary memory after pollinator isolation does not imply evolutionary arrest" in manuscript
    assert "CHAPTER2_MUTATION_HISTORY_MAINLINE_20261006.md" in manuscript
    assert "no longer the paper-level" in process
    assert "irreversible evolution" in lock["excluded_claims"]
    assert "alternative stable attractors" in lock["excluded_claims"]
