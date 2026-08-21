import json
import subprocess
import sys
from pathlib import Path

from channel_id.functional_exposure_harmonization import current_exposure_audits, harmonization_state

ROOT = Path(__file__).resolve().parents[1]


def test_izu_reference_is_the_only_current_fdq_ready_panel() -> None:
    state = harmonization_state()
    assert state["reference_estimand"] == "abundance_weighted_Rao_Q_of_pollinator_proboscis_length"
    assert state["fdq_ready_panels"] == ["izu_hiraiwa_2024"]
    assert state["exact_joint_fdq_dependency_panels"] == []
    assert state["cross_system_moderation_ready"] is False


def test_external_joint_candidates_are_not_relabelled_as_fdq() -> None:
    audits = {row.panel: row for row in current_exposure_audits()}
    for panel in (
        "seychelles_thespesia_2020",
        "puerto_rico_mona_guaiacum_2022",
        "balearic_malva_2024",
        "canary_lotus_2024",
    ):
        assert audits[panel].relative_abundance_available is True
        assert audits[panel].quantitative_pollination_trait_available is False
        assert audits[panel].rao_q_estimable is False
        assert audits[panel].izu_compatible_fdq_ready is False


def test_direct_dependency_does_not_override_exposure_gate() -> None:
    audits = {row.panel: row for row in current_exposure_audits()}
    assert audits["seychelles_thespesia_2020"].direct_dependency_same_source_unit is True
    assert audits["balearic_malva_2024"].direct_dependency_same_source_unit is True
    assert audits["canary_lotus_2024"].direct_dependency_same_source_unit is True
    assert not audits["seychelles_thespesia_2020"].exact_joint_ready
    assert not audits["balearic_malva_2024"].exact_joint_ready
    assert not audits["canary_lotus_2024"].exact_joint_ready


def test_audit_cli_writes_current_gate() -> None:
    subprocess.run([sys.executable, "scripts/audit_functional_exposure_harmonization.py"], cwd=ROOT, check=True)
    result = json.loads((ROOT / "data/results/functional_exposure_harmonization_gate.json").read_text())
    assert result["state"] == harmonization_state()
    assert "species richness" in result["prohibited_substitutions"]
    assert "Shannon diversity" in result["prohibited_substitutions"]
