from pathlib import Path

from channel_id.joint_interval_channel_profile import (
    PROFILE_CHANNELS,
    load_izu_records,
    profile_cases,
    summarize,
)

ROOT = Path(__file__).resolve().parent.parent


def test_two_stage_profile_wins_every_admissible_izu_outcross_endpoint_case():
    records = load_izu_records(ROOT / "data/inoue_literature_island_traits.csv")
    cases, loadings, _ = profile_cases(records)
    report = summarize(cases, loadings, records)
    assert len(cases) == 64  # six Izu outcrossing intervals
    assert report["profile_wins"]["two_stage_hybrid"] == 64
    assert all(case["winner"] == "two_stage_hybrid" for case in cases)
    assert all(float(case["delta_aicc"]) > 0 for case in cases)


def test_profile_contract_keeps_reproductive_step_separate_from_morphological_clines():
    hybrid = PROFILE_CHANNELS["two_stage_hybrid"]
    assert hybrid["flower_length_mm"] == "island_order_cline"
    assert hybrid["outcrossing"] == "island_order_cline"
    assert hybrid["autonomous_capacity"] == "oshima_to_toshima_step"


def test_no_second_threshold_is_a_deliberately_weaker_joint_profile():
    profile = PROFILE_CHANNELS["no_second_threshold"]
    assert profile["flower_length_mm"] == "island_order_cline"
    assert profile["outcrossing"] == "null"
    assert profile["autonomous_capacity"] == "null"
