# Guide evidence discovery registry

## Why a registry is needed

The nectar-guide question needs more than public photographs. Relevant clues can
appear in floras, original descriptions, figure captions, plates, herbarium
media, regional reports, and first-party field images. These sources differ in
what they can establish. The registry retains all leads without silently
turning a phrase such as "purple spots" into an island-level trait datum.

## Record types

| source type | useful for | not sufficient for by itself |
|---|---|---|
| `literature_text` | terminology, locality leads, figure and specimen pointers | ordinal image score or island trait frequency |
| `literature_figure` | source-locatable visual lead | island assignment or taxon confirmation without source review |
| `public_photo` | possible independent photographed unit | random sampling, guide function, island assignment from a proxy |
| `herbarium_media` | historical morphology lead | living-flower guide state or pollinator interaction |
| `field_photo` | first-party, traceable candidate unit | guide function or island-wide frequency |

## Routes

`not_eligible` is the default. A photo/figure can enter `blind_review_queue`
only after taxon and island are accepted. A record can become
`manual_constraint_candidate` only after adequate inner-corolla visibility and
an ordinal trait review; it is still not a model constraint. `field_bundle` is
reserved for accepted first-party field-photo records.

The validator rejects a text-only source pretending to have an ordinal image
score, a photo route without accepted taxon/island review, and a candidate
constraint lacking adequate visibility or completed review.

## Discovery practice

Start with `configs/guide_evidence_discovery_queries.csv`, but record the exact
source URL or citation and locator before claiming that a hit is useful. Query
labels are search routes, not taxonomy decisions. In particular, older labels
such as `Campanula punctata var. microdonta` remain candidate-only until an
expert review connects them to the focal entity.

Run:

```bash
python scripts/summarize_guide_evidence_registry.py \
  --registry data/guide_evidence_registry.csv \
  --output-dir guide_evidence_registry_summary
```

## Boundary

The registry is a collection and audit instrument. Its counts are not the
number of plants, flowers, islands, guide losses, or independent evolutionary
transitions. `data/guide_direction_constraints.csv` remains untouched until a
separate human decision documents the final source units and comparison.
