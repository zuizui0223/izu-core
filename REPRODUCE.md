# Reproducing the Chapter 2 headline result

The shortest reviewer path is the frozen headline regression, not the historical acquisition workflow archive.

```bash
python -m pip install -e '.[dev]'
pytest -q tests/test_chapter2_headline_freeze_regression.py
pytest -q tests/test_gaussian_matching_kernel_equivalence.py tests/test_workflow_trigger_policy.py
```

The headline regression re-runs the 96 matched-community baseline from the frozen design and checks the committed result with floating-point tolerances rather than byte equality. It protects the state counts **41 mixed / 42 positive / 13 negative** and the normalized decomposition **S = 0.0218320837, C = 0.8017383395, I = 0.1764295768**.

For the full current Chapter 2 scientific gate, run:

```bash
python -m scripts.run_response_geometry_realization_stability --replicates 96 --seed 20260826 --out /tmp/response_geometry.json
python -m scripts.audit_chapter2_interaction_kernel --out /tmp/interaction_kernel.json
python -m scripts.audit_chapter2_el_rank_crossover_generalization
```

Historical acquisition and diagnostic workflows are retained for provenance but are manual-only. Pull requests automatically run only `.github/workflows/ci.yml` and `.github/workflows/chapter2-scientific-gate.yml`; `tests/test_workflow_trigger_policy.py` enforces that boundary.
