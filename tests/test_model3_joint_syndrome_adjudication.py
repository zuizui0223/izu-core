import json
from pathlib import Path

from scripts.adjudicate_model3_joint_syndrome import adjudicate


def _write(tmp_path, setting, *, syndrome=0.0, outcross=0.0, branching=False, agreement=1.0):
    p = tmp_path / f"{setting}.json"
    summary = {
        "histories_total": 128,
        "histories_eligible": 128,
        "class_counts": {
            "syndrome": int(round(128 * syndrome)),
            "outcross": int(round(128 * outcross)),
            "intermediate": 128 - int(round(128 * syndrome)) - int(round(128 * outcross)),
        },
        "class_frequencies": {
            "syndrome": syndrome,
            "outcross": outcross,
            "intermediate": 1 - syndrome - outcross,
        },
        "history_branching": branching,
        "split_half_classifiable_histories": 128,
        "split_half_class_agreement": agreement,
        "split_half_agreement_gate_pass": agreement >= 0.70,
    }
    p.write_text(json.dumps({
        "status": "finite_joint_syndrome_followup_complete",
        "setting": setting,
        "terminal_occupancy_fraction_all_trajectories": 1.0,
        "summary_by_initial_state": {
            "outcross_like": summary,
            "central": summary,
            "selfing_like": summary,
        },
        "any_history_branching": branching,
        "any_reproducible_history_branching": branching and agreement >= 0.70,
    }))
    return str(p)


def test_adjudication_requires_realized_endpoint_for_mechanistic_promotion(tmp_path):
    paths = [
        _write(tmp_path, "delayed_control"),
        _write(tmp_path, "prior_selfing"),
        _write(tmp_path, "pollen_discount", syndrome=0.2),
        _write(tmp_path, "assurance_cost"),
    ]
    result = adjudicate(paths)
    assert result["overall_promotion"] == "mechanistic_core"
    assert result["settings"]["pollen_discount"]["promotion"] == "mechanistic_core"


def test_reproducible_branching_outranks_mechanistic_core(tmp_path):
    paths = [
        _write(tmp_path, "delayed_control"),
        _write(tmp_path, "prior_selfing", syndrome=0.2, outcross=0.2, branching=True, agreement=0.8),
        _write(tmp_path, "pollen_discount"),
        _write(tmp_path, "assurance_cost"),
    ]
    result = adjudicate(paths)
    assert result["overall_promotion"] == "repeatability_core_or_next_paper"
