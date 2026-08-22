# Effective-dependency raw field freeze

## Purpose

Freeze the linked raw field bundle **before inferential analysis or outcome-dependent cleaning decisions**. The freeze records exact file identity; it is not a scientific admission test.

Required raw channels:

- plant registry
- observation effort, including zero-visit windows
- visitor/contact manifest
- single-visit pollen deposition (SVD)
- pollination treatments
- mature fruit outcomes

Optional channels can be frozen in the same bundle:

- seed/parentage
- pollinator trait lookup used for strict FDQ
- flower geometry
- calibration records

## Command

```bash
python scripts/freeze_effective_dependency_field_bundle.py \
  --plants field_dependency_plant_registry.csv \
  --effort field_observation_effort.csv \
  --visits field_visitor_contact_manifest.csv \
  --svd field_single_visit_pollen_deposition.csv \
  --treatments field_pollination_treatments.csv \
  --fruits field_mature_fruit.csv \
  --seeds-parentage field_seed_parentage.csv \
  --traits field_pollinator_trait_lookup.csv \
  --output freezes/effective_dependency_raw_v1.json
```

Omit optional arguments when those channels were not collected or are not being used for that bundle version.

## What is locked

For each supplied CSV the manifest records:

- SHA256
- byte count
- non-empty data-row count
- exact header
- required/optional channel status

The manifest also records a bundle-level SHA256 fingerprint calculated from the channel identities. When strict FDQ is requested, the exact trait lookup is therefore part of the same bundle identity rather than a mutable downstream analysis input.

Re-running the command against an existing manifest is allowed only when the raw bundle is byte-identical. If any raw file or supplied trait lookup changes, write a **new versioned freeze manifest** rather than overwriting the previous freeze.

## Gate separation

A successful freeze sets none of these states to true:

- structural completion
- pilot dispersion estimability
- confirmatory adequacy
- analysis admission

Those remain the responsibility of the existing dependency/admission audits. In particular, a checksum does not make `pending`, `lost`, `damaged`, unscorable visits, unresolved parentage, missing traits, or failed genotype QC analyzable.

## Corrections after freeze

When a genuine raw-data correction is necessary:

1. retain the previous raw files and freeze manifest;
2. create corrected raw files as a new version;
3. freeze them to a new manifest;
4. record the reason for the correction separately;
5. rerun structural/admission audits from the new frozen bundle.

Do not silently mutate a frozen raw file or trait lookup in place.

## Claim boundary

The freeze establishes provenance and immutability of the collected field inputs only. It does not increase sample size, repair missing controls, create independent plants, resolve parentage, make incomplete FDQ trait coverage complete, estimate historical selection, or open a causal Oshima–Toshima/Bombus-loss claim.
