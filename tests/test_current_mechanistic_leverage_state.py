from pathlib import Path


def read_current_synthesis() -> str:
    return Path("docs/CURRENT_MECHANISTIC_LEVERAGE.md").read_text(encoding="utf-8")


def test_hendriks_provenance_is_currently_complete_not_stale_open_gate():
    text = read_current_synthesis()
    assert "Hendriks provenance is now **complete**" in text
    assert "Hendriks provenance remains unlocked" not in text
    assert "exact PDF/data bytes remain undelivered" not in text


def test_external_bridge_state_is_partial_not_formal():
    text = read_current_synthesis()
    assert "bridge_system_partial = 3" in text
    assert "bridge_system_complete = 0" in text
    assert "formal_cross_system_mechanism_fit_ready = false" in text
    assert "near_complete_within_archipelago" in text


def test_issue_91_remains_first_empirical_priority():
    text = read_current_synthesis()
    priority = text.split("## Decisive next evidence", 1)[1]
    assert "1. **Issue #91:**" in priority
    assert "first real linked" in priority


def test_source_availability_gates_are_not_active_code_loops():
    text = read_current_synthesis()
    assert "Source-triggered reopen gates, not active code loops" in text
    assert "automated public/OpenAlex routes are" in text
    assert "A source route being exhausted is not evidence that the underlying data never" in text
