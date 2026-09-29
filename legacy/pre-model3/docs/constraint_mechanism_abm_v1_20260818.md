# Constraint-mediated pollination ABM v1 — 2026-08-18

## Purpose

This model is a **mechanistic hypothesis test**, not a new empirical evidence source.

The empirical mainline already supports three distinct layers:

1. pollination function is generally important for reproduction and is not island-specific;
2. oceanic insularity changes pollination-network opportunity space more strongly than continental insularity;
3. in the Izu gradient, lower functional diversity / trait matching is directly linked to lower pollination success.

The unresolved mechanistic question is why similar geographic constraint does **not** produce one universal floral or reproductive syndrome.

## Model question

Can a reduction in available pollinator partners and arrival opportunities, without hard-coding a single island syndrome, produce multiple interaction architectures while reproduction is maintained by different combinations of retained specialist matching, generalist/redundant partners, novel partner replacement, reproductive assurance, and gradual trait adjustment?

If yes, this supplies a plausible mechanism for the repository synthesis `constraint-mediated functional conservation`: the conserved object is reproductive function, while the ecological solution can diverge.

## Agents

Plants carry a one-dimensional floral matching trait, reproductive-assurance state, and realized reproduction. Pollinator types carry a matching trait, interaction breadth, and native versus introduced/replacement status.

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

Architecture labels are descriptive coarse states: concentrated dependency; complementary/redundant generalism; species-specific mosaic; novel-partner replacement; and assurance-dominated when no pollinators remain.

### P3 — functional conservation can coexist with architectural divergence
Some constrained runs should preserve moderate/high reproduction through distinct combinations of partner matching, replacement/generalization and reproductive assurance.

### P4 — falsification
If the oceanic scenario invariably collapses or invariably produces one architecture, the current minimal mechanism is insufficient. Additional processes would then be required rather than tuning the model until it reproduces the desired narrative.

## First mechanism screen

The predeclared v1 screen used 200 replicate runs per scenario, 120 steps, base seed `20260818`.

| scenario | mean final pollinator types | mean reproduction | mean assurance | observed final architectures |
|---|---:|---:|---:|---|
| mainland-like | 17.11 | 0.851 | 0.113 | mosaic 174; generalism 26 |
| continental island | 7.88 | 0.655 | 0.294 | mosaic 96; generalism 87; concentrated 17 |
| oceanic island | 2.115 | 0.490 | 0.934 | generalism 84; replacement 49; concentrated 44; assurance-dominated 20; mosaic 3 |

### Reading

P1 passes qualitatively: stronger opportunity constraint sharply reduces the surviving partner pool.

P2 also passes qualitatively: the oceanic-island scenario does not converge on one architecture. All five descriptive architecture states occur across the 200 runs.

P3 is **partially supported**, not confirmed. Reproduction declines with increasing constraint, but the constrained runs use several distinct mechanisms, and reproductive assurance rises strongly. The model therefore shows that a common opportunity constraint can generate divergent solutions without a universal island syndrome, but v1 does not yet demonstrate full conservation of reproductive performance under the strongest constraint.

P4 is not triggered: the oceanic scenario neither invariably collapses nor invariably produces one architecture.

This result is mechanistic compatibility only. It does not establish that the synthetic parameter values are realistic or that the simulated architecture frequencies match nature.

## Held-out empirical use

The current empirical island systems are **not parameter-fitting targets** in v1. Systems such as Canary, Galápagos, Seychelles, Hawaii, Ogasawara, Caribbean Gesneriaceae and the Izu gradient remain held out from parameter fitting.

The next model gate is not further tuning. It is to define an explicit mapping from source-native empirical quantities to broad model parameter ranges, then ask whether the same predeclared mechanism can recover held-out architecture/function classes without system-specific hand tuning.

## Claim boundary

ABM output cannot upgrade a partial empirical pathway to a full pathway, establish global prevalence of architecture classes, show that one architecture is caused by island geography, replace a missing reproductive-performance measurement, or count as independent evidence for the island comparison.

It can only test whether a proposed mechanism is capable of generating the observed class of patterns under predeclared constraints.
