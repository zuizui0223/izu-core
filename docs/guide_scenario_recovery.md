# Competing guide-scenario recovery

## Purpose

The six-layer guide architecture is not itself an analysis. This module turns
it into competing restricted scenario classes and asks a pre-data question:

> Given the observations we plan to collect, which guide-evolution scenarios
> would remain compatible, and which additional intermediate observation would
> actually distinguish them?

## Scenario classes

| Scenario | Active guide-linked route | What it deliberately excludes |
|---|---|---|
| `null` | none | independent guide effects and guide cost |
| `visit_attraction` | guide -> visit rate -> maternal outcross seed | handling, paternal, assurance, spatial routes |
| `handling` | guide -> legitimate contact -> maternal outcross seed | visit, paternal, assurance, spatial routes |
| `paternal` | guide -> pollen export/siring | maternal guide pathways, assurance, spatial routes |
| `assurance` | assurance/selfing path | guide-dependent visit and handling pathways |
| `spatial` | destination-specific recruitment | guide-dependent visit/handling and assurance paths |
| `mixed` | all declared paths | no route is excluded; interpret sparingly |

These are **restricted mechanism classes**, not the only biological realities.
`mixed` is intentionally flexible and should not be treated as a winning
explanation merely because it can fit more patterns.

## Synthetic recovery standard

A model extension should pass four checks before field data enter it:

1. Generate virtual observations from a named scenario without passing that
   name to the recovery function.
2. Supply only a coarse terminal outcome, such as total contribution, and
   confirm that multiple mechanism classes remain compatible where they should.
3. Add the intermediate observables predicted by the truth scenario.
4. Confirm that the compatible set shrinks to the true restricted scenario, or
   explicitly record the irreducible ambiguity.

`examples/synthetic_scenario_recovery.py` demonstrates this with a virtual
visit-attraction system. A broad total-contribution interval retains multiple
scenarios. Adding expected visits and outcross viable seed output recovers the
visit-attraction class.

This does not validate the model biologically. It validates that the design
logic can recover a known virtual mechanism under its own assumptions.

## Observations supported now

Year-level observations:

```text
expected_visits
outcross_viable_seeds
selfed_viable_seeds
female_recruits
paternal_contribution
total_contribution
```

Summary-level observation:

```text
geometric_mean_contribution
```

Each observation is an interval. The interval must be chosen from planned
sampling precision, not after seeing which width produces a preferred result.

## Recommended first real-data analysis

Do not start with all seven scenarios and all six layers. For the first Izu
campaign, use a small declared comparison:

```text
M0 null guide
M1 visit-attraction
M2 handling/pollen-placement
M4 assurance compensation
```

Then collect the minimal intermediate quantities needed to separate them:

- guide contrast, flower display, nectar, plant condition;
- guild-resolved visits;
- legitimate contact or stigma pollen deposition per visit;
- fruit/seed output and, where feasible, outcross versus selfed component;
- a short explicitly declared recruitment window.

Paternal, temporal, genetic-plasticity, and spatial scenarios should be
activated only once their required data exist. They are not optional confounder
lists; each is a separate claim with a separate measurement burden.

## Interpretation

A surviving scenario means only:

> This scenario class is compatible with the declared observations, parameter
> bounds, and life cycle.

It does not mean the scenario is historically true, uniquely causal, or
selected in nature. A rejected scenario is only as meaningful as the
measurement interval, model restriction, and calibration that produced the
rejection.