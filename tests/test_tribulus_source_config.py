import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_tribulus_source_is_open_and_single_lineage_only():
    config = json.loads(
        (ROOT / "config/tribulus_zenodo_source.json").read_text(encoding="utf-8")
    )
    assert config["article_doi"] == "10.1002/ece3.9766"
    assert config["record_id"] == 7551873
    assert config["dataset_doi"] == "10.5061/dryad.h70rxwdnz"
    assert config["analysis_target"] == "Tribulus_flower_data_clean.csv"
    assert "Tribulus_flower_data_clean.csv" in config["expected_files"]
    assert config["analysis_role"].startswith("single_lineage")
    boundary = config["claim_boundary"].lower()
    assert "not a second independent cross-lineage" in boundary
    assert "not pollinator effectiveness" in boundary
