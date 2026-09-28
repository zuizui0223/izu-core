# Source-level island-order alternative

## Purpose

`isolation_order` is a fifth source-level candidate added to make the existing
pollinator-bridge comparison symmetric. It uses the same direct-table
likelihoods as the other source-level candidates, but makes predictions from the
already locked `region_order` scaffold rather than pollinator availability.

It is **not** a reconstruction of colonization history, a continuous isolation
distance, or evidence that geographic isolation caused floral evolution.

## Fixed input

The input is the existing `region_order` column in
`data/inoue_literature_island_traits.csv`:

```text
Honshu = 0; Oshima = 1; Toshima = 2; Niijima = 3;
Kozushima = 4; Miyake = 5; Hachijo = 6
```

The values are rescaled to 0–1 inside each comparison. Every included island
must have one unique finite value. Missing, duplicate, constant, or post hoc
reordered values cause the model to stop rather than filling or optimizing the
order.

## Restricted proxy mechanism

The scenario has the following sign restrictions:

```text
higher region_order -> autonomous assurance increases
higher region_order -> expected outcrossing decreases
higher region_order -> bagged capsule set increases through assurance
higher region_order -> flower length decreases
higher region_order -> latent guide decreases
```

The last pathway is only a prediction for future guide data; no current
island-resolved guide channel is used. Pollinator availability fields are not
read by this candidate's prediction function.

## Shared observation model

All five source-level candidates are scored against the same source rows:

- population-level outcrossing estimates on the logit scale, with reported SD/n
  plus a declared residual;
- bagged flower/capsule counts with beta-binomial overdispersion;
- common-garden flower-length means with SEM plus between-population residual;
- reviewed ordinal guide comparisons when they exist.

The ordinal candidate also enters the same leave-one-channel-out analysis,
observation-scale sensitivity grid, seed sweep, importance-ESS diagnostic, and
profile search as the original four candidates.

## Interpretation boundary

A favorable score can only mean that this fixed ordinal proxy is more compatible
with the retained direct summaries under the declared priors and likelihoods.
It cannot establish a historical dispersal route, pollinator extinction,
pollination effectiveness, or causation by isolation.

The useful result of this addition is not a new narrative by itself. It is a
fairer discrimination test: whether the bridge model still outperforms an
ordered-island explanation after both are evaluated with the same source-row
uncertainty model.
