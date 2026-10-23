"""Validate source-backed island primary literature and inference-safe framing."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MASTER=ROOT/"docs/CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md"
WORKING=ROOT/"docs/CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md"
AUDIT=ROOT/"docs/CHAPTER2_ISLAND_PRIMARY_LITERATURE_AUDIT_20261023.md"
YEARS_DOI={
 "Hetherington-Rauth and Johnson, 2020": "10.1086/709018",
 "Schueller, 2004": "10.3732/ajb.91.5.672",
 "Ciarle, 2026": "10.1002/oik.11782",
}


def test_empirical_island_results_are_correctly_separated_from_model_evidence():
    m=MASTER.read_text(encoding="utf8")
    w=WORKING.read_text(encoding="utf8")
    intro=m.split("## Introduction\n",1)[1].split("## Results",1)[0]
    discussion=m.split("## Discussion\n",1)[1].split("## Online Methods",1)[0]
    ref=m.split("## References",1)[1]
    assert "556 plant species and 136 phylogenetically independent" in intro
    assert "not smaller on average" in intro
    assert "*Nicotiana glauca*" in intro
    assert "not accompanied by reduced pollinator service" in intro
    assert "examined leaf size and stature, not mating systems" in intro
    assert "can sometimes distinguish filtering" in intro
    assert "does not demonstrate natural colonization filtering" in discussion
    assert "universal decline in island flower size" not in intro
    assert "impossible to separate in nature" not in m
    for citation,doi in YEARS_DOI.items():
        assert citation in intro or citation in discussion
        assert doi in ref
        assert ref.count(doi)==1
        assert doi in w
    assert "Ciarle, R. (2026; first published online 2025)" in ref
    assert "Ciarle et al." not in m


def test_the_two_archival_manuscripts_share_same_current_island_context():
    a=MASTER.read_text(encoding="utf8")
    b=WORKING.read_text(encoding="utf8")
    start="Natural islands complicate a single selfing-syndrome prediction."
    end="These processes have strong precedents."
    assert a.split(start,1)[1].split(end,1)[0] == b.split(start,1)[1].split(end,1)[0]
    start2="For empirical island comparisons, this interpretation suggests measuring investment allocation"
    end2="Repeated populations within comparable founding"
    assert a.split(start2,1)[1].split(end2,1)[0] == b.split(start2,1)[1].split(end2,1)[0]
    assert a.split("## Abstract\n",1)[1].split("## Introduction\n",1)[0] == (
        b.split("## Abstract — provisional, existing evidence only; NOT for submission\n",1)[1]
         .split("## Introduction\n",1)[0])
    # Authoritative completed article, not the archival PENDING research proposals:
    main=a.split("## Introduction\n",1)[1].split("## Online Methods",1)[0]
    assert len(main.split())<=3500
    intro=a.split("## Introduction\n",1)[1].split("## Results\n",1)[0]
    assert 450<=len(intro.split())<=650
    assert "## Planned new decisive Results" not in a


def test_primary_study_scope_is_explicit():
    t=AUDIT.read_text(encoding="utf8")
    for phrase in ("556 species", "136 phylogenetically", "establishment filtering",
                   "leaf size and stature", "no new preregistered",
                   "10.1002/oik.11782", "10.1086/709018", "10.3732/ajb.91.5.672"):
        assert phrase.lower() in t.lower()
    assert "not the raw data" in t
    assert "no new biological simulations" in t
