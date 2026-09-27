import numpy as np

from scripts.summarize_model3_ch2_bridge_production import _bootstrap_mean, _history_labels


def test_history_labels_keep_mixed_and_repeat_instability_separate():
    x = np.array([
        [[0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]],
        [[-0.2, -0.2, -0.2, -0.2, 0.2, 0.2, 0.2, 0.2]],
        [[0.1, 0.1, 0.1, 0.1, -0.1, -0.1, -0.1, -0.1]],
    ])
    r = _history_labels(x, 0.05)
    assert r["mean8_counts"]["positive"] == 1
    assert r["first4_last4_label_disagreements"] == 1
    assert r["any_repeat_label_disagreements"] == 1


def test_history_labels_preserve_undefined_support():
    x = np.ones((3, 2, 8))
    x[:, 1, 3] = np.nan
    r = _history_labels(x, 0.0)
    assert r["mean8_counts"]["undefined"] == 1
    assert r["mean8_counts"]["positive"] == 1
    assert r["mean8_mixed_fraction"] == 0.0


def test_bootstrap_is_history_clustered_and_reproducible():
    x = np.zeros((3, 4, 8))
    x[:, :, :] = np.array([0.1, 0.2, 0.3, 0.4])[None, :, None]
    rng = np.random.default_rng(927032)
    resamples = rng.integers(0, 4, size=(1999, 4))
    a = _bootstrap_mean(x, resamples)
    b = _bootstrap_mean(x, resamples)
    assert a == b
    assert np.isclose(a["mean"], 0.25)
    assert a["n_finite_history_means"] == 4
