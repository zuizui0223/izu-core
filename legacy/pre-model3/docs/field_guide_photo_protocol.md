# First-party field guide-photo protocol

## Aim

Create an island-resolved nectar-guide evidence channel that does not depend on
public-photo selection or proxy island assignment. The output is an ordinal,
double-blind image review dataset; it is not automatic colour quantification or
pollination evidence.

## Independent unit

One **tagged plant** is one review unit. Take multiple images and, when useful,
multiple flowers from that same plant as alternate views, but record the same
`plant_id` for all of them. Do not use several flowers from one plant as several
independent plants.

For each island, three eligible plants is only the existing threshold for a
non-binding pairwise draft. Aim for at least five plants across at least two
sites before treating a field-photo contrast as a serious biological lead.

## Per-plant capture

1. Assign `field_event_id`, `site_id`, and a unique `plant_id` before taking the
   first image.
2. Record one open flower whose inner corolla can be viewed. Take two or three
   inside-corolla views rather than repeatedly photographing the same exterior
   angle.
3. Use diffuse natural light where possible. Avoid an image whose guide region
   is saturated by flash, deep shadow, or strong colour cast.
4. Include a neutral reference frame or colour target in at least one image per
   event when feasible. It documents capture conditions; the current ordinal
   review does not calculate raw colour values from it.
5. Log latitude, longitude, field taxon label, and confidence. A field island
   claim is still checked in the geographic/taxon review sheet.
6. Put image paths or stable storage URLs in `photo_uri`. The images themselves
   need not be committed to the repository.

## Manifest

Start from `templates/field_guide_photo_manifest_template.csv`. Each row is one
photo. Required identifiers are:

```text
field_event_id, island_id, site_id, plant_id, flower_id, photo_id, photo_uri
```

Other columns preserve capture time, coordinates, field identification,
standardisation status, photographer, voucher/sample association, and notes.
The builder rejects duplicate photo IDs, invalid island labels, missing required
fields, invalid coordinates, and one tagged plant that spans declared islands.

## Build and review

```bash
python scripts/build_field_guide_photo_review_bundle.py \
  --manifest field_guide_photo_manifest.csv \
  --output-dir field_guide_review_bundle
```

The output contains a provenance file, an unblinded geographic/taxonomic sheet,
two blinded trait sheets, and a private blind key. Do not give provenance,
geographic metadata, or the key to trait reviewers.

After two independent trait reviews:

```bash
python scripts/reconcile_field_guide_reviews.py \
  --geographic-review field_guide_review_bundle/field_geographic_taxonomic_review.csv \
  --trait-review-a field_guide_review_bundle/field_blind_trait_review_A.csv \
  --trait-review-b field_guide_review_bundle/field_blind_trait_review_B.csv \
  --blind-key field_guide_review_bundle/field_blind_review_key_DO_NOT_SHARE_WITH_TRAIT_REVIEWERS.csv \
  --output-dir field_guide_review_reconciled
```

Run the merged audit and progress monitor on the same field bundle when needed.
Do not concatenate field review files with public-photo files; they have
different sampling boundaries.

## Interpretation boundary

A reconciled field bundle provides first-party ordinal image evidence. It does
not establish guide loss, guide function, pollinator preference, pollen transfer,
or fitness. Any guide-direction constraint remains a separate manual scientific
decision after inspecting plants, sites, images, reviewer notes, and the
relationship to reproductive data.
