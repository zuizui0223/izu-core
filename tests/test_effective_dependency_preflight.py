from pathlib import Path

from channel_id.effective_dependency_preflight import CHANNEL_TEMPLATES, build_preflight


def test_committed_templates_remain_template_only():
    templates = Path(__file__).resolve().parents[1] / "templates"
    paths = {name: templates / filename for name, filename in CHANNEL_TEMPLATES.items()}
    result = build_preflight(paths, templates)
    assert result["status"] == "template_only_no_field_rows"
    assert result["freeze_recommended"] is False
    assert result["structural_audit_recommended"] is False
    assert result["analysis_admission_opened"] is False


def test_missing_required_channel_is_explicit(tmp_path):
    templates = Path(__file__).resolve().parents[1] / "templates"
    paths = {name: templates / filename for name, filename in CHANNEL_TEMPLATES.items()}
    paths["svd"] = tmp_path / "missing.csv"
    result = build_preflight(paths, templates)
    assert result["status"] == "required_files_missing"
    assert result["structural_audit_recommended"] is False
