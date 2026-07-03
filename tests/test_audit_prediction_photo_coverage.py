import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "paper" / "audit_prediction_photo_coverage.py"


def audit_module():
    spec = importlib.util.spec_from_file_location("audit_prediction_photo_coverage", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_select_candidates_filters_to_confident_specialists(tmp_path: Path):
    source = tmp_path / "groups.csv"
    fields = ["name", "functional_group", "confidence", "n_islands", "total_occ"]
    rows = [
        {"name": "Strong", "functional_group": "specialist_bee", "confidence": "high", "n_islands": "5", "total_occ": "40"},
        {"name": "Medium", "functional_group": "specialist_bee", "confidence": "medium", "n_islands": "3", "total_occ": "10"},
        {"name": "Low", "functional_group": "specialist_bee", "confidence": "low", "n_islands": "6", "total_occ": "99"},
        {"name": "General", "functional_group": "generalist_open", "confidence": "high", "n_islands": "6", "total_occ": "99"},
    ]
    with source.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
    selected = audit_module().select_candidates(source, min_islands=3, min_total_occ=10, max_candidates=20)
    assert [row["name"] for row in selected] == ["Strong", "Medium"]
