import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/design/guaiacum_joint_source_audit.json"


def load():
    return json.loads(AUDIT.read_text(encoding="utf-8"))


def test_source_native_population_contrast_is_preserved() -> None:
    audit = load()
    exposure = audit["source_native_pollinator_contrast"]
    assert exposure["guanica"]["reported_species_richness"] == 8
    assert exposure["mona"]["reported_species_richness"] == 17
    assert exposure["guanica"]["table1_total_visits_2008_2010"] == 9443
    assert exposure["mona"]["table1_total_visits_2008_2010"] == 3358
    assert exposure["guanica"]["apis_share_of_table1_visits"] == pytest.approx(9282 / 9443)
    assert exposure["harmonized_with_izu_fdq"] is False


def test_breeding_evidence_is_direct_but_total_dependency_ratio_stays_closed() -> None:
    audit = load()
    reproductive = audit["source_native_reproductive_contrast"]
    assert reproductive["autogamy"]["guanica_mature_fruits"] == 3
    assert reproductive["autogamy"]["mona_mature_fruits"] == 2
    assert reproductive["isi_seedset_self_over_outcross"] == {
        "guanica": 0.60,
        "mona": 0.63,
        "between_island_test": "t=-0.29, df=18, P=0.77",
    }
    assert reproductive["direct_vector_dependency"] == "supported"
    assert reproductive["direct_total_dependency_ratio"] == "not_reconstructed_without_numeric_outcross_or_open_fruitset_values"


def test_guaiacum_does_not_open_cross_lineage_moderation() -> None:
    audit = load()
    joint = audit["joint_identifiability"]
    assert joint["same_species_two_population_exposure_contrast"] == "exact_source_native"
    assert joint["same_population_breeding_experiment"] == "exact_source_native"
    assert joint["same_tree_exposure_dependency_linkage"] == "not_reported"
    assert joint["harmonized_functional_exposure"] == "not_identified"
    assert joint["cross_lineage_dependency_x_functional_exposure_ready"] is False
