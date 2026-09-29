from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.audit_izu_transition_linked_chain import build_audit


def fixture_rows():
    blocks = [{
        "block_id": "B1", "population_id": "POP1", "field_event_id": "E1", "island_id": "Oshima",
        "site_id": "SITE1", "taxon": "Campanula microdonta", "block_start": "2026-07-01T08:00:00+09:00",
        "block_end": "2026-07-01T18:00:00+09:00", "season_id": "2026_main", "block_role": "pilot",
        "predeclared_before_outcomes": "yes", "notes": "",
    }]
    plants = [
        {
            "population_id": "POP1", "field_event_id": "E1", "island_id": "Oshima", "site_id": "SITE1",
            "taxon": "Campanula microdonta", "plant_id": "PL1", "analysis_role": "focal_anchor",
            "tagged_at": "2026-07-01T07:00:00+09:00", "notes": "",
        },
        {
            "population_id": "POP1", "field_event_id": "E1", "island_id": "Oshima", "site_id": "SITE1",
            "taxon": "Campanula microdonta", "plant_id": "PL2", "analysis_role": "functional_control",
            "tagged_at": "2026-07-01T07:05:00+09:00", "notes": "donor",
        },
    ]
    geometry = [{
        "field_event_id": "E1", "island_id": "Oshima", "site_id": "SITE1", "plant_id": "PL1",
        "flower_id": "G1", "measurement_id": "M1", "flower_stage": "open", "flower_orientation": "horizontal",
        "corolla_length_mm": "30", "corolla_mouth_diameter_mm": "12", "corolla_inner_depth_mm": "25",
        "measurement_method": "caliper", "photo_id": "", "measurement_date": "2026-07-01",
        "measurer_id": "obs", "notes": "",
    }]
    effort = [{
        "field_event_id": "E1", "island_id": "Oshima", "site_id": "SITE1", "effort_id": "EFF1",
        "plant_id": "PL1", "flower_id": "VIS1", "start_time": "2026-07-01T09:00:00+09:00",
        "end_time": "2026-07-01T10:00:00+09:00", "monitored_open_flower_count": "1", "method": "live",
        "video_id": "", "recording_status": "complete", "usable_observation": "yes", "observer_id": "obs",
        "notes": "",
    }]
    visits = [{
        "visit_id": "V1", "field_event_id": "E1", "island_id": "Oshima", "site_id": "SITE1",
        "effort_id": "EFF1", "plant_id": "PL1", "flower_id": "VIS1", "source_video_id": "",
        "visit_start_offset_s": "600", "visit_end_offset_s": "620", "individual_track_id": "T1",
        "detection_source": "live", "visitor_group": "bombus_ardens_confirmed", "visitor_taxon_id": "Bombus ardens",
        "body_size_class": "large", "identification_confidence": "confirmed", "corolla_entry": "entered",
        "anther_contact": "confirmed", "stigma_contact": "confirmed", "contact_visibility": "clear",
        "contact_evidence": "live_direct", "scorer_id": "obs", "scored_at": "2026-07-01T12:00:00+09:00",
        "notes": "",
    }]
    svd = [
        {
            "svd_id": "SVD1", "population_id": "POP1", "field_event_id": "E1", "island_id": "Oshima",
            "site_id": "SITE1", "taxon": "Campanula microdonta", "plant_id": "PL1", "flower_id": "VIS1",
            "record_type": "single_visit", "effort_id": "EFF1", "visit_id": "V1",
            "visitor_group": "bombus_ardens_confirmed", "identification_confidence": "confirmed",
            "first_visit_confirmed": "yes", "bag_on_time": "2026-07-01T08:00:00+09:00",
            "bag_off_time": "2026-07-01T09:00:00+09:00", "stigma_collected_time": "2026-07-01T09:20:00+09:00",
            "pollen_count_method": "light_microscopy", "total_pollen_grains": "12",
            "conspecific_pollen_grains": "10", "heterospecific_pollen_grains": "1",
            "unclassified_pollen_grains": "1", "counter_id": "counter", "notes": "",
        },
        {
            "svd_id": "CTRL1", "population_id": "POP1", "field_event_id": "E1", "island_id": "Oshima",
            "site_id": "SITE1", "taxon": "Campanula microdonta", "plant_id": "PL1", "flower_id": "CTRL",
            "record_type": "exposed_no_visit_control", "effort_id": "", "visit_id": "", "visitor_group": "",
            "identification_confidence": "not_applicable", "first_visit_confirmed": "not_applicable",
            "bag_on_time": "2026-07-01T08:00:00+09:00", "bag_off_time": "2026-07-01T09:30:00+09:00",
            "stigma_collected_time": "2026-07-01T09:50:00+09:00", "pollen_count_method": "light_microscopy",
            "total_pollen_grains": "1", "conspecific_pollen_grains": "1", "heterospecific_pollen_grains": "0",
            "unclassified_pollen_grains": "0", "counter_id": "counter", "notes": "",
        },
    ]
    treatments = [
        {
            "treatment_id": "TR_OPEN", "population_id": "POP1", "field_event_id": "E1", "island_id": "Oshima",
            "site_id": "SITE1", "taxon": "Campanula microdonta", "plant_id": "PL1", "flower_id": "F_OPEN",
            "treatment_type": "open_pollinated", "assigned_at": "2026-07-01T10:30:00+09:00", "bag_on_time": "",
            "bag_off_time": "", "hand_pollen_source_site_id": "", "hand_pollen_source_plant_id": "",
            "outcome_status": "mature_fruit", "fruit_id": "FR1", "notes": "",
        },
        {
            "treatment_id": "TR_AUTO", "population_id": "POP1", "field_event_id": "E1", "island_id": "Oshima",
            "site_id": "SITE1", "taxon": "Campanula microdonta", "plant_id": "PL1", "flower_id": "F_AUTO",
            "treatment_type": "bagged_autonomous", "assigned_at": "2026-07-01T10:35:00+09:00",
            "bag_on_time": "2026-07-01T10:35:00+09:00", "bag_off_time": "",
            "hand_pollen_source_site_id": "", "hand_pollen_source_plant_id": "", "outcome_status": "aborted",
            "fruit_id": "", "notes": "",
        },
        {
            "treatment_id": "TR_OUT", "population_id": "POP1", "field_event_id": "E1", "island_id": "Oshima",
            "site_id": "SITE1", "taxon": "Campanula microdonta", "plant_id": "PL1", "flower_id": "F_OUT",
            "treatment_type": "supplemental_outcross", "assigned_at": "2026-07-01T10:40:00+09:00",
            "bag_on_time": "", "bag_off_time": "", "hand_pollen_source_site_id": "SITE1",
            "hand_pollen_source_plant_id": "PL2", "outcome_status": "mature_fruit", "fruit_id": "FR2",
            "notes": "",
        },
    ]
    fruits = [
        {
            "fruit_id": "FR1", "site_id": "SITE1", "maternal_id": "PL1", "collection_date": "2026-08-01",
            "mature_seed_count": "20", "genotyped_seed_target": "0", "genotyped_seed_count": "0", "fruit_notes": "",
        },
        {
            "fruit_id": "FR2", "site_id": "SITE1", "maternal_id": "PL1", "collection_date": "2026-08-01",
            "mature_seed_count": "35", "genotyped_seed_target": "0", "genotyped_seed_count": "0", "fruit_notes": "",
        },
    ]
    return blocks, plants, geometry, effort, visits, svd, treatments, fruits


