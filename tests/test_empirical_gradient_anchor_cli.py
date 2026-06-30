from pathlib import Path
import subprocess
import sys


def test_empirical_anchor_cli_writes_templates_then_report(tmp_path: Path) -> None:
    template_dir = tmp_path / "anchors"
    subprocess.run(
        [
            sys.executable,
            "scripts/generate_empirical_anchor_report.py",
            "--write-templates",
            str(template_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    (template_dir / "population_traits.csv").write_text(
        "population_id,spot_trait_mean,spot_trait_sd,trait_n\n"
        "low,0.1,0.02,8\n"
        "high,0.7,0.03,9\n",
        encoding="utf-8",
    )
    (template_dir / "pst_fst.csv").write_text(
        "trait_name,pst,fst,critical_c_over_h2\nspot,0.4,0.1,0.3\n",
        encoding="utf-8",
    )
    (template_dir / "inbreeding_fitness.csv").write_text(
        "census_interval,selfed_mean_fitness,outcrossed_mean_fitness\npost_seed,0.3,0.6\n",
        encoding="utf-8",
    )
    (template_dir / "pollinator_availability.csv").write_text(
        "population_id,guild,detected,effort_minutes\nlow,bumblebee,false,30\nhigh,bumblebee,true,30\n",
        encoding="utf-8",
    )
    output = tmp_path / "report.md"

    subprocess.run(
        [
            sys.executable,
            "scripts/generate_empirical_anchor_report.py",
            "--input-dir",
            str(template_dir),
            "--focal-guild",
            "bumblebee",
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    rendered = output.read_text(encoding="utf-8")
    assert "# Empirical anchor report for spot-trait gradient simulation" in rendered
    assert "service_increases_with_spot_axis" in rendered
    assert "not a visit-rate estimate" in rendered
