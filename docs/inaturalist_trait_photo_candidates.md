# iNaturalist flower-photo candidate channel

## Purpose

Public photographs can help locate material for a **reviewed directional**
nectar-guide/spot comparison. They are not a random sample of flowers, a direct
island trait frequency, or a pollination observation.

The snapshot workflow therefore has two stages:

```text
raw iNaturalist API pages
  -> observation-level candidate table
  -> one-row-per-photo candidate inventory
  -> manual review
  -> source-locatable, directional constraint only when eligible
```

The raw API pages remain in the workflow artifact. The new
`trait_photo_candidates.csv` is an index, not a derived trait dataset.

## Candidate schema and review gates

The extractor retains observation date, coordinates, positional accuracy, taxon
returned by iNaturalist, source observation URL, photo URLs, photo identifier,
and attribution/license metadata when supplied by the API.

Every photo starts as:

```text
corolla_inner_visibility = unreviewed
island_assignment_status = unreviewed
trait_eligibility = requires_independent_review
review_status = candidate
```

A reviewer must not change `trait_eligibility` to usable until all of the
following are recorded outside the raw API output:

1. the focal taxon remains appropriate after reviewing the observation;
2. geography supports the named island assignment rather than merely the broad
   Izu bounding rectangle;
3. the inner corolla and putative guide region are visible;
4. flower stage, angle, focus, and lighting permit the stated comparison;
5. photo license/attribution and the source URL are retained;
6. the claim is directional and source-locatable, for example
   `Oshima > Hachijo` under a declared guide region.

A photo of an exterior flower, a plant without an open corolla, or a poorly
localized observation remains a lead only. It must not become a row in
`data/guide_direction_constraints.csv`.

## Run locally

```bash
python scripts/extract_inaturalist_trait_photo_candidates.py \
  --snapshot-root izu_inaturalist_candidate_snapshots \
  --output-csv izu_inaturalist_candidate_snapshots/trait_photo_candidates.csv \
  --output-md izu_inaturalist_candidate_snapshots/TRAIT_PHOTO_CANDIDATES.md
```

The Izu iNaturalist workflow runs this after a complete retrieval and uploads
both the raw snapshot and the candidate inventory as a 30-day artifact.

## Boundary

This channel can eventually add **ordinal trait evidence**. It cannot by itself
provide island trait prevalence, heritability, selection, historical trait loss,
or evidence that a pollinator group visited the focal flower.
