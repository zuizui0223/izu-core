# Reproduce the Chapter 2 headline

The shortest reviewer path is deliberately small. From a clean checkout, run exactly these three commands:

```bash
python -m pip install -e '.[dev]'
python scripts/reproduce_chapter2_headline.py
python -m pytest -q tests/test_chapter2_frozen_headline_regression.py
```

The recomputation must recover the frozen matched-community baseline:

- realization classes: **41 mixed / 42 all-positive / 13 all-negative / 0 other** out of 96;
- starting-position share: **0.021832083717572618**;
- community-realization share: **0.8017383395125494**;
- state-by-community non-additivity share: **0.17642957676987792**.

The regression test compares recomputed floating-point quantities with `pytest.approx(rel=1e-9, abs=1e-12)` rather than byte identity, so harmless platform-level summation differences do not hide genuine model drift.

For the current Ecology Letters figures, run:

```bash
python scripts/render_chapter2_el_main_figures.py --out-dir data/results/chapter2_el_figures
```

This produces four SVG and four vector-PDF figures from the committed result objects.
