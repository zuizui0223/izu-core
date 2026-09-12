from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data" / "design" / "chapter2_nee_r1b_permit_contact_plan_20260913.json"
CANDIDATES = ROOT / "data" / "design" / "chapter2_nee_r1_site_registry_candidates_20260913.csv"


def _load() -> dict:
    return json.loads(PLAN.read_text(encoding="utf-8"))


def test_permit_plan_is_precontact_not_permission() -> None:
    data = _load()
    assert data["status"] == "precontact_plan_frozen_before_field_outcomes"
    assert data["parents"]["candidate_registry"] == str(CANDIDATES.relative_to(ROOT))
    assert "does not grant permission" in data["claim_boundary"].lower()
    forbidden = "\n".join(data["forbidden"])
    assert "permit_status confirmed" in forbidden
    assert "occurrence evidence" in forbidden
    assert "before all required approvals" in forbidden


def test_official_contact_roles_are_separated() -> None:
    contacts = _load()["official_contacts"]
    assert contacts["moe_izu_islands_management_office"]["telephone"] == "04992-2-7115"
    assert contacts["moe_izu_islands_management_office"]["email"] == "RO-IZUIS@env.go.jp"
    assert contacts["tokyo_education_oshima_office"]["telephone"] == "04992-2-4451"
    assert contacts["kozu_village_industry_tourism"]["telephone"] == "04992-8-0011"
    assert contacts["kozu_village_industry_tourism"]["email"] == "kankou@vill.kouzushima.tokyo.jp"


def test_contact_order_keeps_kozu_farfugium_as_primary_transport() -> None:
    groups = _load()["candidate_contact_order"]
    kozu_transport = next(g for g in groups if "Farfugium" in g["candidate_group"])
    assert kozu_transport["priority"] == 3
    assert kozu_transport["candidate_ids"] == ["kozu-sainbara-lighthouse"]
    assert set(kozu_transport["first_contacts_parallel"]) == {
        "kozu_village_industry_tourism",
        "moe_izu_islands_management_office",
    }
    assert "remains candidate" in kozu_transport["admission_effect"]


def test_natural_monument_and_national_park_rules_fail_closed() -> None:
    data = _load()
    monument = data["natural_monument_rule"]
    park = data["national_park_rule"]
    assert monument["standard_processing_period_days"] == 50
    assert "not evidence" in monument["firewall"]
    assert "preconsult" in park["rule"]
    assert "do not infer" in park["firewall"].lower()


def test_preconsultation_action_package_names_all_manipulative_elements() -> None:
    text = "\n".join(_load()["planned_actions_to_describe_verbatim_in_preconsultation"]).lower()
    for token in ("camera", "bags", "pollen", "single-visit", "fruit/seed", "floral geometry"):
        assert token in text
