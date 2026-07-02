# Blinded public-photo review for nectar-guide/spot evidence

## Why the layer exists

The candidate workflows now retrieve source-linked flower images from both
iNaturalist and GBIF. Candidate photographs are not measurements. The key
failure modes are:

1. a nearest island proxy is silently mistaken for island membership;
2. a reviewer knows the hypothesized island gradient and scores photos toward
   the expected direction;
3. several images from one source record are counted as several flowers;
4. a re-published image is counted again across data sources.

The review bundle prevents the first three directly and keeps source identity
visible to the geographic reviewer for duplicate checking.

## Unit of analysis and source-specific triage

**One source record = one review unit.** Multiple linked images are alternative
views, retained as a semicolon-delimited bundle. They are never independent
replicates.

The default iNaturalist triage gate is:

- focal target: `campanula_microdonta`;
- `research` quality grade;
- positional accuracy at or below 100 m;
- distance to the nearest declared island proxy at least 20 km smaller than the
  second-nearest proxy.

The initial GBIF triage gate uses `HUMAN_OBSERVATION` rather than `research`.
Those values are source-specific filtering labels, not equivalent evidence
quality claims. GBIF preserved-specimen media remain candidate records but are
not sent to living-flower guide scoring by default.

No triage filter proves island membership, floral trait prevalence,
representative sampling, or independence across sources.

## Two independent review tasks

### Geographic and taxonomic review

The geographic reviewer sees source type, source URL, coordinates, uncertainty,
observed taxon, and proxy-distance metadata. They must verify:

- `geographic_review_status = accepted`;
- `verified_island_id` is one of the declared focal islands;
- `taxon_review_status = accepted`.

The reviewer records a concrete basis, such as source geometry plus taxon
assessment. “Nearest proxy” alone is not an acceptable basis. Where a GBIF
record may re-publish an iNaturalist image, source links, dataset provenance,
media references, and image URLs must be inspected before combining units.

### Blinded trait review

Two trait reviewers independently receive only a randomized blind ID and photo
URLs. The sheets deliberately omit coordinates, island names, proxy names,
source names, and source URLs.

A score can be accepted only when both reviewers record:

```text
focal_taxon_consistent = yes
inner_corolla_visibility = adequate
flower_open_stage = open
image_comparable = yes
trait_review_status = accepted
```

The guide ordinal uses one predeclared four-level scale:

| score | interpretation |
|---:|---|
| 0 | no or negligible visible inner-corolla guide/spot expression |
| 1 | weak visible expression |
| 2 | moderate visible expression |
| 3 | strong visible expression |

A reviewer should exclude a source record rather than force a score when
lighting, focus, corolla angle, developmental stage, color rendering, or image
provenance prevents a fair comparison.

## Reconciliation rule

The reconciliation script retains a unit only after geography/taxon acceptance,
acceptance from both trait reviewers, and reviewer ordinal difference of at most
one class. It then summarizes unique source records by verified island.

A directional pair is only a **draft** when each island meets the predeclared
minimum of three eligible units. A source-combined directional draft must also
pass explicit duplicate/provenance review; source-specific outputs should not be
summed merely because they share an island label.

No workflow writes `data/guide_direction_constraints.csv` automatically.
Before manual entry, inspect the source units, reviewer notes, exact guide-region
meaning, source overlap, and the non-random public-photo boundary.

## Commands

```bash
# iNaturalist (default research-grade triage)
python scripts/build_blinded_guide_photo_review_bundle.py \
  --proxy-queue izu_inaturalist_candidate_snapshots/trait_photo_proxy_review_queue.csv \
  --output-dir guide_photo_review_bundle_inaturalist

# GBIF (initial human-observation triage)
python scripts/build_blinded_guide_photo_review_bundle.py \
  --proxy-queue izu_gbif_candidate_snapshots/trait_photo_proxy_review_queue.csv \
  --output-dir guide_photo_review_bundle_gbif \
  --allowed-quality-grade HUMAN_OBSERVATION

python scripts/reconcile_blinded_guide_photo_reviews.py \
  --geographic-review guide_photo_review_bundle_inaturalist/geographic_taxonomic_review.csv \
  --trait-review-a guide_photo_review_bundle_inaturalist/blind_trait_review_A.csv \
  --trait-review-b guide_photo_review_bundle_inaturalist/blind_trait_review_B.csv \
  --blind-key guide_photo_review_bundle_inaturalist/blind_review_key_DO_NOT_SHARE_WITH_TRAIT_REVIEWERS.csv \
  --output-dir guide_photo_review_reconciliation
```

Do not send the blind key or the geographic review sheet to trait reviewers.
