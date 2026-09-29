# Direct effective-pollinator dependency field protocol

## Why this is the next empirical gate

The current evidence programme has a strong contemporary community-level link between pollinator functional diversity (`FDQ`) and flower–pollinator trait matching, but direct `effective dependency × FDQ` moderation is not identified. The source-defined dominant target set has no source-resolved high-dependency Bombus endpoint measured in the exact 2024 Izu populations.

The missing field link is also explicit in the existing protocol stack:

```text
camera effort -> visit bout -> visually confirmed floral contact
                                      |
                                      v
                            [missing effectiveness]
                                      |
                                      v
                           fruit / seed / parentage
```

This protocol fills the bracketed channel with **single-visit pollen deposition (SVD)** and links it to a flower-level reproductive treatment panel.

The goal is not to assign plants to `specialist` or `generalist` classes from floral form. The goal is to measure effective pollinator dependence directly in the same tagged populations used for visitor and reproductive records.

## Three quantities that must remain separate

### 1. Per-visit effectiveness

For a previously unvisited receptive stigma, record the number of conspecific pollen grains deposited after one observed visitor bout.

This is `single_visit pollen deposition` (SVD). It is closer to pollinator effectiveness than visit frequency, visit duration, body size, or visually inferred stigma contact. The field literature also shows that visitors within the same broad functional group can differ strongly in SVD, so higher taxonomic grouping should not silently replace the measurement.

### 2. Realized visitor-group contribution

For one population and visitor group:

```text
observed visit bouts per monitored flower-hour
    × mean background-adjusted SVD
    = effective pollen delivery per monitored flower-hour
```

The audit also reports each measured visitor group's share of the rate-weighted SVD total.

This is a **sampled-window service estimate**. It is not proof that a visitor is absent from an island when no bouts were recorded.

The official CLI withholds background-adjusted SVD, effective pollen delivery, and service share when that visitor group lacks a no-visit SVD control. Raw visit rate and raw SVD remain auditable, but an uncontrolled value is not silently presented as effective service.

### 3. Plant reproductive dependence

Use three core flower treatments on tagged plants:

- `open_pollinated`;
- `bagged_autonomous`;
- `supplemental_outcross`.

Optional `hand_self` and `emasculated_open` treatments may be added for a species-specific question, but they do not replace the three core treatments.

The core panel separates autonomous reproductive capacity from open service and supplemental pollen. It does **not** equate self-compatibility, autonomous reproduction, and realized selfing.

## Stable identifiers

Use the same identifiers across all linked records:

```text
population_id
field_event_id
island_id
site_id
plant_id
flower_id
```

When an SVD flower receives its one observed visit, also preserve:

```text
effort_id
visit_id
visitor_group
```

When a treatment flower matures a fruit, preserve the existing raw-record `fruit_id`. The fruit record keeps mature-seed counts and the downstream parentage rows.

Do not create a new plant/flower identifier during pollen counting or fruit processing.

## Files

New templates:

- `templates/field_dependency_plant_registry_template.csv`
- `templates/field_single_visit_pollen_deposition_template.csv`
- `templates/field_pollination_treatment_template.csv`
- `templates/effective_dependency_precision_goals_template.csv`

Existing linked files:

- `templates/field_observation_effort_template.csv`
- `templates/field_visitor_contact_manifest_template.csv`
- generated raw-record `fruits.csv`
- generated raw-record `paternity_calls.csv` where available

## SVD field procedure

### Before exposure

1. Tag the plant and flower.
2. Exclude visitors **before the stigma becomes receptive to external pollen**. The exact developmental stage must be species-specific; do not assume that `before anthesis` and `virgin stigma` are synonymous for every taxon.
3. Record `bag_on_time`.
4. When the flower is ready for the assay, record `bag_off_time`.

### Single-visit record

1. Observe until the first confirmed visitor bout.
2. Score the visit in the existing visitor-contact manifest.
3. Preserve the same `visit_id` in the SVD row.
4. After the visitor leaves, prevent further visits and collect the stigma using the predeclared preservation/counting method.
5. Count conspecific, heterospecific, and unclassified grains separately.

