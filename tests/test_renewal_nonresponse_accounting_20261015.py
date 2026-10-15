import numpy as np
import pytest

from scripts.audit_renewal_nonresponse_accounting_20261015 import (
    nonresponse_class, price_terms, replay_children,
)


def test_nonresponse_partition_distinguishes_support_mean_and_horizon():
    a = np.ones(201, dtype=bool)
    h = np.zeros(201, dtype=bool)
    assert nonresponse_class(a, h, 182, None) == 'late_reopening'
    a[20::10] = False
    assert nonresponse_class(a, h, 1, None) == 'no_support_window'
    assert nonresponse_class(np.ones(201, bool), h, 1, None) == 'mean_never_reached'
    h[30] = True
    assert nonresponse_class(np.ones(201, bool), h, 1, None) == 'mean_not_sustained'


def test_exact_window_and_existing_events_are_not_nonresponders():
    a = np.zeros(201, bool); a[181:201] = True
    h = np.zeros(201, bool)
    assert nonresponse_class(a, h, 181, None) == 'mean_never_reached'
    assert nonresponse_class(a, h, None, None) == 'never_reopened'
    h[1:21] = True
    assert nonresponse_class(np.ones(201, bool), h, 100, 1) == 'completed_before_reopening'
    h[:] = False
    h[181:201] = True
    assert nonresponse_class(a, h, 181, 181) == 'completed_after_reopening'


def test_invalid_mean_without_allele_support_and_unrecorded_event_reject():
    a = np.ones(201, bool); h = np.zeros(201, bool)
    a[10] = False; h[10] = True
    with pytest.raises(ValueError, match='necessary support'):
        nonresponse_class(a, h, 1, None)
    h[:] = False; h[30:50] = True; a[:] = True
    with pytest.raises(ValueError, match='event inventory'):
        nonresponse_class(a, h, 1, None)


def test_price_identity_separates_parent_choice_segregation_and_mutation():
    t = price_terms(.6, np.array([-.02, -.01, .01]), .55, .57, .58)
    np.testing.assert_allclose(t, [-.02, -.01, .01, -.03, .02, .01, -.02], atol=1e-15)
    assert abs(t[:6].sum()-t[6]) < 1e-15


def test_reconstruction_uses_two_segregation_draws_and_cumulative_flags():
    class Seg:
        def __init__(self): self.calls = 0
        def integers(self, low, high, size):
            assert (low, high, size) == (0, 2, (1, 3))
            self.calls += 1
            return np.full(size, self.calls-1, dtype=int)
    class Mut:
        def random(self, shape): return np.zeros(shape)
        def normal(self, loc, scale, shape):
            assert (loc, scale) == (0, .05)
            return np.full(shape, .2)
    a = np.array([[[.2, .4], [.9, .1], [.3, .5]]])
    o = np.array([[[1, 2], [3, 4], [5, 6]]])
    f = np.zeros_like(a, dtype=bool); f[0, 0, 0] = True
    pre, child, origins, flags, draws = replay_children(a, o, f, [0], [0], Seg(), Mut())
    np.testing.assert_array_equal(pre, a)
    np.testing.assert_array_equal(origins, o)
    np.testing.assert_array_equal(child[:, 0, :], a[:, 0, :])
    np.testing.assert_array_equal(child[:, 1:, :], 1-np.abs(np.mod(a[:, 1:, :]+.2, 2)-1))
    assert flags[0, 0, 0] and flags[0, 1:, :].all()
    assert draws == 18


# Independent checks of *committed handoff tables*; these do not substitute
# for the separately preserved original-array replay and source hashes.
def _cell_table(path, *, key_columns=2):
    from pathlib import Path
    doc = (Path(__file__).resolve().parents[1] / path).read_text(encoding="utf-8")
    rows = [
        [x.strip() for x in line.split("|")[1:-1]]
        for line in doc.splitlines()
        if line.startswith("| main |") or line.startswith("| confirmation |")
    ]
    assert len(rows) == 18, path
    # Nonresponse/standing tables use block + context ID; renewal adds composition.
    assert len({tuple(row[:key_columns]) for row in rows}) == 18, path
    return rows


def test_renewal_handoff_has_full_paired_cell_and_failure_partition():
    non = _cell_table("docs/CHAPTER2_RENEWAL_NONRESPONSE_ACCOUNTING_RESULTS_20261015.md")
    columns = [sum(int(r[i]) for r in non) for i in range(2, 9)]
    # 758 re-opened failures; 156 event completers; 1390 never reopened.
    assert columns == [33, 420, 248, 57, 64, 92, 1390]
    assert sum(columns) == 2304
    assert sum(columns[:4]) == 758
    assert sum(columns[:6]) == 914
    assert all(sum(int(r[i]) for i in range(2, 9)) == 128 for r in non)
    access = _cell_table("docs/CHAPTER2_RENEWAL_STANDING_ACCESS_RESULTS_20261015.md")
    archive_totals = [sum(int(r[i]) for r in access) for i in range(2, 8)]
    # Previous and renewed arms are PAIRED, not independent replication.
    assert archive_totals == [1238, 1214, 914, 92, 1138, 1246]
    assert all(int(r[-1]) <= 128 for r in access)


def test_renewed_six_class_table_and_signed_accounting_stay_coherent():
    from pathlib import Path
    renewal = _cell_table("docs/ECOLOGICAL_INVESTMENT_RENEWAL_RESULTS_20261015.md", key_columns=3)
    totals = [sum(int(r[i]) for r in renewal) for i in range(3, 9)]
    # A-first, I-first, ties and I-only all have the defined I event.
    assert totals == [479, 420, 341, 778, 6, 280]
    assert sum(totals) == 2304
    assert totals[0] + totals[1] + totals[2] + totals[4] == 1246
    for row in renewal:
        assert sum(int(row[i]) for i in range(3, 9)) == 128
        assert abs((int(row[3])-int(row[4])) / 128 - float(row[9])) < 2e-6
        lo, hi = [float(x) for x in row[10].strip("[]").split(",")]
        assert lo <= 0 <= hi

    source = (Path(__file__).resolve().parents[1] /
              "docs/CHAPTER2_RENEWAL_NONRESPONSE_ACCOUNTING_RESULTS_20261015.md").read_text(encoding="utf-8")
    channel_rows = [
        [x.strip() for x in line.split("|")[1:-1]]
        for line in source.splitlines()
        if line.startswith("| late_reopening |") or line.startswith("| no_support_window |")
        or line.startswith("| mean_never_reached |") or line.startswith("| mean_not_sustained |")
    ]
    assert [(r[0], int(r[1])) for r in channel_rows] == [
        ("late_reopening", 33), ("no_support_window", 420),
        ("mean_never_reached", 248), ("mean_not_sustained", 57),
    ]
    for row in channel_rows:
        channels = [float(v) for v in row[2:8]]
        observed = float(row[8])
        assert abs(sum(channels) - observed) <= 3e-6  # six-decimal table rounding
    mean_never = next(r for r in channel_rows if r[0] == "mean_never_reached")
    expected_direction = sum(float(v) for v in mean_never[2:5])
    assert abs(expected_direction - 0.02956) < 2e-6
    # These outcome-selected conditional parental weights favour HIGHER I, not
    # lower I; the 248 cases are not evidence of selection favouring target decline.
    assert expected_direction > 0
