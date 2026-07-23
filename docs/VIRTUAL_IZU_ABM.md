# Virtual Izu ABM v0

This model constructs a declared synthetic archipelago inspired by the research structure of the Izu Islands. It does not impute missing empirical measurements and does not estimate real historical parameters.

## Agents and environment

- Plant individuals are agents.
- Pollinators are island-level functional services.
- Each plant carries specialization, floral matching, autonomous selfing, dispersal, environmental optimum and inbreeding depression.
- Islands carry ordered position, environment, carrying capacity and pollinator-service states.

The default scaffold has a mainland large-Bombus state, an Oshima-like `ardens` bridge, and southern non-`ardens` islands.

## Scenarios

- `environment_only`
- `distance_only`
- `pollinator_regime`
- `environment_plus_pollinator`
- `small_bee_substitution`

The same founders and seed can be run under each mechanism. Differences among outputs therefore arise from declared scenario rules rather than post-hoc selection of empirical lineages.

## Generation cycle

1. Environmental survival is evaluated.
2. Outcross service is determined by plant specialization, floral match and island pollinator service.
3. Autonomous reproduction contributes when pollination is low and is discounted by inbreeding depression.
4. Offspring disperse among islands.
5. Traits mutate slightly.
6. Island carrying capacities are applied.

## Run

```bash
python scripts/run_virtual_izu_abm.py \
  --scenario environment_plus_pollinator \
  --generations 80 --founders 180 --seed 1 \
  --output results/virtual-izu-abm.json
```

## v0 outputs

- total population;
- extant lineage count;
- lineages reaching islands south of the declared `ardens` boundary;
- island-level richness;
- mean specialization;
- mean autonomous selfing;
- trajectory snapshots at generation 0, midpoint and final generation.

## Claim boundary

The v0 model is a mechanistic sandbox and identifiability engine. A realistic-looking pattern is not evidence that the corresponding process generated the real Izu flora. The next layer should run replicated scenario ensembles and ask whether observation models can recover the true generating scenario.
