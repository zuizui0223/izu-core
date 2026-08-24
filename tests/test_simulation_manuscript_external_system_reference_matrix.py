import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data/design/simulation_manuscript_external_system_reference_matrix.json"
GATE = ROOT / "data/design/system_agnostic_multi_system_validation_gate_v2.json"
DOC = ROOT / "docs/SIMULATION_MANUSCRIPT_EXTERNAL_SYSTEM_REFERENCES_20260824.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_reference_matrix_matches_all_thirteen_strict_targets():
    matrix = load(MATRIX)
    gate = load(GATE)
    systems = matrix["systems"]
    assert matrix["strict_system_count"] == 13
    assert len(systems) == 13
    matrix_ids = [row["system_id"] for row in systems]
    gate_ids = [row["system_id"] for row in gate["targets"]]
    assert len(set(matrix_ids)) == 13
    assert set(matrix_ids) == set(gate_ids)


def test_reference_matrix_preserves_state_count_contract_and_failures():
    matrix = load(MATRIX)
    counts = Counter(row["strict_state_group"] for row in matrix["systems"])
    assert counts == Counter(matrix["state_count_contract"])
    rows = {row["system_id"]: row for row in matrix["systems"]}
    assert rows["dominica_heliconia"]["strict_state_group"] == "retained_falsification"
    assert "not retuned" in rows["dominica_heliconia"]["claim_boundary"]
    assert rows["puerto_rico_mona_guaiacum"]["strict_state_group"] == "reproductive_axes_decouple"
    assert "must not be collapsed" in rows["puerto_rico_mona_guaiacum"]["claim_boundary"]


def test_every_external_system_has_references_and_existing_source_paths():
    matrix = load(MATRIX)
    doi_count = 0
    for row in matrix["systems"]:
        assert row["primary_references"], row["system_id"]
        assert row["source_paths"], row["system_id"]
        assert row["observed_state_basis"]
        assert row["claim_boundary"]
        for reference in row["primary_references"]:
            assert reference["citation"]
            doi = reference.get("doi")
            assert doi and doi.startswith("10."), (row["system_id"], reference)
            doi_count += 1
        for source_path in row["source_paths"]:
            assert (ROOT / source_path).exists(), source_path
    assert doi_count >= 20


def test_supplementary_reference_doc_keeps_state_counts_and_interpretation_boundary():
    text = DOC.read_text(encoding="utf-8")
    assert "branching: **3** systems" in text
    assert "same-direction propagation: **6** systems" in text
    assert "buffering / alternative: **2** systems" in text
    assert "reproductive-axis decoupling constraint: **1** system" in text
    assert "retained falsification: **1** system" in text
    assert "does **not** support" in text
