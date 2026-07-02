# Blinded public-photo review for nectar-guide/spot evidence

## Why the new layer exists

The iNaturalist workflow now finds geographically plausible, source-linked
flower-photo candidates. That is useful, but candidate photographs are not
measurements. Three failure modes are especially easy here:

1. a nearest island proxy is silently mistaken for island membership;
2. a reviewer knows the hypothesized island gradient and scores photos toward
   the expected direction;
3. several angles from one observation are counted as several flowers.

The blinded review bundle prevents those shortcuts before any guide-direction
constraint can be proposed.

## Unit of analysis

**One iNaturalist observation = one review unit.** Multiple linked photos are
alternative views, retained as a semicolon-delimited bundle. They are never
independent replicates.

The initial triage gate is deliberately modest:

- focal target: `campanula_microdonta`;
- `research` grade;
- positional accuracy at or below 100 m;
- distance to the nearest declared island proxy at least 20 km smaller than the
  second-nearest proxy.

These filters only identify an efficient review queue. They do not prove island
assignment, floral trait prevalence, or representative sampling.

## Two independent review tasks

### Geographic and taxonomic review

The geographic reviewer sees coordinates, uncertainty, the observation URL,
observed taxon, and proxy-distance metadata. They must verify:

- `geographic_review_status = accepted`;
- `verified_island_id` is one of the declared focal islands;
- `taxon_review_status = accepted`.

The reviewer records a concrete basis, such as observation geometry plus taxon
assessment. “Nearest proxy” alone is not an acceptable basis.

### Blinded trait review

Two trait reviewers independently receive only a randomized blind ID and photo
URLs. The sheets deliberately omit coordinates, island names, proxy names, and
observation URLs.

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

A reviewer should exclude a photograph rather than force a score when lighting,
focus, corolla angle, developmental stage, or color rendering prevents a fair
comparison.

## Reconciliation rule

The reconciliation script retains a unit only after geography/taxon acceptance,
acceptance from both trait reviewers, and reviewer ordinal difference of at most
one class. It then summarizes unique observation units by verified island.

A directional pair is only a **draft** when each island meets the predeclared
minimum of three eligible observation units. It is still not written into
`data/guide_direction_constraints.csv` automatically. Before manual entry, the
researcher must inspect the source units, reviewer notes, exact guide-region
meaning, and whether the pattern is biologically interpretable rather than an
artifact of public-photo sampling.

## Commands

```bash
python scripts/build_blinded_guide_photo_review_bundle.py \
  --proxy-queue izu_inaturalist_candidate_snapshots/trait_photo_proxy_review_queue.csv \
  --output-dir guide_photo_review_bundle

python scripts/reconcile_blinded_guide_photo_reviews.py \
  --geographic-review guide_photo_review_bundle/geographic_taxonomic_review.csv \
  --trait-review-a guide_photo_review_bundle/blind_trait_review_A.csv \
  --trait-review-b guide_photo_review_bundle/blind_trait_review_B.csv \
  --blind-key guide_photo_review_bundle/blind_review_key_DO_NOT_SHARE_WITH_TRAIT_REVIEWERS.csv \
  --output-dir guide_photo_review_reconciliation
```

Do not send the blind key or the geographic review sheet to trait reviewers.
