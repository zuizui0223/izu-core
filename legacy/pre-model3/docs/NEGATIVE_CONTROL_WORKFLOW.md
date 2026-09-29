# Specialist–generalist negative-control workflow

This workflow tests whether a predeclared island or pollinator boundary is selectively expressed in specialist lineages rather than shared by all plants.

## Input

One row is one mainland–island contrast for one lineage and trait. `matched_set` links specialist and generalist contrasts chosen before inspecting their effects. Matching should prioritize growth form, flowering season, island coverage and approximate floral scale.

Required columns:

- `lineage`
- `group`: `specialist` or `generalist`
- `trait`
- `mainland_mean`, `island_mean`
- `mainland_se`, `island_se`
- `boundary`
- `matched_set`

## Run

```bash
python scripts/run_negative_control.py examples/negative_control/contrasts.csv \
  --output results/negative-control.json \
  --equivalence-margin 0.5 \
  --specialist-effect -1.0 \
  --generalist-effect 0.0 \
  --replicates 2000
```

The equivalence margin must be declared on the original trait scale before inspecting group effects.

## Interpretation

Each lineage receives one of three labels:

- `changed`: its confidence interval lies beyond the practical-equivalence region;
- `equivalent`: its full confidence interval lies inside that region;
- `inconclusive`: neither change nor equivalence is resolved.

A non-significant contrast is never automatically called unchanged.

The output also reports the pooled specialist-minus-generalist contrast and a simulation audit. The audit estimates how often the current precision would support the selective-response pattern, falsely show a shared generalist change, or remain inconclusive under declared true effects.

## Scientific boundary

This analysis tests selective compatibility with a shared boundary. It does not prove that Bombus loss caused a trait change. Distance, climate, island area, disturbance, population history and unmatched lineage biology remain competing explanations and should be added as separate predictors when enough lineages are available.
