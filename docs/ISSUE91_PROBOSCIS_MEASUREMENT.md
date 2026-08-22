# Issue #91 prospective proboscis measurement

## Current role

Historical 2017 Table S2 proboscis values are known to exist but are not yet recoverable in the current execution environment. That source-recovery block must not force the prospective Campanula pilot to use taxonomic/guild approximations.

For new field visitors, measure the trait directly and admit it as `measured_new` only under a source-matched protocol.

## Source-matched hierarchy

Hiraiwa & Ushimaru (2017) measured pollinator proboscis length in millimetres with digital calipers and calculated a mean for each species × site from five individuals, or all individuals when fewer than five were available.

The prospective admission rule therefore mirrors that hierarchy:

- one row = one independently measured visitor specimen;
- the primary unit is `visitor_taxon_id × site_id`;
- method must be `digital_caliper` for source-matched admission;
- target = five independent specimens per taxon × site;
- fewer than five can be admitted only when `all_available_at_site=yes` is explicitly recorded;
- otherwise the group remains visible but is not promoted to the FDQ trait lookup.

This is not a claim that five specimens are a universal biological precision target. It is a compatibility rule chosen to match the source trait construction.

## Template

Use:

`templates/field_pollinator_proboscis_measurement_template.csv`

Required fields include specimen and taxon IDs, site/event identity, numeric length in mm, method, instrument resolution, measurer, timezone-aware measurement time and the explicit `all_available_at_site` state.

Do not reuse one specimen under multiple specimen IDs. Preserve a voucher ID where feasible.

## Audit

```bash
python scripts/audit_field_proboscis_measurement.py \
  --measurements field_pollinator_proboscis_measurement.csv \
  --output-dir proboscis_measurement_audit
```

Outputs:

- `proboscis_taxon_site_summary.csv`
- `field_pollinator_trait_lookup_measured_new.csv`
- `summary.json`

Only ready taxon × site means are written into the trait-lookup output. Blocked groups do not receive an imputed number.

## Relationship to FDQ

The ready lookup rows can feed the strict Issue #91 FDQ audit:

```text
visitor bout counts
+ confirmed visitor_taxon_id
+ admitted site-specific proboscis mean
-> abundance-weighted Rao-Q FDQ
```

This leaves the existing service path unchanged:

```text
visitor_group -> SVD -> background-adjusted effective service
```

A visitor can therefore be usable for SVD/service while still being excluded from official FDQ until taxon resolution and trait admission are complete.

## Claim boundary

A `measured_new` proboscis mean is a prospective site-specific functional trait. It does not reconstruct the historical 2017 Table S2, prove visitor effectiveness, alter the reproductive-treatment contract, or identify historical Bombus-loss causation.
