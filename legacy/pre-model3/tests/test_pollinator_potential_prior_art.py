import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRIOR_ART = ROOT / "data/design/pollinator_potential_prior_art.json"
NOVELTY = ROOT / "paper/NOVELTY.md"


def load_prior_art():
    return json.loads(PRIOR_ART.read_text(encoding="utf-8"))


def test_prior_art_lock_contains_inoue_and_hendriks_boundaries():
    data = load_prior_art()
    assert data["status"] == "prior_art_boundary_locked"
    by_id = {source["source_id"]: source for source in data["sources"]}
    assert by_id["inoue_1986_izu_campanula"]["doi"] == "10.1111/j.1442-1984.1986.tb00018.x"
    assert by_id["inoue_1990_pollinator_availability"]["doi"] == "10.1111/j.1442-1984.1990.tb00192.x"
    hendriks = by_id["hendriks_2019_pollinator_potential_paradigm"]
    assert hendriks["identifier"] == "10.13140/RG.2.2.25945.08805"
    assert "Pollinator Potential Paradigm" in hendriks["source_supported_boundary"]
    assert "does not directly measure" in hendriks["empirical_scope"]


def test_prohibited_novelty_claims_cover_basic_pollinator_compression_story():
    data = load_prior_art()
    claims = "\n".join(data["prohibited_novelty_claims"]).lower()
    assert "pollinator limitation can reduce flower size" in claims
    assert "smaller island pollinators" in claims
    assert "pollinator diversity or body-size range" in claims
    assert "universal island-rule coefficient" in claims


def test_defensible_novelty_requires_functional_exposure_dependency_and_adversarial_gates():
    data = load_prior_art()
    novelty = "\n".join(data["izu_core_defensible_novelty"]).lower()
    assert "functional pollinator exposure" in novelty
    assert "effective reproductive dependency" in novelty
    assert "single-visit pollen deposition" in novelty
    assert "measurement-error admission gates" in novelty
    assert "independent system clusters" in novelty


def test_novelty_document_explicitly_rejects_generic_pollinator_potential_novelty():
    text = NOVELTY.read_text(encoding="utf-8").lower()
    assert "pollinator potential paradigm" in text
    assert "not** the generic hypothesis" in text
    assert "required conditions, not estimated reliabilities" in text
    assert "functional exposure" in text
    assert "effective dependency" in text
