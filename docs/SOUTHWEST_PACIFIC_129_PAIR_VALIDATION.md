# Southwest Pacific 129-pair external validation

## Role in the Izu programme

The Southwest Pacific dataset is an external morphology validation layer, not a
replicate of the Izu Bombus-regime experiment. It asks whether island flower-size
responses are universally directional or instead depend on the starting trait
state and context across independent colonisation events.

Article DOI: `10.1093/aob/mcaf005`  
PMCID: `PMC12445859`

The checked S2 workbook contains 129 source-defined mainland–island comparison
rows in the `Flower dataframe` sheet. The analysis workbook SHA-256 is
`452c6f83143eb17e8249faae9659386be7b162f93742c4e137921952a9b88677`.
The Europe PMC recovery lane is required to reproduce the existing SHA-256 lock
before source-native analysis is admitted.

## Source-row state

The released workbook contains:

- 89 source-coded animal-pollinated rows;
- 39 source-coded wind-pollinated rows;
- one unresolved pollination-mode row;
- valid flower-size values for 88 animal and 38 wind rows.

The difference from the counts stated in the article is retained as a source
reconciliation issue and is not repaired by inventing undocumented exclusions.
Pollination mode is a source-provided broad category; it is **not** an effective
pollinator-dependency or specialist/generalist measurement.

## Starting-size dependence

The transparent source-native OLS analysis uses

```text
log10(island flower size / mainland flower size)
    ~ log10(mainland flower size)
```

and reports cluster-bootstrap uncertainty.

| pollination mode | n | slope | island-cluster 95% interval |
|---|---:|---:|---:|
| animal | 88 | **-0.15099** | **[-0.29979, -0.07390]** |
| wind | 38 | -0.07611 | [-0.14840, 0.10946] |

The animal slope also remains negative under family resampling and in every
leave-one-island sensitivity. However, the animal mean log response ratio is
near zero. Therefore the supported pattern is **starting-value dependence**, not
universal island dwarfism: larger mainland flowers tend to shrink
proportionally, while small flowers can increase.

## Archipelago heterogeneity

All ten source-defined island groups contain at least one valid animal-pollinated
comparison. Six groups meet the predeclared minimum of five valid pairs for a
within-group descriptive slope.

- estimable slope groups: 6;
- negative point slopes: 6/6;
- positive point slopes: 0/6;
- slope range: `-0.52091 .. -0.01172`;
- median slope: `-0.12404`;
- island-group mean log response ratio: negative in 4 groups, positive in 6;
- mean-response range: `-0.18811 .. +0.13554`.

Thus the negative starting-size relationship is geographically broad among the
groups with enough pairs, while the **mean direction of flower-size change is
not shared**. These island-group rows are robustness diagnostics, not ten
independent experiments or ten effect-registry entries.

## Direct animal-versus-wind contrast

A key guard is to test the between-mode difference directly rather than infer it
from `animal p < 0.05` and `wind p > 0.05`.

Observed slopes:

```text
animal = -0.15099
wind   = -0.07611
animal - wind = -0.07488
```

Bootstrap intervals for the slope difference are:

| resampling unit | median difference | 95% interval |
|---|---:|---:|
| individual colonisation event | -0.07788 | [-0.26479, +0.11882] |
| island group | -0.08827 | [-0.38327, +0.04550] |
| taxonomic family | -0.07051 | [-0.31417, +0.24219] |

All three intervals include zero. The checked result therefore sets
`robust_mode_difference = false`.

This does **not** erase the well-supported negative animal starting-size slope.
It means the present source does not provide a robust direct estimate that the
animal slope is more negative than the wind slope. Stratum-specific significance
must not be mistaken for evidence of a significant interaction.

## Implication for the Izu hypothesis

The Southwest Pacific system strengthens a specific external prediction:

> island floral responses are conditional and response-shape dependent rather
> than a single directional island syndrome.

It does **not** independently validate `effective dependency × functional
pollinator environment`, because the source records pollination mode rather than
direct effective dependency. Its main value for Izu is therefore as an
adversarial morphology benchmark: even across 129 independent colonisation
events, mean flower-size shifts can change sign among island groups while a
starting-state-dependent response remains.

## Effect-registry boundary

Three Southwest Pacific summaries have compatible within-source uncertainty and
are retained as potential future effect rows:

1. animal-pollinated starting-size slope;
2. wind-pollinated starting-size slope;
3. animal-pollinated mean floral-display log ratio.

They are not pooled with Wanshan–Yongxing visitation or partner-turnover effects.
The current cross-archipelago registry has two external system clusters with
model-eligible rows, but **zero effect families represented in two independent
systems**, so formal cross-system synthesis remains closed.

## Claim boundary

Supported:

- conditional flower-size response tied to mainland starting size in the animal
  subset;
- broad negative point slopes among adequately sampled island groups;
- heterogeneous mean flower-size responses among island groups;
- no robust direct animal-versus-wind slope difference under event-, island-, or
  family-level bootstrap.

Not supported by this source:

- effective pollinator dependency;
- specialist-versus-generalist moderation;
- a universal shrinkage direction;
- a causal pollinator mechanism;
- a causal geological-origin effect;
- historical Bombus causation in Izu.
