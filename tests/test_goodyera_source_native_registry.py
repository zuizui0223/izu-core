from pathlib import Path

from channel_id.primary_source_holdout import (
    compile_holdout_observations,
    load_native_evidence,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "predictive_meta" / "primary_source_native_evidence.csv"


def test_goodyera_rows_are_source_native_but_excluded_from_numeric_holdout():
    records = load_native_evidence(REGISTRY)
    goodyera = [record for record in records if record.source_id == "goodyera_suetsugu_2024"]
    assert len(goodyera) == 3
    assert all(record.analysis_group == "excluded" for record in goodyera)
    assert all(record.scoring_status == "excluded_comparator" for record in goodyera)
    assert all(record.numeric_status == "qualitative_only" for record in goodyera)
    assert {record.trait_family for record in goodyera} == {
        "hybrid_replacement", "pollinator_context", "interaction_rewiring"
    }

    emitted_ids = {row["observation_id"] for row in compile_holdout_observations(records)}
    assert not emitted_ids.intersection(record.evidence_id for record in goodyera)


def test_goodyera_registry_preserves_the_mechanistic_boundary():
    records = load_native_evidence(REGISTRY)
    rows = {record.evidence_id: record for record in records}
    replacement = rows["goodyera-2024-hybrid-replacement"]
    rewiring = rows["goodyera-2024-kozu-rewiring"]
    assert "pure G. henryi" in replacement.claim
    assert "rather than retaining" in rewiring.claim
    assert "not evidence that pure G. henryi evolved" in rewiring.notes
