# iNaturalist flower-photo candidate channel

## Purpose

Public photographs can help locate material for a **reviewed directional**
nectar-guide/spot comparison. They are not a random sample of flowers, a direct
island trait frequency, or a pollination observation.

The snapshot workflow therefore has three stages:

```text
raw iNaturalist API pages
  -> observation-level candidate table
  -> one-row-per-photo candidate inventory
  -> nearest-proxy review queue
  -> manual review
  -> source-locatable, directional constraint only when eligible
```

The raw API pages remain in the workflow artifact. The
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

## Proxy review queue

`trait_photo_proxy_review_queue.csv` adds the nearest and second-nearest
**declared island proxy point**, the two distances, and their gap. It is a
navigation aid for reviewer triage only.

```text
nearest declared proxy != island polygon
nearest declared proxy != confirmed island assignment
nearest declared proxy != population membership
```

The reviewer must inspect the original coordinate, positional accuracy, and
observation page before entering `reviewer_island_decision`. This explicitly
prevents the broad iNaturalist envelope from becoming an automatic island label.

## Run locally

```bash
python scripts/extract_inaturalist_trait_photo_candidates.py \
  --snapshot-root izu_inaturalist_candidate_snapshots \
  --output-csv izu_inaturalist_candidate_snapshots/trait_photo_candidates.csv \
  --output-md izu_inaturalist_candidate_snapshots/TRAIT_PHOTO_CANDIDATES.md

python scripts/build_inaturalist_photo_proxy_queue.py \
  --candidates izu_inaturalist_candidate_snapshots/trait_photo_candidates.csv \
  --proxy-config configs/izu_island_proxy_points.json \
  --output-csv izu_inaturalist_candidate_snapshots/trait_photo_proxy_review_queue.csv \
  --output-md izu_inaturalist_candidate_snapshots/TRAIT_PHOTO_PROXY_QUEUE.md
```

The Izu iNaturalist workflow runs both after a complete retrieval and uploads
the raw snapshot, candidate inventory, and reviewer queue as a 30-day artifact.

## Boundary

This channel can eventually add **ordinal trait evidence**. It cannot by itself
provide island trait prevalence, heritability, selection, historical trait loss,
or evidence that a pollinator group visited the focal flower.
