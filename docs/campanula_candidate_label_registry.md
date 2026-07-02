# Campanula candidate-label registry

## Why the registry exists

Public databases may expose the same biological entity under an exact focal
name, a broader aggregate name, or a historical infraspecific label. Treating
all of those searches as the same taxonomic assertion would create an avoidable
error: the search term would silently become the identification.

The registry keeps three operations separate:

```text
query label
  -> candidate discovery
  -> geographic and focal-taxon review
  -> only then, optional entry into blinded floral-trait review
```

It does not resolve synonymy or establish which label is currently accepted.

## Declared roles

| role | use in this repository | automatic focal trait route? |
|---|---|---|
| `focal_exact` | ordinary focal candidate discovery | only after manual taxon review |
| `broader_aggregate` | find possible focal observations stored under a broad name | no |
| `historical_record_label` | search for records filed under a label seen in retained source metadata | no |

The current historical record label is `Campanula punctata var. microdonta`.
Its registry entry records that the label occurred in a retained GBIF candidate
record. It does **not** assert that the label is accepted, synonymous, or
interchangeable with the focal entity.

## Record-level audit

`audit_campanula_candidate_labels.py` runs after the iNaturalist candidate and
proxy queues are created. It produces two outputs:

- `campanula_label_candidate_records.csv`: one source record even when the same
  observation appears under several declared search labels;
- `campanula_label_audit_summary.csv`: query-label coverage, Hachijo-proxy
  counts, and cross-query overlap.

This avoids counting one public observation repeatedly simply because it is
retrieved by several taxon-name queries.

## Routing rule

A record discovered solely by `broader_aggregate` or
`historical_record_label` remains:

```text
candidate_only_do_not_send_to_focal_blind_review_without_explicit_taxon_promotion
```

Promotion requires manual geographic and focal-taxonomic review. The registry
never writes a taxonomic decision into a model input and never edits
`data/guide_direction_constraints.csv`.

## Interpretation boundary

A zero result for a query label is a result of the named API query within the
broad Izu bounding rectangle. It is not evidence that the label or focal entity
is absent from an island. A positive hit under a broader/historical label is a
lead, not evidence of island occurrence or floral trait state.
