# Constraint-mediated pollination ABM v1 — 2026-08-18

## Purpose

This model is a **mechanistic hypothesis test**, not a new empirical evidence source.

The empirical mainline already supports three distinct layers:

1. pollination function is generally important for reproduction and is not island-specific;
2. oceanic insularity changes pollination-network opportunity space more strongly than continental insularity;
3. in the Izu gradient, lower functional diversity / trait matching is directly linked to lower pollination success.

The unresolved mechanistic question is why similar geographic constraint does **not** produce one universal floral or reproductive syndrome.

## Model question

Can a reduction in available pollinator partners and arrival opportunities, without hard-coding a single island syndrome, produce multiple interaction architectures while reproduction is maintained by different combinations of:

- retained specialist matching;
- generalist/redundant partners;
- novel partner replacement;
- reproductive assurance;
- gradual trait adjustment?

If yes, this supplies a plausible mechanism for the repository synthesis `constraint-mediated functional conservation`: the conserved object is reproductive function, while the ecological solution can diverge.

## Agents

### Plants
Each plant has:

- a one-dimensional floral matching trait;
- reproductive-assurance capacity;
- realized reproduction in the current step.

### Pollinators
Each pollinator type has:

- a matching trait;
- interaction breadth;
- native versus introduced/replacement status.

The model is intentionally minimal. It does not currently simulate explicit population genetics, species abundances, spatial coordinates, nectar guides, or phylogeny.

## Opportunity-space scenarios

The three scenarios are not empirical parameter estimates. They are ordered mechanism probes.

- `mainland_like`: larger partner pool, higher arrival, lower partner loss;
- `continental_island`: intermediate opportunity constraint;
- `oceanic_island`: smaller pool, lower arrival, higher partner loss, more generalist and replacement opportunities.

The ordering is motivated by the empirical comparative layer, especially mainland / continental-island / oceanic-island network differences. The numerical values are deliberately synthetic and must not be interpreted as fitted estimates.

## Predeclared qualitative predictions

### P1 — opportunity constraint
Increasing insular constraint should reduce the expected number of available pollinator types.

### P2 — no universal architecture
The model should be able to produce more than one final architecture without assigning an architecture directly from geography.

Architecture labels are descriptive coarse states:

- concentrated dependency;
- complementary/redundant generalism;
- species-specific mosaic;
- novel-partner replacement;
- assurance-dominated when no pollinators remain.

### P3 — functional conservation can coexist with architectural divergence
Some constrained runs should preserve moderate/high reproduction through distinct combinations of partner matching, replacement/generalization and reproductive assurance.

### P4 — falsification
If the oceanic scenario invariably collapses or invariably produces one architecture, the current minimal mechanism is insufficient. Additional processes would then be required rather than tuning the model until it reproduces the desired narrative.

## Held-out empirical use

The current empirical island systems are **not parameter-fitting targets** in v1. After qualitative behavior is validated, systems such as Canary, Galápagos, Seychelles, Hawaii, Ogasawara, Caribbean Gesneriaceae and the Izu gradient can be used as held-out architecture/function patterns.

A future calibration step may estimate broad parameter ranges from source-native network metrics, but only after the mapping from empirical quantities to model parameters is explicitly registered.

## Claim boundary

ABM output cannot:

- upgrade a partial empirical pathway to a full pathway;
- establish global prevalence of architecture classes;
- show that one architecture is caused by island geography;
- replace a missing reproductive-performance measurement;
- count as independent evidence for the island comparison.

It can only test whether a proposed mechanism is capable of generating the observed class of patterns under predeclared constraints.
