import csv
from pathlib import Path

import pytest

from paper.validate_regime_transition_registry import REGISTRY, validate


def test_committed_regime_transition_registry() -> None:
    summary = validate()
    assert summary == {
        "records": 6,
        "eligible": 4,
        "calibration": 3,
        "negative_controls": 1,
        "pending": 2,
    }


def test_unfinished_campanula_guide_cannot_enter_registry(tmp_path: Path) -> None:
    rows = list(csv.DictReader(REGISTRY.open(encoding="utf-8")))
    rows.append(
        {
            **rows[0],
            "record_id": "forbidden_guide",
            "response_family": "visible_signal",
        }
    )
    path = tmp_path / "registry.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    with pytest.raises(ValueError, match="visible-signal"):
        validate(path)
