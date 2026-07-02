# GBIF flower-photo candidate channel

## Purpose

GBIF occurrence search can return attached media for some records. These media
are useful only as **review leads** for the currently missing island-resolved
nectar-guide/spot channel. They are not field measurements, random floral
samples, pollinator observations, or evidence of a historical transition.

The GBIF workflow now produces:

```text
raw GBIF occurrence pages
  -> one media row per source occurrence image
  -> proxy-only geographic review queue
  -> blinded trait-review bundle for declared record types
  -> human review and non-binding directional draft
```

## What is retained

For each image-like GBIF media entry, the candidate table retains the GBIF
occurrence key, taxon returned by GBIF, date, coordinates and uncertainty,
basis of record, dataset key, image identifier, media type/format, license,
creator, references, and the source occurrence URL.

The workflow does not download or rehost images. It preserves source URLs and
license metadata so the reviewer can inspect provenance at the source.

## Source-specific triage

The review bundle does not treat GBIF `HUMAN_OBSERVATION` as equivalent to
an iNaturalist research-grade observation. They are source-specific declared
triage values.

For the initial GBIF run, only:

```text
basisOfRecord / quality_grade = HUMAN_OBSERVATION
```

is sent into the blinded guide-review bundle. `PRESERVED_SPECIMEN` media remain
in the candidate inventory but are not presumed to show a living open corolla,
so they are not sent to floral-guide scoring by default.

A GBIF `HUMAN_OBSERVATION` is still not automatically eligible. It must pass
all existing gates: coordinate accuracy, proxy-gap triage, geography review,
taxon review, open inner-corolla visibility, image comparability, and agreement
between two blind trait reviewers.

## Non-independence boundary

- Multiple media from one GBIF occurrence are one review unit.
- A GBIF image may be a re-published image from another platform, including a
  potential overlap with an iNaturalist record.
- Therefore GBIF and iNaturalist units must **not** be added as independent
  evidence across sources until the geographic reviewer checks source links,
dataset provenance, media references, and possible duplicate image URLs.

The current workflow keeps the GBIF bundle separate for precisely this reason.

## Commands

```bash
python scripts/extract_gbif_trait_photo_candidates.py \
  --snapshot-root izu_gbif_candidate_snapshots \
  --output-csv izu_gbif_candidate_snapshots/trait_photo_candidates.csv \
  --output-md izu_gbif_candidate_snapshots/TRAIT_PHOTO_CANDIDATES.md

python scripts/build_gbif_photo_proxy_queue.py \
  --candidates izu_gbif_candidate_snapshots/trait_photo_candidates.csv \
  --output-csv izu_gbif_candidate_snapshots/trait_photo_proxy_review_queue.csv \
  --output-md izu_gbif_candidate_snapshots/TRAIT_PHOTO_PROXY_QUEUE.md

python scripts/build_blinded_guide_photo_review_bundle.py \
  --proxy-queue izu_gbif_candidate_snapshots/trait_photo_proxy_review_queue.csv \
  --output-dir izu_gbif_candidate_snapshots/guide_photo_review_bundle \
  --allowed-quality-grade HUMAN_OBSERVATION
```

A generated directional draft remains a draft. It never updates
`data/guide_direction_constraints.csv` automatically.
