# Constrained life-history simulation

## Purpose

This module is the next layer after the `W = F E` readiness protocol.  It is
for comparing *declared* mechanistic explanations when some quantities are not
directly measurable, such as an attraction-maintenance cost, the viability of
selfed seed, or the efficiency of delayed-selfing compensation.

It does **not** infer hidden costs from a floral phenotype alone and it does
not turn a successful reconstruction into proof of a mechanism.

The output is a set of compatible parameter settings:

```text
observed intervals + declared life cycle
    -> parameter settings that reproduce every declared observation
    -> parameter settings rejected by at least one observation
```

The scientific result is therefore a constraint statement, for example:

> Given the declared life cycle and measurement intervals, a no-cost attraction
> model cannot reproduce the island pattern, whereas attraction costs between
> the retained range can.

Not:

> The true attraction cost equals one selected simulation value.

## Declared minimal life cycle

For a trait state `(A, R)` and regime `(P, E_env)`:

1. attraction and assurance investments reduce a potential viable-seed budget;
2. pollinator service `P` and attraction set the outcrossed fraction;
3. assurance converts a share of not-outcrossed ovules into viable selfed seed;
4. establishment maps local viable seed output `F` to retained recruits `W`.

```text
trait and regime -> F (local viable seed output) -> E (establishment) -> W
```

The initial model intentionally keeps trait effects inside `F`.  A direct
trait-to-establishment effect must not be added just because a model needs it
to fit; it needs an independent biological rationale and a measurable
observation target.

## What must be measured

A simulation case may constrain any subset of:

- outcross viable seeds;
- selfed viable seeds;
- total local viable seed output `F`;
- establishment probability `E`;
- retained recruits `W`.

A case must contain at least one predeclared interval, but weak cases produce
wide compatible sets.  To distinguish pollinator-attraction from assurance
compensation within `F`, use at least one observable that separates outcrossed
and selfed seed production, such as treatment-specific seed set, paternity,
or a validated mating-system measure.

## Example workflow

```python
from channel_id.life_history import (
    Metric, ObservationInterval, ParameterGrid, Regime,
    SimulationCase, TraitState, retain_compatible_candidates,
)

island_white = SimulationCase(
    name="island_white",
    trait=TraitState(attraction=0.2, assurance=0.8),
    regime=Regime(pollinator_service=0.25, establishment_multiplier=1.0),
    observations=(
        ObservationInterval(Metric.LOCAL_VIABLE_SEED_OUTPUT, 2.0, 3.0),
        ObservationInterval(Metric.RETAINED_RECRUITS, 0.3, 0.6),
    ),
)

grid = ParameterGrid(
    seed_budget=(4.0, 5.0),
    baseline_outcross_fraction=(0.1,),
    attraction_pollination_gain=(0.6, 1.0),
    attraction_cost=(0.0, 0.5, 1.0),
    assurance_cost=(0.0, 0.3),
    selfing_viability=(0.4, 0.7),
    baseline_establishment=(0.15, 0.2),
)

compatible = retain_compatible_candidates(grid, [island_white])
```

The next analysis should report the number and ranges of compatible candidates,
then ask which new measurement would most reduce that range.  It should not
select the first compatible candidate as a biological estimate.

## Required discrimination tests before a field claim

For each intended claim, write down:

1. **Competing mechanisms.** For example: attraction loss, delayed-selfing
   compensation, or establishment advantage.
2. **Observed target.** Exact quantities and uncertainty intervals to be
   reproduced across both island and mainland regimes.
3. **Rejection rule.** What prediction excludes a candidate class?
4. **Measurement priority.** Which future observation would distinguish the
   remaining compatible mechanisms?

Only then should the model leave the incubator as a field-facing analysis.