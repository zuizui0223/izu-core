from pathlib import Path

from scripts.build_island_ecology_manuscript_v3 import SOURCE, build_text

ROOT = Path(__file__).resolve().parents[1]


def rendered() -> tuple[str, str]:
    source = SOURCE.read_text(encoding="utf-8")
    return source, build_text(source)


def test_v3_integrates_frozen_h2_sign_decomposition_without_scientific_drift():
    source, v3 = rendered()
    assert source != v3
    assert "sign(Δ reproduction) = sign(Δ service) = sign(Δ functional opportunity)" in v3
    assert "had to be present already in lineage-specific functional-opportunity change" in v3
    assert "The key state dependence therefore enters before those downstream filters" in v3
    assert "does not assign the synthetic functional coordinate to a named empirical trait" in v3
    for token in ("0.4167", "105/288", "16/96", "85/96", "11/96", "207/216"):
        assert token in v3
    assert "zero sign rescues among 525 eligible declines" in v3


def test_v3_sharpens_gap_without_reopening_island_syndrome_question():
    _, v3 = rendered()
    assert "The unresolved problem is therefore not whether island floras show recurrent syndromes" in v3
    assert "the same island-associated change in pollinator function can send already-established lineages in different directions" in v3
    assert "The study does not test whether island syndromes exist." in v3


def test_v3_keeps_reference_list_identical_to_v2():
    source, v3 = rendered()
    assert source.split("# References", 1)[1] == v3.split("# References", 1)[1]


def test_v3_numbered_abstract_remains_under_journal_limit():
    _, v3 = rendered()
    abstract = v3.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]
    words = abstract.replace("**", "").split()
    assert len(words) <= 350
    assert "5. Synthesis." in abstract.replace("**", "")


def test_v3_preserves_protected_external_boundaries():
    _, v3 = rendered()
    assert "strict challenge systems" in v3
    assert "not a random sample from which prevalence can be estimated" in v3
    assert "Dominica *Heliconia* was retained as a failed signed-position projection rather than retuned after failure" in v3
    assert "It did not treat 13 systems as independent demonstrations of one causal mechanism" in v3
