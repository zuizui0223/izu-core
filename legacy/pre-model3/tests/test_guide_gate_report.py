import csv
import subprocess
import sys
from pathlib import Path


def test_gate_matrix_status_values_are_declared():
    rows = list(csv.DictReader(Path("data/guide_loss_required_channels.csv").open(encoding="utf-8")))
    assert rows
    assert {row["current_status"] for row in rows} <= {"locked", "partial", "blocked"}
    ids = {row["channel_id"] for row in rows}
    assert "island_resolved_guide_spot" in ids
    assert "visitor_frequency" in ids


def test_gate_report_builder_runs(tmp_path):
    output = tmp_path / "gate.md"
    subprocess.run([sys.executable, "scripts/build_guide_gate_report.py", "--output", str(output)], check=True)
    text = output.read_text(encoding="utf-8")
    assert "Guide gate report" in text
    assert "blocked" in text
