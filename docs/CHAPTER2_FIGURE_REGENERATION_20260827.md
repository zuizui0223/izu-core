# Chapter 2 figure regeneration

Updated: 2026-08-28

## Command

Install the repository development environment and run:

```bash
python -m pip install -e '.[dev]'
python scripts/generate_chapter2_manuscript_figures.py
```

The generator fails closed if deterministic recomputation no longer matches the frozen Chapter 2 gate summary.

## Outputs

The script generates four main SVG figures and five detailed supporting SVG figures under `figures/chapter2/`:

- `fig1_mechanistic_resolution_funnel.svg` — model possibilities → world response diversity → zero-contract identifiability gate → Izu resolution → Chapter 3 measurement handoff;
- `fig2_response_geometry.svg` — mean island-minus-mainland service across the 21-point starting-position grid;
- `fig3_proximal_why_hierarchy.svg` — fixed-surface drivers, response-matrix decomposition, directional filtering and downstream assurance;
- `fig4_global_to_izu_resolution.svg` — external admission/identifiability state beside raw and null-corrected Izu estimates;
- `figS2_conditional_why_diagnostics.svg` — fixed-surface parameter associations, baseline response decomposition and direction-specific local-filtering transitions.
- `figS3_external_prediction_readiness.svg` — source-native field availability across all 25 entries;
- `figS4_joint_regime_map.svg` — 48 joint Latin-hypercube points × 21 starting positions, displaying the mean response sign after sorting points by response regime;
- `figS5_local_context_threshold.svg` — total and directional response-sign changes across the local filtering-strength envelope;
- `figS6_assurance_sensitivity.svg` — magnitude improvement versus sign rescue across the 0–4× assurance envelope.

For local visual QA, the generator also writes PNG copies of the new Fig. 1, Fig. 3 and Fig. 4 plus Figs. S2 and S3; the review/submission archive uses the SVG.

It also writes the fully regenerated figure input payload to:

`data/results/chapter2_manuscript_figure_inputs_20260827.json`.

## Local verification during implementation

The same deterministic calculations were executed while implementing the generator and reproduced the frozen results:

- response geometry: 41 mixed-sign, 42 all-positive and 13 all-negative realizations among 96;
- joint 48-point design: 16 mixed, 22 all-positive and 10 all-negative mean geometries;
- mixed-sign realization fraction across joint points ranged from 1/24 to 22/24, with mean 0.4852430556;
- Fig. 2 reproduced the U-shaped mean geometry with positive responses through starting position 0.30, negative responses from 0.35 through 0.65, and positive responses from 0.70 through 1.00;
- Fig. 3 uses the committed conditional-WHY and context/assurance results directly rather than a separate tuned run;
- Fig. 4 uses the committed external-readiness and Izu structural-audit results directly;
- Fig. S2 reads the frozen conditional-WHY result only after all parent-result identity checks pass.

## Inference boundary

The figures visualize frozen synthetic model response geometry and sensitivity, external source readiness and focal Izu structural results. The sign-switch positions, filtering threshold, design-space frequencies, driver coefficients, variance shares, directional transition rates and assurance multiplier envelope are not empirical ecological estimates or causal field effects. The 25-entry panel is not predictive validation, and the Izu raw slope is not beyond-composition sorting or causal floral evolution.
