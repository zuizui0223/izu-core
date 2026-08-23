import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data/design/buffer_mechanism_discriminator_gate.json"
PRIORITY = ROOT / "data/design/system_agnostic_buffer_closure_priority.json"


def test_no_current_partial_bridge_is_promoted_to_buffer_mechanism():
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    assert gate["summary"]["systems_screened"] == 6
    assert gate["summary"]["buffer_mechanism_ready_for_abm_admission"] == 0
    assert gate["decision"] == "no_existing_partial_bridge_yet_identifies_a_buffer_filter_strongly_enough_for_abm_admission"
    assert gate["summary"]["nearest_existing_bridge"] == "xisha_cordia_subcordata_two_island_system"
    assert gate["summary"]["strongest_observed_buffer_boundary"] == "hawaii_lobelioid_post_extinction_pollination_2026"


def test_generic_hidden_buffer_parameter_is_forbidden():
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    shortcuts = " ".join(gate["admission_contract"]["forbidden_shortcuts"])
    assert "generic buffer parameter" in shortcuts
    assert "transport effectiveness" in shortcuts
    assert "transport reproductive dependency" in shortcuts


def test_system_agnostic_priority_does_not_privilege_issue91():
    ranking = json.loads(PRIORITY.read_text(encoding="utf-8"))
    targets = {row["system_id"]: row["rank"] for row in ranking["priorities"]}
    assert targets["hawaii_lobelioid_post_extinction_pollination_2026"] == 1
    assert targets["xisha_cordia_subcordata_two_island_system"] == 2
    assert targets["california_channel_islands_nicotiana_glauca"] == 3
    assert targets["issue91_campanula_microdonta"] == 4
    assert next(row for row in ranking["priorities"] if row["system_id"] == "issue91_campanula_microdonta")["programme_blocker"] is False
    assert ranking["decision"].startswith("prioritize_closure_of_existing_buffer_boundaries")