The SVD row is rejected if the first visit is not confirmed, if it does not link to an observed visit, or if the pollen-count partition does not sum to the recorded total.

### Controls

Collect both control types whenever feasible:

- `bagged_unvisited_control`: remains excluded until stigma collection;
- `exposed_no_visit_control`: undergoes comparable bag removal/handling but is collected without a visitor bout.

The second control is particularly useful for detecting pollen introduced by handling/exposure rather than by the scored visitor.

Bagging can itself alter floral state, including nectar availability and visitor handling. Record exact bagging duration and preserve paired no-visit controls rather than assuming the bag has no effect. Any nectar manipulation must be species-specific and predeclared rather than invented after visitor groups are seen.

Primary methodological context: King et al. (2013), DOI `10.1111/2041-210X.12074`; Cecala et al. (2020), DOI `10.1111/een.12890`. A Campanulaceae example comparing pollen deposition with single-visit seed production is Wang et al. (2017), DOI `10.1002/ece3.3391`.

## Pollination-treatment procedure

Assign flowers before looking at their outcome. Preserve flowers lost to damage as `lost` or `damaged`; do not silently delete them.

### `open_pollinated`

Normal visitor access. This measures realized open reproductive outcome under the local pollination environment.

### `bagged_autonomous`

Exclude visitors through the relevant reproductive period. This measures autonomous reproductive capacity under the treatment conditions. It is not a direct measure of self-compatibility or realized selfing.

### `supplemental_outcross`

Apply pollen from a different tagged plant. The donor plant must differ from the maternal plant and should be recorded explicitly. This treatment provides a pollen-supplemented reference; it is not automatically a universal biological maximum if hand pollination itself is imperfect.

### Outcomes

Use:

```text
pending | mature_fruit | aborted | lost | damaged
```

Only `mature_fruit` and `aborted` form the basic capsule-set denominator. `pending`, `lost`, and `damaged` remain visible but are not silently coded as reproductive failures.

A mature treatment fruit links to the existing `fruits.csv`, where mature seed count and later genotyping are retained.

## Audit

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

Outputs:

```text
svd_by_visitor_group.csv
rate_weighted_effective_service.csv
pollination_treatment_summary.csv
population_dependency_readiness.csv
summary.json
```

## Readiness is structural, not statistical

`dependency_panel_structurally_complete=yes` means only that a population has:

- usable monitored flower-hours;
- at least one visitor group with linked SVD and a no-visit background control; and
- at least one analyzable flower in each core reproductive treatment.

That status is **not** a sample-size, precision, equivalence, or power claim. Pilot dispersion must be used to predeclare the number of independent plants, SVD events per visitor group, treatment flowers per plant/site, and repeated temporal blocks needed for inference.

The audit intentionally does not define a universal `high dependency` cutoff. If a later analysis dichotomizes dependency, the threshold must be preregistered biologically or derived from an external calibration rather than selected to maximize the Izu result.

## Pilot first, precision lock second

Do **not** begin the field programme by declaring an arbitrary universal number such as `10 flowers per treatment` or by treating all flowers as independent replicates.

The planning unit is the **independent plant**. Repeated flowers or SVD visits first form a within-plant mean/proportion; pilot dispersion is then estimated among plant means.

### Step 1 — pilot without a precision target

Run:

```bash
python scripts/plan_effective_dependency_pilot_precision.py \
  --svd field_single_visit_pollen_deposition.csv \
  --treatments field_pollination_treatments.csv \
  --output-dir dependency_pilot_precision
```

This produces:

```text
svd_plant_pilot.csv
svd_pilot_dispersion.csv
treatment_plant_pilot.csv
treatment_pilot_dispersion.csv
precision_recommendations.csv
```

With no goal file, `precision_recommendations.csv` contains no invented target. The pilot summaries report the number of independent plants, the number of within-plant events/flowers, mean plant response, and between-plant SD/CV when at least two independent plants are available.

### Step 2 — freeze, admit, then lock an absolute CI half-width

Before confirmatory precision planning, freeze the complete raw field bundle and run the admission audit on the exact frozen pilot inputs. The admission artifact records SHA256 identities for the plant, SVD, and treatment files used to determine the pilot-dispersion gate.

