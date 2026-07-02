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
  -> origin-platform hint and proxy-only geographic review queue
  -> provenance-filtered blinded trait-review bundle
  -> human review and non-binding directional draft
```

## What is retained

For each image-like GBIF media entry, the candidate table retains the GBIF
occurrence key, taxon returned by GBIF, date, coordinates and uncertainty,
basis of record, dataset key, image identifier, media type/format, license,
creator, references, and the source occurrence URL.

The workflow does not download or rehost images. It preserves source URLs and
license metadata so the reviewer can inspect provenance at the source.

`origin_platform_hint` is also recorded. The current positive label,
`iNaturalist_republication`, requires an explicit `inaturalist` string in the
media identifier or its references field. It is high-specificity duplicate
evidence. The negative label, `not_flagged_as_iNaturalist`, is **not** proof
that a GBIF record is independent of other sources.

## Source-specific triage

The review bundle does not treat GBIF `HUMAN_OBSERVATION` as equivalent to
an iNaturalist research-grade observation. They are source-specific declared
triage values.

For the initial GBIF run, only:

```text
basisOfRecord / quality_grade = HUMAN_OBSERVATION
```

is eligible for the blinded guide-review bundle. `PRESERVED_SPECIMEN` media
remain in the candidate inventory but are not presumed to show a living open
corolla, so they are not sent to floral-guide scoring by default.

Before the GBIF bundle is built, every explicit iNaturalist republication is
written to `excluded_iNaturalist_republication_rows.csv` and excluded from the
parallel GBIF review bundle. It stays in the candidate inventory for audit
purposes. A retained row still requires all ordinary gates: coordinate accuracy,
proxy-gap triage, geography review, taxon review, open inner-corolla visibility,
image comparability, and agreement between two blind trait reviewers.

## Initial live result

The first live GBIF run found four `Campanula microdonta` human-observation
records eligible for the geographic triage gates: three nearest the Oshima
proxy and one nearest the Hachijo proxy. All four had explicit iNaturalist media
URLs or references. They are therefore republications of the existing
platform's candidate stream, not four new independent observations. The
provenance-filtered GBIF bundle correctly contains no independent human-
observation units from this initial snapshot.

The same artifact retains several preserved-specimen images, including Hachijo
localities, as source-linked catalog material. They are not living-flower
nectar-guide evidence under the present protocol.

## Non-independence boundary

- Multiple media from one GBIF occurrence are one review unit.
- An explicit iNaturalist republication is excluded from the parallel GBIF
  blind bundle because it belongs to the iNaturalist source lane.
- Unflagged GBIF records are not automatically independent; the geographic
  reviewer still checks source links, dataset provenance, media references, and
  possible duplicate image URLs before any cross-source combination.

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

python scripts/build_gbif_blinded_guide_review_bundle.py \
  --proxy-queue izu_gbif_candidate_snapshots/trait_photo_proxy_review_queue.csv \
  --output-dir izu_gbif_candidate_snapshots/guide_photo_review_bundle
```

A generated directional draft remains a draft. It never updates
`data/guide_direction_constraints.csv` automatically.
