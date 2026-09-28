from channel_id.study_workflow import SummaryRow, analyze_summary, validate_summary


def row(channel, regime, order, step, mean, n=20, sd=1.0):
    return SummaryRow(channel, regime, order, step, mean, n, sd, None)


def test_validation_rejects_missing_threshold_side():
    rows = [row("x", "a", 0, 0, 1), row("x", "b", 1, 0, 2), row("x", "c", 2, 0, 3)]
    assert any("both 0 and 1" in error for error in validate_summary(rows))


def test_workflow_distinguishes_channels():
    rows = [
        row("cline", "a", 0, 0, 3.0), row("cline", "b", 1, 0, 2.0), row("cline", "c", 2, 1, 1.0),
        row("step", "a", 0, 0, 3.0), row("step", "b", 1, 0, 3.0), row("step", "c", 2, 1, 1.0),
    ]
    result = analyze_summary(rows, replicates=200, seed=7)
    assert result["status"] == "ok"
    assert result["channels"]["cline"]["selected_shape"] == "cline"
    assert result["channels"]["step"]["selected_shape"] == "second_step"
