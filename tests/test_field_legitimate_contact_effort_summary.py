from channel_id.field_legitimate_contact import audit_field_contacts


def test_effort_summary_is_retained_when_no_visitor_is_scored() -> None:
    effort = {
        "field_event_id": "izu_20260704",
        "island_id": "Hachijo",
        "site_id": "HAC_01",
        "effort_id": "E_ZERO",
        "plant_id": "P001",
        "flower_id": "F001",
        "start_time": "2026-07-04T09:00:00+09:00",
        "end_time": "2026-07-04T09:30:00+09:00",
        "monitored_open_flower_count": "2",
        "method": "fixed_video",
        "video_id": "VID_ZERO",
        "recording_status": "complete",
        "usable_observation": "yes",
        "observer_id": "observer_1",
        "notes": "",
    }

    audit = audit_field_contacts([effort], [])

    assert audit.rate_summary_rows == ()
    assert audit.effort_summary_rows == ({
        "island_id": "Hachijo",
        "usable_effort_windows": "1",
        "monitored_flower_hours": "1.00000000",
        "scored_visit_bouts": "0",
        "boundary": "Effort is a detection denominator, not proof of visitor absence. Zero scored bouts can reflect limited time, weather, video coverage, or scoring scope.",
    },)
