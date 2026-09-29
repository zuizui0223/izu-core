import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "data/results/olesen2002_tierb_weighted_anchor_source_lock.json"


def load():
    return json.loads(LOCK.read_text())


def test_rp18_is_exact_weighted_anchor():
    x = load()
    a = x["exact_frozen_weighted_anchor"]
    assert a["region_pub"] == "RP18"
    assert a["system"] == "Azores"
    assert a["n_plants"] == 10
    assert a["n_pollinators"] == 12
    assert a["n_positive_links"] == 30
    assert a["total_visitation_rate"] == 1139.0
    assert a["dore_frozen_counts_and_visits_reconcile_exactly"] is True
    assert math.isfinite(a["interaction_shannon"])
    assert 0 <= a["mean_plant_niche_overlap_morisita_horn"] <= 1


def test_rp17_is_not_promoted_across_filter_mismatch():
    x = load()
    m = x["method_validation_only"]
    assert m["region_pub"] == "RP17"
    assert m["dore_frozen_counts_and_visits_reconcile_exactly"] is False
    assert m["source_counts"]["n_pollinators"] != m["dore_frozen_counts"]["n_pollinators"]
    assert m["source_counts"]["n_positive_links"] != m["dore_frozen_counts"]["n_positive_links"]
    assert m["source_counts"]["total_visitation_rate"] != m["dore_frozen_counts"]["total_visitation_rate"]


def test_weighted_anchor_claim_boundary_stays_noncausal():
    x = load()
    assert x["decision"] == "rp18_is_exact_weighted_tier_b_anchor_rp17_is_method_validation_only"
    assert "not pollinator effectiveness" in x["claim_boundary"]
    assert "RP17 is not admitted" in x["claim_boundary"]
