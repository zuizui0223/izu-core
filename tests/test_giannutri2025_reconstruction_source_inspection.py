from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/extract_giannutri2025_daily_network_reconstruction_spec.py"


def test_reconstruction_source_inspection_is_checksum_locked_and_metric_free():
    text = SCRIPT.read_text()
    assert "b1eae37f3cada984dcbe439c75806c39" in text
    assert "a8b6a0acaa7a5082264d93f5ab01067d6fc79ab1a202d8ff06fd3b76eed79a39" in text
    assert "SOURCE_RANGES = ((150, 350),)" in text
    assert "network_metrics" not in text
    assert "interaction_shannon" not in text
    assert "mean_plant_niche_overlap" not in text
    assert '"target_metrics_calculated": False' in text
