# Linking flower geometry, visitor handling, pollen deposition, and reproductive outcomes

## Why the IDs matter

The central question is not whether islands differ in flower length alone, or whether different insects appear alone. The useful unit is a traceable chain:

```text
island -> site -> tagged plant -> tagged flower
                     |                |
             flower geometry      observation effort
                                      |
                                  visitor bout
                                      |
                           single-visit pollen deposition
                                      |
                         open / bagged / hand-cross outcome
                                      |
                              fruit / seed / parentage
```

Use the same `field_event_id`, `island_id`, `site_id`, `plant_id`, and where possible `flower_id` across linked files. The direct-dependency panel also introduces `population_id` so repeated plants from the same population are not mistaken for independent geographic units.

Core files now include:

- `field_flower_geometry_manifest_template.csv`
- `field_observation_effort_template.csv`
- `field_visitor_contact_manifest_template.csv`
- `field_dependency_plant_registry_template.csv`
- `field_single_visit_pollen_deposition_template.csv`
- `field_pollination_treatment_template.csv`
- generated raw-record `fruits.csv` and `paternity_calls.csv` where available

A missing `flower_id` can remain acceptable for a video covering several flowers in the general visit-rate dataset, but it cannot be used to invent a flower-level SVD linkage. A single-visit pollen-deposition row must refer to a known tagged flower and observed visit.

## Geometry capture

For each tagged plant, measure one to three freshly open flowers. Record:

- corolla length;
- mouth diameter;
- inner depth;
- orientation and stage;
- method (`caliper`, `ruler_photo`, or `calibrated_photo`);
- an image reference when available.

Do not repeatedly measure the same flower to inflate sample size. Summarize flowers first within plant, then plants within population/site.

```bash
python scripts/summarize_field_flower_geometry.py \
  --geometry field_flower_geometry_manifest.csv \
  --output-dir field_geometry_summary
```

## Visitor-contact capture

Use fixed windows whenever possible and record every usable window regardless of whether visits occur. Then score actual visit bouts in the contact manifest.

When video resolution cannot show floral organs, score `not_confirmable`. Do not infer contact from visitor body size or trajectory.

```bash
python scripts/audit_field_visitor_contacts.py \
  --effort field_observation_effort.csv \
  --visits field_visitor_contact_manifest.csv \
  --output-dir field_contact_audit
```

Confirmed anther-plus-stigma contact remains a **handling proxy**. It is not promoted to pollinator effectiveness.

## Direct single-visit pollen deposition

For a pre-excluded, previously unvisited receptive stigma, expose the flower until one confirmed visitor bout, then collect the stigma before another visit occurs. Preserve the same `visit_id` in the SVD manifest and count conspecific pollen separately from heterospecific/unclassified grains.

Pair single-visit rows with no-visit controls so handling/background contamination is measurable. Exact bagging duration is retained because exclusion bags can alter floral state and visitor behavior.

See `docs/EFFECTIVE_POLLINATOR_DEPENDENCY_FIELD_PROTOCOL.md`.

## Reproductive treatment linkage

At the same population, assign tagged flowers prospectively to:

- `open_pollinated`;
- `bagged_autonomous`;
- `supplemental_outcross`.

Mature treatment fruits link to the existing raw-record `fruit_id`. `aborted`, `lost`, and `damaged` states remain explicit rather than being silently merged.

This keeps autonomous reproductive capacity, pollen limitation, mature-seed output, and later parentage as separate channels.

## Integrated audit

```bash
python scripts/audit_effective_pollinator_dependency.py \
  --plants field_dependency_plant_registry.csv \
  --effort field_observation_effort.csv \
  --visits field_visitor_contact_manifest.csv \
  --svd field_single_visit_pollen_deposition.csv \
  --treatments field_pollination_treatments.csv \
  --fruits fruits.csv \
  --output-dir effective_dependency_audit
```

The audit can estimate, descriptively:

- visitor-group SVD;
- observed visit rate per monitored flower-hour;
- rate-weighted effective pollen delivery;
- measured visitor-group share of effective service;
- treatment capsule set and mature seeds per analyzable flower;
- structural completion of the direct-dependency panel.

## What can later be compared

The linked data can support questions such as:

- At sites with shorter/narrower flowers, which visitors enter and actually deposit conspecific pollen?
- Does visually confirmed stigma contact predict SVD within visitor groups?
- Is a large share of effective pollen service concentrated in one visitor group, or distributed across groups?
- Does a population with weak effective service also show a larger autonomous-reproduction component or stronger pollen limitation?
- Do different plant lineages convert the same pollinator-functional environment into different reproductive response modes?

These comparisons still require replication across plants, sites, and temporal blocks. A structurally complete panel is not a power claim, and a rate-weighted SVD association is not proof of historical selection or a causal Oshima–Toshima transition.
