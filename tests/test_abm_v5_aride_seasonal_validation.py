from __future__ import annotations

import importlib.util
import io
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v5_aride_seasonal_validation_v1.json"
ACQUIRE = ROOT / "scripts/acquire_aride2026_dryad_matrices.py"
GEO = ROOT / "scripts/match_aride2026_to_gift_opportunity.py"
VALIDATE = ROOT / "scripts/run_abm_v5_aride_seasonal_validation.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_design_keeps_exact_three_dryad_streams_and_two_targets():
    design = json.loads(DESIGN.read_text())
    assert design["held_out_system"]["dryad_file_streams"] == {
        "Early_Oct.csv": 4845709,
        "Mid_Nov.csv": 4845711,
        "Late_Dec.csv": 4845710,
    }
    assert design["outcomes_frozen_before_matrix_download"] == [
        "interaction_shannon",
        "mean_plant_niche_overlap_morisita_horn",
    ]
    assert design["v5_predictive_distribution"]["context_strengths"] == [0.25, 0.5, 0.75, 1.0]
    assert design["v5_predictive_distribution"]["v4_saturations"] == [1.0, 1.5, 2.0, 2.5, 3.0]
    assert design["v5_predictive_distribution"]["replicates_per_setting"] == 100


def test_frozen_ecdf_interpolation_preserves_reference_knots_without_insertion():
    geo = load(GEO, "aride_geo_test")
    reference = [10.0, 20.0, 40.0]
    assert geo.frozen_ecdf_interpolate(10.0, reference) == 0.0
    assert geo.frozen_ecdf_interpolate(20.0, reference) == 0.5
    assert geo.frozen_ecdf_interpolate(40.0, reference) == 1.0
    assert math.isclose(geo.frozen_ecdf_interpolate(30.0, reference), 0.75)
    assert geo.frozen_ecdf_interpolate(1.0, reference) == 0.0
    assert geo.frozen_ecdf_interpolate(100.0, reference) == 1.0


def test_source_schema_audit_rejects_negative_or_ragged_weights():
    acquire = load(ACQUIRE, "aride_acquire_test")
    good = b",poll_a,poll_b\nplant_a,0.1,0.2\nplant_b,0,0.3\n"
    audit = acquire.parse_matrix_shape(good)
    assert audit["n_plants"] == 2
    assert audit["n_pollinators"] == 2
    assert audit["n_positive_links"] == 3
    for bad in (
        b",poll_a,poll_b\nplant_a,0.1\n",
        b",poll_a,poll_b\nplant_a,-0.1,0.2\n",
    ):
        try:
            acquire.parse_matrix_shape(bad)
        except RuntimeError:
            pass
        else:
            raise AssertionError("invalid source matrix must be rejected")


def test_percentile_and_primary_envelope_rule_are_fixed():
    validation = load(VALIDATE, "aride_validation_test")
    values = [0.0, 1.0, 2.0, 3.0, 4.0]
    assert validation.percentile(values, 0.0) == 0.0
    assert validation.percentile(values, 0.5) == 2.0
    assert validation.percentile(values, 1.0) == 4.0
    interval = {"p2_5": 1.0, "p97_5": 3.0}
    assert validation.inside(2.0, interval)
    assert not validation.inside(4.0, interval)


def test_design_prohibits_posthoc_setting_selection_and_empty_rule_changes():
    design = json.loads(DESIGN.read_text())
    prohibited = " ".join(design["prohibited_after_matrix_download"]).lower()
    assert "choose a context strength or saturation" in prohibited
    assert "empty/single-partner" in prohibited
    assert design["v5_predictive_distribution"]["context_strength_weighting"] == "equal"
    assert design["v5_predictive_distribution"]["saturation_weighting"] == "equal"
