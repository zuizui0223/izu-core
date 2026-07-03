# Field visitor-contact protocol

## Question this channel can answer

The goal is not simply to count insects on flowers. It is to distinguish:

- insects that were detected near a flower;
- visitors that entered the corolla; and
- visits in which both anther and stigma contact were **visually confirmed**.

The final category is a `confirmed_both_contact` **handling proxy**. It is not
pollen deposition, pollen-tube growth, fruit set, seed set, or pollinator
effectiveness.

This is the missing channel needed to assess whether small bees merely occur at
flowers or plausibly handle their reproductive structures differently from
Bombus-sized visitors.

## Two linked manifests

### 1. Observation effort

Use `templates/field_observation_effort_template.csv` once per fixed video or
direct-observation window. Record every usable window, including zero-visit
windows. Essential fields are the island, site, start/end time with a timezone,
and the number of open flowers being monitored.

Use exactly the same `field_event_id`, `site_id`, `plant_id`, and `flower_id`
labels as the field guide-photo manifest when they concern the same tagged
plant or flower.

A `failed` recording cannot be marked usable. A usable window with no visitors
is valuable data; do not delete it.

### 2. Visit bouts

Use `templates/field_visitor_contact_manifest_template.csv` once for one
uninterrupted visit bout, not once per video frame. Link it to an `effort_id`.
If a video tracks a recognizable insect leaving and returning, score separate
bouts unless continuity is visible.

For every bout, record:

- a conservative visitor group and body-size class;
- entry into the corolla;
- anther contact and stigma contact separately;
- how clearly contact was visible;
- whether evidence came from video, live observation, or only a still image;
- scorer and scoring time.

Use `bombus_ardens_confirmed` only after the identification itself is
confirmed. Ambiguous Bombus should remain `bombus_small`, `bombus_large_other`,
or `unknown_visitor` as appropriate.

## Scoring rules

| observation | score |
|---|---|
| insect approaches but does not land | `approached_no_landing` |
| lands but does not enter the corolla | `landed_no_entry` |
| enters but floral organs are obscured | `entered`, contact = `not_confirmable` |
| anther or stigma is visibly touched | corresponding contact = `confirmed` |
| neither organ is seen touched in a clear view | both = `not_seen` |

Never score a contact as confirmed from a silhouette, a blurred frame, or an
inferred trajectory. Such rows remain `not_confirmable`.

## Audit

```bash
python scripts/audit_field_visitor_contacts.py \
  --effort field_observation_effort.csv \
  --visits field_visitor_contact_manifest.csv \
  --output-dir field_contact_audit
```

The audit rejects a visit outside its effort window, a visit tied to unusable
effort, inconsistent island/site/plant/flower or video identity, a confirmed
contact when there was no corolla entry, and an unconfirmed identification
labelled as confirmed *B. ardens*.

`field_contact_rate_summary.csv` uses total usable monitored flower-hours for
an island as denominator, including zero-visit windows. A visitor group absent
from the summary has **not** been shown absent from the island; it simply has no
scored bout in the submitted manifest.

## Experimental interpretation

The field data will discriminate hypotheses only when paired with flower
geometry, guide traits, and later reproductive measurements at the same sites.

| candidate explanation | discriminating observation |
|---|---|
| initial Oshima-size step plus later reproductive change | reduced flower geometry appears at/after Oshima, while contact structure and autonomous reproduction can change farther downstream |
| continuous small-bee size adaptation | flower geometry and small-bee contact should covary repeatedly across populations |
| island-order latent gradient | changes may align with island order but lack a specific body-size/contact mechanism |

Even an association between body size and both-contact rate is not proof of
selection. Per-visit pollen deposition and reproductive outcome are separate
measurements still needed.