Copy `templates/effective_dependency_precision_goals_template.csv` and add a row only after deciding what precision is biologically useful. Available pilot metrics are:

- `background_adjusted_svd` for a named visitor group;
- `capsule_set_proportion` for a named treatment.

A goal row records:

```text
goal_id
metric
population_id
group_label
absolute_half_width
confidence
status
notes
```

Keep `status=draft` while the target is undecided. A draft row generates **no sample-size recommendation**.

Only after the target is fixed, set `status=locked`, then rerun with the frozen bundle and matching admission artifact:

```bash
python scripts/plan_effective_dependency_pilot_precision.py \
  --svd field_single_visit_pollen_deposition.csv \
  --treatments field_pollination_treatments.csv \
  --goals effective_dependency_precision_goals.csv \
  --freeze-manifest effective_dependency_raw_bundle.freeze.json \
  --admission effective_dependency_admission.json \
  --output-dir dependency_pilot_precision
```

Locked-goal planning is rejected unless all of the following are true:

- the freeze manifest declares the complete six-channel raw field bundle;
- current SVD and treatment bytes match the SHA256 values in that frozen bundle;
- the admission artifact fingerprints the same current SVD and treatment bytes;
- every population referenced by a locked goal has `pilot_dispersion_gate_pass=true`.

This prevents a stale admission result or post-freeze edited pilot file from being used to justify confirmatory replication. Draft goals and pilot dispersion summaries remain available without these confirmatory-planning artifacts.

The current calculator uses the normal-approximation planning identity

```text
n ≈ ceil[( z * between-plant SD / absolute half-width )²]
```

for the number of independent plants. It is deliberately a **first planning diagnostic**, not final power analysis. Confirmatory design must additionally account for site and temporal replication, expected flower/fruit loss, rare visitor groups, unequal SVD availability, and the eventual hierarchical model.

The scientific order is therefore:

```text
raw bundle freeze -> linkage/QC -> admission audit -> pilot plant-level dispersion
                  -> lock biologically meaningful precision
                  -> calculate approximate independent-plant n
                  -> simulate/check final hierarchical design
```

not:

```text
inspect desired result -> choose a convenient n or precision target
```

## Quantities that may be reported descriptively

### Visitor-group SVD

- number of single-visit stigmas;
- raw mean conspecific pollen deposition;
- no-visit background level;
- background-adjusted SVD.

### Rate-weighted service

- observed visits per monitored flower-hour;
- background-adjusted SVD;
- effective pollen delivery per monitored flower-hour;
- visitor-group share of measured effective service.

### Reproductive panel

- treatment assignment count;
- analyzable count;
- capsule-set proportion;
- mature seeds per analyzable assigned flower when fruit records are linked;
- `bagged_autonomous / supplemental_outcross` capsule-set ratio;
- `open_pollinated / supplemental_outcross` capsule-set ratio.

The ratios are descriptive. Values do not become selfing rates or causal dependency coefficients by renaming them.

## Target hierarchy for the next field cycle

1. **Focal anchor:** *Campanula microdonta* populations, preserving exact site/population identity rather than an island-only label.
2. **Measured functional controls/comparators:** taxa are chosen from direct interaction/reproductive evidence and phenological feasibility, not floral syndrome labels.
3. **High-dependency endpoint:** must be demonstrated by direct effective-pollinator data. A taxon is not prelabelled `Bombus-dependent` merely because its corolla appears adapted to a large bee.
4. **Survivorship outcomes:** non-establishment, hybrid replacement, or interaction rewiring remain biological response modes and should not be discarded solely because a clean same-lineage island comparator is absent.

Whenever possible, resample sites that can be linked to existing network/environment records. But a repeated sample at one Oshima site is still one geographic bridge-state unit; the new dependency measurements improve the mechanism axis without creating a second independent Oshima-like replicate.

## Claim boundary

The intended prospective chain is:

```text
pollinator functional environment
    -> visitor-specific SVD / effective service
    -> plant reproductive dependence / pollen limitation
    -> longer-term demographic or evolutionary response
```

The first two arrows can become much better measured with this protocol. They still do not identify the historical cause of the Campanula transition without temporal or independent geographic replication and matched population-history controls.
