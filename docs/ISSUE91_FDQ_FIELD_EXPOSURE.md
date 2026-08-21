# Issue #91 strict FDQ field exposure

## Result first

The Issue #91 field stack can now keep two visitor-data uses separate:

```text
visitor_group
    -> SVD / rate-weighted effective service

visitor_taxon_id + numeric proboscis trait
    -> abundance-weighted Rao-Q FDQ
```

A group-level visitor record can remain scientifically useful for SVD/effective-service summaries without being admitted to FDQ.

## Why `visitor_taxon_id` is separate from `visitor_group`

The existing visitor-contact manifest used broad operational groups such as `bombus_ardens_confirmed`, `bombus_large_other` and `small_bee_non_bombus`. Those groups are useful in field scoring and SVD summaries, but the source-locked Izu FDQ is a species/taxon abundance-weighted quantitative trait-distance metric.

The visitor template therefore adds an optional:

```text
visitor_taxon_id
```

immediately after `visitor_group`.

For ordinary contact/SVD analysis the field may remain blank when taxonomic resolution is unavailable. For FDQ, every positive-abundance visit in an exposure unit must be taxon-resolved with `identification_confidence=confirmed`.

## Exposure unit

The primary prospective FDQ unit is:

```text
population_id × field_event_id × island_id × site_id
```

`population_id` is recovered by exact `plant_id` linkage to the dependency plant registry. A visit whose plant is outside that registry, or whose event/island/site disagrees with the plant registry, is rejected from the FDQ audit rather than reassigned.

## Trait join

Traits are read from:

`templates/field_pollinator_trait_lookup_template.csv`

The primary join key is:

```text
visitor_taxon_id × site_id
```

Admitted numeric statuses are:

- `source_exact_site`;
- `source_transfer_prespecified`;
- `measured_new`.

`trait_missing` is explicit and contains no hidden numeric value.

## Strict missing-data rule

Official FDQ is reported only if **both** conditions hold for the whole exposure unit:

1. every scored visit bout has confirmed taxon identity;
2. every positive-abundance taxon has an admitted numeric proboscis trait for that site.

If either fails, FDQ is withheld.

The audit still reports:

- total visit bouts;
- taxon-resolved visit bouts;
- trait-covered visit bouts;
- taxon-resolution fraction;
- trait-coverage fraction;
- unresolved visit IDs/groups;
- confirmed taxa missing numeric traits.

It does **not** drop unresolved/missing-trait visits and then renormalize the remaining abundance distribution. That would change the FDQ exposure construct in a way that could depend on which visitors happen to be easier to identify or measure.

## Rao-Q engine

`channel_id/fdq_exposure.py` implements the source formula:

```text
FDQ = sum_i sum_j p_i p_j |L_i - L_j|
```

with `p_i` the visitor-bout relative abundance inside the exposure unit and `L_i` the admitted proboscis length in mm.

Synthetic regression tests verify, among other cases:

- equal counts at 1 and 3 mm -> `FDQ = 1`;
- 3:1 counts at 2 and 10 mm -> `FDQ = 3`;
- a positive-abundance visitor lacking a trait blocks FDQ;
- non-strict diagnostics return coverage but **no renormalized FDQ**.

## CLI

```bash
python scripts/audit_field_fdq_exposure.py \
  --plants field_dependency_plant_registry.csv \
  --effort field_observation_effort.csv \
  --visits field_visitor_contact_manifest.csv \
  --traits field_pollinator_trait_lookup.csv \
  --output-dir field_fdq_audit
```

Outputs:

- `fdq_exposure_units.csv`
- `summary.json`

## Current empirical state

The execution path is ready, but the source-native historical proboscis table is not yet recovered in the repository. The current recovery audit remains:

```text
2024 named pollinator taxa = 209
numeric source-native proboscis traits recovered = 0
trait coverage = 0 / 209
Table S2 source values = known to exist, not yet recovered
```

Therefore this implementation makes future #91 rows immediately auditable, but it does not manufacture an empirical FDQ value today.

## Claim boundary

FDQ readiness and SVD/service readiness are different gates. A population can have valid visitor-group SVD and reproductive treatments while FDQ is withheld for incomplete taxon/trait coverage. Conversely, a complete FDQ exposure unit does not by itself identify reproductive dependency, historical selection, or Bombus-loss causation.
