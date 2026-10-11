# Izu Lane C — linked parentage extension, not an admitted field trial

**2026-10-10 · PR #452 · prospective implementation, no new natural observations.**

## Current location and inheritance boundary

- The **canonical legacy field-chain code is still present**, but was relocated under `legacy/pre-model3/`: `legacy/pre-model3/scripts/audit_izu_transition_linked_chain.py`, `legacy/pre-model3/data/design/izu_transition_linked_chain_freeze_20260909.json`, and `legacy/pre-model3/docs/IZU_TRANSITION_LINKED_CHAIN_PRIORITY_20260909.md`.
- The separate outcome-blind site admission material is in `legacy/routes/nee/`: `legacy/routes/nee/scripts/audit_chapter2_nee_r1_site_registry.py`, `legacy/routes/nee/data/design/chapter2_nee_r1_site_registry_candidates_20260913.csv` and `legacy/routes/nee/data/design/chapter2_nee_r1b_permit_contact_plan_20260913.json`.
- Issue [#343](https://github.com/zuizui0223/izu-core/issues/343) requires `block_id × plant_id` linked *flower geometry → monitored effort/zero visits → single-visit pollen deposition (SVD) and no-visit control → open/bagged/supplemented reproductive treatments → fruit/seed outcomes*.
- Issue [#349](https://github.com/zuizui0223/izu-core/issues/349) currently retains **5 focal Campanula microdonta and 3 prospective Farfugium japonicum candidate localities; zero admitted sites**. The `32` pre-pilot screen is not an empirical power calculation. Names and locations in the candidate registry do **not** authorize sampling or confirm flowering/current experimental availability.

These frozen precedents are **not edited** by this PR. The new parentage extension adds a distinct molecular-data layer, rather than upgrading the existing SVD-only chain to a biological father-identification claim.

## What PR #452's Model3 result actually predicts

Under 36 explicitly artificial plant/visitor conditions with the same total delivered pollen, group viable-seed output converged but the distribution of *expected paternal returns* shifted in all 18 intentionally mixed-diploid plant fixtures. Mean paternal-share L1 distance was ~0.112, while mean absolute collective viable-seed difference was ~0.0009. The male and female components of local genetic investment gradients both varied; this does **not** demonstrate natural pollen-mediated selection, a paternal-only effect or historical island adaptation.

A natural falsifier would ask whether plant-specific paternity shares and maternal success vary with the **observed effective visitor composition** after controlling for exposure, mother/father genotypes, plant matching traits, pollen delivery, and sampling/assay uncertainty. A sum of seeds alone cannot answer this; nor can SVD grains identify fathers.

### Added observational layer (not a promise of randomized natural causality)

For each *prospectively frozen* site × population × season × time block:

1. Import genuine `plant_chain_readiness.csv` output from the legacy linked-chain audit. Preserve original `block_id × plant_id`, the zero-visit effort windows, SVD controls, and open/bagged/supplemented treatment links. Do **not** replace missing SVD with a paternity result.
2. Independently register the **open-pollinated** fruit's `fruit_id`, `maternal_id`, mature seed count, and tagged plant/block. Record whether each sampled offspring seed was genotype-usable, assay-failed or still pending; retain the complete sampled denominator. Bagged or supplemented offspring can be used in *separate validation/control analyses*, but not as ordinary open-pollinated paternal-share observations.
3. Obtain a documented maternal genotype and a defined site/season **candidate-father pool** with collection/sample identifiers and genotype evidence. Explicitly recognize possible fathers *outside the sampled pool*; no finite local pollen-donor census can silently be assumed exhaustive.
4. Run an external, independently specified parentage assignment method with documented genotype error, missing loci/alleles, maternity confirmation, selfing and unsampled fathers. Store the original genotype archive/report SHA-256. The add-on **does not fit a paternity model**; it only checks the traceability and probability ledger of the output.
5. For each genotype-usable offspring keep a posterior vector for `self`, `unsampled_or_unknown` and zero or more explicitly sampled, genotyped `named_father` candidates. The probabilities must sum to one. A failed assay, missing candidate father or zero-visit period is **not evidence of selfing**, and incomplete paternity assignments must not be forced to certainty.
6. Aggregate expected father shares **within mother × block over usable sampled offspring only**, while reporting the failed/pending sample counts. Link to visitor composition and SVD strictly via the shared plant/block identifiers. Keep offspring nested within mothers and mothers within actual blocks for any later uncertainty or observational model.

The statistical target is not “parentage is causal”. It is whether, **among comparable blocks/plants**, estimated father-share distribution relates to functional service composition beyond total delivery, with pre-outcome plant matching and measured site/season covariates. A credible assessment needs independent blocks, robust assignment sensitivity and adequate precision; there is **no effect-size estimate or accepted power claim yet**.

## Implemented mechanical gate

- Frozen empty-input template: `data/design/izu_parentage_bridge_template_20261010.json`
- Validator/summary: `scripts/audit_izu_parentage_bridge.py`
- Fail-closed unit tests (only synthetic, never presented as field observations): `tests/test_izu_parentage_bridge.py`

Run:

```bash
python -m scripts.audit_izu_parentage_bridge \
  --manifest data/design/izu_parentage_bridge_template_20261010.json \
  --out /tmp/izu-parentage-bridge-status.json
pytest -q tests/test_izu_parentage_bridge.py
```

The empty template returns `NO_FIELD_OFFSPRING_DATA`. Invalid joins, missing named fathers, posterior sums not equal to 1, missing self/unknown probability categories, more sampled offspring than mature seeds, or an experimental seed classified as naturally open-pollinated cause **`INVALID_DATA_OR_LINKAGE`**. A valid *synthetic* fixture returns `SYNTHETIC_SCHEMA_CHECK_ONLY`, not empirical proof. If an externally supplied field-looking dataset passes these structural checks, the maximum result is **`STRUCTURALLY_LINKED_CLAIM_REQUIRES_EXTERNAL_VALIDATION`**, because this script does not authenticate permits, genotype bytes, algorithm calibration, sampling representativeness, or population-level causal inference.

**Critical status note:** The upstream legacy gate and R1b admission auditor reside under `legacy/`. They must actually be run on the raw field records, with **independent source-locked reports**, before extending their `plant_chain_rows` into this optional input. Never manufacture `admitted`, block completeness or valid paternity from a reported candidate occurrence.

## What is concretely still missing

1. Authoritative access/permit determinations and outcome-blind seasonal site/block admission. No site is currently admitted.
2. Field-collected same-block visitor/SVD/seed records; **no newly observed field data in this PR**.
3. Mother's and candidate fathers' genotypes and offspring genotypes; independent assignment model including unknown donor category and uncertainty.
4. Independent block replication and an outcome-blind precision/power gate before any claim that matching/service composition affects paternity.

These are external observations/permissions, not gaps that Model3 can legitimately fill. The frozen Chapter 2 simulation paper and PR #451 capacity companion are not reopened or relabeled as natural field evidence. Keep PR #452 **Draft**.
