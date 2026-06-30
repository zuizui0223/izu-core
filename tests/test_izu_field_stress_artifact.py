from pathlib import Path
import subprocess
import sys


def test_field_stress_generator_writes_markdown(tmp_path: Path) -> None:
    output = tmp_path / "izu_field_stress.md"

    subprocess.run(
        [
            sys.executable,
            "scripts/generate_izu_field_stress_report.py",
            "--replicates",
            "1",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    rendered = output.read_text(encoding="utf-8")
    assert "# Virtual Izu field-misspecification stress report" in rendered
    assert "site_maternal_variation" in rendered
    assert "wind_light_detection_loss" in rendered
    assert "handling_dependent_detection_loss" in rendered
    assert "outcross_biased_unresolved" in rendered
    assert "combined_field_stress" in rendered
    assert "unique truth top" in rendered
