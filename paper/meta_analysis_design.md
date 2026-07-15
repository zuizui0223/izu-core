# Izu cross-lineage regime-transition test — prospective design

> **Current status:** `focal_three_channel_calibration_established_independent_holdout_blocked`.
> The machine-generated [`docs/CURRENT_EVIDENCE_STATE.md`](../docs/CURRENT_EVIDENCE_STATE.md)
> defines the empirical claim boundary. The fuller scientific design is
> [`docs/REGIME_TRANSITION_COMPARATIVE_DESIGN.md`](../docs/REGIME_TRANSITION_COMPARATIVE_DESIGN.md).

## Core question

Do independent Izu plant lineages repeatedly change at the same pollinator-service
boundary, or are their responses better described by smooth environmental clines,
lineage-specific histories, ecological filtering, or no ordered change?

The predeclared regime scaffold is:

```text
large Bombus -> B. ardens -> no effective Bombus
```

This scaffold is not assumed to be a causal distance axis. Climate, island area,
isolation, colonisation history, taxonomy, and observation effort remain explicit
competitors.

## Adopted focal calibration

The focal lineage is calibration only and never an independent replicate.

| channel | retained focal shape | interpretation boundary |
|---|---|---|
| floral size | continuous erosion | real morphology pattern; not a unique staged-loss marker |
| multilocus outcrossing | continuous erosion | direct mating-system estimate; not a declared first threshold |
| autonomous reproductive capacity | second-transition step | bagged capsule set; not realised selfing |

Nectar-guide and visible-signal analyses are excluded. They supply no current
response direction or breakpoint.

## Competing response shapes

For each eligible lineage-response family, compare:

1. `none`;
2. `cline`;
3. `first_step`;
4. `second_step`;
5. `two_step`; and
6. `environment_history`.

The same shape vocabulary may be applied through different native likelihoods:
continuous, count, proportion, Bernoulli, ordinal, multistate, interaction, or
occupancy. Effects from different domains are not pooled onto one artificial scale.

## Presence/absence route

Presence/absence is admissible only as an occupancy or state response.

### Species occupancy

A detection-aware model can test whether specialist-like mainland plants are less
likely than open generalists to occupy islands beyond a regime boundary:

```text
occupancy ~ regime * dependency_class
          + climate + area + isolation + history
          + lineage/phylogeny + observation_effort
```

This tests ecological filtering or range truncation. It is not evidence that a
floral or mating-system trait evolved within an island population.

### Binary trait state

Source-native states such as SI/SC, autonomous reproduction absent/present, or
restrictive/open floral architecture can be analysed with Bernoulli or multistate
models. The state definition must be fixed before inspecting the island response.

## Generalist negative controls

Open-generalist lineages are controls for a **shared specialist breakpoint**. They
are not assumed to be absolutely invariant. The main falsification test is a
dependency-class by boundary interaction, preferably evaluated with lineage-level
leave-one-out validation.

A convincing pattern would require specialist-like lineages to select the same
step more often than generalists, while the contrast survives environment/history
and observation-process sensitivity.

## Mating-system and specialisation transitions

Keep these channels distinct:

- self-incompatibility -> self-compatibility;
- autonomous reproduction;
- realised selfing;
- de-specialisation / functional broadening;
- replacement by an alternative specialised guild; and
- interaction loss before morphological change.

“Reverse evolution” is not used as a model state. SI loss is a specific compatibility
transition, while specialist-to-generalist change is multidimensional ecological
rewiring.

## Independent comparison unit

One lineage x one prespecified response family is one comparison unit. Multiple
islands, populations, flowers, images, or correlated traits within that unit are
observations rather than independent evolutionary replications.

Admission requires:

1. accepted taxonomy and a defensible within-lineage comparison;
2. named localities mapped to regimes;
3. source-native response and sampling unit;
4. fixed response definition and dependency classification;
5. no unresolved taxon/variety-by-geography confounding; and
6. separation of calibration, positive holdout, negative control, context, and pending records.

The executable admission table is
`data/predictive_meta/regime_transition_registry.csv`.

## Source-native queue

- *Weigela coraeensis*: recover original trait tables, uncertainty, n, and locality mapping before assigning a response.
- *Ligustrum ovalifolium*: recover population-level floral tables and island mapping; current abstract-level directions are not shape-test effects.
- *Lilium auratum*: retain as an alternative Lepidoptera mechanism because variety and geography are confounded.
- *Clerodendrum izuinsulare*: retain as a between-taxon contextual comparison.

## Current stop rules

Do not:

- describe the project as a completed Izu-flora meta-analysis;
- adopt any unfinished nectar-guide result;
- infer pollinator effectiveness from visitor identity or raw occurrence;
- treat occupancy as a floral phenotype;
- call bagged capsule set realised selfing;
- equate SC with autonomous selfing;
- reject `environment_history` using regime contrasts alone;
- reopen the specialist photo holdout without biological-positive-control validation; or
- count calibration, contextual taxa, images, or multiple traits as independent replications.

## Next sequence

1. validate and expand the regime-transition registry;
2. recover and source-lock *Weigela* and *Ligustrum* population tables;
3. screen source-native SI/SC, autonomous reproduction, floral architecture,
   effective-guild, and occupancy channels;
4. implement the explicit environment/history competitor;
5. run native-likelihood shape comparisons with lineage-level validation; and
6. proceed to hierarchical synthesis only after enough independent lineages pass
   the evidence gates.
