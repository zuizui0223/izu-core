# Issue #91 one-command field-bundle intake

## Current gate

The prospective propagation/buffering interpretation structure is already frozen in:

`data/design/issue91_propagation_buffering_prediction_freeze.json`

The next empirical input is the first real linked *Campanula microdonta* field bundle. The intake command below applies the existing contracts in a fixed order; it does not add a new estimand or tune any mechanism after seeing outcomes.

## Canonical bundle filenames

Place the six required raw channels in one directory using these names:

- `field_dependency_plant_registry.csv`
- `field_observation_effort.csv`
- `field_visitor_contact_manifest.csv`
- `field_single_visit_pollen_deposition.csv`
- `field_pollination_treatments.csv`
- `field_mature_fruit.csv`

Optional files are auto-detected when present:

- `field_seed_parentage.csv`
- `field_pollinator_trait_lookup.csv`

Flower geometry and calibration files can be supplied explicitly with `--geometry` and `--calibration`; they are frozen as provenance channels but do not replace the core six-channel contract.

## One command

```bash
python scripts/intake_issue91_field_bundle.py \
  --bundle-dir field_bundle_v1 \
  --output-dir field_bundle_v1_intake
```

The command executes, in order:

1. validate that the committed Issue #91 prediction freeze still predates real field outcomes and has no locked decision threshold;
2. freeze exact raw bytes and headers with SHA256 hashes;
3. run the existing direct effective-dependency structural audit;
4. run the existing independent-plant admission/dispersion audit;
5. if present, run optional seed-parentage linkage audit;
6. if present, run strict proboscis-length Rao-Q FDQ audit.

## Output

`field_bundle_v1_intake/intake_summary.json` is the top-level receipt. It records:

- prediction-freeze SHA256 and status;
- raw bundle fingerprint;
- structural audit summary;
- plant-level dispersion/admission summary;
- optional parentage/FDQ status;
- every executed command and return code;
- the next admissible gate.

Core states are deliberately narrow:

- `raw_frozen_structural_incomplete`
- `structural_complete_pilot_dispersion_not_yet_estimable`
- `pilot_dispersion_estimable_precision_thresholds_still_unlocked`

Even the last state is **not** confirmatory adequacy. It only means the pilot has enough independent plants for the relevant between-plant dispersion to be defined.

## Optional channels do not silently block or rescue the core panel

Parentage and FDQ remain separate channels.

- Missing or unresolved parentage is not selfing and does not invalidate the open/bagged/supplemental core dependency panel.
- Missing FDQ trait coverage withholds FDQ; it does not invalidate SVD/effective-service or reproductive-treatment estimates.
- A failed optional audit is reported separately and cannot be used to relabel missing core data as present.

## Freeze-before-analysis rule

The raw-byte freeze runs before structural or dispersion auditing. If a genuine raw correction is required later, preserve the previous bundle and manifest and create a new version. Do not overwrite frozen raw bytes.

The intake summary also records the SHA256 of the prospective prediction freeze. This makes it possible to verify that the interpretation rules were committed before the corresponding field outcome bundle entered analysis.

## What remains locked after intake

The intake command never by itself:

- identifies historical Bombus-loss causation;
- identifies an Oshima–Toshima causal boundary;
- declares one universal buffering mechanism;
- estimates final dependency-predictor reliability;
- fixes a confirmatory sample size before pilot dispersion/coverage/loss are observed;
- treats flowers or repeated SVD events as independent plants;
- substitutes FDQ, visitor occurrence, or visitation rate for direct effective service or reproductive dependency.

If pilot dispersion becomes estimable, the next step is to use the observed variance, coverage and loss assumptions to lock a biologically meaningful precision target before confirmatory planning. If it does not, collect more independent-plant records under the already frozen measurement and interpretation contracts.
