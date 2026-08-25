import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data/design/island_syndrome_literature_claim_matrix_20260824.json"
REVIEW = ROOT / "docs/ISLAND_SYNDROME_DEEP_LITERATURE_REVIEW_20260824.md"
INSERTIONS = ROOT / "docs/ISLAND_SYNDROME_MANUSCRIPT_INSERTIONS_20260824.md"
MANUSCRIPT = ROOT / "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md"


def test_island_syndrome_review_uses_three_layer_framework():
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    assert set(matrix["layers"]) == {
        "assembly_filtering",
        "in_situ_evolution",
        "interaction_reorganization",
    }
    review = matrix["review_level_evidence"]
    assert review["globally_proposed_components"] == 21
    assert review["components_investigated_regionally"] == 16
    assert review["well_supported_components"] == 4
    assert review["tentative_components"] == 9
    assert review["components_with_limited_evidence_against_syndrome_membership"] == 3


def test_claim_boundaries_prevent_universal_island_syndrome_overclaim():
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    banned = set(matrix["manuscript_claim_boundary"]["do_not_claim"])
    assert "island_syndromes_are_false" in banned
    assert "all_island_syndrome_components_share_one_causal_mechanism" in banned
    assert "island_flowers_universally_shrink" in banned
    assert "self_compatibility_implies_high_realized_selfing" in banned
    assert matrix["manuscript_claim_boundary"]["current_paper_gap_filled"] == "mechanistic_post_establishment_response_architecture"


def test_key_literature_and_manuscript_insertions_are_present():
    review = REVIEW.read_text(encoding="utf-8")
    insertions = INSERTIONS.read_text(encoding="utf-8")
    for token in [
        "10.1111/nph.13539",
        "10.1111/mec.13087",
        "10.1086/709018",
        "10.1111/brv.12782",
        "10.1080/0028825X.2024.2377418",
        "10.1093/aob/mcaf005",
        "10.1111/geb.12362",
        "10.1038/s41598-020-70954-7",
        "10.1111/1365-2435.14527",
    ]:
        assert token in review
    assert "assembly" in insertions.lower()
    assert "post-establishment" in insertions.lower()
    assert "starting state" in insertions.lower()


def test_primary_manuscript_integrates_deep_island_syndrome_review():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    lower = text.lower()
    for citation in [
        "Pannell et al., 2015",
        "Pannell, 2015",
        "Hetherington-Rauth & Johnson (2020)",
        "Schrader et al., 2021",
        "Ciarle & Burns (2025)",
        "Ciarle et al. (2025)",
        "Traveset et al., 2016",
        "Wang et al., 2020",
    ]:
        assert citation in text
    assert "colonization/assembly filtering" in lower
    assert "in-situ evolutionary change" in lower
    assert "post-establishment ecological response" in lower
    assert "not the existence of recurrent island syndromes" in lower
    assert "pollinator **functional diversity**" in text
