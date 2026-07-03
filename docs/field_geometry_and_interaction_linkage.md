# Linking flower geometry, guide photographs, and visitor-contact observations

## Why the IDs matter

The central question is not whether islands differ in flower length alone, or
whether different insects appear alone. The useful unit is a traceable chain:

```text
island -> site -> tagged plant -> tagged flower
                     |                |
          geometry / guide photo      monitored video / direct observation
```

Use the same `field_event_id`, `island_id`, `site_id`, `plant_id`, and where
possible `flower_id` across these files:

- `field_guide_photo_manifest_template.csv`
- `field_flower_geometry_manifest_template.csv`
- `field_observation_effort_template.csv`
- `field_visitor_contact_manifest_template.csv`

A missing `flower_id` is acceptable for a video covering several flowers, but
do not invent a flower-level link that was not visible.

## Geometry capture

For each tagged plant, measure one to three freshly open flowers. Record:

- corolla length;
- mouth diameter;
- inner depth;
- orientation and stage;
- method (`caliper`, `ruler_photo`, or `calibrated_photo`);
- an image reference when available.

Do not repeatedly measure the same flower to inflate sample size. The geometry
manifest accepts one final record per tagged flower and summarizes flowers first
within plant, then plants within island.

```bash
python scripts/summarize_field_flower_geometry.py \
  --geometry field_flower_geometry_manifest.csv \
  --output-dir field_geometry_summary
```

## Visitor-contact capture

Use fixed windows whenever possible: for example, several independent
10--20 minute windows per site distributed across comparable daylight periods.
Record every usable window in the effort manifest regardless of visits. Then
score only actual visit bouts in the contact manifest.

When video resolution cannot show both floral organs, score `not_confirmable`.
Do not turn a movement into a contact based on expectation about insect size.

```bash
python scripts/audit_field_visitor_contacts.py \
  --effort field_observation_effort.csv \
  --visits field_visitor_contact_manifest.csv \
  --output-dir field_contact_audit
```

## What can later be compared

The resulting data can support descriptive questions such as:

- At sites with shorter, narrower flowers, which visitor body-size groups enter
the corolla?
- Among scorable visits, do visitor groups differ in visually confirmed
anther-plus-stigma contact?
- Do downstream islands resemble Oshima in geometry but differ in contact
structure or autonomous reproduction?

These comparisons require replication across sites and tagged plants. They do
not automatically establish pollen transfer, adaptation, historical transition,
or a causal role for any particular bee group. Per-visit pollen deposition and
fruit/seed outcomes remain separate evidence channels.
