# Chapter 2 figure regeneration

Updated: 2026-08-27

## Command

Install the repository development environment and run:

```bash
python -m pip install -e '.[dev]'
python scripts/generate_chapter2_manuscript_figures.py
```

The generator fails closed if deterministic recomputation no longer matches the frozen Chapter 2 gate summary.

## Outputs

The script generates four separate SVG figures under `figures/chapter2/`:

- `fig2_response_geometry.svg` — mean island-minus-mainland service across the 21-point starting-position grid;
- `fig3_joint_regime_map.svg` — 48 joint Latin-hypercube points × 21 starting positions, displaying the mean response sign after sorting points by response regime;
- `fig4a_local_context_threshold.svg` — total and directional response-sign changes across the local filtering-strength envelope;
- `fig4b_assurance_sensitivity.svg` — magnitude improvement versus sign rescue across the 0–4× assurance envelope.

It also writes the fully regenerated figure input payload to:

`data/results/chapter2_manuscript_figure_inputs_20260827.json`.

## Local verification during implementation

The same deterministic calculations were executed while implementing the generator and reproduced the frozen results:

- response geometry: 41 mixed-sign, 42 all-positive and 13 all-negative realizations among 96;
- joint 48-point design: 16 mixed, 22 all-positive and 10 all-negative mean geometries;
- mixed-sign realization fraction across joint points ranged from 1/24 to 22/24, with mean 0.4852430556;
- Fig. 2 reproduced the U-shaped mean geometry with positive responses through starting position 0.30, negative responses from 0.35 through 0.65, and positive responses from 0.70 through 1.00;
- Fig. 4 uses the committed final context/assurance threshold result directly rather than a separate tuned run.

## Inference boundary

The figures visualize frozen synthetic model response geometry and sensitivity. The sign-switch positions, filtering threshold, design-space frequencies and assurance multiplier envelope are not empirical ecological estimates.
