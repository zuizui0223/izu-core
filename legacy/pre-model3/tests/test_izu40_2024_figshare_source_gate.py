from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v8_izu40_figshare_source_gate_v1.json"
SCRIPT = ROOT / "scripts/acquire_audit_izu40_2024_figshare.py"


def test_source_gate_freezes_figshare_v1_and_published_40_network_scope():
    design = json.loads(DESIGN.read_text())
    candidate = design["candidate_system"]
    assert candidate["figshare_article_id"] == 25025000
    assert candidate["figshare_version"] == 1
    assert candidate["figshare_doi"] == "10.6084/m9.figshare.25025000.v1"
    assert "40 spatiotemporally variable" in candidate["published_scope"]
    assert design["target_metrics_calculated"] is False


def test_source_gate_prohibits_target_inspection_and_old_dryad_substitution():
    design = json.loads(DESIGN.read_text())
    prohibited = " ".join(design["prohibited_before_source_admission"]).lower()
    assert "shannon" in prohibited
    assert "plant niche overlap" in prohibited
    assert "support estimands" in prohibited
    assert "predictive envelope" in prohibited
    assert "2016 dryad" in prohibited


def test_source_audit_does_not_import_network_metric_layer():
    text = SCRIPT.read_text().lower()
    assert "external_archipelago_network" not in text
    assert "weightednetwork" not in text
    assert "interaction_shannon" not in text
    assert "mean_plant_niche_overlap" not in text


def test_structured_role_detection_requires_interaction_entities_and_context():
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location("izu40_source_gate_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    roles = module.role_candidates(["site", "season", "plant", "pollinator", "visits"])
    assert roles["network_or_site"] == ["site"]
    assert roles["time"] == ["season"]
    assert roles["plant"] == ["plant"]
    assert roles["pollinator"] == ["pollinator"]
    assert roles["weight"] == ["visits"]