def test_same_block_same_plant_chain_opens_structural_bridge():
    payload = build_audit(*fixture_rows())
    assert payload["summary"]["full_chain_plants"] == 1
    assert payload["summary"]["full_chain_blocks"] == 1
    assert payload["summary"]["transition_linked_blocks"] == 1
    pl1 = next(row for row in payload["plant_chain_rows"] if row["plant_id"] == "PL1")
    assert pl1["full_chain_plant"] is True
    block = payload["block_chain_rows"][0]
    assert block["observed_visitor_key_richness"] == 1
    assert block["effective_service_composition_ready"] is True
    assert block["transition_linked_chain_ready"] is True


def test_population_level_completion_does_not_substitute_for_same_plant_chain():
    rows = list(fixture_rows())
    treatments = deepcopy(rows[6])
    fruits = deepcopy(rows[7])
    # Move the outcross treatment to PL2: the population still has all channels,
    # but no tagged plant carries the whole chain.
    treatments[2]["plant_id"] = "PL2"
    treatments[2]["flower_id"] = "PL2_OUT"
    treatments[2]["hand_pollen_source_plant_id"] = "PL1"
    fruits[1]["maternal_id"] = "PL2"
    rows[6] = treatments
    rows[7] = fruits
    payload = build_audit(*rows)
    assert payload["summary"]["full_chain_plants"] == 0
    assert payload["summary"]["transition_linked_blocks"] == 0


def test_effort_cannot_cross_prespecified_block_boundary():
    rows = list(fixture_rows())
    effort = deepcopy(rows[3])
    effort[0]["end_time"] = "2026-07-01T19:00:00+09:00"
    rows[3] = effort
    with pytest.raises(ValueError, match="crosses transition-block boundary"):
        build_audit(*rows)
