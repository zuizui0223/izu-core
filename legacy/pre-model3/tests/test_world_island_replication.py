import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/world_island_replication_summary.json"


def test_world_island_replication_regenerates_and_preserves_claim_boundary():
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/analyze_world_island_replication.py")],
        cwd=ROOT,
        check=True,
    )
    result = json.loads(RESULT.read_text())
    assert result["n_systems"] == 8
    assert result["n_ocean_basin_labels"] >= 6
    assert result["n_direct_or_reproductively_linked_systems"] == 7
    assert result["n_explicit_no_limitation_counterexamples"] == 1
    assert result["n_architecture_macroclasses"] == 4
    assert result["architecture_macroclass_counts"] == {
        "complementary_or_redundant_generalism": 2,
        "concentrated_dependency": 2,
        "novel_partner_replacement": 2,
        "species_specific_mosaic": 2,
    }
    assert result["hypothesis_assessment"]["H_architecture_divergence"] == "supported"
    assert result["hypothesis_assessment"]["H_universal_single_syndrome"] == "contradicted_by_screen"
    assert "not a meta-analysis" in result["claim_boundary"]
    assert "global prevalence" in result["claim_boundary"]
