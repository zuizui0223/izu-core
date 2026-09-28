import subprocess
import sys
from pathlib import Path


def test_template_validates_and_reports(tmp_path):
    output = tmp_path / "guide_spot.md"
    subprocess.run([
        sys.executable,
        "scripts/validate_island_guide_spot_channel.py",
        "--output",
        str(output),
    ], check=True)
    text = output.read_text(encoding="utf-8")
    assert "Island guide spot channel report" in text
    assert "Informative rows: 0" in text


def test_require_informative_blocks_template_only_table(tmp_path):
    output = tmp_path / "guide_spot.md"
    result = subprocess.run([
        sys.executable,
        "scripts/validate_island_guide_spot_channel.py",
        "--output",
        str(output),
        "--require-informative",
    ], text=True, capture_output=True)
    assert result.returncode != 0
    assert "no informative spot_value rows present" in result.stderr
