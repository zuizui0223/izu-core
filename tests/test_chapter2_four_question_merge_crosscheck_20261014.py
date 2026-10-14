"""Read-only, independent arithmetic checks for the Q1–Q4 paper merge gate.

These are cross-record consistency checks from admitted JSONs, NOT an original
genome/runtime replay, prospective replication, stochastic expectation, drift
mediation, natural island validation, DOI deposit or permission to merge.

Do not import analytical producer/readout helpers: rederive simple identities
using only the stored numerical outcomes and their predeclared classifications.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return json.loads((ROOT / "data/results" / relative).read_text(encoding="utf-8"))


def close(a, b, tol=1e-10):
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)


def test_q2_all_start_six_class_and_simultaneous_nulls():
    d = read("ecological_order_boundary_20261013.json")
    assert d["cases"] == 2304 and d["updates"] == 460800
    assert len(d["cells"]) == 18
    assert d["supported_supply_pairs"] == []
    assert d["supported_composition_pairs"] == []
    total = 0
    for cell in d["cells"]:
        n = sum(cell["categories"].values())
        assert n == cell["starts"] == 128
        total += n
        c = cell["categories"]
        assert close(cell["D"], (c["assurance_first"] - c["investment_first"]) / n)
        lo, hi = cell["simultaneous_interval"]
        assert lo <= 0 <= hi
    assert total == 2304
    assert d["independent"]["no_producer_or_reader_import"] is True


def test_q3_retained_genomes_selection_sampling_and_fixation():
    d = read("genome_response_accounting_readout_20261013.json")
    assert d["cases"] == 320 and d["updates"] == 64000
    assert d["new_biological_histories"] == 0
    assert len(d["contexts"]) == 10
    fixation = []
    for ctx in d["contexts"]:
        assert ctx["cases"] == 32
        fixation.append(ctx["I_fixed_by200"])
        comp = ctx["mean_cumulative_components"]
        for k in range(3):  # matching, investment, assurance
            expected = (
                comp["selection"][k]
                + comp["parent_sampling"][k]
                + comp["transmission"][k]
                + comp["birth_mutation"][k]
            )
            assert close(expected, comp["observed_change"][k])
    assert 27 <= min(fixation) <= max(fixation) <= 32


def test_q3_density_comparator_signed_accounting_is_not_drift_attribution():
    d = read("matched_operator_gap_20261013.json")
    assert d["cases"] == 320 and d["updates"] == 64000
    assert len(d["contexts"]) == len(d["density_references"]) == 10
    assert d["max_closure_error"] == 0
    for ctx in d["contexts"]:
        assert ctx["cases"] == 32
        assert close(ctx["initial_gap"], 0)
        assert close(ctx["endpoint_gap"], sum(ctx["components"].values()))
    assert "not pure drift" in d["scope"].lower()


def test_q3_restoration_event_counts_and_conditional_limits():
    d = read("q3_conditional_paper_20261014/READOUT.json")
    e = read("q3_event_conditions_paper_20261014/SUMMARY.json")
    assert d["original_primary"] == "unresolved_unchanged"
    assert d["decision"] == "evaluated_conditional"
    assert d["slots"] == e["original_slots"] == 64
    assert d["policy_zero_slots"] == e["nontrigger_policy_zero_slots"] == 3
    assert d["pairs"] == e["triggered_pairs"] == 61 * 64
    assert d["survival"]["both_alive"] == 61 * 64
    assert not any(d["survival"][k] for k in ("native_only", "restored_only", "both_extinct"))
    avg = 0.5 * (
        d["means"]["causal_main"]["estimate"]
        + d["means"]["causal_confirmation"]["estimate"]
    )
    assert close(avg, d["means"]["all64"]["estimate"])
    assert d["means"]["causal_confirmation"]["practical"] == "unresolved"
    assert e["exploratory"] is True and e["biological_updates"] == 0
    assert e["original_primary"] == e["confirmation_margin_0_01"] == "unresolved"
    assert sum(b["pairs"] for b in e["blocks"].values()) == d["pairs"]
    for block in e["blocks"].values():
        j = block["joint"]
        assert sum(j.values()) == block["pairs"]
        assert j["11"] + j["10"] == block["native_events"]
        assert j["11"] + j["01"] == block["restored_events"]
    assert e["blocks"]["causal_confirmation"]["joint"]["10"] == 72
    assert e["blocks"]["causal_confirmation"]["refixation_by_joint"]["10"]["upper"] == 72


def test_q4_initial_assurance_mean_controls_are_not_natural_mediation():
    d = read("initial_assurance_mean_20261013/readout.json")
    assert d["new_native_futures"] == 4096
    assert d["new_clamp_identity_futures"] == 8
    assert len(d["primary"]) == 4
    assert [p["decision"] for p in d["primary"]] == [
        "positive", "unresolved", "positive", "unresolved"
    ]
    low, high = d["policy_route_differences"]
    assert close(low[0] - low[1], 0.03125)
    assert close(high[0] - high[1], 0.044921875)
    assert close(d["primary"][0]["estimate"], low[0] - low[1])
    assert close(d["primary"][2]["estimate"], high[0] - high[1])
    for row in d["primary"]:
        assert row["distribution_free_interval"][0] <= 0 <= row["distribution_free_interval"][1]
    assert "not independent confirmation" in d["inference"].lower()


def test_q4_future_parent_undetermined():
    d = read("future_parent_selection_20261013.json")
    assert d["status"] == "COMPLETE_ALL4096_INDEPENDENTLY_RECOMPUTED_PRIMARY_UNRESOLVED"
    assert len(d["primary"]) == 4
    assert all(p["decision"] == "unresolved" for p in d["primary"])
    assert "not pure assurance-locus selection" in d["estimand"]


def test_original_discovery_archive_is_not_authenticated_full_replay():
    d = read("chapter2_discovery_archive_recovery_20261013.json")
    assert d["status"] == "ARCHIVE_BYTES_AND_DISCOVERY_ENDPOINTS_VERIFIED"
    assert d["verification"]["archive_identity_verified"] is True
    assert d["verification"]["discovery_endpoints_complete"] is True
    assert d["verification"]["original_discovery_full_replay_completed"] is False
    assert d["verification"]["runtime_identity_verified"] is False
    assert d["counts"]["discovery_cases_verified"] == 2048
    assert d["counts"]["genome_checkpoints_verified"] == 8192
