# Reproducing the Chapter 2 headline result

The shortest reviewer path is the frozen headline regression, not the historical acquisition workflow archive.

```bash
python -m pip install -e '.[dev]'
pytest -q tests/test_chapter2_frozen_headline_regression.py
pytest -q tests/test_gaussian_matching_kernel_equivalence.py tests/test_workflow_trigger_policy.py
```

The headline regression re-runs the 96 matched-community corrected primary draw using collision-free hierarchical RNG streams and checks the committed result with floating-point tolerances rather than byte equality. It protects the corrected primary-draw state counts **43 mixed / 45 positive / 8 negative** and decomposition **S = 0.0408685179, C = 0.6978123459, I = 0.2613191363**. A separate ensemble regression protects the six-seed baseline summary (**mixed median 45.5 [43–59], C median 0.7427 [0.6978–0.7873], I median 0.2282 [0.1864–0.2676]**) and the rank-crossover boundary (**4/6 seeds at k=4; 6/6 at k=8 and k=16**). The legacy offset-stream values remain archived for provenance but are superseded for active inference.

To reproduce the temporal-depth sensitivity directly from the six checksum-locked/public source datasets:

```bash
python -m scripts.run_chapter2_phi_timebin_rarefaction_from_locked_sources \
  --work-dir /tmp/chapter2-phi-rarefaction \
  --out data/results/chapter2_phi_timebin_rarefaction_20260922.json
```

This rebuilds the canonical source tables through the frozen adapters, rarefies every admitted system to six source-native time bins for 1,000 prespecified draws, and re-evaluates the full-plane and leave-one-source-out dispersion criteria.

For the full current Chapter 2 scientific gate, run the same six analysis steps as `.github/workflows/chapter2-scientific-gate.yml`:

```bash
python -m scripts.run_response_geometry_realization_stability --replicates 96 --seed 20260826 --out /tmp/response_geometry.json
python -m scripts.run_joint_response_transition_surface --points 48 --replicates 24 --seed 20260826 --out /tmp/joint_transition.json
python -m scripts.run_context_assurance_threshold_maps --replicates 12 --contexts 4 --lineages 24 --steps 120 --seed 20260826 --out /tmp/context_thresholds.json
python -m scripts.evaluate_chapter2_scientific_gate --phase1 /tmp/response_geometry.json --joint /tmp/joint_transition.json --thresholds /tmp/context_thresholds.json --out /tmp/chapter2_gate_decision.json
python -m scripts.audit_chapter2_interaction_kernel --out /tmp/interaction_kernel.json
python -m scripts.audit_chapter2_el_rank_crossover_generalization
```

Historical acquisition and diagnostic workflows are retained for provenance but are manual-only. Pull requests automatically run only `.github/workflows/ci.yml` and `.github/workflows/chapter2-scientific-gate.yml`; `tests/test_workflow_trigger_policy.py` enforces that boundary.
