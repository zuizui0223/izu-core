import csv
import subprocess
import sys
from pathlib import Path


def test_counterfactual_validity_conditions_have_required_statuses():
    rows = list(csv.DictReader(Path("data/counterfactual_validity_conditions.csv").open(encoding="utf-8")))
    assert rows
    assert {row["status"] for row in rows} <= {"active", "partial", "blocked"}
    ids = {row["condition_id"] for row in rows}
    assert "cf_guide_after_hierarchy_loss" in ids
    assert "cf_inbreeding_cost" in ids


def test_counterfactual_validity_report_builds(tmp_path):
    output = tmp_path / "validity.md"
    subprocess.run([sys.executable, "scripts/build_counterfactual_validity_report.py", "--output", str(output)], check=True)
    text = output.read_text(encoding="utf-8")
    assert "Counterfactual validity scope" in text
    assert "cf_environment_residual" in text
