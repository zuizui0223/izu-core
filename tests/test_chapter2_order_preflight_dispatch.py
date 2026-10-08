"""Workflow permission regression: old-history audit must NOT launch new cohort."""
from pathlib import Path

WORKFLOW = Path(".github/workflows/chapter2-order-expression-cohort.yml")


def _job(text: str, name: str) -> str:
    key = f"  {name}:\n"
    assert text.count(key) == 1, name
    start = text.index(key)
    end = text.find("\n  ", start + len(key))
    # Match only the next top-level job, never a nested 'if' or step.
    import re
    next_job = re.search(r"^  [a-z][a-z0-9-]*:\s*$", text[start + len(key):], re.M)
    return text[start:start + len(key) + next_job.start()] if next_job else text[start:]


def test_separate_preflight_is_default_and_manual_only():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    event_header = workflow.split("permissions:", 1)[0]
    assert "workflow_dispatch:" in event_header
    assert "pull_request:" not in event_header
    assert "push:" not in event_header
    assert "schedule:" not in event_header
    assert "default: preflight_only" in event_header
    assert "- preflight_only" in event_header
    assert "- full_cohort" in event_header
    assert "full_cohort_launch_approved:" in event_header
    assert "default: false" in event_header
    assert "source_commit_sha:" in event_header


def test_preflight_requires_main_and_exact_reviewed_source_sha():
    t = WORKFLOW.read_text(encoding="utf-8")
    preflight = _job(t, "preflight")
    assert "github.ref == 'refs/heads/main'" in preflight
    assert "inputs.mode == 'preflight_only'" in preflight
    assert "inputs.mode == 'full_cohort'" in preflight
    assert "inputs.full_cohort_launch_approved == true" in preflight
    assert 'test "$REVIEWED_SHA" = "$CHECKED_OUT_SHA"' in preflight
    assert "python -m scripts.audit_chapter2_order_engineering_cost" in preflight
    assert "tests/test_chapter2_order_full_archive_smoke.py" in preflight
    assert "order-cohort-preflight-old-history-receipts" in preflight


def test_no_new_biological_history_without_full_explicit_approval():
    t = WORKFLOW.read_text(encoding="utf-8")
    history = _job(t, "prehistory")
    assert "needs: preflight" in history
    assert "inputs.mode == 'full_cohort'" in history
    assert "inputs.full_cohort_launch_approved == true" in history
    assert "--execute-frozen-cohort" in history
    future = _job(t, "postshock")
    assert "needs: prehistory" in future
    final = _job(t, "final-readout")
    assert "needs: postshock" in final
