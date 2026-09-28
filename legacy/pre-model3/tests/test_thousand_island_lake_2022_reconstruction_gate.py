from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v9_thousand_island_lake_reconstruction_gate_v1.json"
SCRIPT = ROOT / "scripts/audit_thousand_island_lake_2022_reconstruction_structure.py"


def load_script():
    scripts_dir = str(ROOT / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location("til_reconstruction_gate_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_design_forbids_spatial_temporal_cartesian_product():
    design = json.loads(DESIGN.read_text())
    boundaries = " ".join(design["hard_boundaries"]).lower()
    assert "42 x 3 site-year grid" in boundaries
    assert "never infer plant availability from visited plants" in boundaries
    assert design["target_metrics_calculated"] is False


def test_reconstruction_script_is_target_free():
    text = SCRIPT.read_text().lower()
    assert "from channel_id.external_archipelago_network" not in text
    assert "network_metrics(" not in text
    assert "interaction_shannon" not in text
    assert "morisita" not in text
    assert "predictive_envelope" not in text


def test_spatial_wide_matrix_structure_is_auditable(tmp_path):
    module = load_script()
    path = tmp_path / "all_ints_spatial.csv"
    path.write_text(
        ',"B0","S01","S48"\n'
        '"PO1_PL1",2,0,1\n'
        '"PO2_PL2",0,3,0\n',
        encoding="utf-8",
    )
    result = module.matrix_structure(path, "spatial")
    assert result["pair_code_count"] == 2
    assert result["unique_pair_code_count"] == 2
    assert result["all_pair_codes_decode_as_PO_then_PL"] is True
    assert result["network_columns"] == ["B0", "S01", "S48"]
    assert result["all_network_columns_nonnegative_integer_counts"] is True


def test_temporal_wide_matrix_structure_is_auditable(tmp_path):
    module = load_script()
    path = tmp_path / "all_ints_temporal.csv"
    path.write_text(
        ',"t2017","t2018","t2019","int"\n'
        '1,0,1,2,"PO1_PL1"\n'
        '2,3,0,0,"PO2_PL2"\n',
        encoding="utf-8",
    )
    result = module.matrix_structure(path, "temporal")
    assert result["pair_code_count"] == 2
    assert result["network_columns"] == ["t2017", "t2018", "t2019"]
    assert result["all_network_columns_nonnegative_integer_counts"] is True


def test_fractional_or_negative_counts_fail_count_semantics(tmp_path):
    module = load_script()
    path = tmp_path / "bad.csv"
    path.write_text(
        ',"B0","S01"\n'
        '"PO1_PL1",1.5,0\n'
        '"PO2_PL2",2,-1\n',
        encoding="utf-8",
    )
    result = module.matrix_structure(path, "spatial")
    assert result["all_network_columns_nonnegative_integer_counts"] is False


def test_independent_plant_opportunity_requires_plant_availability_without_pair_or_pollinator(tmp_path):
    module = load_script()
    path = tmp_path / "plant_availability.csv"
    path.write_text(
        "plant,site,flower_abundance\n"
        "PL1,S01,12\n"
        "PL2,S01,0\n",
        encoding="utf-8",
    )
    result = module.structural_candidates(path)
    assert result["long_independent_plant_opportunity_candidate"] is True


def test_visited_pair_table_is_not_independent_plant_opportunity(tmp_path):
    module = load_script()
    path = tmp_path / "visits.csv"
    path.write_text(
        "pair,site,visits\n"
        "PO1_PL1,S01,4\n"
        "PO2_PL2,S01,2\n",
        encoding="utf-8",
    )
    result = module.structural_candidates(path)
    assert not result or result.get("long_independent_plant_opportunity_candidate") is False


def test_joint_site_year_pair_candidate_requires_joint_structure(tmp_path):
    module = load_script()
    path = tmp_path / "joint.csv"
    path.write_text(
        "pair,site,year,count\n"
        "PO1_PL1,S01,2017,4\n"
        "PO2_PL2,S01,2018,2\n",
        encoding="utf-8",
    )
    result = module.structural_candidates(path)
    assert result["joint_site_year_pair_candidate"] is True
