import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "analyze_galapagos_source_networks.py"
SPEC = importlib.util.spec_from_file_location("galapagos_analysis", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def long_record(path: Path):
    return {
        "file": str(path),
        "sheet": None,
        "delimiter": ",",
        "role_matches": {
            "island": ["island"],
            "plant": ["plant species"],
            "pollinator": ["pollinator species"],
            "interaction_weight": ["visit count"],
        },
        "long_edge_list_candidate": True,
    }


def matrix_record(path: Path, label: str):
    return {
        "file": str(path),
        "sheet": None,
        "source_label": label,
        "matrix_orientation": "plants_by_pollinators",
        "analysis_admissible_matrix": True,
    }


def test_long_edge_table_builds_multiple_island_networks(tmp_path: Path):
    path = tmp_path / "edges.csv"
    path.write_text(
        "island,plant species,pollinator species,visit count\n"
        "Santa Cruz,P1,B1,3\n"
        "Santa Cruz,P2,B2,2\n"
        "San Cristobal,P1,B1,1\n"
        "San Cristobal,P1,B3,4\n",
        encoding="utf-8",
    )
    networks = MODULE.parse_long_edge_table(long_record(path))
    assert set(networks) == {"Santa Cruz", "San Cristobal"}
    metrics = [{"island": island, **MODULE.network_metrics(network)} for island, network in networks.items()]
    assert all(row["total_interaction_weight"] > 0 for row in metrics)
    assert all(row["total_interaction_weight"] == row["total_visitation_rate"] for row in metrics)


def test_oriented_wide_matrix_is_admitted_and_unresolved_label_is_blocked(tmp_path: Path):
    path = tmp_path / "Santa_Cruz.csv"
    path.write_text(
        "plant species,B1,B2,B3\nP1,1,0,2\nP2,0,3,0\n",
        encoding="utf-8",
    )
    label, network = MODULE.parse_oriented_matrix(matrix_record(path, "Santa Cruz"))
    assert label == "Santa_Cruz"
    assert network.plant_names == ("P1", "P2")
    assert network.pollinator_names == ("B1", "B2", "B3")

    generic = tmp_path / "network.csv"
    generic.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    try:
        MODULE.parse_oriented_matrix(matrix_record(generic, "network"))
    except ValueError as error:
        assert "label unresolved" in str(error)
    else:
        raise AssertionError("generic matrix label should remain blocked")


def test_pairwise_metrics_retain_shared_plant_turnover(tmp_path: Path):
    first = tmp_path / "A.csv"
    second = tmp_path / "B.csv"
    first.write_text("plant species,X,Y,Z\nP1,4,0,0\nP2,0,2,0\n", encoding="utf-8")
    second.write_text("plant species,X,Y,Z\nP1,0,0,4\nP3,0,1,0\n", encoding="utf-8")
    networks = {
        "A": MODULE.parse_oriented_matrix(matrix_record(first, "A"))[1],
        "B": MODULE.parse_oriented_matrix(matrix_record(second, "B"))[1],
    }
    pairs, contrasts = MODULE.pairwise_metrics(networks)
    assert len(pairs) == 1
    assert pairs[0]["n_shared_plants"] == 1
    assert {row["plant_name"] for row in contrasts} == {"P1"}


def test_covariate_links_are_descriptive_and_require_four_islands():
    metrics = [
        {
            "island": f"I{index}",
            "plant_richness": float(index),
            "pollinator_richness": float(index + 1),
            "link_richness": float(index + 2),
            "weighted_shannon": float(index) / 10,
            "connectance": float(index) / 20,
        }
        for index in range(1, 5)
    ]
    covariates = [
        {
            "island": f"I{index}",
            "island_key": f"i{index}",
            "area": float(index),
            "isolation": float(5 - index),
            "age": float(index + 2),
            "elevation": float(index * 10),
        }
        for index in range(1, 5)
    ]
    links = MODULE.descriptive_covariate_links(metrics, covariates)
    area_plant = next(row for row in links if row["predictor"] == "area" and row["network_metric"] == "plant_richness")
    assert area_plant["n_islands"] == 4
    assert area_plant["status"] == "descriptive_only"
    assert area_plant["pearson_r"] == 1.0
