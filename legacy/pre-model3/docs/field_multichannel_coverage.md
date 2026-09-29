# Field multichannel coverage audit

## Purpose

The project now records four first-party channels:

1. inner-corolla / guide photographs;
2. flower geometry;
3. time-bounded observation effort; and
4. manually scored visitor-contact bouts.

A field day can easily produce each channel in different places or on different
plants. This audit identifies those linkage gaps before they become an
uninterpretable island summary.

## Inputs

Use the existing four raw manifests:

```text
field_guide_photo_manifest.csv
field_flower_geometry_manifest.csv
field_observation_effort.csv
field_visitor_contact_manifest.csv
```

The audit uses `field_event_id`, `island_id`, `site_id`, and `plant_id` as the
plant linkage key. `flower_id` remains in the source manifests for finer-grained
checks but is not required for all effort windows because a single video may
cover several flowers on one tagged plant.

## Run

```bash
python scripts/audit_field_multichannel_coverage.py \
  --guide-photos field_guide_photo_manifest.csv \
  --geometry field_flower_geometry_manifest.csv \
  --effort field_observation_effort.csv \
  --visits field_visitor_contact_manifest.csv \
  --output-dir field_multichannel_coverage
```

Outputs:

- `field_multichannel_plant_coverage.csv`
- `field_multichannel_site_coverage.csv`
- `field_multichannel_island_coverage.csv`

## Coverage states

| state | meaning | next action |
|---|---|---|
| `missing_guide_inner_corolla_photo` | no tagged-plant photo shows the corolla interior | take a standardized inner-corolla photo |
| `missing_flower_geometry` | no final geometry record | measure one or more open flowers |
| `missing_usable_plant_effort` | no usable observation window links to that plant | record a time-bounded video or direct-observation window |
| `linked_multichannel_unit_no_scored_visit` | guide, geometry, and usable effort exist but no visit bout was scored | retain the zero-visit window and add comparable effort; do not infer absence |
| `linked_multichannel_unit_with_scored_visit` | all channels are linked and at least one bout was scored | retain the linkage and, when possible, add reproductive-outcome data |

## Boundaries

The audit is a collection-control tool. It does not estimate guide frequency,
visitor abundance, pollen deposition, reproductive success, adaptation, or
historical mechanism. A site-level video with no `plant_id` is retained as site
effort, but is never assigned to a tagged plant post hoc.
