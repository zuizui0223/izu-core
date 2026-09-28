import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "results" / "balearic_malva_effectiveness_summary.json"


def load_result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_source_files_are_checksum_locked():
    data = load_result()
    assert data["source_files"]["Fruit and seed set.csv"]["sha256"] == "946de8875630762e9f7b90d54cdaef9087e46d80f2eb59cb2fc4a31a186a9595"
    assert data["source_files"]["FVR.csv"]["sha256"] == "f2c57f07fd03dded229dff57fb6f84ad62c121b347c57e69596fa8d8cf53a4f9"


def test_real_data_scale_is_preserved():
    data = load_result()
    assert data["scale"]["visitor_event_rows"] == 83
    assert data["scale"]["treatment_rows"] == 78
    assert data["scale"]["treatment_codes"] == ["TA", "TC", "TEA", "TEL"]


def test_quantity_and_treatment_outcomes_remain_separate():
    data = load_result()
    visitors = data["quantitative_component"]["by_visitor_class"]
    assert visitors["insect"]["visits"] == 198.0
    assert visitors["bird"]["visits"] == 15.0
    assert visitors["lizard"]["visits"] == 8.0
    treatments = data["qualitative_component"]["by_treatment"]
    assert treatments["control_open"]["weighted_fruit_set"] == 152 / 210
    assert treatments["autogamy_all_pollinators_excluded"]["weighted_fruit_set"] == 129 / 201


def test_autogamy_is_direct_but_incomplete_reproductive_assurance_context():
    data = load_result()["reproductive_assurance_context"]
    assert data["autogamy_weighted_fruit_set"] > 0.6
    assert data["autogamy_weighted_fruit_set"] < data["control_weighted_fruit_set"]
    assert abs(data["autogamy_to_control_ratio"] - 0.8866849960722702) < 1e-12


def test_claim_boundary_blocks_izu_transport():
    boundary = load_result()["claim_boundary"]
    assert "not numerically transported" in boundary
    assert "reproductive-assurance evidence" in boundary
