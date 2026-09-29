import csv
import json
from pathlib import Path

import pytest

from channel_id.real_data_causal_bridge import audit_real_data_bridge, source_native_dependency_endpoints

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def load_csv(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def inputs():
    return dict(
        izu_fdq=load_json("data/predictive_meta/hiraiwa_ushimaru_continuous_functional_exposure.json"),
        izu_matching_pollen=load_json("data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen.json"),
        izu_matching_pollen_heterogeneity=load_json("data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen_heterogeneity.json"),
        izu_2017_rows=load_csv("data/predictive_meta/hiraiwa_ushimaru_2017_reproductive_sensitivity.csv"),
        seychelles=load_json("data/results/seychelles_pollination_effectiveness_summary.json"),
        malva=load_json("data/results/balearic_malva_effectiveness_summary.json"),
        lotus=load_json("data/results/canary_lotus_effectiveness_summary.json"),
    )


def test_real_source_native_dependency_endpoints_span_low_to_high_shortfall():
    x = inputs()
    malva, lotus = source_native_dependency_endpoints(x["malva"], x["lotus"])
    assert malva.dependency_shortfall == pytest.approx(0.11331500392772975)
    assert lotus.dependency_shortfall == pytest.approx(0.9782608695652174)
    assert lotus.dependency_shortfall - malva.dependency_shortfall == pytest.approx(0.8649458656374877)
    assert not malva.transportable_to_izu
    assert not lotus.transportable_to_izu


def test_current_izu_real_data_chain_stops_before_direct_dependency():
    result = audit_real_data_bridge(**inputs())
    chain = result["izu_contemporary_chain"]
    assert chain["fdq_to_matching"]["post_oshima_fdq_coefficient"] > 0
    assert chain["fdq_to_matching"]["stable_to_leave_one_island"] is True
    assert chain["matching_to_pollen"]["post_oshima_tm_coefficient"] > 0
    assert chain["matching_to_pollen"]["interval_excludes_zero"] is False
    assert chain["direct_reproductive_dependency_in_exact_izu_populations"] is False


def test_real_data_rejects_universal_pollinator_and_reproductive_cascade():
    result = audit_real_data_bridge(**inputs())
    assert result["izu_2017_reproductive_heterogeneity"]["universal_one_direction_response_falsified"] is True
    assert result["izu_2017_reproductive_heterogeneity"]["oshima_reproductive_data_available"] is False
    sey = result["external_direct_function"]["seychelles"]
    assert sey["single_visit_rows"] == 489
    assert sey["breeding_rows"] == 557
    assert sey["universal_visitor_winner"] is False


def test_committed_result_matches_recomputed_real_data_audit():
    expected = audit_real_data_bridge(**inputs())
    committed = load_json("data/results/real_data_causal_bridge.json")
    assert committed == expected


def test_no_cross_system_endpoint_is_promoted_to_izu_dependency():
    result = audit_real_data_bridge(**inputs())
    blocked = result["still_not_identified"]
    assert "direct reproductive dependency for Campanula microdonta in the exact Izu pilot populations" in blocked
    assert "an empirical cross-lineage dependency x FDQ coefficient" in blocked
    assert all(not row["transportable_to_izu"] for row in result["external_direct_function"]["source_native_dependency_endpoints"])
