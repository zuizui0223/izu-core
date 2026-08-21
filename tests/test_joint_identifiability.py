import json
import subprocess
import sys
from pathlib import Path

from channel_id.joint_identifiability import (
    joint_identifiability_matrix,
    moderation_test_state,
    panels_with_exact_joint_exposure_dependency,
    panels_with_partial_or_exact_joint_context,
)

ROOT = Path(__file__).resolve().parents[1]


def test_current_repository_has_no_harmonized_exact_joint_exposure_dependency_panel():
    rows = joint_identifiability_matrix()
    assert panels_with_exact_joint_exposure_dependency(rows) == []
    state = moderation_test_state(rows)
    assert state["n_exact_joint_panels"] == 0
    assert state["empirical_dependency_x_functional_exposure_test_identified"] is False
    assert state["decision"] == "not_identified_due_to_missing_harmonized_exact_joint_panels"


def test_exact_channels_exist_but_in_different_panels():
    rows = joint_identifiability_matrix()
    exposure = {r["panel"] for r in rows if r["functional_exposure"] == "exact"}
    dependency = {r["panel"] for r in rows if r["direct_total_reproductive_dependency"] == "exact"}
    assert exposure == {"izu_hiraiwa_2024", "izu_hiraiwa_2017_reproductive"}
    assert dependency == {"balearic_malva_2024", "canary_lotus_2024"}
    assert exposure.isdisjoint(dependency)


def test_partial_joint_context_is_visible_without_promotion():
    rows = {r["panel"]: r for r in joint_identifiability_matrix()}
    assert rows["seychelles_fuster_2020"]["same_population_joint_exposure_dependency"] == "partial"
    assert rows["puerto_rico_mona_guaiacum_2022"]["same_population_joint_exposure_dependency"] == "partial"
    assert rows["puerto_rico_mona_guaiacum_2022"]["functional_exposure"] == "partial"
    assert rows["puerto_rico_mona_guaiacum_2022"]["direct_total_reproductive_dependency"] == "partial"
    joint = set(panels_with_partial_or_exact_joint_context(rows.values()))
    assert {"seychelles_fuster_2020", "puerto_rico_mona_guaiacum_2022", "galapagos_effectiveness_2018"}.issubset(joint)


def test_partial_evidence_is_not_promoted_to_exact_dependency():
    rows = {r["panel"]: r for r in joint_identifiability_matrix()}
    assert rows["seychelles_fuster_2020"]["direct_total_reproductive_dependency"] == "partial"
    assert rows["puerto_rico_mona_guaiacum_2022"]["direct_total_reproductive_dependency"] == "partial"
    assert rows["balearic_cneorum_2020"]["direct_total_reproductive_dependency"] == "partial"
    assert rows["galapagos_effectiveness_2018"]["direct_total_reproductive_dependency"] == "partial"


def test_audit_script_reproduces_current_gate(tmp_path):
    subprocess.run([sys.executable, "scripts/audit_joint_identifiability.py"], cwd=ROOT, check=True)
    result = json.loads((ROOT / "data/results/joint_identifiability_matrix.json").read_text())
    assert result["summary"]["n_panels"] == 8
    assert result["summary"]["dependency_x_functional_exposure_test"]["empirical_dependency_x_functional_exposure_test_identified"] is False
    assert result["summary"]["exact_joint_exposure_dependency_panels"] == []
    assert "puerto_rico_mona_guaiacum_2022" in result["summary"]["partial_or_exact_same_population_joint_context_panels"]
